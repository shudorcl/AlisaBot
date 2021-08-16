import random
import re

from nonebot.adapters.cqhttp import Message, MessageSegment

from .deck import DeckDict


def draw_handler(args: str) -> list:
    ReturnList = []
    DrawList = []
    if "张" not in args:
        if args not in DeckDict.keys():
            ReturnList.append("没有这个牌堆可怎么抽？难道让我闪光印卡吗~")
            ReturnList.append("现在的牌堆有：\n" + "\n".join(DeckDict.keys()))
            return ReturnList
        if args == "塔罗牌":
            tarot = random.sample(DeckDict[args], k=3)[0]
            position = random.sample(['positive', 'negative'], k=1)[0]
            if position == 'positive':
                position_text = '正位'
            else:
                position_text = '逆位'
            ReturnList.append(f"【{position_text}】/{tarot['name']}\n{tarot[position]}")
        else:
            ReturnList.append(random.sample(DeckDict[args], k=3)[0])
        return ReturnList
    num = re.search(r"(.*)张", args).group(1)
    deck = re.search(r"张(.*)", args).group(1)
    try:
        num = int(num)
    except ValueError:
        ReturnList.append("张数输入错误~目前只支持阿拉伯数字喔~")
        return ReturnList
    if deck not in DeckDict.keys():
        ReturnList.append("没有这个牌堆可怎么抽？难道让我闪光印卡吗~")
        ReturnList.append("现在的牌堆有：\n" + "\n".join(DeckDict.keys()))
        return ReturnList
    elif num > len(DeckDict[deck]):
        ReturnList.append(f"{num}张也太多了，整个牌堆抽完都不够用的")
        return ReturnList
    msg = f"锵锵锵，我们就来看看在{deck}中会抽到什么！\n"
    if deck == "塔罗牌":
        TarotList = random.sample(DeckDict[deck], k=num)
        for card in TarotList:
            position = random.choice(['正位', '逆位'])
            DrawList.append(f"【{position}】/{card['name']}")
    else:
        DrawList = random.sample(DeckDict[deck], k=num)
    msg += "\n".join(DrawList)
    ReturnList.append(msg)
    return ReturnList


def jrrp_handler(uid: str) -> list:
    ReturnList = []
    at_msg = Message(f">{MessageSegment.at(uid)}\n")
    rp_msg = at_msg + random.choice(["要我测测您今天的人品嘛？今天的人品指数是", "根据占星学和量子力学，对您今天人品观测的结果是", "根据我们大型量子计算机的预测，您今天的人品指数为"])
    rp = random.randint(1, 100)
    if rp > 90:
        rp_msg += f"——{rp}!!!\n"
        rp_msg += random.choice(["看来今天是个买彩票的好日子呢~", "快去抽卡吧少年！"])
        rp_msg += "不过，还是得小心点喔"
    elif rp > 60:
        rp_msg += f"——{rp}\n"
        rp_msg += random.choice(["出去走走吧，没准可以遇到好事", "或许喝饮料能够中奖？"])
    elif rp > 30:
        rp_msg += f"{rp}\n"
        rp_msg += random.choice(["又是平凡的一天，不过这也不错嘛", "今天也是好天气呢~"])
    else:
        rp_msg += f"——呃，{rp}\n"
        rp_msg += random.choice(["今天恐怕得小心行事了。。。", "总而言之谨慎一点也不坏是吧~"])
    ReturnList.append(Message(rp_msg))
    if rp < 30:
        ReturnList.append(Message("不过话又说回来我也不一定准，别放在心上啦"))
    return ReturnList
