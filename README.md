<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
  <img src="https://github.com/skyipeng/readme_r1v_test/raw/main/pic/logo.jpeg" width="60%" alt="DeepSeek-V3" />
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


### Base Model
#### Standard Benchmarks

<div align="center">


|  | Benchmark (Metric) | # Shots | DeepSeek-V2 | Qwen2.5 72B | LLaMA3.1 405B | DeepSeek-V3 |
|---|-------------------|----------|--------|-------------|---------------|---------|
| | Architecture | - | MoE | Dense | Dense | MoE |
| | # Activated Params | - | 21B | 72B | 405B | 37B |
| | # Total Params | - | 236B | 72B | 405B | 671B |
| English | Pile-test (BPB) | - | 0.606 | 0.638 | **0.542** | 0.548 |
| | BBH (EM) | 3-shot | 78.8 | 79.8 | 82.9 | **87.5** |
| | MMLU (Acc.) | 5-shot | 78.4 | 85.0 | 84.4 | **87.1** |
| | MMLU-Redux (Acc.) | 5-shot | 75.6 | 83.2 | 81.3 | **86.2** |
| | MMLU-Pro (Acc.) | 5-shot | 51.4 | 58.3 | 52.8 | **64.4** |
| | DROP (F1) | 3-shot | 80.4 | 80.6 | 86.0 | **89.0** |
| | ARC-Easy (Acc.) | 25-shot | 97.6 | 98.4 | 98.4 | **98.9** |
| | ARC-Challenge (Acc.) | 25-shot | 92.2 | 94.5 | **95.3** | **95.3** |
| | HellaSwag (Acc.) | 10-shot | 87.1 | 84.8 | **89.2** | 88.9 |
| | PIQA (Acc.) | 0-shot | 83.9 | 82.6 | **85.9** | 84.7 |
| | WinoGrande (Acc.) | 5-shot | **86.3** | 82.3 | 85.2 | 84.9 |
| | RACE-Middle (Acc.) | 5-shot | 73.1 | 68.1 | **74.2** | 67.1 |
| | RACE-High (Acc.) | 5-shot | 52.6 | 50.3 | **56.8** | 51.3 |
| | TriviaQA (EM) | 5-shot | 80.0 | 71.9 | 82.7 | **82.9** |
| | NaturalQuestions (EM) | 5-shot | 38.6 | 33.2 | **41.5** | 40.0 |
| | AGIEval (Acc.) | 0-shot | 57.5 | 75.8 | 60.6 | **79.6** |
| Code | HumanEval (Pass@1) | 0-shot | 43.3 | 53.0 | 54.9 | **65.2** |
| | MBPP (Pass@1) | 3-shot | 65.0 | 72.6 | 68.4 | **75.4** |
| | LiveCodeBench-Base (Pass@1) | 3-shot | 11.6 | 12.9 | 15.5 | **19.4** |
| | CRUXEval-I (Acc.) | 2-shot | 52.5 | 59.1 | 58.5 | **67.3** |
| | CRUXEval-O (Acc.) | 2-shot | 49.8 | 59.9 | 59.9 | **69.8** |
| Math | GSM8K (EM) | 8-shot | 81.6 | 88.3 | 83.5 | **89.3** |
| | MATH (EM) | 4-shot | 43.4 | 54.4 | 49.0 | **61.6** |
| | MGSM (EM) | 8-shot | 63.6 | 76.2 | 69.9 | **79.8** |
| | CMath (EM) | 3-shot | 78.7 | 84.5 | 77.3 | **90.7** |
| Chinese | CLUEWSC (EM) | 5-shot | 82.0 | 82.5 | **83.0** | 82.7 |
| | C-Eval (Acc.) | 5-shot | 81.4 | 89.2 | 72.5 | **90.1** |
| | CMMLU (Acc.) | 5-shot | 84.0 | **89.5** | 73.7 | 88.8 |
| | CMRC (EM) | 1-shot | **77.4** | 75.8 | 76.0 | 76.3 |
| | C3 (Acc.) | 0-shot | 77.4 | 76.7 | **79.7** | 78.6 |
| | CCPM (Acc.) | 0-shot | **93.0** | 88.5 | 78.6 | 92.0 |
| Multilingual | MMMLU-non-English (Acc.) | 5-shot | 64.0 | 74.8 | 73.8 | **79.4** |

</div>

