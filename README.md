<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

# Skywork-R1V：Bridging Vision and Language for Advanced Multimodal Reasoning

<div align="center">
  <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/logo.jpeg" width="60%" alt="skywork-r1v" />
</div>

<font size=7><div align='center' > [[📖Technical Report]([https://github.com/SkyworkAI/Skywork-R1V/blob/main/Skywork_R1V.pdf])</div></font>

## Table of Contents

1. [Introduction](#1-introduction)
2. [Model Summary](#2-model-summary)
3. [Model Downloads](#3-model-downloads)
4. [Evaluation Results](#4-evaluation-results)
5. [How to Run Locally](#5-how-to-run-locally)
6. [License](#6-license)
7. [Citation](#7-citation)

## 1. Introduction

We introduce Skywork-R1V, a multimodal reasoning model that extends the R1-series text models to visual modalities through a near-lossless transfer method. Using a lightweight visual projector, Skywork-R1V enables seamless multimodal adaptation without requiring retraining of either the base language model or vision encoder. To enhance visual-text alignment, we developed a hybrid optimization strategy combining Iterative Supervised Fine-Tuning (SFT) with Group Relative Policy Optimization (GRPO), significantly improving cross-modal integration. Additionally, we created an adaptive-length Chain-of-Thought distillation approach for generating reasoning data, which dynamically optimizes reasoning chain lengths to improve inference efficiency and prevent overthinking. The model achieves good performance on key multimodal reasoning benchmarks, scoring 69.0 on MMMU and 67.5 on MathVista, comparable to leading closed-source models like Gemini 2.0 and Kimi-k1.5. It also maintains strong textual reasoning capabilities, achieving impressive scores of 72.0 on AIME and 94.0 on MATH500. 

## 2. Model Summary

****Architecture:**** 

Skywork-R1V employs a modular architecture that efficiently combines vision and language capabilities:

- Vision Encoder: Uses Vision Transformer (ViT) as the visual backbone to process image inputs.
- Visual Projector: A lightweight MLP (multilayer perceptron) adapter that serves as the bridge between the vision and language components.
- Language Model: Utilizes R1-distilled-Qwen-32B as the reasoning-capable language model backbone.

The model follows a connection pattern of Vision Encoder → MLP Adapter → Language Model, where the MLP adapter aligns the output space of the vision encoder with the input space of the language model. This design allows for efficient transfer of reasoning capabilities from text to multimodal domains without requiring extensive retraining of either the vision encoder or language model.

 ****Methodology****

_Efficient Multimodal Transfer of Reasoning-Capable LLMs：_
A staged alignment approach that efficiently transfers reasoning capabilities from text to vision by first connecting a vision encoder to a substitute LLM before transferring to the reasoning-capable LLM, preserving reasoning abilities while minimizing data requirements.
- The MLP adapter is first trained to align the ViT with a substitute LLM (Qwen-32B-Instruct) using 2M samples of SFT data, while keeping both the vision encoder and language model frozen.
- The trained MLP is then transferred to connect the ViT with the reasoning-capable LLM (R1-distilled-Qwen-32B).
- Fine-tuning only the MLP parameters while keeping the vision encoder and language model frozen, ensuring preservation of reasoning capabilities while effectively aligning visual and textual representations.

_Hybrid Optimization Framework：_
A multi-stage training strategy combining iterative supervised fine-tuning with reinforcement learning that progressively improves model performance through error correction and reward-based optimization.
- Initial supervised fine-tuning (SFT) using the complete dataset.
- Iterative training with customized data. A reward model evaluates data quality and selects high-scoring samples. 
- Reinforcement learning using Group Relative Policy Optimization (GRPO) with a rule-based reward system (accuracy and format rewards) to enhance generalizability.

_Adaptive-Length Chain-of-Thought Distillation:_ 
The model uses Adaptive-Length Chain-of-Thought Distillation (AL-CoTD) to generate high-quality reasoning-oriented training data
- Evaluates image-text pairs through vision and text scoring.
- Determines required depth of cross-modal integration.
- Adaptively regulates reasoning chain length based on query complexity.
- Progressive refinement of reasoning processes with external evaluation and correction when needed.

## 3. Model Downloads

<div align="center">

| **Model** | **#Total Params** | **Download** |
| :------------: | :------------: | :------------: |
| skywork-r1v | 38B | [🤗 Hugging Face](https://huggingface.co/Skywork/Skywork-R1V-38B)   |

</div>

## 4. Evaluation Results
<div align="center">
  <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/eval.jpeg" width="80%" alt="skywork_r1v_eval" />
</div>

<div align="center">
  <b>Evaluation results of state-of-the-art LLMs and VLMs</b>
</div>
<table>
  <thead>
    <tr>
      <th></th>
      <th align="center"><strong>Vision</strong></th>
      <th align="center" colspan="3"><strong>Reasoning</strong></th>
      <th align="center" colspan="3"><strong>Vision</strong></th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th align="center"><strong>MATH-500</strong></th>
      <th align="center"><strong>AIME 2024</strong></th>
      <th align="center"><strong>GPQA</strong></th>
      <th align="center"><strong>MathVista(mini)</strong></th>
      <th align="center"><strong>MMMU(Val)</strong></th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th align="center">pass@1</th>
      <th align="center">pass@1</th>
      <th align="center">pass@1</th>
      <th align="center">pass@1</th>
      <th align="center">pass@1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Qwen2.5-72B-Instruct</td>
      <td align="center">❌</td>
      <td align="center">80.0</td>
      <td align="center">23.3</td>
      <td align="center">49.0</td>
      <td align="center">-</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Deepseek V3</td>
      <td align="center">❌</td>
      <td align="center">90.2</td>
      <td align="center">39.2</td>
      <td align="center">59.1</td>
      <td align="center">-</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Deepseek R1</td>
      <td align="center">❌</td>
      <td align="center">97.3</td>
      <td align="center">79.8</td>
      <td align="center">71.5</td>
      <td align="center">-</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Claude 3.5 Sonnet</td>
      <td align="center">✅</td>
      <td align="center">78.3</td>
      <td align="center">16.0</td>
      <td align="center">65.0</td>
      <td align="center">65.3</td>
      <td align="center">66.4</td>
    </tr>
    <tr>
      <td>GPT-4o</td>
      <td align="center">✅</td>
      <td align="center">74.6</td>
      <td align="center">9.3</td>
      <td align="center">49.9</td>
      <td align="center">63.8</td>
      <td align="center">69.1</td>
    </tr>
    <tr>
      <td>Kimi k1.5</td>
      <td align="center">✅</td>
      <td align="center">96.2</td>
      <td align="center">77.5</td>
      <td align="center">-</td>
      <td align="center">74.9</td>
      <td align="center">70.0</td>
    </tr>
    <tr>
      <td>Qwen2.5-VL-72B-Instruct</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">74.8</td>
      <td align="center">70.2</td>
    </tr>
    <tr>
      <td>LLaVA-Onevision-72B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">67.5</td>
      <td align="center">56.8</td>
    </tr>
    <tr>
      <td>InternVL2-Llama3-76B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">65.5</td>
      <td align="center">62.7</td>
    </tr>
    <tr>
      <td>InternVL2.5-78B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">72.3</td>
      <td align="center">70.1</td>
    </tr>
    <tr>
      <td>Skywork-R1V-38B</td>
      <td align="center">✅</td>
      <td align="center">94.0</td>
      <td align="center">72.0</td>
      <td align="center">61.6</td>
      <td align="center">67.5</td>
      <td align="center">69.0</td>
    </tr>
  </tbody>
</table>

<div align="center">
  <b>Comparison with Larger-Scale Open-Source and Closed-Source Models</b>
</div>

<table align="center">
  <thead>
    <tr>
      <th></th>
      <th align="center"><strong>Benchmark</strong></th>
      <th align="center"><strong>LLM</strong></th>
      <th align="center" colspan="4"><strong>VLM</strong></th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th align="center"><strong>QwQ-32B-Preview</strong></th>
      <th align="center"><strong>InternVL-2.5-38B</strong></th>
      <th align="center"><strong>VILA 1.5-40B</strong></th>
      <th align="center"><strong>InternVL2-40B</strong></th>
      <th align="center"><strong>Skywork-R1V-38B</strong></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3">Reasoning</td>
      <td>MATH-500</td>
      <td align="center">90.6</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center"><strong>94.0</strong></td>
    </tr>
    <tr>
      <td>AIME 2024</td>
      <td align="center">50.0</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center"><strong>72.0</strong></td>
    </tr>
    <tr>
      <td>GPQA</td>
      <td align="center">54.5</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center"><strong>61.6</strong></td>
    </tr>
    <tr>
      <td rowspan="3">Vision</td>
      <td>MathVista(mini)</td>
      <td align="center">-</td>
      <td align="center">71.9</td>
      <td align="center">49.5</td>
      <td align="center">63.7</td>
      <td align="center">67.5</td>
    </tr>
    <tr>
      <td>MMMU(Val)</td>
      <td align="center">-</td>
      <td align="center">63.9</td>
      <td align="center">55.1</td>
      <td align="center">55.2</td>
      <td align="center"><strong>69.0</strong></td>
    </tr>
  </tbody>
</table>


## 5. How to Run Locally

```python
import math
import torch
import torchvision.transforms as T
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from transformers import AutoConfig, AutoModel, AutoTokenizer

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform

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

def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images

def load_image(image_file, input_size=448, max_num=12):
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values

def split_model(model_path):
    device_map = {}
    world_size = torch.cuda.device_count()
    config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
    num_layers = config.llm_config.num_hidden_layers
    num_layers_per_gpu = math.ceil(num_layers / (world_size - 0.5))
    num_layers_per_gpu = [num_layers_per_gpu] * world_size
    num_layers_per_gpu[0] = math.ceil(num_layers_per_gpu[0] * 0.5)
    layer_cnt = 0
    for i, num_layer in enumerate(num_layers_per_gpu):
        for j in range(num_layer):
            device_map[f'language_model.model.layers.{layer_cnt}'] = i
            layer_cnt += 1
    device_map['vision_model'] = 0
    device_map['mlp1'] = 0
    device_map['language_model.model.tok_embeddings'] = 0
    device_map['language_model.model.embed_tokens'] = 0
    device_map['language_model.output'] = 0
    device_map['language_model.model.norm'] = 0
    device_map['language_model.model.rotary_emb'] = 0
    device_map['language_model.lm_head'] = 0
    device_map[f'language_model.model.layers.{num_layers - 1}'] = 0
    return device_map

path = 'Skywork/Skywork-R1V-38B'
device_map = split_model(path)
model = AutoModel.from_pretrained(
    path,
    torch_dtype=torch.bfloat16,
    load_in_8bit=False,
    low_cpu_mem_usage=True,
    use_flash_attn=True,
    trust_remote_code=True,
    device_map=device_map).eval()
tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True, use_fast=False)
generation_config = dict(max_new_tokens=64000, do_sample=True, temperature=0.6, top_p=0.95, repetition_penalty=1.05)

# single-image conversation
pixel_values = load_image('./examples/image1.jpg', max_num=12).to(torch.bfloat16).cuda()
question = '<image>\nSelect the correct option from this question.'
response = model.chat(tokenizer, pixel_values, question, generation_config)
print(f'User: {question}\nAssistant: {response}')

# multi-image conversation 
pixel_values1 = load_image('./examples/image1.jpg', max_num=12).to(torch.bfloat16).cuda()
pixel_values2 = load_image('./examples/image2.jpg', max_num=12).to(torch.bfloat16).cuda()
pixel_values = torch.cat((pixel_values1, pixel_values2), dim=0)
num_patches_list = [pixel_values1.size(0), pixel_values2.size(0)]
question = '<image>\n<image>\nSelect the correct option from this question.'
response, history = model.chat(tokenizer, pixel_values, question, generation_config,
                               num_patches_list=num_patches_list,
                               history=None, return_history=True)
print(f'User: {question}\nAssistant: {response}')
```

## 6. License
This code repository is licensed under [the MIT License](LICENSE-CODE). 
✅ Commercial use permitted

✅ Modification allowed

✅ Distribution allowed

❌ No liability


## 7. Citation
If you use Skywork-R1V in your research, please cite:

```
@article{skywork2025r1v,
  title     = {Skywork R1V: Bridging Vision and Language for Advanced Multimodal Reasoning},
  author    = {Yi Peng, Chris, Xiaokun Wang, Yichen Wei, Jiangbo Pei, Weijie Qiu, Ai Jian, Yunzhuo Hao, Jiachun Pan, Tianyidan Xie, Li Ge, Rongxian Zhuang, Xuchen Song, Yang Liu, Yahui Zhou},
  year      = {2025},
  journal   = {https://github.com/SkyworkAI/Skywork-R1V/blob/main/Skywork_R1V.pdf},
  url       = {https://huggingface.co/Skywork/Skywork-R1V-38B}
}
```
