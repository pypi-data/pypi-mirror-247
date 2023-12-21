# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2023/12/21 17:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from urllib.parse import quote


_ = quote("http://150.109.20.187:39000/v1|sk-wewfUjhh5aMmLcGJE5653430C9Fb42F7A3885f166568Ed0f|x|\n\n[永远相信美好的事情即将发生](https://api.chatllm.vip/)")

print(_)