> [!NOTE]
> Best results are shown in bold. Scores with a gap not exceeding 0.3 are considered to be at the same level. DeepSeek-V3 achieves the best performance on most benchmarks, especially on math and code tasks.
> For more evaluation details, please check our paper. 

#### Context Window
<p align="center">
  <img width="80%" src="figures/niah.png">
</p>

Evaluation results on the ``Needle In A Haystack`` (NIAH) tests.  DeepSeek-V3 performs well across all context window lengths up to **128K**. 

### Chat Model
#### Standard Benchmarks (Models larger than 67B)
<div align="center">

| | **Benchmark (Metric)** | **DeepSeek V2-0506** | **DeepSeek V2.5-0905** | **Qwen2.5 72B-Inst.** | **Llama3.1 405B-Inst.** | **Claude-3.5-Sonnet-1022** | **GPT-4o 0513** | **DeepSeek V3** |
|---|---------------------|---------------------|----------------------|---------------------|----------------------|---------------------------|----------------|----------------|
| | Architecture | MoE | MoE | Dense | Dense | - | - | MoE |
| | # Activated Params | 21B | 21B | 72B | 405B | - | - | 37B |
| | # Total Params | 236B | 236B | 72B | 405B | - | - | 671B |
| English | MMLU (EM) | 78.2 | 80.6 | 85.3 | **88.6** | **88.3** | 87.2 | **88.5** |
| | MMLU-Redux (EM) | 77.9 | 80.3 | 85.6 | 86.2 | **88.9** | 88.0 | **89.1** |
| | MMLU-Pro (EM) | 58.5 | 66.2 | 71.6 | 73.3 | **78.0** | 72.6 | 75.9 |
| | DROP (3-shot F1) | 83.0 | 87.8 | 76.7 | 88.7 | 88.3 | 83.7 | **91.6** |
| | IF-Eval (Prompt Strict) | 57.7 | 80.6 | 84.1 | 86.0 | **86.5** | 84.3 | 86.1 |
| | GPQA-Diamond (Pass@1) | 35.3 | 41.3 | 49.0 | 51.1 | **65.0** | 49.9 | 59.1 |
| | SimpleQA (Correct) | 9.0 | 10.2 | 9.1 | 17.1 | 28.4 | **38.2** | 24.9 |
| | FRAMES (Acc.) | 66.9 | 65.4 | 69.8 | 70.0 | 72.5 | **80.5** | 73.3 |
| | LongBench v2 (Acc.) | 31.6 | 35.4 | 39.4 | 36.1 | 41.0 | 48.1 | **48.7** |
| Code | HumanEval-Mul (Pass@1) | 69.3 | 77.4 | 77.3 | 77.2 | 81.7 | 80.5 | **82.6** |
| | LiveCodeBench (Pass@1-COT) | 18.8 | 29.2 | 31.1 | 28.4 | 36.3 | 33.4 | **40.5** |
| | LiveCodeBench (Pass@1) | 20.3 | 28.4 | 28.7 | 30.1 | 32.8 | 34.2 | **37.6** |
| | Codeforces (Percentile) | 17.5 | 35.6 | 24.8 | 25.3 | 20.3 | 23.6 | **51.6** |
| | SWE Verified (Resolved) | - | 22.6 | 23.8 | 24.5 | **50.8** | 38.8 | 42.0 |
| | Aider-Edit (Acc.) | 60.3 | 71.6 | 65.4 | 63.9 | **84.2** | 72.9 | 79.7 |
| | Aider-Polyglot (Acc.) | - | 18.2 | 7.6 | 5.8 | 45.3 | 16.0 | **49.6** |
| Math | AIME 2024 (Pass@1) | 4.6 | 16.7 | 23.3 | 23.3 | 16.0 | 9.3 | **39.2** |
| | MATH-500 (EM) | 56.3 | 74.7 | 80.0 | 73.8 | 78.3 | 74.6 | **90.2** |
| | CNMO 2024 (Pass@1) | 2.8 | 10.8 | 15.9 | 6.8 | 13.1 | 10.8 | **43.2** |
| Chinese | CLUEWSC (EM) | 89.9 | 90.4 | **91.4** | 84.7 | 85.4 | 87.9 | 90.9 |
| | C-Eval (EM) | 78.6 | 79.5 | 86.1 | 61.5 | 76.7 | 76.0 | **86.5** |
| | C-SimpleQA (Correct) | 48.5 | 54.1 | 48.4 | 50.4 | 51.3 | 59.3 | **64.8** |

</div>

