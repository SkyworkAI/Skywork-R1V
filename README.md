<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

# Skywork-R1V: Pioneering Multimodal Reasoning with CoT
<font size=7><div align='center' >  [[🤗 Skywork-R1V3-38B](https://huggingface.co/Skywork/Skywork-R1V3-38B)] [[📖 R1V1 Report]([https://arxiv.org/abs/2504.05599](https://github.com/SkyworkAI/Skywork-R1V/blob/main/Skywork_R1V3.pdf))] </div></font>


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

<br></br>
Welcome to the Skywork-R1V repository! Here, you'll find the model weights and inference code for our state-of-the-art open-sourced multimodal reasoning model, enabling advanced visual and text thinking.

## 🔥News

**July 9, 2025**: We released Skywork-R1V3-38B [[🤗 Skywork-R1V3-38B](https://huggingface.co/Skywork/Skywork-R1V3-38B)], the latest and most powerful open-source multimodal reasoning model in the Skywork series, pushing the boundaries of multimodal and cross-disciplinary intelligence. With elaborate RL algorithm in the post-training stage, R1V3 significantly enhances multimodal reasoning ablity and achieves open-source state-of-the-art (SOTA) performance across multiple multimodal reasoning benchmarks.

**April 28, 2025**: We released awq quantized version of Skywork R1V2[[🤗 Skywork-R1V2-38B-AWQ](https://huggingface.co/Skywork/Skywork-R1V2-38B-AWQ)], supporting single-card (above 30GB) inference.

 **April 24, 2025**: We released **Skywork-R1V2**, an advanced open-source multimodal reasoning model that demonstrates strong performance across a range of multimodal reasoning benchmarks including MMMU, MMMU-Pro, MathVista, and OlympiadBench.[[🤗 Skywork-R1V2-38B](https://huggingface.co/Skywork/Skywork-R1V2-38B)][[📖R1V2 Report](https://arxiv.org/abs/2504.16656)] 
 
**April 9, 2025**: Our technical report is currently available on arxiv: [[Skywork-R1V: Pioneering Multimodal Reasoning with CoT](https://arxiv.org/abs/2504.05599)].

**April 1, 2025**: Skywork-R1V supports inference with [[vLLM](https://github.com/vllm-project/vllm)], On 4×L20Y GPUs, vLLM generates 1k tokens in ~12.3s, at least 5× faster than transformers.

**Mar 26, 2025**: We released awq quantized version of Skywork R1V[[🤗 Skywork-R1V-38B-AWQ](https://huggingface.co/Skywork/Skywork-R1V-38B-AWQ)], supporting single-card (above 30GB) inference.

**Mar 18, 2025**: We are thrilled to introduce Skywork R1V, the first industry open-sourced multimodal reasoning model with advanced visual chain-of-thought capabilities, pushing the boundaries of AI-driven vision and logical inference! 🚀



## R1V3-38B Evaluation
 Skywork-R1V3-38B demonstrates state-of-the-art performance on multiple multimodal reasoning tasks.

**Comparison of Skywork-R1V3 with Multimodal Open-Source and Proprietary Models**

<img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/r1v3_eval.png?raw=true" width="800"/>

**Performance Overview**

<img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/r1v_eval1.png?raw=true" width="800"/>

 
## How to Run Locally

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
# For vLLM  
conda create -n r1v-vllm python=3.10 && conda activate r1v-vllm  
pip install -U vllm  
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


## Citation
If you use Skywork-R1V in your research, please cite:
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
