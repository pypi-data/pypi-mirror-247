from typing import Any

import google.generativeai as genai

from .agent import Agent

class GeminiAgent(Agent):
    model: str
    message: str
    gen_model: object
    chat: object
    def __init__(self, api_key: str, model: str = "gemini-pro", **kwargs) -> None:
        super().__init__()
        self.api_key = api_key
        self.model = model
        self.message = ""
        genai.configure(api_key=api_key)
        self.gen_model = genai.GenerativeModel(model_name=model)
        self.chat = self.gen_model.start_chat()

    def receive_prompt(self, prompt: str) -> Any:
        self.message = prompt

    def _postprocess(self, response: str) -> str:
        return response.strip()

    def generate_reply(self) -> Any:
        response = self.chat.send_message(self.message)
        return self._postprocess(response.text)
