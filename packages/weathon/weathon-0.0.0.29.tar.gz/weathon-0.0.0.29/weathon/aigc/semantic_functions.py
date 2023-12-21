import os
import pathlib
from typing import Dict
import semantic_kernel as sk
from semantic_kernel import SKContext, SKFunctionBase,ContextVariables
from semantic_kernel.connectors.ai import  CompleteRequestSettings
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import \
    OpenAIChatCompletion as ChatCompletion
from weathon.aigc.services.qwen_chat_completion import QwenChatCompletion as ChatCompletion

from semantic_kernel.connectors.memory.milvus.milvus_memory_store import MilvusMemoryStore


class SemanticFunctions:

    def __init__(self,model_id='qwen-14b-chat', api_key="sk-27cc994e5db0436eb9f717c8624709fe", endpoint = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"):
        self.kernel = sk.Kernel()
        self.kernel.add_chat_service("chat_model",
                                     service=ChatCompletion(model_id=model_id, api_key=api_key, endpoint=endpoint))

        skills_directory: str = os.path.join(__file__, "../plugins")
        self.test_plugins: Dict[str, SKFunctionBase] = self.kernel.import_semantic_skill_from_directory(skills_directory, "test")
        self.poem_plugins: Dict[str, SKFunctionBase] = self.kernel.import_semantic_skill_from_directory(skills_directory, "poem")

    def run_prompt(self, prompt, temperature=0.7, number_of_responses=3) -> str:
        """
            测试 helloworld
        """
        variables = ContextVariables()
        variables['prompt'] = prompt
        settings = CompleteRequestSettings(temperature=temperature, number_of_responses=number_of_responses)
        result:SKContext = self.test_plugins["prompt"].invoke(variables=variables, settings=settings)

        return result['input']

    def poem_interpretation(self, title: str, poet: str, dynasty: str, poem: str, sentence_idx:int, sentence: str,
                            temperature: float = 0.7, number_of_responses: int = 1) -> str:
        variables = ContextVariables()
        variables["title"] = title
        variables["poet"] = poet
        variables["dynasty"] = dynasty
        variables["poem"] = poem
        variables["sentence"] = sentence
        settings = CompleteRequestSettings(temperature=temperature, number_of_responses=number_of_responses)
        result:SKContext = self.poem_plugins["poem_interpretation"].invoke(variables=variables, settings=settings)
        return result["input"]


if __name__ == '__main__':
    sf = SemanticFunctions()
    result: str = sf.run_prompt("""
    """)
    print(result)