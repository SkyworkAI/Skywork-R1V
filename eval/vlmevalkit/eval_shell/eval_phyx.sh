#!/bin/bash

export LMUData=./eval/vlmevalkit/eval_shell/LMUData
cd ./eval/vlmevalkit
set -e
#sleep 1h
export LMDEPLOY_API_KEY="kunlun"
export LMDEPLOY_API_BASE="http://127.0.0.1:8000/v1/chat/completions"

LOG_DIR="logs"
MODEL_NAME="Skywork_R1V3"

mkdir -p $LOG_DIR/$MODEL_NAME

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/$MODEL_NAME/phyx_eval_${TIMESTAMP}.log"

echo "Starting PHYX evaluation at $(date)" | tee -a "$LOG_FILE"

USE_COT=0 python run_phyx.py \
    --data PHYX \
    --model R1V3-alpha \
    --verbose \
    --reuse \
    --work-dir ./outputs/$MODEL_NAME \
    --judge gpt-4o-2024-05-13 \
    --api-nproc 200 2>&1 | tee -a "$LOG_FILE" &

PID=$!

echo "Evaluation process started with PID: $PID" | tee -a "$LOG_FILE"

wait $PID

if [ $? -eq 0 ]; then
    echo "Evaluation completed successfully at $(date)" | tee -a "$LOG_FILE"
else
    echo "Evaluation failed at $(date)" | tee -a "$LOG_FILE"
    exit 1
fi


