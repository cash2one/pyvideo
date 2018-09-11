
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
    db.createTable(CreateUserSql, 'User')
    db.createTable(CreateUploaderSql, 'uploader')
    db.createTable(CreateAnchorSql, 'anchor')
    db.createTable(CreateVideosSql, 'videos')

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

def insertUploader(account, pwd, ext, platform):
    if gfunc.isLogin == False:
        return False
    dic = {
        'account': account,
        'pwd': pwd,
        'ext': ext,
        'platform': platform
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




def getVideos(data={}, other='', cursor=0):
    # TODO data 注销登陆会记录上一次登陆的userid 不知什么原因 目前强制加入userid
    dic = addFromUserId(data)
    count = 9
    limit = [int(cursor), int(cursor)+count]
    return getData('videos', dic, other, limit)

def getVideos

# 未发布 [0, 13]
def getNotPublishVideoFromAid(aid, limit=[]):
    dic = { 'aid': aid }
    dic = addFromUserId(dic)
    res = getData('videos', dic, 'publish_time is null', limit)
    return res





# 今天已发布的视频
def fetchTodayPublishedVideo(qq):
    db = dbHelper.database()  
    day_sql = "AND publish_time >= date_format(NOW(),'%Y-%m-%d')"
    
    sql = "SELECT * FROM videos WHERE qq = '%s' %s" % (qq, day_sql)

    res = db.fetch(sql)
    return res

# 未发布视频 qq
def fetchNotPublishedAndQQ():
    db = dbHelper.database()
    sql = "SELECT * FROM videos WHERE qq!=0 AND publish_time is null"
    res = db.fetch(sql)
    if res:
        return res
    return []

def fetchVideo(qq, day=None, count=None):
    db = dbHelper.database()
    day_sql = ''
    if day != None:
        day_sql = "AND create_time >= date_format(NOW(),'%Y-%m-%d')"
    
    sql = "SELECT * FROM videos WHERE qq = '%s' AND publish_time is null %s" % (qq, day_sql)
    res = db.fetch(sql, limit=count)
    return res

def fetchVideoFromAlias(qq, alias):
    db = dbHelper.database()
    sql = "SELECT * FROM videos WHERE qq = '%s' AND publish_time is null AND alias = '%s'" % (qq, alias)
    res = db.fetch(sql)
    return res

def fetchVideoFromAnchor(aid):
    db = dbHelper.database()
    sql = "select * from videos where aid = '%d' and publish_time is null " % int(aid)
    res = db.fetch(sql)
    return res

def fetchTodayVideo():
    db = dbHelper.database()
    sql = "SELECT * FROM videos WHERE create_time >= date_format(NOW(),'%Y-%m-%d')"
    res = db.fetch(sql)

    dd = []
    for item in res:
        if item[8].find('小时') != -1:
            dd.append(item)
    return dd

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
        if sql.find('and') == -1:
            sql = sql + other
        else:
            sql = sql + ' and ' + other

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
    pass

if __name__ == '__main__':
    main()
