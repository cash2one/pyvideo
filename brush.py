import requests
import re
import json
import dbfunc
from random import Random
import random
import time

from config import *


def main():
    url = 'https://mp.qq.com/api/article_manager/article/list?current=1&every=15&state=0&token=1609723396'

    headers = {
        'authority': 'mp.qq.com',
        'method': 'GET',
        'path': '/api/article_manager/article/list?current=1&every=15&state=0&token=1609723396',
        'scheme': 'https',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'pgv_pvi=1057001472; RK=FrBxn1CERL; ptcz=43adaf6cdb11ef8863c8f30c9ecca3f7d794c907342145a2a976088de7a7286a; pgv_pvid=7568353335; tvfe_boss_uuid=8cb0b948d6dd6ac4; eas_sid=M155I3d119c7L4o1w1J3N8W6d7; ue_uk=e098cf75fb374372f79380486f251299; ue_uid=940371b6f425307d6badf1f9085d1650; LW_uid=J1P5W3K15947T557p8a7O9t6T2; LW_pid=72d6681a10f61d611fb7d9a5f94288f6; ue_ts=1531975945; ue_skey=5924dc23dac6300d4b818499c5175f24; mobileUV=1_164b18eaa0c_6b9b8; LW_sid=B1G5c3b3U7a9b030x2l6F1K4r5; AMCV_248F210755B762187F000101%40AdobeOrg=-1891778711%7CMCIDTS%7C17753%7CMCMID%7C69604585822315279883440476244192776143%7CMCAAMLH-1534402396%7C11%7CMCAAMB-1534402396%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1533804796s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17760%7CvVersion%7C2.4.0; __root_domain_v=.mp.qq.com; _qddaz=QD.itx4t7.l3txjt.jkm7ki04; ts_uid=8883746491; pac_uid=1_810359132; pgv_pvid_new=810359132_3a88ec091e; pgv_si=s4023227392; ptisp=ctc; pgv_info=ssid=s5995211425; ts_refer=xui.ptlogin2.qq.com/cgi-bin/xlogin%3Fappid%3D717054801%26daid%3D296%26s_url%3Dhttps%3A//mp.qq.com%26style%3D33%26hide_title_bar%3D1%26fontcolor%3Dffffff%26e; o_cookie=810359132; _supWebp=1; kdmp-session=eyJzZWNyZXQiOiJBR1J2QmxSVFFxcU5RanVURzBiaF9xRUsiLCJfZXhwaXJlIjoxNTM2MDg1MzE5ODI0LCJfbWF4QWdlIjo3MjAwMDAwfQ==; ptui_loginuin=1194332304; pt2gguin=o1194332304; uin=o1194332304; skey=@CpMF0u4ju; p_uin=o1194332304; pt4_token=QUHvokXSE7YpBoxWlNqGNNNBuL0mdcvwLu-RNm5Ifug_; p_skey=-E6UNYrbV1T0oaHi7MmeSvjPxidtHvYH9MHxXJYDz48_; mp_uin=1466387522; _qddamta_2852156220=3-0; _qdda=3-1.4d1w7p; _qddab=3-nqe5gc.jlo1g3o9; mp_skey=zzBlce5BX1vVr1H3ogvzmOY3455tKcL-kOYXpJI3cXM_; ts_last=mp.qq.com/page/article_manager',
        'referer': 'https://mp.qq.com/page/article_manager',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'x-csrf-token': 'ogfl2Dnc-ilt-2xIKEYo_JK6TeFm3mht4xDs',
        'x-requested-with': 'XMLHttpRequest'
    }
    res = requests.get(url, headers=headers)
    text = json.loads(res.text)

    if text['ret']==0:
        data = text['data']
        datalist = data['list']
# http://post.mp.qq.com/kan/video/1901292418-8595b8ca06e431aj-wAfbNN.html?_wv=2281701505&sig=d5453cdfac58079e8eee8baaf999cb4f&time=1535942766
        for item in datalist:
            url = item['article_url']+'&sourcefrom=6'
            title = item['content']['title']
            rowkey = item['rowkey']
            vid = re.findall(rowkey+"-(.*?).html", url)[0]
            kid = '1'
            dbfunc.addKdvideo(url, title, vid, kid)

def random_phonenum(numlength=32):
    num =''
    chars='1234567890'
    length=len(chars)-1
    rd=Random()
    for j in range(numlength):
        num +=chars[rd.randint(0,length)]
    return num

def refresh(item):
    refer = item[1]
    headers = {
        'Host': 'kandian.qq.com',
        'Origin': 'http://post.mp.qq.com',
        'Referer': refer,
        'User-Agent': random.choice(USER_AGENTS)

    }

    vid = item[3]
    token = random_phonenum(10)
    uuid = random_phonenum(30)
    TIMEOUT = 10

    url = 'http://kandian.qq.com/qz_kandian_ext/kandian_ext/SetVideoPlayCount?vid=%s&rtype=0&rcode=0&token=%s&uuid=%s' % (vid, token, uuid)

    try:
        res = requests.get(url, headers=headers, timeout=TIMEOUT)
        print(res.text)

    except Exception as e:
        print('request error')

def brush():
    res = dbfunc.getKdvideo()
    while True:
        for item in res:
            refresh(item)

        time.sleep(5)
        
brush()
    