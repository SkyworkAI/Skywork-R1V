#!/bin/bash

set -e
set -x

cd ./eval/vlmevalkit
export LMDEPLOY_API_KEY="kunlun"
export LMDEPLOY_API_BASE="http://127.0.0.1:8000/v1/chat/completions"

LOG_DIR="logs"
MODEL_NAME="Skywork-R1V3"

mkdir -p "$LOG_DIR/$MODEL_NAME"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/$MODEL_NAME/bench_${TIMESTAMP}.log"

echo "Starting evaluation at $(date)" | tee -a "$LOG_FILE"

# if first argument is empty, use default
if [ -z "$1" ]; then
    echo "⚠️  [INFO] No benchmark specified, defaulting to MMMU_DEV_VAL." | tee -a "$LOG_FILE"
    echo "👉  To evaluate on other benchmarks, run:"
    echo '    bash run_eval.sh "MMMU_DEV_VAL MathVista_MINI HallusionBench ..."'
    DATA_ARGS="MMMU_DEV_VAL"
else
    DATA_ARGS="$1"
fi

USE_COT=1 python run.py \
    --data $DATA_ARGS \
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
