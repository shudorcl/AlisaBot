# import nonebot
import json
from random import choice

from nonebot import get_driver, on_command
from nonebot.adapters.cqhttp import MessageEvent, Bot, ActionFailed, MessageSegment, Message, GroupMessageEvent, Event
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from alisabot.utils.request import post_bytes
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

lolicon_url = "https://api.lolicon.app/setu/"
lolicon_key = global_config.lolicon_key
setu = on_command("来点涩图", aliases={"涩图gkd", "来点色图", "色图gkd", "涩图来", "色图来"})
setu_type = 3  # 1为普通发图，2为构造转发，3为大涩图


@setu.handle()
async def setu_handle(bot: Bot, event: GroupMessageEvent):
    global setu_type
    keyword = str(event.get_message()).strip()
    user = event.user_id
    group = event.group_id
    if keyword:
        msgwait = choice([f"正在依据关键词{keyword}发起setu委托",
                          f"{keyword}涩图搜索请求已发出，正等待回复"])
        await bot.send(event, Message(msgwait))
    params = {"apikey": lolicon_key, "r18": "0", "size1200": "true"}
    data = {"msg": ""}
    try:
        data = json.loads(await post_bytes(lolicon_url, params))["data"][0]
    except:
        await setu.finish("请求数据失败")
    msg0 = choice(["已找到目标", "任务完成"])
    await bot.send(event, msg0 + choice(["，正在建立传送连接", "，等待传送中"]))
    try:
        if setu_type == 1:
            pid = data["pid"]
            title = data["title"]
            img = MessageSegment.image(data["url"], proxy=False)
            msg = ""
            msg += Message(f">{MessageSegment.at(user)}\n")
            msg += Message(f"Pid: {pid}\n" f"Title: {title}\n" f"{img}")
            await setu.finish(Message(msg))
        elif setu_type == 2:
            img = MessageSegment.image(data["url"], proxy=False)
            pid = data["pid"]
            title = data["title"]
            msg = Message(f"Pid: {pid}\n" f"Title: {title}\n" f"{img}")
            node = [{
                "type": "node",
                "data": {
                    "name": "某老涩批",
                    "uin": f"{user}",
                    "content": msg
                }
            }
            ]
            await bot.send_group_forward_msg(group_id=group, messages=node)
        elif setu_type == 3:
            msg = f"[CQ:cardimage,file={data['url']}]"
            await setu.finish(Message(msg))
    except ActionFailed:
        await setu.finish(f"消息传输失败，通道似乎受到了管制")


set_setu_type = on_command("setu-type", permission=SUPERUSER)


@set_setu_type.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    arg = str(event.get_message()).strip()
    global setu_type
    typelist = {1: "普通图", 2: "构造转发", 3: "大涩图"}
    former_setu_type = setu_type
    if arg == "1":
        setu_type = 1
    elif arg == "2":
        setu_type = 2
    elif arg == "3":
        setu_type = 3
    else:
        await set_setu_type.finish("请检查输入")
    msg = f"原先的setu类型为{typelist[former_setu_type]}\n"
    msg += "现在的setu类型为" + typelist[int(arg)]
    await set_setu_type.finish(msg)


bugouse = on_command("不够涩", aliases={"不够色"})


@bugouse.handle()
async def bugouse_handle(bot: Bot, event: MessageEvent):
    await bugouse.finish(Message("那你来发"))
