
from DBHelper import dbHelper
from config import *

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
    print(len(res))
    return res

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
        # 更新时间 qq_create_time
        sql = "update videos set qq_create_time = '%s' where vid = '%s'" % (qq_create_time, vid)
        print('videos table is exist update time '+ sql)

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
        item = key + ' = ' + "'" +data[key] + "'"
        if valueStr == '':
            valueStr = item
        else:
            valueStr = valueStr + ', ' + item
    sql = "update %s set %s where id = '%d'" % (table, valueStr, int(id))
    print(sql)
    db.update(sql)
    db.close()

def fetchVideo(qq):
    db = dbHelper.database()
    sql = "SELECT * FROM videos WHERE qq = '%s' AND publish_time is null" % qq
    res = db.fetch(sql)
    print(len(res))
    return res

def fetchVideoFromAnchor(aid):
    db = dbHelper.database()
    sql = "select * from videos where aid = '%d' and publish_time is null " % int(aid)
    res = db.fetch(sql)
    return res

def main():
    createTablekduser()
    # createBaseTable()
    # createTable()

if __name__ == '__main__':
    main()
