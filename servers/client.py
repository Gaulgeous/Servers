import socket
import time

from constants import *

    # while True:
        
    #     # By convention, the client starts the conversation by sending in requests
    #     # TODO implement flushing
    #     # TODO implement message length during send and rcv functions
    #     client_socket.setblocking(False)
    #     message = client_socket.recv(MESSAGE_LENGTH).decode()
    #     print(message)


    # TODO Implement handling of closing of connections


class Client:

    def __init__(self, port):
        self.port = port
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Might have to keep this one blanked out until we figure out how to use it
        # Plus it might not even be necessary for our intents and purposes
        # self.socket.setblocking(False)

        self.socket.connect((HOST, port))


    def send_message(self, message):

        message = message.encode('utf-8')
        self.socket.send(message)

        # total_sent = 0
        # while total_sent < MESSAGE_LENGTH:
        #     sent = self.socket.send(message[total_sent:])
        #     if sent == 0:
        #         raise RuntimeError("socket connection broken")
        #     total_sent = total_sent + sent


if __name__=="__main__":
    client = Client(port=5000)

    start = time.time()

    while True:
        now = time.time()

        if now - start >= TEST_INTERVAL:
            print("Sending message")
            client.send_message("Hello")
            start = now