#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量Plan测试脚本 - 流式版本（读取jsonl文件并调用API获取结果）

用法:
    python3 batch_plan_stream.py [input_jsonl] [output_jsonl]
"""

import os
import sys
import json
import base64
import requests
from tqdm import tqdm
import time


def image_to_base64(image_path):
    """将图片文件转换为base64编码"""
    with open(image_path, "rb") as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        from mimetypes import guess_type

        mime_type, _ = guess_type(image_path)
        return f"data:{mime_type};base64,{image_base64}"


def call_api(image_path, question):
    """调用API获取响应"""

    # 配置
    base_url = "https://test-platform-api.singularity-ai.com"
    api_key = "sk-ELGYcvIJYZnDoiLDxdrDlGIRvZLSFzRB"

    # 构建消息内容（图片在前，问题在后）
    content = []

    # 如果有图片，先添加图片
    if image_path and image_path.strip() and os.path.exists(image_path):
        try:
            image_base64 = image_to_base64(image_path)
            content.append({"type": "image_url", "image_url": {"url": image_base64}})
        except Exception as e:
            print(f"  ⚠️  读取图片失败: {e}")
            return {"error": f"读取图片失败: {e}"}

    # 然后添加问题文本
    content.append({"type": "text", "text": question})

    # 请求数据 - 流式模式
    data = {
        "messages": [{"role": "user", "content": content}],
        "model": "skywork/r1v4-vl-planner-lite",
        "stream": True,
    }

    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    url = f"{base_url}/api/v1/chat/completions"

    try:
        # 发送请求
        print(f"发送请求到: {url}")
        response = requests.post(
            url, json=data, headers=headers, stream=True, timeout=120
        )
        print(f"响应状态码: {response.status_code}")

        if response.status_code != 200:
            return {"error": f"请求失败: {response.status_code}, {response.text}"}

        # 收集所有SSE事件
        full_response = ""
        events = []

        for line in response.iter_lines(decode_unicode=True):
            if line:
                if isinstance(line, bytes):
                    line = line.decode("utf-8")

                events.append(line)

                # 尝试提取content
                if line.startswith("data: ") and line != "data: [DONE]":
                    try:
                        event_data = json.loads(line[6:])
                        if "choices" in event_data and len(event_data["choices"]) > 0:
                            delta = event_data["choices"][0].get("delta", {})
                            content_chunk = delta.get("content", "")
                            if content_chunk:
                                print(content_chunk, end="", flush=True)
                                full_response += content_chunk
                    except:
                        pass

        print()  # 换行
        return {"full_response": full_response, "raw_events": "\n".join(events)}

    except Exception as e:
        return {"error": str(e)}


def batch_process(input_jsonl, output_jsonl):
    """批量处理jsonl文件"""

    print(f"📂 读取输入文件: {input_jsonl}")

    # 读取输入jsonl
    test_cases = []
    with open(input_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                test_cases.append(json.loads(line))

    print(f"✅ 共加载 {len(test_cases)} 个测试用例")
    print(f"🚀 开始批量测试...\n")

    results = []

    # 使用tqdm显示进度
    for idx, test_case in enumerate(tqdm(test_cases, desc="测试进度"), 1):
        image_path = test_case.get("image")
        question = test_case.get("question")

        # 显示当前测试
        image_desc = (
            os.path.basename(image_path)
            if (image_path and image_path.strip())
            else "无图片"
        )
        print(f"\n[{idx}/{len(test_cases)}] 📝 问题: {question[:50]}...")
        print(f"         🖼️  图片: {image_desc}")

        # 调用API
        response = call_api(image_path, question)

        # 保存结果
        result = {"image": image_path, "question": question, "response": response}
        results.append(result)

        # 显示简要结果
        if "error" in response:
            print(f"         ❌ 错误: {response['error']}")

        # 延迟避免请求过快
        if idx < len(test_cases):
            time.sleep(1)

    # 保存结果
    print(f"\n💾 保存结果到: {output_jsonl}")
    with open(output_jsonl, "w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(f"\n🎉 完成! 共处理 {len(results)} 个测试用例")

    # 统计
    error_count = sum(1 for r in results if "error" in r["response"])
    success_count = len(results) - error_count
    print(f"✅ 成功: {success_count} 个")
    print(f"❌ 失败: {error_count} 个")


def main():
    if len(sys.argv) > 1:
        input_jsonl = sys.argv[1]
    else:
        input_jsonl = "test_cases.jsonl"

    if len(sys.argv) > 2:
        output_jsonl = sys.argv[2]
    else:
        output_jsonl = "result_plan_stream.jsonl"

    if not os.path.exists(input_jsonl):
        print(f"❌ 错误: 输入文件不存在 - {input_jsonl}")
        sys.exit(1)

    batch_process(input_jsonl, output_jsonl)


if __name__ == "__main__":
    main()
