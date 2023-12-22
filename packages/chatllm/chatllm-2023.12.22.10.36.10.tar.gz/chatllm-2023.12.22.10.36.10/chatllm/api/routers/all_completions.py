#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : completions
# @Time         : 2023/12/19 16:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials

from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request

from sse_starlette import EventSourceResponse

from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from chatllm.llmchain.completions import github_copilot
from chatllm.llmchain.completions import moonshot_kimi
from chatllm.llmchain.completions import deepseek

from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo

router = APIRouter()

ChatCompletionResponse = Union[ChatCompletion, List[ChatCompletionChunk]]


@router.post("/chat/completions")
def chat_completions(
    request: ChatCompletionRequest,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)
):
    logger.debug(request)

    api_key = auth and auth.credentials or None
    logger.debug(api_key)

    model = request.model.strip().lower()
    stream = request.stream
    data = request.model_dump()

    if model.startswith(('kimi', 'moonshot')):
        if any(i in model for i in ('web', 'search', 'net')):
            data['use_search'] = True  # 联网模型
        # state_file = "/www/0_apps/cookies/kimi_cookies.json"
        # api_key = Path(state_file).exists() and state_file or None

        completions = moonshot_kimi.Completions(api_key=api_key)

    elif model.startswith(('deepseek',)):
        completions = deepseek.Completions(api_key=api_key)

    else:  # todo: 兜底
        completions = github_copilot.Completions(api_key=api_key)  # OpenAI().completions

    response: ChatCompletionResponse = completions.create(**data)
    if stream:
        # generator = map(lambda chunk: chunk.model_dump_json(), response)
        generator = (chunk.model_dump_json() for chunk in response)

        return EventSourceResponse(generator, ping=10000)  # todo: 耗时监控

    return response


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1')

    app.run()
