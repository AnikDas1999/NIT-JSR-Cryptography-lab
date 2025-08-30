def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def encrypt(text, key):
    result = ""
    for ch in text.upper():
        if ch.isalpha():
            result += chr(((ord(ch)-65) * key) % 26 + 65)
        else:
            result += ch
    return result

def decrypt(text, key):
    inv = mod_inverse(key, 26)
    result = ""
    for ch in text.upper():
        if ch.isalpha():
            result += chr(((ord(ch)-65) * inv) % 26 + 65)
        else:
            result += ch
    return result


msg = input("Enter message: ")
k = int(input("Enter key (coprime with 26): "))

enc = encrypt(msg, k)
print("Encrypted:", enc)

dec = decrypt(enc, k)
print("Decrypted:", dec)
