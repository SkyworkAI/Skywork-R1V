<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

# Skywork-R1V: Pioneering Multimodal Reasoning with CoT
<font size=7><div align='center' > [[📖Technical Report](https://arxiv.org/abs/2504.05599)] [[🤗 Skywork-R1V-38B](https://huggingface.co/Skywork/Skywork-R1V-38B)] [[🤖 ModelScope](https://modelscope.cn/models/Skywork/Skywork-R1V-38B)]</div></font>

Welcome to the Skywork-R1V repository! Here, you'll find the model weights and inference code for our state-of-the-art open-sourced multimodal reasoning model, enabling advanced visual and logical thinking.
## 🔥News
**April 9, 2025**: Our technical report is currently available on arxiv: [[Skywork-R1V: Pioneering Multimodal Reasoning with CoT](https://arxiv.org/abs/2504.05599)].

**April 1, 2025**: Skywork-R1V supports inference with [[vLLM](https://github.com/vllm-project/vllm)], On 4×L20Y GPUs, vLLM generates 1k tokens in ~12.3s, at least 5× faster than transformers.

**Mar 26, 2025**: We released awq quantized version of Skywork R1V[[🤗 Skywork-R1V-38B-AWQ](https://huggingface.co/Skywork/Skywork-R1V-38B-AWQ)], supporting single-card (above 30GB) inference.

**Mar 18, 2025**: We are thrilled to introduce Skywork R1V, the first industry open-sourced multimodal reasoning model with advanced visual chain-of-thought capabilities, pushing the boundaries of AI-driven vision and logical inference! 🚀



<div align="center">
  <table>
    <tr>
      <td>
        <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/math_r1v.gif" width="450" height="400" alt="math_r1v" />
      </td>
      <td>
        <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/Chemistry_cn.gif" width="450" height="400" alt="chemistry_1" />
      </td>
    </tr>
  </table>
</div>



## Feature
- **Visual Chain-of-Thought**: Enables multi-step logical reasoning on visual inputs, breaking down complex image-based problems into manageable steps.
- **Mathematical & Scientific Analysis**: Capable of solving visual math problems and interpreting scientific/medical imagery with high precision.
- **Cross-Modal Understanding**: Seamlessly integrates text and images for richer, context-aware comprehension.

## Evaluation 

<div align="center">
  <b>Comparison with Larger-Scale Open-Source and Closed-Source Models</b>
</div>

<table align="center">
  <thead>
    <tr>
      <th></th>
      <th align="center"><strong>Benchmark</strong></th>
      <th align="center"><strong>LLM</strong></th>
      <th align="center" colspan="4"><strong>VLM</strong></th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th align="center"><strong>QwQ-32B-Preview</strong></th>
      <th align="center"><strong>QwenVL-2-72B</strong></th>
      <th align="center"><strong>InternVL-2.5-38B</strong></th>
      <th align="center"><strong>VILA 1.5-40B</strong></th>
      <th align="center"><strong>InternVL2-40B</strong></th>
      <th align="center"><strong>Skywork-R1V-38B</strong></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3">Reasoning</td>
      <td>MATH-500</td>
      <td align="center">90.6</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center"><strong>94.0</strong></td>
    </tr>
    <tr>
      <td>AIME 2024</td>
      <td align="center">50.0</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center"><strong>72.0</strong></td>
    </tr>
    <tr>
      <td>GPQA</td>
      <td align="center">54.5</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center"><strong>61.6</strong></td>
    </tr>
    <tr>
      <td rowspan="3">Vision</td>
      <td>MathVista(mini)</td>
      <td align="center">-</td>
      <td align="center">70.5</td>
      <td align="center"><strong>71.9</strong></td>
      <td align="center">49.5</td>
      <td align="center">63.7</td>
      <td align="center">67.5</td>
    </tr>
    <tr>
      <td>MMMU(Val)</td>
      <td align="center">-</td>
      <td align="center">64.5</td>
      <td align="center">63.9</td>
      <td align="center">55.1</td>
      <td align="center">55.2</td>
      <td align="center"><strong>69.0</strong></td>
    </tr>
  </tbody>
</table>

<div align="center">
  <b>Evaluation results of state-of-the-art LLMs and VLMs</b>
</div>
<table>
  <thead>
    <tr>
      <th></th>
      <th align="center"><strong>Size</strong></th>
      <th align="center"><strong>Vision</strong></th>
      <th align="center" colspan="3"><strong>Reasoning</strong></th>
      <th align="center" colspan="3"><strong>Vision</strong></th>
    </tr>
    <tr>
      <th></th>
      <th align="center"></th>
      <th></th>
      <th align="center"><strong>MATH-500</strong></th>
      <th align="center"><strong>AIME 2024</strong></th>
      <th align="center"><strong>GPQA</strong></th>
      <th align="center"><strong>MathVista(mini)</strong></th>
      <th align="center"><strong>MMMU(Val)</strong></th>
    </tr>
    <tr>
      <th></th>
      <th align="center"></th>
      <th></th>
      <th align="center">pass@1</th>
      <th align="center">pass@1</th>
      <th align="center">pass@1</th>
      <th align="center">pass@1</th>
      <th align="center">pass@1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Qwen2.5-72B-Instruct</td>
      <td align="center">72B</td>
      <td align="center">❌</td>
      <td align="center">80.0</td>
      <td align="center">23.3</td>
      <td align="center">49.0</td>
      <td align="center">-</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Deepseek V3</td>
      <td align="center">671B</td>
      <td align="center">❌</td>
      <td align="center">90.2</td>
      <td align="center">39.2</td>
      <td align="center">59.1</td>
      <td align="center">-</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Deepseek R1</td>
      <td align="center">671B</td>
      <td align="center">❌</td>
      <td align="center">97.3</td>
      <td align="center">79.8</td>
      <td align="center">71.5</td>
      <td align="center">-</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Claude 3.5 Sonnet</td>
      <td align="center">-</td>
      <td align="center">✅</td>
      <td align="center">78.3</td>
      <td align="center">16.0</td>
      <td align="center">65.0</td>
      <td align="center">65.3</td>
      <td align="center">66.4</td>
    </tr>
    <tr>
      <td>GPT-4o</td>
      <td align="center">-</td>
      <td align="center">✅</td>
      <td align="center">74.6</td>
      <td align="center">9.3</td>
      <td align="center">49.9</td>
      <td align="center">63.8</td>
      <td align="center">69.1</td>
    </tr>
    <tr>
      <td>Kimi k1.5</td>
      <td align="center">-</td>
      <td align="center">✅</td>
      <td align="center">96.2</td>
      <td align="center">77.5</td>
      <td align="center">-</td>
      <td align="center">74.9</td>
      <td align="center">70.0</td>
    </tr>
    <tr>
      <td>Qwen2.5-VL-72B-Instruct</td>
      <td align="center">72B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">74.8</td>
      <td align="center">70.2</td>
    </tr>
    <tr>
      <td>LLaVA-Onevision-72B</td>
      <td align="center">72B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">67.5</td>
      <td align="center">56.8</td>
    </tr>
    <tr>
      <td>InternVL2-Llama3-76B</td>
      <td align="center">76B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">65.5</td>
      <td align="center">62.7</td>
    </tr>
    <tr>
      <td>InternVL2.5-78B</td>
      <td align="center">78B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">72.3</td>
      <td align="center">70.1</td>
    </tr>
    <tr>
      <td><strong>Skywork-R1V-38B</strong></td>
      <td align="center"><strong>38B</strong></td>
      <td align="center">✅</td>
      <td align="center">94.0</td>
      <td align="center">72.0</td>
      <td align="center">61.6</td>
      <td align="center">67.5</td>
      <td align="center">69.0</td>
    </tr>
  </tbody>
</table>

<br></br>
<div align="center">
  <b>Comparison with Larger-Scale Closed-Source Models</b>
</div>
<div align="center">
  <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/comparsion.png" width="100%" alt="skywork_r1v_eval" />
</div>

<br></br>
<div align="center">
  <b>Comparison with Larger-Scale Open-Source Models</b>
</div>
<div align="center">
  <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/r1v_comp.png" width="100%" alt="skywork_r1v_eval" />
</div>

## How to Run Locally

### 1. Clone the Repository

```shell
git clone https://github.com/SkyworkAI/Skywork-R1V.git
cd skywork-r1v/inference
```
### 2. Set Up the Environment

```shell
conda create -n r1-v python=3.10
conda activate r1-v
bash setup.sh
```

### 3. Run the Inference Script

```shell
CUDA_VISIBLE_DEVICES="0,1" python inference_with_transformers.py \
    --model_path path \
    --image_paths image1_path \
    --question "your question"
```

## How to Run Locally with vLLM

### 1. Set Up the Environment
Refer to vLLM's installation from the source. https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html
```shell
conda create -n r1v-vllm python=3.12
conda activate r1v-vllm
pip install pillow==11.1.0
git clone https://github.com/vllm-project/vllm.git
cd vllm
pip install -e . 
```
### 2. Clone the Repository

```shell
git clone https://github.com/SkyworkAI/Skywork-R1V.git
cd skywork-r1v/inference
```

### 3. Run the Inference Script

```shell
python inference_with_vllm.py \
    --model_path path \
    --image_paths image1_path image2_path \
    --question "your question" \
    --tensor_parallel_size 4
```

## License
This code repository is licensed under [the MIT License](https://github.com/SkyworkAI/Skywork-R1V/blob/main/LICENSE). 
✅ Commercial use permitted

✅ Modification allowed

✅ Distribution allowed

❌ No liability


## Citation
If you use Skywork-R1V in your research, please cite:

```
@misc{peng2025skyworkr1vpioneeringmultimodal,
      title={Skywork R1V: Pioneering Multimodal Reasoning with Chain-of-Thought}, 
      author={Yi Peng and Chris and Xiaokun Wang and Yichen Wei and Jiangbo Pei and Weijie Qiu and Ai Jian and Yunzhuo Hao and Jiachun Pan and Tianyidan Xie and Li Ge and Rongxian Zhuang and Xuchen Song and Yang Liu and Yahui Zhou},
      year={2025},
      eprint={2504.05599},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2504.05599}, 
}
```

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=SkyworkAI/Skywork-R1V&type=Date)](https://www.star-history.com/#SkyworkAI/Skywork-R1V&Date)
