<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
  <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/skywork_logo.png" alt="Skywork Logo" width="400">
  <h1><strong>Skywork-R1V3</strong></h1>
</div>

<font size=7><div align='center' >  [[🤗 Skywork-R1V3-38B](https://huggingface.co/Skywork/Skywork-R1V3-38B)] [[📖 Skywork-R1V3 Report](https://github.com/SkyworkAI/Skywork-R1V/blob/main/Skywork_R1V3.pdf)] </div></font>

Welcome to the Skywork-R1V3 repository! Here, you'll find the model weights and inference code for our state-of-the-art open-sourced multimodal reasoning model by reinforcement finetuning.

## 🔥 News

**July 9, 2025: 💥 We released Skywork-R1V3-38B [[🤗 Skywork-R1V3-38B](https://huggingface.co/Skywork/Skywork-R1V3-38B)], the latest and most powerful open-source multimodal reasoning model in the Skywork series, pushing the boundaries of multimodal and cross-disciplinary intelligence. Mainly through RL algorithm in post-training, R1V3 significantly enhances multimodal reasoning ablity and achieves open-source state-of-the-art (SOTA) performance across multiple multimodal reasoning benchmarks, e.g. 76.0 on MMMU.**

**April 28, 2025**: We released awq quantized version of Skywork R1V2[[🤗 Skywork-R1V2-38B-AWQ](https://huggingface.co/Skywork/Skywork-R1V2-38B-AWQ)], supporting single-card (above 30GB) inference.

 **April 24, 2025**: We released **Skywork-R1V2**, an advanced open-source multimodal reasoning model that demonstrates strong performance across a range of multimodal reasoning benchmarks including MMMU, MMMU-Pro, MathVista, and OlympiadBench.[[🤗 Skywork-R1V2-38B](https://huggingface.co/Skywork/Skywork-R1V2-38B)][[📖R1V2 Report](https://arxiv.org/abs/2504.16656)] 
 
**April 9, 2025**: Our technical report is currently available on arxiv: [[Skywork-R1V: Pioneering Multimodal Reasoning with CoT](https://arxiv.org/abs/2504.05599)].

**Mar 26, 2025**: We released awq quantized version of Skywork R1V[[🤗 Skywork-R1V-38B-AWQ](https://huggingface.co/Skywork/Skywork-R1V-38B-AWQ)], supporting single-card (above 30GB) inference.

**Mar 18, 2025**: We are thrilled to introduce Skywork R1V, the first industry open-sourced multimodal reasoning model with advanced visual chain-of-thought capabilities, pushing the boundaries of AI-driven vision and logical inference! 🚀


## 📊 Evaluation
Skywork-R1V3-38B demonstrates state-of-the-art performance on various multimodal reasoning tasks. We provide the code in [eval](https://github.com/SkyworkAI/Skywork-R1V/tree/main/eval) to reproduce these results.

**Comparison of Skywork-R1V3 with Multimodal Open-Source and Proprietary Models**

| Category       | Benchmark               | Metric  | Skywork-38B | QVQ-72B | InternVL-78B | Qwen-72B | Claude 3.7 | GPT-4o |
|----------------|-------------------------|---------|------------:|--------:|-------------:|--------:|----------:|---------:|
| **General**    | MMMU (val)              | Acc.    | 🏆 **76.0**   | 70.3    | 72.2         | 70.3    | 75.0      | 70.7   |
|                | EMMA (mini-cot)         | Acc.    | 40.3       | 32.0    | 38.3         | 39.3    | 🏆 **56.5**   | 36.0   |
|                | MMMU-pro                | Acc.    | 🏆 **55.4**   | 46.9*   | 48.6         | 51.1    | 50.0      | 54.5   |
|                | MMK12                   | Acc.    | 🏆 **78.5**    | 62.7*   | 67.4*        | 70.5*   | 55.3      | 49.9   |
|                | MMstar                  | Acc.    | 70.6       | 60.8    | 🏆 **72.5**     | 70.8    | 68.8      | 65.1   |
|                | MMBench-en-1.1          | Acc.    | 85.7       | 72.6*   | 87.7         | 🏆 **88.0** | 82.0      | 84.3   |
|                | HallusionBench          | Acc.    | 🏆 **61.3**   | 55.3*   | 59.1         | 55.2    | 58.3      | 56.2   |
| **Mathematics**| MathVista (mini)        | Acc.    | 77.1       | 71.4    | 🏆 **79.0**      | 74.8    | 66.8      | 62.9   |
|                | MathVerse (vision-only) | Acc.    | 🏆 **59.6**   | 45.1    | 51.0         | 57.6    | 49.9*     | 49.9   |
|                | MathVision              | Acc.    | 52.6       | 35.9    | 43.1         | 38.1    | 🏆 58.6   | 31.2   |
|                | WeMath (strict)          | Acc.    |🏆 **56.5**   | 37.7    | 46.1         | 50.6    | 48.9*     | 50.6   |
| **Logic**      | Visulogic               | Acc.    | 🏆 **28.5**   | 23.5*   | 27.7         | 26.2    | 25.9      | 26.3   |
|                | LogicVista              | Acc.    | 59.7       | 53.8    | 55.9         | 57.1    | 60.6*     | 🏆 **64.4** |
|                | MME-reasoning           | Acc.    | 🏆 **42.8**   | 35.2    | 32.1         | 34.1    | 34.1      | 30.2   |
| **Physics**    | PhyX (mc-text-minimal)  | Acc.    | 🏆 **52.8**    | 35.2*   | 40.5         | 44.8    | 41.6      | 43.8   |
|                | SeePhys                 | Acc.    | 31.5       | 22.5    | 19.0*        | 24.2    | 🏆 **34.6**   | 21.9   |

🏆 **Top performer** in each benchmark  
[*] indicates results from our evaluation framework.


**Performance Overview**

<img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/r1v3_eval2.png?raw=true" width="800"/>

 
## 🚀 How to Run Locally

### 1. Clone the Repository

```shell
git clone https://github.com/SkyworkAI/Skywork-R1V.git
cd skywork-r1v/inference
```

### 2. Set Up the Environment

```shell
# For Transformers  
conda create -n r1-v python=3.10 && conda activate r1-v  
bash setup.sh  
# For vLLM/evaluation  
conda create -n r1v-vllm python=3.10 && conda activate r1v-vllm  
bash ./eval/vlmevalkit/build_env.sh
```

### 3. Run the Inference Script

#### Using Transformers
```shell
CUDA_VISIBLE_DEVICES="0,1" python inference_with_transformers.py \
    --model_path path \
    --image_paths image1_path \
    --question "your question"
```
#### Using vLLM
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

This project uses the [InternVL3-38B](https://huggingface.co/OpenGVLab/InternVL3-38B) as the base model, which is licensed under the MIT License.

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
