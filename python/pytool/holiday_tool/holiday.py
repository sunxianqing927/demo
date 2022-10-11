from pymysql import *
from holidayfile import *
import os

#使用前请先更新chinese_calendar python 库，获取最近的节假日数据
def ExecuteSQL(conn,sqlcommamds):  # 封装一个读取sql文件中的sql语句，并执行语句的方法
    cs = conn.cursor()
    if  type(sqlcommamds) !=list :
        sqlcommamds=[sqlcommamds]
    total=0
    for sqlcommamd in sqlcommamds:
        try:
             total+= cs.execute(sqlcommamd)  # 执行每个sql语句
        except Exception as msg:
            print("错误信息： ", msg)
            return (False,0)
    conn.commit()
    cs.close()
    return  (True,total)

def ExecuteFromfile(conn,filename):  # 封装一个读取sql文件中的sql语句，并执行语句的方法
    sqlcommamds = open(filename, 'r', encoding='utf-8').read().split(";")[:-1]  
    return ExecuteSQL(conn,sqlcommamds)
 
def UpdateHoliday(con_cfgs,day_infos):
    try:
        for con_cfg  in con_cfgs:
            conn = connect(host=con_cfg["host"], port=con_cfg["port"], database=con_cfg["database"], user=con_cfg["user"],password=con_cfg["password"], charset='utf8')
                
            print('host:%s'%con_cfg["host"])
            #执行建表语句，如果表不存在就建表
            res=ExecuteFromfile(conn,"holiday.sql")
            if res[0]:
                print('sql执行成功:holiday.sql,影响行数%s'%res[1])
            else:
                print('sql执行失败:holiday.sql')
                continue

            query="insert into holiday(date,trade_flag,week_day) values"
            for day_info in day_infos:
                query+="(%s,%s,%s),"%(day_info[0],day_info[1],day_info[2])
                
            query=query[:-1]+" on duplicate key update trade_flag=values(trade_flag),week_day=values(week_day)"
            res=ExecuteSQL(conn,query)
            if res[0]:
                print('更新数据库holiday表成功,影响行数%s\n'%res[1])
            else:
                print('更新数据库holiday表失败\n')
            conn.close()
    except Exception as exception:
        print(exception)

def ReadHolidayInfo(file_name):
    f = open('calendar/tradeCalendar.xml')
    root = ET.parse(f).getroot()
    day_infos=[]
    for child in root:
        day_infos.append((child.get('date'),child.get('tradeFlag'),child.get('weekday')))
    return day_infos

if __name__ == '__main__':
    if not os.path.exists("calendar"):
        os.makedirs("calendar")
	
    GeneralWorkAndHolidayFile()
 
    print('更新数据库holiday表通过tradeCalendar.xml')
    day_infos=ReadHolidayInfo("calendar/tradeCalendar.xml")
    UpdateHoliday(config["connects"],day_infos)