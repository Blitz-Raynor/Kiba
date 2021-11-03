import random
import re

from PIL import Image
from nonebot import on_command, on_message, on_notice, require, get_driver, on_regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot
from src.libraries.image import *
from random import randint
import asyncio

from src.libraries.image import image_to_base64, path, draw_text, get_jlpx, text_to_image
from src.libraries.tool import hash

import time
from collections import defaultdict
from src.libraries.config import Config

driver = get_driver()

scheduler = require("nonebot_plugin_apscheduler").scheduler

helper = on_command('help', aliases={'about'})

@helper.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await helper.send("※> 关于\n犽(Kiba) By BlitzR | V2.32_A\nLeangle Universe\n----------------------\n本软件为开源软件。\nGithub:\nhttps://github.com/Blitz-Raynor/Kiba\n感谢:\n@Diving-Fish\n@BlueDeer233\n----------------------\n※> 帮助\n查询舞萌模块帮助 maimai.help\n查询跑团模块帮助 coc.help\n查询其它模块帮助 others.help")
   
help_others = on_command('others.help')

@help_others.handle()
async def _(bot: Bot, event: Event, state: T_State):
    help_str = '''※> 其它模块可用命令 | Commands For Others                                              
------------------------------------------------------------------------------------------------------------------------------
戳一戳                                                                                  来戳戳我？

本群戳一戳情况                                                                    查看一下群里有几位杰出的无聊人

今日雀魂                                                                               查看今天的雀魂运势

mjxp                                                                                     看看你今天要做什么牌捏？

低情商<str1>高情商<str2>                                                 生成一张低情商高情商图片，
                                                                                              把str1/2换成自己的话。

gocho <str1> <str2>                                                         生成一张gocho图。

金龙盘旋 <str1> <str2> <str3>                                         生成一张金龙盘旋图。

投骰子<数量>                                                                       在线投骰子(?)
投百面骰子<数量>                                                             * 可以选择六面/百面

                                                                                              这个功能可以随机禁言你1-600秒，前提小犽是管理员。
烟我                                                                                    * 注意：为防止误触发，
                                                                                              这个功能你需要at一下小犽再说这个命令才能执行。

                                                                                               群里摇人。
随个[男/女]群友                                                                      你也可以不带参数直接说“随个”然后后面加啥都可以。
                                                                                               当然小犽容易骂你就是了。

帮选                                                                                      帮你选 
------------------------------------------------------------------------------------------------------------------------------'''
    await help_others.send(Message([{
        "type": "image",
        "data": {
            "file": f"base64://{str(image_to_base64(text_to_image(help_str)), encoding='utf-8')}"
        }
    }]))


async def _group_poke(bot: Bot, event: Event, state: dict) -> bool:
    value = (event.notice_type == "notify" and event.sub_type == "poke" and event.target_id == int(bot.self_id))
    return value


poke = on_notice(rule=_group_poke, priority=10, block=True)
poke_dict = defaultdict(lambda: defaultdict(int))

async def invoke_poke(group_id, user_id) -> str:
    db = get_driver().config.db
    ret = "default"
    ts = int(time.time())
    c = await db.cursor()
    await c.execute(f"select * from group_poke_table where group_id={group_id}")
    data = await c.fetchone()
    if data is None:
        await c.execute(f'insert into group_poke_table values ({group_id}, {ts}, 1, 0, "default")')
    else:
        t2 = ts
        if data[3] == 1:
            return "disabled"
        if data[4].startswith("limited"):
            duration = int(data[4][7:])
            if ts - duration < data[1]:
                ret = "limited"
                t2 = data[1]
        await c.execute(f'update group_poke_table set last_trigger_time={t2}, triggered={data[2] + 1} where group_id={group_id}')
    await c.execute(f"select * from user_poke_table where group_id={group_id} and user_id={user_id}")
    data2 = await c.fetchone()
    if data2 is None:
        await c.execute(f'insert into user_poke_table values ({user_id}, {group_id}, 1)')
    else:
        await c.execute(f'update user_poke_table set triggered={data2[2] + 1} where user_id={user_id} and group_id={group_id}')
    await db.commit()
    return ret

