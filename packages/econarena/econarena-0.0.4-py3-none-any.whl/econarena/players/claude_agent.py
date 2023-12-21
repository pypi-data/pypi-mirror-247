from typing import Any

import anthropic

from .agent import Agent

class ClaudeAgent(Agent):
    model: str
    history: list
    cli: object
    def __init__(self, api_key: str, model: str = "claude-2.1", **kwargs) -> None:
        super().__init__()
        self.api_key = api_key
        self.model = model
        self.cli = anthropic.Anthropic(api_key=api_key)
        self.history = []

    def receive_prompt(self, prompt: str) -> Any:
        self.history.append({"role": "user", "content": prompt})

    def _postprocess(self, response) -> str:
        message = response.content[0].text
        self.history.append({"role": "assistant", "content": message})
        return message.strip()

    def generate_reply(self) -> Any:
        response = self.cli.beta.messages.create(
            model=self.model,
            messages=self.history,
            max_tokens=4096
        )
        return self._postprocess(response)