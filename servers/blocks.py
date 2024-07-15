from constants import *


def blockchain_from_text(message):

    chain = Chain()

    chunks = message.split(BLOCKCHAIN_DELIMITER)
    for chunk in chunks:
        block = block_from_text(chunk)
        chain.add_block(block)

    return chain


def block_from_text(chunk):

    prev_hash, message, powork, next_hash = chunk.split(BLOCK_DELIMITER)

    if prev_hash == "none":
        prev_hash = None

    if next_hash == "none":
        next_hash = None

    block = Block(prev_hash=prev_hash, message=message, pow=powork, next_hash=next_hash)
    return block


class Block:

    def __init__(self, prev_hash=None, message=None, pow=None, next_hash=None):
        self.prev_hash = prev_hash
        self.message = message
        self.pow = pow
        self.next_hash = next_hash
        self.prev = None
        self.next = None


    def print_values(self):
        print(f"prev_hash {self.prev_hash}")
        print(f"message {self.message}")
        print(f"pow {self.pow}")
        print(f"next_hash {self.next_hash}")
        print()


    def set_pow(self, pow):
        self.pow = pow


    def set_prev_hash(self, prev_hash):
        self.prev_hash = prev_hash


    def set_message(self, message):
        self.message = message


    def get_message(self):
        return self.message
    

    def get_pow(self):
        return self.pow
    

    def get_prev_hash(self):
        return self.prev_hash
    

    def get_next_hash(self):
        return self.next_hash
    

    def set_next(self, next):
        self.next = next


    def get_next(self):
        return self.next
    

    def set_prev(self, prev):
        self.prev = prev


    def get_prev(self):
        return self.prev
    

    def to_text(self):

        prev_hash = "none"
        next_hash = "none"

        if self.prev_hash is not None:
            prev_hash = prev_hash

        if self.next_hash is not None:
            next_hash = next_hash

        text = BLOCK_DELIMITER.join([prev_hash, self.message, self.pow, next_hash])
        return text



class Chain:

    def __init__(self):
        self.head = None


    def find_hash(self, hash):
        next = self.head
        while next.get_next() is not None:
            compare_hash = next.get_pow()
            if compare_hash == hash:
                return next
            next = next.get_next()
        raise ValueError("Could not find hash within Blockchain")


    def add_block(self, block):

        # Set the head if it's an empty blockchain
        if self.head is None:
            self.head = block
            block.set_prev(None)

        # Keep iterating through the blockchain until you can add the next spot in
        else:
            next = self.head
            while next.get_next() is not None:
                next = next.get_next()

            block.set_prev_hash(next.get_next_hash())
            block.set_prev(next)
            next.set_next(block)


    def print_chain(self):
        next = self.head

        while next.get_next() is not None:
            next.print_values()
            next = next.get_next()

        next.print_values()


    def return_length(self):

        links = 1
        head = self.head
        while head.get_next() is not None:
            head = head.get_next()
            links += 1

        return links
    

    def to_text(self):

        head = self.head
        chunks = []

        chunks.append(head.to_text())

        while head.get_next() is not None:
            head = head.get_next()
            chunks.append(head.to_text())

        message = BLOCKCHAIN_DELIMITER.join(chunks)
        return message
    




if __name__=="__main__":
    chain = Chain()
    block_1 = Block()
    block_2 = Block()
    block_3 = Block()

    block_1.set_prev_hash("a")
    block_2.set_prev_hash("b")
    block_3.set_prev_hash("c")

    chain.add_block(block_1)
    chain.add_block(block_2)
    chain.add_block(block_3)

    block = chain.find_hash('b')
    block = chain.find_hash('c')
    block = chain.find_hash('d')
       