import re
import urllib.request
import json
import time
import random
import sys
import requests
from urllib.parse import quote


def getVideoInfo(url):
    ruleTitle = re.compile('<title>(.*)</title>')
    ruleId = re.compile('v.youku.com/v_show/id_(.*).html')
    showId = re.compile('&s=(.*?)&')

    text = urllib.request.urlopen(url).read().decode('utf8')
    videoTitle = ruleTitle.findall(text)
    showid = showId.findall(text)
    videoId = ruleId.findall(url)
    return videoTitle[0], videoId[0], showid[0]

def getRrueLink(videoid, link, showid):
    # url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.11&appKey=24679788&t=1533086546066&sign=73e9085d64e0bc7f80708d8c4c096fb8&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data={"steal_params":"{\"ccode\":\"0502\",\"client_ip\":\"192.168.1.1\",\"utid\":\"iTbUE8VuE3ECAXZyBV8VD0xE\",\"client_ts\":1533086546,\"version\":\"0.5.64\",\"ckey\":\"110#CgCkAUkfkzseyLJegkTuMuy2kMZ/buAMjQkgkGjx81HOJVaTfJF/83scuMF+AIjIjVK3+n4x8f+QlkGq3tdtW39TkuBWeMudjaYAkgax82ZTRcUIbR+qFMlnWS5QUqlm+rVu6w/oQSSirK4rsAkwsziN1w9ij9cwkP5ysn8ysbBJDyEesfSwnake9aZ/sTAu4CFSyL2usFjxkcZws3cwsGkkgOmOoc+Pkk2mswn/DY7f/1kKIsy2DHkkGEm29oFGnwSvpkkX8J0prq971c6hyj0D+pKHL5ssNvQjhpvfcu1pMDJ8UPIVaDYvNylyHhbJ4OZ9x2XjR4PRRh5BZW0XGsym6+1qcO+EEMHJ7U5GpXVOoPRF07y5/yN4vt8psb3NE0l4F8pxvqY9T5r/ePSfJYtZ1k9YwGCqCzG1oiT01nUjBvJCtTACkFm6n56JjSsHJjehjbAhp3kfXBNKGYWqw5S2Y8b9W/8C1Rgfvi+JJK==\"}","biz_params":"{\"vid\":\"XMzYzMjk0MDA2OA==\",\"current_showid\":\"396037\"}","ad_params":"{\"site\":1,\"wintype\":\"interior\",\"p\":1,\"fu\":0,\"vs\":\"1.0\",\"rst\":\"mp4\",\"dq\":\"hd2\",\"os\":\"mac\",\"osv\":\"\",\"d\":\"0\",\"bt\":\"pc\",\"aw\":\"w\",\"needbf\":1,\"atm\":\"\"}"}'
    # url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.11&appKey=24679788&t=1533091661422&sign=1b1c1fca1e5b797d5f29719ee02983ed&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22steal_params%22%3A%22%7B%5C%22ccode%5C%22%3A%5C%220502%5C%22%2C%5C%22client_ip%5C%22%3A%5C%22192.168.1.1%5C%22%2C%5C%22utid%5C%22%3A%5C%22iTbUE8VuE3ECAXZyBV8VD0xE%5C%22%2C%5C%22client_ts%5C%22%3A1533091661%2C%5C%22version%5C%22%3A%5C%220.5.64%5C%22%2C%5C%22ckey%5C%22%3A%5C%22110%23EjskAUkfkzUQHcBAgkTuMuy2kMZ%2FbiJgjQkgkGjx81GSmUTCeWpwN3snkg8VM3J%2F0NB2%2FngqNOnQiKvH3A8ETxzn2IIxPmjgjqwkizJ08MzQvKDCGTUt5EaZNH3%2FOEhTpBntGWfoTzRFiOf9T5KijTkiAfI0Slzis9kk4EKQFeKwtncO9PSwdOgpwTDsp9SwDxIkwYQWs9IiWGUkG9kwj9kimkk3sLsWDsOU%2BrmQsEkmDH2DBFw3Z52D2a2DsLgOkrFYrajM2pUkDoBADvt1%2FH9M6LKykq6o7zsSWOz8Id69kNScB41XgeRom9o7jvnidQqAR5SzjDgCltsYvKAoSaS3JCD1Q8P1gQwYvlpq%2FJ5inEm%2B0mGfWpexmUxGAvC6sg3HQdffJq6tK%2Fpfv7bwofwwONyiQynF%2BKFfbs%2BK2VBAsTj8TPe0DXuTOOhn8qGUqJwkv9zfDxv9dU7HDaqpC9sgGw3l2SbdSLrldr8mp1XhK7my%5C%22%7D%22%2C%22biz_params%22%3A%22%7B%5C%22vid%5C%22%3A%5C%22XMzYzMjk0MDA2OA%3D%3D%5C%22%2C%5C%22current_showid%5C%22%3A%5C%22396037%5C%22%7D%22%2C%22ad_params%22%3A%22%7B%5C%22site%5C%22%3A1%2C%5C%22wintype%5C%22%3A%5C%22interior%5C%22%2C%5C%22p%5C%22%3A1%2C%5C%22fu%5C%22%3A0%2C%5C%22vs%5C%22%3A%5C%221.0%5C%22%2C%5C%22rst%5C%22%3A%5C%22mp4%5C%22%2C%5C%22dq%5C%22%3A%5C%22hd2%5C%22%2C%5C%22os%5C%22%3A%5C%22mac%5C%22%2C%5C%22osv%5C%22%3A%5C%22%5C%22%2C%5C%22d%5C%22%3A%5C%220%5C%22%2C%5C%22bt%5C%22%3A%5C%22pc%5C%22%2C%5C%22aw%5C%22%3A%5C%22w%5C%22%2C%5C%22needbf%5C%22%3A1%2C%5C%22atm%5C%22%3A%5C%22%5C%22%7D%22%7D'
    
    url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.11&appKey=24679788&t=1533091661422&sign=1b1c1fca1e5b797d5f29719ee02983ed&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data='    
    # url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/'
    biz_params = {
        "vid":videoid,
        "current_showid":str(showid)
    }

    data = {
        "steal_params":"{\"ccode\":\"0502\",\"client_ip\":\"192.168.1.1\",\"utid\":\"iTbUE8VuE3ECAXZyBV8VD0xE\",\"client_ts\":1533091661,\"version\":\"0.5.64\",\"ckey\":\"110#EjskAUkfkzUQHcBAgkTuMuy2kMZ/biJgjQkgkGjx81GSmUTCeWpwN3snkg8VM3J/0NB2/ngqNOnQiKvH3A8ETxzn2IIxPmjgjqwkizJ08MzQvKDCGTUt5EaZNH3/OEhTpBntGWfoTzRFiOf9T5KijTkiAfI0Slzis9kk4EKQFeKwtncO9PSwdOgpwTDsp9SwDxIkwYQWs9IiWGUkG9kwj9kimkk3sLsWDsOU+rmQsEkmDH2DBFw3Z52D2a2DsLgOkrFYrajM2pUkDoBADvt1/H9M6LKykq6o7zsSWOz8Id69kNScB41XgeRom9o7jvnidQqAR5SzjDgCltsYvKAoSaS3JCD1Q8P1gQwYvlpq/J5inEm+0mGfWpexmUxGAvC6sg3HQdffJq6tK/pfv7bwofwwONyiQynF+KFfbs+K2VBAsTj8TPe0DXuTOOhn8qGUqJwkv9zfDxv9dU7HDaqpC9sgGw3l2SbdSLrldr8mp1XhK7my\"}",
        "biz_params":json.dumps(biz_params),
	    "ad_params":"{\"site\":1,\"wintype\":\"interior\",\"p\":1,\"fu\":0,\"vs\":\"1.0\",\"rst\":\"mp4\",\"dq\":\"hd2\",\"os\":\"mac\",\"osv\":\"\",\"d\":\"0\",\"bt\":\"pc\",\"aw\":\"w\",\"needbf\":1,\"atm\":\"\"}"
    }

    data = quote(json.dumps(data), 'utf-8')
    # print(data)

    return
    pram = {
        'jsv': '2.4.11',
        'appkey': '24679788',
        't': '1534842071024',
        'sign': '657220dca238bf7e8f72810352074a93',
        'api': 'mtop.youku.play.ups.appinfo.get',
        'v': '1.1',
        'timeout': '20000',
        'YKPid': '20160317PLF000211',
        'YKLoginRequest': 'true',
        'type': 'json',
        'dataType': 'jsonp',
        'callback': 'mtopjsonp1',
        'data': data
    }

    url = url + data
    # 多空格 替换
    url = url.replace('%20', '')

    headers = {
        # 'referer': 'http://player.youku.com/embed/XMzYzMjk0MDA2OA=='
        'cookie': '__ysuid=1531791676673fQy; cna=iTbUE8VuE3ECAXZyBV8VD0xE; juid=01ciocrmbla8i; __yscnt=1; __aryft=1532608660; __aysid=1532841299144PKc; __ayft=1533059513805; __ayscnt=1; yseid=15330856090927r3Env; yseidcount=8; ycid=0; rpvid=1533085645926Avh4SC-1533085656223; __utmarea=; __arycid=cms-00-1519-27244-0; __arcms=cms-00-1519-27244-0; P_ck_ctl=3F4E0690C5AB7412905FDDDE48A3D811; _m_h5_tk=9e5625e48af2a16c90150ae820ea438f_1533101218495; _m_h5_tk_enc=2aa4f4820a8b61a7b9b528a0940bbc5b; seid=01cjpquse52639; referhost=; seidtimeout=1533098518795; ypvid=1533096719723zhFbq4; ysestep=13; yseidtimeout=1533103919724; ystep=161; __ayvstp=46; __aysvstp=71; isg=BPHxrDI3DuFKCqLEUDO0TsjaAHtLdmRd1iFL4NMG3rj1-hBMGy6HIavbGM45Rv2I; __arpvid=1533097225248UlQ6sv-1533097225266; __aypstp=24; __ayspstp=101',
        'referer': link,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    data = requests.get(url, headers=headers)
    # print(data.text)
    text = data.text

    dic = re.compile('mtopjsonp1\(({.*?})\)')

    retStr = dic.findall(text)[0]
    retDic = json.loads(retStr)

    print(retDic)

    stream = retDic['data']['data']['stream']

    for item in stream:
        # 3gphd 480
        # mp4sd 640
        # mp4hd 960
        # mp4hd2v2 1280
        # mp4hd3v2 1920
        m3u8_url = item['m3u8_url']
        segs = item['segs']
        if item['stream_type'] == 'mp4hd2v2':
            for i in range(0, len(segs)):
                seg = segs[0]
                data = requests.get(seg['cdn_url']).text
                name = 'python_pandas_%02d.mp4' % (i)
                with open(name, "wb") as code:
                    code.write(data)
            
        

    # info = json.loads(data.text)
    # print(info)

def main():
    link = 'https://v.youku.com/v_show/id_XMzYzMjk0MDA2OA==.html'
    videotitle, videoid, showid = getVideoInfo(link)
    print(videotitle)
    print(videoid)
    print(showid)
    getRrueLink(videoid, link, showid)


if __name__ == '__main__':
    main()