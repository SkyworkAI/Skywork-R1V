pip install -r ./eval/vlmevalkit/requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple
pip install vllm==0.8.3 -i https://mirrors.bfsu.edu.cn/pypi/web/simple
export TORCH_CUDA_ARCH_LIST="8.9+PTX"
pip install -U torchao -i https://mirrors.bfsu.edu.cn/pypi/web/simple
apt-get update && apt-get install libgl1
pip install modelscope
