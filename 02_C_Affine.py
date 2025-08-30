def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def encrypt(text, a, b):
    res = ""
    for ch in text.upper():
        if ch.isalpha():
            res += chr(((a * (ord(ch)-65) + b) % 26) + 65)
        else:
            res += ch
    return res

def decrypt(text, a, b):
    res = ""
    inv = mod_inverse(a, 26)
    for ch in text.upper():
        if ch.isalpha():
            res += chr(((inv * ((ord(ch)-65) - b)) % 26) + 65)
        else:
            res += ch
    return res


msg = input("Enter message: ")
a = int(input("Enter key a (coprime with 26): "))
b = int(input("Enter key b: "))

enc = encrypt(msg, a, b)
print("Encrypted:", enc)

dec = decrypt(enc, a, b)
print("Decrypted:", dec)
