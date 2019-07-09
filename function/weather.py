import json
import os
from collections import OrderedDict

import requests
import xmltodict

# 参考的博客与库:"https://blog.csdn.net/x_iya/article/details/52189750"
#               "https://github.com/ruixingchen/ChinaCityList"

query_url = "http://mobile.weather.com.cn/js/citylist.xml"


def query_weather(city_name: str, county_name: str = None) -> str:
    """
    根据传入的城市名与县名查询当地天气。县名可选。
    因此要求在调用函数时分辨好城市名和县名。
    返回值为格式化好的字符串，可直接输出。(格式待定)
    """
    fail_msg_1 = '抱歉，好像查不到呢，请检查一下输入格式:"天气 <城市名> <县城名>(可选)"。'
    fail_msg_2 = '查询失败，请稍后再试。'

    if not county_name:
        county_name = city_name
    code = get_specific_code(city_name, county_name)

    if not code:
        # 查询不到相应的城市代码，返回失败信息
        return fail_msg_1

    r = requests.get("http://wthrcdn.etouch.cn/WeatherApi?citykey=" + code, timeout=3)
    if r.status_code == requests.codes.ok:
        r.encoding = 'utf-8'
        # tree = ET.fromstring(r.content)  解析xml有至少三种解法你可知道？
        # tree = xd.parseString(r.content)
        tree = xmltodict.parse(r.content)
        # tree = etree.fromstring(r.content)
        # return etree.tostring(tree, pretty_print=True, encoding="utf-8").decode('utf-8')
        # print(etree.tostring(etree.fromstring(r.content), pretty_print=True, encoding="utf-8").decode('utf-8'))
        return pretty(tree['resp'])
    else:
        # return fail_msg_2
        raise Exception(fail_msg_2)


def get_specific_code(city_name: str, county_name: str) -> str:
    # 根据城市名与县名查找具体的地区代码(似乎城市名也没必要用，不过，管他呢)
    # path = os.path.join(os.pardir, 'files', 'ChinaCityList.json') # 单独测试这个文件时用这个目录
    path = os.path.join(os.getcwd(), 'files', 'ChinaCityList.json')

    # with open("../files/ChinaCityList.json", 'r', encoding='UTF-8') as f:
    with open(path, 'r', encoding='UTF-8') as f:
        province_list = json.load(f, encoding="UTF-8")

    code = ""
    # name_en = "" 城市拼音，不过似乎暂时用不到
    for province in province_list:
        for city in province["city"]:
            if city["name"] == city_name:
                for county in city["county"]:
                    if county["name"] == county_name:
                        code = county["code"][2:]
                        # name_en = county["name_en"]
                        return code
    return code


def pretty(root: OrderedDict) -> str:
    head = "下面由小澄为您播报{0}的天气情况，此时温度为{1}℃。\n".format(root['city'], root['wendu'])
    if 'environment' in root:
        environment = root['environment']
        envir = '空气指数(AQI)是{0}，空气质量为{1}，风力等级为{2}。小澄的建议是{3}。\n'.format(environment['aqi'], environment['quality'],
                                                                      root['fengli'], environment['suggest'])
        head = head.replace('\n', envir)

    forecast = root['forecast']['weather']
    zhishus = root['zhishus']['zhishu']
    head = head + "我们来看看今天总体的天气情况，"

    today = root['yesterday']
    head = head + '最{0}，最{1}。白天{2}，夜晚{3}。' \
        .format(today['high_1'], today['low_1'], today['day_1']['type_1'], today['night_1']['type_1'])
    head = head + "穿衣建议为{0}不知道同学你的衣服晒好了么？今天的晾晒建议是{1}；{2}" \
        .format(zhishus[2]['detail'], zhishus[4]['value'], zhishus[4]['detail'])
    head = head + "怕被浇成落汤鸡？小澄为您遮风挡雨。今天是否需要带伞呢？{0}。建议是：{1}\n" \
        .format(zhishus[10]['value'], zhishus[10]['detail'])

    tomorrow = forecast[0]
    head = head + "下面由小澄播报明天的天气状况，明天即{0}，最{1}，最{2}，白天{3}，夜晚{4}。不知道小澄的天气播报是否让您满意呢？(#^.^#)" \
        .format(tomorrow['date'], tomorrow['high'], tomorrow['low'], tomorrow['day']['type'], tomorrow['night']['type'])
    return head


if __name__ == "__main__":
    res = query_weather("南京")
    print(res)
