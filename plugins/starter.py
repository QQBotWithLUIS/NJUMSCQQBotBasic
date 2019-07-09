import time

from nonebot import on_natural_language, NLPSession

# GRP ADD BEGIN
from function.EntitiesSwitch import *
from function.submit2LUISandGetPrediction import get_prediction
from function.submit2QnAGetAns import *

# GRP ADD END

SUBSCRIPTION_KEY_ENV_NAME = "36fb4cae87a246169da2edf98e082113"


@on_natural_language(keywords=('',), only_to_me=True)  # 关掉only_to_me可应答群消息
async def get_massage(session: NLPSession):
    start = time.clock()  # 测试总查询用时
    # 获取用户提问
    question = str(session.msg_text.strip())
    # 将问题发送给LUIS,获取prediction
    prediction = get_prediction(SUBSCRIPTION_KEY_ENV_NAME, question)
    print(prediction.as_dict())  # 将数据库读取结果作为字典进行输出

    ans = ""
    # 判断有无实体
    if len(prediction.entities) > 0:
        # GRP ADD BEGIN
        # entities_index = entities_match(prediction.entities)
        entities_index = entities_module_match(prediction)
        if entities_index == -1:
            ans = ""
            # 在这里可以添加一个对管理员的反馈，此时两端的实体识别不一致，出现了匹配的缺失
        elif entities_index == 0:
            ans = get_weather_ans(prediction.entities)
            await session.send(ans)
            
        else:
            # ans = entities_ans(entities_index)
            ans = entities_module_ans(entities_index)
            await session.send(ans)
        # GRP ADD END
        pass
    else:
        query = {
            'question': question,
            'top': 1
        }
        print("ques" + question)
        ans = get_answers_from_file(question)
        print("ans" + ans)
        if ans == "No answer":
            ans = "呜呜呜人家不知道说什么啦" # RPG's advice        
        end = time.clock()
        await session.send(ans)
