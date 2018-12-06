import requests
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as xd
import xmltodict

# 参考的博客与库:"https://blog.csdn.net/x_iya/article/details/52189750"
#               "https://github.com/ruixingchen/ChinaCityList"

city_key = "http://mobile.weather.com.cn/js/citylist.xml"


def query_weather(city_name: str, county_name: str = None)->dict:
    if not county_name:
        county_name = city_name
    code = get_county_code(city_name, county_name)

    if not code:
        # 应该raise exception的，不过晚点再做……
        return None

    r = requests.get("http://wthrcdn.etouch.cn/WeatherApi?citykey="+code, timeout=3)
    if r.status_code == requests.codes.ok:
        # tree = ET.fromstring(r.content)  解析xml有至少三种解法你可知道？
        # tree = xd.parseString(r.content)
        tree = xmltodict.parse(r.content)
        # further processing...
        return tree


def get_county_code(city_name:str, county_name:str)->str:
    with open("../files/ChinaCityList.json", 'r', encoding='UTF-8') as f:
        province_list = json.load(f, encoding="UTF-8")

    code = ""
    # name_en = ""
    for province in province_list:
        for city in province["city"]:
            if city["name"] == city_name:
                for county in city["county"]:
                    if county["name"] == county_name:
                        code = county["code"][2:]
                        # name_en = county["name_en"]
                        return code
    return code


if __name__ == "__main__" :
    res = query_weather("北京")
    print(res if res else "None")
