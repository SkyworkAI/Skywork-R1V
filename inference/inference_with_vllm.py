import argparse
import os
from typing import List

from PIL import Image
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams


def initialize_environment() -> None:
    """Initialize environment variables for vLLM."""
    os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run inference with Skywork-R1V model using vLLM."
    )
    
    parser.add_argument(
        "--model_path",
        type=str,
        default="Skywork/Skywork-R1V-38B",
        help="Path to the model."
    )
    parser.add_argument(
        "--tensor_parallel_size",
        type=int,
        default=4,
        help="Number of GPUs for tensor parallelism."
    )
    
    parser.add_argument(
        "--image_paths",
        type=str,
        nargs="+",
        required=True,
        help="Path(s) to the image(s)."
    )
    parser.add_argument(
        "--question",
        type=str,
        required=True,
        help="Question to ask the model."
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0,
        help="Temperature for sampling (higher = more creative)."
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=64000,
        help="Maximum number of tokens to generate."
    )
    parser.add_argument(
        "--repetition_penalty",
        type=float,
        default=1.05,
        help="Penalty for repeated tokens (1.0 = no penalty)."
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=0.95,
        help="Top-p (nucleus) sampling probability."
    )
    
    return parser.parse_args()


def load_images(image_paths: List[str]) -> List[Image.Image]:
    """Load images from given paths."""
    return [Image.open(img_path) for img_path in image_paths]


def generate_response(
    llm: LLM,
    tokenizer: AutoTokenizer,
    question: str,
    images: List[Image.Image],
    sampling_params: SamplingParams
) -> str:
    """Generate response from the model."""
    messages = [{"role": "user", "content": question}]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    outputs = llm.generate(
        {
            "prompt": prompt,
            "multi_modal_data": {
                "image": images  
            },
        },
        sampling_params=sampling_params
    )
    
    return outputs[0].outputs[0].text


def main() -> None:
    """Main execution function."""
    initialize_environment()
    args = parse_arguments()
    
    # Initialize sampling parameters
    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        repetition_penalty=args.repetition_penalty
    )

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    llm = LLM(
        model=args.model_path,
        tensor_parallel_size=args.tensor_parallel_size,
        trust_remote_code=True,
        limit_mm_per_prompt={"image": 20},  # Support for multiple images
        gpu_memory_utilization=0.9
    )

    # Load images and prepare question
    images = load_images(args.image_paths)
    question = "<image>\n" * len(images) + args.question
    
    # Generate and print response
    response = generate_response(llm, tokenizer, question, images, sampling_params)
    print(f"User: {args.question}\nAssistant: {response}")


if __name__ == "__main__":
    main()