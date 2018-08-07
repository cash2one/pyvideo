import requests
import json

# url = 'http://114.118.4.4/rest/n/feed/profile2?appver=5.8.2.576&did_gt=1533519178726&did=8C85DE7D-D43D-4BA0-A7B0-769AEBC23D81&c=a&ver=5.8&ud=1053007186&sys=ios11.4.1&mod=iPhone6%2C2&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5'
url = 'http://124.243.205.129/rest/n/feed/profile2?appver=5.8.2.576&did_gt=1533519178726&did=8C85DE7D-D43D-4BA0-A7B0-769AEBC23D81&c=a&ver=5.8&sys=ios11.4.1&mod=iPhone6%2C2&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5'
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


hh = {
    'Host': '114.118.4.4',
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

# data = '__NStokensig=a6f91b67d78dceb9d6f19172d3d01d8f0d870695ac70e5052d4ed45a23793629&client_key=56c3713c&count=20&country_code=cn&language=zh-Hans-CN%3Bq%3D1%2C%20en-CN%3Bq%3D0.9&privacy=public&sig=3363f8cfd1fd419fc16ef8ef66e7db9b&source=1&token=2d2e10c7487d4243bba95c3004808a2d-1053007186&user_id=184196'
# data=json.dumps(data),
data = 'client_key=56c3713c&count=20&country_code=cn&language=zh-Hans-CN%3Bq%3D1%2C%20en-CN%3Bq%3D0.9&pcursor=1.529169123262E12&privacy=public&sig=3fdb0572efb11de274fd56f952ba9483&source=1&user_id=208272134'

res = requests.post(url, headers=hh, data=data)

print(res.text)