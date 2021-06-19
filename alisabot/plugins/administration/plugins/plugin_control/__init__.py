import json
import re
from pathlib import Path

from nonebot import get_driver
from nonebot.adapters.cqhttp import GROUP_ADMIN, GROUP_OWNER, Bot, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command

from alisabot.utils.rule import plugin_control

global_config = get_driver().config
superusers = global_config.superusers
switch = on_command('/switch',
                    permission=(SUPERUSER | GROUP_OWNER | GROUP_ADMIN))


@switch.handle()
async def _(bot: Bot, event: GroupMessageEvent) -> None:
    user = str(event.user_id)
    group = str(event.group_id)
    func = str(event.message).strip()

    switch_path = Path('.') / 'alisabot' / 'data' / 'switch.json'
    with open(switch_path, 'r') as f:
        data = json.load(f)
        funclist = []
        for i in data:
            funclist.append(i)
    if not func:
        msg = "现在注册控制的功能有："
        for i in funclist:
            msg += i
            msg += " "
        msg.strip()
        await switch.finish(msg)

    funct = re.findall(r"[on|off]-(.*)", func)

    if "all-on" in func:
        if int(user) in superusers:
            await switch.finish(plugin_control(funct[0], True))

        else:
            await switch.finish("Permission Denied")

    elif "all-off" in func:
        if int(user) in superusers:
            await switch.finish(plugin_control(funct[0], False))

        else:
            await switch.finish("Permission Denied")

    elif "on" in func:
        await switch.finish(plugin_control(funct[0], True, group))

    elif "off" in func:
        await switch.finish(plugin_control(funct[0], False, group))

    else:
        await switch.finish("请检查输入")
