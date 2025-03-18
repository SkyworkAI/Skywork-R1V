import torch
from transformers import AutoModel, AutoTokenizer
from utils import load_image, split_model
# If you set `load_in_8bit=True`, you will need one 80GB GPUs.
# If you set `load_in_8bit=False`, you will need at least two 80GB GPUs.
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
# Prefix the question with <image>\n for each image.
pixel_values1 = load_image('./examples/image1.jpg', max_num=12).to(torch.bfloat16).cuda()
pixel_values2 = load_image('./examples/image2.jpg', max_num=12).to(torch.bfloat16).cuda()
pixel_values = torch.cat((pixel_values1, pixel_values2), dim=0)
num_patches_list = [pixel_values1.size(0), pixel_values2.size(0)]
question = '<image>\n<image>\nSelect the correct option from this question.'
response, history = model.chat(tokenizer, pixel_values, question, generation_config,
                               num_patches_list=num_patches_list,
                               history=None, return_history=True)
print(f'User: {question}\nAssistant: {response}')