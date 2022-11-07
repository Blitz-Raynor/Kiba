from nonebot.adapters.cqhttp import MessageEvent, MessageSegment
from src.arcaea.matcher import arc
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot

async def default_handler(bot: Bot, event: Event, state: T_State):
    await arc.finish(MessageSegment.reply(event.message_id) + "这是当前 Arcaea 模块中不支持的命令参数.....还是您要看看其他模块呢？")
