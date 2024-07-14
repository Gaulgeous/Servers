import socket

# Specifies the number of connections that can be backlogged by the server prior to accept()
# Note that this does not specify the number of clients within the server
CONNECTIONS = 5

# Specifies the length of send and recv messages
HEADER_LENGTH = 4

# Maximum size of message allowed to be transmitted at once
BUFFER_SIZE = 1024

# Specifies the length of time to wait prior to timing the client or server out
TIMEOUT = 1

# Specifies the host we want to connect to
HOST = socket.gethostname()

# Specify the waiting time between sending messages during automated testing
TEST_INTERVAL = 2

# TODO implement flushing
# TODO implement message length during send and rcv functions
# Python sends strings. You can calculate their length using the len command
# Your sends should have the architecture:
# message_type | message_length | message 
# Best way is to have two receive functions : The first gets the message type and length, the second keeps looping til it
# This is going to be a bit of a pain to make work. But comms are always like that.
# Achieve flushing by sending an empty byte string. Note that this will also close the connection????