import os
import math
import numpy as np
import torch
import torch.distributed as dist
import torchvision.transforms as T
from decord import VideoReader, cpu
from PIL import Image
from transformers import AutoConfig
from torchvision.transforms.functional import InterpolationMode


IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def load_image(image_file, input_size=448, max_num=12, upscale=False):
    image = Image.open(image_file).convert('RGB')
    if upscale:
        image = image.resize((image.width * 2, image.height * 2), Image.BILINEAR)
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values

def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform

def get_rank_and_world_size():
    rank = int(os.environ.get('RANK', 0))
    world_size = int(os.environ.get('WORLD_SIZE', 1))
    return rank, world_size

def get_local_rank_and_local_world_size():
    if not dist.is_available():
        return 0, 1
    if not dist.is_initialized():
        return 0, 1

    if 'SLURM_LOCALID' in os.environ:
        local_rank = int(os.environ['SLURM_LOCALID'])
        local_world_size = int(os.environ['SLURM_NTASKS_PER_NODE'])
        return local_rank, local_world_size

    if 'LOCAL_RANK' in os.environ and 'LOCAL_WORLD_SIZE' in os.environ:
        return int(os.environ['LOCAL_RANK']), int(os.environ['LOCAL_WORLD_SIZE'])

    raise NotImplementedError(
        "Fail to get local_rank and local_world_size! "
        "Please ensure that you set the environment variable "
        "`LOCAL_RANK` and `LOCAL_WORLD_SIZE`"
    )

def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio


def dynamic_preprocess(image, min_num=1, max_num=6, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # calculate the existing image aspect ratio
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # find the closest aspect ratio to the target
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # calculate the target width and height
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # resize the image
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images

def split_model(model_path):
    num_gpus_per_node = torch.cuda.device_count()
    rank, world_size = get_rank_and_world_size()
    try:
        local_rank, local_world_size = get_local_rank_and_local_world_size()
    except:
        local_rank = rank

    if 'GPUS_PER_PROCESS' in os.environ:
        gpus_per_process = int(os.environ['GPUS_PER_PROCESS'])
    else:
        gpus_per_process = 8  # default to use 8 GPUs for one model
    gpus_per_process = min(gpus_per_process, num_gpus_per_node // local_world_size)
    start_gpu = local_rank * gpus_per_process
    end_gpu = start_gpu + gpus_per_process

    assert end_gpu <= num_gpus_per_node, f"Process {local_rank} tries to access GPU {end_gpu}, " \
                                         f"but only {num_gpus_per_node} GPUs are available per node."

    visible_devices = list(range(start_gpu, end_gpu))

    device_map = {}
    config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)

    num_gpus_for_vit = 0.5
    num_layers = config.llm_config.num_hidden_layers
    num_layers_per_gpu = math.ceil(num_layers / (len(visible_devices) - num_gpus_for_vit))
    num_layers_per_gpu = [num_layers_per_gpu] * len(visible_devices)
    num_layers_per_gpu[0] = math.ceil(num_layers_per_gpu[0] * 0.5)

    layer_cnt = 0
    for i, num_layer in enumerate(num_layers_per_gpu):
        for j in range(num_layer):
            device_map[f'language_model.model.layers.{layer_cnt}'] = visible_devices[i]
            layer_cnt += 1
    device_map['vision_model'] = visible_devices[0]
    device_map['mlp1'] = visible_devices[0]
    device_map['language_model.model.tok_embeddings'] = visible_devices[0]
    device_map['language_model.model.embed_tokens'] = visible_devices[0]
    device_map['language_model.output'] = visible_devices[0]
    device_map['language_model.model.norm'] = visible_devices[0]
    device_map['language_model.model.rotary_emb'] = visible_devices[0]
    device_map['language_model.lm_head'] = visible_devices[0]
    device_map[f'language_model.model.layers.{num_layers - 1}'] = visible_devices[0]

    return device_map, visible_devices

