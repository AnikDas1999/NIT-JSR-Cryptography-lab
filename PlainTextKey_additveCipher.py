def additive_decrypt(ciphertext: str, key: int) -> str:
    result = ""
    for c in ciphertext:
        if c.isalpha():
            base = ord('A')
            result += chr((ord(c) - base - key) % 26 + base)
        else:
            result += c
    return result

cipher = "UDUCOYIQFFHEQSXYD"

print("Trying all possible keys:\n")
for k in range(26):
    plaintext = additive_decrypt(cipher, k)
    print(f"Key {k:2}: {plaintext}")
