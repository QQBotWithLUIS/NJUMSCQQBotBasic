import re

from nonebot.default_config import *

HOST = '127.0.0.1'
PORT = 8080

SUPERUSERS = {1320163325, 1206985125, 710282573}
COMMAND_START.add('')

psychological_committee = {'2018-1': '1111', '2018-2': '1111'}
default_committee = '1111'
clazz_student_mapper = {'2018-1': '(正则表达式)'}
academic_wall = '1111'


def find_corresponding_psychological_committee(student_id: str):
    for k, v in clazz_student_mapper:
        if re.match(v, student_id):
            return psychological_committee[k]
    return default_committee
