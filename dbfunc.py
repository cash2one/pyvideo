
from DBHelper import dbHelper
from config import *
import random
import gfunc

# 删除
def delVideos():
    db = dbHelper.database()
    sql = "DELETE FROM videos where pic is null"
    db.update(sql)
    db.close()

def createTable():
    db = dbHelper.database()
    db.createTable('User', CreateUserSql)
    db.createTable('uploader', CreateUploaderSql)
    db.createTable('anchor', CreateAnchorSql)
    db.createTable('videos', CreateVideosSql)

def getUser(dic={}):
    return getData('user', dic)

def addUser(name, pwd, pic=''):
    md5pwd = gfunc.pwdEncrypt(pwd)
    dic = {
        'name': name,
        'pwd': pwd,
        'md5pwd': md5pwd,
        'pic': pic
    }

    return insertData('user', dic)


# [ uploader ]

def insertUploader(account, pwd, ext, platform, loginType):
    if gfunc.isLogin == False:
        return False
    dic = {
        'account': account,
        'pwd': pwd,
        'ext': ext,
        'platform': platform,
        'loginType': loginType
    }
    dic = addFromUserId(dic)

    return insertData('uploader', dic)

def getUploader(platform):
    dic = addFromUserId({'platform': platform})
    return getData('uploader', dic)

# [ 主播 ]
# 获取主播
def getAnchor(platform):
    dic = addFromUserId({'platform': platform})
    return getData('anchor', dic)

# 添加主播 dic = {name, uin, intr, vnum, page, fromUserId, platform}
def addAnchor(dic):
    # TODO fromUserId
    if gfunc.isLogin() == False:
        return False
    dic = addFromUserId(dic)
    flag = insertData('anchor', dic)
    
    return flag

# 主播是否存在
def checkAnchor(dic):
    return checkDataExistToTable('anchor', dic)
    
# 更新主播
def updateAnchor(setDic, whereDic):
    # 添加条件userid
    whereDic = addFromUserId(whereDic)
    updateData('anchor', setDic, whereDic)

# 【videos】

# 插入数据库 video
def insertVideo(dic):
    # TODO 登录验证
    if checkLogin() == False:
        return False
    
    vid = dic['vid']
    dic = addFromUserId(dic)
    db = dbHelper.database()
    # 查询vid 是否存在 存在更新qq_create_time 不存在加入
    existDic = { 'vid': vid }
    existDic = addFromUserId(existDic)
    isExist = checkDataExistToTable('videos', existDic)
    print('查询 数据库videos中 vid是否存在...')
    if isExist:
        # 更新
        flag = updateVideo({'platform_create_time': dic['platform_create_time']}, existDic)
        print('videos table is exist update time')
        return flag
    else:
        flag = insertData('videos', dic)
        print('inset video success')
        return flag

# 更新video 
def updateVideo(setDic, whereDic):
    whereDic = addFromUserId(whereDic)
    flag = updateData('videos', setDic, whereDic)
    return flag

# 获得video
def getVideo(dic={}, other='', limit=[]):
    dic = addFromUserId(dic)
    res = getData('videos', dic, other, limit)
    return res


# 获得数据库所有的视频
def getAllVideo(limit=[]):
    dic = addFromUserId()
    res = getData('videos', dic, limit=limit)
    return res

# 今天采集的
def getTodayVideo(limit=[]):
    other = " and create_time >= date_format(NOW(),'%Y-%m-%d')"
    res = getVideo(other=other, limit=limit)


def getVideos(data={}, other='', cursor=0):
    # TODO data 注销登陆会记录上一次登陆的userid 不知什么原因 目前强制加入userid
    dic = addFromUserId(data)
    count = 9
    limit = [int(cursor), int(cursor)+count]
    return getData('videos', dic, other, limit)

# 未发布 [0, 13]
def getNotPublishVideoFromAid(aid, limit=[]):
    dic = { 'aid': aid }
    dic = addFromUserId(dic)
    res = getData('videos', dic, 'publish_time is null', limit)
    return res

# 今天待发布的
def getTodayWartpublishVideo(account='', limit=[]):
    dic = {}
    if len(account) > 0:
        dic = { 'qq': account }
    other = " and create_time >= date_format(NOW(),'%Y-%m-%d') and publish_time is null"
    return getVideo(dic, other=other, limit=limit)

# 未发布 [0, 13]
def getUnpublishedVideo(aid='', limit=[]):
    dic = { 'aid': aid }
    other = 'and publish_time is null'
    return getVideo(dic, other=other, limit=limit)

# 待发布
def getWartpublishVideo(account='', limit=[]):
    dic = {}
    other = 'and publish_time is null'
    if len(account) > 0:
        dic['qq'] = account
    else:
        other = 'qq!=0 and publish_time is null'
    return getVideo(dic, other=other, limit=limit)

# 今天已发布视频
def getTodayPublishedVideo(account='', limit=[]):
    dic = {}
    if len(account) > 0:
        dic = { 'qq': account }
    other = " and publish_time >= date_format(NOW(),'%Y-%m-%d')"
    res = getVideo(dic, other=other, limit=limit)
    return res


def fetchVideo(qq, day=None, count=None):
    db = dbHelper.database()
    day_sql = ''
    if day != None:
        day_sql = "AND create_time >= date_format(NOW(),'%Y-%m-%d')"
    
    sql = "SELECT * FROM videos WHERE qq = '%s' AND publish_time is null %s" % (qq, day_sql)
    res = db.fetch(sql, limit=count)
    return res

# [ Public ]

def insertData(table, dic):
    db = dbHelper.database()
    ls = list(dic)
    sql = 'insert %s (' % table + ','.join(ls) + ') values (' +\
            ','.join(['%({})r'.format(field) for field in ls]) + ');'
    sql = sql % dic
    flag = db.inset(sql)
    db.close()
    return flag

# 更新数据 table setDic whereDic
def updateData(table, setDic, whereDic):
    db = dbHelper.database()
    setKeys = setDic.keys()
    whereKeys = whereDic.keys()

    sql = 'update %s set ' % table + ' , '.join([ key+'='+ "'%s'" % setDic[key] for key in setKeys]) + '\
           where ' + ' and '.join([key+'='+ "'%s'" % whereDic[key] for key in whereKeys]) 
    print(sql)
    flag = db.update(sql)
    db.close()
    return flag

# 获得所有数据 table conditionDic other:publish_time is null create_time >= date_format(NOW(),'%Y-%m-%d' 

def getData(table, dic={}, other='', limit=[]):
    db = dbHelper.database()
    keys = dic.keys()
    sql = 'select * from %s where ' % table + ' and '.join([ key+'='+ "'%s'" % dic[key] for key in keys])
    if len(other) > 0:
        sql = sql + ' ' + other
    if limit != None and len(limit) == 2:
        sql = sql + " limit %d,%d" % (int(limit[0]),int(limit[1]))
    print(sql)
    res = db.fetch(sql)
    print(len(res))
    return res

# 检查该数据是否存在 table conditionDic
def checkDataExistToTable(table, conditionDic={}):

    res = getData(table, conditionDic)
    if len(res) > 0:
        return True
    else:
        return False

def addFromUserId(conditionDic={}):
    conditionDic['fromUserId'] = gfunc.getUserId()
    return conditionDic

def checkLogin():
    return gfunc.isLogin()

# TODO 特殊
def updateAllFromUserId():
    db = dbHelper.database()
    db.update("update kduser set fromUserId = '1'")
    db.update("update videos set fromUserId = '1'")
    db.update("update anchor set fromUserId = '1'")

def main():  
    # createTable()  
    pass

if __name__ == '__main__':
    main()
