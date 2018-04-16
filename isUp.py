import socket, os, threading, sys
from datetime import datetime
t1=datetime.now()
up=[]

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP=s.getsockname()[0]
s.close()
localIP=localIP[:localIP.rindex('.')]

def isUp(start,end,step):
    for x in range(start,end,step):
        if os.system("ping -w 5 -n 1 "+localIP+"."+str(x+1))==0:
            up.append(localIP+"."+str(x+1))

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
for x in range(len(up)):
    print(up[x])

print(datetime.now()-t1)
