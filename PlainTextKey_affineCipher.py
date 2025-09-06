from math import gcd

# function to compute modular inverse
def mod_inverse(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# affine decryption
def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    inv_a = mod_inverse(a, 26)
    if inv_a is None:
        return None
    result = ""
    for c in ciphertext:
        if c.isalpha():
            base = ord('A')
            val = ord(c) - base
            dec = (inv_a * (val - b)) % 26
            result += chr(dec + base)
        else:
            result += c
    return result

cipher = "RXQMHSJDGGDRVGHJF"

# valid multiplicative keys
valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

print("Trying all Affine cipher keys:\n")
for a in valid_a:
    for b in range(26):
        plain = affine_decrypt(cipher, a, b)
        if plain:
            print(f"a={a:2}, b={b:2} -> {plain}")
