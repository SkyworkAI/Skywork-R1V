import json
import openai
import argparse
import datasets
import re
import numpy as np
import math

judger = "o3-mini"  # 评测模型
judge_process = 16  # 并行进程数（HF datasets map 多进程）

# Configuration - Please fill in your own values
BASE_URL = ""  # TODO: Fill in your OpenAI endpoint
API_KEY = ""  # TODO: Fill in your API key

JUDGE_PROMPT = """
Judge whether the following [response] to [question] is correct or not based on the precise and unambiguous [correct_answer] below.

[question]: {question}

[response]: {response}

[correct_answer]: {correct_answer}

Your judgement must be in the format and criteria specified below:

reasoning: Explain why the extracted_final_answer is correct or incorrect based on [correct_answer], focusing only on if there are meaningful differences between [correct_answer] and the extracted_final_answer. Do not comment on any background to the problem, do not attempt to solve the problem, do not argue for any answer different than [correct_answer], focus only on whether the answers match.

correct: Answer 'yes' if extracted_final_answer matches the [correct_answer] given above, or is within a small margin of error for numerical problems. Answer 'no' otherwise, i.e. if there is any inconsistency, ambiguity, non-equivalency, or if the extracted answer is incorrect.

""".strip()

client = openai.OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)


# source: https://github.com/hendrycks/outlier-exposure/blob/master/utils/calibration_tools.py
def calib_err(confidence, correct, p="2", beta=100):
    # beta is target bin size
    idxs = np.argsort(confidence)
    confidence = confidence[idxs]
    correct = correct[idxs]
    bins = [[i * beta, (i + 1) * beta] for i in range(len(confidence) // beta)]
    bins[-1] = [bins[-1][0], len(confidence)]

    cerr = 0
    total_examples = len(confidence)
    for i in range(len(bins) - 1):
        bin_confidence = confidence[bins[i][0] : bins[i][1]]
        bin_correct = correct[bins[i][0] : bins[i][1]]
        num_examples_in_bin = len(bin_confidence)

        if num_examples_in_bin > 0:
            difference = np.abs(np.nanmean(bin_confidence) - np.nanmean(bin_correct))

            if p == "2":
                cerr += num_examples_in_bin / total_examples * np.square(difference)
            elif p == "1":
                cerr += num_examples_in_bin / total_examples * difference
            elif p == "infty" or p == "infinity" or p == "max":
                cerr = np.maximum(cerr, difference)
            else:
                assert False, "p must be '1', '2', or 'infty'"

    if p == "2":
        cerr = np.sqrt(cerr)

    return cerr


def dump_metrics(datas):
    correct = []
    n = len(datas)
    for item in datas:
        correct.append("yes" in item["correct"])

    correct = np.array(correct)

    accuracy = round(100 * sum(correct) / n, 2)
    # Wald estimator, 95% confidence interval
    confidence_half_width = round(1.96 * math.sqrt(accuracy * (100 - accuracy) / n), 2)

    print("*** Metrics ***")
    print(f"Accuracy: {accuracy}% +/- {confidence_half_width}% | n = {n}")

    output_jsonl = args.input_jsonl.replace(".jsonl", "_metrics.txt")
    with open(output_jsonl, "w") as f:
        f.write(f"Accuracy: {accuracy}% +/- {confidence_half_width}% | n = {n}\n")


def post_process(text):
    """从返回的 text 中抽取两个字段(单行):
    reasoning, correct
    若某个字段缺失则对应变量为 "".
    规则: 匹配以字段名开头(忽略大小写)后跟冒号, 取其后直到行结束的内容.
    """
    fields = {
        "reasoning": "",
        "correct": "",
    }
    for key in fields.keys():
        # 保证以换行结束: 先补一个末尾换行, 用非贪婪匹配直到首个换行
        m = re.search(rf"{key}\s*:\s*(.*?)(?:\n|$)", text, re.IGNORECASE)
        if m:
            value_line = m.group(1).strip()
            fields[key] = value_line
    return fields


def judge(item):

    response = item[args.answer_column]
    # 提取response中的<answer>...</answer>内容
    ANSWER_TAG_REGEX = re.compile(r"<answer>(.*?)</answer>", re.DOTALL)
    match = ANSWER_TAG_REGEX.search(response)
    # 1. 先提取<answer>...</answer>
    # 2. 若无<answer>标签, 则找</think>, 取其后内容
    # 3. 若都无, 则直接用完整response
    if match:
        response = match.group(1).strip()
    else:
        response = ""

    question = item["question"]
    correct_answer = item["answer"]

    prompt = JUDGE_PROMPT.format(
        question=question, correct_answer=correct_answer, response=response
    )

    messages = [
        {"role": "user", "content": prompt},
    ]

    try:

        response = client.chat.completions.create(
            model=judger,
            messages=messages,
            stream=False,
        )

        text = response.choices[0].message.content

        information = post_process(text)
    except Exception as e:
        print(f"Error processing item with question: {question}. Error: {e}")
        information = {
            "reasoning": "error when calling judger",
            "correct": "no",
        }

    return information


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_jsonl", required=True, help="输入待评测的 jsonl 文件路径"
    )
    parser.add_argument("--answer_column", required=False, help="答案列名")
    args = parser.parse_args()

    args.output_jsonl = args.input_jsonl.replace(".jsonl", "_judged.jsonl")

    # 读取数据
    dataset = datasets.load_dataset("json", data_files=args.input_jsonl, split="train")

    # 模型判断答案是否正确
    result_dataset = dataset.map(judge, num_proc=judge_process)

    # 写入结果
    with open(args.output_jsonl, "w") as f:
        for item in result_dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    # 统计指标
    dump_metrics(result_dataset)
