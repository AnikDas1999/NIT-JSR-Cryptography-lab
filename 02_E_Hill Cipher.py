import numpy as np

def text_to_nums(text):
    return [ord(c)-65 for c in text.upper() if c.isalpha()]

def nums_to_text(nums):
    return ''.join(chr(n%26+65) for n in nums)

def mod_inverse(a, m):
    for x in range(1, m):
        if (a*x) % m == 1:
            return x
    return None

def encrypt(text, key):
    n = len(key)
    nums = text_to_nums(text)
    if len(nums)%n: nums.append(23)  # pad 'X'
    nums = np.array(nums).reshape(-1,n)
    res=[]
    for b in nums: res.extend((key.dot(b))%26)
    return nums_to_text(res)

def decrypt(text, key):
    n = len(key)
    nums = np.array(text_to_nums(text)).reshape(-1,n)
    det = int(round(np.linalg.det(key))) % 26
    inv_det = mod_inverse(det,26)
    if not inv_det: return "Key not invertible!"
    key_inv = (inv_det * np.round(det*np.linalg.inv(key)).astype(int))%26
    res=[]
    for b in nums: res.extend((key_inv.dot(b))%26)
    return nums_to_text(res)

# Example
key = np.array([[3,3],[2,5]])   # 2x2 key matrix
msg = input("Enter message: ")

enc = encrypt(msg,key)
print("Encrypted:",enc)

dec = decrypt(enc,key)
print("Decrypted:",dec)
