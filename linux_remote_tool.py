import shutil
import paramiko
import os

#shutil.copyfile(src_file_full_name, file_name)
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
            self.sftp.get(from_file, to_file) if gp == "get" else  sftp.put(from_file, to_file)
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
        return (False,res) if len(res) else (True,list(stdout.readlines()))
        
    def Close(self):
        if not self.state:
            return 
        self.ssh.close()

class RemoteTool:
    def __init__(self,sftp,ssh_cmd):
        self.sftp=sftp
        self.ssh_cmd=ssh_cmd

class RemoteToolMgr:
    usr_infos=dict(default_name=UsrInfo('127.0.0.1',22,'sunny','123456'))
    data={}
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

default_name=RemoteToolMgr.GetDefaultUsr('default_name')
src='123'
src1='123'
des='123'

default_name.sftp.SftpGet(src,des)
default_name.sftp.SftpGet(src,'HH/gateway')
default_name.sftp.SftpGet(src,'HH1/gateway')
print(dwzq.ssh_cmd.Exec_Commend('ls'))
print(dwzq.ssh_cmd.Exec_Commend('ll'))


#os.popen('')
#import os
#f=os.popen('./cpfile.sh')
#print(f.read())  