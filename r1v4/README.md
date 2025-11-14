# Server Test 工具集

用于批量测试 AI API 接口的工具集，支持图文问答测试和结果可视化。

## 📁 文件说明

### 测试脚本
- `batch_nonstream.py` - 非流式模式批量测试（使用 r1v4-lite 模型）
- `batch_stream.py` - 流式模式批量测试（使用 r1v4-lite 模型）
- `batch_planner_nonstream.py` - 非流式模式批量测试（使用 planner 模型）
- `batch_planner_stream.py` - 流式模式批量测试（使用 planner 模型）

### 辅助文件
- `test_cases.jsonl` - 测试用例输入文件
- `visual.py` - Web 可视化工具，查看测试结果
- `result_*.jsonl` - 测试结果输出文件

## 🚀 快速开始

### 1. 准备测试用例

编辑 `test_cases.jsonl`，每行一个测试用例（JSON 格式）：

```json
{"image": "./demo_image/demo_1.png", "question": "图片中的内容是什么？"}
{"image": "", "question": "这是一个纯文本问题"}
```

### 2. 运行批量测试

```bash
# 使用默认文件（test_cases.jsonl -> result_nonstream.jsonl）
python3 batch_nonstream.py

# 指定输入输出文件
python3 batch_nonstream.py input.jsonl output.jsonl

# 使用流式模式
python3 batch_stream.py

# 使用 planner 模型
python3 batch_planner_nonstream.py
```

### 3. 查看测试结果

```bash
# 启动可视化工具
python3 visual.py

# 指定端口
python3 visual.py 8080
```

然后在浏览器中输入结果文件路径（如 `result_nonstream.jsonl`）查看结果。

## 📝 测试用例格式

```json
{
  "image": "图片路径（可选，留空表示纯文本）",
  "question": "问题内容"
}
```

## 📊 结果文件格式

```json
{
  "image": "图片路径",
  "question": "问题",
  "response": {
    "full_response": "完整回答内容",
    "raw_response": "原始API响应"
  }
}
```

## ⚙️ 配置说明

API 配置在各个脚本的 `call_api()` 函数中：
- `base_url` - API 地址
- `api_key` - API 密钥
- `model` - 模型名称
- `enable_search` - 是否启用联网搜索（True/False）

## 💡 常用场景

1. **测试图文理解**：使用 `batch_nonstream.py` 或 `batch_stream.py`
2. **测试规划能力**：使用 `batch_planner_nonstream.py` 或 `batch_planner_stream.py`
3. **查看结果对比**：使用 `visual.py` 在浏览器中查看

## 📦 依赖

```bash
pip install requests tqdm flask pillow
```

