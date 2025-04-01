from vllm import LLM, SamplingParams
import PIL
import os
import argparse

os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Run inference with Skywork-R1V model using vLLM.")
    # Model configuration
    parser.add_argument('--model_path', type=str, default='Skywork/Skywork-R1V-38B', 
                       help="Path to the model.")
    parser.add_argument('--tensor_parallel_size', type=int, default=4, 
                       help="Number of GPUs for tensor parallelism.")
    
    # Input parameters
    parser.add_argument('--image_paths', type=str, nargs='+', required=True, 
                       help="Path(s) to the image(s).")
    parser.add_argument('--question', type=str, required=True, 
                       help="Question to ask the model.")
    
    # Generation parameters
    parser.add_argument('--temperature', type=float, default=0,
                       help="Temperature for sampling (higher = more creative).")
    parser.add_argument('--max_tokens', type=int, default=64000,
                       help="Maximum number of tokens to generate.")
    parser.add_argument('--repetition_penalty', type=float, default=1.05,
                       help="Penalty for repeated tokens (1.0 = no penalty).")
    parser.add_argument('--top_p', type=float, default=0.95,
                       help="Top-p (nucleus) sampling probability.")
    
    args = parser.parse_args()

    # 初始化采样参数
    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        repetition_penalty=args.repetition_penalty
    )

    # 初始化LLM
    llm = LLM(
        model=args.model_path,
        tensor_parallel_size=args.tensor_parallel_size,
        trust_remote_code=True,
        limit_mm_per_prompt={"image": 20},
        gpu_memory_utilization=0.9
    )

    # 准备图像输入
    images = [PIL.Image.open(img_path) for img_path in args.image_paths]
    
    # 构建prompt - 为每张图片添加<image>标记
    question = "<image>\n" * len(images) + args.question 
    prompt = f"<｜begin▁of▁sentence｜><｜User｜>\n{question}<｜Assistant｜><think>\n"

    # 执行推理 - 支持多图输入
    outputs = llm.generate(
        {
            "prompt": prompt,
            "multi_modal_data": {
                "image": images  # 传入所有图片的列表
            },
        },
        sampling_params=sampling_params
    )

    # 获取生成结果
    response = outputs[0].outputs[0].text
    
    # 输出结果
    print(f'User: {args.question}\nAssistant: {response}')

if __name__ == '__main__':
    main()