@poke.handle()
async def _(bot: Bot, event: Event, state: T_State):
    v = "default"
    if event.__getattribute__('group_id') is None:
        event.__delattr__('group_id')
    else:
        group_dict = poke_dict[event.__getattribute__('group_id')]
        group_dict[event.sender_id] += 1
        if v == "disabled":
            await poke.finish()
            return
    r = randint(1, 20)
    if v == "limited":
        await poke.send(Message([{
            "type": "poke",
            "data": {
                "qq": f"{event.sender_id}"
            }
        }]))
    elif r == 2:
        await poke.send(Message('戳你🐎'))
    elif r == 3:
        url = await get_jlpx('戳', '你妈', '闲着没事干')
        await poke.send(Message([{
            "type": "image",
            "data": {
                "file": url
            }
        }]))
    elif r == 4:
        img_p = Image.open(path)
        draw_text(img_p, '戳你妈', 0)
        draw_text(img_p, '有尝试过玩Cytus II吗', 400)
        await poke.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(img_p), encoding='utf-8')}"
            }
        }]))
    elif r == 5:
        await poke.send(Message('呜呜呜...不要再戳啦...'))
    elif r <= 7 and r > 5:
        await poke.send(Message([{
            "type": "image",
            "data": {
                "file": f"https://www.diving-fish.com/images/poke/{r - 5}.gif",
            }
        }]))
    elif r <= 12 and r > 7:
        await poke.send(Message([{
            "type": "image",
            "data": {
                "file": f"https://www.diving-fish.com/images/poke/{r - 7}.jpg",
            }
        }]))
    elif r <= 17 and r > 12:
        await poke.send(Message(f'好的....大家请各位戳刚刚戳我的那位。'))
    elif r <= 19 and r > 17:
        t = random.randint(60,90)
        try:
            await bot.set_group_ban(group_id=event.__getattribute__('group_id'), user_id=event.sender_id, duration=t)
            await poke.send(f'别戳了！！烟你{t}秒冷静一下。')
        except Exception as e:
            print(e)
            await poke.send(Message('一天到晚就知道戳戳戳，你不许戳了！(╬▔皿▔)╯'))
    elif r == 1:
        await poke.send(Message('一天到晚就知道戳戳戳，戳自己肚皮不行吗？'))
    else:
        await poke.send(Message([{
            "type": "poke",
            "data": {
                "qq": f"{event.sender_id}"
            }
        }]))

async def send_poke_stat(group_id: int, bot: Bot):
    if group_id not in poke_dict:
        return
    else:
        group_stat = poke_dict[group_id]
        sorted_dict = {k: v for k, v in sorted(group_stat.items(), key=lambda item: item[1], reverse=True)}
        index = 0
        data = []
        for k in sorted_dict:
            data.append((k, sorted_dict[k]))
            index += 1
            if index == 3:
                break
        await bot.send_msg(group_id=group_id, message="※> 戳一戳总结\n欢迎来到“金中指奖”的颁奖现场！\n接下来公布一下上次重启以来，本群最JB闲着没事 -- 干玩戳一戳的获奖者。")
        await asyncio.sleep(1)
        if len(data) == 3:
            await bot.send_msg(group_id=group_id, message=Message([
                {"type": "text", "data": {"text": "※> 戳一戳总结 - 铜牌\n铜中指奖的获得者是"}},
                {"type": "at", "data": {"qq": f"{data[2][0]}"}},
                {"type": "text", "data": {"text": f"!!\n累计戳了 {data[2][1]} 次！\n让我们恭喜这位闲的没事干的家伙！"}},
            ]))
            await asyncio.sleep(1)
        if len(data) >= 2:
            await bot.send_msg(group_id=group_id, message=Message([
                {"type": "text", "data": {"text": "※> 戳一戳总结 - 银牌\n银中指奖的获得者是"}},
                {"type": "at", "data": {"qq": f"{data[1][0]}"}},
                {"type": "text", "data": {"text": f"!!\n累计戳了 {data[1][1]} 次！\n这太几把闲得慌了，请用中指戳戳自己肚皮解闷!"}},
            ]))
            await asyncio.sleep(1)
        await bot.send_msg(group_id=group_id, message=Message([
            {"type": "text", "data": {"text": "※> 戳一戳总结 - 金牌\n最JB离谱的!!金中指奖的获得者是"}},
            {"type": "at", "data": {"qq": f"{data[0][0]}"}},
            {"type": "text", "data": {"text": f"!!!\nTA一共戳了{data[0][1]}次，此时此刻我想询问获奖者一句话:就那么喜欢听我骂你吗?"}},
        ]))


