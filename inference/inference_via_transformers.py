from transformers import AutoTokenizer, AutoConfig, AutoModel, CLIPImageProcessor
from utils_ import split_model, load_image
import sys, os
import torch
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))


path = 'Skywork/Skywork-R1V-38B'
# path = '/mnt/datasets_vlm/yi.peng/internvl_vlm/internvl_chat/work_dirs/skywork_r1v'
path = "/mnt/datasets_vlm/yi.peng/tmp/DeepSeek-R1-Distill-Qwen-38B-combine"
image_path = '/mnt/datasets_vlm/multimodal_data/SFT/gaokao/images/GAOKAO_V/Physics/Physics_2024_1/e06d7516840dff604767c6a72dcd3e2c194b3fca89dff1c746d155a98f5403be.jpg'


device_map, visible_devices = split_model(path)
tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True, use_fast=False)
model = AutoModel.from_pretrained(
    path,
    torch_dtype=torch.bfloat16,
    load_in_8bit=False,
    low_cpu_mem_usage=True,
    use_flash_attn=True,
    trust_remote_code=True,
    device_map=device_map).eval()
    
generation_config = dict(max_new_tokens=64000, do_sample=True, temperature=0.6, top_p=0.95, repetition_penalty=1.05)

image_path = "/path/to/image"
pixel_values = load_image(image_path, max_num=12).to(torch.bfloat16).cuda()

# pure-text conversation (纯文本对话)
question = 'If all cats can fly, and Tom is a cat, can Tom fly?'
response = model.chat(tokenizer, None, question, generation_config, history=None)
print(f'User: {question}\nAssistant: {response}')

# single-image single-round conversation (单图单轮对话)
question = '<image>\nSelect the correct option from this question.'
response = model.chat(tokenizer, pixel_values, question, generation_config)
print(f'User: {question}\nAssistant: {response}')

# single-image multi-round conversation (单图多轮对话)
question = '<image>\nSelect the correct option from this question.'
response, history = model.chat(tokenizer, pixel_values, question, generation_config, history=None, return_history=True)
print(f'User: {question}\nAssistant: {response}')

question = 'What if the height in the question is changed to 0.5?'
response, history = model.chat(tokenizer, pixel_values, question, generation_config, history=history, return_history=True)
print(f'User: {question}\nAssistant: {response}')

# multi-image multi-round conversation, separate images (多图多轮对话，独立图像)
pixel_values1 = load_image('./examples/image1.jpg', max_num=12).to(torch.bfloat16).cuda()
pixel_values2 = load_image('./examples/image2.jpg', max_num=12).to(torch.bfloat16).cuda()
pixel_values = torch.cat((pixel_values1, pixel_values2), dim=0)
num_patches_list = [pixel_values1.size(0), pixel_values2.size(0)]

question = '<image>\n<image>\nSelect the correct option from this question.'
response, history = model.chat(tokenizer, pixel_values, question, generation_config,
                               num_patches_list=num_patches_list,
                               history=None, return_history=True)
print(f'User: {question}\nAssistant: {response}')

question = 'What if the height in the question is changed to 0.5?'
response, history = model.chat(tokenizer, pixel_values, question, generation_config,
                               num_patches_list=num_patches_list,
                               history=history, return_history=True)
print(f'User: {question}\nAssistant: {response}')