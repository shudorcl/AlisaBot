# import nonebot
from nonebot import get_driver, on_message
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent

from .config import Config
from .data_source import forbidden_word

global_config = get_driver().config
config = Config(**global_config.dict())

delete_msg = on_message(priority=5)


@delete_msg.handle()
async def delete_msg_handle(bot: Bot, event: GroupMessageEvent):
    '''
    撤回违规消息，在data_source中修改违禁词列表
    '''
    msg_id = event.message_id
    msg = event.get_plaintext()
    for i in forbidden_word:
        if i in msg:
            await bot.call_api("delete_msg", **{'message_id': msg_id})
            await bot.send(event, f"在消息{msg_id}发现违禁词，已排除")
            break
