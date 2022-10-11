import os
import sys
import shutil
import json

sys.path.append("..")
from common.remote_tool import *
from common.MakeSoLinkTool import *

class WorkConfig:
    def __init__(self,work_dir,project_name,config_dir,debug_dir,debug_exe,release_dir,release_exe,protocsvr_sh,protoc):
        self.work_dir=work_dir
        self.project_name=project_name
        self.config_dir=config_dir
        self.debug_dir=debug_dir
        self.debug_exe=debug_exe
        self.release_dir=release_dir
        self.release_exe=release_exe
        self.protocsvr_sh=protocsvr_sh
        self.protoc=protoc

    def create_poto_cpp(self):
        old_work_path=os.getcwd()
        work_path=os.path.abspath(os.path.dirname(self.protocsvr_sh))
        os.chdir(work_path)

        os.system('chmod +x '+self.protocsvr_sh)
        os.system('dos2unix ' +self.protocsvr_sh)
        os.system('chmod +x ' +self.protoc)
        os.system('source '+self.protocsvr_sh)
        os.chdir(old_work_path)

    def InitConfig(self):
        self.InitDebugConfig()
        self.InitReleaseConfig()

    def InitDebugConfig(self):
        shutil.copytree(self.config_dir,self.debug_dir+r'/config',dirs_exist_ok=True)

    def InitReleaseConfig(self):
        shutil.copytree(self.config_dir,self.release_dir+r'/config',dirs_exist_ok=True)

class SvrTool:
    def __init__(self,ipname,svr_root,project_name):
        self.project_name=project_name
        self.svr_root=svr_root
        self.remote_ssh=RemoteToolMgr.GetDefaultUsr(ipname)
        
        test_dir=os.path.expanduser('~/test/')+project_name+'/'
        for dir_name in ['bin','log','bin_bak','log_bak']:
            os.makedirs(test_dir+dir_name,exist_ok=True)

    def make_move_cmd(src_dir,des_dir):
        return 'mkdir -p '+des_dir+ ' && mv ' +src_dir+'/* '+des_dir 
            
    def MoveSvrDirToBak(self,dir_path):
        dir_bak_path=dir_path+"_bak"
        cmd=SvrTool.make_move_cmd(dir_path,dir_bak_path)
        self.remote_ssh.ssh_cmd.Exec_Commend(cmd)

    def GetRemoteSvrDirFiles(self,dir_path,bak=False):
        srv_dir=self.svr_root+'/running/'+self.project_name+'/'+dir_path
        test_dir=os.path.expanduser('~/test/')+self.project_name
        test_cp_dir=test_dir+'/'+dir_path
        os.popen("mv "+test_cp_dir+"/* "+test_cp_dir+"_bak 1>/dev/null 2>&1")
        self.remote_ssh.TarSftpGetGZ(srv_dir,test_dir) 
        if bak:
            self.MoveSvrDirToBak(srv_dir)

    def ResetServer(self,loc_exe):
        svr_tool.GetRemoteSvrDirFiles("log",True)
        svr_tool.GetRemoteSvrDirFiles("bin",True)
        stop_cmd='sh '+  self.svr_root+'/batch/stop_'+self.project_name+'.sh'
        self.remote_ssh.ssh_cmd.Exec_Commend(stop_cmd)
        
        time.sleep(2)
        self.remote_ssh.sftp.SftpPut(loc_exe,  self.svr_root+'/running/'+self.project_name+'/'+self.project_name)
        start_cmd='sh '+  self.svr_root+'/batch/start_'+self.project_name+'.sh'
        res=self.remote_ssh.ssh_cmd.Exec_Commend(start_cmd)
        print(res)

if __name__=="__main__":
    use_info="""
1:copy config
2:pass
3:MakeSoLinkTool
4:create_poto_cpp
5:get_bin_file
6:reset_debug_server
7:reset_release_server
"""

    if len(sys.argv)==1:
       print(use_info)
       exit(0)

    os.chdir(os.path.dirname(__file__))
    config=json.load(open("config.json",encoding='utf8'))
    RemoteToolMgr.SetUsrInfos(config["connects"])
    use_config=config[config["use_config"]]
    
    svr_tool=SvrTool(
        use_config["connect_name"],
        use_config["svr_root"],
        use_config["project_name"])
        
    work_config=WorkConfig(
        use_config["work_dir"],
        use_config["project_name"],
        use_config["config_dir"],
        use_config["debug_dir"],
        use_config["debug_exe"],
        use_config["release_dir"],
        use_config["release_exe"],
        use_config["protocsvr_sh"],
        use_config["protoc"])
        
            
            
    #svr_tool.GetRemoteSvrDirFiles("log")
    #svr_tool.GetRemoteSvrDirFiles("bin")

    #exit(0)
                        
    for x in range(1,len(sys.argv)):
        if sys.argv[x]=='1':
            work_config.InitConfig()
        elif sys.argv[x]=='2':pass
        elif sys.argv[x]=='3':
            so_link_tool=SoLinkTool(use_config["work_dir"])
            so_link_tool.MakeSoLink()
        elif sys.argv[x]=='4':
            work_config.create_poto_cpp()
        elif sys.argv[x]=='5':
            svr_tool.GetRemoteSvrDirFiles("log",True)
            svr_tool.GetRemoteSvrDirFiles("bin",True)
        elif sys.argv[x]=='6':
            svr_tool.ResetServer(use_config["debug_exe"])
        elif sys.argv[x]=='7':
            svr_tool.ResetServer(use_config["release_exe"])
        else:
            print(x ,' is invalid',use_info)
            exit(0)
    
    print('finish ') 
    