from http import HTTPStatus
from logging import Logger
from typing import Any, List, Optional, Tuple, Union

# import openai
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Message
from semantic_kernel.connectors.ai.ai_exception import AIException
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.chat_request_settings import ChatRequestSettings
from semantic_kernel.connectors.ai.complete_request_settings import CompleteRequestSettings
from semantic_kernel.connectors.ai.text_completion_client_base import TextCompletionClientBase
from semantic_kernel.utils.null_logger import NullLogger


class QwenChatCompletion(ChatCompletionClientBase, TextCompletionClientBase):
    _model_id: str
    _api_key: str
    _org_id: Optional[str] = None
    _api_type: Optional[str] = None
    _api_version: Optional[str] = None
    _endpoint: Optional[str] = None
    _log: Logger

    def __init__(self, model_id: str,
                 api_key: str,
                 org_id: Optional[str] = None,
                 api_type: Optional[str] = None,
                 api_version: Optional[str] = None,
                 endpoint: Optional[str] = None,
                 log: Optional[Logger] = None, ):

        self._model_id = model_id
        self._api_key = api_key
        self._org_id = org_id
        self._api_type = api_type
        self._api_version = api_version
        self._endpoint = endpoint
        self._log = log if log is not None else NullLogger()
        self._messages = []
        self.gen = Generation()

    async def complete_chat_async(self, messages: List[Tuple[str, str]], request_settings: ChatRequestSettings,
                                  logger: Optional[Logger] = None) -> Union[str, List[str]]:

        response = await self._send_chat_request(messages, request_settings, False)
        response = response.output

        if len(response.choices) == 1:
            return response.choices[0].message.content
        else:
            return [choice.message.content for choice in response.choices]

    async def complete_chat_stream_async(self, messages: List[Tuple[str, str]], request_settings: ChatRequestSettings,
                                         logger: Optional[Logger] = None):
        response = await self._send_chat_request(messages, request_settings, True)
        # parse the completion text(s) and yield them
        for chunk in response:
            text = _parse_choices(chunk.output)
            yield text

    async def complete_async(self, prompt: str, request_settings: CompleteRequestSettings, logger: Optional[Logger] = None) -> \
    Union[str, List[str]]:
        prompt_to_message = [("user", prompt)]
        chat_settings = ChatRequestSettings.from_completion_config(request_settings)

        response = await self._send_chat_request(prompt_to_message, chat_settings, False)
        response = response.output

        if len(response.choices) == 1:
            return response.choices[0].message.content
        else:
            return [choice.message.content for choice in response.choices]

    async def complete_stream_async(self, prompt: str, request_settings: "CompleteRequestSettings",
                                    logger: Optional[Logger] = None):
        prompt_to_message = [("user", prompt)]
        response = await self._send_chat_request(prompt_to_message, request_settings, True)
        # parse the completion text(s) and yield them
        for chunk in response:
            text = _parse_choices(chunk.output)
            yield text


    async def _send_chat_request(
        self,
        messages: List[Tuple[str, str]],
        request_settings: ChatRequestSettings,
        stream: bool,
    ):
        """
        Completes the given user message with an asynchronous stream.

        Arguments:
            user_message {str} -- The message (from a user) to respond to.
            request_settings {ChatRequestSettings} -- The request settings.

        Returns:
            str -- The completed text.
        """
        if request_settings is None:
            raise ValueError("The request settings cannot be `None`")

        if request_settings.max_tokens < 1:
            raise AIException(
                AIException.ErrorCodes.InvalidRequest,
                "The max tokens must be greater than 0, "
                f"but was {request_settings.max_tokens}",
            )

        if len(messages) <= 0:
            raise AIException(
                AIException.ErrorCodes.InvalidRequest,
                "To complete a chat you need at least one message",
            )

        if messages[-1][0] != "user":
            raise AIException(
                AIException.ErrorCodes.InvalidRequest,
                "The last message must be from the user",
            )

        formatted_messages = [
            Message(role=role,content=message) for role, message in messages
        ]

        try:
            response = self.gen.call(
                model=self._model_id,
                api_key=self._api_key,
                messages=formatted_messages,
                result_format='message',
                stream=stream,
                output_in_full=True
                )
            if not response.status_code == HTTPStatus.OK:
                raise AIException(AIException.ErrorCodes.ServiceError,
                                  f"Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}",)

        except Exception as ex:
            raise AIException(
                AIException.ErrorCodes.ServiceError,
                "qwen service failed to complete the chat",
                ex,
            )

        return response

def _parse_choices(chunk):
    message = ""
    if "role" in chunk.choices[0].message:
        message += chunk.choices[0].message.role + ": "
    if "content" in chunk.choices[0].message:
        message += chunk.choices[0].message.content

    return message