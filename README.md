<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

# Skywork-R1V: Pioneering Multimodal Reasoning with CoT
<font size=7><div align='center' >  [[🤗 Skywork-R1V2-38B](https://huggingface.co/Skywork/Skywork-R1V2-38B)] [[🤖 R1V2 ModelScope](https://modelscope.cn/models/Skywork/Skywork-R1V2-38B)] [[📖R1V2 Report](https://github.com/SkyworkAI/Skywork-R1V/blob/main/Skywork_R1V2.pdf)] <br></br>[[🤗 Skywork-R1V-38B](https://huggingface.co/Skywork/Skywork-R1V-38B)] [[📖R1V1 Report](https://arxiv.org/abs/2504.05599)] </div></font>


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

 **April 24, 2025**: We released **Skywork-R1V2**, a state-of-the-art, open-source multimodal reasoning model that achieves leading performance across multiple vision-language benchmarks.[[🤗 Skywork-R1V2-38B](https://huggingface.co/Skywork/Skywork-R1V2-38B)][[📖R1V2 Report](https://github.com/SkyworkAI/Skywork-R1V/blob/main/Skywork_R1V2.pdf)] [ArXiv (to be updated)]
 
**April 9, 2025**: Our technical report is currently available on arxiv: [[Skywork-R1V: Pioneering Multimodal Reasoning with CoT](https://arxiv.org/abs/2504.05599)].

**April 1, 2025**: Skywork-R1V supports inference with [[vLLM](https://github.com/vllm-project/vllm)], On 4×L20Y GPUs, vLLM generates 1k tokens in ~12.3s, at least 5× faster than transformers.

**Mar 26, 2025**: We released awq quantized version of Skywork R1V[[🤗 Skywork-R1V-38B-AWQ](https://huggingface.co/Skywork/Skywork-R1V-38B-AWQ)], supporting single-card (above 30GB) inference.

**Mar 18, 2025**: We are thrilled to introduce Skywork R1V, the first industry open-sourced multimodal reasoning model with advanced visual chain-of-thought capabilities, pushing the boundaries of AI-driven vision and logical inference! 🚀



## R1V2-38B Evaluation
 Skywork-R1V2-38B demonstrates state-of-the-art performance on both text and multimodal reasoning tasks.
 <div align="center">
   <b>Comparison of Skywork-R1V2 with Multimodal Open-Source and Proprietary Models</b>
 </div>
 
 <table align="center">
   <thead>
     <tr>
       <th rowspan="2">Model</th>
       <th colspan="5" align="center"><strong>Text Reasoning (pass@1 or %)</strong></th>
       <th colspan="5" align="center"><strong>Multimodal Reasoning (%)</strong></th>
     </tr>
     <tr>
       <th>AIME24</th>
       <th>LiveCodebench</th>
       <th>liveBench</th>
       <th>IFEVAL</th>
       <th>BFCL</th>
       <th>MMMU(val)</th>
       <th>MathVista(mini)</th>
       <th>MathVision(mini)</th>
       <th>OlympiadBench</th>
       <th>mmmu-pro</th>
     </tr>
   </thead>
   <tbody>
     <tr>
       <td><strong>Skywork-R1V2-38B</strong></td>
       <td align="center"><strong>78.9</strong></td>
       <td align="center"><strong>63.6</strong></td>
       <td align="center"><strong>73.2</strong></td>
       <td align="center"><strong>82.9</strong></td>
       <td align="center"><strong>66.3</strong></td>
       <td align="center"><strong>73.6</strong></td>
       <td align="center">74.0</td>
       <td align="center">49.0</td>
       <td align="center"><strong>62.6</strong></td>
       <td align="center"><strong>52.0</strong></td>
     </tr>
     <tr>
       <td>OpenAI-4o</td>
       <td align="center">74.6</td>
       <td align="center">9.3</td>
       <td align="center">49.9</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">69.1</td>
       <td align="center">63.8</td>
       <td align="center"><strong>58.0</strong></td>
       <td align="center">—</td>
       <td align="center">—</td>
     </tr>
     <tr>
       <td>Claude 3.5 Sonnet</td>
       <td align="center">16.0</td>
       <td align="center">—</td>
       <td align="center">65.0</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">66.4</td>
       <td align="center">65.3</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
     </tr>
     <tr>
       <td>Kimi k1.5</td>
       <td align="center">77.5</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">70.0</td>
       <td align="center">74.9</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
     </tr>
     <tr>
       <td>Qwen2.5-VL-72B</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">70.2</td>
       <td align="center">74.8</td>
       <td align="center">38.1</td>
       <td align="center">40.4</td>
       <td align="center">—</td>
     </tr>
     <tr>
       <td>InternVL3-38B</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">—</td>
       <td align="center">70.1</td>
       <td align="center"><strong>75.1</strong></td>
       <td align="center">34.2</td>
       <td align="center">-</td>
       <td align="center">—</td>
     </tr>
   </tbody>
 </table>
 
 
 <br></br>
 <div align="center">
   <b>Text Reasoning Performance</b>
 </div>
 <div align="center">
   <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/text_reasoning.png?raw=true" width="100%" alt="text_reasoning" />
 </div>
 
 <br></br>
 <div align="center">
   <b>Multimodal Reasoning vs Proprietary Models</b>
 </div>
 <div align="center">
   <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/multi_reasoning_pm.png?raw=true" width="100%" alt="multi_reasoning_pm" />
 </div>
 
 <br></br>
 <div align="center">
   <b>Multimodal Reasoning vs Open-Source Models</b>
 </div>
 <div align="center">
   <img src="https://github.com/SkyworkAI/Skywork-R1V/blob/main/imgs/multi_reasoning_osm.png?raw=true" width="100%" alt="multi_reasoning_osm" />
 </div>
 
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
      author={Chris and Yichen Wei and Yi Peng and Xiaokun Wang and Weijie Qiu and Wei Shen and Tianyidan Xie and Jiangbo Pei and Jianhao Zhang and Yunzhuo Hao and Xuchen Song and Yang Liu and Yahui Zhou},
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
      author={Yi Peng and Chris and Xiaokun Wang and Yichen Wei and Jiangbo Pei and Weijie Qiu and Ai Jian and Yunzhuo Hao and Jiachun Pan and Tianyidan Xie and Li Ge and Rongxian Zhuang and Xuchen Song and Yang Liu and Yahui Zhou},
      year={2025},
      eprint={2504.05599},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2504.05599}, 
}
```
