# Economic Arena for Large Language Models

## Current Version
0.0.4

## Integrated LLM agent
| Series          | Models                 |
|-----------------|------------------------|
| OpenAI          | gpt-3.5, gpt-4         |
| Google DeepMind | PaLM2, Gemini-Pro      |
| Anthropic       | Claude, Claude-instant |
| Baichuan AI     | Baichuan2              |

## To use this package

Python requires **>= 3.9**

### 1. Install the package
```
pip install econarena
```

### 2. Write your script
In `example.py` you can write your script and run it.

To successfully run a script, you have to complete 3 steps in the script:

1. initial a `Host` instance
2. set api configurations
3. run the game and fetch the result

After that, just call `python example.py` and start your game with LLMs!