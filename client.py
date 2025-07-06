import socket
from protocol import *
import os


c: socket.socket = socket.socket()

c.connect(("127.0.0.1" , PORT))

while(True):

    data_from_server: bytes = get_response_in_bytes(c)

    if data_from_server.startswith(f"{STARTING_DOWNLOAD_MESSAGE}".encode()):
        content: bytes = data_from_server[len(f"{STARTING_DOWNLOAD_MESSAGE}".encode()):]
        new_file_path: str = input("Enter a path to the new file\n")

        with open(new_file_path , "wb") as file:
            file.write(content)
            
        break

    else:

        data: str = data_from_server.decode("utf-8")

        print(data)
        
        if data == END_CONNECTION_MESSAGE :
            print("connection ended")
            break

        if data == SEND_FILE_MESSAGE: 
            path: str = input("Write the path to the file you want to upload\n")

            while not os.path.exists(fr"{path}"):
                path = input("Couldn't find that file . Try again!")

            send_bytes(get_file(path) , c) 
        else:

            user_input: str = input()
            send_data(user_input , c)



