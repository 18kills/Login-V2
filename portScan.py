import socket
try:
    for port in range(443,444):
        sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(2)
        result=sock.connect_ex(('8.8.8.8',port))
        if result==0:
            print('yes')
        else:
            print('no')
        sock.close()
except KeyboardInterrupt:
    sys.exit()
except socket.gaierror:
    print('no')
