import os
import chinese_calendar
import json
import datetime
import xml.etree.ElementTree as ET

def __indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            __indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

config=json.load(open("config.json",encoding='utf8'))
def GeneralHolidayFile(holiday_days):
    holiday_info=""
    for holiday_day in holiday_days:
        holiday_info+=holiday_day.strftime("%Y%m%d\n")
    open("calendar/"+"holiday.txt",'w',encoding='utf8').write(holiday_info)

def GeneralHolidayAndWeekendFile(all_days,holiday_days):
    holiday_days=set(holiday_days)
    holiday_weekend_info=""
    for day in all_days:
        if day.isoweekday() in [6,7] or day in holiday_days:
            holiday_weekend_info+=day.strftime("%Y%m%d\n")
    open("calendar/"+"holiday.cfg",'w',encoding='utf8').write(holiday_weekend_info)

def GeneralAllDayFile(all_days,holiday_days):
    holiday_days=set(holiday_days)
    all_info=""
    for day in all_days:
        all_info+=day.strftime("%Y%m%d")+" "+str(day.isoweekday())+" "+("1" if day in holiday_days else "0")+"\n"
    open("calendar/"+"calendar.xml",'w',encoding='utf8').write(all_info)

    
def GeneralAllDayFileXML(all_days,holiday_days):
    holiday_days=set(holiday_days)
    root = ET.Element('tradeCalendar')       # 创建节点
    for day in all_days:
        is_ex_holiday= day.isoweekday() in [6,7] or day in holiday_days
        element = ET.Element('day')
        element.set('date', day.strftime("%Y%m%d"))
        element.set('tradeFlag',("0" if is_ex_holiday else "1") )
        element.set('weekday', str(day.isoweekday()))
        root.append(element)
   
    tree = ET.ElementTree(root)     # 创建文档
    __indent(root)          # 增加换行符
    tree.write('calendar/tradeCalendar.xml', encoding='utf-8', xml_declaration=True)
    
def GeneralWorkAndHolidayFile():
    start_date=datetime.datetime.strptime(config["start"]+"0101","%Y%m%d")
    end_date=datetime.datetime.strptime(config["end"]+"1231","%Y%m%d")
    all_days=chinese_calendar.get_dates(start_date,end_date)
    holiday_days=chinese_calendar.get_holidays(start_date,end_date)
    GeneralAllDayFileXML(all_days,holiday_days)
    GeneralHolidayAndWeekendFile(all_days,holiday_days)

if __name__=="__main__":
    if not os.path.exists("calendar"):
        os.makedirs("calendar")
    GeneralWorkAndHolidayFile()