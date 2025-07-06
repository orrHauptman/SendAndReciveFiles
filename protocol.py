
import socket
END_OF_HEADER: str = ";"
END_CONNECTION_MESSAGE: str = "Successfully executed !"
SEND_FILE_MESSAGE: str = "Great!\nNow I am ready to receive the file. Please send its contents as raw bytes."
PORT: int = 4422

def get_response(conv_socket: socket.socket) -> str:
    data_received: str = ""

    while END_OF_HEADER not in data_received:
        data_received += conv_socket.recv(1000).decode("utf-8")

    index_of_header: int = data_received.index(END_OF_HEADER)
    bytes_to_received: int = int(data_received[:index_of_header])

    data: str = data_received[index_of_header + 1:]
    bytes_received: int = len(data.encode("utf-8"))

    while bytes_received < bytes_to_received:
        data += conv_socket.recv(1000).decode("utf-8")
        bytes_received = len(data.encode("utf-8"))

    return data

def send_data(data: str ,conv_socket: socket.socket):
    conv_socket.send(f"{len(data.encode('utf-8'))}{END_OF_HEADER}{data}".encode("utf-8"))

# The following methods are used for sending and receiving the context of the files

def get_response_in_bytes(conv_socket: socket.socket) -> bytes:
    data_received: bytes = b""

    while END_OF_HEADER.encode("utf-8") not in data_received:
        data_received += conv_socket.recv(1000)

    index_of_header: int = data_received.index(END_OF_HEADER.encode("utf-8"))
    bytes_to_receive: int = int(data_received[:index_of_header].decode("utf-8"))

    data: bytes = data_received[index_of_header + 1:]
    bytes_received: int = len(data)

    while bytes_received < bytes_to_receive:
        data += conv_socket.recv(1000)
        bytes_received = len(data)

    return data


def send_bytes(data: bytes ,conv_socket:socket.socket) :
    conv_socket.send(f"{len(data)}{END_OF_HEADER}".encode("utf-8") + data)

def get_file(path: str) -> bytes:
    with open(fr"{path}" , "rb") as file:
        return file.read()

