
import requests
import json
import re
import dbfunc
import time
import gfunc
import math
from config import *

def getJsonFromUin(uin, pagenum):
    num = 30 # 最多30 一般24
    url = 'http://c.v.qq.com/vchannelinfo?otype=json&uin='+ uin +'&qm=1&pagenum='+ str(pagenum) +'&num='+str(num)+'&sorttype=0&orderflag=0&callback=jQuery19104105733024427589_1531375140863&low_login=1&_=1531375140876'
    print(url)
    req = requests.get(url)
    data = re.findall('\(({.*?})\)', req.text)[0]
    jsondata = json.loads(data)
    return jsondata

def addVideo(video, aid):

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

def addVideos(videolst, aid):
    try:
        for video in videolst:
            addVideo(video, aid)
    except Exception as e:
        pass
    
def updateAnchorVNum(vtotal, aid):
    dbfunc.updateAnchor({'vnum': vtotal}, {'aid': aid})

def index(anchor, page=None):
    # url = 'http://v.qq.com/vplus/3fcca62af8c4b211b87401b4530cff9a/videos '
    aid = anchor[0]
    uin = anchor[2]
    pagenum = anchor[5]
    
    jsondata = getJsonFromUin(uin, pagenum)
    print(jsondata['videolst'])
    addVideos(jsondata['videolst'], aid)
    vtotal = jsondata['vtotal']
    updateAnchorVNum(vtotal, aid)

    if page != None:

        # 向上取整
        loopnum = math.ceil(int(vtotal)/30)
        
        for i in range(1, loopnum):
            pagenum += 1
            jsondata = getJsonFromUin(uin, pagenum)
            addVideos(jsondata['videolst'], aid)

# anchors anchor数组 page=all
def main(anchors=None, page=None):
    if anchors is None:
        anchors = dbfunc.fetchAllAnchor()
    for anchor in anchors:
        index(anchor, page)

# if __name__ == '__main__':
#     main()




# uids = [

#     '0c6fcdeff1c6fd7788923deaee77407e',     # 综艺明星 明星风云

#     '7464eec19eb5b6e885fc9e995a19b595',     # 电影 寻找感动瞬间   猴子看影视
#     '0524cbe3cafc8c0d3d9d36e561cdbe5c',     # 林正英  圆圆的酒窝 鬼片

#     '3fcca62af8c4b211b87401b4530cff9a',     # 动漫 皮皮马动漫 动漫
#     'd45c5239b8048e6bb188a15948ea99e1',     # 鑫动漫迷  狐妖小红娘
#     '33ab11c1024d6fadbac790ee1028a77e',     # 猪小屁

#     '8fd0b60d936e2de673a28f240e970869',     # 绝地吃鸡亡者 
#     'ac5cb071aaf678ff7ca329be3aecc704',     #  躺着吃鸡模式  绝地求生
#     'fda0e81923207a2f7fdb7a4974c77e1b',     # 游戏老家 cf

#     'c30a67f97703cbac18616f9785799de9'      # 萌萌图图  游戏动漫
# ]

# for uid in uids:
#     pagenum = 1
#     index(uid, pagenum)