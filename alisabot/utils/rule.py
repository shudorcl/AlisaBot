import json
import os
from pathlib import Path
from typing import Optional

from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.rule import Rule


def check_control_function(function_name: str, group: int) -> bool:
    switch_all_path = Path('.') / 'alisabot' / 'data' / 'switch.json'
    switch_alone_dir = Path(
        '.') / 'alisabot' / 'data' / 'Group' / f"{group}"
    switch_alone_path = Path(
        '.') / 'alisabot' / 'data' / 'Group' / f"{group}" / 'switch.json'
    if not os.path.exists(switch_alone_dir):
        os.makedirs(switch_alone_dir)
    # 检查文件是否存在，如不存在，自动创建并写入默认值
    if not switch_all_path.is_file():
        with open(switch_all_path, 'w+') as f:
            f.write(json.dumps({}))
            f.close()
    if not switch_alone_path.is_file():
        try:
            os.mkdir(
                Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}')
        except:
            pass

        with open(switch_alone_path, 'w') as f:
            f.write(json.dumps({}))
            f.close()
    with open(switch_all_path, 'r') as f:
        data_all = json.load(f)
        f.close()

    with open(switch_alone_path, 'r') as f:
        data_alone = json.load(f)
        f.close()
    if function_name not in data_all:
        data_all[function_name] = "True"
        with open(switch_all_path, 'w') as f:
            f.write(json.dumps(data_all))
            f.close()

    if function_name not in data_alone:
        data_alone[function_name] = "True"
        with open(switch_alone_path, 'w') as f:
            f.write(json.dumps(data_alone))
            f.close()
        # 判断目标
    if data_all[function_name] == "True" and data_alone[function_name] == "True":
        return True
    else:
        return False


def check_switch(func_name: str, notice: bool) -> Rule:
    async def _check_switch(bot: Bot, event: GroupMessageEvent, state: dict) -> bool:
        # 获取目标信息
        group = event.group_id
        return check_control_function(func_name, group)

    return Rule(_check_switch)


def plugin_control(func_name: str,
                   control: bool,
                   group: Optional[str] = None) -> str:
    file_switch_all = Path('.') / 'alisabot' / 'data' / 'switch.json'

    if group:
        file_switch_group = Path(
            '.') / 'alisabot' / 'data' / 'Group' / f"{group}" / 'switch.json'
        try:
            with open(file_switch_group, 'r') as f:
                data_switch_group = json.load(f)
        except FileNotFoundError:
            data_switch_group = {}

        if data_switch_group[f"{func_name}"]:
            pass
        else:
            return f"Can't find func({func_name})"

        data_switch_group[f"{func_name}"] = f"{control}"

        with open(file_switch_group, 'w') as f:
            f.write(json.dumps(data_switch_group))
            f.close()

    else:
        with open(file_switch_all, 'r') as f:
            try:
                data_switch_all = json.load(f)
            except:
                data_switch_all = {}

        if not data_switch_all[f"{func_name}"]:
            return f"Can't find func({func_name})"

        data_switch_all[f"{func_name}"] = f"{control}"

        with open(file_switch_all, 'w') as f:
            f.write(json.dumps(data_switch_all))
            f.close()

    if control:
        if group:
            msg = f"({func_name}) has been opened for group ({group})!"
        else:
            msg = f"({func_name}) has been opened for all group"

    else:
        if group:
            msg = f"({func_name}) has been closed for group ({group})!"
        else:
            msg = f"({func_name}) has been closed for all group!"

    return msg
