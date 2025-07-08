import openai
import os
import json
import time
import re
import pandas as pd
from tqdm import tqdm
from tenacity import retry, wait_random_exponential, stop_after_attempt
def rule_based_evaluation(item):
    prediction = str(item['prediction'])
    answer = str(item['answer']).strip()
    boxed_matches = re.findall(r'\\boxed\{(.*?)\}', prediction)
    if not boxed_matches:
        return False, ""
    last_boxed = boxed_matches[-1].strip()
    def normalize(s):
        s = re.sub(r'\$|\\[a-z]+|\s+', '', s)
        s = re.sub(r'^\{|\}$', '', s)
        return s.lower()
    if last_boxed == answer or normalize(last_boxed) == normalize(answer):
        return True, f"规则匹配：预测的 \\boxed{{{last_boxed}}} 与标准答案 '{answer}' 一致"
        
    return False, ""

def process_one(item):
    if not str(item['id']).startswith('val'):
        return item
    rule_match, explanation = rule_based_evaluation(item)
    if rule_match:
        item["is_correct"] = True
        item["explanation"] = explanation
        item["gpt_score"] = "规则匹配成功，跳过GPT评分"
        return item
    
    item["gpt_score"] =""  # str(e)
    item["is_correct"] = False
    item["explanation"] = "评分请求失败"
    return item

def calculate_accuracy(jsonl_path):
    correct, total, original_hit, rule_matched = 0, 0, 0, 0
    single_total,single_acc=0,0
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if not str(data.get('id', '')).startswith('val'):
                continue
            
            total += 1
            if not "image 2" in data.get('question', '') and not "image" in data.get('A',''):
                single_total+=1
            
            if data.get('is_correct'):
                correct += 1
                
            if data.get('hit', 0) == 1:
                original_hit += 1
                if not "image 2" in data.get('question', '') and not "image" in data.get('A',''):
                    single_acc+=1
            if "规则匹配" in data.get('explanation', '') and data.get('is_correct', False):
                if data.get('hit', 0) == 0:
                    rule_matched += 1
                    if not "image 2" in data.get('question', '') and not "image" in data.get('A',''):
                        single_acc+=1
            
    if total > 0:
        print(f"\n正确率统计:")
        print(f"- 总val数据量: {total}")
        print(f"- 原始hit=1数量: {original_hit} ({original_hit / total * 100:.2f}%)")
        print(f"- 规则匹配补正数量: {rule_matched} ({rule_matched / total * 100:.2f}%)")
        print(f"- 总正确数量: {original_hit+rule_matched} ({(original_hit+rule_matched) / total * 100:.2f}%)")
        
    else:
        print("无可统计数据")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='评估回答的准确性')
    parser.add_argument('--input', type=str, default='')
    parser.add_argument('--output', type=str, default='./eval/vlmevalkit/outputs/Skywork-R1V3/R1V3-alpha/R1V3-alpha_MMMU_DEV_VAL_gpt4o_rule_based.jsonl')
    
    args = parser.parse_args()

    df = pd.read_excel(args.input)
    data = df.to_dict('records')

    with open(args.output, 'w', encoding='utf-8') as f_out:
        for item in tqdm(data):
            processed = process_one(item)
            f_out.write(json.dumps(processed, ensure_ascii=False) + '\n')
            f_out.flush()

    calculate_accuracy(args.output)
    print("任务完成，结果已写入文件。")
    


    # 新增：收集分类样本
    hit0_rule_correct = []
    hit1_rule_wrong = []

    with open(args.output, 'w', encoding='utf-8') as f_out:
        for item in tqdm(data):
            processed = process_one(item)
            f_out.write(json.dumps(processed, ensure_ascii=False) + '\n')
            f_out.flush()


            if str(processed.get('id', '')).startswith('val'):
                is_correct = processed.get('is_correct', False)
                explanation = processed.get('explanation', '')
                hit = processed.get('hit', 0)
                if hit == 0 and is_correct and "规则匹配" in explanation:
                    hit0_rule_correct.append(processed)
                elif hit == 1 and (not is_correct or "规则匹配" not in explanation):
                    hit1_rule_wrong.append(processed)


    def save_to_excel(data_list, output_path):
        if not data_list:
            print(f"无数据可写入 {output_path}")
            return
        df_out = pd.DataFrame(data_list)
        df_out.to_excel(output_path, index=False)
        print(f"写入完成：{output_path}")


    base_dir = os.path.dirname(args.output)
    save_to_excel(hit0_rule_correct, os.path.join(base_dir, 'hit0_rule_matched.xlsx'))
    save_to_excel(hit1_rule_wrong, os.path.join(base_dir, 'hit1_rule_failed.xlsx'))
