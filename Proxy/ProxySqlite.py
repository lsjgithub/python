import sqlite3
import time
import xiaoshu_proxy_grab

DatabasePath = "proxyList.db"

def ShowRecord(type, ipAddr, port, useable, delayTime, createTime):
    print("socket type:%s, ip:%s:%s useable:%d delay:%d createTime:%s" % 
          (type, ipAddr, port, useable, delayTime, createTime))

def CreateTable():
    dbconnect = sqlite3.connect(DatabasePath)
    cursor = dbconnect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS PROXYLIST
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TYPE VARCHAR(32) NOT NULL,
    IPADDRESS VARCHAR(32) NOT NULL,
    PORT INTEGER NOT NULL,
    DELAYTIME INT,
    USEABLE INT DEFAULT 0,
    CREATETIME VARCHAR(32));''')
    dbconnect.commit()
    dbconnect.close()

def InsertProxyRecord(type, ipAddr, port, delayTime, useable):
    type = type.lower()
    dbconnect = sqlite3.connect(DatabasePath)
    cursor = dbconnect.cursor()

    sqlString = "select type from proxyList where type='%s' and ipaddress='%s' and port='%d'" % (type, ipAddr, port)
    cursor.execute(sqlString)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    recordList = cursor.fetchall()
    if len(recordList) == 0:
        cursor.execute("""insert into proxyList (type, ipaddress, port, delayTime, useable, createTime) 
        values('%s', '%s', '%d', '%d', '%d', '%s')""" % (type, ipAddr, port, delayTime, useable, strTime))
        dbconnect.commit()
    elif len(recordList) == 1:
        cursor.execute("""update proxyList set delayTime=%d, useable=%d 
        where type='%s' and ipaddress='%s' and port='%d'""" % (delayTime, useable, type, ipAddr, port))
        dbconnect.commit()

    dbconnect.close()


def DelProxyRecord(type, ipAddr, port):
    type = type.lower()
    dbconnect = sqlite3.connect(DatabasePath)
    cursor = dbconnect.cursor()
    cursor.execute("delete from proxyList where type='%d' and ipAddress='%s' and port='%d'" % (type, ipAddr, port))
    dbconnect.commit()
    dbconnect.close()

def QueryRecord(order, callback):
    dbconnect = sqlite3.connect(DatabasePath)
    cursor = dbconnect.cursor()

    sqlStr = "select * from proxyList "
    if order == "type":
        sqlStr += "order by type"
    elif order == "ipAddress":
        sqlStr += "order by ipAddress"
    elif order == "port":
        sqlStr += "order by port"
    elif order == "delayTime":
        sqlStr += "order by delayTime"
    elif order == "useable":
        sqlStr += "order by useable"
    elif order == "CreateTime":
        sqlStr += "order by CreateTime"
    cursor.execute(sqlStr)

    for row in cursor:
        callback(row[1], row[2], row[3], row[4], row[5], row[6])
    dbconnect.close()

