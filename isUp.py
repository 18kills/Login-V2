import socket, os, threading, sys

from datetime import datetime
t1=datetime.now()
up=[]

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP=s.getsockname()[0]
s.close()
localIP=localIP[:localIP.find(".",localIP.find(".")+localIP.find(".",localIP.find("."))+localIP.find(".",localIP.find(".",localIP.find("."))),)]

def isUp(start,end,step):
    for x in range(start,end,step):
        check=os.system("ping -w 5 -n 1 "+localIP+"."+str(x+1))
        if check==0:
            up.append(localIP+"."+str(x+1))

def threads():
    try:
        for numThread in range(4):
            threading.Thread(target=isUp, args=(numThread,255,4)).start()
    except KeyboardInterrupt:
        sys.exit()

activeThreads=threading.activeCount()
threads()
while threading.activeCount()>activeThreads:
    pass

for x in range(len(up)):
    print(up[x])

print(datetime.now()-t1)
