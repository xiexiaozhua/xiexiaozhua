import asyncio
import json
from aiohttp import web, web_request
from khl import Bot, Message, PrivateMessage
from khl.card import Card, CardMessage, Module

# 读取配置
with open('./config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

bot = Bot(token=config['token'])

# 初始化卡片消息
cm = CardMessage()
cm.append(Card(
    Module.Section("指令界面"),
    Module.Section("`/help` | 获取帮助"),
    Module.Section("`/activate 激活码`  | 激活"),
    Module.Section("`/hwid your hwid` | 绑定hwid,一定要在!hwid后面空一格"),
))

# 定义一个异步函数来处理私信消息
@bot.on_private_message()
async def handle_private_message(msg: PrivateMessage):
    # 假设我们只对文本为"help"的消息作出回应
    if msg.content == "help":
        print("114514")
        await msg.reply(cm, use_quote=False)

# 定义一个简单的HTTP处理器作为示例
@web.get('/')
async def hello_world(request: web_request.Request):
    return web.Response(text="hello")

# 创建并运行web应用
app = web.Application()
app.add_routes([web.get('/', hello_world)])

# 运行bot
bot.run()
