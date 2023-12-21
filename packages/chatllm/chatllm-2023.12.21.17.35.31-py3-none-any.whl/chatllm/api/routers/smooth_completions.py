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

from urllib.parse import quote, unquote
from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status

from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from chatllm.llmchain.completions import smooth
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo

router = APIRouter()

ChatCompletionResponse = Union[ChatCompletion, List[ChatCompletionChunk]]


@lru_cache
def _unquote(api_key):
    api_key = unquote(api_key)
    logger.debug(api_key)
    return api_key


@router.post("/chat/completions")
def chat_completions(
    request: ChatCompletionRequest,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)
):
    api_key = auth and auth.credentials or None
    if api_key is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")

    # 适配 oneapi
    base_url, api_key, sub_pattern, slogan = _unquote(api_key).split('|')  # base_url|api_key|sub_pattern|slogan

    data = request.model_dump()

    response: ChatCompletionResponse = (
        smooth.Completions(api_key=api_key, base_url=base_url, slogan=slogan, sub_pattern=sub_pattern)
        .create_sse(**data)
    )

    return response


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1')

    app.run()
