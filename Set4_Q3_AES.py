# Pure-Python AES-128 (single-block) implementation
# Author: ChatGPT (educational)
from typing import List

SBOX = [
    # 0     1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

INV_SBOX = [0]*256
for i, v in enumerate(SBOX):
    INV_SBOX[v] = i

RCON = [
    0x00,
    0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36,
    # enough for AES-128 (10 rounds)
]

def xtime(a: int) -> int:
    """Multiply by x (i.e., 2) in GF(2^8)"""
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1) & 0xFF

def gmul(a: int, b: int) -> int:
    """Galois field multiplication"""
    res = 0
    for i in range(8):
        if b & 1:
            res ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return res

def sub_word(word: List[int]) -> List[int]:
    return [SBOX[b] for b in word]

def rot_word(word: List[int]) -> List[int]:
    return word[1:] + word[:1]

def key_expansion(key: bytes) -> List[List[int]]:
    """Expand 16-byte key into 11 round keys (AES-128). Each round key = 16 bytes."""
    assert len(key) == 16
    Nk = 4
    Nr = 10
    Nb = 4
    w = [list(key[i:i+4]) for i in range(0, 16, 4)]  # 4 words initially
    for i in range(Nk, Nb*(Nr+1)):
        temp = w[i-1].copy()
        if i % Nk == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= RCON[i//Nk]
        w.append([ (w[i-Nk][j] ^ temp[j]) & 0xFF for j in range(4) ])
    # Convert to round keys: 11 keys * 16 bytes
    round_keys = []
    for r in range(Nr+1):
        rk = []
        for i in range(4):
            rk += w[r*4 + i]
        round_keys.append(rk)
    return round_keys

def add_round_key(state: List[int], round_key: List[int]) -> None:
    for i in range(16):
        state[i] ^= round_key[i]

def sub_bytes(state: List[int]) -> None:
    for i in range(16):
        state[i] = SBOX[state[i]]

def inv_sub_bytes(state: List[int]) -> None:
    for i in range(16):
        state[i] = INV_SBOX[state[i]]

def shift_rows(state: List[int]) -> None:
    # State is column-major. Index mapping: state[col*4 + row]
    tmp = state.copy()
    # row 0: no shift
    # row 1: shift left by 1
    state[1]  = tmp[5]
    state[5]  = tmp[9]
    state[9]  = tmp[13]
    state[13] = tmp[1]
    # row 2: shift left by 2
    state[2]  = tmp[10]
    state[6]  = tmp[14]
    state[10] = tmp[2]
    state[14] = tmp[6]
    # row 3: shift left by 3
    state[3]  = tmp[15]
    state[7]  = tmp[3]
    state[11] = tmp[7]
    state[15] = tmp[11]

def inv_shift_rows(state: List[int]) -> None:
    tmp = state.copy()
    # row 0 no shift
    state[1]  = tmp[13]
    state[5]  = tmp[1]
    state[9]  = tmp[5]
    state[13] = tmp[9]
    state[2]  = tmp[10]
    state[6]  = tmp[14]
    state[10] = tmp[2]
    state[14] = tmp[6]
    state[3]  = tmp[7]
    state[7]  = tmp[11]
    state[11] = tmp[15]
    state[15] = tmp[3]

def mix_single_column(a: List[int]) -> List[int]:
    # Perform MixColumns on one 4-byte column
    # AES mix: [2 3 1 1; 1 2 3 1; 1 1 2 3; 3 1 1 2]
    t = a.copy()
    return [
        (gmul(t[0],2) ^ gmul(t[1],3) ^ t[2] ^ t[3]) & 0xFF,
        (t[0] ^ gmul(t[1],2) ^ gmul(t[2],3) ^ t[3]) & 0xFF,
        (t[0] ^ t[1] ^ gmul(t[2],2) ^ gmul(t[3],3)) & 0xFF,
        (gmul(t[0],3) ^ t[1] ^ t[2] ^ gmul(t[3],2)) & 0xFF,
    ]

def mix_columns(state: List[int]) -> None:
    for c in range(4):
        col = [ state[c*4 + r] for r in range(4) ]
        mc = mix_single_column(col)
        for r in range(4):
            state[c*4 + r] = mc[r]

def inv_mix_single_column(a: List[int]) -> List[int]:
    # Inverse MixColumns uses matrix with 14,11,13,9
    t = a.copy()
    return [
        (gmul(t[0],0x0e) ^ gmul(t[1],0x0b) ^ gmul(t[2],0x0d) ^ gmul(t[3],0x09)) & 0xFF,
        (gmul(t[0],0x09) ^ gmul(t[1],0x0e) ^ gmul(t[2],0x0b) ^ gmul(t[3],0x0d)) & 0xFF,
        (gmul(t[0],0x0d) ^ gmul(t[1],0x09) ^ gmul(t[2],0x0e) ^ gmul(t[3],0x0b)) & 0xFF,
        (gmul(t[0],0x0b) ^ gmul(t[1],0x0d) ^ gmul(t[2],0x09) ^ gmul(t[3],0x0e)) & 0xFF,
    ]

def inv_mix_columns(state: List[int]) -> None:
    for c in range(4):
        col = [ state[c*4 + r] for r in range(4) ]
        mc = inv_mix_single_column(col)
        for r in range(4):
            state[c*4 + r] = mc[r]

def encrypt_block(block: bytes, round_keys: List[List[int]]) -> bytes:
    assert len(block) == 16
    state = list(block)
    add_round_key(state, round_keys[0])
    for r in range(1, 10):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[r])
    # final round
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, round_keys[10])
    return bytes(state)

def decrypt_block(block: bytes, round_keys: List[List[int]]) -> bytes:
    assert len(block) == 16
    state = list(block)
    add_round_key(state, round_keys[10])
    for r in range(9, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, round_keys[r])
        inv_mix_columns(state)
    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, round_keys[0])
    return bytes(state)

# Helpers
def hex_to_bytes(h: str) -> bytes:
    h = h.strip().replace(" ", "")
    return bytes.fromhex(h)

def bytes_to_hex(b: bytes) -> str:
    return b.hex()

# Self-test with known AES-128 test vector
if __name__ == "__main__":
    # FIPS-197 test vector (first AES block)
    key_hex = "2b7e151628aed2a6abf7158809cf4f3c"
    pt_hex  = "6bc1bee22e409f96e93d7e117393172a"
    # expected ciphertext: 3ad77bb40d7a3660a89ecaf32466ef97

    key = hex_to_bytes(key_hex)
    pt  = hex_to_bytes(pt_hex)
    rk = key_expansion(key)
    ct = encrypt_block(pt, rk)
    recovered = decrypt_block(ct, rk)

    print("Key      :", key_hex)
    print("Plaintext:", pt_hex)
    print("Ciphertext:", bytes_to_hex(ct))
    print("Recovered :", bytes_to_hex(recovered))
    # validate
    assert bytes_to_hex(ct) == "3ad77bb40d7a3660a89ecaf32466ef97", "Ciphertext mismatch!"
    assert recovered == pt, "Decryption failed!"
    print("AES-128 single-block test passed.")
