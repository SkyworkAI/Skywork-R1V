DATA_ARGS="LogicVista"
bash ./eval/vlmevalkit/eval_shell/eval_bench.sh "$DATA_ARGS"

if [[ "$DATA_ARGS" == *"MMMU_DEV_VAL"* ]] || [[ "$DATA_ARGS" == *"MMMU_Pro_10c"* ]]; then
    echo ""
    echo "✅ [NOTICE] Running the rule-based check script for MMMU..."
    python ./eval/vlmevalkit/eval_shell/rule_base_mmmu.py \
      --input ./eval/vlmevalkit/outputs/Skywork-R1V3/R1V3-alpha/R1V3-alpha_MMMU_DEV_VAL_gpt4o_result.xlsx
elif [[ "$DATA_ARGS" == *"LogicVista"* ]]; then
    echo ""
    echo "✅ [NOTICE] Running the rule-based check script for LogicVista..."
    python ./eval/vlmevalkit/eval_shell/rule_base_logicvista.py \
      --input ./eval/vlmevalkit/outputs/Skywork-R1V3/R1V3-alpha/R1V3-alpha_LogicVista_gpt4o-mini.xlsx
fi
