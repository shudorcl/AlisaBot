from typing import Dict

from nonebot.adapters.cqhttp import MessageSegment, Message


def setu_msg(data: Dict, type: int, user: int) -> Message:
    msg = ""
    pid = data["pid"]
    title = data["title"]
    img_url = data["urls"]["original"]
    img = MessageSegment.image(img_url, proxy=False)
    setu = Message(f"Pid: {pid}\n" f"Title: {title}\n" f"{img}")
    at_msg = Message(f">{MessageSegment.at(user)}\n")
    if type == 3:
        msg = f"[CQ:cardimage,file={img_url}]"
    elif type == 1:
        msg = at_msg + setu
    return Message(msg)
