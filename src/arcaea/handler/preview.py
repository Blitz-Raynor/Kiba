from nonebot.adapters.cqhttp import MessageEvent, Message, MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from src.arcaea.matcher import arc
from src.arcaea.api.request import API
from src.arcaea.schema import diffstr2num


async def preview_handler(bot: Bot, event: Event, state: T_State):
    """
    /arc preview Fracture Ray ftr
    """
    args = str(event.get_message()).split()
    if len(args) >= 2 and args[0] == "preview":
        # get args
        difficulty = diffstr2num(args[-1].upper())
        if difficulty is not None:
            songname = " ".join(args[1:-1])
        else:
            difficulty = 2
            songname = " ".join(args[1:])
        # query
        resp = await API.get_song_preview(songname=songname, difficulty=difficulty)
        await arc.finish(
            MessageSegment.reply(event.message_id) + MessageSegment.image(resp)
        )
