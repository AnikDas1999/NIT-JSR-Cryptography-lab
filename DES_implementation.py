# pure_des_fixed.py
# Pure-Python DES implementation (ECB). Educational only.
# No external libraries required (uses hashlib from stdlib).

from typing import List
import hashlib

# --- DES tables (standard) ---
IP = [
    58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
    57,49,41,33,25,17, 9,1,59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7
]

IP_INV = [
    40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25
]

E = [
    32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,
    12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,
    24,25,24,25,26,27,28,29,28,29,30,31,32,1
]

P = [
    16,7,20,21,29,12,28,17,
    1,15,23,26,5,18,31,10,
    2,8,24,14,32,27,3,9,
    19,13,30,6,22,11,4,25
]

S_BOX = [
    # S1
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],
    # S2
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],
    # S3
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],
    # S4
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],
    # S5
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],
    # S6
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],
    # S7
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ],
    # S8
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]

PC1 = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

PC2 = [
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

KEY_SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

# --- helper bit utilities ---
def permute(block: int, table: List[int], nbits_out: int) -> int:
    """Permute bits in block using 1-based positions in table.
       Assumes block is aligned as a 64-bit integer (highest bit at position 64)."""
    out = 0
    for pos in table:
        out = (out << 1) | ((block >> (64 - pos)) & 1)
    return out & ((1 << nbits_out) - 1)

def left_rotate(val: int, nbits: int, width: int) -> int:
    return ((val << nbits) & ((1 << width) - 1)) | (val >> (width - nbits))

# --- Key schedule ---
def make_subkeys(key64: int) -> List[int]:
    key56 = permute(key64, PC1, 56)
    C = (key56 >> 28) & ((1 << 28) - 1)
    D = key56 & ((1 << 28) - 1)
    subkeys = []
    for shift in KEY_SHIFTS:
        C = left_rotate(C, shift, 28)
        D = left_rotate(D, shift, 28)
        combined = (C << 28) | D
        # aligned to 64-bit for permute helper (shift left to put bits in high positions)
        subkey = permute(combined << 8, PC2, 48)
        subkeys.append(subkey)
    return subkeys

# --- Feistel (F) ---
def feistel(R: int, subkey: int) -> int:
    expanded = permute(R << 32, E, 48)  # expand 32->48 (aligned)
    x = expanded ^ subkey
    out = 0
    for i in range(8):
        six = (x >> (42 - 6*i)) & 0x3F
        row = ((six >> 5) << 1) | (six & 1)
        col = (six >> 1) & 0xF
        s_val = S_BOX[i][row][col]
        out = (out << 4) | s_val
    return permute(out << 32, P, 32)

# --- Block encrypt/decrypt ---
def des_block_encrypt(block64: int, subkeys: List[int]) -> int:
    permuted = permute(block64, IP, 64)
    L = (permuted >> 32) & 0xFFFFFFFF
    R = permuted & 0xFFFFFFFF
    for k in subkeys:
        L, R = R, L ^ feistel(R, k)
    preout = (R << 32) | L
    return permute(preout, IP_INV, 64)

def des_block_decrypt(block64: int, subkeys: List[int]) -> int:
    return des_block_encrypt(block64, list(reversed(subkeys)))

# --- Padding helpers (PKCS#7/5) ---
def pad_pkcs7(data: bytes, block_size: int = 8) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len] * pad_len)

def unpad_pkcs7(data: bytes) -> bytes:
    if not data:
        return data
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError("Invalid padding")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid padding bytes")
    return data[:-pad_len]

# --- Utils ---
def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, 'big')

def int_to_bytes(i: int, length: int) -> bytes:
    return i.to_bytes(length, 'big')

# --- Key helpers ---
def derive_key8_from_passphrase(passphrase: str) -> bytes:
    # stable 8-byte key derived from passphrase using MD5
    return hashlib.md5(passphrase.encode('utf-8')).digest()[:8]

def normalize_key(key) -> bytes:
    """Accepts bytes or str. Returns exactly 8 bytes."""
    if isinstance(key, str):
        return derive_key8_from_passphrase(key)
    if isinstance(key, bytes):
        if len(key) == 8:
            return key
        if len(key) < 8:
            return key.ljust(8, b'\0')
        return key[:8]
    raise TypeError("Key must be bytes or str")

# --- High-level ECB encrypt/decrypt ---
def des_encrypt_ecb(plaintext: bytes, key) -> bytes:
    key8 = normalize_key(key)
    subkeys = make_subkeys(bytes_to_int(key8))
    padded = pad_pkcs7(plaintext, 8)
    out = bytearray()
    for i in range(0, len(padded), 8):
        block = bytes_to_int(padded[i:i+8])
        cblock = des_block_encrypt(block, subkeys)
        out.extend(int_to_bytes(cblock, 8))
    return bytes(out)

def des_decrypt_ecb(ciphertext: bytes, key) -> bytes:
    key8 = normalize_key(key)
    subkeys = make_subkeys(bytes_to_int(key8))
    if len(ciphertext) % 8 != 0:
        raise ValueError("Ciphertext length must be multiple of 8")
    out = bytearray()
    for i in range(0, len(ciphertext), 8):
        block = bytes_to_int(ciphertext[i:i+8])
        pblock = des_block_decrypt(block, subkeys)
        out.extend(int_to_bytes(pblock, 8))
    return unpad_pkcs7(bytes(out))

# --- Demo / quick test ---
if __name__ == "__main__":
    # Example usages:
    # Option 1: provide a passphrase (str) -> derived to 8 bytes
    key_pass = "my demo pass"
    # Option 2: provide explicit 8-byte key (bytes)
    key_bytes = b"secr_key!"  # exactly 8 bytes; you can use this too

    plaintext = b"Hello DES! This is a demo of DES in pure Python."

    # Using passphrase (string)
    print("Using passphrase -> derived key (hex):", derive_key8_from_passphrase(key_pass).hex())
    ct = des_encrypt_ecb(plaintext, key_pass)
    print("Ciphertext (hex):", ct.hex())
    pt = des_decrypt_ecb(ct, key_pass)
    print("Decrypted (passphrase):", pt)

    # Using explicit bytes key
    print("\nUsing explicit bytes key (hex):", key_bytes.hex())
    ct2 = des_encrypt_ecb(plaintext, key_bytes)
    print("Ciphertext (hex):", ct2.hex())
    pt2 = des_decrypt_ecb(ct2, key_bytes)
    print("Decrypted (bytes key):", pt2)

    assert pt == plaintext and pt2 == plaintext
    print("\nAll tests passed.")
