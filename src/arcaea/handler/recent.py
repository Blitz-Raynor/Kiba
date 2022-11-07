from nonebot.adapters.cqhttp import MessageEvent
from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from src.arcaea.database import UserInfo
from src.arcaea.message.image_message import UserArcaeaInfo
from src.arcaea.matcher import arc


async def recent_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    if args[0] == "recent":
        user_info: UserInfo = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)

        # Expection

        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")

        if UserArcaeaInfo.is_querying(user_info.arcaea_id):
            await arc.finish(
                MessageSegment.reply(event.message_id) + "您已在查询队列, 请勿重复发起查询。"
            )

        # Query
        result = await UserArcaeaInfo.draw_user_recent(arcaea_id=user_info.arcaea_id)
        await arc.finish(MessageSegment.reply(event.message_id) + result)
