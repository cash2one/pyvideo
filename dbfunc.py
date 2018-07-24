
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
                qq_create_time DATE, 
                create_time DATETIME, 
                publish_time DATETIME, 
                other char(255), 
                extension char(255) )"""    
    res = db.createTable(table, sql)

    if res:
        print('succ')
    else:
        print('fail')

def insertVideo(qq, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time):
    db = dbHelper.database()
    sql = "INSERT INTO videos (qq, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s','%d', '%s', '%s', '%s') " % (qq, title, url, alias, tags, first_class, second_class, is_exist_local, local_path, qq_create_time, create_time )

    db.update(sql)
    db.close()

def updateVideo(id, data):
    db = dbHelper.database()
    arrKey = data.keys()

    valueStr = ''
    for key in arrKey:
        item = key + ' = ' + data[key]
        if valueStr == '':
            valueStr = item
        else:
            valueStr = valueStr + ', ' + item
    sql = "update videos set %s where id = '%d'" % (valueStr, int(id))
    
    db.update(sql)
    db.close()

def fetchVideo():
    db = dbHelper.database()
    sql = "SELECT * FROM videos WHERE qq = '810359132' AND alias = '23' AND publish_time is null"
    res = db.fetch(sql)
    print(len(res))
    return res

def main():
    createTable()

if __name__ == '__main__':
    main()
