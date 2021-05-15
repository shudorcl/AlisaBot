# import nonebot
import json
import re
from random import randint

from nonebot import get_driver, on_regex, on_message
from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import Message, MessageEvent

from alisabot.utils.request import post_bytes
from alisabot.utils.translate import to_simple_string
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

EAT_URL = "https://wtf.hiigara.net/api/run/{}"

eat_wat = on_regex(r"[今|明|后|大后]天(.*?)吃什么")


@eat_wat.handle()
async def _eat(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).strip()
    user = event.user_id
    user_n = event.sender.nickname
    arg = re.findall(r"大?[今|明|后]天(.*?)吃什么", msg)[0]
    nd = re.findall(r"大?[今|明|后]天", msg)[0]

    if arg == "中午":
        a = f"LdS4K6/{randint(0, 999999)}"
        url = EAT_URL.format(a)
        params = {"event": "ManualRun"}
        data = json.loads(await post_bytes(url, params))

        text = to_simple_string(data['text']).replace('今天', nd)
        get_a = re.search(r"非常(.*?)的", text)[0]
        result = f"> [CQ:at,qq={user}]\n" + text.replace(get_a, '')

    elif arg == "晚上":
        a = f"KaTMS/{randint(0, 999999)}"
        url = EAT_URL.format(a)
        params = {"event": "ManualRun"}
        data = json.loads(await post_bytes(url, params))

        text = to_simple_string(data['text']).replace('今天', '')
        result = f"> [CQ:at,qq={user}]\n" + text

    else:
        rd = randint(1, 10)
        if rd == 5:
            result = "吃我吧 ❤"
        else:
            a = f"JJr1hJ/{randint(0, 999999)}"
            url = EAT_URL.format(a)
            params = {"event": "ManualRun"}
            data = json.loads(await post_bytes(url, params))

            text = to_simple_string(data['text']).replace('今天', nd)
            get_a = re.match(r"(.*?)的智商", text)[0]
            result = f"> [CQ:at,qq={user}]\n" + text.replace(get_a, f'{user_n}的智商')

    await eat_wat.finish(Message(result))


me_to_you = on_message()


@me_to_you.handle()
async def _me_to_you(bot: Bot, event: MessageEvent) -> None:
    if randint(0, 15) == 5:
        msg = str(event.message)
        if "我" in msg and "CQ" not in msg:
            await me_to_you.finish(msg.replace("我", "你"))


girl_test = on_command("girltest")


@girl_test.handle()
async def girltesthandle(bot: Bot, event: MessageEvent):
    keyword = str(event.message).strip()
    user = event.user_id
    name = event.sender.nickname
    if keyword:
        name = keyword
    a = f"MtnVv9/{name}"
    url = EAT_URL.format(a)
    params = {"event": "ManualRun"}
    data = json.loads(await post_bytes(url, params))
    text = to_simple_string(data['text'])
    result = f"> [CQ:at,qq={user}]\n" + text
    await girl_test.finish(Message(result))
