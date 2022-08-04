import paramiko
import time

src='/home/sunny/.vs/project/5e0353be-4a37-41f0-908d-929789c7996c/src'
out='/home/sunny/.vs/project/5e0353be-4a37-41f0-908d-929789c7996c/out'
project_name="exe"
ipname="sunny"
class UsrInfo:
    def __init__(self,ip,port,usr,password):
        self.ip=ip
        self.port=port
        self.usr=usr
        self.password=password

    def __repr__(self):
        return 'ip=%s port =%s usr=%s password=%s'%(self.ip,self.port,self.usr,self.password)

class Sftp:
    def __init__(self,usr_info):
        try:
            self.usr_info=usr_info
            self.transport = paramiko.Transport(self.usr_info.ip, self.usr_info.port)
            self.transport.connect(username=self.usr_info.usr, password=self.usr_info.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.state=True
        except Exception as e:
            self.state=False
            print(e,'Sftp init fail',self.usr_info)

    def Close(self):
        if not self.state:
            return 
        self.transport.close()
          
        #sftp下载文件到本地
    def SftpImpl(self,from_file, to_file, gp):
        if not self.state:
            print('sftp state error, %s %s to %s fail '%(gp, from_file,to_file))
            return False
        try:
            self.sftp.get(from_file, to_file) if gp == "get" else  self.sftp.put(from_file, to_file)
            print('sftp:  %s %s to %s  success'%(gp, from_file,to_file))
            return True
        except Exception as e:
            print('sftp error , %s %s to %s fail '%(gp, from_file,to_file))
            print("Exception:",e,self.usr_info)
            return False

    def SftpGet(self,from_file, to_file,):
        return self.SftpImpl(from_file,to_file,'get')
    
    def SftpPut(self,from_file, to_file):
        return self.SftpImpl(from_file,to_file,'put')

class SshCmd:
    def __init__(self,usr_info):
        try:
            self.usr_info=usr_info
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.usr_info.ip, self.usr_info.port, self.usr_info.usr, self.usr_info.password)
            self.state=True
        except Exception as e:
            self.state=False
            print(e,'SshCmd init fail',self.usr_info)

    def Exec_Commend(self,cmd):
        if not self.state:
            print('SshCmd state error, cmd: excute fail '%(cmd))
            return False
        (stdin,stdout,stderr)=self.ssh.exec_command(cmd)
        res=list(stderr.readlines())
        return (False,res) if len(res) else (True,stdout.read().decode().splitlines())
        
    def Close(self):
        if not self.state:
            return 
        self.ssh.close()

class RemoteTool:
    def __init__(self,sftp,ssh_cmd):
        self.sftp=sftp
        self.ssh_cmd=ssh_cmd

class RemoteToolMgr:
    usr_infos=dict(default_name=UsrInfo('127.0.0.1',22,'root','123456'),
                   sunny=UsrInfo('192.168.222.222',22,'sunny','123456'),
                   )
    data={}
    def CreateRemoteTool(ip,port,usr,password):
        RemoteToolMgr.usr_infos[ip]=UsrInfo(ip,port,usr,password)
        return RemoteToolMgr.GetDefaultUsr(ip)

    def GetDefaultUsr(usr_name):
        usr_info=RemoteToolMgr.usr_infos.get(usr_name)
        if not usr_info:
            print('%s is not default user'%usr_name)
            return
        res=RemoteToolMgr.data.get(usr_name)
        if res:
            return res

        ssh_cmd=SshCmd(usr_info)
        sftp=Sftp(usr_info)
        remote_tool=RemoteTool(sftp,ssh_cmd,)
        RemoteToolMgr.data[usr_name]=remote_tool
        return remote_tool

loc_debug_dir=out+'/build/Linux-GCC-Debug/'+project_name+'/Debug'
loc_bin_dir=loc_debug_dir+'/bin'
loc_his_bin_dir=loc_debug_dir+'/his_bin'
loc_debug_srv=loc_debug_dir+'/'+project_name

loc_release_dir=out+'/build/Linux-GCC-Release/'+project_name+'/Release'
loc_release_srv=loc_release_dir+'/'+project_name

loc_bin_init_cmd='mkdir -p  '+loc_bin_dir+' && mkdir -p '+loc_his_bin_dir+ ' && mv ' +loc_bin_dir+'/* '+loc_his_bin_dir


svr_dir='/root/project/'+project_name
svr_files=svr_dir+'/'+project_name
svr_bin_dir=svr_dir+'/bin'
svr_bin_dir_his=svr_dir+'/his_bin'
svr_log_dir=svr_dir+'/log'
svr_log_dir_his=svr_dir+'/Log_His'

svr_bin_init_cmd='mkdir -p  '+svr_bin_dir+' && mkdir -p '+svr_bin_dir_his+ ' && mv ' +svr_bin_dir+'/* '+svr_bin_dir_his
svr_log_init_cmd='mkdir -p  '+svr_log_dir_his+' && mv ' +svr_log_dir+'/* '+svr_log_dir_his

svr_batch_dir='/root/project/batch'
svr_start_file=svr_batch_dir+'/start_'+project_name+'.sh'
svr_stop_file=svr_batch_dir+'/stop_'+project_name+'.sh'
svr_rm_log=svr_batch_dir+'/stop_'+project_name+'.sh'


def get_bin_file():
    remote=RemoteToolMgr.GetDefaultUsr(ipname)
    sunny=RemoteToolMgr.GetDefaultUsr('sunny')
    sunny.ssh_cmd.Exec_Commend(loc_bin_init_cmd)
    des_files=sunny.ssh_cmd.Exec_Commend('ls '+  loc_bin_dir)
    src_files=remote.ssh_cmd.Exec_Commend('ls '+  svr_bin_dir)

    files=set(src_files[1])-set(des_files[1])
    for x in files:
        remote.sftp.SftpGet(svr_bin_dir+'/'+x,loc_bin_dir+'/'+x)
    print(*files,sep='\n')

def reset_server(srv_file):
    remote=RemoteToolMgr.GetDefaultUsr(ipname)
    res=remote.ssh_cmd.Exec_Commend(svr_bin_init_cmd)
    print(res)
    res=remote.ssh_cmd.Exec_Commend(svr_log_init_cmd)
    print(res)
    res=remote.ssh_cmd.Exec_Commend('sh '+  svr_stop_file)
    print(res)
    time.sleep(2)
    remote.sftp.SftpPut(srv_file,svr_files)
    res=remote.ssh_cmd.Exec_Commend('sh '+  svr_start_file)
    print(res)

def reset_debug_server():
    reset_server(loc_debug_srv)

def reset_release_server():
    reset_server(loc_release_srv)

def rm_server_log():
    remote=RemoteToolMgr.GetDefaultUsr('remote')
    res=remote.ssh_cmd.Exec_Commend('sh '+  svr_stop_file)
    print(res)
    remote.sftp.SftpPut(loc_debug_srv,svr_files)
    res=remote.ssh_cmd.Exec_Commend('sh '+  svr_start_file)
    print(res)
