def create_matrix(key):
    key = key.upper().replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = ""
    for ch in key + alphabet:
        if ch not in matrix:
            matrix += ch
    return [list(matrix[i:i+5]) for i in range(0, 25, 5)]

def pos(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j

def prepare(text):
    text = text.upper().replace("J", "I")
    res, i = "", 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b:
            res += a + "X"
            i += 1
        else:
            res += a + b
            i += 2
    if len(res) % 2: res += "X"
    return res

def playfair(text, key, encrypt=True):
    m = create_matrix(key)
    text = prepare(text)
    out = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = pos(m, a)
        r2, c2 = pos(m, b)
        if r1 == r2:
            out += m[r1][(c1+(1 if encrypt else -1))%5]
            out += m[r2][(c2+(1 if encrypt else -1))%5]
        elif c1 == c2:
            out += m[(r1+(1 if encrypt else -1))%5][c1]
            out += m[(r2+(1 if encrypt else -1))%5][c2]
        else:
            out += m[r1][c2] + m[r2][c1]
    return out

# Example
msg = input("Enter message: ")
key = input("Enter key: ")

enc = playfair(msg, key, True)
print("Encrypted:", enc)

dec = playfair(enc, key, False)
print("Decrypted:", dec)
