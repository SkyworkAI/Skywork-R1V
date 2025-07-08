import logging
import re
import base64
from io import BytesIO

from anthropic import Anthropic


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
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_base64
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


# build claude class
class Claude_Model():
    def __init__(
            self,
            client: Anthropic,
            model="claude-3-5-sonnet-latest",
            temperature=0,
            max_tokens=1024
    ):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def get_response(self, sample):
        messages = create_message(sample)
        try:

            v_response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=messages
            )
            response = v_response.content[0].text

            return response
        except Exception as e:
            print(e)
            return None
