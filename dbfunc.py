
from DBHelper import dbHelper

def createTable():
    db = dbHelper.database()
    table = 'videos'
    sql = """CREATE TABLE videos (
                id int auto_increment primary key,
                qq CHAR(20),
                title CHAR(255), 
                url CHAR(255), 
                alias CHAR(255), 
                tags CHAR(255), 
                first_class CHAR(10),
                second_class CHAR(10),
                is_exist_local int(1), 
                local_path CHAR(255), 
                qq_create_time CHAR(50), 
                create_time DATETIME, 
                publish_time DATETIME, 
                other char(255), 
                extension char(255)
                vid char(255) )"""    
    res = db.createTable(table, sql)

    if res:
        print('succ')
    else:
        print('fail')

def insertVideo(qq, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time, vid):
    db = dbHelper.database()
    sql = "select * from videos where vid = '%s'" % vid    
    dd = db.fetch(sql) 
    if dd:
        print('videos 表中已存在了')
        # 更新时间 qq_create_time
        sql = "update videos set qq_create_time = '%s' where vid = '%s'" % (qq_create_time, vid)
        db.update(sql)
        db.close()
    else:
        sql = "INSERT INTO videos (qq, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time, vid) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s','%d', '%s', '%s', '%s', '%s') " % (qq, title, url, alias, tags, first_class, second_class, int(is_exist_local), local_path, qq_create_time, create_time, vid )
        db.update(sql)
        db.close()
        print('inset')
    

def updateVideo(id, data):
    db = dbHelper.database()
    arrKey = data.keys()

    valueStr = ''
    for key in arrKey:
        item = key + ' = ' + "'" +data[key] + "'"
        if valueStr == '':
            valueStr = item
        else:
            valueStr = valueStr + ', ' + item
    sql = "update videos set %s where id = '%d'" % (valueStr, int(id))
    print(sql)
    db.update(sql)
    db.close()

def fetchVideo(qq):
    db = dbHelper.database()
    sql = "SELECT * FROM videos WHERE qq = '%s' AND publish_time is null" % qq
    res = db.fetch(sql)
    print(len(res))
    return res

def main():
    createTable()

if __name__ == '__main__':
    main()
