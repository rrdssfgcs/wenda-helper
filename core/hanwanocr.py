# -*- coding: utf-8 -*-

"""

    hanwan ocr service from aliyun

"""
import json

import base64
import requests


def get_text_from_image(image_data, appcode, timeout=3):
    """
    Get text from image use HanWang OCR

    :param image_data:
    :param appcode:
    :param timeout:
    :return:
    """
    data = "{\"uid\":\"118.12.0.12\",\"lang\":\"chns\",\"color\":\"color\",\"image\":\"" +bytes.decode(base64.b64encode(image_data)) + "\"}"
    headers = {
        "Authorization": "APPCODE {0}".format(appcode),
        "Content-Type": "application/octet-stream"
    }
    base_url = "http://text.aliapi.hanvon.com/rt/ws/v1/ocr/text/recg"
    resp = requests.post(
        base_url,
        data=str.encode(data),
        headers=headers,
        timeout=timeout
    )
    if not resp.ok:
        print("汉王OCR识别出错，是不是免费使用次数用完了啊~")
        return ""
    rjson = resp.json()
    if rjson["code"] != "0":
        print(rjson["textResult"])
        return ""
    return rjson["textResult"]
