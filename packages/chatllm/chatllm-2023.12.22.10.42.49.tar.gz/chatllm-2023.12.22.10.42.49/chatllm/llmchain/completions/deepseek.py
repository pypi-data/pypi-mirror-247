#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deepseek
# @Time         : 2023/12/11 14:27
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.uniform_queue import UniformQueue
from meutils.notice.feishu import send_message

from chatllm.llmchain.utils import tiktoken_encoder
from chatllm.llmchain.completions import github_copilot

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat import chat_completion_chunk, chat_completion
from chatllm.schemas.openai_types import chat_completion_error, chat_completion_chunk_error

requests.post = retrying(requests.post)


# DeepSeek-LLM-67B-chat
class Completions(github_copilot.Completions):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')
        self.access_token = self.get_access_token(self.api_key)

    def create(self, messages: Union[str, List[Dict[str, Any]]], **kwargs):
        """
            {message: "讲个故事", stream: true, model_preference: null, model_class: "deepseek_chat", temperature: 0}
        """

        data = {
            "model": 'gpt-4',
            "messages": messages,

            "message": messages[-1].get('content'),
            "model_preference": None,
            "model_class": "deepseek_chat",  # deepseek_code

            **kwargs
        }

        data['model_class'] = data['model'] if data['model'] in {"deepseek_chat", "deepseek_code"} else "deepseek_chat"

        if data.get('stream'):
            return self.smooth_stream(interval=0.01, **data)
        else:
            return self._create(**data)

    def _create(self, **data):
        data['stream'] = True  # 这个参数必须为True

        content = ''
        chunk_id = created = None
        model = data.get('model', 'kimi')
        for chunk in self._stream_create(**data):
            chunk_id = chunk.id
            created = chunk.created
            content += chunk.choices[0].delta.content

        message = chat_completion.ChatCompletionMessage(role='assistant', content=content)

        choice = chat_completion.Choice(
            index=0,
            message=message,
            finish_reason='stop'
        )

        prompt_tokens, completion_tokens = map(len, tiktoken_encoder.encode_batch([str(data.get('messages')), content]))
        total_tokens = prompt_tokens + completion_tokens

        usage = chat_completion.CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens
        )

        completion = chat_completion.ChatCompletion(
            id=chunk_id,
            choices=[choice],
            created=created,
            model=model,
            object="chat.completion",
            usage=usage

        )

        return completion

    def _stream_create(self, **data):
        response = self._post(**data)
        if response.status_code != 200:
            chat_completion_chunk_error.choices[0].delta.content = response.text
            yield chat_completion_chunk_error
            return

        for chunk in response.iter_lines(chunk_size=1024):
            # logger.debug(chunk)
            if chunk.strip() and b'created' in chunk:

                chunk = chunk.strip(b"data: ")
                # chunk = json.loads(chunk)
                # chunk = ChatCompletionChunk.model_validate(chunk)
                chunk = ChatCompletionChunk.model_validate_json(chunk)

                chunk.choices[0].delta.role = 'assistant'
                content = chunk.choices[0].delta.content or ''
                chunk.choices[0].delta.content = content

                if content or chunk.choices[0].finish_reason:
                    yield chunk

    def _post(self, **data):
        headers = {
            'Authorization': f"Bearer {self.access_token}",  # access_token
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/119.0.0.0 Safari/537.36'
        }

        url = "https://chat.deepseek.com/api/v0/chat/completions"
        response = requests.post(
            url,
            json=data,
            headers=headers,
            stream=data.get('stream')
        )
        if response.status_code != 200:
            send_message(title=self.__class__.__name__, content=f"{response.text}\n\n{self.api_key}")

        return response

    def get_access_token(self, api_key: Optional[str] = None):
        api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZDQ0NDc4MmMtZWMyOC00Y2MzLWIwNWMtOWEwZDFjMGNhZmQ2IiwiZW1haWwiOiIzMTMzMDMzMDNAcXEuY29tIiwibW9iaWxlX251bWJlciI6IjE4NTUwMjg4MjMzIiwiYXJlYV9jb2RlIjoiKzg2IiwibW9iaWxlIjoiMTg1NTAyODgyMzMiLCJleHAiOjE3MDM2NzA5MjIsImF1ZCI6IjY1MjhhZDM5NmZhYTEzNjdmZWU2ZDE2YyJ9.KQO5dTWy8WgzscD2PoCWhmeiTE9A2AIhBJHBDmZy2oI"
        return api_key


if __name__ == '__main__':
    # data = {'model': 'gpt-114111', 'messages': [{'role': 'user', 'content': '你是谁'}], 'stream': False}
    data = {'model': 'deepseek', 'messages': [{'role': 'user', 'content': '错了'}], 'stream': True}

    Completions.chat(data)

    # with timer('异步'):
    #     print([Completions().acreate(**data) for _ in range(10)] | xAsyncio)

    #
    # data = {'model': 'gpt-4', 'messages': [{'role': 'user', 'content': '你是谁'}], 'stream': False}
    # _ = Completions().create(**data, smooth=0)
    # # _ = Completions()._stream_create(**data)
    #
    # # 我是DeepSeek Chat，一个由深度求索公司开发的智能助手，旨在通过自然语言处理和机器学习技术来提供信息查询、对话交流和解答问题等服务。
    #
    # if isinstance(_, Generator):
    #     for i in tqdm(_):
    #         content = i.choices[0].delta.content
    #         print(content, end='')
    # else:
    #     print(_)
