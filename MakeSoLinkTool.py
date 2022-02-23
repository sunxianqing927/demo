import os

class SoLinkTool:
    def __init__(self):
        self.so_link_infos=[]
        self.root=os.getcwd()
    
    def GetSolinkCmd(self,path,file_name):
        file_path=path+'/'+file_name;
        if '.so' in file_name and os.stat(file_path).st_size<256:
            link_file=open(file_path).readline()
            if os.path.exists(path+'/'+link_file):
                self.so_link_infos.append('cd %s && ln -fs %s %s && cd %s'%(path,link_file,file_name,self.root))
    
    def MakeSoLink(self):
        for root, dirs, files in os.walk('.'):
            for file_name in files:
                self.GetSolinkCmd(root,file_name)

        cmd=''
        for so_link_info in self.so_link_infos:
            print(so_link_info)
            cmd+=so_link_info+' && '

        cmd=cmd.rstrip(' && ')
        os.popen(cmd)

so_link_tool=SoLinkTool()
so_link_tool.MakeSoLink()