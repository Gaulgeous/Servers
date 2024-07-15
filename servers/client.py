import socket
import time
from random import randint

from constants import *
from encryptions import *
from coms import *
from blocks import *

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
        self.address_book = []
        self.chain = Chain()
        self.name = name
        self.wallet = wallet
        self.public_key, self.private_key = generate_key_pair()

        self.socket.connect((HOST, port))

        # Might have to keep this one blanked out until we figure out how to use it
        # Plus it might not even be necessary for our intents and purposes
        # self.socket.setblocking(False)


    def update_chain(self, chain):
        new_length = chain.get_length()
        existing_length = self.chain.get_length()

        if new_length > existing_length:
            self.chain = chain


    def add_address(self, address):
        if address not in self.address_book:
            self.address_book.append(address)


    def remove_address(self, address):
        if address in self.address_book:
            self.address_book.remove(address)


    def send_message(self, message, message_type):
        send_data(message, message_type, self.sequence_number, self.socket)
        self.sequence_number += 1


    def send_transaction(self):
        if len(self.address_book) > 0:
            recipient_index = randint(0, len(self.address_book) - 1)
            recipient = self.address_book[recipient_index]
            amount = min(self.wallet, randint(1, 100))
            self.wallet -= amount
            message = ",".join([self.name, recipient, str(amount)])
            send_data(message, TRANSACTION, self.sequence_number, self.socket)
            self.sequence_number += 1


    def receive_message(self):
        message, message_type, sequence_number = receive_data(self.socket)
        self.sequence_number = sequence_number

        if message_type == BLOCK:
            blockchain = blockchain_from_text(message)
            self.update_chain(blockchain)
        elif message_type == ADD_ADDRESS:
            self.add_address(message)
        elif message_type == REMOVE_ADDRESS:
            self.remove_address(message)
        elif message_type == RECEIVED:
            print("Message sent and received successfully")

        if message_type != RECEIVED:
            send_data("RECEIVED", RECEIVED, sequence_number, self.socket)


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

        client.receive_message()

        if now - start >= TEST_INTERVAL:
            client.send_transaction()
            start = now