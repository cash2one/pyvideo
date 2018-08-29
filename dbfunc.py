
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
def createBaseTable():
    db = dbHelper.database()
    table = 'anchor'
    sql = """create table anchor (
        aid int auto_increment primary key, 
        name varchar(100), 
        uin varchar(100),
        intr varchar(255),
        vnum int(10),
        page int(10) default 1,
        allpage int(10) default 1,
        fromId int(10),
        ext varchar(255) )"""
    db.createTable(table, sql)

# videos
def createTable():
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
                qq_create_time varchar(50), 
                create_time DATETIME, 
                publish_time DATETIME, 
                aid varchar(100),
                vid varchar(50),
                pic varchar(255),
                is_exist_local int(1), 
                local_path varchar(255), 
                fromId int(10),
                ext varchar(255) )
                """
    res = db.createTable(table, sql)

    if res:
        print('succ')
    else:
        print('fail')

# kduser
def createTablekduser():
    db = dbHelper.database()
    table = 'kduser'
    sql = """CREATE TABLE kduser(
                id int auto_increment primary key,
                qq varchar(50),
                pwd varchar(50),
                fromId int(10),
                ext varchar(255)
                )"""
    res = db.createTable(table, sql)

# 创建用户
def createUser():
    db = dbHelper.database()
    table = 'user'
    sql = """CREATE TABLE user(
        userId int auto_increment primary key,
        name varchar(100),
        pwd varchar(100),
        ext varchar(255)
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

def insetkdUser(qq, pwd, ext):
    # TODO fromUserId
    login = gfunc.getLoginNameForLocal()
    if login[0] == False:
        return False
        
    db = dbHelper.database()
    sql = "insert into kduser (qq, pwd, ext, fromUserId) values ('%s', '%s', '%s', '%s')" % (qq, pwd, ext, login[2])
    flag = db.update(sql)
    db.close()
    return flag

def fetchAllUser():
    db = dbHelper.database()
    sql = 'select * from kduser'
    res = db.fetch(sql)
    return res

# anchor
def insertAnchor(name, uin, intr, vnum):
    # TODO fromUserId
    login = gfunc.getLoginNameForLocal()
    if login[0] == False:
        return False
    db = dbHelper.database()
    sql = "insert into anchor(name, uin, intr, vnum, fromUserId) values ('%s', '%s', '%s', '%d', '%s')" % (name, uin, intr, int(vnum), login[2])
    flag = db.update(sql)
    db.close()
        
    return flag

def fetchAllAnchor():
    db = dbHelper.database()
    sql = 'select * from anchor'
    res = db.fetch(sql)
    return res

def updateAllVideo():
    res = fetchAllVideo()

    for item in res:
        qq = item[1]
        title = item[2]
        alias = item[4]

        tags = item[5]
        
        first_class = item[6]
        second_class = item[7]

        if len(qq) == 0:
            seg_list = gfunc.participle(title)
            tags = ' '.join(seg_list)

            clas = gfunc.classFromTags(tags)
            first_class = clas[0]
            second_class = clas[1]
            qq = clas[2]
        idd = item[0]
        data = {
            'qq': qq,
            'first_class': first_class,
            'second_class': second_class,
            'tags': tags,
        }
        updateVideo(idd, data, 'videos')

# video
def insertVideo(dic):
    # TODO 登录验证
    login = gfunc.getLoginNameForLocal()
    if login[0] == False:
        return False
    vid = dic['vid']
    db = dbHelper.database()
    # 查询vid 是否存在 存在更新qq_create_time 不存在加入
    isExist = db.fetch("select * from videos where vid = '%s'" % vid )
    print('查询 数据库videos中 vid是否存在...')
    if isExist:
        # 更新
        sql = "update videos set qq_create_time = '%s' where vid = '%s'" % (dic['qq_create_time'], vid)
        db.update(sql)
        print('videos table is exist update time')
    else:
        ls = list(dic)
        sql = 'insert %s (' % 'videos' + ','.join(ls) + ') values (' +\
               ','.join(['%({})r'.format(field) for field in ls]) + ');'
        sql = sql % dic

        db.inset(sql)
        print('inset video success')
    # TODO 
    db.close()




# # video
# def insertVideo(qq, aid, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time, vid, pic):
#     # TODO 登录验证
#     login = gfunc.getLoginNameForLocal()
#     if login[0] == False:
#         return False
    
#     db = dbHelper.database()
#     sql = "select * from videos where vid = '%s'" % vid    
#     dd = db.fetch(sql)

#     if dd:

#         sql = "update videos set qq_create_time = '%s' where vid = '%s'" % (qq_create_time, vid)
#         print('videos table is exist update time ')
#         db.update(sql)
#         db.close()
#     else:
#         sql = "INSERT INTO videos (qq, aid, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time, vid, pic, fromUserId) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%d', '%s', '%s', '%s', '%s', '%s', '%s') " % (qq, aid, title, url, alias, tags, first_class, second_class, int(is_exist_local), local_path, qq_create_time, create_time, vid, pic, login[2] )
#         db.inset(sql)
#         db.close()
#         print('inset into success')

def updateVideoQQ(id, qq):
    db = dbHelper.database()
    sql = "update videos set qq = '%s' where id = '%d'" % (qq, int(id))
    print(sql)
    db.update(sql)
    db.close()

# 为空时会更新
def updateVideoFromData(id, data, table=None):
    db = dbHelper.database()
    arrKey = data.keys()
    valueStr = ''
    for key in arrKey:
        item = key + ' = ' + "'" +data[key] + "'"
        if valueStr == '':
            valueStr = item
        else:
            valueStr = valueStr + ', ' + item
    if len(valueStr) > 0:
        sql = "update %s set %s where id = '%d'" % (table, valueStr, int(id))
        print(sql)
        db.update(sql)
    db.close()

# 字段值为空时不会更新
def updateVideo(id, data, table=None):
    db = dbHelper.database()
    arrKey = data.keys()
    valueStr = ''
    for key in arrKey:
        if len(data[key]) != 0:
            item = key + ' = ' + "'" +data[key] + "'"
            if valueStr == '':
                valueStr = item
            else:
                valueStr = valueStr + ', ' + item
    if len(valueStr) > 0:
        sql = "update %s set %s where id = '%d'" % (table, valueStr, int(id))
        print(sql)
        db.update(sql)
    db.close()

# 获得数据库所有的视频
def fetchAllVideo():
    db = dbHelper.database()
    sql = 'select * from videos'
    res = db.fetch(sql)
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

    return res

# TODO 特殊
def updateAllFromId():
    db = dbHelper.database()
    db.update("update kduser set fromUserId = '1'")
    db.update("update videos set fromUserId = '1'")
    db.update("update anchor set fromUserId = '1'")

def main():
    updateAllFromId()
    # createUser()
    # delVideos()
    # fetchVideoFromAlias('3216598385', 'b')
    # updateAllVideo()
    # createTablekduser()
    # createBaseTable()
    # createTable()

if __name__ == '__main__':
    main()
