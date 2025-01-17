from scapy.all import *
import sys
import argparse

def finScan(target,startPort,endPort):
    global count
    for port in range(startPort,endPort+1):
        receivedPacket = sr1(IP(dst=target)/TCP(sport=RandShort(),dport=port,flags="F"),timeout=.5,verbose=0)
        if receivedPacket == None:
            # this it the opened port
            count = count + 1
            print("Port %d opened|filtered" % port)
        elif receivedPacket.haslayer(TCP):
            # hexdump(receivedPacket)
            # print("Port %d closed" % port)
            if receivedPacket.getlayer(TCP).flags == 0x14:
                pass
            elif receivedPacket.haslayer(ICMP):
                # print("Port %d filtered" % port)
                if int(receivedPacket.getlayer(ICMP).type) == 3 and int(receivedPacket.getlayer(ICMP).code) in [1,2,3,9,10,13]:
                    pass

count = 0
ip = ''
startPort = 0
endPort = 0

try:
    opts, args = getopt.getopt(sys.argv[1:],"t:hs:e:",["target=","help","startPort=","endPort="])
except:
    print("Invalid option")
    exit(0)

for o,a in opts:
    if o in ("-t","--target"):
        ip = a
    elif o in ("-h","--help"):
        print("Usage:")
        print("python attacker.py -t targetip -p portnumber")
        print("-t or --target : The ip of the target that you want to attack")
        print("-s or --startPort : The starting port number of the target that you want to attack")
        print("-e or --endPort : The end port number of the target that you want to attack")
        print("\npython attacker.py -h")
        print("-h or --help : print this menu")
        exit()
    elif o in ("-s","--startPort"):
        try:
            startPort = int(a)
            if startPort < 1 or startPort > 65535:
                print("Invalid start port number")
                exit()
        except:
            print("Invalid start port")
            exit()
    elif o in ("-e","--endPort"):
        try:
            endPort = int(a)
            if endPort < 1 or endPort > 65535:
                print("Invalid start port number")
        except:
            print("Invalid start port")
            exit()
    
if startPort == 0 or ip == '' or endPort == 0:
    print("You must specify ip address, starting port number and ending port number")
    exit()
    
finScan(ip,startPort,endPort)
print("Finish scanning and found %d open|filtered port" % count)