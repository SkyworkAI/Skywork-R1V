import argparse
import json
import os
import random
import time
from tqdm import tqdm
from io import BytesIO
import base64
from concurrent.futures import ThreadPoolExecutor
def pil_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

from datasets import load_dataset
from qwen_vl_utils import process_vision_info
from transformers import AutoProcessor
from vllm import LLM, SamplingParams
from openai import OpenAI
import random
# Openai setting
openai_api_key = "kunlun"
hostname = "xxx"
openai_api_base = f"http://{hostname}:8000/v1"
client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)


ds_collections = {
    "MMK12": {
        "root": "FanqingM/MMK12",
        "split": "test",
    }
}

SYSTEM_PROMPT_32B = "Solve the question. The user asks a question, and you solves it. You first thinks about the reasoning process in the mind and then provides the user with the answer. The answer is in latex format and wrapped in $...$. The final answer must be wrapped using the \\\\boxed{} command. Th answer should be enclosed within <answer> </answer> tags, i.e., Since $1+1=2$, so the answer is $2$. <answer> The answer is $\\\\boxed{2}$ </answer>, which means the final answer assistant's output should start with <answer> and end with </answer>."
SYSTEM_PROMPT_7B = "Solve the question. The user asks a question, and you solves it. You first thinks about the reasoning process in the mind and then provides the user with the answer. The answer is in latex format and wrapped in $...$. The final answer must be wrapped using the \\\\boxed{} command. The reasoning process and answer are enclosed within <think> </think> and <answer> </answer> tags, respectively, i.e., <think> Since $1+1=2$, so the answer is $2$. </think><answer> The answer is $\\\\boxed{2}$ </answer>, which means assistant's output should start with <think> and end with </answer>."


def vllm_inference(message):
    max_retries = 2
    retry_count = 0
    timeout_seconds = 600
    while retry_count < max_retries:
        try:
            chat_response = client.chat.completions.create(
                model="r1v3-alpha",
                max_tokens=16384,
                temperature=0.8,
                timeout=timeout_seconds,
                messages=message
            )
            return {
                "response": chat_response.choices[0].message.content,
                "completion_token": chat_response.usage.completion_tokens,
                "prompt_token": chat_response.usage.prompt_tokens,
            }
        except Exception as e:
            retry_count += 1
            print(f"Request failed (attempt {retry_count}/{max_retries}): {str(e)}")
            if retry_count >= max_retries:
                return {"response": f"Error after {max_retries} retries: {str(e)}", "reasoning_content": "", "completion_token": 0, "prompt_token": 0}
            timeout_seconds += 30

def evaluate_chat_model():
    random.seed(args.seed)

    for ds_name in args.datasets:
        data = load_dataset(ds_collections[ds_name]["root"], cache_dir=os.path.join(os.getcwd(), "data/MMK12/"))[
            ds_collections[ds_name]["split"]
        ]
        # data = data.select(range(5))
        results_file = "MMK12_0618_fast_thinking_all_2k.json"
        output_path = os.path.join(args.out_dir, results_file)
        if os.path.exists(output_path):
            with open(output_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            already_done_ids = set(existing_data.keys())
            print(f"Already evaluated {already_done_ids} samples.")
            print(f"Found {len(already_done_ids)} already evaluated samples.")
        else:
            existing_data = {}
            already_done_ids = set()

        messages = []
        data_to_process = []
        for data_item in tqdm(data, desc="Preparing messages"):
            if str(data_item["id"]) in already_done_ids:
                continue  # 已经完成的样本跳过
            data_item["query"] = data_item["question"]
            image = data_item["image"]

            message = [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": SYSTEM_PROMPT_32B},
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{pil_to_base64(image)}"}},
                        {"type": "text", "text": data_item["query"]},
                    ],
                },
            ]
            messages.append(message)
            data_to_process.append(data_item)

        if not messages:
            print(f"All samples already processed for {ds_name}.")
            continue

        # 并发执行
        with ThreadPoolExecutor(max_workers=256) as executor:
            model_outputs = list(tqdm(executor.map(vllm_inference, messages), total=len(messages), desc="Parallel inference"))

        # 把新推理结果更新进去
        for data_item, model_output in zip(data_to_process, model_outputs):
            del data_item["image"]
            data_item["response"] = model_output["response"]
            existing_data[str(data_item["id"])] = data_item
        
        json.dump(existing_data, open(output_path, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
        print(f"Results saved to {output_path}")

        cmd = f"python eval/mmk12/extract_calculate.py --output_file {results_file}"
        print(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", type=str, default="MMK12")
    parser.add_argument("--out-dir", type=str, default="results")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    args.datasets = args.datasets.split(",")

    print("datasets:", args.datasets)

    evaluate_chat_model()
