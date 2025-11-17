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
- `parse_utils.py` - 解析工具，将 full_response 拆分成结构化信息
- `demo_parse.py` - 解析工具使用示例

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

### 4. 解析结构化响应

使用 `parse_utils.py` 可以将 `full_response` 拆分成结构化的信息，便于分析每一轮的思考、工具调用和观察结果。

#### 快速体验

```bash
# 运行演示脚本，解析第一条数据
python3 demo_parse.py
```

这将显示：
- 原始数据的基本信息
- 按轮次展示的思考、工具调用和观察
- 最终轮的思考和答案
- 统计信息（总轮数、使用的工具等）

#### 编程使用

```python
from parse_utils import parse_full_response, get_round_statistics
import json

# 读取数据
with open('result_nonstream.jsonl', 'r') as f:
    data = json.loads(f.readline())

# 解析 full_response
parsed = parse_full_response(data['response']['full_response'])

# 访问结构化数据
for round_data in parsed['rounds']:
    print(f"轮次 {round_data['round_num']}")
    print(f"思考: {round_data['think']}")
    print(f"工具: {round_data['tool_call']['name']}")
    print(f"观察: {round_data['observation']}")

# 最终答案
print(f"最终答案: {parsed['final_round']['answer']}")

# 获取统计信息
stats = get_round_statistics(parsed)
print(f"总轮数: {stats['total_rounds']}")
print(f"使用的工具: {stats['tools_used']}")
```

#### 批量处理

```python
from parse_utils import parse_jsonl_file

# 解析整个 JSONL 文件
results = parse_jsonl_file(
    'result_nonstream.jsonl',
    'result_nonstream_parsed.jsonl'  # 可选：保存解析结果
)

# 处理所有结果
for item in results:
    print(f"问题: {item['question']}")
    print(f"轮数: {len(item['parsed_response']['rounds'])}")
    print(f"答案: {item['parsed_response']['final_round']['answer']}")
```

## 📝 测试用例格式

```json
{
  "image": "图片路径（可选，留空表示纯文本）",
  "question": "问题内容"
}
```

## 📊 结果文件格式

### 原始格式

```json
{
  "image": "图片路径",
  "question": "问题",
  "response": {
    "full_response": "完整回答内容（包含 <think>、<tool_call>、<observation>、<answer> 标签）",
    "raw_response": "原始API响应"
  }
}
```

### 解析后的结构化格式

使用 `parse_full_response()` 解析后的数据结构：

```json
{
  "rounds": [
    {
      "round_num": 1,
      "think": "第一轮思考内容",
      "tool_call": {
        "name": "code",
        "arguments": {...}
      },
      "observation": {
        "type": "code",
        "result": "执行结果"
      }
    }
  ],
  "final_round": {
    "think": "最终思考",
    "answer": "最终答案"
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
4. **分析推理过程**：使用 `parse_utils.py` 解析每一轮的思考和工具调用
5. **批量数据分析**：使用 `parse_jsonl_file()` 处理整个结果文件，统计轮次、工具使用等信息

## 📦 依赖

```bash
pip install requests tqdm flask pillow
```

