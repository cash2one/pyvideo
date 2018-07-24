
import requests
import json
import re
import dbfunc
import time

def index():
    # url = 'http://v.qq.com/vplus/3fcca62af8c4b211b87401b4530cff9a/videos '

    uid = '607af5db22c0f59aa0b6c87bb849e22c'
    pagenum = 1

    url = 'http://c.v.qq.com/vchannelinfo?otype=json&uin='+ uid +'&qm=1&pagenum='+ str(pagenum) +'&num=24&sorttype=0&orderflag=0&callback=jQuery19104105733024427589_1531375140863&low_login=1&_=1531375140876'
    print(url)
    req = requests.get(url)
    print(req.text)
    html = req.text    
    dd = re.findall('\(({.*?})\)', html)[0]

    jsondd = json.loads(dd)
    videolst = jsondd['videolst']
    
    for video in videolst:

        uploadtime = video['uploadtime']
        today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        # TODO
        if uploadtime.find(u'前') or uploadtime.find(u'内') != -1:
            # 今天
            uploadtime = today

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

        dbfunc.insertVideo(account, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time)

index()