import random

def is_probable_prime(n, k=5):  # k = number of tests
    if n <= 1:
        return False
    if n <= 3:
        return True

    # Perform k tests
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False  # Composite
    return True  # Probably Prime

# Test
num = int(input("Enter a number: "))
if is_probable_prime(num):
    print(num, "is probably prime (Fermat Test)")
else:
    print(num, "is composite")
