
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
#     'f401289eef888c247afa2888d66bd01c',     # 其实你很幽默 国外 幽默段子 憨豆先生
#     '9d0387de8f60ab27bafef9e42a504593',     # 搞笑 有色有声姐

#     '0c4932b8a08dd5b42a4797b4c8060361',     # 电视剧 畅涵影视
#     '0c6fcdeff1c6fd7788923deaee77407e',     # 综艺明星 明星风云

#     '48655f5bb2709cfef893016a79843b0d',     # 影视 风云英雄 
#     '35f2a7e76ee6cf68b1f4158faf187d3f',     # 影视 余独不觉 
#     '96486663bb39295ba0b6c87bb849e22c',     # 影视新天地
#     '7464eec19eb5b6e885fc9e995a19b595',     # 电影 寻找感动瞬间   猴子看影视
#     '0524cbe3cafc8c0d3d9d36e561cdbe5c',     # 林正英  圆圆的酒窝 鬼片

#     '3fcca62af8c4b211b87401b4530cff9a',     # 动漫 分享驿站 动漫
#     '3189c372f7673e44573f990813172070',     # 动漫 火影
#     '1661bab3a8dbd85ba0b6c87bb849e22c',     # 动漫 御宅小夜动漫社
#     '3189c372f7673e44573f990813172070',     # 动漫  趣谈史  火影
#     'd45c5239b8048e6bb188a15948ea99e1',     # 鑫动漫迷  狐妖小红娘
#     'ee37cd3c7d125b709fcf6a40cd1fae90',     # 漫妙次元 动漫
#     '33ab11c1024d6fadbac790ee1028a77e',     # 猪小屁

#     '3a648b8b537c74308adc82edb0c933ed',     # lol 每日撸报  徐老师来巡山
#     'b125da5d9a0d60877126a454e1060f71',     # 王者荣耀 朋弟说游
#     '06c7b21843daa5fdea1d320834d87bff',     # 星爷说游戏  刺激战场 王者荣耀
#     '77847f85dd4bf9073c127e842543015d',     # 小樱桃说游戏  绝地求生 王者荣耀
#     '8fd0b60d936e2de673a28f240e970869',     # 绝地吃鸡亡者 绝地求生
#     '312e417342de792818616f9785799de9',     # 纯儿看动漫   王者荣耀动漫
#     'ac5cb071aaf678ff7ca329be3aecc704',     #  躺着吃鸡模式  绝地求生
#     '2c947ccd552aa084a0b6c87bb849e22c',     # 电竞小迷妹 绝地求生
#     'fda0e81923207a2f7fdb7a4974c77e1b',     # 游戏老家 cf

#     'c30a67f97703cbac18616f9785799de9'      # 萌萌图图  游戏动漫
# ]

# for uid in uids:
#     pagenum = 1
#     index(uid, pagenum)