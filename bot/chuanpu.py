import asyncio
import json
from aiohttp import web, web_request
from khl.card import  CardMessage, Card, Module
from khl import Bot, Message

bot = Bot(token="1/Mjg1MDg=/OGRPSYmwgWiyFk8ZKO0i+g==")
@bot.command(name='兄弟我爱你')
async def help_command(msg: Message):
    await help_handler(msg)
async def help_handler(msg: Message):
    await msg.reply("兄弟我爱你", use_quote=False)
bot.run()