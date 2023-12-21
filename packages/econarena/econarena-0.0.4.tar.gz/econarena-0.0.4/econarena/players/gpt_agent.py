from typing import Any, Optional

import openai

from .agent import Agent

class GPTAgent(Agent):
    model: str
    history: list
    def __init__(self, api_base: Optional[str] = None, api_key: str = None, model: str = "gpt-3.5-turbo", **kwargs) -> None:
        super().__init__()
        self.model = model
        self.history = []
        openai.api_base = api_base
        openai.api_key = api_key
    
    def _preprocess(self, role: str, content: str) -> dict:
        return {"role": role, "content": content}

    def receive_prompt(self, prompt: str) -> Any:
        self.history.append(self._preprocess(role="user", content=prompt))

    def _postprocess(self, response: dict) -> str:
        role = response["choices"][0]["message"]["role"] or "assistant"
        content = response["choices"][0]["message"]["content"].strip()
        self.history.append(self._preprocess(role=role, content=content))
        return content

    def generate_reply(self) -> Any:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history
        )
        return self._postprocess(response)
