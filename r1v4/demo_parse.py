"""
演示如何使用 parse_utils 解析 result_nonstream.jsonl 文件
"""

import json
from parse_utils import parse_full_response, get_round_statistics


def demo_parse_first_entry():
    """演示解析第一条数据"""
    input_file = "/data_r1v4/data_r1v4/liang.hu/Skywork-R1V/r1v4/result_nonstream.jsonl"

    print("=" * 80)
    print("读取并解析第一条数据")
    print("=" * 80)

    with open(input_file, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        data = json.loads(first_line)

    print(f"\n原始数据字段:")
    print(f"- image: {data['image']}")
    print(f"- question: {data['question']}")
    print(f"- full_response 长度: {len(data['response']['full_response'])} 字符")

    # 解析 full_response
    parsed = parse_full_response(data["response"]["full_response"])

    print(f"\n解析后的结构:")
    print(f"- 轮数: {len(parsed['rounds'])} 轮")

    # 显示每一轮的信息
    for i, round_data in enumerate(parsed["rounds"], 1):
        print(f"\n第 {i} 轮:")
        print(
            f"  Think: {round_data['think'][:100]}..."
            if len(round_data["think"]) > 100
            else f"  Think: {round_data['think']}"
        )

        if round_data["tool_call"]:
            if isinstance(round_data["tool_call"], dict):
                print(f"  Tool: {round_data['tool_call'].get('name', 'N/A')}")
            else:
                print(
                    f"  Tool call (unparsed): {str(round_data['tool_call'])[:100]}..."
                )

        if round_data["observation"]:
            if isinstance(round_data["observation"], dict):
                print(
                    f"  Observation type: {round_data['observation'].get('type', 'N/A')}"
                )
                if "result" in round_data["observation"]:
                    result = str(round_data["observation"]["result"])
                    print(
                        f"  Result: {result[:100]}..."
                        if len(result) > 100
                        else f"  Result: {result}"
                    )
            else:
                print(
                    f"  Observation (unparsed): {str(round_data['observation'])[:100]}..."
                )

    # 显示最终轮
    print(f"\n最终轮:")
    final = parsed["final_round"]
    print(
        f"  Final Think: {final['think'][:150]}..."
        if len(final["think"]) > 150
        else f"  Final Think: {final['think']}"
    )
    print(f"  Answer: {final['answer']}")

    # 获取统计信息
    stats = get_round_statistics(parsed)
    print(f"\n统计信息:")
    print(f"  总轮数: {stats['total_rounds']}")
    print(
        f"  使用的工具: {', '.join(stats['tools_used']) if stats['tools_used'] else '无'}"
    )
    print(f"  有最终答案: {'是' if stats['has_final_answer'] else '否'}")

    # 保存解析结果到 JSON 文件（方便查看）
    output_file = "/data_r1v4/data_r1v4/liang.hu/Skywork-R1V/r1v4/sample_parsed.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    print(f"\n解析结果已保存到: {output_file}")


if __name__ == "__main__":
    demo_parse_first_entry()
