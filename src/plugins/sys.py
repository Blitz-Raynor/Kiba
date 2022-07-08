from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters import Event, Bot
import platform
import time
using_distro = False
try:
    import distro
    using_distro = True
except ImportError:
    pass


start = time.time()
start = int(start)

systeminfo = on_command("systeminfo", aliases={"系统状态", "ping", "Ping"} ,priority=5)

@systeminfo.handle()
async def _(bot: Bot, event: Event):
    python_version = platform.python_version()
    arch = platform.architecture()
    node = platform.node()
    platform_version = platform.platform()
    processor = platform.processor()
    build_time = platform.python_build()
    system = platform.system()
    release = platform.release()
    m, s = divmod((int(time.time()) - start), 60)
    h, m = divmod(m, 60)
    result = "▾ 系统状态\n"
    flag = False
    if using_distro == True:
        flag = True
        if distro.name() == "" and distro.version() == "":
            flag = False
    if flag == False:
        result += "系统类型：" + system + "\n系统版本号：" + release + "\n系统架构：" + arch[0] + "\n处理器信息：" + processor + "\n设备名：" + node + "\n系统版本：" + platform_version + "\nPython 版本：" + python_version + "\nPython 构建时间：" + build_time[1] + "\nKiba 运行时间：" + str(h) + "h " + str(m) + "min " + str(s) + "s"
        await systeminfo.send(result)
    elif flag == True:
        distro_name = distro.name()
        distro_version = distro.version()
        result += "系统类型：" + system + "\n系统版本号：" + release + "\n系统架构：" + arch[0] + "\n处理器信息：" + processor + "\n设备名：" + node + "\nLinux 发行版：" + distro_name + "\nLinux 发行版版本：" + distro_version + "\nPython 版本：" + python_version + "\nPython 构建时间：" + build_time[1] + "\nBot 运行时间：" + str(h) + "h " + str(m) + "min " + str(s) + "s"
        await systeminfo.send(result)