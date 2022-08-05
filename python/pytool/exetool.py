from get_bin_files import *
import re
import os
import shutil
import sys
from xml.etree.ElementTree import parse
        
default_lib_paths=["/lib","/usr/lib","/usr/local/lib","/usr/local"]

TEMPLATE_ROOT_DIR="TEMPLATE_ROOT_DIR"
TEMPLATE_EXE_DIR="TEMPLATE_EXE_DIR"
TEMPLATE_NAME="TEMPLATE_NAME"
remote_tool=None


def InitProject(cfgfile):
    global remote_tool
    root =  parse(cfgfile).getroot()
    remote_tool=RemoteToolMgr.CreateRemoteTool(root.get("ip"),22,root.get("username"),root.get("password"))
    exe=root.get("exe")
    shutil.rmtree(exe,ignore_errors=True)
    os.makedirs(exe, exist_ok=True)
    old_cwd=os.getcwd()
    os.chdir(exe)

    fix_dir=root.find("fix_dir")
    root_dir=fix_dir.get("root_dir")
    exe_dir=fix_dir.get("exe_dir")
    os.makedirs(exe_dir, exist_ok=True)
    
    copys=root.find("copys")
    if copys:
        for copy in copys:
            dirname=os.path.dirname(copy.get("des"))
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
            remote_tool.TarSftpGetGZ(copy.get("src"),copy.get("des"))
    os.system("chmod +x "+exe_dir+"/"+exe)
    os.chdir(old_cwd)
    return root_dir,exe_dir,exe

def GetPid(name):
    file_name = os.path.basename(sys.argv[0])
    cmd="ps aux | grep -w \'"+name+ "\' | grep -v \'grep\|"+file_name+"\' | awk '{print $2}'"
    res=remote_tool.ssh_cmd.Exec_Commend(cmd)
    if not res[0] or not len(res[1]):
        return ""
    return res[1][0]

def readProcMapsInfos(pid):
    print("pid:%s"%pid)
    cmd="cat /proc/"+pid+"/maps"
    maps_items=remote_tool.ssh_cmd.Exec_Commend(cmd)
    if not maps_items[0]:
        return []
    mach=re.compile(r".+/.+\.so[\.\d]*")
    local_libs= set() 
    default_libs= set() 
    for maps_item in maps_items[1]:
        lib_path=re.split("[ ]+",maps_item)[-1]
        if not len(lib_path):
            continue
        for default_lib_path in default_lib_paths:
            if lib_path.startswith(default_lib_path):
               default_libs.add(lib_path)
               break 
        else:
             re_lib_path=mach.search(lib_path)
             if re_lib_path:
                 local_libs.add(re_lib_path.string)
    return local_libs

def FIndFileLink(src_file):
    base_dir = os.path.dirname(src_file)
    base_name = os.path.basename(src_file)
    res=remote_tool.ssh_cmd.Exec_Commend("ls -l "+base_dir)
    if not res[0]:
        print("错误",res[1])
        return []
    links=[]
    for file_info in res[1]:
        file_info_items=re.split("[ ]+",file_info)#[-1].split(" -> ")
        if len(file_info_items) > 2 and file_info_items[-1]==base_name and file_info_items[-2]=="->":
            links.append(file_info_items[-3])
    return links


def CopyRemoteToLocal(lib_dir,src_files):
    if type(src_files) !=list:
        src_files=[src_files]

    old_cwd=os.getcwd()
    os.makedirs(lib_dir, exist_ok=True)
    os.chdir(lib_dir)

    for src_file in src_files:
        base_name=os.path.basename(src_file)
        remote_tool.sftp.SftpGet(src_file,base_name)
        link_files=FIndFileLink(src_file)
        for link_file in link_files:
            os.symlink(base_name, link_file)
    
    os.chdir(old_cwd)

def CreateBatchScript(src_dir,des_dir,server_root_dir,server_exe_dir,sever_name):
    os.makedirs(des_dir, exist_ok=True)
    for root, dirs, file_names in os.walk(src_dir):
        for file_name in file_names:
            txt_data=open(root+"/"+file_name).read().replace(TEMPLATE_ROOT_DIR,server_root_dir).replace(TEMPLATE_EXE_DIR,server_root_dir+"/"+server_exe_dir).replace(TEMPLATE_NAME,sever_name)
            des_file_name=file_name.replace("template",sever_name)
            open(des_dir+"/"+des_file_name,"w").write(txt_data)
    os.system("chmod +x "+des_dir+"/*")

if __name__ == "__main__":
        
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    cfg=sys.argv[1] if len(sys.argv)==2 else "exe.xml"
    root_dir,exe_dir,exe=InitProject(cfg)
    pid=GetPid(exe)
    if not pid:
        print("请先启动程序：",exe)
        exit(1) 

    remote_lib_paths=readProcMapsInfos(pid)
    CopyRemoteToLocal(exe+"/lib",list(remote_lib_paths))
    CreateBatchScript("batch_template",exe+"/batch",root_dir,exe_dir,exe)

