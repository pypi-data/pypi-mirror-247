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
from urllib.parse import quote, unquote


_ = quote("http://0.0.0.0:39000/v1|sk-wewfUjhh5aMmLcGJE5653430C9Fb42F7A3885f166568Ed0f||")

print(_)


print(unquote(_))
