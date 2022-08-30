from multiprocessing import Process
from mul_thread import *
import os, time

#I/0密集型任务
#默认根据机器的内核数量创建python物理线程数量
#根据需要为每个物理线程创建N个虚拟线程，总线程数量等于物理线程数量乘以虚拟线程数量

def work(cpu_id):
   MutiWork(cpu_id,1)#设置虚拟线程数量

if __name__ == "__main__":
    if os.path.exists("bin"):
        shutil.rmtree("bin")
    l = []
    print("本机为", os.cpu_count(), "核 CPU")  
    start = time.time()
    for cpu_id in range(os.cpu_count()):
        p = Process(target=work,args=(cpu_id,))  # 多进程
        l.append(p)
        p.start()
    for p in l:
        p.join()
    stop = time.time()
    print("I/0密集型任务，多进程耗时 %s" % (stop - start))

