from src.arcaea.api import API
from src.arcaea.database import UserInfo, ArcInfo
from src.arcaea.matcher import arc
from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.adapters.cqhttp import MessageEvent
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot


async def bind_handler(bot: Bot, event: Event, state: T_State):
    if args[0] == "bind":
        if len(args) == 1:
            await arc.finish(MessageSegment.reply(event.message_id) + "缺少参数 arcaea_id！")

        arc_id = args[1]

        arc_info: ArcInfo = ArcInfo.get_or_none(
            (ArcInfo.arcaea_name == arc_id) | (ArcInfo.arcaea_id == arc_id)
        )
        if arc_info:
            arc_id = arc_info.arcaea_id
            arc_name = arc_info.arcaea_name

        resp = await API.get_user_info(arcaea_id=arc_id)
        if error_message := resp.message:
            await arc.finish(MessageSegment.reply(event.user_id) + error_message)
        arc_id = resp.content.account_info.code
        arc_name = resp.content.account_info.name
        ArcInfo.replace(
            arcaea_id=arc_id,
            arcaea_name=arc_name,
            ptt=resp.content.account_info.rating,
        ).execute()
        UserInfo.delete().where(UserInfo.user_qq == event.user_id).execute()
        UserInfo.replace(user_qq=event.user_id, arcaea_id=arc_id).execute()
        await arc.finish(
            MessageSegment.reply(event.message_id)
            + f"绑定成功, 用户名: {arc_name}, id: {arc_id}"
        )
