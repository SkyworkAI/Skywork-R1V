<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
  <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/skywork_logo.png" alt="Skywork Logo" width="400">
  <h1><strong>Skywork-R1V4</strong></h1>
</div>

<font size=7><div align='center' >  [[📖 Skywork-R1V4 Report](https://github.com/SkyworkAI/Skywork-R1V/blob/main/Skywork_R1V4.pdf)] </div></font>

Welcome to the Skywork-R1V repository! Here, you'll find a series of state-of-the-art multimodal reasoning models with powerful agentic capabilities. From open-source versions with model weights and inference code to our latest closed-source offerings, the Skywork-R1V series delivers exceptional performance across vision understanding, code execution, and deep research tasks.

## 🔥 News

**💥 November 18, 2025**: We released **Skywork-R1V4-Lite**, a lightweight and ultra-fast closed-source multimodal reasoning model that achieves exceptional image understanding capabilities through code execution tools. R1V4-Lite features blazing-fast inference speed and can be integrated with search tools to enable deep research capabilities. Available now on Skywork Platform, and coming soon to OpenRouter—stay tuned!

**July 15, 2025**: We've released quantized versions of ​Skywork-R1V3​ for efficient inference:
* AWQ Quantization: [🤗 Skywork-R1V3-38B-AWQ](https://huggingface.co/Skywork/Skywork-R1V3-38B-AWQ) -- Supports single-GPU inference (VRAM ≥ 30GB).
* ​GGUF Quantization (4-bit & 8-bit)​: [🤗 Skywork-R1V3-38B-GGUF](https://huggingface.co/Skywork/Skywork-R1V3-38B-GGUF) -- Optimized for CPU-based inference.

**July 9, 2025**: We released Skywork-R1V3-38B [[🤗 Skywork-R1V3-38B](https://huggingface.co/Skywork/Skywork-R1V3-38B)], the latest and most powerful open-source multimodal reasoning model in the Skywork series, pushing the boundaries of multimodal and cross-disciplinary intelligence. Mainly through RL algorithm in post-training, R1V3 significantly enhances multimodal reasoning ablity and achieves open-source state-of-the-art (SOTA) performance across multiple multimodal reasoning benchmarks, e.g. 76.0 on MMMU.

**April 28, 2025**: We released awq quantized version of Skywork R1V2[[🤗 Skywork-R1V2-38B-AWQ](https://huggingface.co/Skywork/Skywork-R1V2-38B-AWQ)], supporting single-card (above 30GB) inference.

 **April 24, 2025**: We released **Skywork-R1V2**, an advanced open-source multimodal reasoning model that demonstrates strong performance across a range of multimodal reasoning benchmarks including MMMU, MMMU-Pro, MathVista, and OlympiadBench.[[🤗 Skywork-R1V2-38B](https://huggingface.co/Skywork/Skywork-R1V2-38B)][[📖R1V2 Report](https://arxiv.org/abs/2504.16656)] 
 
**April 9, 2025**: Our technical report is currently available on arxiv: [[Skywork-R1V: Pioneering Multimodal Reasoning with CoT](https://arxiv.org/abs/2504.05599)].

**Mar 26, 2025**: We released awq quantized version of Skywork R1V[[🤗 Skywork-R1V-38B-AWQ](https://huggingface.co/Skywork/Skywork-R1V-38B-AWQ)], supporting single-card (above 30GB) inference.

**Mar 18, 2025**: We are thrilled to introduce Skywork R1V, the first industry open-sourced multimodal reasoning model with advanced visual chain-of-thought capabilities, pushing the boundaries of AI-driven vision and logical inference! 🚀


## 📊 Evaluation
Skywork-R1V4-Lite demonstrates state-of-the-art performance on various multimodal tasks, particularly excelling in perception and deep research capabilities.

**Comparison of Skywork-R1V4 with Leading Multimodal Models**

| Benchmark | Split | Skywork-R1V4<br/>30B(A3B) | Qwen3-VL<br/>30B(A3B) | Qwen3-VL<br/>235B(A22B) | Gemini 2.5 Flash | Gemini 2.5 Pro |
|-----------|-------|:-------------------------:|:---------------------:|:-----------------------:|:----------------:|:--------------:|
| **Perception** |
| HIRbench-4K | FSP | **91.8** | 88.5 | 89.0 | 81.5 | 85.5 |
| | FCP | 73.8 | 68.5 | **77.0** | 74.0 | 82.3 |
| | Overall | **82.8** | 78.5 | 83.0 | 77.5 | 83.9 |
| HIRbench-8K | FSP | **88.8** | 80.3 | 83.0 | 75.8 | 83.0 |
| | FCP | 70.8 | 68.3 | **77.3** | 71.8 | 80.0 |
| | Overall | **79.8** | 74.2 | 80.4 | 73.7 | 81.5 |
| MME-Real | Perception | **73.4** | 70.4 | 74.3 | 62.3 | 73.1 |
| | Reasoning | 56.4 | 47.7 | 52.5 | 51.0 | **58.2** |
| | Overall | **71.4** | 67.7 | 71.6 | 60.9 | 71.3 |
| MME-Real-CN | Perception | **76.3** | 72.6 | 76.0 | 65.8 | 74.5 |
| | Reasoning | **59.4** | 45.0 | 53.8 | 51.3 | 58.3 |
| | Overall | **70.8** | 63.7 | 68.8 | 61.2 | 69.3 |
| MME-Real-Lite | Perception | **63.2** | 58.0 | 60.2 | 50.4 | 59.9 |
| | Reasoning | **53.2** | 46.3 | 50.7 | 49.9 | 55.1 |
| | Overall | **59.3** | 53.2 | 56.5 | 50.2 | 58.3 |
| V* | Attribute | **90.4** | 81.7 | 79.1 | 77.3 | 86.8 |
| | Spatial | **84.2** | 82.9 | 82.9 | 64.4 | 68.4 |
| | Overall | **88.0** | 82.2 | 80.6 | 72.3 | 79.1 |
| TreeBench | Overall | 48.4 | 42.7 | 49.6 | 45.9 | **54.6** |
| Visual Probe | Hard | 42.4 | 30.1 | **42.4** | 28.3 | 33.9 |
| | Medium | 42.9 | 35.8 | 39.1 | 31.3 | **35.4** |
| | Easy | **66.7** | 65.2 | 65.9 | 45.3 | 49.6 |
| **Deep Research** |
| MMSearch | Overall | **66.1** | 18.7 | 48.0 | 64.9 | 71.9 |
| FVQA | Overall | **67.2** | 53.3 | 54.4 | 60.7 | 72.0 |
| BrowseComp-VL | Overall | 38.4 | 30.0 | 31.6 | 40.8 | **45.4** |

**Key Highlights:**
- 🏆 Skywork-R1V4 achieves **top performance** among 30B-class models across most perception benchmarks
- 🚀 **Outstanding FSP scores** on HIRbench-4K (91.8) and HIRbench-8K (88.8), demonstrating exceptional high-resolution image understanding
- 🔍 **Strong deep research capabilities** with competitive performance on MMSearch (66.1) and FVQA (67.2)

 
## 🚀 How to Use Skywork-R1V4-Lite

Skywork-R1V4-Lite is available as an API service. You can access it through [Skywork Platform](https://platform.skyworkmodel.ai) or [OpenRouter](https://openrouter.ai) (coming soon).

### 1. Get API Access

Visit [Skywork Platform](https://platform.skyworkmodel.ai) to obtain your API key.

### 2. Quick Start with Python

```python
import requests
import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
        return base64.b64encode(image_data).decode("utf-8")

# API configuration
base_url = "https://api.skyworkmodel.ai"
api_key = "your_api_key_here"

# Prepare the request
image_base64 = image_to_base64("path/to/your/image.jpg")
content = [
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
    {"type": "text", "text": "What's in this image?"}
]

# Call the API
response = requests.post(
    f"{base_url}/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "skywork/r1v4-lite",
        "messages": [{"role": "user", "content": content}],
        "stream": False,
        "enable_search": False  # Set to True for deep research capabilities
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

### 3. Batch Testing with Our Tool Suite

We provide a comprehensive testing toolkit in the `r1v4` folder for batch processing and result visualization.

#### Clone and Setup

```shell
git clone https://github.com/SkyworkAI/Skywork-R1V.git
cd Skywork-R1V/r1v4
pip install -r requirements.txt
```

#### Prepare Test Cases

Edit `test_cases.jsonl` with your test cases (one JSON per line):

```json
{"image": "./demo_image/demo_1.png", "question": "What's in this image?"}
{"image": "", "question": "This is a text-only question"}
```

#### Run Batch Tests

```shell
# Non-streaming mode (default)
python3 batch_nonstream.py

# Streaming mode
python3 batch_stream.py

# With custom input/output files
python3 batch_nonstream.py input.jsonl output.jsonl

# Using planner model for task planning
python3 batch_planner_nonstream.py
```

#### Visualize Results

```shell
# Start the web viewer
python3 visual.py

# Then open browser and input result file path (e.g., result_nonstream.jsonl)
```

#### Parse Structured Responses

```python
from parse_utils import parse_full_response

# Parse the response to extract reasoning steps, tool calls, and observations
parsed = parse_full_response(response_text)

# Access structured data
for round_data in parsed['rounds']:
    print(f"Round {round_data['round_num']}")
    print(f"Thinking: {round_data['think']}")
    print(f"Tool: {round_data['tool_call']['name']}")
```

### 4. Features

- **Code Execution**: R1V4-Lite can write and execute Python code for complex tasks
- **Deep Research**: Enable `enable_search=True` to integrate web search capabilities
- **Multi-turn Reasoning**: Automatic multi-step reasoning with tool usage
- **Streaming Support**: Real-time response streaming for better user experience

## License
This code repository is licensed under [the MIT License](https://github.com/SkyworkAI/Skywork-R1V/blob/main/LICENSE). 

✅ Commercial use permitted

✅ Modification allowed

✅ Distribution allowed

❌ No liability

Skywork-R1V4-Lite is based on [Qwen3-VL-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-30B-A3B-Instruct) as the base model, which is licensed under the Apache 2.0 License.

## Acknowledgments

We would like to express our gratitude to the following open-source projects that have been instrumental in our work:

- [MS-SWIFT](https://github.com/modelscope/swift): A powerful framework for model training and fine-tuning that greatly facilitated our model development process.
- [VLMEvalKit](https://github.com/open-compass/VLMEvalKit): A comprehensive evaluation toolkit for vision-language models that enabled our extensive benchmarking.

## 🔮 Future Directions

We are excited to share our vision for the future development of the Skywork-R1V series:

- **Skywork-R1V4-Pro**: We are developing a more powerful model with enhanced capabilities across all benchmarks. Stay tuned for the upcoming release!
- **Reinforcement Learning Research**: We are actively exploring the application of reinforcement learning techniques to advance multimodal reasoning and agentic capabilities, pushing the boundaries of what's possible in vision-language AI.

## Citation
If you use Skywork-R1V in your research, please cite:
```
@misc{shen2025skyworkr1v3technicalreport,
      title={Skywork-R1V3 Technical Report}, 
      author={Wei Shen and Jiangbo Pei and Yi Peng and Xuchen Song and Yang Liu and Jian Peng and Haofeng Sun and Yunzhuo Hao and Peiyu Wang and Jianhao Zhang and Yahui Zhou},
      year={2025},
      eprint={2507.06167},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2507.06167}, 
}
```
```
@misc{chris2025skyworkr1v2multimodalhybrid,
      title={Skywork R1V2: Multimodal Hybrid Reinforcement Learning for Reasoning}, 
      author={Peiyu Wang and Yichen Wei and Yi Peng and Xiaokun Wang and Weijie Qiu and Wei Shen and Tianyidan Xie and Jiangbo Pei and Jianhao Zhang and Yunzhuo Hao and Xuchen Song and Yang Liu and Yahui Zhou},
      year={2025},
      eprint={2504.16656},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2504.16656}, 
}
```

```
@misc{peng2025skyworkr1vpioneeringmultimodal,
      title={Skywork R1V: Pioneering Multimodal Reasoning with Chain-of-Thought}, 
      author={Yi Peng and Peiyu Wang and Xiaokun Wang and Yichen Wei and Jiangbo Pei and Weijie Qiu and Ai Jian and Yunzhuo Hao and Jiachun Pan and Tianyidan Xie and Li Ge and Rongxian Zhuang and Xuchen Song and Yang Liu and Yahui Zhou},
      year={2025},
      eprint={2504.05599},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2504.05599}, 
}
```
