import requests
import getopt
import sys

f = open("./directory-list-2.3-medium.txt")

ip = ''
port = 0

try:
    opts, args = getopt.getopt(sys.argv[1:],"t:p:h",["target=","port=","help"])
except:
    print("Invalid option")
    exit(0)

for o,a in opts:
    if o in ("-t","--target"):
        ip = a
    elif o in("-p","--port"):
        try:
            port = int(a)
            if port < 0 or port > 65535:
                print("Invalid port number")
                exit()
        except:
            print("Invalid port")
            exit()
    elif o in ("-h","--help"):
        print("Usage:")
        print("python attacker.py -t targetip -p portnumber")
        print("-t or --target : The ip of the target that you want to attack")
        print("-p or --port : The port number of the target that you want to attack")
        print("\npython attacker.py -h")
        print("-h or --help : print this menu")
        exit()
    
if port == 0 and ip == '':
    print("You must specify ip address and port number")
    exit()

# print(ip,port)

print("Found : ")

for i in f.readlines():
    resp = requests.get("http://" + ip + ":" + str(port) + "/" + i.rstrip() + ".php")
    # print(resp.text)
    if resp.status_code != 404:
        print("/" + i.rstrip() + ".php")
    

print("\nFinished Searching")
