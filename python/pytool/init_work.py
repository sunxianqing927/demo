import os
import shutil
import sys
from get_bin_files import *

use_info='1:copy src/'+project_name+"""/config  and testdata'
2:src/depends
3:MakeSoLinkTool
4:create_poto_cpp
5:get_bin_file
6:reset_debug_server
7:reset_release_server
"""

def copytree(src,des):
    if os.path.exists(des):
        shutil.rmtree(des)
    shutil.copytree(src,des)

def copytree_check(src,des):
    if os.path.exists(des):
        return
    shutil.copytree(src,des)

def create_poto_cpp():
    print(os.path.abspath('.'))
    work_path=src+'/proto'
    protocsvr_sh=work_path+'/protocsvr.sh'
    protoc=work_path+'/../depends/protobuf/bin/protoc'

    os.chdir(work_path)
    print(os.path.abspath('.'))
    os.system('chmod +x '+protocsvr_sh)
    os.system('dos2unix ' +protocsvr_sh)
    os.system('chmod +x ' +protoc)
    os.system('source '+protocsvr_sh)
    print(os.path.abspath('.'))


if len(sys.argv)==1:
   print(use_info)
   exit(0)

for x in range(1,len(sys.argv)):
    if sys.argv[x]=='1':
        #testbin=src+r'/'+project_name+'/src/testtool/testdata/bin/*'
        copytree( src+r'/'+project_name+'/config',loc_debug_dir+r'/config')
        copytree( src+r'/'+project_name+'/config',loc_release_dir+r'/config')
        #os.system('dos2unix -q '+testbin)
        #os.system('mkdir -p '+loc_debug_dir+'/bin/param'+' && cp '+ testbin+' '+loc_debug_dir+'/bin/param')
        #os.system('mkdir -p '+loc_release_dir+'/bin/param'+' && cp '+ testbin+' '+loc_release_dir+'/bin/param')
    elif sys.argv[x]=='2':pass


    elif sys.argv[x]=='3':
        os.system('python3 MakeSoLinkTool.py')
        create_poto_cpp()
        print(os.path.abspath('.'))
    elif sys.argv[x]=='4':
        create_poto_cpp()
    elif sys.argv[x]=='5':
        get_bin_file()
    elif sys.argv[x]=='6':
        reset_debug_server()
    elif sys.argv[x]=='7':
        reset_release_server()
    else:
        print(x ,' is invalid',use_info)
        exit(0)

print('finish ') 
