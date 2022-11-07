from nonebot.adapters.cqhttp import MessageEvent, Message, MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from src.arcaea.matcher import arc
from src.arcaea.message.text_message import TextMessage
from src.arcaea.api.request import API


async def random_handler(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    args = {i: v for i, v in enumerate(args)}
    if args.get(0, None) == "random":
        # get args
        start = args.get(1, "0")
        end = args.get(2, "20")
        resp = await API.get_song_random(start=start, end=end)
        if error_message := resp.message:
            await arc.finish(MessageSegment.reply(event.message_id) + error_message)
        await arc.finish(
            MessageSegment.reply(event.message_id) + TextMessage.song_info_detail(resp)
        )
