# Diffie-Hellman Key Exchange Implementation
# Simple example for assignment

# Publicly known values (agreed by both)
p = 23   # Prime number
g = 5    # Primitive root of p

print("Publicly Shared Values:")
print("Prime (p):", p)
print("Base (g):", g)

# Alice selects a private key (a)
a = 6
# Bob selects a private key (b)
b = 15

# Alice computes her public key A = g^a mod p
A = (g ** a) % p
# Bob computes his public key B = g^b mod p
B = (g ** b) % p

print("\nPrivate Keys:")
print("Alice's private key (a):", a)
print("Bob's private key (b):", b)

print("\nPublic Keys:")
print("Alice's public key (A):", A)
print("Bob's public key (B):", B)

# Exchange public keys and compute the shared secret
shared_key_Alice = (B ** a) % p
shared_key_Bob = (A ** b) % p

print("\nShared Secret Calculation:")
print("Shared key computed by Alice:", shared_key_Alice)
print("Shared key computed by Bob  :", shared_key_Bob)

# Both shared keys will be same
if shared_key_Alice == shared_key_Bob:
    print("\n✅ Key Exchange Successful! Shared Secret Key =", shared_key_Alice)
else:
    print("\n❌ Key Exchange Failed!")
