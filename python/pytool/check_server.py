# Python实用宝典
# 2021/11/13
from ding_ding_send_msg import *
from get_bin_files import *
from datetime import * 
from time import * 

        
dwzq=RemoteToolMgr.GetDefaultUsr(ipname)

def GetToDayTime(time_str):#%H:%M:%S
    check_date_time_str = datetime.now().strftime("%Y-%m-%d "+time_str)
    return datetime.strptime(check_date_time_str,"%Y-%m-%d %H:%M:%S")

def SendMsgToDingDing(msg):
    dd_token="eae395dc6d4f44b92a49efd9f9c523660f83c15a81cc637d4976f1c3925c1677"
    dd_secret="SEC7504d9bd28509d5fb01659c1eb2c21d0268b57e5fd98cc7eab290ac679ee3122"
    m = Messenger(dd_token,dd_secret)
    return m.send_text(msg)

def GetTodayLogName(log_regex):
    if datetime.today().isoweekday()<6:
        log_regex_cmd = datetime.now().strftime("ls -t "+log_regex+"%Y%m%d* | tail -1")
        log_info=dwzq.ssh_cmd.Exec_Commend(log_regex_cmd)
        if log_info[0] and len(log_info[1]):
            return log_info[1][0]
        return "";


def CheckServerLive(name):
    cmd="ps aux | grep -w '"+name+ "' | grep -v grep | awk '{print $2}'"
    res=dwzq.ssh_cmd.Exec_Commend(cmd)
    return res[0] and len(res[1])


def CheckServersLive():
    check_servers=["servername"]
    for server in check_servers:
        if not CheckServerLive(server):
            SendMsgToDingDing("[WARNING] "+server+" server is not start")


check_time = [GetToDayTime("16:35:00"),GetToDayTime("17:35:00")]
def CheckServer():
    global check_time
    if datetime.now()>check_time[0]:
        log_name=GetTodayLogName("/root/project/exe_name/log/exe_name_");
        if log_name=="":
            SendMsgToDingDing("XXX服务:错误,获取日志文件失败")
            return False
                
        grep_cmd = datetime.now().strftime("grep '%Y-%m-%d.*XXXX'")
        hh=dwzq.ssh_cmd.Exec_Commend("cat "+log_name+" | " +grep_cmd+" | "+ "tail -1" )
        if hh[0] and len(hh[1]):
            SendMsgToDingDing("XXX服务:成功,"+hh[1][0])
            check_time[0]+=timedelta(days=1)
            check_time[1]+=timedelta(days=1)
            return True
        else:
            SendMsgToDingDing("XXX服务:失败")
            if datetime.now()>check_time[1]:
                check_time[0]+=timedelta(days=1)
                check_time[1]+=timedelta(days=1)
            return False

    
daily_hello_times = [GetToDayTime("08:25:00"),GetToDayTime("17:25:00")]

def HelloUser():
    global daily_hello_times
    now=datetime.now()
    for idx in range(len(daily_hello_times)):
        if now>daily_hello_times[idx]:
            SendMsgToDingDing("当前钉钉巡检工具运行正常")
            daily_hello_times[idx]+=timedelta(days=1)

if __name__ == "__main__":
    try:
        while True:
            HelloUser()
            CheckServersLive()
            CheckServer()
            sleep(300)
    except :
        while True:
            SendMsgToDingDing("当前钉钉巡检工具运行错误，请及时检查")
            sleep(3600)

