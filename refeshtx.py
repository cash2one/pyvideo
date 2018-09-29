import os
import time
import threading
from selenium import webdriver

from splinter import Browser
import requests
import json
import random

def run():

    driverpath = './Source/mac/chromedriver'
    headless = False

    # proxyIP = proxy[0]
    # proxyPort = proxy[1]
    # print(proxyIP)
    # proxy_type = 'http'
    # bb = str(proxyIP)+':'+str(proxyPort)
    # proxy_server = '{0}://{1}'.format(proxy_type, bb)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--proxy-server={}'.format(proxy_server))

    # chrome_options.add_experimental_option("mobileEmulation",
    #                             mobile_emulation)

    with Browser('chrome', executable_path=driverpath, headless=headless) as browser:
        url = 'https://v.qq.com/x/page/c0712jjvn6k.html'
        browser.visit(url)
        time.sleep(20)
        print('complete')
        exit()


def getProxy():
    res = requests.get('http://0.0.0.0:8000/')
    # print(res.text)
    text = res.text

    jsondata = json.loads(text)

    ii = random.randrange(0, len(jsondata))

    item = jsondata[ii]
    ip = item[0]
    port = item[1]

    # proxies = {
    #     'http': 'http://%s:%s' % (ip, port),
    #     'https': 'http://%s:%s' % (ip, port)
    # }
    return item
    # return proxies


while 1:

    # proxy = getProxy()
    # print(proxy)
    t1 = threading.Thread(target=run)

    t2 = threading.Thread(target=run)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    num = 3
    tts = []
    for i in range(0, num):
        t= threading.Thread(target=run)
        t.setDaemon(True)
        t.start()



# class ProxyBrowser(object):
#     def __new__(cls, driver='chrome', proxy=None, proxy_type='http', **kwargs):
#         """
#         >>> browser = ProxyBrowser(driver='chrome', proxy='61.132.74.89:1080', proxy_type='socks5')
#         >>> browser.visit('http://wtfismyip.com')
#         """
#         browser = partial(Browser, driver)

#         proxy_kwargs = cls.get_proxy_kwargs(driver, proxy, proxy_type)
#         kwargs.update(proxy_kwargs)

#         return browser(**kwargs)

#     @classmethod
#     def get_proxy_kwargs(cls, driver, proxy, proxy_type):
#         """
#         :param driver: chrome | phantomjs
#         :param proxy: {address}:{port}
#         :param proxy_type: http | socks5
#         """
#         proxy_server = '{0}://{1}'.format(proxy_type, proxy)
#         print proxy_server
#         if proxy:
#             if driver == 'phantomjs':
#                 return {'service_args': ['--proxy={}'.format(proxy), '--proxy-type={}'.format(proxy_type)]}
#             elif driver == 'chrome':
#                 chrome_options = webdriver.ChromeOptions()
#                 chrome_options.add_argument('--proxy-server={}'.format(proxy_server))
#                 return {'options': chrome_options}
#             else:
#                 raise DriverNotFoundError('Not supported driver: {}'.format(driver))
#         else:
#             return {}
        
