import argparse
import json
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import openai
import regex
from openai import OpenAI

# Initialize client
client = OpenAI(
    api_key="xxx",
    base_url="xxx"
)


# Setup logging format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def query_gpt_judge(prompt, model="gpt-4o", max_tokens=256, retries=5):
    """Query the OpenAI model with prompt and return Yes/No."""
    messages = [{"role": "user", "content": prompt}]
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.5 * attempt,
                max_tokens=max_tokens
            )
            result = response.choices[0].message.content.strip()
            if result.lower() in {"yes", "no"}:
                return result
        except Exception as e:
            logging.warning(f"Request failed (attempt {attempt + 1}): {e}")
    return "no"

def create_comparison_prompt(data):
    """Build a prompt to compare model output and ground truth answer."""
    template = """
You are given a question, the correct answer, and a model's answer. Decide whether the model's answer matches the correct answer.

Ignore formatting differences such as LaTeX syntax, symbols, or wrappers (e.g., \boxed, $...$). Focus only on semantic or mathematical correctness.

If the model's answer is correct, respond with "Yes". Otherwise, respond with "No". Only output "Yes" or "No".

Question:
{question}
---
Correct Answer:
{answer}
---
Model Answer:
{model_response}
---
"""
    response = str(data["response"])
    # Try to extract answer from XML or boxed format
    match = re.search(r"<answer>(.*?)</answer>", response, re.DOTALL)
    if match:
        response = match.group(1).strip()
    else:
        boxed = regex.findall(r"\\boxed\{((?:[^{}]+|(?P<BRACES>\{(?:[^{}]+|(?P>BRACES))*\}))*?)\}", response, re.DOTALL)
        response = boxed[-1][0].strip() if boxed else response

    return template.format(
        question=data["question"],
        answer=data["answer"],
        model_response=response
    )

def evaluate_sample(problem):
    """Evaluate a single problem instance."""
    prompt = create_comparison_prompt(problem)
    logging.info(f"Evaluating ID: {problem['id']}")
    verdict = query_gpt_judge(prompt)
    return (verdict.lower() == "yes"), problem["id"]

def compute_accuracy(records):
    correct = sum(1 for item in records if item.get("score"))
    total = len(records)
    return {"correct": correct, "total": total, "accuracy": correct / total if total else 0.0}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, default="./results")
    parser.add_argument("--output_file", type=str, default="MMK12.json")
    parser.add_argument("--response_label", type=str, default="response")
    parser.add_argument("--number", type=int, default=-1)
    parser.add_argument("--output_label", type=str, default="extract")
    args = parser.parse_args()

    input_path = os.path.join(args.output_dir, args.output_file)
    print(f"Loading: {input_path}")
    with open(input_path, "r") as f:
        data = json.load(f)

    ids_to_process = list(data.keys())
    if args.number > 0:
        ids_to_process = ids_to_process[:args.number]

    print(f"Evaluating {len(ids_to_process)} samples...")
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = [
            executor.submit(evaluate_sample, data[sid]) for sid in ids_to_process
        ]
        for future in as_completed(futures):
            result, pid = future.result()
            data[pid]["score"] = result

    # Save annotated results
    output_path = input_path.replace(".json", f"_{args.output_label}.json")
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Detailed results saved to {output_path}")

    # Compute summary stats
    results_list = list(data.values())
    metrics = compute_accuracy(results_list)
    print(metrics)

    # Save accuracy
    score_path = input_path.replace(".json", "_score.json")
    with open(score_path, "w") as f:
        json.dump(metrics, f, indent=4, ensure_ascii=False)
    print(f"Accuracy summary saved to {score_path}")