> [!NOTE]
> All models are evaluated in a configuration that limits the output length to 8K. Benchmarks containing fewer than 1000 samples are tested multiple times using varying temperature settings to derive robust final results. DeepSeek-V3 stands as the best-performing open-source model, and also exhibits competitive performance against frontier closed-source models.


####  Open Ended Generation Evaluation

<div align="center">



| Model | Arena-Hard | AlpacaEval 2.0 |
|-------|------------|----------------|
| DeepSeek-V2.5-0905 | 76.2 | 50.5 |
| Qwen2.5-72B-Instruct | 81.2 | 49.1 |
| LLaMA-3.1 405B | 69.3 | 40.5 |
| GPT-4o-0513 | 80.4 | 51.1 |
| Claude-Sonnet-3.5-1022 | 85.2 | 52.0 |
| DeepSeek-V3 | **85.5** | **70.0** |

</div>

> [!NOTE]
> English open-ended conversation evaluations. For AlpacaEval 2.0, we use the length-controlled win rate as the metric.


## 5. Chat Website & API Platform
You can chat with DeepSeek-V3 on DeepSeek's official website: [chat.deepseek.com](https://chat.deepseek.com/sign_in)

We also provide OpenAI-Compatible API at DeepSeek Platform: [platform.deepseek.com](https://platform.deepseek.com/)

## 6. How to Run Locally

DeepSeek-V3 can be deployed locally using the following hardware and open-source community software:

1. **DeepSeek-Infer Demo**: We provide a simple and lightweight demo for FP8 and BF16 inference.
2. **SGLang**: Fully support the DeepSeek-V3 model in both BF16 and FP8 inference modes, with Multi-Token Prediction [coming soon](https://github.com/sgl-project/sglang/issues/2591).
3. **LMDeploy**: Enables efficient FP8 and BF16 inference for local and cloud deployment.
4. **TensorRT-LLM**: Currently supports BF16 inference and INT4/8 quantization, with FP8 support coming soon.
5. **vLLM**: Support DeepSeek-V3 model with FP8 and BF16 modes for tensor parallelism and pipeline parallelism.
6. **AMD GPU**: Enables running the DeepSeek-V3 model on AMD GPUs via SGLang in both BF16 and FP8 modes.
7. **Huawei Ascend NPU**: Supports running DeepSeek-V3 on Huawei Ascend devices.

Since FP8 training is natively adopted in our framework, we only provide FP8 weights. If you require BF16 weights for experimentation, you can use the provided conversion script to perform the transformation.

Here is an example of converting FP8 weights to BF16:

```shell
cd inference
python fp8_cast_bf16.py --input-fp8-hf-path /path/to/fp8_weights --output-bf16-hf-path /path/to/bf16_weights
```

```
#### Model Weights & Demo Code Preparation

First, clone our DeepSeek-V3 GitHub repository:

```shell
git clone https://github.com/deepseek-ai/DeepSeek-V3.git
```

Navigate to the `inference` folder and install dependencies listed in `requirements.txt`. Easiest way is to use a package manager like `conda` or `uv` to create a new virtual environment and install the dependencies.

```shell
cd skywork-r1v/inference
pip install -r requirements.txt
```

Download the model weights from Hugging Face, and put them into `/path/to/skywork-r1v` folder.


#### Run

Then you can chat with DeepSeek-V3:

```shell
torchrun --nnodes 2 --nproc-per-node 8 --node-rank $RANK --master-addr $ADDR generate.py --ckpt-path /path/to/DeepSeek-V3-Demo --config configs/config_671B.json --interactive --temperature 0.7 --max-new-tokens 200
```

Or batch inference on a given file:

```shell
torchrun --nnodes 2 --nproc-per-node 8 --node-rank $RANK --master-addr $ADDR generate.py --ckpt-path /path/to/DeepSeek-V3-Demo --config configs/config_671B.json --input-file $FILE
```

## 7. License
This code repository is licensed under [the MIT License](LICENSE-CODE). 
✅ Commercial use permitted

✅ Modification allowed

✅ Distribution allowed

❌ No liability


## 8. Citation
If you use Skywork-R1V in your research, please cite:

```
@article{skywork2025r1v,
  title     = {Skywork-R1V: Bridging Vision and Language for Advanced Multimodal Reasoning},
  author    = {Skywork VL Team},
  year      = {2025},
  journal   = {arXiv preprint arXiv:XXXX.XXXXX},
  url       = {https://github.com/skywork-ai/Skywork-R1V}
}
