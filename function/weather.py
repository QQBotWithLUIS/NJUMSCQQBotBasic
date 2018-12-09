from collections import OrderedDict

import requests
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as xd
import xmltodict
from lxml import etree, objectify
import os

# 参考的博客与库:"https://blog.csdn.net/x_iya/article/details/52189750"
#               "https://github.com/ruixingchen/ChinaCityList"

query_url = "http://mobile.weather.com.cn/js/citylist.xml"


def query_weather(city_name: str, county_name: str = None)->str:
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
        # 应该raise exception的，不过晚点再做……
        return fail_msg_1

    r = requests.get("http://wthrcdn.etouch.cn/WeatherApi?citykey="+code, timeout=3)
    if r.status_code == requests.codes.ok:
        r.encoding = 'utf-8'
        # tree = ET.fromstring(r.content)  解析xml有至少三种解法你可知道？
        # tree = xd.parseString(r.content)
        tree = xmltodict.parse(r.content)
        # tree = etree.fromstring(r.content)
        # further processing...
        # return etree.tostring(tree, pretty_print=True, encoding="utf-8").decode('utf-8')
        print(etree.tostring(etree.fromstring(r.content), pretty_print=True, encoding="utf-8").decode('utf-8'))
        return pretty(tree['resp'])
    else:
        return fail_msg_2


def get_specific_code(city_name: str, county_name: str)->str:
    # 根据城市名与县名查找具体的地区代码(似乎城市名也没必要用，不过，管他呢)
    # path = os.path.join(os.pardir, 'files', 'ChinaCityList.json') 单独测试这个文件时用这个目录
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


def pretty(root: OrderedDict)->str:

    head = "地区：{0}，当前温度{1}℃，湿度{2}。".format(root['city'], root['wendu'], root['shidu'])
    if 'environment' in root:
        environment = root['environment']
        envir = "pm2.5指数为{0}，空气质量{1}，{2}。".format(environment['pm25'], environment['quality'], environment['suggest'])
        head = head+envir
    forecast = root['forecast']['weather']
    # zhishus = root['zhishus']

    result = [head]
    for i in range(0, 5):
        day_info = "白天{0}，{1}{2}"\
            .format(forecast[i]['day']['type'], forecast[i]['day']['fengxiang'], forecast[i]['day']['fengli'])
        night_info = "夜晚{0}，{1}{2}" \
            .format(forecast[i]['night']['type'], forecast[i]['night']['fengxiang'], forecast[i]['night']['fengli'])
        s = "{0}，最高温{1}，最低温{2}。{3}，{4}。"\
            .format(forecast[i]['date'], forecast[i]['high'][3:], forecast[i]['low'][3:], day_info, night_info)
        result.append(s)
    return "\n".join(result)


if __name__ == "__main__":
    res = query_weather("北京")
    print(res)


