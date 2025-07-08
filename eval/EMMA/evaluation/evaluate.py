import argparse
import json
import logging
import os
from tqdm import tqdm
from utils import *
import re
import time


def fast_extract_answer(response) :
    response = response.strip()
    # Direct Strategy Multi-Choice
    # A / A: / A.
    for ch in 'ABCDEFGH':
        if response.upper() == ch or response.startswith(f'{ch}:') or response.startswith(f'{ch}.'):
            return ch

    # Direct Strategy Open-ended
    # 1
    if is_number(response):
        return response

    # CoT strategy
    if 'boxed{' in response:
        try:
            model_answers = extract_full_boxed_content(response)
            if model_answers:
                # for coding
                # \\boxed{\\text{}}
                try:
                    text_content = re.findall(r'\\text{(.*?)}', model_answers[-1])
                    if text_content:
                        return text_content[-1].strip()
                except Exception:
                    pass
                return model_answers[-1].strip()
        except Exception:
            pass

    # for Coding
    # the correct answer is\n D.
    for flag in ['final answer is', 'correct answer is', 'answer should be', 'answer is', 'answer:']:
        if flag in response.lower():
            try:
                model_answer = response.lower().split(flag)[-1].strip()
                return model_answer.split('\n')[0].split('.')[0]
            except Exception:
                pass

    return ""


def create_test_prompt(score_prompt, problem, label):
    score_prompt = score_prompt.strip()
    response = problem[label]
    answer = problem['answer']
    full_prompt = f'{score_prompt}\n' + f'Response: {response}\n' + f'Answer: {answer}\n' + 'Correct_or_not:'
    return full_prompt


def call_gpt(client, model, user_prompt):
    attempt = 0
    while attempt < 5:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")

            if 'error' in str(e) and 'message' in str(e):
                error_message = str(e)
                if 'The server had an error processing your request.' in error_message:
                    sleep_time = 30
                    logging.error(f"Server error, retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                elif 'Please try again in ' in error_message:
                    sleep_time = float(error_message.split('Please try again in ')[1].split('s.')[0])
                    logging.error(f"Rate limit exceeded, retrying in {sleep_time * 2}s...")
                    time.sleep(sleep_time * 2)
                else:
                    print("Unknown error, skipping this request.")
                    break
            attempt += 1


def gen_true_false(answer_file, args):
    logging.info(f"Reading {answer_file}.....")
    label = args.response_label
    if args.gpt_eval:
        from openai import OpenAI
        client = OpenAI(api_key=args.api_key)
    with open(answer_file, "r") as f:
        results = json.load(f)
    full_pids = list(results.keys())

    skip_pids = []
    for pid, problem in results.items():
        flag = problem.get('true_false')
        if flag is not None:
            skip_pids.append(problem['pid'])

    if args.rerun:
        test_pids = full_pids
    else:
        if len(skip_pids) > 0:
            logging.info(
                f"Found existing results file with {len(skip_pids)} problems with valid responses. Skipping these problems..."
            )
        test_pids = [pid for pid in full_pids if pid not in skip_pids]

    logging.info(f"Number of test problems to run: {len(test_pids)}")

    for i, pid in enumerate(tqdm(test_pids)):
        problem = results[pid]
        flag = False
        if label not in problem or not problem[label]:
            results[pid]['extraction'] = None
            results[pid]['true_false'] = False
            continue

        if args.gpt_eval:
            user_prompt = create_test_prompt(score_demo_prompt, problem, label)
            flag_cache = call_gpt(client, args.model, user_prompt)
            results[pid]['gpt_eval'] = flag_cache
            if flag_cache.lower() == 'correct':
                flag = True
            else:
                flag = False
        else:
            model_answer = fast_extract_answer(problem[label])
            results[pid]['extraction'] = model_answer
            if is_equal(model_answer, results[pid]['answer']) or is_equal(model_answer, results[pid]['gt_content']):
                flag = True

        results[pid]['true_false'] = flag

        if (i % args.save_every == 0 and i > 0) or i == len(test_pids) - 1:
            with open(answer_file, "w") as f:
                f.write(json.dumps(results, indent=2))
            logging.info(f"Saved results to {answer_file}")

    with open(answer_file, "w") as f:
        f.write(json.dumps(results, indent=2))
    logging.info(f"Saved results to {answer_file}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--results_dir', type=str, default='/mnt/datasets_vlm/yunzhuo.hao/benchmarks/EMMA/results/EMMA-mini/open-source')
    parser.add_argument('--response_label', type=str, default='response', help='response label for the input file')
    parser.add_argument('--rerun', action='store_true', help='rerun the answer extraction')
    parser.add_argument('--save_every', type=int, default=10, help='save every n problems')

    parser.add_argument('--gpt_eval', action='store_true', help='use gpt to evaluate')
    parser.add_argument('--api_key', type=str, default="")
    parser.add_argument('--model', type=str, default="chatgpt-4o-latest")

    args = parser.parse_args()

    logging.info("Starting to extract answers.......")
    
    for root, dirs, files in os.walk(args.results_dir):
        for file in files:
            if file.endswith(".json") and not file.endswith("_result.json"):
                gen_true_false(os.path.join(root, file), args)

    
if __name__ == "__main__":
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO").upper(),
        format="[%(name)s] %(message)s",
        datefmt="[%X]"
    )
    logger_blocklist = [
        "asyncio",
        "azure",
        "azureml",
        "datasets",
        "httpx",
        "httpcore",
        "filelock",
        "fsspec",
        "msal",
        "msrest",
        "openai",
        "PIL",
        "urllib3",
    ]
    for module in logger_blocklist:
        logging.getLogger(module).setLevel(logging.WARNING)

    main()