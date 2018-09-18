
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

# 创建 anchor
def createTableAnchor():
    db = dbHelper.database()
    table = 'anchor'
    sql = """create table anchor (
        aid int auto_increment primary key, 
        name varchar(100), 
        uin varchar(100),
        intr varchar(255),
        vnum int(10) default 0,
        page int(10) default 1,

        fromUserId int(10),
        platform varchar(20)
        )"""
    db.createTable(table, sql)

# videos
def createTableVideos():
    db = dbHelper.database()
    table = 'videos'
    sql = """CREATE TABLE videos (
                id int auto_increment primary key,
                qq varchar(20),
                title varchar(255), 
                url varchar(255), 
                alias varchar(255), 
                tags varchar(255), 
                first_class varchar(10),
                second_class varchar(10),
                platform_create_time varchar(50), 
                create_time DATETIME, 
                publish_time DATETIME, 
                aid varchar(100),
                vid varchar(50),
                pic varchar(255),
                is_exist_local int(1), 
                local_path varchar(255), 
                fromUserId int(10),
                platform varchar(20) )
                """
    res = db.createTable(table, sql)

    if res:
        print('succ')
    else:
        print('fail')

# uploader
def createTableUploader():
    db = dbHelper.database()
    table = 'uploader'
    sql = """CREATE TABLE uploader(
                id int auto_increment primary key,
                account varchar(50),
                pwd varchar(50),
                fromUserId int(10),
                platform varchar(10)，
                ext varchar(255)
                )"""
    res = db.createTable(table, sql)

# 创建用户
def createTableUser():
    db = dbHelper.database()
    table = 'user'
    sql = """CREATE TABLE user(
        userId int auto_increment primary key,
        name varchar(100),
        pwd varchar(100),
        md5pwd varchar(100),
        pic varchar(100)
        )"""
    db.createTable(table, sql)

def fetchUserFromName(name):
    db = dbHelper.database()
    sql = "SELECT * FROM user WHERE name='%s'" % (name)
    res = db.fetchUser(sql)
    return res

def insetUser(name, pwd):
    db = dbHelper.database()
    sql = "INSERT INTO user (name, pwd) values ('%s', '%s')" % (name, pwd)
    flag = db.inset(sql)
    db.close()
    return flag

def fetchAllUser():
    db = dbHelper.database()
    sql = 'select * from kduser'
    res = db.fetch(sql)
    return res

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

def getUploaderWithPlatform(platform):
    dic = addFromUserId({'platform': platform})
    res = selectData('uploader', dic)
    return res

# [ 主播 ]
# 获取主播
def getAnchorFromPlatform(platform):
    db = dbHelper.database()
    sql = "select * from anchor where platform = '%s'" % platform
    sql = getfetchSqlVerifyLogin(sql)
    print(sql)
    res = db.fetch(sql)
    return res

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
        flag = updateVideo({'platform_create_time': dic[platform_create_time]}, existDic)
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
    res = selectData('videos', dic, other, limit)
    return res


# 获得数据库所有的视频
def getAllVideo(limit=[]):
    dic = addFromUserId()
    res = selectData('videos', dic, limit=limit)
    return res

# 今天采集的
def getTodayVideo(limit=[]):
    other = " and create_time >= date_format(NOW(),'%Y-%m-%d')"
    res = getVideo(other=other, limit=limit)
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
def selectData(table, dic={}, other='', limit=[]):
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
    res = selectData(table, conditionDic)
    if len(res) > 0:
        return True
    else:
        return False

def addFromUserId(conditionDic={}):
    if not 'fromUserId' in conditionDic.keys():
        conditionDic['fromUserId'] = gfunc.getUserId()
    return conditionDic

def checkLogin():
    return gfunc.isLogin()
    


# 查询sql 验证登陆
def getfetchSqlVerifyLogin(sql, limit=None):
    # TODO 登录
    login = gfunc.getLoginNameForLocal()
    # print(login)
    isLogin = login[0]
    name = login[1]
    userId = login[2]
    extSql = ''
    if isLogin:
        if sql.find('where') != -1 or sql.find('WHERE') != -1:
            extSql = " and fromUserId = '%s'" % (userId)
        else:
            extSql = " where fromUserId = '%s'" % (userId)

    if limit != None:
        extSql = extSql + "limit 0,%d" % int(limit)

    if len(extSql) == 0:
        return ''
    return sql+extSql

# TODO 特殊
def updateAllFromUserId():
    db = dbHelper.database()
    db.update("update kduser set fromUserId = '1'")
    db.update("update videos set fromUserId = '1'")
    db.update("update anchor set fromUserId = '1'")

def main():    
    createTableUser()
    createTableUploader()
    createTableAnchor()
    createTableVideos()

if __name__ == '__main__':
    main()
