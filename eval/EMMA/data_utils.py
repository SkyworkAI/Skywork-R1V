import yaml
import json


def load_yaml(file_path):
    with open(file_path, 'r') as stream:
        try:
            yaml_dict = yaml.safe_load(stream)
            return yaml_dict
        except yaml.YAMLError as exc:
            print(exc)
            return None


def verify_response(response):
    if isinstance(response, str):
        response = response.strip()
    if response == "" or response is None:
        return False
    if "Response Error" in response:
        return False
    return True


def build_query(sample, config, strategy):
    """Build the text query by combining the context, question and options. The <image_n> token is still there"""
    context = sample['context']
    question = sample['question']
    example = ""
    res_dict = {}
    if sample['type'].lower() == 'multiple choice':
        options = sample['options']
        start_chr = 'A'
        for option in options:
            example += f"{start_chr}: {option}\n"
            start_chr = chr(ord(start_chr) + 1)
        empty_prompt_sample_structure = config['multi_choice_format']
        empty_prompt = empty_prompt_sample_structure.format(context=context, question=question, options=example)
        if strategy == 'CoT':
            res_dict['query'] = empty_prompt + config['Strategy_Instruction']['CoT']
        else:
            res_dict['query'] = empty_prompt + config['Strategy_Instruction']['Directly']

        res_dict['gt_content'] = options[ord(sample['answer'].upper()) - ord('A')]
    else:
        empty_prompt_sample_structure = config['open_ended_format']
        empty_prompt = empty_prompt_sample_structure.format(context=context, question=question)
        if strategy == 'CoT':
            res_dict['query'] = empty_prompt + config['Strategy_Instruction']['CoT']
        else:
            res_dict['query'] = empty_prompt + config['Strategy_Instruction']['Directly']
        res_dict['gt_content'] = sample['answer']

    # append existing key and value in data
    res_dict.update(sample)
    return res_dict
