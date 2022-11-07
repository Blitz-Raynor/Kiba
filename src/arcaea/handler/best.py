from nonebot.adapters.cqhttp import MessageEvent
from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from src.arcaea.database import UserInfo
from src.arcaea.message.image_message import UserArcaeaInfo
from src.arcaea.matcher import arc
from ..schema import diffstr2num


async def best_handler(bot: Bot, event: Event, state: T_State):
    """
    /arc best Fracture Ray ftr
    """
    args = str(event.get_message()).split()
    if len(args) >= 2 and args[0] == "best":
        user_info: UserInfo = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        # get args
        difficulty = diffstr2num(args[-1].upper())
        if difficulty is not None:
            songname = " ".join(args[1:-1])
        else:
            difficulty = 2
            songname = " ".join(args[1:])
        # Exception
        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "嘿，你还没绑定呢！")

        if UserArcaeaInfo.is_querying(user_info.arcaea_id):
            await arc.finish(
                MessageSegment.reply(event.message_id) + "您已在查询队列啦, 请耐心等候一下 Kiba~"
            )
        # Query
        result = await UserArcaeaInfo.draw_user_best(
            arcaea_id=user_info.arcaea_id, songname=songname, difficulty=difficulty
        )
        await arc.finish(MessageSegment.reply(event.message_id) + result)