poke_stat = on_command("本群戳一戳情况")


@poke_stat.handle()
async def _(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id
    await send_poke_stat(group_id, bot)


poke_setting = on_command("戳一戳设置")


@poke_setting.handle()
async def _(bot: Bot, event: Event, state: T_State):
    db = get_driver().config.db
    group_members = await bot.get_group_member_list(group_id=event.group_id)
    for m in group_members:
        if m['user_id'] == event.user_id:
            break
    if m['role'] != 'owner' and m['role'] != 'admin' and str(m['user_id']) != Config.superuser:
        await poke_setting.finish("这个...只有管理员可以设置戳一戳, 但是你不要去戳我....嗯..尽量别戳啦。")
        return
    argv = str(event.get_message()).strip().split(' ')
    try:
        if argv[0] == "默认":
            c = await db.cursor()
            await c.execute(f'update group_poke_table set disabled=0, strategy="default" where group_id={event.group_id}')
        elif argv[0] == "限制":
            c = await db.cursor()
            await c.execute(
                f'update group_poke_table set disabled=0, strategy="limited{int(argv[1])}" where group_id={event.group_id}')
        elif argv[0] == "禁用":
            c = await db.cursor()
            await c.execute(
                f'update group_poke_table set disabled=1 where group_id={event.group_id}')
        else:
            raise ValueError
        await poke_setting.send("设置成功")
        await db.commit()
    except (IndexError, ValueError):
        await poke_setting.finish("※> 戳一戳设置 - 帮助\n本命令的格式:\n戳一戳设置 <默认/限制 (秒)/禁用>\n\n - 默认:将启用默认的戳一戳设定，包括随机性抽中禁言 1 - 1 分 30 秒。\n - 限制 (秒):在戳完一次 Kiba 的指定时间内，调用戳一戳只会让 Kiba 反过来戳你。在指定时间外时，与默认相同。\n- 禁用:禁用戳一戳的相关功能。")
    pass

shuffle = on_command('shuffle')


@shuffle.handle()
async def _(bot: Bot, event: Event):
    argv = int(str(event.get_message()))
    if argv > 100:
        await shuffle.finish('❌> 随机排列 - 数字过大\n随机排列太多了会刷屏，请输入100以内的数字。')
        return
    d = [str(i + 1) for i in range(argv)]
    random.shuffle(d)
    await shuffle.finish(','.join(d))

roll = on_regex(r"^([1-9]\d*)r([1-9]\d*)")

@roll.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "([1-9]\d*)r([1-9]\d*)"
    groups = re.match(regex, str(event.get_message())).groups()
    try:
        num = random.randint(int(groups[0]),int(groups[1]))
        await roll.send(f"※> 随机数\n您的随机数是{num}。")
    except Exception:
        await roll.send("❌> 随机数 - 错误\n语法有错哦，您是不是输入的浮点数还是落了一个？或者左面比右面的数字大？这都是不可以的。")

tz = on_regex(r"^投骰子([1-9]\d*)")

@tz.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "投骰子([1-9]\d*)"
    groups = re.match(regex, str(event.get_message())).groups()
    try:
        if int(groups[0]) > 10:
            await roll.send("❌> 骰子 - 过多\n骰子数量不能大于10个。你是要刷屏嘛？")
        else:
            s = "※> 骰子\n结果如下："
            for i in range(int(groups[0])):
                num = random.randint(1,6)
                s += f'\n第 {i + 1} 个骰子 投掷结果是: {num}点'
            await roll.send(s)
    except Exception:
        await roll.send("❌> 骰子 - 错误\n语法上可能有错哦。再检查一下试试吧！")

tz_100 = on_regex(r"^投百面骰子([1-9]\d*)")

@tz_100.handle()
async def _(bot: Bot, event: Event, state: T_State):
    regex = "投百面骰子([1-9]\d*)"
    groups = re.match(regex, str(event.get_message())).groups()
    try:
        if int(groups[0]) > 10:
            await roll.send("❌> 百面骰子 - 过多\n骰子数量不能大于10个。你是要刷屏嘛？")
        else:
            s = "※> 百面骰子\n结果如下："
            for i in range(int(groups[0])):
                num = random.randint(1,100)
                s += f'\n第 {i + 1} 个骰子 投掷结果是: {num}点'
            await roll.send(s)
    except Exception:
        await roll.send("❌> 百面骰子 - 错误\n语法上可能有错哦。再检查一下试试吧！")

random_person = on_regex("随个([男女]?)群友")

@random_person.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        gid = event.group_id
        glst = await bot.get_group_member_list(group_id=gid, self_id=int(bot.self_id))
        v = re.match("随个([男女]?)群友", str(event.get_message())).group(1)
        if v == '男':
            for member in glst[:]:
                if member['sex'] != 'male':
                    glst.remove(member)
        elif v == '女':
            for member in glst[:]:
                if member['sex'] != 'female':
                    glst.remove(member)
        m = random.choice(glst)
        await random_person.finish(Message([
        {
            "type": "text",
            "data": {
                "text": f"※> To "
            }
        },
        {
            "type": "at",
            "data": {
                "qq": event.user_id
            }
        }, 
        {
            "type": "text",
            "data": {
                "text": f" | 随人\n{m['card'] if m['card'] != '' else m['nickname']}({m['user_id']})"
            }
        }]))
    except AttributeError:
        await random_person.finish("你不在群聊使用.....所以你随啥呢这是，这个要去群里用。")

snmb = on_regex(r"随个.*", priority=50)

@snmb.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        gid = event.group_id
        if random.random() < 0.5:
            await snmb.finish(Message([
                {"type": "text", "data": {"text": "随你"}},
                {"type": "image", "data": {"file": "https://www.diving-fish.com/images/emoji/horse.png"}}
            ]))
        else:
            glst = await bot.get_group_member_list(group_id=gid, self_id=int(bot.self_id))
            m = random.choice(glst)
            await random_person.finish(Message([
            {
                    "type": "text",
                    "data": {
                        "text": f"※> To "
                }
            },
            {
                "type": "at",
                "data": {
                    "qq": event.user_id
                }
            },
            {
                "type": "text",
                "data": {
                    "text": f" | 随人\n{m['card'] if m['card'] != '' else m['nickname']}({m['user_id']})"
                }
            }]))
    except AttributeError:
        await random_person.finish("你不在群聊使用.....所以你随啥呢这是，这个要去群里用。")


select = on_command("帮选", aliases={"帮我选"})
@select.handle()
async def _(bot: Bot, event: Event, state: T_State):
    nickname = event.sender.nickname
    argv = str(event.get_message()).strip().split(" ")
    if len(argv) == 1:
        await select.finish("❌> 帮选\n选你🐎。")
        return
    elif len(argv) is not None:
        result = random.randint(0, len(argv) - 1)
        await select.finish(f"※> 帮选\n我选 {argv[result]}。")
        return
    else:
        await select.finish("❌> 帮选 - 错误\n选你🐎。")
        return
