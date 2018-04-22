import socket, os, sys, threading, random
from datetime import datetime
t1=datetime.now()
isOpen=[]
scanned=[]

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP=s.getsockname()[0]
s.close()
localIP=localIP[:localIP.rindex('.')+1]

def portScan(start,end,step):
    for x in range(start,end,step):
        IP=str(localIP+str(random.randint(1,254)))
        while IP in scanned:
            IP=str(localIP+str(random.randint(1,254)))
        else:
            scanned.append(IP)
        if os.system("ping -w 5 -n 1 "+IP)==0:
            try:
                for port in range(22,23):
                    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result=sock.connect_ex((IP,port))
                    if result==0:
                        isOpen.append(IP)
                    sock.close()
            except KeyboardInterrupt:
                sys.exit()
            except socket.gaierror:
                pass

def threads(numThreads,function,argument):
    activeThreads=threading.activeCount()
    try:
        for num in range(numThreads):
            threading.Thread(target=function, args=(num,argument,numThreads)).start()
    except KeyboardInterrupt:
        sys.exit()
    while threading.activeCount()>activeThreads:
        pass

threads(15,portScan,254)
print(datetime.now()-t1)
print('Total ips scanned',len(scanned))
for x in range(len(isOpen)):
    print(isOpen[x],': 22')
print(len(isOpen),'have ssh open')
