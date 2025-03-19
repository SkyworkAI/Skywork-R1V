import torch
from transformers import AutoModel, AutoTokenizer
from utils import load_image, split_model
import argparse

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Run inference with Skywork-R1V model.")
    parser.add_argument('--model_path', type=str, default='Skywork/Skywork-R1V-38B', help="Path to the model.")
    parser.add_argument('--image_paths', type=str, nargs='+', required=True, help="Path(s) to the image(s).")
    parser.add_argument('--question', type=str, required=True, help="Question to ask the model.")
    args = parser.parse_args()

    device_map = split_model(args.model_path)
    model = AutoModel.from_pretrained(
        args.model_path,
        torch_dtype=torch.bfloat16,
        load_in_8bit=False,
        low_cpu_mem_usage=True,
        use_flash_attn=True,
        trust_remote_code=True,
        device_map=device_map
    ).eval()
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True, use_fast=False)

    pixel_values = [load_image(img_path, max_num=12).to(torch.bfloat16).cuda() for img_path in args.image_paths]
    if len(pixel_values) > 1:
        pixel_values = torch.cat(pixel_values, dim=0)
        num_patches_list = [img.size(0) for img in pixel_values]
    else:
        pixel_values = pixel_values[0]
        num_patches_list = None
        
    prompt = "<image>\n"*len(args.image_paths) + args.question
    generation_config = dict(max_new_tokens=64000, do_sample=True, temperature=0.6, top_p=0.95, repetition_penalty=1.05)
    response = model.chat(tokenizer, pixel_values, prompt, generation_config, num_patches_list=num_patches_list)

    print(f'User: {args.question}\nAssistant: {response}')

if __name__ == '__main__':
    main()