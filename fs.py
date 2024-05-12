#FOR UPLOADING IMAGES TO REMOTE LOCAL SMB SERVER
from dotenv import load_dotenv
import subprocess
import os

import time # for speed tests

load_dotenv()

def mkdirSamba(folder_name:str):
    """Create a Directory on the OptiSafe File Server, folder name may also be an address"""
    command = f"smbclient {os.getenv('FS_SERVER')} --user {os. getenv('FS_USER_PASSWORD')} -c 'mkdir {folder_name} && exit'"
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
        print(f"Folder '{folder_name}' successfully created.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def putSamba(local_file:str, dir_and_name:str):
    """Uploads a File from the local Machine to the OptiSafe File Server
    Works Only of Directory destination already exists"""
    command = f"smbclient {os.getenv('FS_SERVER')} --user {os.getenv('FS_USER_PASSWORD')} -c 'put {local_file} {dir_and_name} && exit'"
    try:
        process = subprocess.Popen(command, shell=True)
        process.wait()
        print(f"File '{dir_and_name}' successfully moved to '{dir_and_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def checkDir(folder:str)->bool:
    """returns True if remote Samba File Server Finds folder tp exist, returns False otherwise"""
    command = f"smbclient {os.getenv('FS_SERVER')} --user {os.getenv('FS_USER_PASSWORD')} -c 'cd  {folder} && exit'"
    try:
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()
        print(str(stdout), str(stderr))

        if 'NT_STATUS_OBJECT_NAME_NOT_FOUND' in str(stdout):
            return False # Directory Not Found
        elif 'NT_STATUS_OBJECT_PATH_NOT_FOUND' in str(stdout):
            return False # Path Not Found
        elif 'NT_STATUS_IO_TIMEOUT' in str(stdout):
            return False # Path Not Found
        else:
            return True # Directory Found
    except Exception as e:
        print(f"Error: {e}")
        return False

# for debugging modules 
if __name__ == '__main__':
   Stime = time.time()
   ## Put Function to test Here
   #putSamba('screenshots/dog.jpg','test1/dog.jpg')
   #checkDir("test3")
   Etime = time.time()
   print(f"Execution time: {Etime-Stime} seconds")
