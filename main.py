# -*- coding:utf-8 -*-


"""

    问答助手~

"""
import time
import win32gui
from pyhooked import Hook, KeyboardEvent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from core.ocr import get_text_from_image_hanwang, get_text_from_image_baidu
from core.windows import analyze_current_screen_text
from xml.dom.minidom import parse

# 默认配置
data_directory = 'screenshots'

vm_name = '夜神模拟器'

app_name = '西瓜视频'

search_engine = 'http://www.baidu.com'

hot_key = 'F2'

# ocr_engine = 'baidu'
ocr_engine = 'baidu'

### baidu orc
app_id = '10685256'
app_key = 'HXaNc3lmpStCNVIQcG8hGB5l'
app_secret = '1x7KQTKEuXECIqqH1D5Fa45sgLV4wBGi'

### 0 表示普通识别
### 1 表示精确识别
api_version = 1

### hanwang orc
hanwan_appcode = '3cc4f16c357e4f329dab5e71c810a871'


# 初始化个人购买的百度或者汉王的账号配置
def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc


def getConfig(tag):
    tagnames = config_element.getElementsByTagName(tag)
    for tag in tagnames:
        return getText(tag.childNodes)

def init():
    global dom1, config_element, data_directory, vm_name, app_name, search_engine, hot_key, ocr_engine, app_id, app_key, app_secret, api_version, hanwan_appcode

    dom1 = parse('config.xml')  # parse an XML file by name

    config_element = dom1.getElementsByTagName("config")[0]

    data_directory = getConfig("data_directory")

    vm_name = getConfig("vm_name")

    search_engine = getConfig("search_engine")

    hot_key = getConfig("hot_key")

    # ocr_engine = 'baidu'或者hanwang
    ocr_engine = getConfig("ocr_engine")

    ### baidu orc
    app_id = getConfig("app_id")
    app_key = getConfig("app_key")
    app_secret = str(getConfig("app_secret"))

    ### 0 表示普通识别
    ### 1 表示精确识别
    api_version = str(getConfig("api_version"))

    ### hanwang orc
    hanwan_appcode = str(getConfig("hanwan_appcode"))
  

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
    try:
        init()
        print("配置文件正常加载!\n")
    except:
        print("配置文件异常，尝试使用默认配置\n")
    try:
        browser = webdriver.Chrome(r'.\tools\chromedriver.exe')
        browser.get(search_engine)
    except:
        print("chrome浏览器打开异常，可能是版本不对\n")
    hld = win32gui.FindWindow(None, vm_name)
    if hld > 0:
        print('使用前记得去config.xml把配置改好哦~~,主要是自己申请换key,不然次数很快就用完啦~~\n\n用模拟器打开对应应用~~\n题目出现的时候按F2，我就自动帮你去搜啦~\n')
        hk = Hook()
        hk.handler = handle_events
        hk.hook()
    else:
        print('咦，你没打开' + vm_name + '吧!请打开' + vm_name + '并重启下start.exe')

