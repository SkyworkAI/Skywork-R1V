#!/bin/bash

# 设置错误时退出
export LMUData=./eval/vlmevalkit/eval_shell/LMUData
cd ./eval/vlmevalkit
set -e
#sleep 1h
export LMDEPLOY_API_KEY="kunlun"
export LMDEPLOY_API_BASE="http://127.0.0.1:8000/v1/chat/completions"

# 创建日志目录
LOG_DIR="logs"
MODEL_NAME="Skywork_R1V3"

mkdir -p $LOG_DIR/$MODEL_NAME

# 生成带时间戳的日志文件名
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/$MODEL_NAME/phyx_eval_${TIMESTAMP}.log"

# 记录开始时间
echo "Starting PHYX evaluation at $(date)" | tee -a "$LOG_FILE"

# 运行评估脚本
USE_COT=0 python run_phyx.py \
    --data PHYX \
    --model R1V3-alpha \
    --verbose \
    --reuse \
    --work-dir ./outputs/$MODEL_NAME \
    --judge gpt-4o-2024-05-13 \
    --api-nproc 200 2>&1 | tee -a "$LOG_FILE" &

# 获取后台进程ID
PID=$!

# 记录进程ID
echo "Evaluation process started with PID: $PID" | tee -a "$LOG_FILE"

# 等待进程完成
wait $PID

# 检查进程退出状态
if [ $? -eq 0 ]; then
    echo "Evaluation completed successfully at $(date)" | tee -a "$LOG_FILE"
else
    echo "Evaluation failed at $(date)" | tee -a "$LOG_FILE"
    exit 1
fi


