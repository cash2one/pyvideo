import requests
import json
import time
import gfunc
import re
import datetime
import sys
import dbfunc


'''
1.知道快手号kwaiId 查到用户userId


'''
# url = 'http://114.118.4.4/rest/n/feed/profile2?appver=5.8.2.576&did_gt=1533519178726&did=8C85DE7D-D43D-4BA0-A7B0-769AEBC23D81&c=a&ver=5.8&ud=1053007186&sys=ios11.4.1&mod=iPhone6%2C2&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5'
# url = 'http://124.243.205.129/rest/n/feed/profile2?appver=5.8.2.576&did_gt=1533519178726&did=8C85DE7D-D43D-4BA0-A7B0-769AEBC23D81&c=a&ver=5.8&sys=ios11.4.1&mod=iPhone6%2C2&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5'

# 用戶
# '/rest/n/user/profile/v2?appver=5.8.5.606&did=8C85DE7D-D43D-4BA0-A7B0-769AEBC23D81&c=a&ver=5.8&ud=1053723107&sys=ios11.4.1&mod=iPhone6%2C2&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5'
# 作品
# 114.118.4.4


dd = {
    'ver': '5.8',
    'ud': '1053007186',
    'sys': 'ios11.4.1',
    'net': '中国移动_5',
    'mod': 'iPhone6,2',
    'did_gt': '1533519178726',
    'did': '8C85DE7D-D43D-4BA0-A7B0-769AEBC23D81',
    'c': 'a',
    'appver': '5.8.2.576'
}

data = {
    '__NStokensig': '0cc83e1454e5a32ca96ba79adda1dfa06c3ff0fa1e1875c53c10d1097a70a3af',
    'client_key': '56c3713c',
    'count': '20',
    'country_code': 'cn',
    'language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'pcursor': '1.532541728534E12',
    'privacy': 'public',
    'sig': 'c5bcec0c558cc73591c8537546cfe2c4',
    'source': '1',
    'token': '2d2e10c7487d4243bba95c3004808a2d-1053007186',
    # 'user_id': '691319980'
}




# data = '__NStokensig=a6f91b67d78dceb9d6f19172d3d01d8f0d870695ac70e5052d4ed45a23793629&client_key=56c3713c&count=20&country_code=cn&language=zh-Hans-CN%3Bq%3D1%2C%20en-CN%3Bq%3D0.9&privacy=public&sig=3363f8cfd1fd419fc16ef8ef66e7db9b&source=1&token=2d2e10c7487d4243bba95c3004808a2d-1053007186&user_id=184196'
# data=json.dumps(data),
# data = 'client_key=56c3713c&count=20&country_code=cn&language=zh-Hans-CN%3Bq%3D1%2C%20en-CN%3Bq%3D0.9&pcursor=1.529169123262E12&privacy=public&sig=3fdb0572efb11de274fd56f952ba9483&source=1&user_id=208272134'
# data = 'client_key=56c3713c&count=20&country_code=cn&language=zh-Hans-CN%3Bq%3D1%2C%20en-CN%3Bq%3D0.9&privacy=public&sig=0d5a39e3b63a0c5ef6202dd20ca75b8f&source=1&token=20c3ce62275040f6a7d0bb60715c7d05-1053723107&user=9896719'
# TODO sig

def index(url, headers, data):
    res = requests.post(url, headers=headers, data=data)
    jsondata = json.loads(res.text)
    result = jsondata['result']
    # print(result)
    if result == 1:
        feeds = jsondata['feeds']
        dataArr = []
        for feed in feeds:
           addVideo(feed)



def addVideo(feed):
    # 标题
    caption = feed['caption']
    main_mv_urls = feed['main_mv_urls']
    url = main_mv_urls[0]['url']

    photo_id = feed['photo_id']
    cover_thumbnail_urls = feed['cover_thumbnail_urls']
    coverurl = cover_thumbnail_urls[0]['url']
    kwaiId = feed['kwaiId']
    username = feed['user_name']
    share_info = feed['share_info']
    userid = feed['user_id']

    # TODO 是否下载 kuaishou
    # os.getcwd()=D:\    sys.path[0]=D:\python_test
    dirname = sys.path[0]+'\kuaishou\\'+kwaiId
    gfunc.createDir(dirname)

    html = requests.get(url)
    html = html.content
    pagename = dirname+'\\'+ re.findall('==_(.*?.mp4)', url)[0]
    start_down_time = datetime.datetime.now()
    print('开始下载时间{}'.format(start_down_time))
    with open(pagename,'wb') as f:
        f.write(html)
    end_time = datetime.datetime.now()
    print('下载结束时间{}'.format(end_time))

    dic = {
        'qq': '',
        'title': caption,
        'url': url,
        'alias': '',
        'tags': '',
        'first_class': '游戏',
        'second_class': '游戏',
        'platform_create_time': feed['time'],
        'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
        'aid': '1000',
        'vid': photo_id,
        'pic': coverurl,
        'is_exist_local': 1,
        'local_path': pagename,
        'fromUserId': '333'
    }

    dbfunc.insertVideo(dic)

# jmz920618
def getUserIdFromKwaiId(kid):
    kurl = 'https://live.kuaishou.com/profile/'+kid
    print(kurl)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1534924914; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1534924914; clientid=3; did=web_93f8f8ff0dc7343496232771212d749b; live_deviceid=web_93f8f8ff0dc7343496232771212d749b; client_key=65890b29',
        'Host': 'live.kuaishou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
    }
    res = requests.get(kurl, headers=headers)
    try:
        userId = re.findall(',"userId":(.*?),"id"', res.text)[1]
        return userId    

    except Exception as e:
        print('eeeeeee: ', str(e))
        return ''
    
# sig = '5513d4690457327e00c1a64336774aa4'
# user_id = '175080210'
def main(kid='', sig=''):

    if len(kid) == 0 and len(sig) == 0:
        return False

    user_id = getUserIdFromKwaiId(kid)
    if len(user_id) == 0:
        return False
    
    url = 'http://180.186.38.200/rest/n/feed/profile2?appver=5.8.5.606&did=8C85DE7D-D43D-4BA0-A7B0-769AEBC23D81&c=a&ver=5.8&ud=1053723107&sys=ios11.4.1&mod=iPhone6%2C2&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5'
    headers = {
        'Host': '180.186.38.200',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Connection': 'keep-alive',
        'X-REQUESTID': '207386912',
        'Accept': 'application/json',
        'User-Agent': 'kwai-ios',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'Content-Length': '297',
        'Accept-Encoding': 'gzip, deflate',
    }

    pcursor = ''
    data = 'client_key=56c3713c&count=20&country_code=cn&language=zh-Hans-CN%3Bq%3D1%2C%20en-CN%3Bq%3D0.9&privacy=public&sig='+sig+'&source=1&token=20c3ce62275040f6a7d0bb60715c7d05-1053723107&user_id='+user_id

    index(url, headers, data)

    
