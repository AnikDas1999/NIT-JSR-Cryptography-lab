# polynomial_multiplication_gf2.py
# Multiplication modulo an irreducible polynomial over GF(2^p)

def poly_mul(a: int, b: int) -> int:
    """
    Multiply two polynomials over GF(2) (no modulo reduction yet).
    Inputs a, b are integers representing polynomials.
    Returns an integer polynomial.
    """
    result = 0
    while b:
        if b & 1:
            result ^= a  # add current a if lowest bit of b is 1
        a <<= 1         # shift a (multiply by x)
        b >>= 1         # move to next bit of b
    return result


def poly_mod(poly: int, mod_poly: int) -> int:
    """
    Reduce polynomial 'poly' modulo 'mod_poly'.
    Both are integers representing polynomials.
    """
    deg_mod = mod_poly.bit_length() - 1
    while poly.bit_length() - 1 >= deg_mod:
        shift = (poly.bit_length() - 1) - deg_mod
        poly ^= (mod_poly << shift)
    return poly


def gf2p_mul(a: int, b: int, mod_poly: int) -> int:
    """
    Multiply two polynomials a, b in GF(2^p) with given irreducible modulus.
    """
    raw = poly_mul(a, b)
    return poly_mod(raw, mod_poly)


def int_to_poly_str(mask: int) -> str:
    """Convert integer polynomial to human-readable string."""
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
    # irreducible polynomial for GF(2^8) used in AES: x^8 + x^4 + x^3 + x + 1
    MOD_POLY = 0x11B  

    # Example: multiply (x^4 + x + 1) with (x^3 + x)
    a = 0b10011   # x^4 + x + 1
    b = 0b1010    # x^3 + x

    print("a =", int_to_poly_str(a))
    print("b =", int_to_poly_str(b))

    result = gf2p_mul(a, b, MOD_POLY)
    print("a * b (mod m(x)) =", int_to_poly_str(result))
