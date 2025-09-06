# gf2p8_mul.py
# Efficient multiplication modulo an irreducible polynomial in GF(2^8)

def gf_mul(a: int, b: int, mod_poly: int = 0x11B) -> int:
    """
    Efficient multiplication in GF(2^8).
    a, b: integers 0..255 (polynomials in GF(2^8))
    mod_poly: irreducible polynomial (default = 0x11B = x^8+x^4+x^3+x+1)
    Returns: product in GF(2^8)
    """
    result = 0
    while b:
        if b & 1:            # if lowest bit of b is set
            result ^= a      # add a to result (XOR)
        b >>= 1              # shift multiplier right
        carry = a & 0x80     # check if highest bit (x^7 term) is set
        a <<= 1              # multiply a by x
        if carry:            # if degree >= 8, reduce modulo
            a ^= mod_poly
        a &= 0xFF            # keep a within 8 bits
    return result


def int_to_poly_str(mask: int) -> str:
    """Convert integer mask to human-readable polynomial string."""
    if mask == 0:
        return "0"
    terms = []
    i = 0
    while mask:
        if mask & 1:
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")
        i += 1
        mask >>= 1
    return " + ".join(reversed(terms))


# -------------------------
# Example run
# -------------------------
if __name__ == "__main__":
    # irreducible polynomial for GF(2^8): x^8 + x^4 + x^3 + x + 1
    MOD_POLY = 0x11B

    # Example: multiply (x^4 + x + 1) with (x^3 + x)
    a = 0b10011   # x^4 + x + 1
    b = 0b1010    # x^3 + x

    print("Irreducible polynomial (modulus):", int_to_poly_str(MOD_POLY))
    print("\na =", int_to_poly_str(a), f"(hex {hex(a)})")
    print("b =", int_to_poly_str(b), f"(hex {hex(b)})")

    result = gf_mul(a, b, MOD_POLY)

    print("\nResult = a * b mod m(x)")
    print("Polynomial form:", int_to_poly_str(result))
    print("Hex form:", hex(result))
