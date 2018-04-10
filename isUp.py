import socket
import os
import threading
import sys
up=[]
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP=s.getsockname()[0]
s.close()
localIP=localIP[:localIP.find(".",localIP.find(".")+localIP.find(".",localIP.find("."))+localIP.find(".",localIP.find(".",localIP.find("."))),)]
def isUp(start,end,step):
    for x in range(start,end,step):
        check=os.system("ping -w 5 -n 2 "+localIP+"."+str(x+1))
        if check==0:
            up.append(localIP+"."+str(x+1))
def threads():
    try:
        for numThread in range(4):
            threading.Thread(target=isUp, args=(numThread,20,4)).start()
    except KeyboardInterrupt:
        sys.exit()
try:
    activeThreads=threading.activeCount()
    threads()
    while threading.activeCount()>activeThreads:
        pass
except KeyboardInterrupt:
    sys.exit()
for x in range(len(up)):
    print(up[x])
