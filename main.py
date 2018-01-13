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

from core.ocr import get_text_from_image_hanwang, get_text_from_image_baidu
from core.windows import analyze_current_screen_text
import configparser

conf = configparser.ConfigParser()
conf.read("config.ini")

data_directory = conf.get('config',"data_directory")

vm_name = conf.get('config',"vm_name")

app_name = conf.get('config',"app_name")

search_engine = conf.get('config',"search_engine")

hot_key = conf.get('config',"hot_key")

# ocr_engine = 'baidu'
ocr_engine = conf.get('config',"ocr_engine")

### baidu orc
app_id = conf.get('config',"app_id")
app_key = conf.get('config',"app_key")
app_secret = conf.get('config',"app_secret")

### 0 表示普通识别
### 1 表示精确识别
api_version = conf.get('config',"api_version")

### hanwang orc
hanwan_appcode = conf.get('config',"hanwan_appcode")

def pre_process_question(keyword):
    """
    strip charactor and strip ?
    :param question:
    :return:
    """
    for char, repl in [("“", ""), ("”", ""), (" ", ""), ("\t", "")]:
        keyword = keyword.replace(char, repl)

    keyword = keyword.split(r".")[-1]
    tag = keyword.find("?")
    if tag != -1:
        keyword = keyword[:tag]
    tag = keyword.find("？")
    if tag != -1:
        keyword = keyword[:tag]
    keywords = keyword.split(" ")
    keyword = "".join([e.strip("\r\n") for e in keywords if e])
    return keyword

def main():
    print('我来识别这个题目是啥!!!')
    text_binary = analyze_current_screen_text(
        label=vm_name,
        directory=data_directory
    )
    if ocr_engine == 'baidu':
        print("用百度去OCR识别了!!!\n")
        keyword = get_text_from_image_baidu(image_data=text_binary, app_id=app_id, app_key=app_key,
                                            app_secret=app_secret, api_version=api_version, timeout=5)
        keyword = "".join([e.strip("\r\n") for e in keyword if e])
    else:
        print("用汉王去OCR识别了!!!\n")
        keyword = get_text_from_image_hanwang(image_data=text_binary, appcode=hanwan_appcode)

    if not keyword:
        print("没识别出来，随机选吧!!!\n")
        print("题目出现的时候按F2，我就自动帮你去搜啦~\n")
        return

    keyword = pre_process_question(keyword)

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
        print('使用前记得去config.ini把配置改好哦~~,主要是自己申请换key,不然次数很快就用完啦~~\n\n用模拟器打开对应应用~~\n题目出现的时候按F2，我就自动帮你去搜啦~\n')
        hk = Hook()
        hk.handler = handle_events
        hk.hook()
    else:
        print('咦，你没打开' + vm_name + '吧!请打开' + vm_name + '并重启下start.bat')
