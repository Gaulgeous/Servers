from constants import *
import select
import errno

def send_data(message, message_type, sequence_number, sock):

    message_length = str(len(message))
    message_type = str(message_type)
    sequence_number = str(sequence_number)

    while len(message_length) < HEADER_LENGTH:
        message_length = "".join(['0', message_length])
    while len(sequence_number) < HEADER_LENGTH:
        sequence_number = "".join(['0', sequence_number])

    header = ",".join([message_length, message_type, sequence_number])

    non_blocking_send(header, sock)
    non_blocking_send(message, sock)


def non_blocking_send(message, sock):

        message_length = len(message)
        total_sent = 0
        while total_sent < message_length:
            try:
                sent = sock.send(message.encode('utf-8'))
                total_sent += sent

                if total_sent < message_length:
                    message = message[sent]

            except socket.error as e:
                if e.errno != errno.EAGAIN:
                    raise e
                print(f'Blocking with {len(message)} remaining')
                select.select([], [sock], [])

            except IndexError as e:
                print(f"Remaining message {len(message)} Sent {sent} Total Sent {total_sent} Message Length {message_length}")


def receive_data(sock):

    # First, receive the length of the following message
    data = sock.recv(TOTAL_HEADER_LENGTH).decode('utf-8')
    message_length, message_type, sequence_number = data.split(",")
    message_length = int(message_length)
    message_type = int(message_type)
    sequence_number = int(sequence_number)

    chunks = []
    characters_received = 0

    while characters_received < message_length:
        chunk = sock.recv(min(message_length-characters_received, BUFFER_SIZE)).decode('utf-8')

        if not chunk:
            raise socket.error

        chunks.append(chunk)
        characters_received += len(chunk)

    data = "".join(chunks)
    message = data.strip()

    return message, message_type, sequence_number
