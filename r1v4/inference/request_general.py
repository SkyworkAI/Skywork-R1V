import requests
import json

# Configuration - Please fill in your own values
SERVER_URL = ""  # TODO: Fill in your server URL
API_KEY = ""  # TODO: Fill in your API key

MODEL_NAME = "skywork/r1v4-general"

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
