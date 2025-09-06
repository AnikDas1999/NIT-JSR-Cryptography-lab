from math import gcd

# find modular inverse of a number under mod 26
def mod_inverse(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def multiplicative_decrypt(ciphertext: str, key: int) -> str:
    inv = mod_inverse(key, 26)
    if inv is None:
        return None
    result = ""
    for c in ciphertext:
        if c.isalpha():
            base = ord('A')
            val = (ord(c) - base)
            dec = (val * inv) % 26
            result += chr(dec + base)
        else:
            result += c
    return result

cipher = "TQKECDIVYIBIVI"

valid_keys = [k for k in range(1, 26) if gcd(k, 26) == 1]

print("Trying all possible keys:\n")
for k in valid_keys:
    plain = multiplicative_decrypt(cipher, k)
    print(f"Key {k:2} (inv={mod_inverse(k)}): {plain}")
