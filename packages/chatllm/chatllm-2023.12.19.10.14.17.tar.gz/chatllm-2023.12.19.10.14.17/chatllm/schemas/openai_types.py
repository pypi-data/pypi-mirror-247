#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_types
# @Time         : 2023/12/19 09:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from openai.types.chat.completion_create_params import CompletionCreateParams


class ChatCompletionRequest(BaseModel):
    request: CompletionCreateParams


if __name__ == '__main__':
    request = {"request": {"stream": True, "model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "你好"}]}}

    print(ChatCompletionRequest.model_validate(request))
