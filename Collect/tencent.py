from config import *
from Public import thread_class
import dbfunc
import json
import gfunc
import math
import requests
import re
import time

class Tencent(object):
    def __init__(self, anchors=[], type = CollectType.alllatest):
        super().__init__()

        self.anchors = anchors
        self.type = type
        if type == CollectType.alllatest:
            # 所有账户
            self.anchors = dbfunc.getAnchor(PlatformType.tencent.value)
            print(self.anchors)
            print(len(self.anchors))
        # self.start()

        
    def start(self):
        mythread = thread_class.MyThread(self.runback)
        mythread.start()

    
    def runback(self, args):

        for anchor in self.anchors:
            aid = anchor[0]
            uin = anchor[2]
            page = anchor[5]
            jsondata = self.getJsonFromUin(uin, page)
            vtotal = jsondata['vtotal']
            self.updateAnchorVNum(vtotal, aid)
            videolst = jsondata['videolst']
            self.addVideos(videolst, aid)

            # 另外的了 所有页面
            if self.type == CollectType.allpage:
                loopnum = math.ceil(int(vtotal)/30)
                for i in range(1, loopnum):
                    page += 1
                    jsondata = self.getJsonFromUin(uin, page)
                    self.addVideos(jsondata['videolst'], aid)
        print('采集完成')


    def getJsonFromUin(self, uin, pagenum):
        num = 30 # 最多30 一般24
        url = 'http://c.v.qq.com/vchannelinfo?otype=json&uin='+ uin +'&qm=1&pagenum='+ str(pagenum) +'&num='+str(num)+'&sorttype=0&orderflag=0&callback=jQuery19104105733024427589_1531375140863&low_login=1&_=1531375140876'
        print(url)
        req = requests.get(url)
        data = re.findall('\(({.*?})\)', req.text)[0]
        jsondata = json.loads(data)
        return jsondata

    def updateAnchorVNum(self, vtotal, aid):
        dbfunc.updateAnchor({'vnum': vtotal}, {'aid': aid})

    def addVideos(self, videolst, aid):
        print(len(videolst))
        try:
            for video in videolst:
                self.addVideo(video, aid)
        except Exception as e:
            pass

    def addVideo(self, video, aid):
        title = video['title']
        print(title)
        # tags 分词
        seg_list = gfunc.participle(title)
        tags = ' '.join(seg_list)
        # 分类
        classly = gfunc.classFromTitle(title)
        qq = classly[2]
        dic = {
            'qq': qq,
            'title': title,
            'url': video['url'],
            'alias': '',
            'tags': tags,
            'first_class': classly[0],
            'second_class': classly[1],
            'platform_create_time': video['uploadtime'],
            'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
            'aid': aid,
            'vid': video['vid'],
            'pic': video['pic'],
            'is_exist_local': 0,
            'local_path': '',
            'fromUserId': gfunc.getUserId(),
            'platform': PlatformType.tencent.value
        }
        # 
        dbfunc.insertVideo(dic)



