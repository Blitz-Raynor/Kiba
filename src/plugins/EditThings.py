from ast import ExceptHandler
import random
import re
from unittest.util import sorted_list_difference

from PIL import Image
from nonebot import on_command, on_message, on_notice, require, get_driver, on_regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot
from src.libraries.image import *
from random import randint
import asyncio
from nonebot.adapters.cqhttp import Message, MessageSegment, GroupMessageEvent, PrivateMessageEvent
from src.plugins.guild import GuildMessageEvent

from nonebot.rule import to_me
from src.libraries.image import image_to_base64, path, draw_text, get_jlpx, text_to_image
from src.libraries.tool import hash

import os
import time
import datetime
from collections import defaultdict
from src.libraries.config import Config



pz = on_command("/cds 排长语录")

@pz.handle()
async def _(bot: Bot, event: Event, state: T_State):
    pzyl = ["排长，再带兄弟们冲一次吧！！", "憋扒拉我", "不想玩啦——", "布响丸辣——", "海底谭你学不会。", "这不带你开点好玩的，比如Garden Of The Dragon?"]
    await pz.send(pzyl[random.randint(0,5)])

sld = on_command("/lz 乌蒙大神",aliases={"/lz 舞萌大神", "/lz 杀戮多", "/lz 纱露朵"})
@sld.handle()
async def _(bot: Bot, event: Event, state: T_State):
    s = "敬爱的舞萌大神，纱露朵：\n你好，我是犽。\n\n恭喜你!!!!!!!\n获得了"
    score = ["爽将与煌将！！", "堇将！！", "舞萌DX 10000分成就！！"]
    s += score[random.randint(0,2)]
    s += "\n......剩下的👴忘了。"
    await sld.send(s)