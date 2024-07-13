import socket
import signal
import select
import sys

from constants import *

    
class Server:

    def __init__(self, port, backlog=5):

        self.clients = 0
        # Haven't decided on the best form for this one yet. Don't really know the information to put in it
        self.client_map = {}
        # Output socket list for clients to write to
        self.write_clients = []

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

            # try:
            read_ready, write_ready, error_ready = select.select(read_clients, self.write_clients, [], TIMEOUT)
            # except select.error:
            #     print("Error in select function from the select package")
            #     break
            # except socket.error:
            #     print("Error in select function from socket package")
            #     break

            for read_client in read_ready:

                print(f"Clients in reading list: {read_client}")
                print(f"Clients in writing list: {write_ready}")

                if read_client == self.server:

                    # When there is a new client ready to join the server
                    # Connection represents the socket connecting to the client -> you can send and receive over that
                    # Address is the address that's bound to the socket on the other end (the client's address)
                    # Note that this is all the server does - just create socket connections to clients. It doesn't send or receive any data.
                    # This created 'client' socket is an equal beast to its true connected client socket -> this is p2p communication
                    client, address = self.server.accept()
                    print(f"Received connection from {address}")

                    # TODO Implement function for adding client into the server map
                    client_name = ""

                    self.clients += 1
                    read_clients.append(client)
                    self.client_map[client] = (address, client_name)
                    self.write_clients.append(client)
                    
                else:

                    print("Received a read request from client")

                    try:
                        # TODO Implement receiving function for getting data in
                        data = read_client.recv(MESSAGE_LENGTH).decode('utf-8')
                        print(f"Received data from client {data}")





                        if data:
                            # TODO send a message to all clients in the server
                            message = ""
                            for recipient in write_ready:
                                if recipient != read_client and recipient != self.server:
                                    # TODO send the message here
                                    print("Sending")

                        else:
                            print(f"Client {read_client} disconnected")
                            self.clients -= 1
                            read_client.shutdown(socket.SHUT_RDWR)
                            read_client.close()
                            read_clients.remove(read_client)
                            self.write_clients.remove(read_client)

                            # TODO implement function to alert other clients that this one has left


                    except socket.error as e:
                        read_ready.remove(client)
                        self.write_clients.remove(client)


if __name__=="__main__":

    server = Server(port=5000)
    server.serve()