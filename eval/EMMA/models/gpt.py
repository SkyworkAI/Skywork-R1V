import logging
import re
import base64
from io import BytesIO
import time

from openai import OpenAI


def encode_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def create_message(sample):
    query = sample['query']
    all_contents = []
    matches = re.findall(r"<(image_\d+)>", query)
    split_text = re.split(r"<image_\d+>", query)
    for i, fragment in enumerate(split_text):
        if fragment.strip():
            all_contents.extend([
                {"type": "text", "text": fragment}
            ])
        if i < len(matches):
            if sample[matches[i]]:
                img_base64 = encode_image_to_base64(sample[matches[i]])
                all_contents.extend([
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ])
            else:
                logging.error(
                    f"The image token {matches[i]} is in the query, but there is no corresponding image provided by the data")

    messages = [
        {
            "role": "user",
            "content": all_contents
        }
    ]
    return messages


# build gpt class
class GPT_Model:
    def __init__(
            self,
            client: OpenAI,
            model="chatgpt-4o-latest",
            temperature=0,
            max_tokens=1024,
            retry_attempts = 5
    ):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.retry_attempts = retry_attempts

    def get_response(self, sample):
        attempt = 0
        messages = create_message(sample)

        while attempt < self.retry_attempts:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )

                return response.choices[0].message.content.strip()
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")

                if 'error' in str(e) and 'message' in str(e):
                    error_message = str(e)
                    if 'The server had an error processing your request.' in error_message:
                        sleep_time = 30
                        logging.error(f"Server error, retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                    elif 'Please try again in ' in error_message:
                        sleep_time = float(error_message.split('Please try again in ')[1].split('s.')[0])
                        logging.error(f"Rate limit exceeded, retrying in {sleep_time * 2}s...")
                        time.sleep(sleep_time * 2)
                    elif 'RESOURCE_EXHAUSTED' in error_message:
                        sleep_time = 30
                        logging.error(f"Gemini rate limit, retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                    else:
                        print("Unknown error, skipping this request.")
                        break
                attempt += 1

        return None
