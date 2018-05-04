# Login-V2
### Windows 10 Version

What this does is pings all the ip addresses of the network you are connected to          
If the ip address is up it is then put into a list of all the ip addresses that are up            
It then scans all of the devices that are up for port 22           
The devices that have port 22 open are then put into a list of all the devices that are up and have port 22 open        
It then takes this list of devices and tries to bruteforce the login for each device        
The usernames and passwords used are taken from the two text files        
If the correct username and password is found it will put the ip address, username, and password into a dictionary        
