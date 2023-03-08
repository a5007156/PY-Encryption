from Crypto.Cipher import AES
import base64
import os

def generate_key():
    return os.urandom(32)

def pad_message(message):
    block_size = AES.block_size
    message_length = len(message)
    padding_length = block_size - message_length % block_size
    padding = bytes([padding_length]) * padding_length
    return message + padding

def unpad_message(message):
    padding_length = message[-1]
    return message[:-padding_length]

def generate_iv():
    return os.urandom(AES.block_size)

def encrypt_message(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad_message(message))
    return encrypted

def decrypt_message(encrypted, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    return unpad_message(decrypted)

def encrypt_and_encode_message(message, key):
    iv = generate_iv()
    encrypted = encrypt_message(message.encode(), key, iv)
    combined = iv + encrypted
    encoded = base64.b64encode(combined).decode()
    return encoded

def decode_and_decrypt_message(encoded, key):
    combined = base64.b64decode(encoded.encode())
    iv = combined[:AES.block_size]
    encrypted = combined[AES.block_size:]
    decrypted = decrypt_message(encrypted, key, iv)
    return decrypted.decode()

key = generate_key()
message = "Tecosse <3 python"
encoded = encrypt_and_encode_message(message, key)
decoded = decode_and_decrypt_message(encoded, key)

print(f"Key: {key}")
print(f"Original message: {message}")
print(f"Encoded and encrypted message: {encoded}")
print(f"Decoded and decrypted message: {decoded}")
