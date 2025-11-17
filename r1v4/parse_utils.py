import re
import json
from typing import Dict, List, Any, Optional


def parse_full_response(full_response: str) -> Dict[str, Any]:
    """
    解析 full_response 字符串，将其拆分成结构化的信息。

    每一轮包含 think、tool_call 和 observation
    最后一轮包含 think 和 answer

    Args:
        full_response: 包含多轮对话的字符串

    Returns:
        结构化的字典，包含:
        {
            "rounds": [
                {
                    "round_num": 1,
                    "think": "思考内容",
                    "tool_call": {...},  # 解析后的 JSON 对象
                    "observation": {...}  # 解析后的 JSON 对象
                },
                ...
            ],
            "final_round": {
                "think": "最终思考",
                "answer": "最终答案"
            }
        }
    """

    # 定义正则表达式模式
    think_pattern = r"<think>(.*?)</think>"
    tool_call_pattern = r"<tool_call>(.*?)</tool_call>"
    observation_pattern = r"<observation>(.*?)</observation>"
    answer_pattern = r"<answer>(.*?)</answer>"

    # 找到所有的 think, tool_call, observation
    thinks = re.findall(think_pattern, full_response, re.DOTALL)
    tool_calls = re.findall(tool_call_pattern, full_response, re.DOTALL)
    observations = re.findall(observation_pattern, full_response, re.DOTALL)
    answers = re.findall(answer_pattern, full_response, re.DOTALL)

    result = {"rounds": [], "final_round": {}}

    # 处理中间轮次（有 tool_call 和 observation 的轮次）
    num_rounds = len(tool_calls)

    for i in range(num_rounds):
        round_data = {
            "round_num": i + 1,
            "think": thinks[i].strip() if i < len(thinks) else "",
            "tool_call": None,
            "observation": None,
        }

        # 解析 tool_call JSON
        if i < len(tool_calls):
            try:
                round_data["tool_call"] = json.loads(tool_calls[i].strip())
            except json.JSONDecodeError as e:
                # 如果解析失败，保留原始字符串
                round_data["tool_call"] = tool_calls[i].strip()
                round_data["tool_call_parse_error"] = str(e)

        # 解析 observation JSON
        if i < len(observations):
            try:
                round_data["observation"] = json.loads(observations[i].strip())
            except json.JSONDecodeError as e:
                # 如果解析失败，保留原始字符串
                round_data["observation"] = observations[i].strip()
                round_data["observation_parse_error"] = str(e)

        result["rounds"].append(round_data)

    # 处理最后一轮（think + answer）
    if len(thinks) > num_rounds:
        result["final_round"]["think"] = thinks[-1].strip()
    else:
        result["final_round"]["think"] = ""

    if answers:
        result["final_round"]["answer"] = answers[0].strip()
    else:
        result["final_round"]["answer"] = ""

    return result


def parse_jsonl_file(
    input_file: str, output_file: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    解析整个 JSONL 文件，将每一行的 full_response 拆分成结构化信息。

    Args:
        input_file: 输入的 JSONL 文件路径
        output_file: 可选，输出解析后的 JSONL 文件路径

    Returns:
        包含所有解析结果的列表
    """
    results = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line.strip())

                # 解析 full_response
                if "response" in data and "full_response" in data["response"]:
                    parsed_response = parse_full_response(
                        data["response"]["full_response"]
                    )

                    # 创建新的数据结构
                    parsed_data = {
                        "line_num": line_num,
                        "image": data.get("image", ""),
                        "question": data.get("question", ""),
                        "raw_response": data.get("response", {}),
                        "parsed_response": parsed_response,
                    }

                    results.append(parsed_data)
                else:
                    print(f"Warning: Line {line_num} missing 'response.full_response'")

            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
            except Exception as e:
                print(f"Unexpected error on line {line_num}: {e}")

    # 如果指定了输出文件，保存解析结果
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            for result in results:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
        print(f"Saved parsed results to {output_file}")

    return results


def get_round_statistics(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    获取解析后数据的统计信息。

    Args:
        parsed_data: parse_full_response 返回的字典

    Returns:
        统计信息字典
    """
    stats = {
        "total_rounds": len(parsed_data.get("rounds", [])),
        "has_final_answer": bool(parsed_data.get("final_round", {}).get("answer", "")),
        "tools_used": [],
    }

    # 统计使用的工具
    for round_data in parsed_data.get("rounds", []):
        tool_call = round_data.get("tool_call")
        if isinstance(tool_call, dict) and "name" in tool_call:
            stats["tools_used"].append(tool_call["name"])

    return stats


# 示例用法
if __name__ == "__main__":
    # 示例：解析单个 full_response
    sample_response = """<think>
I need to identify the rightmost child in the image and determine the color of their skirt.
</think>
<tool_call>{"name": "code", "arguments": {"code": "print('hello')"}}</tool_call>
<observation>{"result": "hello", "type": "code"}</observation>
<think>
The cropped image shows the rightmost child clearly.
</think>
<answer>
The rightmost child has a red/orange colored skirt.
</answer>"""

    parsed = parse_full_response(sample_response)
    print("Parsed structure:")
    print(json.dumps(parsed, indent=2, ensure_ascii=False))

    print("\n" + "=" * 80 + "\n")

    # 示例：解析整个文件（注释掉，避免自动运行）
    # input_file = "/data_r1v4/data_r1v4/liang.hu/Skywork-R1V/r1v4/result_nonstream.jsonl"
    # output_file = "/data_r1v4/data_r1v4/liang.hu/Skywork-R1V/r1v4/result_nonstream_parsed.jsonl"
    # results = parse_jsonl_file(input_file, output_file)
    # print(f"Parsed {len(results)} entries")
    #
    # # 显示第一条的统计信息
    # if results:
    #     stats = get_round_statistics(results[0]["parsed_response"])
    #     print(f"First entry statistics: {stats}")
