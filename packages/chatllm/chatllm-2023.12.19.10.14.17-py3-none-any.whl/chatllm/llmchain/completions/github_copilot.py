#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : copilot
# @Time         : 2023/12/6 13:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 不准白嫖 必须 star

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.uniform_queue import UniformQueue
from meutils.async_utils import sync_to_async

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

requests.post = retrying(requests.post)


class Completions(object):
    def __init__(self, **client_params):
        self.client_params = client_params
        api_key = self.client_params.get('api_key')
        self.access_token = self.get_access_token(api_key)

    def create(self, messages: Union[str, List[Dict[str, Any]]], **kwargs):  # ChatCompletionRequest: 定义请求体

        data = {
            "model": 'gpt-4',
            "messages": messages if isinstance(messages, list) else [{"role": "user", "content": messages}],
            **kwargs
        }

        # logger.debug(data)

        if data.get('stream'):
            interval = 0.05 if "gpt-4" in data['model'] else 0.01
            return self.smooth_stream(interval=interval, **data)
        else:
            return self._create(**data)

    @sync_to_async(thread_sensitive=False)
    def acreate(self, messages: Union[str, List[Dict[str, Any]]], **kwargs):
        """
            generator = (chunk.model_dump_json() for chunk in completions.acreate(messages)
        """
        return self.create(messages, **kwargs)

    def _create(self, **data):
        response = self._post(**data).json()
        response['model'] = data.get('model', 'gpt-4')
        response['object'] = 'chat.completion'

        return ChatCompletion.model_validate(response)

    def _stream_create(self, **data):
        response = self._post(**data)

        for chunk in response.iter_lines(chunk_size=1024):
            # logger.debug(chunk)
            if chunk and chunk != b'data: [DONE]':

                chunk = chunk.strip(b"data: ")
                chunk = json.loads(chunk)
                chunk['model'] = data.get('model', "gpt-4")
                chunk['object'] = "chat.completion.chunk"
                chunk['choices'][0]['finish_reason'] = chunk['choices'][0].get('finish_reason')  # 最后为 "stop"
                chunk = ChatCompletionChunk.model_validate(chunk)

                chunk.choices[0].delta.role = 'assistant'
                content = chunk.choices[0].delta.content or ''
                chunk.choices[0].delta.content = content

                # logger.debug(chunk)

                if content or chunk.choices[0].finish_reason:
                    yield chunk

    def _post(self, **data):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            # 'X-Request-Id': str(uuid.uuid4()),
            # 'Vscode-Sessionid': str(uuid.uuid4()) + str(int(datetime.datetime.utcnow().timestamp() * 1000)),
            # 'vscode-machineid': machine_id,
            'Editor-Version': 'vscode/1.84.2',
            'Editor-Plugin-Version': 'copilot-chat/0.10.2',
            'Openai-Organization': 'github-copilot',
            'Openai-Intent': 'conversation-panel',
            'Content-Type': 'application/json',
            'User-Agent': 'GitHubCopilotChat/0.10.2',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        url: str = 'https://api.githubcopilot.com/chat/completions'
        response = requests.post(
            url,
            json=data,
            headers=headers,
            stream=data.get('stream')
        )
        # logger.debug(response.text)
        return response

    @staticmethod
    @retrying
    @ttl_cache(ttl=15 * 60)  # 1500
    def get_access_token(api_key: Optional[str] = None):
        """
        {
            "annotations_enabled": true,
            "chat_enabled": true,
            "chat_jetbrains_enabled": false,
            "code_quote_enabled": false,
            "copilot_ide_agent_chat_gpt4_small_prompt": false,
            "copilotignore_enabled": false,
            "expires_at": 1702022150,
            "prompt_8k": true,
            "public_suggestions": "enabled",
            "refresh_in": 1500,
            "sku": "free_educational",
            "snippy_load_test_enabled": false,
            "telemetry": "enabled",
            "token": "tid=74069a4394491f4f41fc74888f24a0ab;exp=1702022150;sku=free_educational;st=dotcom;chat=1;sn=1;rt=1;8kp=1:b78c67b8a5d886b71b13a956f378d9b955299e5ad156a5699ab12cbeb5e7b960",
            "tracking_id": "74069a4394491f4f41fc74888f24a0ab",
            "vsc_panel_v2": false
        }
        """
        api_key = api_key or os.getenv("GITHUB_COPILOT_TOKEN")
        assert api_key

        headers = {
            'Host': 'api.github.com',
            'authorization': f'token {api_key}',
            "Editor-Version": "vscode/1.84.2",
            "Editor-Plugin-Version": "copilot/1.138.0",
            "User-Agent": "GithubCopilot/1.138.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close"
        }
        response = requests.get('https://api.github.com/copilot_internal/v2/token', headers=headers).json()
        # logger.debug(response)

        return response.get('token', response.get('error_details'))  # 监控到 token 失效，返回 error_details，半小时过期

    @staticmethod
    def break_fn(line: ChatCompletionChunk):
        return line.choices[0].finish_reason

    def smooth_stream(self, interval: Optional[float] = None, **data):
        stream = self._stream_create(**data)
        if interval:
            # logger.debug(interval)
            stream = UniformQueue(stream).consumer(interval=interval, break_fn=self.break_fn)
        return stream

    @classmethod
    def chat(cls, data: dict):  # TEST
        """
            Completions.chat(data)
        """
        with timer('聊天测试'):
            _ = cls().create(**data)

            print(f'{"-" * 88}\n')
            if isinstance(_, Generator):
                for i in _:
                    content = i.choices[0].delta.content
                    print(content, end='')
            else:
                print(_.choices[0].message.content)
            print(f'\n\n{"-" * 88}')


if __name__ == '__main__':
    data = {'model': 'gpt-3', 'messages': [{'role': 'user', 'content': '讲个故事'}], 'stream': True}

    Completions.chat(data)

    # async def main():
    #     _ = await Completions().acreate(**data)
    #
    #     content = ''
    #     for i in _:
    #         content += i.choices[0].delta.content
    #     return content
    #
    #
    # print(arun(main()))

    # with timer('异步'):
    #     print([Completions().acreate(**data) for _ in range(10)] | xAsyncio)

    # data = {
    #     'model': 'gpt-xxx',
    #     'messages': [{'role': 'user', 'content': '讲个故事。 要足够长，这对我很重要。'}],
    #     'stream': False,
    #     # 'max_tokens': 16000
    # }
    # data = {
    #     'model': 'gpt-4',
    #     'messages': '树上9只鸟，打掉1只，还剩几只',  # [{'role': 'user', 'content': '树上9只鸟，打掉1只，还剩几只'}],
    #     'stream': False,
    #     'temperature': 0,
    #     # 'max_tokens': 32000
    # }
    #
    # for i in tqdm(range(1000)):
    #     _ = Completions().create(**data)
    #     print(_.choices[0].message.content)
    #     break
