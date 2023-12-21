from dataclasses import dataclass, field
from typing import List


@dataclass
class OpenAIConfig:
    # openai
    api_key: str = "sk-5RWLAZmivydLKUA80483CaAcDe1f4c7aB56cD7395a80DcAb"
    base_endpoint: str = "https://chatapi.omycloud.site"
    completion_endpoint: str = "https://chatapi.omycloud.site/v1/chat/completions"

    models: List[str] = field(default_factory=lambda: ["gpt-3.5-turbo-0613", "gpt-4-0613"])
    chat_model: str = "gpt-3.5-turbo-0613"
    whisper_model: str = "whisper-1"


@dataclass
class AzureOpenAI(OpenAIConfig):
    api_key = "1700006389466390612"
    base_endpoint = "https://aigc.sankuai.com/v1/openai/native"

