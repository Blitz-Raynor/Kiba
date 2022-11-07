from nonebot.adapters.cqhttp import MessageEvent, Message, MessageSegment
from nonebot.adapters import Bot
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from src.arcaea.matcher import arc
from src.arcaea.message.text_message import TextMessage


async def help_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    if args[0] == "help":
        await arc.finish(
            MessageSegment.reply(event.message_id) + TextMessage.help_message
        )
