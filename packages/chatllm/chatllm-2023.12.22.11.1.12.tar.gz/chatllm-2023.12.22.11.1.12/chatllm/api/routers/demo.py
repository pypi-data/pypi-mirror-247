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


_ = quote("sk-api-xyhelper-cn-free-token-for-everyone-xyhelper|| ")

print(_)


print(unquote(_))
