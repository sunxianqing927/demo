import threading
from multiprocessing import Process
from http_test import *
import os, time

class MyThread(threading.Thread):
    ret_data={}
    summy={}
    summy_success={}
    summy_failed={}
    except_error={}

    def __init__(self, obj):
        super(MyThread, self).__init__()  # 重构run函数必须要写
        self.obj = obj

    def run(self):
        self.obj.SetupTest()
        MyThread.ret_data[self.ident]=self.obj.ret_data
        MyThread.summy[self.ident]=self.obj.summy
        MyThread.summy_success[self.ident]=self.obj.summy_success
        if self.obj.summy_failed:
            MyThread.except_error[self.ident]=self.obj.summy_failed
        if self.obj.except_error:
            MyThread.except_error[self.ident]=self.obj.except_error

    def SaveTestData(cpu_id):
        bin_dir="bin/"+str(cpu_id)
        if os.path.exists(bin_dir):
            shutil.rmtree(bin_dir)
        os.makedirs(bin_dir)
        json.dump(MyThread.ret_data,open(bin_dir+"/test_res.json",'w',encoding='utf8'),ensure_ascii=False,indent=4)
        json.dump(MyThread.summy,open(bin_dir+"/summy.json",'w',encoding='utf8'),ensure_ascii=False,indent=4)
        json.dump(MyThread.summy_success,open(bin_dir+"/summy_success.json",'w',encoding='utf8'),ensure_ascii=False,indent=4)
        json.dump(MyThread.summy_failed,open(bin_dir+"/summy_failed.json",'w',encoding='utf8'),ensure_ascii=False,indent=4)
        json.dump(MyThread.except_error,open(bin_dir+"/except_error.json",'w',encoding='utf8'),ensure_ascii=False,indent=4)
        MyThread.SaveSummy(bin_dir)

    def SaveSummy(bin_dir):
        times=[]
        for sub_summy in MyThread.summy_success.items():
            for item in sub_summy[1].values():
                for val in item.values():
                    times.append(val[1]/1000)


        local_cnt=0;
        for sub_ret_data in MyThread.ret_data.items():
            for item in sub_ret_data[1].values():
                for val in item.values():
                    local_cnt+=1

        times.sort()
        min_time_10="min:"
        max_time_10="max:"
        for x in times[:100]:
            min_time_10+=str(x)+","
        for x in times[-100:-1]:
            max_time_10+=str(x)+","
         
        with open(bin_dir+"/Summy.txt","w",encoding='utf8') as f:
            for x in [min_time_10,max_time_10,"average value:"+str(sum(times)/len(times)),"total success cnt:"+str(len(times))+"/ all cnt:"+str(local_cnt)]:
                f.write(x+"\n")
#设置测试用的数据文件名字
def MutiWork(cpu_id,cnt):
    url_infos=json.load(open("market_20108.json",encoding='utf8'))
    ts=[]
    for i in range(cnt):
        t=MyThread(HttpTest(url_infos))
        t.start()
        ts.append(t)
 
    for t in ts:
        t.join()

    MyThread.SaveTestData(cpu_id)


if __name__ == "__main__":
    print(os.getcwd())
    MutiWork(1,1)

