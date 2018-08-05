# -*- coding:utf-8 -*-

import os
import time
from splinter import Browser
import dbfunc
from config import *

def login(name=account, pwd=pwdDic[account]):

    print('name: '+ name)
    headless = True

    datas = dbfunc.fetchVideo(name)
    if len(datas) == 0:
        return False

    with Browser('chrome', headless=headless) as browser:
        # Visit URL
        url = LoginURL
        browser.visit(url)

        with browser.get_iframe("login_if") as iframe:
            print('正在登录qq: '+name+ '   请稍后...')
            iframe.find_by_id('switcher_plogin').first.click()

            iframe.find_by_id('u').first.fill(name)
            iframe.find_by_id('p').first.fill(pwd)

            iframe.find_by_id("login_button").first.click()

        time.sleep(5)
        print('登录成功')
        for i in range(0, len(datas)):
            # data = datas[len(datas)-i-1]
            data = datas[i]
        # for data in datas:
            start(data, browser)

# 确定视频 未成功
def checkTitle(browser):
    title = browser.find_by_id('title-fld')
    if len(title) > 0:
        return True
    else:
        print('checkTitle error')
        return False

# 发布视频
def pubVideo(browser, row_url):
    try:
        url = PubVideoURL
        browser.visit(url)
        browser.find_by_id('select_from_video_url').first.click()
        time.sleep(1)
        # 链接
        browser.find_by_id('full_video_url-picker').first.fill(row_url)
        time.sleep(3)
        dialog = browser.find_by_id('mask_video-picker-dialog-url-4-vip')

        # 确定 视频
        sure = dialog.find_by_css('div>div>a.act_ok')[0]
        sure.click()
        time.sleep(2)

    except Exception as e:
        print('pub video fail:'+ str(e))
        time.sleep(0.5)
        pubVideo(browser, row_url)

def pubStart(browser, row_url):

    pubVideo(browser, row_url)
    check = checkTitle(browser)
    if check:
        pass
    else:
        pubStart(browser, row_url)

def start(data, browser):
    
    title = data[2]
    print(title)

    url = data[3]
    tags = data[5]
    first_class_name = data[6]
    second_class_name = data[7]

    pubStart(browser, url)
 
    # title
    titleinput = browser.find_by_id('title-fld').first
    titleinput.clear()
    titleinput.fill(title)

    # 分类
    browser.find_by_id('normal_first_class')[0].find_by_css('a')[0].click()
    browser.find_by_xpath('//input[@type="search"and@placeholder="搜索"]').first.fill(first_class_name)
    browser.find_by_xpath('//li[@value="%s"]' % (first_class_name)).first.click()

    browser.find_by_id('normal_second_class')[0].find_by_css('a').first.click()
    browser.find_by_xpath('//input[@type="search"and@placeholder="搜索"]')[1].fill(second_class_name)
    if first_class_name == second_class_name:
        browser.find_by_xpath('//li[@value="%s"]' % (second_class_name))[1].click()
    else:
        browser.find_by_xpath('//li[@value="%s"]' % (second_class_name))[0].click()

    # 标签
    browser.find_by_id('tag-input').first.fill(tags)

    # 简介
    if len(title) <= 10:
        title = title + '......'
    browser.find_by_id('video-summary-textarea').first.fill(title)

    # 发布视频
    browser.find_by_id('video_publish_commit').first.click()
    
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    # TODO 验证 发布成功
    dic = {'publish_time': today}
    dbfunc.updateVideo(data[0], dic, 'videos')
    time.sleep(3)

def main():
    login()


if __name__ == '__main__':
    main()


