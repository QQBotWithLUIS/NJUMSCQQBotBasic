
from submit2LUISandGetPrediction import get_prediction

SUBSCRIPTION_KEY_ENV_NAME = "36fb4cae87a246169da2edf98e082113"

if __name__ == "__main__":
    # 获取用户提问
    # question = get_question()
    question = "活动部是干什么的"

    # 将问题发送给LUIS,获取prediction
    prediction = get_prediction(SUBSCRIPTION_KEY_ENV_NAME,question)
    print (prediction.as_dict())

    ans = ""
    print (len(prediction.entities))
    # 判断有无实体
    if len(prediction.entities) > 0:
        # 调用处理实体的函数并获得回答
        # ans = ""
        pass
    else:
        # 将prediction发送给QnA maker 
        # ans = "" 
        pass
    
    # 将ans返回给用户

