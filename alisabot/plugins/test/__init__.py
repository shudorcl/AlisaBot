# import nonebot
from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

test1 = on_command("testAlisa", permission=SUPERUSER)


@test1.handle()
async def test1_handle(bot: Bot, event: Event, state: T_State):
    name = global_config.nickname
    if "Alisa" in name:
        name = "Alisa"
    await test1.finish(f"收到，我是{name}")


testzhuanfa = on_command("转发测试", permission=SUPERUSER)


@testzhuanfa.handle()
async def handle(bot: Bot, event: GroupMessageEvent):
    user = event.user_id
    group = event.group_id
    msg = "欧内的手，好汉！"
    node = MessageSegment.node_custom(user, "test", msg)
    node2 = [
        {
            "type": "node",
            "data": {
                "name": "消息发送者A",
                "uin": "10086",
                "content": [
                    {
                        "type": "text",
                        "data": {"text": "测试消息1"}
                    }
                ]
            }
        },
        {
            "type": "node",
            "data": {
                "name": "消息发送者B",
                "uin": "10087",
                "content": "[CQ:image,file=xxxxx]测试消息2"
            }
        }
    ]
    await bot.send(event, str(node))
    await bot.send(event, str(node2))
    await bot.send_group_forward_msg(group_id=group, messages=node2)
