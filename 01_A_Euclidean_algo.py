def gcd(a, b):
    while b != 0:
        a, b = b, a % b  # update values
    return a

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

print("GCD is:", gcd(num1, num2))
