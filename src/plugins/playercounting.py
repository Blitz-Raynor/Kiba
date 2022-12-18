from collections import defaultdict
from msilib.schema import AdvtExecuteSequence
from tkinter import Image
from types import MethodType

from nonebot import on_command, get_driver, on_regex
from nonebot.typing import T_State
from nonebot.adapters import Event, Bot
from src.libraries.image import image_to_base64, path, draw_text, get_jlpx, text_to_image
import re
import datetime
from io import BytesIO
from nonebot.rule import to_me
from src.libraries.config import Config
from nonebot.adapters.cqhttp import Message

help_count = on_command('count.help')

@help_count.handle()
async def _(bot: Bot, event: Event, state: T_State):
    help_str = '''▼ 出勤人数统计模块可用命令 | Commands For Player Counting
------------------------------------------------------------------------------------------------------------------------------
/count <出勤店铺><人数/几>人                                             设置或者显示当前店铺的出勤人数
/count <出勤店铺>位置                                                           显示店铺的位置

▼ 管理员设置 | Administrative                                             
------------------------------------------------------------------------------------------------------------------------------
/count set <店铺名> <店铺位置（可选）>   -- 此命令可以添加店铺。
------------------------------------------------------------------------------------------------------------------------------'''
    await help_count.send(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(text_to_image(help_str)), encoding='utf-8')}"
        }
    }]))

waiting_set = on_command("/count set")

@waiting_set.handle()
async def _(bot: Bot, event: Event, state: T_State):
    argv = str(event.get_message()).strip().split(" ")
    db = get_driver().config.db
    now = datetime.datetime.now()
    c = await db.cursor()
    if event.message_type != "group":
        await waiting_set.finish("▿ 游玩人数统计 - 设置\n抱歉，请在群内再发送一次来验证您的身份。")
        return
    group_members = await bot.get_group_member_list(group_id=event.group_id)
    for m in group_members:
        if m['user_id'] == event.user_id:
            break
    if m['role'] != 'owner' and m['role'] != 'admin' and str(m['user_id']) not in Config.superuser:
        await waiting_set.finish("▿ 游玩人数统计 - 设置\n抱歉，只有群管理员 / KibaBot 管理者才有权调整店铺设置。")
        return
    if len(argv) > 2 or argv[0] == "帮助":
        await waiting_set.finish("▾ 游玩人数统计 - 帮助\n命令格式是:\n设置店铺 [店铺名] [店铺位置]\n注意只有管理员才可以有权设置店铺信息哦。")
        return
    time = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.strftime('%M')}:{now.strftime('%S')}"
    await c.execute(f'select * from waiting_table where shop="{argv[0]}"')
    data = await c.fetchone()
    if data is None:
        if len(argv) == 2:
            await c.execute(f'insert into waiting_table values ("{argv[0]}","{argv[1]}",0,"{time}")')
            await db.commit()
        elif len(argv) == 1:
            await c.execute(f'insert into waiting_table values ("{argv[0]}","待设置",0,"{time}")')
            await db.commit()
        await waiting_set.finish(f"▾ 游玩人数统计\n已成功设置店铺。\n店铺名: {argv[0]}\n出勤人数: 0\n修改时间: {time}")
    else:
        if len(argv) == 1:
            await waiting_set.finish("▿ 游玩人数统计 - 设置\n已存在此店铺，您可以选择修改店铺位置信息。")
            return
        elif len(argv) == 2:
            await c.execute(f'update waiting_table set location={argv[1]} where shop={argv[0]}')
            await waiting_set.finish(f"▾ 游玩人数统计\n已成功设置店铺。\n店铺名: {argv[0]}\n出勤人数: 0\n修改时间: {time}")
            await db.commit()

waiting = on_regex(r'/count (.+) ([0-9]?几?\+?\-?1?)人?', priority=15)
@waiting.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "(.+) ([0-9]?几?\+?\-?1?)人?"
    res = re.match(regex, str(event.get_message()).lower())
    db = get_driver().config.db
    now = datetime.datetime.now()
    c = await db.cursor()
    time = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.strftime('%M')}:{now.strftime('%S')}"
    shop = res.groups()[0].split(" ")[1]
    if res.groups()[1] == "几":
        await c.execute(f'select * from waiting_table where shop="{shop}"')
        data = await c.fetchone()
        if data is None:
            await waiting.finish(f"▿ 游玩人数统计\n此店铺\"{shop}\"不存在，请联系管理员添加此店铺。")
            return
        else:
            await waiting.finish(f"▾ 游玩人数统计\n{data[0]}有{data[2]}人出勤。\n最后更新时间:{data[3]}")
            return
    elif res.groups()[1] == "+1":
        await c.execute(f'select * from waiting_table where shop="{shop}"')
        data = await c.fetchone()
        if data is None:
            await waiting.finish(f"▿ 游玩人数统计\n此店铺\"{shop}\"不存在，请联系管理员添加此店铺。")
            return
        else:
            await c.execute(f'update waiting_table set wait={data[2] + 1}, updated="{time}" where shop="{res.groups()[0]}"')
            await db.commit()
            await waiting.finish(f"▾ 游玩人数统计\n更新完成！\n{data[0]}有{data[2] + 1}人出勤。\n最后更新时间:{time}")
            return
    elif res.groups()[1] == "-1":
        await c.execute(f'select * from waiting_table where shop="{shop}"')
        data = await c.fetchone()
        if data is None:
            await waiting.finish(f"▿ 游玩人数统计\n此店铺\"{shop}\"不存在，请联系管理员添加此店铺。")
            return
        else:
            if data[2] - 1 < 0:
                await waiting.finish("▿ 游玩人数统计\n不能再减了，再减就变成灵异事件了！")
                return
            await c.execute(f'update waiting_table set wait={data[2] - 1}, updated="{time}" where shop="{res.groups()[0]}"')
            await db.commit()
            await waiting.finish(f"▾ 游玩人数统计\n更新完成！\n{data[0]}有{data[2] - 1}人出勤。\n最后更新时间:{time}")
            return
    else:
        await c.execute(f'select * from waiting_table where shop="{shop}"')
        data = await c.fetchone()
        if data is None:
            await waiting.finish(f"▿ 游玩人数统计\n此店铺\"{shop}\"不存在，请联系管理员添加此店铺。")
            return
        else:
            await c.execute(f'update waiting_table set wait={res.groups()[1]}, updated="{time}" where shop="{shop}"')
            await db.commit()
            await waiting.finish(f"▾ 游玩人数统计\n更新完成！\n{shop}有{res.groups()[1]}人出勤。\n最后更新时间:{time}")
            return

location = on_regex(r'/count (.+)位置')
@location.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "/count (.+)位置"
    name = re.match(regex, str(event.get_message())).groups()[0].strip().lower()
    db = get_driver().config.db
    c = await db.cursor()
    await c.execute(f'select * from waiting_table where shop="{name}"')
    data = await c.fetchone()
    if data is None:
        await waiting.finish("▿ 游玩人数统计\n此店铺不存在，请联系管理员添加此店铺。")
        return
    else:
        await waiting.finish(f"▾ 游玩人数统计 - 位置\n{data[0]}: {data[1]}")
        return


