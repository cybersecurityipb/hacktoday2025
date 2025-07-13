# Broken Bytes

## Author
Nikoo

## Categories
Digital Forensic

## Description
My image is corrupted and appears to have been encrypted by someone inexperienced. Fortunately, the encryption is flawed. The file isn't fully encrypted, but from what I can tell, it seems to have been shifted multiple times. Interestingly, the encryption key and the pattern appear to be the same. Can you help me uncover the encryption flow to restore the image?

**Note:** Format flag `hacktoday{}`

## Solver

### Langkah 1: Analisis Header PNG
Diberikan sebuah file PNG yang rusak/terenkripsi. Untuk memahami pola enkripsi, kita perlu menganalisis struktur header PNG yang seharusnya.

**Referensi untuk analisis header PNG:**
- [PNG - Wikipedia](https://en.wikipedia.org/wiki/PNG)
- [PNG Specification](https://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html)
- [PNG Structure for Beginner](https://medium.com/@0xwan/png-structure-for-beginner-8363ce2a9f73)

### Langkah 2: Identifikasi Magic Bytes PNG
Header PNG yang benar memiliki magic bytes:
```
89 50 4E 47 0D 0A 1A 0A
```

Bandingkan dengan magic bytes file yang terenkripsi untuk menemukan pola enkripsi dan key yang digunakan.

### Langkah 3: Analisis Pola Enkripsi
Dengan mencocokkan hex atau magic bytes yang telah terenkripsi dengan hex atau magic bytes format PNG yang benar, kita dapat menemukan pola enkripsi sebagai berikut:

**Pola Enkripsi:**
- Enkripsi dilakukan dengan algoritma **shift cipher ke kiri** menggunakan kunci tetap `key = 4`
- Pattern enkripsi memiliki pola **lompat-lompat**:
  - Setiap kelompok **4 byte pertama** (indeks 0–3, 8–11, 16–19, dst.) **dienkripsi** dengan mengurangi nilai setiap byte sebesar 4 (`byte - key`)
  - Setiap kelompok **4 byte berikutnya** (indeks 4–7, 12–15, 20–23, dst.) **dilewati** atau tidak dienkripsi
- Pola: **4 dienkripsi → 4 tidak dienkripsi → 4 dienkripsi → 4 tidak dienkripsi** (berulang sampai habis)

### Langkah 4: Implementasi Dekripsi
Untuk mendekripsi file, kita perlu membalikkan proses enkripsi:

```python
def shift_decipher_all(data: bytearray, key: int = 4) -> bytearray:
    """Dekripsi dengan shift cipher ke kanan: 4 byte didekripsi (pakai +key), 4 byte dilewati"""
    result = bytearray()
    for i, byte in enumerate(data):
        if (i // 4) % 2 == 0:  # Setiap kelompok 4 byte pertama
            result.append((byte + key) % 256)  # Dekripsi (geser kanan)
        else:  # Setiap kelompok 4 byte berikutnya
            result.append(byte)  # Tidak diubah
    return result

def decrypt_full_png(input_file: str, output_file: str, key: int = 4):
    with open(input_file, 'rb') as f:
        content = bytearray(f.read())

    decrypted = shift_decipher_all(content, key=key)

    with open(output_file, 'wb') as f:
        f.write(decrypted)

    print(f"[+] File berhasil didekripsi dan disimpan ke: {output_file}")

# Eksekusi dekripsi
decrypt_full_png("file.png", "fix.png")
```

### Langkah 5: Verifikasi Hasil
Setelah menjalankan script dekripsi `vsolver.py`, file PNG yang telah diperbaiki akan menampilkan gambar yang berisi flag.

## References
- [PNG - Wikipedia](https://en.wikipedia.org/wiki/PNG)
- [PNG Specification](https://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html)
- [PNG Structure for Beginner](https://medium.com/@0xwan/png-structure-for-beginner-8363ce2a9f73)

## Flag
```
hacktoday{wh3n_y0u_sh1ft_3very_f0ur_byte5_l3ft_4nd_sk1p_th3_n3xt_f0ur_thin9s_bre4k}
```
