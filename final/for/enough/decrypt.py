import os

BUF_SZ = 4096
KEY_LEN = 32

def rotl8(v, r):
    r &= 7
    return ((v << r) & 0xFF) | (v >> (8 - r))

def rotr8(v, r):
    r &= 7
    return ((v >> r) | ((v << (8 - r)) & 0xFF)) & 0xFF

def inverse_transform(buf, offset, key):
    n = len(buf)
    out = bytearray(buf)

    # Step 10 inverse
    for i in range(n):
        k = key[(offset + i * 7) % KEY_LEN]
        out[i] ^= (k + (i & 7)) & 0xFF

    # Step 9 inverse
    for i in range(n):
        out[i] = rotr8(out[i], 5)

    # Step 8 inverse
    for i in range(n):
        out[i] ^= (((i & 15) * 17 + 11) & 0xFF)

    # Step 7 inverse
    for i in range(n):
        out[i] = (out[i] - ((offset + i * 3) & 0xFF)) & 0xFF

    # Step 6 inverse
    for i in range(n):
        out[i] ^= key[KEY_LEN - 1 - ((offset + i) % KEY_LEN)]

    # Step 5 inverse
    for i in range(n):
        out[i] = rotl8(out[i], 2)

    # Step 4 inverse
    for i in range(n):
        out[i] ^= ((i * 13 + 7) & 0xFF)

    # Step 3 inverse
    for i in range(n):
        out[i] = rotr8(out[i], 3)

    # Step 2 inverse
    for i in range(n):
        out[i] ^= ((offset + i) & 0xFF)

    # Step 1 inverse
    for i in range(n):
        out[i] ^= key[(offset + i) % KEY_LEN]

    return out

def decrypt_file(enc_filename, key_filename):
    # Load key
    with open(key_filename, "rb") as f:
        key = f.read(KEY_LEN)
    if len(key) != KEY_LEN:
        raise ValueError("Key file size mismatch")

    # Output filename
    if enc_filename.endswith(".enc"):
        out_filename = enc_filename[:-4]
    else:
        out_filename = enc_filename + ".dec"

    with open(enc_filename, "rb") as fin, open(out_filename, "wb") as fout:
        offset = 0
        while True:
            chunk = fin.read(BUF_SZ)
            if not chunk:
                break
            plain = inverse_transform(bytearray(chunk), offset, key)
            fout.write(plain)
            offset += len(chunk)

    print(f"[+] Decrypted: {enc_filename} -> {out_filename}")

# contoh penggunaan
decrypt_file(r"D:\os\ransomware\coba\exp\0001.jpg.enc",
             r"D:\os\ransomware\coba\exp\output.bin")
