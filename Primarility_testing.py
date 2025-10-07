import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Test
num = int(input("Enter a number: "))
if is_prime(num):
    print(num, "is a Prime Number")
else:
    print(num, "is NOT a Prime Number")
