def poly_to_str(p):
    terms, i = [], 0
    while p:
        if p & 1:
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")
        p >>= 1
        i += 1
    return " + ".join(reversed(terms)) if terms else "0"

def poly_mul_mod(a, b, mod):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    m_deg = mod.bit_length() - 1
    while result.bit_length() >= m_deg + 1:
        shift = result.bit_length() - m_deg - 1
        result ^= mod << shift
    return result


A = int(input("Enter polynomial A in binary: "), 2)
B = int(input("Enter polynomial B in binary: "), 2)
MOD = int(input("Enter irreducible polynomial in binary: "), 2)

C = poly_mul_mod(A, B, MOD)

print("\nResults:")
print("A(x) =", poly_to_str(A))
print("B(x) =", poly_to_str(B))
print("MOD(x) =", poly_to_str(MOD))
print("A(x) * B(x) mod MOD(x) =", poly_to_str(C))
