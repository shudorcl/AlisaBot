import json

from nonebot import get_driver
from nonebot.adapters.cqhttp.utils import escape as message_escape
from nonebot.plugin import on_command
from nonebot.typing import Bot, Event

from alisabot.utils.request import post_bytes

global_config = get_driver().config
RUN_API_URL_FORMAT = "https://run.glot.io/languages/{}/latest"
SUPPORTED_LANGUAGES = {
    "assembly": {"ext": "asm"},
    "bash": {"ext": "sh"},
    "c": {"ext": "c"},
    "clojure": {"ext": "clj"},
    "coffeescript": {"ext": "coffe"},
    "cpp": {"ext": "cpp"},
    "csharp": {"ext": "cs"},
    "erlang": {"ext": "erl"},
    "fsharp": {"ext": "fs"},
    "go": {"ext": "go"},
    "groovy": {"ext": "groovy"},
    "haskell": {"ext": "hs"},
    "java": {"ext": "java", "name": "Main"},
    "javascript": {"ext": "js"},
    "julia": {"ext": "jl"},
    "kotlin": {"ext": "kt"},
    "lua": {"ext": "lua"},
    "perl": {"ext": "pl"},
    "php": {"ext": "php"},
    "python": {"ext": "py"},
    "ruby": {"ext": "rb"},
    "rust": {"ext": "rs"},
    "scala": {"ext": "scala"},
    "swift": {"ext": "swift"},
    "typescript": {"ext": "ts"},
}
api_token = global_config.glot_key

coderunner = on_command("code_runner", aliases={"run", "运行代码", "运行", "执行代码"})


@coderunner.handle()
async def _(bot: Bot, event: Event, state: dict):
    args = str(event.get_message()).strip()

    if args:
        state['args'] = args
        language, *remains = state['args'].split("\n", maxsplit=1)
        language = language.strip()
        if language not in SUPPORTED_LANGUAGES:
            await bot.finish("暂时不支持运行你输入的编程语言")
        state["language"] = language

        if remains:
            code = remains[0].strip()  # type: ignore
            if code:
                state["code"] = code


supported_languages = ", ".join(sorted(SUPPORTED_LANGUAGES))


@coderunner.got("language", prompt=f"你想运行的代码是什么语言？\n目前支持 {supported_languages}")
@coderunner.got("code", prompt='请输入你要运行的代码')
async def _(bot: Bot, event: Event, state: dict) -> None:
    code = state['code']
    language = state["language"]
    if language not in SUPPORTED_LANGUAGES:
        await bot.finish("暂时不支持运行你输入的编程语言")
    await bot.send(event, "正在运行，请稍等……")
    url = RUN_API_URL_FORMAT.format(language)
    data = {
        "files": [
            {
                "name": (SUPPORTED_LANGUAGES[language].get("name", "main"))
                        + f'.{SUPPORTED_LANGUAGES[language]["ext"]}',
                "content": code,
            }
        ],
    }
    headers = {"Authorization": f"Token {api_token}"}
    resp = await post_bytes(url, data, headers)
    if not resp:
        await coderunner.finish("运行失败，服务可能暂时不可用，请稍后再试。")
    sent = False
    resp = json.loads(resp)
    for output_name in ["stdout", "stderr", "error"]:
        output_text = resp.get(output_name)
        lines = output_text.splitlines()
        lines, remained_lines = lines[:10], lines[10:]
        out = "\n".join(lines)
        out, remained_out = out[: 60 * 10], out[60 * 10:]

        if remained_lines or remained_out:
            out += f"\n太长力，不打了"
        out = message_escape(out)
        if out:
            await bot.send(event, f"{output_name}:\n{out}")
            sent = True
    if not sent:
        await coderunner.finish("运行成功，没有任何输出")
