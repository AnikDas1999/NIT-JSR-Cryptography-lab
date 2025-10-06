# pure_py_3des.py -- pure Python 3DES (EDE) implementation, no external libs
# Supports 16- or 24-byte keys (16 -> K1,K2,K1). PKCS#7 padding.

IP = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]

FP = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,
      38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,
      36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,
      34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]

E = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,
     16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

P = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]

PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,
       60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4,27,19,11,3]

PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]

SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

SBOX = [
# S1
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
 0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
 4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
 15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
# S2
[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
 3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
 0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
 13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
# S3
[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
 13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
 13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
 1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
# S4
[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
 13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
 10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
 3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
# S5
[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
 14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
 4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
 11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
# S6
[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
 10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
 9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
 4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
# S7
[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
 13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
 1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
 6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
# S8
[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
 1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
 7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
 2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
]

def _bits_from_bytes(b):
    return [(b[i//8] >> (7 - (i%8))) & 1 for i in range(len(b)*8)]

def _bytes_from_bits(bits):
    out = bytearray(len(bits)//8)
    for i,b in enumerate(bits):
        out[i//8] |= (b & 1) << (7 - (i%8))
    return bytes(out)

def permute(bits, table):
    return [bits[i-1] for i in table]

def left_shift(lst, n):
    return lst[n:] + lst[:n]

def make_subkeys(key64):
    # key64: 8-byte key (parity bits included or ignored)
    bits = _bits_from_bytes(key64)
    # PC1 expects 64->56
    key56 = permute(bits, PC1)
    C, D = key56[:28], key56[28:]
    subkeys = []
    for s in SHIFTS:
        C = left_shift(C, s); D = left_shift(D, s)
        CD = C + D
        subkeys.append(permute(CD, PC2))
    return subkeys  # 16 lists of 48 bits

def f_func(R, K):
    # R: 32-bit list, K: 48-bit list
    ER = permute(R, E)  # 48
    x = [a ^ b for a,b in zip(ER, K)]
    out = []
    for i in range(8):
        block6 = x[i*6:(i+1)*6]
        row = (block6[0]<<1) | block6[5]
        col = (block6[1]<<3) | (block6[2]<<2) | (block6[3]<<1) | block6[4]
        val = SBOX[i][row*16 + col]
        out += [(val >> (3-j)) & 1 for j in range(4)]
    return permute(out, P)

def des_block(block8, subkeys, encrypt=True):
    bits = _bits_from_bytes(block8)
    bits = permute(bits, IP)
    L, R = bits[:32], bits[32:]
    k_iter = subkeys if encrypt else list(reversed(subkeys))
    for K in k_iter:
        T = f_func(R, K)
        L, R = R, [l ^ t for l,t in zip(L, T)]
    preout = R + L  # note swap
    final = permute(preout, FP)
    return _bytes_from_bits(final)

def pkcs7_pad(data, block=8):
    pad = block - (len(data) % block)
    return data + bytes([pad])*pad

def pkcs7_unpad(data):
    if not data: return b''
    pad = data[-1]
    if pad <1 or pad>8: raise ValueError("Bad padding")
    if data[-pad:] != bytes([pad])*pad: raise ValueError("Bad padding")
    return data[:-pad]

def des_encrypt(data, key8):
    # data: bytes padded to 8, key8: 8 bytes
    subkeys = make_subkeys(key8)
    out = bytearray()
    for i in range(0,len(data),8):
        out += des_block(data[i:i+8], subkeys, encrypt=True)
    return bytes(out)

def des_decrypt(data, key8):
    subkeys = make_subkeys(key8)
    out = bytearray()
    for i in range(0,len(data),8):
        out += des_block(data[i:i+8], subkeys, encrypt=False)
    return bytes(out)

def _ensure_8byte_key(k):
    if len(k) != 8: raise ValueError("DES key must be 8 bytes")

def triple_des_encrypt(plaintext, key):
    """
    plaintext: bytes
    key: 16 or 24 bytes
    returns: ciphertext bytes (no encoding). Uses EDE: E_k1(D_k2(E_k3(plaintext)))? 
    We'll use E_k1(D_k2(E_k3())) is uncommon — standard EDE is: C = E_k3(D_k2(E_k1(P))).
    We'll implement standard EDE: C = E_k3(D_k2(E_k1(P))).
    For 16-byte key -> k1,k2,k1.
    """
    if len(key) not in (16,24): raise ValueError("Key must be 16 or 24 bytes")
    k1 = key[:8]; k2 = key[8:16]; k3 = key[16:24] if len(key)==24 else k1
    data = pkcs7_pad(plaintext, 8)
    # E_k1
    t1 = des_encrypt(data, k1)
    # D_k2
    t2 = des_decrypt(t1, k2)
    # E_k3
    c = des_encrypt(t2, k3)
    return c

def triple_des_decrypt(ciphertext, key):
    if len(key) not in (16,24): raise ValueError("Key must be 16 or 24 bytes")
    k1 = key[:8]; k2 = key[8:16]; k3 = key[16:24] if len(key)==24 else k1
    # D_k3
    t1 = des_decrypt(ciphertext, k3)
    # E_k2
    t2 = des_encrypt(t1, k2)
    # D_k1
    p = des_decrypt(t2, k1)
    return pkcs7_unpad(p)

# Example / quick test
if __name__ == "__main__":
    key24 = b'01234567abcdefghABCDEFG'[:24]  # 24 bytes
    pt = b"The quick brown fox jumps over the lazy dog"
    print("Plain:", pt)
    ct = triple_des_encrypt(pt, key24)
    print("Cipher (hex):", ct.hex())
    pt2 = triple_des_decrypt(ct, key24)
    print("Decrypted:", pt2)
    assert pt2 == pt
