#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : smooth
# @Time         : 2023/12/21 09:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 加广告 去广告 平滑

from meutils.pipe import *
from meutils.queues.uniform_queue import UniformQueue

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk


class Completions(object):

    def __init__(self, **client_params):
        api_key = client_params.get('api_key')
        base_url = client_params.get('base_url')
        self.completions = OpenAI(api_key=api_key, base_url=base_url).chat.completions
        self.interval = client_params.get('interval', 0.015)

        self.slogan = client_params.get('slogan', '')  # 加广告
        self.sub_pattern = client_params.get('sub_pattern')  # 去广告

    def create(self, **data):
        data.pop("additional_kwargs", None)
        response = self.completions.create(**data)
        if data.get('stream'):
            def generator():
                for chunk in response:
                    raw_content = chunk.choices[0].delta.content

                    if self.sub_pattern:
                        raw_content = re.sub(self.sub_pattern, "", raw_content)

                    for content in raw_content:
                        _chunk = chunk.model_copy(deep=True)
                        _chunk.choices[0].delta.content = content
                        yield _chunk

                yield self.chat_completion_chunk_slogan

            return UniformQueue(generator()).consumer(interval=self.interval, break_fn=self.break_fn)

        else:
            response.choices[0].message.content = response.choices[0].message.content + self.slogan
            return response

    def create_sse(self, **data):
        response = self.create(**data)
        if data.get('stream'):
            from sse_starlette import EventSourceResponse
            generator = (chunk.model_dump_json() for chunk in response)
            return EventSourceResponse(generator, ping=10000)
        return response

    @staticmethod
    def break_fn(line: ChatCompletionChunk):
        return line.choices[0].finish_reason

    # @property
    # def chat_completion_slogan(self):
    #     from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk
    #
    #     chat_completion = chat_completion.model_copy(deep=True)
    #     chat_completion.choices[0].message.content = self.slogan
    #     return chat_completion

    @cached_property
    def chat_completion_chunk_slogan(self):
        from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk
        chat_completion_chunk = chat_completion_chunk.model_copy(deep=True)
        chat_completion_chunk.choices[0].delta.content = self.slogan
        return chat_completion_chunk


if __name__ == '__main__':

    data = {'model': 'gemini-pro', 'messages': [{'role': 'user', 'content': '你是谁'}], 'stream': True}

    completions = Completions(
        api_key='sk-wewfUjhh5aMmLcGJE5653430C9Fb42F7A3885f166568Ed0f',
        base_url='http://150.109.20.187:39000/v1',
        slogan='\n\n[永远相信美好的事情即将发生](https://api.chatllm.vip/)',
    )
    print(completions.create(**data))
    for i in completions.create(**data):
        print(i.choices[0].delta.content, end='')
