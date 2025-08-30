def encrypt(text, key):
    result = ""
    for ch in text.upper():
        if ch.isalpha():
            result += chr((ord(ch) - 65 + key) % 26 + 65)
        else:
            result += ch
    return result

def decrypt(text, key):
    result = ""
    for ch in text.upper():
        if ch.isalpha():
            result += chr((ord(ch) - 65 - key) % 26 + 65)
        else:
            result += ch
    return result


msg = input("Enter message: ")
k = int(input("Enter key: "))

enc = encrypt(msg, k)
print("Encrypted:", enc)

dec = decrypt(enc, k)
print("Decrypted:", dec)
