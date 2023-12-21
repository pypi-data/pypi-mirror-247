# WebChatter

[English](README-EN.md) | [简体中文](README.md)

[![PyPI version](https://img.shields.io/pypi/v/webchatter.svg)](https://pypi.python.org/pypi/webchatter)
[![Tests](https://github.com/cubenlp/webchatter/actions/workflows/test.yml/badge.svg)](https://github.com/cubenlp/webchatter/actions/workflows/test.yml/)
[![Documentation Status](https://img.shields.io/badge/docs-github_pages-blue.svg)](https://apicall.wzhecnu.cn)
[![Coverage](https://codecov.io/gh/cubenlp/webchatter/branch/main/graph/badge.svg)](https://codecov.io/gh/cubenlp/webchatter)


## 特性

基于 AccessToken 的 Chat 封装，可用于数据标注。

## 安装

```bash
pip install webchatter --upgrade
```

设置环境变量
```bash
export OPENAI_ACCESS_TOKEN="your_access_token"
export API_REVERSE_PROXY="http://your_reverse_proxy"
export WEB_REVERSE_PROXY="http://your_reverse_proxy/backend-api"
```

其中 `OPENAI_ACCESS_TOKEN` 可在登录会话后，访问网站 [/api/auth/session](https://chat.openai.com/api/auth/session) 得到，反向代理可以参考 [ninja 项目](https://github.com/gngpp/ninja/)进行构建。

## 基本使用

数据标注示例，计算加法：
```py
from webchatter import process_messages
from random import randint

msgs = [f"find the result of {randint(3, 100)} + {randint(4, 100)}" for _ in range(4)]
# 标注一部分后被中断
process_messages(msgs[:2], "test.jsonl", time_interval=5, max_tries=3)
# 继续标注
process_messages(msgs, "test.jsonl")
```

常规使用：

```py
from webchatter import WebChat

# 创建对话
chat = WebChat()
# 输入问题 | 返回答案
chat.ask("hello world!")
# 获取对话历史
chat.print_log()
```

其他用法：

```py
from webchatter import WebChat
from pprint import pprint
chat = WebChat()

# 查看 web 对话总数
pprint(chat.num_of_chats())
# 获取近期对话
pprint(chat.chat_list(limit=3))
# 继续某个对话
chat_id = "xxx" # 从前边获取
newchat = chat.chat_by_id(chat_id)
newchat.ask("ok, let's continue")
```
