import socket
from protocol import *
import os


c: socket.socket = socket.socket()

c.connect(("127.0.0.1" , PORT))

while(True):

    data_from_server: str = get_response(c)

    print(data_from_server)
    
    if data_from_server == END_CONNECTION_MESSAGE :
        print("connection ended")
        break

    if data_from_server == SEND_FILE_MESSAGE: 
        path: str = input("Write the path to the file you want to upload\n")

        while not os.path.exists(fr"{path}"):
            path = input("Couldn't find that file . Try again!")


        file : bytes = get_file(path)

        send_bytes(file , c) 
    else:

        user_input: str = input()
        send_data(user_input , c)



