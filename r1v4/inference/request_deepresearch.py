# Deep Research Mode

# This mode is e2e, thus the output is a single string
# you could use specific extraction methods to get the desired content

import requests
import json

# Configuration - Please fill in your own values
SERVER_URL = ""  # TODO: Fill in your server URL
API_KEY = ""  # TODO: Fill in your API key

MODEL_NAME = "skywork/r1v4-deepresearch"

# Check required configuration
if not SERVER_URL or not API_KEY:
    raise ValueError("Please set SERVER_URL and API_KEY variables in the script")


def encode_image_to_base64(image_path):
    import base64

    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def encode_image(image_path):
    # Convert image path to base64 encoded string
    from mimetypes import guess_type

    mime_type, _ = guess_type(image_path)
    return f"data:{mime_type};base64,{encode_image_to_base64(image_path)}"


def query(messages, max_tokens=8192, temperature=0.2):
    # you could also use stream=True to get the stream output

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        # you can set other parameters as you want, for example:
        # "top_p": 0.9, # you can set top_p as you want
        # "presence_penalty": 0.5, # you can set presence_penalty as you want
        # "stop": ["<end_of_text>"], # you can set stop as you want
        # ....
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    response = requests.post(SERVER_URL, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


pure_text_messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "your question here"},
        ],
    },
]

multi_modal_messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {"url": encode_image("your image path here")},
            },
            {"type": "text", "text": "your question here"},
        ],
    },
]

pure_text_model_output = query(pure_text_messages)
print(pure_text_model_output)

multi_modal_model_output = query(multi_modal_messages)
print(multi_modal_model_output)

# the output is a multi-turn conversation like <think>...</think> <image_search>...</image_search> <observation>...</observation> <think>...</think> <text_search>...</text_search> <observation>...</observation> <think>...</think> <answer>...</answer>
# you could extract every turn of the conversation and the specific content from each turn
import re


def extract_turns(model_output):
    """
    Extract turns from model output.
    Each turn is a dict containing:
    - think: the thinking content
    - tool_name: the tool name (image_search/text_search/web_content/code/answer)
    - tool-specific key: image_path/query/url/code/answer
    - observation: the observation content (if not answer)
    """
    turns = []

    # Pattern to match think + tool + observation (or answer)
    # Match pattern: <think>...</think> followed by a tool tag
    pattern = r"<think>(.*?)</think>\s*<(\w+)>(.*?)</\2>(?:\s*<observation>(.*?)</observation>)?"

    matches = re.finditer(pattern, model_output, re.DOTALL)

    for match in matches:
        think_content = match.group(1).strip()
        tool_name = match.group(2)
        tool_content = match.group(3).strip()
        observation_content = match.group(4).strip() if match.group(4) else None

        turn = {"think": think_content, "tool_name": tool_name}

        # Add tool-specific key based on tool_name
        if tool_name == "image_search":
            turn["image_path"] = tool_content
        elif tool_name == "text_search":
            turn["query"] = tool_content
        elif tool_name == "web_content":
            turn["url"] = tool_content
        elif tool_name == "answer":
            turn["answer"] = tool_content
        else:
            # For other tools, use a generic "content" key
            turn["content"] = tool_content

        # Add observation if it exists (not for answer)
        if observation_content:
            turn["observation"] = observation_content

        turns.append(turn)

    return turns


extracted_turns = extract_turns(pure_text_model_output)

# the observation of image_search and text_search is a json string from web search, you could use json.loads to parse it

# for text_search, the schema is like this:
#   [
#         {
#             "title": "the title of the search result",
#             "url": "the url of the search result",
#             "snippet": "the snippet of the search result"
#         }
#   ]
for turn in extracted_turns:
    if turn["tool_name"] == "text_search":
        text_search_observation = json.loads(turn["observation"])
        print(text_search_observation)

# for image_search, the schema is like this:
#   [
#         {
#             "title": "the title of the search result",
#             "source": "the corresponding image url",
#             "link": "the url of the search result"
#         }
#   ]
for turn in extracted_turns:
    if turn["tool_name"] == "image_search":
        image_search_observation = json.loads(turn["observation"])
        print(image_search_observation)

# the observation of web_content is a summarized web content of a specific url
for turn in extracted_turns:
    if turn["tool_name"] == "web_content":
        web_content_observation = json.loads(turn["observation"])
        print(web_content_observation)

# if you just want to get the answer, you could get it from the last turn
for turn in extracted_turns:
    if turn["tool_name"] == "answer":
        answer = turn["answer"]
        print(answer)
