import argparse
import logging
import os
import json
from collections import defaultdict


def gen_score(input_file, output_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    total_correct = 0
    total_count = 0

    subject_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    type_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    category_stats = defaultdict(lambda: defaultdict(lambda: {"correct": 0, "total": 0}))
    task_stats = defaultdict(lambda: {"correct": 0, "total": 0})

    for key, entry in data.items():
        total_count += 1
        is_correct = 1 if entry["true_false"] else 0
        total_correct += is_correct

        subject = entry["subject"]
        question_type = entry["type"].lower()
        if entry["category"]:
            if subject == "Coding":
                category_list = entry["category"].split(';')
                for category in category_list:
                    category = category.strip()
                    category_stats[subject][category]["total"] += 1
                    category_stats[subject][category]["correct"] += is_correct
            else:
                category = entry["category"]
                category_stats[subject][category]["total"] += 1
                category_stats[subject][category]["correct"] += is_correct
        if entry["task"]:
            task = subject + '_' + entry["task"]
            task_stats[task]["total"] += 1
            task_stats[task]["correct"] += is_correct

        subject_stats[subject]["total"] += 1
        subject_stats[subject]["correct"] += is_correct

        type_stats[question_type]["total"] += 1
        type_stats[question_type]["correct"] += is_correct



    average_accuracy = total_correct / total_count if total_count > 0 else 0
    logging.info(f"Average accuracy: {average_accuracy}")

    score = {
        "average": {
            "accuracy": average_accuracy,
            "correct": total_correct,
            "total": total_count
        },
        "subject": {
            subject: {
                "accuracy": stats["correct"] / stats["total"] if stats["total"] > 0 else 0,
                "correct": stats["correct"],
                "total": stats["total"]
            } for subject, stats in subject_stats.items()
        },
        "question_type": {
            question_type: {
                "accuracy": stats["correct"] / stats["total"] if stats["total"] > 0 else 0,
                "correct": stats["correct"],
                "total": stats["total"]
            } for question_type, stats in type_stats.items()
        },
        "category": {
            subject:{
                category: {
                    "accuracy": stats["correct"] / stats["total"] if stats["total"] > 0 else 0,
                    "correct": stats["correct"],
                    "total": stats["total"]
                } for category, stats in categories.items()
            }for subject, categories in category_stats.items()
        },
        "task": {
            task: {
                "accuracy": stats["correct"] / stats["total"] if stats["total"] > 0 else 0,
                "correct": stats["correct"],
                "total": stats["total"]
            } for task, stats in task_stats.items()
        }
    }

    with open(output_file, "w") as f:
        f.write(json.dumps(score, indent=2))

def main():
    parser = argparse.ArgumentParser()
    # output
    parser.add_argument('--results_dir', type=str, default='/mnt/datasets_vlm/yunzhuo.hao/benchmarks/EMMA/results/EMMA-mini/open-source')
    args = parser.parse_args()
    for root, dirs, files in os.walk(args.results_dir):
        for file in files:
            if file.endswith(".json") and not file.endswith("_result.json"):
                gen_score(os.path.join(root, file), os.path.join(root, file).replace('.json', '_result.json'))


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