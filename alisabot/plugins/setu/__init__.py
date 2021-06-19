# import nonebot
import json
from random import choice, randint

from nonebot import get_driver, on_command, on_keyword
from nonebot.adapters.cqhttp import MessageEvent, Bot, ActionFailed, Message, GroupMessageEvent, Event
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from varname import nameof

from alisabot.utils.request import post_bytes
from alisabot.utils.rule import check_control_function
from .config import Config
from .data_source import setu_msg

global_config = get_driver().config
config = Config(**global_config.dict())

lolicon_url = "https://api.lolicon.app/setu/"
lolicon_url_v2 = "https://api.lolicon.app/setu/v2"
lolicon_key = global_config.lolicon_key
setu = on_command("来点涩图", aliases={"涩图gkd", "来点色图",
                                   "色图gkd", "涩图来", "色图来"}, priority=5)
setu_type = 1  # 1为普通发图，2为构造转发，3为大涩图
setu_name = nameof(setu)


@setu.handle()
async def setu_handle(bot: Bot, event: GroupMessageEvent):
    global setu_type, setu_name
    keyword = str(event.get_message()).strip()
    user = event.user_id
    group = event.group_id
    if not check_control_function(setu_name, group):
        await setu.finish(f"{setu_name}是不允许的！")
    if keyword:
        msgwait = choice([f"正在依据关键词{keyword}发起setu委托",
                          f"{keyword}涩图搜索请求已发出，正等待回复"])
        params = {"r18": "0", "tag": [keyword], "size": ["regular"]}
        await bot.send(event, Message(msgwait))
    else:
        params = {"r18": "0", "size": ["original", "regular"]}
    data = {"msg": ""}
    try:
        data = json.loads(await post_bytes(lolicon_url_v2, params))["data"][0]
    except:
        await setu.finish("请求数据失败")
    try:
        if setu_type != 2:
            try:
                await setu.finish(setu_msg(data, setu_type, user))
            except ActionFailed:
                await bot.send(event, "那就正常发吧，虽然可能还会有问题就是了~")
                await setu.finish(setu_msg(data, 1, user))
        elif setu_type == 2:
            node = [{
                "type": "node",
                "data": {
                    "name": "某老涩批",
                    "uin": f"{user}",
                    "content": setu_msg
                }
            }]
            try:
                await bot.send_group_forward_msg(group_id=group, messages=node)
            except ActionFailed:
                await bot.send(event, "果然迫害人是不好的，那就正常发吧，虽然可能还会有问题就是了~")
                await setu.finish(setu_msg(data, 1, user))
    except ActionFailed:
        await setu.finish(f"消息传输失败，通道似乎受到了管制")


set_setu_type = on_command("setu-type", permission=SUPERUSER, priority=5)


@set_setu_type.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    arg = str(event.get_message()).strip()
    global setu_type
    typelist = {1: "普通图", 2: "构造转发", 3: "大涩图"}
    former_setu_type = setu_type
    if arg not in ["1", "2", "3"]:
        await set_setu_type.finish("请检查输入")
    setu_type = int(arg)
    msg = f"原先的setu类型为{typelist[former_setu_type]}\n"
    msg += "现在的setu类型为" + typelist[int(arg)]
    await set_setu_type.finish(msg)


bugouse = on_keyword({"不够涩", "不够色"}, priority=5)


@bugouse.handle()
async def bugouse_handle(bot: Bot, event: MessageEvent):
    await bugouse.finish(Message("那你来发" + "❤" if (randint(1, 15) < 5) else ""))
