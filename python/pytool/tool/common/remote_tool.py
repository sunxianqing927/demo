import paramiko
import os
import time

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

    def TarSftpGetGZ(self,src,des_dir):
        src_file=os.path.basename(src)
        src_file_tz=src_file+str(time.time())+".tz"
        self.ssh_cmd.Exec_Commend( "tar -czf %s -C %s %s"%(src_file_tz,os.path.dirname(src),src_file))
        self.sftp.SftpGet(src_file_tz,src_file_tz)
        self.ssh_cmd.Exec_Commend( "rm -f " +src_file_tz)

        os.makedirs(des_dir,exist_ok=True)
        os.system("tar -xzf %s -C %s && rm -f %s"%(src_file_tz,des_dir,src_file_tz))

class RemoteToolMgr:
    usr_infos={"default_name":UsrInfo('127.0.0.1',22,'root','123456')}
    data={}

    def SetUsrInfos(connects):
        for connect_info in connects.items():
            RemoteToolMgr.usr_infos[connect_info[0]]=UsrInfo(connect_info[1][0],connect_info[1][1],connect_info[1][2],connect_info[1][3])

    def CreateRemoteTool(ip,port,usr,password):
        RemoteToolMgr.usr_infos[ip]=UsrInfo(ip,port,usr,password)
        return RemoteToolMgr.GetDefaultUsr(ip)

    def GetDefaultUsr(usr_name="default_name"):
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
