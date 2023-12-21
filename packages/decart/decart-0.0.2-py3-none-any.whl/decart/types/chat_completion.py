from typing import Literal, Optional, Sequence
import pydantic

from ..types.chat_completion_message import ChatCompletionMessage
from ..types.finish_reason import FinishReason
from ..types.model import Model
from ..types.completion_usage import CompletionUsage


class CreateChatCompletion(pydantic.BaseModel):
    messages: Sequence[ChatCompletionMessage]
    model: Model
    frequency_penalty: float
    presence_penalty: float
    stop: Sequence[str]
    max_tokens: Optional[int]
    stream: bool
    temperature: float
    top_p: float
    top_k: int | None


class Choice(pydantic.BaseModel):
    finish_reason: FinishReason
    index: int
    message: ChatCompletionMessage


class ChatCompletion(pydantic.BaseModel):
    id: str
    choices: Sequence[Choice]
    created: int
    model: str
    object: Literal["chat.completion"]
    system_fingerprint: Optional[str] = None
    usage: Optional[CompletionUsage] = None
