import random
from function.weather import query_weather
from config import ENTITY_FILEPATH
import json



def entities_match_from_file(full_data):
    """前面的函数虽然实现了一定的功能，但是在同一大类的实体识别的时候，运维十分的繁琐
       或许可以增加一个以大类进行识别的方式"""

    entity_data = full_data.entities
    intent_data = full_data.top_scoring_intent.intent

    if full_data.top_scoring_intent.intent  == "天气.查询天气":
        return get_weather_ans(entity_data)
    else:
        # entity_module_find = 0
        power = 0.0000000

        with open(ENTITY_FILEPATH, "r", encoding="UTF-8") as entities:
            entity_list = json.load(entities)
            for input_entity in entity_data:
                for item in entity_list["entities_and_answer"]:
                    # 目前entity只有simple和list两种形式才这么写 
                    if intent_data == item["intent"] and \
                        (input_entity.entity in item["entities"] \
                            or input_entity.additional_properties["resolution"]["values"][0] in item["entities"]) :
                        return item["answers"][random.randint(0, len(item["answers"]) - 1)]         
        return None




def get_weather_ans(entities):
    if len(entities) == 0:
        return "暂时没有查询到您想要的天气"
    elif len(entities) >1:
        typenum = 0
        city_name = ""
        for entity in entities:
            if entity.type == "城市":
                typenum+=1
                city_name = entity
        if typenum > 1 or typenum == 0:
            return "每次请只查询一座城市哟~"
        else:
            ans = query_weather(city_name)
            return ans
    else:
        entity = entities[0]
        city_name = entity.entity
        if entity.type != "城市":
            return "请输入城市的名称"
        else:
            ans = query_weather(city_name)
            return ans
            