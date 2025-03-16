<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
  <img src="https://github.com/skyipeng/readme_r1v_test/raw/main/pic/logo.jpeg" width="60%" alt="skywork-r1v" />
</div>
<hr>

## Table of Contents

1. [Introduction](#1-introduction)
2. [Model Summary](#2-model-summary)
3. [Model Downloads](#3-model-downloads)
4. [Evaluation Results](#4-evaluation-results)
5. [Chat Website & API Platform](#5-chat-website--api-platform)
6. [How to Run Locally](#6-how-to-run-locally)
7. [License](#7-license)
8. [Citation](#8-citation)
9. [Contact](#9-contact)

## 1. Introduction

We introduce Skywork-R1V, a multimodal reasoning model that extends the R1-series text models to visual modalities through a near-lossless transfer method. Using a lightweight visual projector, Skywork-R1V enables seamless multimodal adaptation without requiring retraining of either the base language model or vision encoder. To enhance visual-text alignment, we developed a hybrid optimization strategy combining Iterative Supervised Fine-Tuning (SFT) with Group Relative Policy Optimization (GRPO), significantly improving cross-modal integration. Additionally, we created an adaptive-length Chain-of-Thought distillation approach for generating reasoning data, which dynamically optimizes reasoning chain lengths to improve inference efficiency and prevent overthinking. The model achieves state-of-the-art performance on key multimodal reasoning benchmarks, scoring 68.1 on MMMU and 71.0 on MathVista, comparable to leading closed-source models like Gemini 2.0 and Kimi-k1.5. It also maintains strong textual reasoning capabilities, achieving impressive scores of 72.6 on AIME and 94.3 on MATH500. 

## 2. Model Summary

****Architecture:**** 

Skywork-R1V employs a modular architecture that efficiently combines vision and language capabilities:

- Vision Encoder: Uses Vision Transformer (ViT) as the visual backbone to process image inputs.
- Visual Projector: A lightweight MLP (multilayer perceptron) adapter that serves as the bridge between the vision and language components.
- Language Model: Utilizes R1-distilled-Qwen-32B as the reasoning-capable language model backbone.

The model follows a connection pattern of Vision Encoder → MLP Adapter → Language Model, where the MLP adapter aligns the output space of the vision encoder with the input space of the language model. This design allows for efficient transfer of reasoning capabilities from text to multimodal domains without requiring extensive retraining of either the vision encoder or language model.

 ****Methodology****

_Efficient Multimodal Transfer of Reasoning-Capable LLMs：_
A staged alignment approach that efficiently transfers reasoning capabilities from text to vision by first connecting a vision encoder to a substitute LLM before transferring to the reasoning-capable LLM, preserving reasoning abilities while minimizing data requirements.
- The MLP adapter is first trained to align the ViT with a substitute LLM (Qwen-32B-Instruct) using 2M samples of SFT data, while keeping both the vision encoder and language model frozen.
- The trained MLP is then transferred to connect the ViT with the reasoning-capable LLM (R1-distilled-Qwen-32B).
- Fine-tuning only the MLP parameters while keeping the vision encoder and language model frozen, ensuring preservation of reasoning capabilities while effectively aligning visual and textual representations.

_Hybrid Optimization Framework：_
A multi-stage training strategy combining iterative supervised fine-tuning with reinforcement learning that progressively improves model performance through error correction and reward-based optimization.
- Initial supervised fine-tuning (SFT) using the complete dataset.
- Iterative training with customized data. A reward model evaluates data quality and selects high-scoring samples. 
- Reinforcement learning using Group Relative Policy Optimization (GRPO) with a rule-based reward system (accuracy and format rewards) to enhance generalizability.

_Adaptive-Length Chain-of-Thought Distillation:_ 
The model uses Adaptive-Length Chain-of-Thought Distillation (AL-CoTD) to generate high-quality reasoning-oriented training data
- Evaluates image-text pairs through vision and text scoring.
- Determines required depth of cross-modal integration.
- Adaptively regulates reasoning chain length based on query complexity.
- Progressive refinement of reasoning processes with external evaluation and correction when needed.

## 3. Model Downloads

<div align="center">

| **Model** | **#Total Params** | **Download** |
| :------------: | :------------: | :------------: |
| skywork-r1v | 38B | [🤗 Hugging Face](https://huggingface.co/Skywork/Skywork-R1V-38B)   |

</div>

## 4. Evaluation Results
<div align="center">
  <img src="https://github.com/skyipeng/readme_r1v_test/raw/main/pic/eval.jpeg" width="80%" alt="skywork_r1v_eval" />
</div>

<div align="center">
  <b>Evaluation results of state-of-the-art LLMs and VLMs</b>
</div>
<table>
  <thead>
    <tr>
      <th></th>
      <th align="center"><strong>Vision</strong></th>
      <th align="center" colspan="3"><strong>Reasoning</strong></th>
      <th align="center" colspan="3"><strong>Vision</strong></th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th align="center"><strong>MATH-500</strong></th>
      <th align="center"><strong>AIME 2024</strong></th>
      <th align="center"><strong>GPQA</strong></th>
      <th align="center"><strong>MathVista(mini)</strong></th>
      <th align="center"><strong>MMMU(Val)</strong></th>
      <th align="center"><strong>CSVQA</strong></th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th align="center">pass@1</th>
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
      <td align="center">❌</td>
      <td align="center">82.6</td>
      <td align="center">23.3</td>
      <td align="center">49.0</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Deepseek V3</td>
      <td align="center">❌</td>
      <td align="center">90.2</td>
      <td align="center">39.2</td>
      <td align="center">59.1</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Deepseek R1</td>
      <td align="center">❌</td>
      <td align="center">97.3</td>
      <td align="center">79.8</td>
      <td align="center">71.5</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Claude 3.5 Sonnet</td>
      <td align="center">✅</td>
      <td align="center">78.3</td>
      <td align="center">16.0</td>
      <td align="center">65.0</td>
      <td align="center">67.7</td>
      <td align="center">68.3</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>GPT-4o</td>
      <td align="center">✅</td>
      <td align="center">76.6</td>
      <td align="center">9.3</td>
      <td align="center">53.6</td>
      <td align="center">63.8</td>
      <td align="center">69.1</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Kimi k1.5</td>
      <td align="center">✅</td>
      <td align="center">96.2</td>
      <td align="center">77.5</td>
      <td align="center">-</td>
      <td align="center">74.9</td>
      <td align="center">70.0</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Qwen2.5-VL-72B-Instruct</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">74.8</td>
      <td align="center">70.2</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>LLaVA-Onevision-72B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">67.5</td>
      <td align="center">56.8</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>InternVL2-Llama3-76B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">65.5</td>
      <td align="center">58.3</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>InternVL2.5-78B</td>
      <td align="center">✅</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">72.3</td>
      <td align="center">70.1</td>
      <td align="center">-</td>
    </tr>
    <tr>
      <td>Skywork-R1V-38B</td>
      <td align="center">✅</td>
      <td align="center">94.0</td>
      <td align="center">72.0</td>
      <td align="center">61.6</td>
      <td align="center">71.0</td>
      <td align="center">68.1</td>
      <td align="center">XXX</td>
    </tr>
  </tbody>
</table>

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
      <td align="center"><strong>94.0</strong></td>
    </tr>
    <tr>
      <td>AIME 2024</td>
      <td align="center">50.0</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center"><strong>72.0</strong></td>
    </tr>
    <tr>
      <td>GPQA</td>
      <td align="center">65.2</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">-</td>
      <td align="center">61.6</td>
    </tr>
    <tr>
      <td rowspan="3">Vision</td>
      <td>MathVista(mini)</td>
      <td align="center">-</td>
      <td align="center">71.9</td>
      <td align="center">49.5</td>
      <td align="center">63.7</td>
      <td align="center">71.0</td>
    </tr>
    <tr>
      <td>MMMU(Val)</td>
      <td align="center">-</td>
      <td align="center">63.9</td>
      <td align="center">55.1</td>
      <td align="center">55.2</td>
      <td align="center">68.1</td>
    </tr>
    <tr>
      <td>CSVQA</td>
      <td align="center">-</td>
      <td align="center"></td>
      <td align="center"></td>
      <td align="center"></td>
      <td align="center"></td>
    </tr>
  </tbody>
</table>


## 5. How to Run Locally

```
#### Model Weights & Demo Code Preparation

First, clone our skywork-r1v GitHub repository:

```shell
git clone https://github.com/SkyworkAI/Skywork-R1V.git
```

Navigate to the `inference` folder and install dependencies listed in `requirements.txt`. Easiest way is to use a package manager like `conda` or `uv` to create a new virtual environment and install the dependencies.

```shell
cd skywork-r1v/inference
pip install -r requirements.txt
```

Download the model weights from Hugging Face, and put them into `/path/to/skywork-r1v` folder.


#### Run

Then you can chat with skywork-r1v:

```shell
torchrun --nnodes 2 --nproc-per-node 8 --node-rank $RANK --master-addr $ADDR generate.py --ckpt-path /path/to/skywork-r1v-Demo --config configs/config_38B.json --interactive --temperature 0.7 --max-new-tokens 200
```

Or batch inference on a given file:

```shell
torchrun --nnodes 2 --nproc-per-node 8 --node-rank $RANK --master-addr $ADDR generate.py --ckpt-path /path/to/skywork-r1v-Demo --config configs/config_38B.json --input-file $FILE
```

## 6. License
This code repository is licensed under [the MIT License](LICENSE-CODE). 
✅ Commercial use permitted

✅ Modification allowed

✅ Distribution allowed

❌ No liability


## 7. Citation
If you use Skywork-R1V in your research, please cite:

```
@article{skywork2025r1v,
  title     = {Skywork-R1V: Bridging Vision and Language for Advanced Multimodal Reasoning},
  author    = {Skywork VL Team},
  year      = {2025},
  journal   = {arXiv preprint arXiv:XXXX.XXXXX},
  url       = {https://github.com/skywork-ai/Skywork-R1V}
}
