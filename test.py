import os
import time
# from splinter import Browser

import test01

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import gfunc

import requests

url = 'http://vd.l.qq.com/proxyhttp'

header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '1022',
    'Content-Type': 'text/plain',
    # 'Cookie': 'pgv_pvi=1057001472; RK=FrBxn1CERL; ptcz=43adaf6cdb11ef8863c8f30c9ecca3f7d794c907342145a2a976088de7a7286a; pgv_pvid=7568353335; appuser=CFFACF2B8A024480; o_minduid=1gCMFGJluYwPsQOzySCdlM4YniCoi8_Q; tvfe_boss_uuid=8cb0b948d6dd6ac4; pac_uid=1_1194332304; eas_sid=M155I3d119c7L4o1w1J3N8W6d7; ue_uk=e098cf75fb374372f79380486f251299; ue_uid=940371b6f425307d6badf1f9085d1650; LW_uid=J1P5W3K15947T557p8a7O9t6T2; LW_pid=72d6681a10f61d611fb7d9a5f94288f6; ue_ts=1531975945; ue_skey=5924dc23dac6300d4b818499c5175f24; mobileUV=1_164b18eaa0c_6b9b8; pgv_si=s3472812032; ptisp=ctc; IED_LOG_INFO2=userUin%3D3216598385%26nickName%3Dhhh%26userLoginTime%3D1533790013; LW_sid=B1G5c3b3U7a9b030x2l6F1K4r5; pgv_info=ssid=s2999018270&pgvReferrer=; cm_cookie=V1,110065&6FPUEuCzG5&AQEB2g8q4Rhcs_RMFCP4v3l8hCUZWmSZyDoz&180809&180809; AMCVS_248F210755B762187F000101%40AdobeOrg=1; s_ppvl=%5B%5BB%5D%5D; s_cc=true; AMCV_248F210755B762187F000101%40AdobeOrg=-1891778711%7CMCIDTS%7C17753%7CMCMID%7C69604585822315279883440476244192776143%7CMCAAMLH-1534402396%7C11%7CMCAAMB-1534402396%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1533804796s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17760%7CvVersion%7C2.4.0; s_ppv=cn%253Avideo%253Adetail%2C34%2C38%2C863%2C1366%2C694%2C1366%2C768%2C1%2CL; LPDFturn=898; uid=836481124; LBSturn=709; LCZCturn=534; LPSJturn=390; LZCturn=254; LZIturn=176; localfcs_CFFACF2B8A024480=54cv8c=1533798433_2&54gs0a=1533798433_1&54o68g=1533798433_1; ptui_loginuin=3216598385; pt2gguin=o3216598385; o_cookie=3216598385; adid=3216598385; LHTturn=879; LKBturn=985; LPVLturn=936; LVMturn=418; Lturn=560; LPPBturn=177; LZTturn=727',
    'Cookie': 'pgv_pvi=1057001472; RK=FrBxn1CERL; ptcz=43adaf6cdb11ef8863c8f30c9ecca3f7d794c907342145a2a976088de7a7286a; pgv_pvid=7568353335; appuser=CFFACF2B8A024480; o_minduid=1gCMFGJluYwPsQOzySCdlM4YniCoi8_Q; tvfe_boss_uuid=8cb0b948d6dd6ac4; pac_uid=1_1194332304; eas_sid=M155I3d119c7L4o1w1J3N8W6d7; ue_uk=e098cf75fb374372f79380486f251299; ue_uid=940371b6f425307d6badf1f9085d1650; LW_uid=J1P5W3K15947T557p8a7O9t6T2; LW_pid=72d6681a10f61d611fb7d9a5f94288f6; ue_ts=1531975945; ue_skey=5924dc23dac6300d4b818499c5175f24; mobileUV=1_164b18eaa0c_6b9b8; pgv_si=s3472812032; ptisp=ctc; IED_LOG_INFO2=userUin%3D3216598385%26nickName%3Dhhh%26userLoginTime%3D1533790013; LW_sid=B1G5c3b3U7a9b030x2l6F1K4r5; pgv_info=ssid=s2999018270&pgvReferrer=; cm_cookie=V1,110065&6FPUEuCzG5&AQEB2g8q4Rhcs_RMFCP4v3l8hCUZWmSZyDoz&180809&180809; AMCVS_248F210755B762187F000101%40AdobeOrg=1; s_ppvl=%5B%5BB%5D%5D; s_cc=true; AMCV_248F210755B762187F000101%40AdobeOrg=-1891778711%7CMCIDTS%7C17753%7CMCMID%7C69604585822315279883440476244192776143%7CMCAAMLH-1534402396%7C11%7CMCAAMB-1534402396%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1533804796s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17760%7CvVersion%7C2.4.0; s_ppv=cn%253Avideo%253Adetail%2C34%2C38%2C863%2C1366%2C694%2C1366%2C768%2C1%2CL; uid=836481124; LBSturn=709; LCZCturn=534; LPSJturn=390; LZCturn=254; LZIturn=176; localfcs_CFFACF2B8A024480=54cv8c=1533798433_2&54gs0a=1533798433_1&54o68g=1533798433_1; ptui_loginuin=3216598385; pt2gguin=o3216598385; o_cookie=3216598385; adid=3216598385; LHTturn=879; LKBturn=985; LPVLturn=936; LVMturn=418; Lturn=560; LPPBturn=177; LZTturn=727; LPDFturn=899',
    'Host': 'vd.l.qq.com',
    'Origin': 'http://sports.qq.com',
    'Referer': 'http://sports.qq.com/kbsweb/game.htm?mid=100002:20189983',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

data = {
    "buid":"vinfoad",
    "adparam":"pf=in&ad_type=LD%7CKB%7CPVL&pf_ex=pc&url=http%3A%2F%2Fsports.qq.com%2Fkbsweb%2Fgame.htm&refer=http%3A%2F%2Fsports.qq.com%2Fkbsweb%2Fgame.htm&ty=web&plugin=1.0.0&v=3.4.37&coverid=&vid=i00275sy7c8&pt=&flowid=eb827ec302457f080168dd37fc8ef712_4100201&vptag=&pu=&chid=8&adaptor=2&dtype=1&live=0&resp_type=json&guid=0f330fd2da1720a95fa4aa096aab2c82&req_type=1&platform=4100201&rfid=0dfa42f6c2bbd6900945a9b70ba8aadc_1533864691",
    "vinfoparam":"charge=0&defaultfmt=auto&otype=ojson&guid=0f330fd2da1720a95fa4aa096aab2c82&flowid=eb827ec302457f080168dd37fc8ef712_4100201&platform=4100201&sdtfrom=v1107&defnpayver=1&appVer=3.4.37&refer=http%3A%2F%2Fsports.qq.com%2Fkbsweb%2Fgame.htm&host=sports.qq.com&ehost=http%3A%2F%2Fsports.qq.com%2Fkbsweb%2Fgame.htm&sphttps=0&tm=1533866597&spwm=4&unid=85fba3609b8f11e89d19a0424b63310a&auth_from=40001&auth_ext=%7B%7D&vid=i00275sy7c8&defn=shd&fhdswitch=0&show1080p=1&isHLS=1&dtype=3&sphls=1&spgzip=&dlver=&defsrc=2&encryptVer=7.5&cKey=889e7545eb8ec25549ffb6e0a4e6fcb6"}
try:
    req = requests.post(url, json=data)
    print(req.text)
except Expression as e:

    print('req')