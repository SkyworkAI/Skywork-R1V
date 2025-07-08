import re
import logging

import torch
from transformers import AutoProcessor, LlavaOnevisionForConditionalGeneration

def create_message(sample):
    query = sample['query']
    all_contents = []
    matches = re.findall(r"<(image_\d+)>", query)
    split_text = re.split(r"<image_\d+>", query)
    images = []
    for i, fragment in enumerate(split_text):
        if fragment.strip():
            all_contents.extend([
                {"type": "text", "text": fragment}
            ])
        if i < len(matches):
            if sample[matches[i]]:
                all_contents.extend([
                    {"type": "image"}
                ])
                images.append(sample[matches[i]])
            else:
                logging.error(
                    f"The image token {matches[i]} is in the query, but there is no corresponding image provided by the data")
    messages = [
        {
            "role": "user",
            "content": all_contents
        }
    ]
    return messages, images


class Llava_Model:
    def __init__(
            self,
            model_path,
            temperature=0,
            max_tokens=1024
    ):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = LlavaOnevisionForConditionalGeneration.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            use_flash_attention_2=True
        )
        self.processor = AutoProcessor.from_pretrained(model_path)


    def get_response(self, sample):

        model = self.model
        processor = self.processor

        try:
            messages, images = create_message(sample)

            input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
            inputs = processor(
                images=images,
                text=input_text,
                add_special_tokens=False,
                return_tensors="pt"
            ).to(model.device, torch.float16)

            output = model.generate(**inputs, do_sample=True, temperature=self.temperature, max_new_tokens=self.max_tokens)
            response = processor.decode(output[0], skip_special_tokens=True)

            assistant_index = response.find("assistant")
            if assistant_index != -1:
                final_answer = response[assistant_index + len("assistant"):].strip()
            else:
                final_answer = response.strip()
            return final_answer

        except Exception as e:
            print(e)
            return None