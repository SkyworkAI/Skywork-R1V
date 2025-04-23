import argparse
from typing import List, Union

from PIL import Image
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for model inference.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Run inference with Skywork-R1V series model using vLLM."
    )
    
    # Model configuration
    parser.add_argument(
        "--model_path",
        type=str,
        default="Skywork/Skywork-R1V2-38B",
        help="Path to the model"
    )
    parser.add_argument(
        "--tensor_parallel_size",
        type=int,
        default=4,
        help="Number of GPUs for tensor parallelism"
    )
    
    # Input parameters
    parser.add_argument(
        "--image_paths",
        type=str,
        nargs="+",
        required=True,
        help="Path(s) to the input image(s)"
    )
    parser.add_argument(
        "--question",
        type=str,
        required=True,
        help="Question to ask the model"
    )
    
    # Generation parameters
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Temperature for sampling (higher = more creative)"
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=8000,
        help="Maximum number of tokens to generate"
    )
    parser.add_argument(
        "--repetition_penalty",
        type=float,
        default=1.05,
        help="Penalty for repeated tokens (1.0 = no penalty)"
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=0.95,
        help="Top-p (nucleus) sampling probability"
    )
    
    return parser.parse_args()


def load_images(image_paths: List[str]) -> Union[Image.Image, List[Image.Image]]:
    """Load images from given paths.
    
    Args:
        image_paths: List of image file paths
        
    Returns:
        Single image if one path provided, else list of images
    """
    images = [Image.open(img_path) for img_path in image_paths]
    return images[0] if len(images) == 1 else images


def prepare_question(question: str, num_images: int) -> str:
    """Format the question with appropriate image tags.
    
    Args:
        question: Original question string
        num_images: Number of images being processed
        
    Returns:
        Formatted question string
    """
    if not question.startswith("<image>\n"):
        return "<image>\n" * num_images + question
    return question


def initialize_model(args: argparse.Namespace) -> tuple[LLM, AutoTokenizer]:
    """Initialize the LLM model and tokenizer.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Tuple of (LLM instance, tokenizer)
    """
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    
    llm = LLM(
        model=args.model_path,
        tensor_parallel_size=args.tensor_parallel_size,
        trust_remote_code=True,
        limit_mm_per_prompt={"image": 20},
        gpu_memory_utilization=0.7,
    )
    
    return llm, tokenizer


def generate_response(
    llm: LLM,
    tokenizer: AutoTokenizer,
    question: str,
    images: Union[Image.Image, List[Image.Image]],
    sampling_params: SamplingParams
) -> str:
    """Generate response from the model.
    
    Args:
        llm: Initialized LLM instance
        tokenizer: Initialized tokenizer
        question: Formatted question string
        images: Input image(s)
        sampling_params: Generation parameters
        
    Returns:
        Generated response text
    """
    messages = [{"role": "user", "content": question}]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    outputs = llm.generate(
        {
            "prompt": prompt,
            "multi_modal_data": {"image": images},
        },
        sampling_params=sampling_params
    )
    
    return outputs[0].outputs[0].text


def main() -> None:
    """Main execution function."""
    args = parse_arguments()
    
    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        repetition_penalty=args.repetition_penalty,
    )
    
    llm, tokenizer = initialize_model(args)
    images = load_images(args.image_paths)
    question = prepare_question(args.question, len(args.image_paths))
    
    response = generate_response(llm, tokenizer, question, images, sampling_params)
    print(f"User: {args.question}\nAssistant: {response}")


if __name__ == "__main__":
    main()