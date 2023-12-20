#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_types
# @Time         : 2023/12/19 09:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai.types.chat.completion_create_params import CompletionCreateParams
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion import ChatCompletion

COMPLETION_ERROR = os.getenv("COMPLETION_ERROR", "请稍后再试！！！")

chat_completion_error = {
    "id": "chatcmpl-",
    "object": "chat.completion",
    "created": 0,
    "model": "LLM",
    "choices": [{"message": {"role": "assistant", "content": COMPLETION_ERROR}, "index": 0, "finish_reason": "stop"}]
}

chat_completion_chunk_error = {
    "id": "chatcmpl-",
    "object": "chat.completion.chunk",
    "created": 0,
    "model": "LLM",
    "choices": [{"delta": {"role": "assistant", "content": COMPLETION_ERROR}, "index": 0, "finish_reason": "stop"}]
}

chat_completion_error = ChatCompletion.model_validate(chat_completion_error)
chat_completion_chunk_error = ChatCompletionChunk.model_validate(chat_completion_chunk_error)


class ChatCompletionRequest(BaseModel):
    request: CompletionCreateParams = {}
    headers: dict = {}  # HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")


if __name__ == '__main__':
    request = {"request": {"stream": True, "model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "你好"}]}}

    print(ChatCompletionRequest.model_validate(request))

    print(chat_completion_chunk_error)
