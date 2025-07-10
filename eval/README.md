# 🧪 Evaluation Reproduction


We provide evaluation scripts to reproduce the results of **Skywork R1V3**.

Most benchmarks can be evaluated using **[VLMEvalKit](https://github.com/open-compass/VLMEvalKit)**

---
## ⚙️ Environment Setup

Install all dependencies:

```bash
bash ./eval/vlmevalkit/build_env.sh
```
### Set OpenAI API Key and Base URL
Create or edit the `.env` file in `vlmevalkit/` and add the following:

```dotenv
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://your_base_url_here
```
## 🚀 Evaluation Steps
**Step 1: Launch the Model**

Start possible setting, and deploy the model
```bash
export TORCH_CUDA_ARCH_LIST="8.9+PTX" # optional
bash ./vlmevalkit/eval_shell/launch_vlm.sh
```
**Step 2: Run Evaluation Scripts**

Evaluate on supported benchmarks:
```bash
bash ./vlmevalkit/eval_shell/run_eval.sh
```
> ⚠️ **Note:** Some benchmarks (e.g., `MMMU`) require post-processing to adjust results using rule-based scripts. For PhyX evaluation, you need to download the TSV dataset from [here](https://huggingface.co/datasets/catpp/skywork-r1v3-phy_tsv) and place it in the `./eval/vlmevalkit/eval_shell/LMUData` directory.



# 📌 Additional Notes
- Ensure the model is properly loaded before running evaluation.
- All results will be saved under the `outputs/` directory.
- For EMMA-mini and MMK12, please refer to [EMMA-mini](https://github.com/EMMA-Bench/EMMA) and [MMK12](https://github.com/ModalMinds/MM-EUREKA) for evaluation instructions.

