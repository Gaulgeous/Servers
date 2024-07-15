from hashlib import sha256
import math
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA


def generate_key_pair():
    public_key = RSA.generate(1024)
    private_key = public_key.publickey()

    return public_key, private_key


def sign(message, private_key):
    message = message.encode('WINDOWS-1252')
    cipher = PKCS1_OAEP.new(key=private_key)
    signature = cipher.encrypt(message)
    return signature


def verify(message, signature, public_key):
    decrypt = PKCS1_OAEP.new(key=public_key)
    decrypted_message = decrypt.decrypt(signature)

    return message == decrypted_message


def return_proof_of_work(message, zero_score=10):
    pow = 0
    zeros = -1

    while True:
        zeros = 0
        digest_message = message + pow.to_bytes(pow.bit_length())
        hash = sha256(digest_message).digest()

        tracker = 0
        while hash[tracker] == 0:
            tracker += 1

        zeros = 8 - (int(math.log(hash[tracker], 2)) + 1) + tracker*8

        if zeros >= zero_score:

            return pow, hash
        
        pow += 1