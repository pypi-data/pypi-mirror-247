import hashlib
import json
import time
from typing import Any, Optional

import requests

from .agent import Agent

def calculate_md5(input_string):
    md5 = hashlib.md5()
    md5.update(input_string.encode("utf-8"))
    encrypted = md5.hexdigest()
    return encrypted

class BaichuanAgent(Agent):
    api_base: str
    api_key: str
    secret_key: str
    model: str
    history: list
    def __init__(self, api_base: Optional[str] = None, api_key: str = None, secret_key: Optional[str] = None, model: str = "Baichuan2", **kwargs) -> None:
        super().__init__()
        self.api_base = api_base
        self.api_key = api_key
        self.secret_key = secret_key
        self.model = model
        self.history = []

    def _preprocess(self, role: str, content: str) -> dict:
        return {"role": role, "content": content}

    def receive_prompt(self, prompt: str) -> Any:
        self.history.append(self._preprocess(role="user", content=prompt))

    def _postprocess(self, response: dict) -> str:
        role = response["data"]["messages"][0]["role"] or "assistant"
        content = response["data"]["messages"][0]["content"]
        self.history.append(self._preprocess(role=role, content=content))
        return content

    def generate_reply(self) -> Any:
        data = {
            "model": self.model,
            "messages": self.history
        }
        json_data = json.dumps(data)
        time_stamp = int(time.time())
        signature = calculate_md5(self.secret_key + json_data + str(time_stamp))
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-BC-Request-Id": "your requestId",
            "X-BC-Timestamp": str(time_stamp),
            "X-BC-Signature": signature,
            "X-BC-Sign-Algo": "MD5",
        }
        response = requests.post(self.api_base, data=json_data, headers=headers)
        return self._postprocess(eval(response.text))
