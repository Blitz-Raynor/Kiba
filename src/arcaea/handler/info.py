from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.adapters.cqhttp import MessageEvent
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from src.arcaea.database import UserInfo, ArcInfo
from src.arcaea.matcher import arc


async def info_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    if args[0] == "info":
        user_info: UserInfo = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        # Exception
        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")

        arc_info: ArcInfo = ArcInfo.get_or_none(
            ArcInfo.arcaea_id == user_info.arcaea_id
        )

        await arc.finish(
            MessageSegment.reply(event.message_id)
            + f"id: {user_info.arcaea_id}, 用户名: {arc_info.arcaea_name}。"
        )
