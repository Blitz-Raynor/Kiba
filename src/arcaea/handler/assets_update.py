from src.arcaea.matcher import arc
from src.arcaea.assets_updater import AssetsUpdater, ApkUpdater
from src.arcaea.resource_manager import db_root as ROOT
from nonebot.adapters.cqhttp import MessageEvent
from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from os import path
from shutil import rmtree
from typing import List


async def assets_update_handler(bot: Bot, event: Event, state: T_State):
    args: List = str(event.get_message()).split()
    if args[0] == "assets_update":
        if len(args) == 2:
            if args[1] == "--purge":
                rmtree(ROOT / "assets", ignore_errors=True)
            if args[1] == "--standalone":
                await arc.send(MessageSegment.reply(event.message_id) + "正在更新……")
                await ApkUpdater.update()
                await arc.finish(MessageSegment.reply(event.message_id) + "更新完成")
        await arc.send("正在更新，请关注控制台更新进度…")

        result_song = await AssetsUpdater.check_song_update()
        result_char = await AssetsUpdater.check_char_update()

        await arc.finish(
            MessageSegment.reply(event.message_id)
            + "\n".join(
                [
                    f"成功更新 {len(result_song)} 张曲绘, ",
                    f"成功更新 {len(result_char)} 张立绘",
                ]
            )
        )
