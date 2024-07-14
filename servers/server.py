import socket
import signal
import select
import sys

from Crypto.PublicKey import RSA

from constants import *
from encryptions import *
from blocks import *
from coms import *


# TODO implement encryption during message sending

    
class Server:

    def __init__(self, port, backlog=5):

        self.clients = 0
        self.transaction_number = 0
        self.client_map = {}
        # Output socket list for clients to write to
        self.write_clients = []
        # Create a buffer for writing transactions to before they're converted to blocks
        self.transaction_buffer = []
        # The head source of blockchain to refer to
        self.blockchain = Chain()

        # AF = Address family, SOCK_STREAM = stream type socket (Datagram being the other option)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # This allows you to reuse an address that is already in use. Comes in handy in the case that a server crashes
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # TODO set this up to be the actual address you want to use
        # Binds to the given internet host
        # If you had used localhost, it would bind locally to the machine
        # Using '' makes the socket connect to any address the machine happens to have (So it becomes unspecified)
        # Then you just specify whichever port (3000 is commonly used in web dev, 80 is the specified internet port (Don't use it))
        # Always use port > 1024
        # 8000 corresponds to localhost
        # Note that client and server don't need to bind to the same port (And really shouldn't)
        self.server.bind((HOST, port))

        # Allows the server to accept connections. CONNECTIONS specifies the maximum number of connections that can be queued, not the number of connections in
        # the server
        self.server.listen(backlog)

        # Signal handler for sigkill, which closes all client connections and the server itself
        signal.signal(signal.SIGINT, self.sighandler)


    def sighandler(self, signum, frame):

        print("Encountered kill signal. Closing server")

        for output in self.write_clients:
            output.shutdown(socket.SHUT_RDWR)
            output.close()

        self.server.close()
        sys.exit()


    def serve(self):

        read_clients = [self.server]

        while True:

            try:
                read_ready, write_ready, error_ready = select.select(read_clients, self.write_clients, [], TIMEOUT)
            except select.error:
                print("Error in select function from the select package")
                break
            except socket.error:
                print("Error in select function from socket package")
                break

            for read_client in read_ready:

                # print(f"Clients in reading list: {read_client}")
                # print(f"Clients in writing list: {write_ready}")

                if read_client == self.server:

                    # When there is a new client ready to join the server
                    # Connection represents the socket connecting to the client -> you can send and receive over that
                    # Address is the address that's bound to the socket on the other end (the client's address)
                    # Note that this is all the server does - just create socket connections to clients. It doesn't send or receive any data.
                    # This created 'client' socket is an equal beast to its true connected client socket -> this is p2p communication
                    client, address = self.server.accept()
                    print(f"Received connection from {address}")

                    # TODO find a way to store the address of the client

                    self.clients += 1
                    read_clients.append(client)
                    self.write_clients.append(client)
                    
                else:

                    self.receive_message(read_client, read_ready, read_clients)

            self.check_transaction_buffer()


    def check_transaction_buffer(self):

        if len(self.transaction_buffer) >= TRANSACTION_BUFFER_LIMIT:
            message = BLOCK_DELIMITER.join(self.transaction_buffer)
            pow, hash = return_proof_of_work(message, NUM_ZEROS)
            block = Block(pow=pow, message=message, next_hash=hash)
            self.blockchain.add_block(block)

            # TODO send the blockchain to everyone
            print("Printing chain")
            print()
            self.blockchain.print_chain()
            self.transaction_buffer = []

                    
    def receive_message(self, read_client, read_ready, read_clients):

        try:
            message, message_type, sequence_number = receive_data(read_client)

            print(f"message_type {message_type}")
            print(f"sequence_number {sequence_number}")
            print(f"message {message}")

            if message_type == HANDSHAKE:
                name, private_key, public_key = message.split(",")
                private_key = RSA.import_key(bytes(private_key, "utf-8"))
                public_key = RSA.import_key(bytes(public_key, "utf-8"))
                client_details = {"name": name, "socket": read_client, "private_key": private_key, 
                                  "sequence_number": sequence_number, "public_key": public_key}
                self.client_map[name] = client_details

                # TODO send the client name to everyone

            elif message_type == TRANSACTION:
                sender, recipient, amount = message.split(',')
                message += f",{str(self.transaction_number)}"
                encoded_transaction = sign(message, self.client_map[sender]["private_key"])
                self.transaction_buffer.append(encoded_transaction)
                self.transaction_number += 1

        except socket.error as e:

            print(f"Client {read_client} disconnected")
            self.clients -= 1
            read_client.shutdown(socket.SHUT_RDWR)
            read_client.close()
            read_clients.remove(read_client)
            self.write_clients.remove(read_client)
            read_ready.remove(read_client)
            self.write_clients.remove(read_client)

        

            # TODO parse message contents
            # TODO send a message to all clients in the server



if __name__=="__main__":

    server = Server(port=5000)
    server.serve()