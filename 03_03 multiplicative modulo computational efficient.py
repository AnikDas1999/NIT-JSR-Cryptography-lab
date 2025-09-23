def poly_mul_mod(a, b, mod_poly):
    p = mod_poly.bit_length() - 1  # degree of the irreducible polynomial
    result = 0
    while b:
        if b & 1:          
            result ^= a
        b >>= 1        
        a <<= 1            
        if a & (1 << p):   
            a ^= mod_poly
    return result

a = int(input("Enter first polynomial (binary): "), 2)
b = int(input("Enter second polynomial (binary): "), 2)
mod_poly = int(input("Enter irreducible polynomial (binary): "), 2)

res = poly_mul_mod(a, b, mod_poly)
print("Result (binary):", bin(res)[2:])
