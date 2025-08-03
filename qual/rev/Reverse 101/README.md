# Reverse 101

## Author
Nikoo

## Categories
Reverse Engineering

## Description
Is the fastest way always the best way?

## Solver

### Analisis Awal
Challenge ini terdiri dari 101 fungsi dengan struktur sebagai berikut:
- **86 fungsi check** (f0 sampai f85) - masing-masing memvalidasi satu karakter flag
- **12 fungsi obfuscation** - pipeline transformasi multi-layer 
- **1 fungsi main** - entry point program
- **2 fungsi tambahan** - `full_transform()` dan `verify_flag()`

### Langkah-Langkah Penyelesaian

#### 1. Memahami Alur Program
- Program menerima input flag sepanjang 86 karakter
- Setiap karakter ditransformasi melalui fungsi `full_transform()` 
- Hasil transformasi divalidasi oleh fungsi check yang sesuai (f0-f85)
- Jika semua validasi berhasil, flag dianggap benar

#### 2. Analisis Pipeline Transformasi
Fungsi `full_transform()` menerapkan 12 transformasi berurutan:
1. **shift()** - Geser karakter berdasarkan posisi
2. **rot13()** - Enkoding ROT13 
3. **rol()** - Rotasi bit ke kiri sesuai posisi
4. **keyxor()** - XOR dengan key berdasarkan posisi
5. **lookup()** - Substitusi menggunakan lookup table
6. **not()** - Operasi bitwise NOT
7. **addpos()** - Penambahan nilai posisi
8. **swap_nibble()** - Tukar nibble atas dan bawah
9. **xor_a5()** - XOR dengan 0xA5
10. **rol3()** - Rotasi 3 bit ke kiri
11. **xor3c()** - XOR dengan 0x3C
12. **rol1()** - Rotasi 1 bit ke kiri

#### 3. Analisis Fungsi Check
Setiap fungsi f0-f85 memiliki constraint matematika berbeda:
- Operasi aritmatika (+, -, *)
- Operasi bitwise (^, &, |, ~)
- Operasi shift dan rotasi
- Kombinasi operasi kompleks

#### 4. Strategi Penyelesaian

**Metode 1: Reverse Mathematical Analysis**
- Analisis setiap fungsi check untuk mendapatkan nilai yang dibutuhkan
- Buat fungsi inverse untuk setiap transformasi
- Terapkan inverse transformation secara berurutan terbalik
- Rekonstruksi karakter asli

**Metode 2: Brute Force**
- Untuk setiap posisi (0-85), coba semua karakter yang mungkin
- Transformasikan karakter dengan `full_transform()`
- Cek apakah hasil transformasi memenuhi fungsi check
- Simpan karakter yang valid

#### 5. Implementasi Reverse Transformation

**Langkah Reverse (urutan terbalik):**
1. Reverse `rol1()` → gunakan rotate right 1 bit
2. Reverse `xor3c()` → XOR lagi dengan 0x3C
3. Reverse `rol3()` → gunakan rotate right 3 bit  
4. Reverse `xor_a5()` → XOR lagi dengan 0xA5
5. Reverse `swap_nibble()` → tukar nibble lagi (self-inverse)
6. Reverse `addpos()` → kurangi nilai posisi
7. Reverse `not()` → operasi NOT lagi
8. Reverse `lookup()` → buat reverse lookup table
9. Reverse `keyxor()` → XOR lagi dengan key yang sama
10. Reverse `rol()` → gunakan rotate right
11. Reverse `rot13()` → ROT13 lagi (self-inverse)
12. Reverse `shift()` → geser balik sesuai posisi

#### 6. Solving Check Functions
Contoh penyelesaian beberapa fungsi check:
- **f0**: `((x ^ 0x4F) + 3) == 0x51` → x = (0x51 - 3) ^ 0x4F
- **f1**: `((~x + 7) & 0xFF) == 0x68` → x = ~(0x68 - 7)
- **f2**: `((x + 5) ^ 0xAA) == 0x28` → x = (0x28 ^ 0xAA) - 5

#### 7. Optimasi dan Shortcut
Berdasarkan hint "Is the fastest way always the best way?", mungkin ada pola atau shortcut:
- Cari pola dalam fungsi check yang berulang
- Identifikasi karakter yang mungkin berdasarkan format flag
- Gunakan dynamic analysis untuk mempercepat proses

#### 8. Verifikasi
- Jalankan hasil flag melalui program asli
- Pastikan semua 86 karakter valid
- Cek format flag sesuai konvensi CTF

## Flag
```
hacktoday{dec0mp1le_th3n_4n4lyze_th3_funct1on_r3v3rse_th3_4lg0rithm_4nd_g3t_th3_fl4g5}
```
