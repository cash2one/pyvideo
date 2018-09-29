
import os
import time
from splinter import Browser
import dbfunc
from config import *
from HTThread import HTThread


class Upload(object):
    def __init__(self, platfrom, data):
        super().__init__()
        self.data = data
        self.platfrom = platfrom
        self.driverpath = DRIVERPATH
        self.headless = False  # 展示

    def run(self):
        self.thread = HTThread(self.runStart)
        self.thread.setDaemon(True)
        self.thread.start()
        

    def runStart(self):

        if self.platfrom == PlatformType.kandian.value:
            # 上传看点
            pass

        return
        self.accountList = dbfunc.getUploader(PlatformType.qierhao.value)
        for account in self.accountList:
            self.runItem(account)

    def runItem(self, account):
        name = account[1]
        pwd = account[2]
        loginType = account[5]
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
