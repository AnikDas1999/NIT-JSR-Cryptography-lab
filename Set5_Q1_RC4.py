# rc4.py -- pure-Python RC4 implementation (educational)
from typing import Iterator

def ksa(key: bytes) -> list:
    """Key-scheduling algorithm: returns initialized S array (list of 256 ints)."""
    assert len(key) > 0
    S = list(range(256))
    j = 0
    key_len = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) & 0xFF
        S[i], S[j] = S[j], S[i]
    return S

def prga(S: list) -> Iterator[int]:
    """Pseudo-random generation algorithm: yields keystream bytes one by one."""
    i = 0
    j = 0
    while True:
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) & 0xFF]
        yield K

def rc4_crypt(key: bytes, data: bytes) -> bytes:
    """
    Encrypt or decrypt `data` with RC4 using `key`.
    Returns bytes of the same length as data.
    """
    S = ksa(key.copy() if isinstance(key, bytearray) else key)
    keystream = prga(S)
    return bytes([b ^ next(keystream) for b in data])

# ---- convenience helpers ------------------------------------------------
def str_to_bytes(s: str, encoding: str = "utf-8") -> bytes:
    return s.encode(encoding)

def bytes_to_hex(b: bytes) -> str:
    return b.hex()

def hex_to_bytes(h: str) -> bytes:
    return bytes.fromhex(h)

# ---- self-test / example ------------------------------------------------
if __name__ == "__main__":
    # Example usage
    key_text = "supersecret"
    plaintext_text = "Hello, RC4! This is a test."

    key = str_to_bytes(key_text)
    pt = str_to_bytes(plaintext_text)

    ct = rc4_crypt(key, pt)           # encrypt
    recovered = rc4_crypt(key, ct)    # decrypt (same function)

    print("Key         :", key_text)
    print("Plaintext   :", plaintext_text)
    print("Ciphertext (hex):", bytes_to_hex(ct))
    print("Recovered   :", recovered.decode("utf-8"))
    assert recovered == pt, "RC4 decrypt failed!"
