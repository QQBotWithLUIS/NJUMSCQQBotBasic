import time

from nonebot import on_natural_language, NLPSession
from function.submit2Tuling import call_tuling_api
# GRP ADD BEGIN
from function.EntitiesSwitch import *
from function.submit2LUISandGetPrediction import get_prediction
from function.submit2QnAGetAns import *
from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression
from config import SUBSCRIPTION_KEY_ENV_NAME
# GRP ADD END
# 定义无法获取图灵回复时的「表达（Expression）」
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)

@on_natural_language(keywords=('',), only_to_me=True)  # 关掉only_to_me可应答群消息
async def get_massage(session: NLPSession):
    start = time.clock()  # 测试总查询用时
    # 获取用户提问
    question = str(session.msg_text.strip())
    print("ques: " + question)
    # 将问题发送给LUIS,获取prediction
    prediction = get_prediction(SUBSCRIPTION_KEY_ENV_NAME, question)
    print(prediction.as_dict())  # 将数据库读取结果作为字典进行输出

    ans = ""
    # 判断有无实体
    if len(prediction.entities) > 0:
        ans = entities_match_from_file(prediction)
    # 从自定义文件获取回答
    if not ans:
        ans = get_answers_from_file(prediction.top_scoring_intent.intent)
    # 从图灵机器人获取回答
    if not ans:
        ans = await call_tuling_api(session,question)
    if not ans:
        await session.send(render_expression(EXPR_DONT_UNDERSTAND))
    await session.send(ans)

