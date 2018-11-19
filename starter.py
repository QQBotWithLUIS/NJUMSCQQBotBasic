from submit2LUISandGetPrediction import get_prediction
# GRP ADD BEGIN
from EntitiesSwitch import entities_match
from EntitiesSwitch import entities_ans
from EntitiesSwitch import entities_module_match
from EntitiesSwitch import entities_module_ans

# GRP ADD END

from none import on_natural_language,NLPSession



SUBSCRIPTION_KEY_ENV_NAME = "36fb4cae87a246169da2edf98e082113"


@on_natural_language(keywords=('',))
async def getMassage(session: NLPSession):

    # 获取用户提问
    question=str(session.msg_text.strip())
    # 将问题发送给LUIS,获取prediction
    prediction = get_prediction(SUBSCRIPTION_KEY_ENV_NAME,question)
    # print("得到的划分为：")
    print (prediction.as_dict()) #将数据库读取结果作为字典进行输出
    # print ("得到的划分:\n" + prediction.as_dict())

    ans = ""
    print (len(prediction.entities))
    # print (prediction.entities[0].as_dict()['entity'])
    # 判断有无实体
    if len(prediction.entities) > 0:
        # GRP ADD BEGIN
        # entities_index = entities_match(prediction.entities)
        entities_index = entities_module_match(prediction.entities)
        if entities_index == -1:
            ans = ""
            #在这里可以添加一个对管理员的反馈，此时两端的实体识别不一致，出现了匹配的缺失
        else:
            # ans = entities_ans(entities_index)
            ans = entities_module_ans(entities_index)

        #test code

        print(ans)
        # GRP ADD END
        # 调用处理实体的函数并获得回答
        # ans = ""
        pass
    else:
        # 将prediction发送给QnA maker
        # ans = ""
        pass
    # 将ans返回给用户
