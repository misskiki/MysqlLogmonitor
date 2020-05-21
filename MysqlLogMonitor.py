import os
import time
import pymysql,json
__author__="misskiki"
def MysqlContent(user,password,port,dbname,host):
    try:
        conn = pymysql.connect(
            host = host,
            user = user,
            password = password,
            db = "mysql",
            charset = "utf8" 
        )
    except Exception as e:
        print("数据库链接失败")
    else:
        cursor = conn.cursor()
        sql = "show variables like '%general%'"
        cursor.execute(sql)
        row = cursor.fetchall()
        conn.commit()
        for i in row:
            if "OFF" in i:
                onsql = "SET GLOBAL general_log = 'On'"
                cursor.execute(onsql)
                path = os.getcwd()
                logfile = path + "/mysql_log" #if windows "//" or liunx "/"
                logfile = logfile.replace("\\","//")
                cursor.execute("SET GLOBAL general_log_file = '{}'".format(logfile))
                conn.commit()
                MysqlMonitor(logfile)
                break
            if "ON" in i:
                path = os.getcwd()
                logfile = path + "/mysql_log" #if windows "//" or liunx "/"
                logfile = logfile.replace("\\","//")
                print(logfile)
                cursor.execute("SET GLOBAL general_log_file = '{}'".format(logfile))
                conn.commit()
                MysqlMonitor(logfile)
                break

def MysqlMonitor(path):
    pos = 0
    while True:
        fd = open(path,"r",encoding='utf8')
        if pos != 0:
            fd.seek(pos,0)
        while True:
            line = fd.read()
            if line.strip():
                print(line.strip())
            pos = pos + len(line)
            if not line.strip():
                break
    fd.close()
if __name__ == "__main__":
    with open("mysql_config.ini","r") as f:
        MysqlIni = json.loads(f.read())
        MysqlContent(MysqlIni["name"],MysqlIni["pass"],MysqlIni["port"],MysqlIni["dbname"],MysqlIni["host"])