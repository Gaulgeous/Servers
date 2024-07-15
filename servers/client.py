import socket
import sys
import time
from random import randint

from constants import *
from encryptions import *
from coms import *
from blocks import *



class Client:

    def __init__(self, port: int, name: str, wallet: int) -> Self:
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
        self.send_handshake()
        self.mainloop()


    def mainloop(self) -> None:

        start = time.time()

        while True:
            now = time.time()

            try:
                read_ready, write_ready, error_ready = select.select([self.socket], [self.socket], [])
            except select.error:
                print("Error in select function from the select package")
                break
            except socket.error:
                print("Error in select function from socket package")
                break

            if len(read_ready) > 0:
                self.receive_message()

            if now - start >= TEST_INTERVAL and len(write_ready) > 0:
                self.send_transaction()
                start = now


    def update_chain(self, chain: Chain) -> None:
        new_length = chain.return_length()
        existing_length = self.chain.return_length()

        if new_length > existing_length:
            self.chain = chain


    def add_address(self, address: str) -> None:
        if address not in self.address_book:
            self.address_book.append(address)


    def remove_address(self, address: str) -> None:
        if address in self.address_book:
            self.address_book.remove(address)


    def send_transaction(self) -> None:
        if len(self.address_book) > 0:
            recipient_index = randint(0, len(self.address_book) - 1)
            recipient = self.address_book[recipient_index]
            amount = min(self.wallet, randint(1, 100))
            self.wallet -= amount
            message = ",".join([self.name, recipient, str(amount)])
            send_data(message, TRANSACTION, self.sequence_number, self.socket)
            self.sequence_number += 1


    def receive_message(self) -> None:
        message, message_type, sequence_number = receive_data(self.socket)
        self.sequence_number = sequence_number

        if message_type == BLOCK:
            blockchain = blockchain_from_text(message)
            blockchain.print_chain()
            self.update_chain(blockchain)
        elif message_type == ADD_ADDRESS:
            self.add_address(message)
        elif message_type == REMOVE_ADDRESS:
            self.remove_address(message)
        elif message_type == RECEIVED:
            print("Message sent and received successfully")

        if message_type != RECEIVED:
            send_data("RECEIVED", RECEIVED, sequence_number, self.socket)


    def send_handshake(self) -> None:
        
        message = ",".join([self.name, self.private_key.exportKey().decode('utf-8'), self.public_key.exportKey().decode('utf-8')])
        send_data(message, HANDSHAKE, self.sequence_number, self.socket)
        self.sequence_number += 1

   
if __name__=="__main__":

    arguments = sys.argv
    name = arguments[1]

    client = Client(port=5000, name=name, wallet=randint(100, 1000))
    