def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def mod_inverse(a, p):
    gcd, x, _ = extended_gcd(a, p)
    if gcd != 1:
        return None   
    else:
        return x % p  


a = int(input("Enter number a: "))
p = int(input("Enter prime p: "))
inv = mod_inverse(a, p)

if inv is None:
    print("Inverse doesn't exist.")
else:
    print(f"The inverse of {a} mod {p} is {inv}")