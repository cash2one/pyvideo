
import requests
import json
import re
import dbfunc
import time


def index(uid, pagenum):
    # url = 'http://v.qq.com/vplus/3fcca62af8c4b211b87401b4530cff9a/videos '

    url = 'http://c.v.qq.com/vchannelinfo?otype=json&uin='+ uid +'&qm=1&pagenum='+ str(pagenum) +'&num=24&sorttype=0&orderflag=0&callback=jQuery19104105733024427589_1531375140863&low_login=1&_=1531375140876'
    print(url)
    req = requests.get(url)
    html = req.text    
    dd = re.findall('\(({.*?})\)', html)[0]

    jsondd = json.loads(dd)
    videolst = jsondd['videolst']
    
    for video in videolst:

        uploadtime = video['uploadtime']
        today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        # # TODO 今天
 
        # if uploadtime.find(u'前') != -1:
        #     uploadtime = today

        # if uploadtime.find(u'内') != -1:
        #     uploadtime = today

        account = ''
        title = video['title']
        print(title)
        url = video['url']
        alias = ''
        tags = ''
        first_class = ''
        second_class = ''
        is_exist_local = 0
        local_path = ''
        qq_create_time = uploadtime
        create_time = today
        vid = video['vid']

        dbfunc.insertVideo(account, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time, vid)

uids = [

    'f401289eef888c247afa2888d66bd01c',     # 其实你很幽默 国外 幽默段子 憨豆先生
    '9d0387de8f60ab27bafef9e42a504593',     # 搞笑 有色有声姐

    '0c4932b8a08dd5b42a4797b4c8060361',     # 电视剧 畅涵影视 
    '48655f5bb2709cfef893016a79843b0d',     # 影视 风云英雄 
    '35f2a7e76ee6cf68b1f4158faf187d3f',     # 影视 余独不觉 
    '96486663bb39295ba0b6c87bb849e22c',     # 影视新天地
    '7464eec19eb5b6e885fc9e995a19b595',     # 电影 寻找感动瞬间   猴子看影视
    '0524cbe3cafc8c0d3d9d36e561cdbe5c',     # 林正英  圆圆的酒窝 鬼片
    '0c6fcdeff1c6fd7788923deaee77407e',     # 综艺明星 明星风云 

    '3fcca62af8c4b211b87401b4530cff9a',     # 动漫 皮皮马动漫
    '3189c372f7673e44573f990813172070',     # 动漫 火影
    '1661bab3a8dbd85ba0b6c87bb849e22c',     # 动漫 御宅小夜动漫社 
    '3189c372f7673e44573f990813172070',     # 动漫  趣谈史  火影 
    'd45c5239b8048e6bb188a15948ea99e1',     # 鑫动漫迷  狐妖小红娘

    '3a648b8b537c74308adc82edb0c933ed',     # lol 每日撸报  徐老师来巡山
    'b125da5d9a0d60877126a454e1060f71',     # 王者荣耀 朋弟说游
    '06c7b21843daa5fdea1d320834d87bff',     # 星爷说游戏  刺激战场 王者荣耀
    '77847f85dd4bf9073c127e842543015d',     # 小樱桃说游戏  绝地求生 王者荣耀
]

for uid in uids:
    pagenum = 1
    index(uid, pagenum)