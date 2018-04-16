#Login
import socket, os, sys, threading
from datetime import datetime
t1=datetime.now()
up=[]
isOpen=[]
ips=[]
scanned=[]

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP=s.getsockname()[0]
s.close()
localIP=localIP[:localIP.rindex('.')]

def isUp(start,end,step):
    for x in range(start,end,step):
        ips.append(localIP+'.'+str(x+1))
        if os.system("ping -w 5 -n 1 "+localIP+"."+str(x+1))==0:
            up.append(localIP+"."+str(x+1))

def portScan(start,end,step):
    for x in range(start,end,step):
        scanned.append(up[x])
        try:
            for port in range(22,23):
                sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.settimeout(2)
                result=sock.connect_ex((up[x],port))
                if result==0:
                    isOpen.append(up[x])
                sock.close()
        except KeyboardInterrupt:
            sys.exit()
        except socket.gaierror:
            pass

def makeThreads(numThreads,function,argument):
    try:
        for num in range(numThreads):
            threading.Thread(target=function, args=(num,argument,numThreads)).start()
    except KeyboardInterrupt:
        sys.exit()
        
def threads(numThreads,function,argument):
    activeThreads=threading.activeCount()
    makeThreads(numThreads,function,argument)
    while threading.activeCount()>activeThreads:
        pass

threads(15,isUp,254)
print('Total IPs scanned',len(ips))
print('IPs up',len(up))
print(datetime.now()-t1)
tl=datetime.now()
threads(10,portScan,len(up))
print('IPs scanned for open ports',len(scanned))
print(datetime.now()-t1)

