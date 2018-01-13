# -*- coding:utf-8 -*-


"""

    问答助手~

"""
import time
import win32gui
from argparse import ArgumentParser

from pyhooked import Hook, KeyboardEvent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config import data_directory, hanwan_appcode, vm_name, search_engine, hot_key, ocr_engine, app_id, app_key, \
    app_secret, api_version
from core.ocr import get_text_from_image_hanwang, get_text_from_image_baidu
from core.windows import analyze_current_screen_text


def parse_args():
    parser = ArgumentParser(description="Assistant")
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=5,
        help="default http request timeout"
    )
    return parser.parse_args()


def main():
    print('我来识别这个题目是啥!!!')
    args = parse_args()
    timeout = args.timeout

    start = time.time()
    text_binary = analyze_current_screen_text(
        label=vm_name,
        directory=data_directory
    )
    if ocr_engine == 'baidu':
        print("用百度去OCR识别了!!!\n")
        keyword = get_text_from_image_baidu(image_data=text_binary, app_id=app_id, app_key=app_key,
                                            app_secret=app_secret, api_version=api_version, timeout=5)
    else:
        print("用汉王去OCR识别了!!!\n")
        keyword = get_text_from_image_hanwang(image_data=text_binary, appcode=hanwan_appcode)

    if not keyword:
        print("没识别出来，随机选吧!!!\n")
        print("题目出现的时候按F2，我就自动帮你去搜啦~\n")
        return

    keyword = "".join([e.strip("\r\n") for e in keyword if e])
    keyword.replace('\n', ' ')
    if len(keyword) < 2:
        print("没识别出来，随机选吧!!!\n")
        print("题目出现的时候按F2，我就自动帮你去搜啦~\n")
        return
    print("我用关键词:\" ", keyword, "\"去百度答案啦!")

    elem = browser.find_element_by_id("kw")
    elem.clear()
    elem.send_keys(keyword)
    elem.send_keys(Keys.RETURN)

    print("结果在浏览器里啦~\n")
    print("题目出现的时候按F2，我就自动帮你去搜啦~\n")


def handle_events(args):
    if isinstance(args, KeyboardEvent):
        if args.current_key == hot_key and args.event_type == 'key down':
            main()
        elif args.current_key == 'Q' and args.event_type == 'key down':
            hk.stop()
            print('退出啦~')


if __name__ == "__main__":
    browser = webdriver.Chrome(r'.\tools\chromedriver.exe')
    browser.get(search_engine)
    hld = win32gui.FindWindow(None, vm_name)
    if hld > 0:
        print('用模拟器打开对应应用~~\n题目出现的时候按F2，我就自动帮你去搜啦~\n')
        hk = Hook()
        hk.handler = handle_events
        hk.hook()
    else:
        print('咦，你没打开' + vm_name + '吧!')
