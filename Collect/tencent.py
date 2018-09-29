import requests
import dbfunc
import gfunc
import re
import json
import math
import time

'''
todo 分布式采集
定时采集
自动采集
'''
class Tencent(object):
    def __init__(self, anchors=None, page=None):
        super().__init__()       

        if anchors is None:
            self.anchors = dbfunc.fetchAllAnchor()
        else:
            self.anchors = anchors
        self.page = page

        for anchor in self.anchors:
            self.index(anchor, self.page)

    def index(self, anchor, page=None):
        # url = 'http://v.qq.com/vplus/3fcca62af8c4b211b87401b4530cff9a/videos '
        aid = anchor[0]
        uin = anchor[2]
        pagenum = anchor[5]
        jsondata = self.getJsonFromUin(uin, pagenum)
        self.addVideos(jsondata['videolst'], aid)

        if page != None:

            vtotal = jsondata['vtotal']
            # 向上取整
            loopnum = math.ceil(int(vtotal)/30)
            
            for i in range(1, loopnum):
                print(uin)

                pagenum += 1
                jsondata = self.getJsonFromUin(uin, pagenum)
                self.addVideos(jsondata['videolst'], aid)

    def getJsonFromUin(self, uin, pagenum):
        num = 30 # 最多30 一般24
        url = 'http://c.v.qq.com/vchannelinfo?otype=json&uin='+ uin +'&qm=1&pagenum='+ str(pagenum) +'&num='+str(num)+'&sorttype=0&orderflag=0&callback=jQuery19104105733024427589_1531375140863&low_login=1&_=1531375140876'
        print(url)
        req = requests.get(url)
        data = re.findall('\(({.*?})\)', req.text)[0]
        jsondata = json.loads(data)
        return jsondata

    def addVideo(self, video, aid):
            
        title = video['title']
        print(title)
        # tags 分词
        seg_list = gfunc.participle(title)
        tags = ' '.join(seg_list)
        # 分类
        classly = gfunc.classFromTags(tags)
        qq = classly[2]
        dic = {
            'qq': qq,
            'title': title,
            'url': video['url'],
            'alias': '',
            'tags': tags,
            'first_class': classly[0],
            'second_class': classly[1],
            'qq_create_time': video['uploadtime'],
            'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
            'aid': aid,
            'vid': video['vid'],
            'pic': video['pic'],
            'is_exist_local': 0,
            'local_path': '',
            'fromUserId': gfunc.getLoginNameForLocal()[2]
        }

        dbfunc.insertVideo(dic)

    def addVideos(self, videolst, aid):
        print(len(videolst))
        try:
            for video in videolst:
                self.addVideo(video, aid)
        except Exception as e:
            pass

    

