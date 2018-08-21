
import requests
import math

# dd = 30/30
# print(math.ceil(dd))
url = 'http://mtrace.qq.com/mkvcollect?k=IJX12I2YLX57&a=4.8.51.129&s=0.5.5.004&n=9'
headers = {
    'Host': 'mtrace.qq.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'isnm=1',
    'Connection': 'keep-alive',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Language': 'zh-cn',
    'Content-Length': '1300',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'KuaiBao/4.8.51.129 CFNetwork/902.2 Darwin/17.7.0',
    'Content-Encoding': 'rc4,gzip',
}

res = requests.post(url, headers=headers)
print(res.content)


