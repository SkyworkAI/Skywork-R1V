import requests
import time
import os
import hashlib
import json
import uuid

# 调用代理，请使用过内部vpn【zjk】或者找 韩广 开放白名单

host = 'https://gpt-us.singularity-ai.com'    # aws这个只有美国链路支持

# url = host + "/gpt-proxy/aws/claude/haiku35"
# url = host + "/gpt-proxy/aws/claude/sonnet35"
# url = host + "/gpt-proxy/aws/claude/sonnet35/v2"
url = host + "/gpt-proxy/aws/claude/sonnet37"

app_key = "gpt-297e11bfb636a9999c70a9ad04e1"        # 这里需要替换你的APPKey
if app_key == '':
    print("not set env var GPTAppKey")
    exit(1)

headers = {
    "app_key": app_key,
    "Content-Type": "application/json"
}

data = {
    "model": "claude-3.7-sonnet-thinking", # claude35-sonnet
    "messages": [
        {
            "role": "user",
            "content": "写一个请假申请"
        }
    ],
    "temperature": 0.8,
    "top_p":        1,
    # "stream": True
    
    # claude37-sonnet 支持cot数据返回
    # 如果需要cot数据的话，添加如下参数
    # 如果开启，那么 temperature 必须为1，top_p 不能传
    # "thinking": {
    #     "type": "enabled",
    #     "budget_tokens": 16000 # 注意这个参数一定要比max_tokens小
    # },
    
    # 如果你想使用prompt_cache功能，参考如下写法
    # https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
    # {
    #     "role": "user",
    #     "content": [
    #         {
    #             "type": "text",
    #             "text": "What is the weather like in San Francisco?",
    #             "cache_control": {
    #                 "type": "ephemeral"
    #             }
    #         }
    #     ]
    # }
}


try:
    response = requests.request('POST', url, json=data, headers=headers)
    resp_struct = json.loads(response.text)
    print(response.status_code)
    # 处理响应流
    print(resp_struct)
    # print(response.text)
    # resp_struct = json.loads(response.text)
except Exception as e:
    print(e)