
from DBHelper import dbHelper
from config import *
import random
import gfunc

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
        ext varchar(255) )"""
    db.createTable(table, sql)


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
                ext varchar(255)
                )"""
    res = db.createTable(table, sql)

def insetkdUser():
    # qq pwd ext
    qqarr = pwdDic.keys()
    db = dbHelper.database()
    for qq in qqarr:
        sql = "insert into kduser (qq, pwd, ext) values ('%s', '%s', '%s')" % (qq, pwdDic[qq], '')
        db.update(sql)
    db.close()

def fetchAllUser():
    db = dbHelper.database()
    sql = 'select * from kduser'
    res = db.fetch(sql)
    return res

# anchor
def insertAnchor(name, uin, intr, vnum):
    db = dbHelper.database()
    sql = "insert into anchor(name, uin, intr, vnum) values ('%s', '%s', '%s', '%d')" % (name, uin, intr, int(vnum))
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
def insertVideo(qq, aid, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time, vid, pic):
    db = dbHelper.database()
    sql = "select * from videos where vid = '%s'" % vid    
    dd = db.fetch(sql)

    # exist_name = db.fetch("select * from videos where title = '%s'" % title)
    # if exist_name:
    #     print('exist name')
    # else:
    
    if dd:

        sql = "update videos set qq_create_time = '%s' where vid = '%s'" % (qq_create_time, vid)
        print('videos table is exist update time ')

        db.update(sql)
        db.close()
    else:
        sql = "INSERT INTO videos (qq, aid, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time, vid, pic) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%d', '%s', '%s', '%s', '%s', '%s') " % (qq, aid, title, url, alias, tags, first_class, second_class, int(is_exist_local), local_path, qq_create_time, create_time, vid, pic )
        db.update(sql)
        db.close()
        print('inset into success')
    

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
    day_sql = "AND create_time >= date_format(NOW(),'%Y-%m-%d')"
    
    sql = "SELECT * FROM videos WHERE qq = '%s' AND publish_time is not null %s" % (qq, day_sql)

    res = db.fetch(sql)
    return res

def fetchVideo(qq, day=None, count=None):
    db = dbHelper.database()
    day_sql = ''
    if day != None:
        day_sql = "AND create_time >= date_format(NOW(),'%Y-%m-%d')"
    count_sql = ''
    if count != None:
        count_sql = "limit 0,%d" % int(count)
    
    sql = "SELECT * FROM videos WHERE qq = '%s' AND publish_time is null %s %s" % (qq, day_sql, count_sql)
    res = db.fetch(sql)
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
def main():
    # fetchVideoFromAlias('3216598385', 'b')
    updateAllVideo()
    # createTablekduser()
    # createBaseTable()
    # createTable()

if __name__ == '__main__':
    main()
