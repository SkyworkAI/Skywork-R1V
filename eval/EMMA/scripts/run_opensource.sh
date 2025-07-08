#!/bin/bash
 python generate_response.py \
 --dataset_name 'luckychao/EMMA' \
 --split 'test' \
 --subject 'Math' 'Physics' 'Chemistry' 'Coding' \
 --strategy 'CoT' \
 --config_path 'configs/gpt.yaml' \
 --model_path 'path_to_your_local_model' \
 --output_path 'path_to_output_file' \
 --max_tokens 4096 \
 --temperature 0.7 \
 --save_every 20


































