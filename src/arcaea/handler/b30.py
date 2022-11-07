from src.arcaea.matcher import arc
from src.arcaea.database import UserInfo
from src.arcaea.message.image_message import UserArcaeaInfo
from nonebot.adapters.cqhttp import MessageEvent
from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot


async def b30_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    if args[0] == "b30" or args[0] == "b40":
        user_info: UserInfo = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "嘿，你还没绑定呢！")
        if UserArcaeaInfo.is_querying(user_info.arcaea_id):
            await arc.finish(
                MessageSegment.reply(event.message_id) + "您已在查询队列啦, 请耐心等候一下 Kiba~"
            )
        result = await UserArcaeaInfo.draw_user_b30(user_info.arcaea_id)
        await arc.finish(MessageSegment.reply(event.message_id) + result)
