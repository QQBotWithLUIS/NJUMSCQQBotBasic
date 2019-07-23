# -*- coding: utf-8 -*-

import http.client
import json
import random
from config import QNA_FILEPATH



question = {
    'question': '你是谁呀',
    'top': 1
}


def pretty_print(content):
    # Note: We convert content to and from an object so we can pretty-print it.
    return json.dumps(json.loads(content), indent=4)

def get_answers_from_file(content):
    with open(QNA_FILEPATH, "r", encoding="UTF-8") as qna:
        qna_list = json.load(qna)
        for item in qna_list["qna"]:
            if item["intent"] == content:
                return item["answers"][random.randint(0, len(item["answers"]) - 1)]
        return None

# Convert the request to a string.
# content = json.dumps(question)
# result = get_answers_from_file("你好")
# print(result)
# print(pretty_print(result).encode('utf-8').decode('unicode_escape'))
