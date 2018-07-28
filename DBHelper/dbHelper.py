
from DBHelper import mod_config
import pymysql


#读取配置文件
DB = "database"    #数据库配置
DBNAME = mod_config.getConfig(DB, 'dbname')
DBHOST = mod_config.getConfig(DB, 'dbhost')
DBUSER = mod_config.getConfig(DB, 'dbuser')
DBPWD = mod_config.getConfig(DB, 'dbpassword')
DBCHARSET = mod_config.getConfig(DB, 'dbcharset')
DBPORT = mod_config.getConfig(DB, "dbport")

# 创建DB
def createDB(isNew=None):
    name = mod_config.getConfig(DB, 'dbname')
    host = mod_config.getConfig(DB, 'dbhost')
    user = mod_config.getConfig(DB, 'dbuser')

    pw = mod_config.getConfig(DB, 'dbpassword')
    charset = mod_config.getConfig(DB, 'dbcharset')
    try:
        db = pymysql.connect(host, user, pw, charset=charset)
        cursor = db.cursor()
        cursor.execute('show databases')
        rows = cursor.fetchall()
        for row in rows:
            tmp = "%2s" % row
            print(tmp)
            if name == tmp:
                if isNew == True:
                    cursor.execute('drop database if exists ' + name) 

        cursor.execute('create database if not exists ' + name)
        db.commit()
        return True   
    except Exception as e:
        print('create db error: '+str(e))
        return False

class database:
    def __init__(self, dbname=None, dbhost=None):
        if dbname is None:
            self._dbname = DBNAME
        else:
            self._dbname = dbname
        if dbhost is None:
            self._dbhost = DBHOST
        else:
            self._dbhost = dbhost

        self._dbuser = DBUSER
        self._dbpassword = DBPWD
        self._dbcharset = DBCHARSET
        self._dbport = DBPORT

        self._conn = self.connectMySQL()

        if (self._conn) :
            self._cursor = self._conn.cursor()

    # 连接
    def connectMySQL(self):
        conn = False
        try:
            conn = pymysql.connect(host=self._dbhost, 
                    user=self._dbuser,
                    passwd=self._dbpassword, 
                    db=self._dbname,
                    charset=self._dbcharset)
        except Exception as e:
            conn = False
        return conn

    def createTable(self, table, sql):
        flag = False
        if self._conn:
            try:
                # 如果表存在则删除
                self._cursor.execute('drop table if exists '+ table)
                self._cursor.execute(sql)
                flag = True
            except Exception as e:
                print(e)
                flag = False
        return flag
            
    # 查询
    def fetch(self, sql):
        res = ''
        if (self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchall()
            except Exception as e:
                res = False
        return res

    # 更新
    def update(self, sql):
        flag = False
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception as e:
                print('update fail: '+ e)
                flag = False
        return flag

    def close(self):
        if (self._conn):
            try:
                if (type(self._cursor) == 'object'):
                    self._cursor.close()
                if (type(self._conn) == 'object'):
                    self._conn.close()
            except Exception as e:
                pass


def main():
    createDB()

if __name__ == '__main__':
    main()