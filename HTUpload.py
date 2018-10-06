
import os
import time
from splinter import Browser
import dbfunc
from config import *
from Public import thread_class

import gfunc
import threading
import download


class Upload(object):
    def __init__(self, platfrom='kandian', data=[], uploaders=[]):
        super().__init__()
        self.data = data
        self.uploaders = uploaders
        self.platfrom = platfrom
        self.driverpath = DRIVERPATH
        self.headless = False  # 展示
        # 线程 
        self.thread = None

    def run(self, platfrom, data=[], uploaders=[]):
        self.data = data
        self.uploaders = uploaders
        self.platfrom = platfrom
        
        if len(self.uploaders) == 0:
            return

        mythread = thread_class.MyThread(self.runStart)
        mythread.start()
        
    def runStart(self):
        print(self.platfrom)

        if self.platfrom == PlatformType.kandian.value:
            # 上传看点
            pass
            for uploader in self.uploaders:
                self.runKandian(uploader)
                

        return
        self.uploaderList = dbfunc.getUploader(PlatformType.qierhao.value)
        for uploader in self.uploaderList:
            self.runItem(uploader)

    def runKandian(self, uploader):
        name = uploader[1]
        pwd = uploader[2]
        loginType = uploader[5]
       
        datas = gfunc.getVideosFromUploader(uploader, self.data)
        print('当前账号 '+name+' 可用视频为: '+ str(len(datas)))

        if len(datas) == 0:
            return

        # TODO 是否需要下载
        datas = download.main(datas)

        with Browser('chrome', executable_path=self.driverpath, headless=self.headless) as browser:
            self.browser = browser
            browser.visit(LoginURL)
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
            for item in datas:
                self.startKandian(item, browser)
            print('看点账号：'+name+' 上传完成 \n *****************')


    def startKandian(self, data, browser):
        # TODO 查看是否已经发过 标题来筛选
        title = data[2]
        print(title)

        url = data[3]
        tags = data[5]
        first_class_name = data[6]
        second_class_name = data[7]
        is_exist_local = data[14]
        local_path = VIDEODIRNAME + '/'+ data[15]
        print(local_path)

        flag = self.pubStart(browser, url, is_exist_local, local_path)
        if flag == 'fail':
            return
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

            if is_exist_local:
                pass
            else:
                dialog = browser.find_by_xpath('//dialog[@class="ui_dialog_container ui_dialog_alert"]')[0]
                dialog.find_by_text('确定')[0].click()

            # TODO 验证 发布成功

            # https://mp.qq.com/page/article_manager
            time.sleep(3)
            arturl = 'https://mp.qq.com/page/article_manager'
            browser.visit(arturl)
            pp = browser.find_by_text(title)
            if len(pp) > 0:
                # 发布成功
                today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

                dic = {'publish_time': today}
                dbfunc.updateVideo(dic, {'id': data[0]})

                print('发布成功')
                time.sleep(3)
            else:
                print('发布失败')

        except Exception as e:
            print(str(e))

    # 确定视频 未成功
    def checkTitle(self, browser):
        title = browser.find_by_id('title-fld')
        if len(title) > 0:
            return True
        else:
            print('checkTitle error')
        return False

    def pubStart(self, browser, row_url, is_exist_local, local_path):
        
        flag = self.pubVideo(browser, row_url, is_exist_local, local_path)
        if flag == 'fail':
            return flag
        print('成功上传视频，检查标题。。')
        check = self.checkTitle(browser)
        if check == False:
            self.pubStart(browser, row_url, is_exist_local, local_path)

    def checkUploadSuccess(self, browser):
        text = '检查视频是否上传成功..'
        print(text, end='\r')
        flag = False
        for i in range(0, 30):
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

    def checkImg(self, browser):
        text = '检查视频封面..'
        print(text, end='\r')
        flag = False
        for i in range(0, 30):
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
    def pubVideo(self, browser, row_url, is_exist_local, local_path):
        try:
            url = PubVideoURL
            browser.visit(url)
            # 本地 腾讯
            if str(is_exist_local) == '1':
                # page = os.getcwd()+'/'+local_path
                
                browser.find_by_xpath('//input[@name="qcloud_upload_file"]')[0].fill(local_path)
                time.sleep(3)
                # 上传中
                suc = self.checkUploadSuccess(browser)
                if suc == False:
                    self.pubVideo(browser, row_url, is_exist_local, local_path)

                # 上传成功
                # 封面
                ss = self.checkImg(browser)
                if ss == False:
                    self.pubVideo(browser, row_url, is_exist_local, local_path)

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
            return 'fail'
            self.pubVideo(browser, row_url, is_exist_local, local_path)


    def runItem(self, uploader):
        name = uploader[1]
        pwd = uploader[2]
        loginType = uploader[5]
        with Browser('chrome', executable_path=self.driverpath, headless=self.headless) as browser:
            browser.visit(LOGINQiERHAOURL)
            # 邮箱登录
            if loginType == LoginType.email.value:
                browser.find_by_class('other-type').first.click()
            
                browser.find_by_class('email-input').first.fill(name)
                browser.find_by_class('password-input').first.fill(pwd)

                browser.find_by_class('btnLogin').first.click()

            if loginType == LoginType.qq.value:
                pass
            time.sleep(100000)


def main():
    upload = Upload()
    upload.run()

if __name__ == '__main__':
    main()
