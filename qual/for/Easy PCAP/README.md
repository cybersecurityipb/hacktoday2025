# Easy PCAP

## Author
Fbrina

## Categories
Digital Forensic

## Description
Kakakku mengirimkan sebuah pesan aneh, entah keyboardnya rusak ataukah dia mengirimkan pesan rahasia. Oh iya dia juga mengirimkan sebuah gambar yang aku tidak tau maksudnya apa.

## Solver

### Langkah 1: Analisis pcapng
Diberikan sebuah file pcapng yang berisi sebuah percakapan

### Langkah 2: Ambil gambar yang dikirim dan juga kode misterius
Bisa langsung export object HTTP.

### Langkah 3: Flag 1
Flag 1 adalah hex yang perlu diubah menjadi text.

### Langkah 4: Analisis PNG
PNG tersebut terdapat sebuah arsip. Dan juga ada text didalam gambarnya, jadi bisa menggunakan stegsolve untuk mengetahui isi flag part 2 nya.

### Langkah 5: Analisa Arsip
Arsip tersebut menggunakan 7z dan memerlukan password untuk membukanya. Password terdapat dipercakapan yang ada di pcapng.
Kemudian akan ada file secret.txt yang berisi flag ke 3

## Flag
```
hacktoday{y0u_kn0w_mY_s3Cr3t_w00psi33}
```
