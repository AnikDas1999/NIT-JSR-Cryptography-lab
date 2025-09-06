# polynomial_gf2.py
# Polynomial addition in GF(2): coefficient-wise addition modulo 2.
# Representation:
#  - integer bitmask: bit i => coefficient of x^i (LSB = x^0)
#  - list: index i => coefficient of x^i (0 or 1)

import re

# -------------------------
# Parsers / Converters
# -------------------------
def parse_poly(s: str):
    """
    Parse a polynomial string like "x^3 + x + 1" or "1 + x + x^2"
    Return integer bitmask representation.
    """
    s = s.strip().replace(' ', '')
    if s == '' or s == '0':
        return 0
    # split on '+'
    tokens = s.split('+')
    mask = 0
    for t in tokens:
        if t == '1':
            power = 0
        elif t == 'x':
            power = 1
        else:
            # expect x^k
            m = re.fullmatch(r'x\^(\d+)', t)
            if not m:
                raise ValueError(f"Can't parse token: {t}")
            power = int(m.group(1))
        mask |= (1 << power)
    return mask

def int_to_poly_str(mask: int) -> str:
    """Convert integer mask -> human polynomial string (e.g. x^3 + x + 1)"""
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

def list_to_mask(coeffs: list) -> int:
    """coeffs: [c0, c1, c2, ...] -> integer bitmask"""
    mask = 0
    for i, c in enumerate(coeffs):
        if c % 2 != 0:
            mask |= (1 << i)
    return mask

def mask_to_list(mask: int) -> list:
    """Convert integer mask to list of coefficients [c0, c1, ...] (trim trailing zeros)"""
    coeffs = []
    i = 0
    while mask:
        coeffs.append(mask & 1)
        mask >>= 1
        i += 1
    return coeffs or [0]

# -------------------------
# Addition in GF(2)
# -------------------------
def add_poly_int(a_mask: int, b_mask: int) -> int:
    """
    Add two polynomials represented as integer masks.
    In GF(2) addition is XOR.
    """
    return a_mask ^ b_mask

def add_poly_list(a_coeffs: list, b_coeffs: list) -> list:
    """Add polynomials given as coefficient lists (lowest index = x^0)."""
    n = max(len(a_coeffs), len(b_coeffs))
    result = []
    for i in range(n):
        a = a_coeffs[i] if i < len(a_coeffs) else 0
        b = b_coeffs[i] if i < len(b_coeffs) else 0
        result.append((a ^ b) & 1)  # XOR then keep 0/1
    # strip trailing zeros but leave at least one coefficient
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result

# -------------------------
# Simple interactive examples / tests
# -------------------------
if __name__ == "__main__":
    examples = [
        ("x^3 + x + 1", "x^2 + x"),   # example 1
        ("x^4 + x^2 + 1", "x^4 + x + 1"), # example 2
        ("1", "1"),                   # cancels to 0
        ("x^5 + x^2", "x^3 + x^2 + 1")
    ]

    for A_str, B_str in examples:
        A_mask = parse_poly(A_str)
        B_mask = parse_poly(B_str)
        S_mask = add_poly_int(A_mask, B_mask)
        print(f"{A_str}  +  {B_str}  =  {int_to_poly_str(S_mask)}")

    # Demonstrate list-based addition
    a_list = [1, 0, 1, 1]   # 1 + x^2 + x^3  -> x^3 + x^2 + 1
    b_list = [1, 1, 0]      # 1 + x
    res_list = add_poly_list(a_list, b_list)
    print("\nList-based example:")
    print(f"{a_list}  +  {b_list}  =  {res_list}  => {int_to_poly_str(list_to_mask(res_list))}")
