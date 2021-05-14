# import nonebot
from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters import Bot, Event
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
