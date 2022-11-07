from nonebot.adapters.cqhttp import MessageEvent, Message, MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from src.arcaea.matcher import arc
from src.arcaea.message.text_message import TextMessage
from src.arcaea.api.request import API
from src.arcaea.schema import diffstr2num


async def song_handler(bot: Bot, event: Event, state: T_State):
    """
    /arc song Fracture Ray ftr
    """
    args = str(event.get_message()).split()
    if len(args) >= 2 and args[0] == "song":
        # get args
        difficulty = diffstr2num(args[-1].upper())
        if difficulty is not None:
            songname = " ".join(args[1:-1])
        else:
            difficulty = -1
            songname = " ".join(args[1:])
        # query
        resp = await API.get_song_info(songname=songname)
        if error_message := resp.message:
            await arc.finish(MessageSegment.reply(event.message_id) + error_message)
        await arc.finish(
            MessageSegment.reply(event.message_id)
            + TextMessage.song_info(data=resp, difficulty=difficulty)
        )
