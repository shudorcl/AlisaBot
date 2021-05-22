# import nonebot

import json
import os
import re
from io import BytesIO
from pathlib import Path
from random import randint, choice

from PIL import Image
from nonebot import get_driver, on_regex, on_message
from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import Message, MessageEvent, ActionFailed

from alisabot.utils.request import post_bytes, get_bytes, get_content
from alisabot.utils.translate import to_simple_string
from .config import Config
from .data_source import generate_gif, dragon_reco

global_config = get_driver().config
config = Config(**global_config.dict())

TestUrl = "https://wtf.hiigara.net/api/run/{}"

eat_wat = on_regex(r"[今|明|后|大后]天(.*?)吃什么", priority=5)


@eat_wat.handle()
async def _eat(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).strip()
    user = event.user_id
    user_n = event.sender.nickname
    arg = re.findall(r"大?[今|明|后]天(.*?)吃什么", msg)[0]
    nd = re.findall(r"大?[今|明|后]天", msg)[0]

    if arg == "中午":
        a = f"LdS4K6/{randint(0, 999999)}"
        url = TestUrl.format(a)
        params = {"event": "ManualRun"}
        data = json.loads(await post_bytes(url, params))

        text = to_simple_string(data['text']).replace('今天', nd)
        get_a = re.search(r"非常(.*?)的", text)[0]
        result = f"> [CQ:at,qq={user}]\n" + text.replace(get_a, '')

    elif arg == "晚上":
        a = f"KaTMS/{randint(0, 999999)}"
        url = TestUrl.format(a)
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
            url = TestUrl.format(a)
            params = {"event": "ManualRun"}
            data = json.loads(await post_bytes(url, params))

            text = to_simple_string(data['text']).replace('今天', nd)
            get_a = re.match(r"(.*?)的智商", text)[0]
            result = f"> [CQ:at,qq={user}]\n" + text.replace(get_a, f'{user_n}的智商')

    await eat_wat.finish(Message(result))


girl_test = on_command("girltest", priority=5)


@girl_test.handle()
async def girltesthandle(bot: Bot, event: MessageEvent):
    keyword = str(event.message).strip()
    user = event.user_id
    name = event.sender.nickname
    if keyword:
        name = keyword
    a = f"MtnVv9/{name}"
    url = TestUrl.format(a)
    params = {"event": "ManualRun"}
    data = json.loads(await post_bytes(url, params))
    text = to_simple_string(data['text'])
    result = f"> [CQ:at,qq={user}]\n" + text
    await girl_test.finish(Message(result))


rua = on_command("rua", priority=5)

data_dir = Path('.') / 'alisabot' / 'plugins' / 'fun' / 'data'
data_dir = os.path.abspath(data_dir)


@rua.handle()
async def creep(bot: Bot, event: MessageEvent):
    raw_msg = str(event.raw_message)
    creep_id = re.findall(r"\[CQ:at,qq=(.*?)\]", raw_msg)
    if len(creep_id):
        creep_id = creep_id[0]
    else:
        await rua.finish(f"没找到rua谁呢")
        return
    url = f'http://q1.qlogo.cn/g?b=qq&nk={creep_id}&s=160'
    resp = await get_bytes(url)
    avatar = Image.open(BytesIO(resp))
    try:
        output = generate_gif(data_dir, avatar, creep_id)
    except Exception as e:
        await rua.finish(f"rua不出来，按理说应该没问题的。。。\n揭示是{e}")
        return
    msg = f'[CQ:image,file=file:///{output}]'
    # msg = MessageSegment.image("///"+output)
    try:
        await bot.send(event, Message(msg))
    except ActionFailed:
        await bot.send(event, "rua不出来，被管住叻...")


dragon_recongnize = on_message(priority=5)


@dragon_recongnize.handle()
async def handler(bot: Bot, event: MessageEvent):
    msg = str(event.message)
    dragon_url = re.findall(r"url=(.*?)]", msg)
    if len(dragon_url):
        dragon_url = dragon_url[0]
    else:
        return
    dragon = await get_content(dragon_url)
    if dragon_reco(dragon):
        if randint(1, 15) < 6:
            await dragon_recongnize.finish(choice(["我看到龙了", "卧槽，龙！", "我发现了龙！"]))
