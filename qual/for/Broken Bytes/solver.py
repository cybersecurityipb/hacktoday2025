# Tidak berubah dari sebelumnya
def shift_decipher_all(data: bytearray, key: int = 4) -> bytearray:
    result = bytearray()
    for i, byte in enumerate(data):
        if (i // 4) % 2 == 0:
            result.append((byte + key) % 256)  
        else:
            result.append(byte)
    return result

def decrypt_full_png(input_file: str, output_file: str, key: int = 4):
    with open(input_file, 'rb') as f:
        content = bytearray(f.read())

    decrypted = shift_decipher_all(content, key=key)

    with open(output_file, 'wb') as f:
        f.write(decrypted)

    print(f"[+] File berhasil didekripsi dan disimpan ke: {output_file}")

decrypt_full_png("file.png", "fix.png")
