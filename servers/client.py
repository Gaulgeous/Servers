import socket
import time
from random import randint

from constants import *
from encryptions import *
from coms import *

    # while True:
        
    #     # By convention, the client starts the conversation by sending in requests
    #     # TODO implement message length during send and rcv functions
    #     client_socket.setblocking(False)
    #     message = client_socket.recv(MESSAGE_LENGTH).decode()
    #     print(message)


    # TODO Implement handling of closing of connections


class Client:

    def __init__(self, port, name, wallet):
        self.port = port
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sequence_number = 0
        self.address_book = ["Alice"]
        self.name = name
        self.wallet = wallet
        self.public_key, self.private_key = generate_key_pair()

        # Might have to keep this one blanked out until we figure out how to use it
        # Plus it might not even be necessary for our intents and purposes
        # self.socket.setblocking(False)

        self.socket.connect((HOST, port))


    def send_message(self, message, message_type):
        send_data(message, message_type, self.sequence_number, self.socket)
        self.sequence_number += 1


    def send_transaction(self):
        recipient_index = randint(0, len(self.address_book) - 1)
        recipient = self.address_book[recipient_index]
        amount = min(self.wallet, randint(1, 100))
        self.wallet -= amount
        message = ",".join([self.name, recipient, str(amount)])
        send_data(message, TRANSACTION, self.sequence_number, self.socket)
        self.sequence_number += 1


    def send_handshake(self):
        
        message = ",".join([self.name, self.private_key.exportKey().decode('utf-8'), self.public_key.exportKey().decode('utf-8')])
        send_data(message, HANDSHAKE, self.sequence_number, self.socket)
        self.sequence_number += 1

   
if __name__=="__main__":

    client = Client(port=5000, name="Bob", wallet=randint(100, 1000))
    client.send_handshake()

    start = time.time()

    while True:
        now = time.time()

        if now - start >= TEST_INTERVAL:
            client.send_transaction()
            start = now