import paramiko
import sys
import os

host = "192.168.1.202"                    
port = 2222
transport = paramiko.Transport((host, port))
password = "vrutik"                
username = "vrutik"                
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)
inp = sys.argv[1]
while inp != "q":
    if inp == "1":
        remoteFileName = input("Enter the file name to send: ")
        remotepath = "./docs/" + remoteFileName
        sftp.put(remoteFileName,remotepath)
    elif inp == "2":
        remoteFileName = input("Enter the file name to get: ")
        remotepath = remoteFileName
        sftp.get(remotepath,remoteFileName)
    elif inp == "3":
        remotepath = input("Enter the path to list: ")
        dirs = sftp.listdir(path=remotepath)
        print(dirs)
    inp = input("Enter command number: ")
sftp.close()
transport.close()
