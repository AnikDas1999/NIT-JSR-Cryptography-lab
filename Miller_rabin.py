import random

def is_prime_miller_rabin(n, k=5):  # k = number of test rounds
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Step 1: Write n-1 as 2^r * d (with d odd)
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Step 2: Perform k tests
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite

    return True  # Probably prime


# Test
num = int(input("Enter a number: "))
if is_prime_miller_rabin(num):
    print(num, "is probably prime (Miller-Rabin Test)")
else:
    print(num, "is composite")
