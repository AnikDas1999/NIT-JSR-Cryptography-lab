
from Crypto.Cipher import DES # type: ignore
from Crypto.Random import get_random_bytes # type: ignore

# pad message to multiple of 8 bytes (DES block size)
def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

# Key must be 8 bytes
key = get_random_bytes(8)
cipher = DES.new(key, DES.MODE_ECB)

# Input message
msg = "HELLODES"
padded_msg = pad(msg)

# Encrypt
ciphertext = cipher.encrypt(padded_msg.encode('utf-8'))
print("Key:       ", key)
print("Encrypted: ", ciphertext)

# Decrypt
decipher = DES.new(key, DES.MODE_ECB)
decrypted = decipher.decrypt(ciphertext).decode('utf-8').rstrip()
print("Decrypted: ", decrypted)
