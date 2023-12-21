from typing import Any

import google.generativeai as palm

from .agent import Agent

class PaLMAgent(Agent):
    model: str
    context: str
    messages: str
    def __init__(self, api_key: str, model: str = "models/chat-bison-001", **kwargs) -> None:
        super().__init__()
        self.api_key = api_key
        self.model = model
        self.context = ""
        self.messages = ""
        palm.configure(api_key=api_key)

    def receive_prompt(self, prompt: str) -> Any:
        self.messages = prompt

    def _postprocess(self, response: str) -> str:
        return response.strip()

    def generate_reply(self) -> Any:
        response = palm.chat(
            context=self.context,
            messages=self.messages,
            model=self.model
        )
        return self._postprocess(response.last)
