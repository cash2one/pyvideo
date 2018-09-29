import time
import threading
from splinter import Browser
from config import *



def run():
    driverpath = DRIVERPATH
    headless = False
    with Browser('chrome', executable_path=driverpath, headless=headless) as browser:
        url = 'https://v.qq.com/x/page/p0713hhaxiy.html'
        browser.visit(url)
        print('【hello】'+browser.url)

        exit()

num = 0

while 1:
    t1 = threading.Thread(target=run, args=())
    t2 = threading.Thread(target=run, args=())
    t3 = threading.Thread(target=run, args=())
    t4 = threading.Thread(target=run, args=())
    t5 = threading.Thread(target=run, args=())
    t6 = threading.Thread(target=run, args=())
    # t7 = threading.Thread(target=run, args=())
    # t8 = threading.Thread(target=run, args=())
    # t9 = threading.Thread(target=run, args=())
    # t10 = threading.Thread(target=run, args=())

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    # t7.start()
    # t8.start()
    # t9.start()
    # t10.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    # t7.join()
    # t8.join()
    # t9.join()
    # t10.join()

    num+=1
    print(num)
