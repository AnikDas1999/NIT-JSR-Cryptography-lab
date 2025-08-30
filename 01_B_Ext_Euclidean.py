def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t

a =int(input("Enter first numbers:"))
b =int(input("Enter second numbers:"))
g, x, y = extended_gcd(a, b)
print(f"GCD({a}, {b}) = {g}")
print(f"x = {x}, y = {y}")
print(f"Check: {a}*{x} + {b}*{y} = {a*x + b*y}")
