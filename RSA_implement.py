# Python Program for implementation of RSA Algorithm (with text input)

def power(base, expo, m):
    res = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            res = (res * base) % m
        base = (base * base) % m
        expo = expo // 2
    return res

def modInverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return -1

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generateKeys():
    p = 7919
    q = 1009
    n = p * q
    phi = (p - 1) * (q - 1)
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            break
    d = modInverse(e, phi)
    return e, d, n

def encrypt(m, e, n):
    return power(m, e, n)

def decrypt(c, d, n):
    return power(c, d, n)

# --- Helpers for text conversion ---
def text_to_int(text):
    return int.from_bytes(text.encode(), 'big')

def int_to_text(num):
    return num.to_bytes((num.bit_length() + 7) // 8, 'big').decode()

# Main execution
if __name__ == "__main__":
    e, d, n = generateKeys()
    print(f"Public Key (e, n): ({e}, {n})")
    print(f"Private Key (d, n): ({d}, {n})")

    # Take text input
    message = input("Enter a message: ")

    # Convert text → int
    M = text_to_int(message)

    # Encrypt
    C = encrypt(M, e, n)
    print(f"Encrypted: {C}")

    # Decrypt
    decrypted_int = decrypt(C, d, n)
    decrypted_text = int_to_text(decrypted_int)
    print(f"Decrypted: {decrypted_text}")
