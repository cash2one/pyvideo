# -*- coding:utf-8 -*-

import os
import time
from splinter import Browser
import dbfunc
from config import *
from PyQt5.QtWidgets import *
import gfunc    
from io import BytesIO
from PIL import Image


def login(name=account, pwd=pwdDic[account], videos=None):

    print('准备上传看点用户：'+ name)
    # QApplication.processEvents()

    headless = False

    todayPub = dbfunc.fetchTodayPublishedVideo(name)

    todayPubNum = len(todayPub)
    allnum = 10

    makePubNum = allnum - todayPubNum
    if videos is None:
        datas = dbfunc.fetchVideo(name, 'today', makePubNum)
    else:
        if len(videos) <= makePubNum:
            datas = videos
        else:
            datas = videos[0:makePubNum]

    # TODO
    if len(datas) < 10:
        pass
    print('当前账号 '+name+' 可用视频为: '+ str(len(datas)))

    if len(datas) == 0:
        return False
    # QApplication.processEvents()
    driverpath = ''
    if PLATFORM == 'MAC':
        driverpath = './Source/mac/chromedriver'
    elif PLATFORM == 'WIN':
        driverpath = './Source/win/chromedriver.exe'

    # start
    # 检查是否下载了
     
    print('检查本地是否有一个视频')
    for item in datas:
        is_exist_local = item[14]
        local_path = item[15]
        url = item[3]
        idd = item[0]
        print(str(idd)+' :  '+local_path)
        # TODO
        if gfunc.isfile(local_path) == False:
            # 1. 下载 todo 视频不存在怎么处理
            local_path = gfunc.downVideo(url)
            print(local_path)
            if (local_path):
            # 2. 存入数据库
                print('存入数据库')
                is_exist_local = '1'
                dic = {
                    'is_exist_local': is_exist_local,
                    'local_path': local_path
                }
                dbfunc.updateVideoFromData(idd, dic, 'videos')
            
        # 2.去水印
        if local_path:
            outfile = gfunc.watermarks(local_path)

        print('存入去水印的视频')
        if outfile:
            dic = { 'local_path': outfile }
            dbfunc.updateVideoFromData(item[0], dic, 'videos')
        time.sleep(1)
    print('下载完成去水印完成')
    
    # end

    dataArr = []
    for item in datas:
        res = dbfunc.fetchVideoFormId(item[0])
        dataArr.append(res[0])
    # dataArr = datas

    with Browser('chrome', executable_path=driverpath, headless=headless) as browser:
        # Visit URL
        url = LoginURL
        browser.visit(url)
        
        with browser.get_iframe("login_if") as iframe:
            print('正在登录qq: '+name+ '   请稍后...')
            iframe.find_by_id('switcher_plogin').first.click()

            iframe.find_by_id('u').first.fill(name)
            iframe.find_by_id('p').first.fill(pwd)

            iframe.find_by_id("login_button").first.click()

            time.sleep(1)
        
            # 验证是否有验证码
            vcode = iframe.find_by_id('newVcodeIframe')
            if len(vcode) > 0:
                # 图形验证码
                print('需验证图形码')
                time.sleep(20)
            else:
                time.sleep(4)

        print('看点账号：'+ name +' 登录成功')
        for i in range(0, len(dataArr)):
            # data = datas[len(datas)-i-1]
            data = dataArr[i]
        # for data in datas:
            start(data, browser)
            if i == len(dataArr)-1:
                print('看点账号：'+name+' 上传完成 \n *****************')

# 确定视频 未成功
def checkTitle(browser):
    title = browser.find_by_id('title-fld')
    if len(title) > 0:
        return True
    else:
        print('checkTitle error')
    return False

#判断元素是否存在
def isElementExist(browser, xpath):
    try:
        xx = browser.find_elements_by_xpath(xpath)
        if len(xx) > 0:
            return True
        else:
            return False
    except Exception as e:
        return False
                
# isexist = isElementExist(browser, '//div[@class="video-material-showcase"and@style="display: block;"]')
def checkUploadSuccess(browser):
    text = '检查视频是否上传成功..'
    print(text, end='\r')
    flag = False
    for i in range(0, 200):
        text=text+'.'
        print(text, end='\r')

        text_scc = browser.find_by_text('视频上传成功')
        if len(text_scc) > 0:
            flag = True
            break
        time.sleep(1)
    print('')
    print('视频上传完成')
    return flag

def checkImg(browser):
    text = '检查视频封面..'
    print(text, end='\r')
    flag = False
    for i in range(0, 200):
        try:
            img = browser.find_by_id('video_content_cover_bg_img')[0]
            src = img['src']
            text=text+'.'
            print(text, end='\r')

            if len(src) > 20:
                flag = True
                break
        except Exception as e:
            pass

        time.sleep(1)

    print('')
    print('视频封面完成')

    return flag

# 发布视频
def pubVideo(browser, row_url, is_exist_local, local_path):
    try:
        url = PubVideoURL
        browser.visit(url)
        # 本地 腾讯
        if str(is_exist_local) == '1':
            page = os.getcwd()+'/'+local_path
            browser.find_by_xpath('//input[@name="qcloud_upload_file"]')[0].fill(page)
            time.sleep(3)
            # 上传中
            suc = checkUploadSuccess(browser)
            if suc == False:
                return
            # 上传成功
            # 封面
            ss = checkImg(browser)
            if ss == False:
                return False
        else:
        # 腾讯在线
            browser.find_by_id('select_from_video_url').first.click()
            time.sleep(1)
            # 链接
            browser.find_by_id('full_video_url-picker').first.fill(row_url)
            time.sleep(4)
            dialog = browser.find_by_id('mask_video-picker-dialog-url-4-vip')

            # 确定 视频
            sure = dialog.find_by_css('div>div>a.act_ok')[0]
            sure.click()
            time.sleep(4)

    except Exception as e:
        print('pub video fail:'+ str(e))
        time.sleep(0.5)
        pubVideo(browser, row_url, is_exist_local, local_path)

def pubStart(browser, row_url, is_exist_local, local_path):

    pubVideo(browser, row_url, is_exist_local, local_path)
    print('成功上传视频，检查标题。。')
    check = checkTitle(browser)
    if check == False:
        pubStart(browser, row_url, is_exist_local, local_path)

def start(data, browser):
    
    title = data[2]
    print(title)

    url = data[3]
    tags = data[5]
    first_class_name = data[6]
    second_class_name = data[7]
    is_exist_local = data[14]
    local_path = data[15]
    print(is_exist_local)
    # if str(is_exist_local) == '0':
    #     return

    pubStart(browser, url, is_exist_local, local_path)
 
    # TODO title clear err 
    try:
        titleinput = browser.find_by_id('title-fld').first
        titleinput.clear()
        titleinput.fill(title)
    except Exception as e:
        print('title input err: '+ str(e))
        time.sleep(5)
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
    try:
        browser.find_by_id('video_publish_commit').first.click()
        today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        # TODO 验证 发布成功
        dic = {'publish_time': today}
        dbfunc.updateVideo(data[0], dic, 'videos')
        print('发布成功')
        time.sleep(3)
    except Exception as e:
        print(str(e))
    

def main():
    login()


if __name__ == '__main__':
    main()




