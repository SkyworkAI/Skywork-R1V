import openai
import os
import json
import time
import re
import pandas as pd
from tqdm import tqdm
from tenacity import retry, wait_random_exponential, stop_after_attempt

def rule_based_evaluation(item):
    prediction = str(item['prediction'])
    answer = str(item['answer']).strip()
    boxed_matches = re.findall(r'\\boxed\{(.*?)\}', prediction)
    if not boxed_matches:
        return False
    last_boxed = boxed_matches[-1].strip()

    def normalize(s):
        s = re.sub(r'\$|\\[a-z]+|\s+', '', s)
        s = re.sub(r'^\{|\}$', '', s)
        return s.lower()

    if last_boxed == answer or normalize(last_boxed) == normalize(answer):
        return True

    return False

def process_one(item):
    rule_match = rule_based_evaluation(item)
    if rule_match:
        item["is_correct"] = True
        item["score"] = 1
        return item
    if item.get('hit', 0) == 1:
        item["score"] = 1
    else:
        item["score"] = 0
    return item

def calculate_accuracy(jsonl_path):
    correct, total, original_hit, rule_matched = 0, 0, 0, 0
    single_total, single_acc = 0, 0

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if not str(data.get('id', '')).startswith('val'):
                continue

            total += 1

            if data.get('score')==1:
                correct += 1


    if total > 0:
        print(f"\nAccuracy Statistics:")
        print(f"- Total val examples: {total}")

        print(f"- Final correct count: {correct} ({(correct) / total * 100:.2f}%)")
    else:
        print("No valid data to evaluate.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Evaluate answer accuracy')
    parser.add_argument('--input', type=str, default='/path/to/MMMU_DEV_VAL_gpt4o_result.xlsx')
    parser.add_argument('--output', type=str, default='/path/to/result.jsonl')

    args = parser.parse_args()

    df = pd.read_excel(args.input)
    data = df.to_dict('records')

    with open(args.output, 'w', encoding='utf-8') as f_out:
        for item in tqdm(data):
            processed = process_one(item)
            f_out.write(json.dumps(processed, ensure_ascii=False) + '\n')
            f_out.flush()

    calculate_accuracy(args.output)
    print("Task completed. Results written to file.")
