
#!/bin/bash
cd ./eval/EMMA

SUBJECT="Math Coding Physics Chemistry" # You can use multiple subjects separated by spaces
STRATEGY="CoT" # CoT or Direct
SUBJECT_FORMATTED=$(echo $SUBJECT | tr ' ' '_')

MODEL_PATH="/path/to/your/model/path"
MODEL=$(basename "$MODEL_PATH")
DATASET_NAME="/path/to/your/dataset/path"
MAX_TOKENS=64000
TEMPERATURE=0.7
SAVE_EVERY=3
SPLIT="test"
CONFIG_PATH="configs/gpt.yaml"

# Construct output and log file paths
OUTPUT_FILE="results/EMMA-mini/open-source/${MODEL}_${SUBJECT_FORMATTED}_${STRATEGY}.json"
# LOG_FILE="logs/${MODEL}_${SUBJECT_FORMATTED}_${STRATEGY}.log"
mkdir -p "$(dirname "$OUTPUT_FILE")"
# mkdir -p "$(dirname "$LOG_FILE")"

# Print constructed file paths for debugging
echo "==============================================="
echo "🚀 Starting Script Execution"
echo "-----------------------------------------------"
echo "---- Model:          ${MODEL}"
echo "📁 Output File Path: ${OUTPUT_FILE}"
echo "📝 Log File Path:    ${LOG_FILE}"
echo "==============================================="


# source ~/miniconda3/etc/profile.d/conda.sh
# conda activate internvl
# pip uninstall -y apex
# pip install timm 
# pip install qwen_vl_utils


export CUDA_VISIBLE_DEVICES="0,1,2,3"
python generate_response.py  \
  --dataset_name $DATASET_NAME \
  --subject $SUBJECT \
  --split $SPLIT \
  --strategy $STRATEGY \
  --output_path $OUTPUT_FILE \
  --model_path $MODEL_PATH \
  --config_path $CONFIG_PATH \
  --max_tokens $MAX_TOKENS \
  --temperature $TEMPERATURE \
  --save_every $SAVE_EVERY
# Completion message
echo "✅ Script launched successfully!"
echo "==============================================="


