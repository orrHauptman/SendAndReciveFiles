import socket
import os
from protocol import *

LISTENING_PAIR: tuple[str , int]  = ("0.0.0.0" , PORT)


def get_action() -> str:

    global conv_socket

    send_data("Please choose what would you like to do :\n Choose 1 for - uploading a file \n Choose 2 for - downloading a file " , conv_socket)
    


    data_received: str = get_response(conv_socket)

    while(data_received != "1" and data_received != "2"):

        send_data("Please choose from the options!" , conv_socket)

        data_received = get_response(conv_socket)


    return data_received


def upload():
    global conv_socket

    send_data("Lets start the uploading process!\nPlease choose a name for your file so you can later download it:\n" , conv_socket)
    file_name: str = get_response(conv_socket)
    existing_files: list[str] = [os.path.basename(path) for path in os.listdir(DATABASE_PATH) ] 


    while(file_name in existing_files ):
        send_data("Name already exist! please choose a different one " , conv_socket)
        file_name = get_response(conv_socket)

    send_data(SEND_FILE_MESSAGE , conv_socket)

    content: bytes = get_response_in_bytes(conv_socket)

    with open(f"{DATABASE_PATH}/{file_name}" , "wb") as file:
        file.write(content)
        send_data(END_CONNECTION_MESSAGE , conv_socket)



def download():

    global conv_socket

    existing_files: str = " , ".join([os.path.basename(path) for path in os.listdir(DATABASE_PATH) ])

    send_data(f"Lets start the downloading process!\nWrite the name of the file you want to download from the following options:\n{existing_files} " ,conv_socket)

    file_path: str =f"{DATABASE_PATH}/{get_response(conv_socket)}"

    while not os.path.exists(file_path) :
        send_data(f"File doesn't exists!\nPlease choose from the following:\n{existing_files}" , conv_socket)
        file_path = f"{DATABASE_PATH}/{get_response(conv_socket)}"

    file_data: bytes = get_file(file_path)

    send_bytes(f"{STARTING_DOWNLOAD_MESSAGE}".encode("utf-8") + file_data , conv_socket)

    #Deleting the file from the database
    os.remove(file_path)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket :

    listening_socket.bind(LISTENING_PAIR)

    listening_socket.listen(1)

    conv_socket , client_pair = listening_socket.accept()
                                                        
    action: str = get_action()

    upload() if action == "1" else download()

