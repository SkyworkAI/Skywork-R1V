set -x
MODEL_PATH=/path/to/r1v3-model
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python -m vllm.entrypoints.openai.api_server --model $MODEL_PATH --port 8000 --trust-remote-code --max_model_len 32768 --served-model-name r1v3-alpha --limit-mm-per-prompt "image=60" --gpu_memory_utilization 0.8 --tensor-parallel-size 8 --dtype auto 

