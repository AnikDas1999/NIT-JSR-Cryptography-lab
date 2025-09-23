def poly_add(a, b):
    return a ^ b  

def poly_to_str(p):
    terms = []
    i = 0
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


A = int(input("Enter polynomial A in binary (e.g. 1011 for x^3+x+1): "))
B = int(input("Enter polynomial B in binary (e.g. 0110 for x^2+x): "))

C = poly_add(A, B)

print("\nResults:")
print("A(x) =", poly_to_str(A))
print("B(x) =", poly_to_str(B))
print("A(x) + B(x) =", poly_to_str(C))
