# short_yak.py - simplified toy YAK authenticated key exchange
import secrets, hashlib

p = 23; g = 5  # public params (toy)

# long-term keys (secret/public)
skA = 3                      # Alice long-term secret
skB = 7                      # Bob   long-term secret
pkA = pow(g, skA, p)
pkB = pow(g, skB, p)

# ephemeral secrets
rA = secrets.randbelow(p-2) + 1
rB = secrets.randbelow(p-2) + 1
RA = pow(g, rA, p)
RB = pow(g, rB, p)

# YAK-style authenticated shared secret (simplified formula)
KA = pow((RB * pkB) % p, (rA + skA), p)
KB = pow((RA * pkA) % p, (rB + skB), p)

# derive fixed-length key (SHA-256) from shared secret integer
keyA = hashlib.sha256(str(KA).encode()).hexdigest()
keyB = hashlib.sha256(str(KB).encode()).hexdigest()

print("pkA, pkB:", pkA, pkB)
print("RA, RB:", RA, RB)
print("Shared int KA, KB:", KA, KB)
print("Derived keys equal?", keyA == keyB)
print("Session key (hex):", keyA)
