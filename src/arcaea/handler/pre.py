from src.arcaea.matcher import arc
from src.arcaea.config import config
from src.arcaea.message import TextMessage
from nonebot.log import logger
from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.adapters.cqhttp import MessageEvent
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot

async def pre_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    if len(args) == 0:
        await arc.finish(
            MessageSegment.reply(event.message_id) + TextMessage.help_message
        )

    aua_token = config.get_config("aua_token")
    aua_url = config.get_config("aua_url")
    if aua_token == "SECRET" or aua_url == "URL":
        logger.error("ArcaeaUnlimitedApi is not configured!")
        await arc.finish("ArcaeaUnlimitedApi is not configured!")
