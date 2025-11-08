#!/usr/bin/env python3
"""
Benchmark evaluation script for r1v4-deepresearch model.

Input: JSONL file with format:
{
    "image": "the path of the image",
    "question": "the question",
    "answer": "the answer"
}

Output: JSONL file with the same fields plus:
{
    ...(original fields),
    "r1v4_deepresearch_output": "model output"
}
"""

import os
import json
import argparse
import requests
import base64
from pathlib import Path
from typing import Dict, Any
from tqdm import tqdm
from mimetypes import guess_type

# Configuration - Please fill in your own values
SERVER_URL = ""  # TODO: Fill in your server URL
API_KEY = ""  # TODO: Fill in your API key
MODEL_NAME = "skywork/r1v4-deepresearch"

# Check required configuration
if not SERVER_URL or not API_KEY:
    raise ValueError("Please set SERVER_URL and API_KEY variables in the script")


def encode_image_to_base64(image_path: str) -> str:
    """Encode image file to base64 string."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def encode_image(image_path: str) -> str:
    """Convert image path to base64 encoded data URL."""
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = "image/jpeg"  # default
    return f"data:{mime_type};base64,{encode_image_to_base64(image_path)}"


def query(messages: list, max_tokens: int = 20480, temperature: float = 0.2) -> str:
    """
    Send request to the model API and get response.

    Args:
        messages: List of message dicts in OpenAI format
        max_tokens: Maximum tokens in response
        temperature: Sampling temperature

    Returns:
        Model output string
    """
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    if not SERVER_URL:
        raise ValueError("SERVER_URL is not set")

    try:
        response = requests.post(SERVER_URL, json=payload, headers=headers, timeout=300)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
        return f"ERROR: {str(e)}"


def create_messages(question: str, image_path: str | None = None) -> list:
    """
    Create messages in OpenAI format for the API request.

    Args:
        question: The question text
        image_path: Optional path to image file

    Returns:
        List of message dicts
    """
    content = []

    # Add image if provided
    if image_path is not None and os.path.exists(image_path):
        content.append(
            {"type": "image_url", "image_url": {"url": encode_image(image_path)}}
        )

    # Add question text
    content.append({"type": "text", "text": question})

    messages = [{"role": "user", "content": content}]

    return messages


def process_single_item(item: Dict[str, Any], base_dir: Path) -> Dict[str, Any]:
    """
    Process a single benchmark item.

    Args:
        item: Dict with 'image', 'question', 'answer' keys
        base_dir: Base directory for resolving relative image paths

    Returns:
        Original item dict with added 'r1v4_deepresearch_output' key
    """
    question = item.get("question", "")
    image_path = item.get("image", "")

    # Resolve image path (handle both absolute and relative paths)
    if image_path:
        image_path_obj = Path(image_path)
        if not image_path_obj.is_absolute():
            image_path = str(base_dir / image_path)

    # Create messages
    messages = create_messages(question, image_path if image_path else None)

    # Query model
    try:
        output = query(messages)
    except Exception as e:
        output = f"ERROR: {str(e)}"
        print(f"Error processing item: {e}")

    # Add output to item
    result = item.copy()
    result["r1v4_deepresearch_output"] = output

    return result


def main():
    """Main function to run benchmark evaluation."""
    parser = argparse.ArgumentParser(
        description="Benchmark evaluation script for r1v4-deepresearch model"
    )
    parser.add_argument(
        "--input", "-i", type=str, required=True, help="Path to input JSONL file"
    )
    parser.add_argument(
        "--output", "-o", type=str, required=True, help="Path to output JSONL file"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=20480,
        help="Maximum tokens in response (default: 20480)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature (default: 0.2)",
    )

    args = parser.parse_args()

    # Get input/output paths
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Get base directory for resolving relative image paths
    base_dir = input_path.parent

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Read input JSONL
    print(f"Reading input from: {input_path}")
    items = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))

    print(f"Total items to process: {len(items)}")

    # Process each item
    results = []
    with open(output_path, "w", encoding="utf-8") as f_out:
        for item in tqdm(items, desc="Processing"):
            result = process_single_item(item, base_dir)
            results.append(result)
            # Write result immediately (streaming output)
            f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
            f_out.flush()

    print(f"Results saved to: {output_path}")
    print(f"Processed {len(results)} items")


if __name__ == "__main__":
    main()
