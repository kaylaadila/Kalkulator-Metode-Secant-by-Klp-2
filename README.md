# Kalkulator Metode Secant

**Kelompok 2 — Komputasi Numerik**

## Anggota Kelompok

Kelompok 2 — Komputasi Numerik
- Kayla Adila Farija Atika
- Aisya Ghaisany 
- Naila Syakira Bahri
- M. Ihsan Syahni
- M. Farras Munawwir
- Shandy Aprilliko Hartianto


## Status Proyek

Dalam tahap pengembangan.

## Deskripsi

Kalkulator Metode Secant merupakan aplikasi berbasis Python dengan antarmuka GUI menggunakan CustomTkinter yang dirancang untuk membantu menyelesaikan persamaan nonlinier (f(x)=0) secara numerik. Pengguna dapat memasukkan fungsi, dua nilai awal, toleransi error, dan maksimum iterasi untuk memperoleh pendekatan akar persamaan.

Program menampilkan hasil perhitungan berupa nilai akar, proses setiap iterasi, error, jumlah iterasi, dan status perhitungan. Selain itu, aplikasi menyediakan grafik fungsi beserta titik-titik iterasi untuk mempermudah pengguna memahami proses pencarian akar.

## Tujuan

1. Mengimplementasikan algoritma metode Secant untuk menyelesaikan persamaan nonlinier f(x) = 0.
2. Menampilkan proses perhitungan secara transparan pada setiap iterasi, mulai dari nilai awal hingga mencapai toleransi error.
3. Menentukan pendekatan akar persamaan beserta ukuran ketelitiannya (error, f(akar), dan jumlah iterasi).
4. Memvisualisasikan fungsi, lintasan iterasi, dan akar dalam bentuk grafik agar perilaku konvergensi mudah dipahami.
5. Mendeteksi dan menangani kondisi gagal (input tidak valid, pembagian dengan nol, divergen) dengan pesan yang jelas.
6. Mendukung pembelajaran metode Secant pada mata kuliah Komputasi Numerik.

## Fitur

- Input fungsi f(x) (contoh: `x^3 - x - 1`, `cos(x) - x`, `exp(-x) - x`)
- Input dua nilai awal (x0 dan x1), toleransi error, dan maksimum iterasi
- Tabel proses setiap iterasi (x0, x1, f(x0), f(x1), x2, f(x2), error)
- Hasil: akar perkiraan, f(akar), jumlah iterasi, error akhir, dan status
- Grafik fungsi lengkap dengan titik iterasi dan akar
- Penanganan kesalahan: input tidak valid, pembagian dengan nol, dan divergen

## Metode Secant

Dua tebakan awal x0 dan x1 dipakai untuk menarik garis lurus (garis sekan) melalui
titik (x0, f(x0)) dan (x1, f(x1)). Titik potong garis itu dengan sumbu x menjadi
tebakan berikutnya:

```
x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
```

- **Error** pada tiap iterasi: |x2 - x1|
- **Kriteria berhenti:** error <= toleransi (konvergen), atau iterasi mencapai maksimum
- **Catatan:** Secant tidak menjamin konvergen. Jika f(x0) = f(x1) rumus tidak dapat
  dihitung, dan program akan menampilkan pesan status.

## Teknologi

- **Python** sebagai bahasa pemrograman untuk mengembangkan aplikasi dan menerapkan perhitungan metode Secant.
- **CustomTkinter** untuk membuat antarmuka GUI aplikasi.
- **NumPy** untuk mendukung operasi dan perhitungan numerik.
- **SymPy** untuk membaca dan mengolah fungsi matematika yang dimasukkan pengguna.
- **Matplotlib** untuk menampilkan grafik fungsi dan titik iterasi.
- **GitHub** digunakan untuk menyimpan dan mempublikasikan source code proyek.

## Cara Menjalankan
*1. Clone Repository*
```
git clone https://github.com/kaylaadila/Kalkulator-Metode-Secant-by-Klp-2.git
```
*2. Masuk ke Folder Proyek*
```
cd Kalkulator-Metode-Secant-by-Klp-2
```
*3. Install Dependencies*
```
pip install -r requirements.txt
```
*4. Jalankan Aplikasi*
```
python main.py
```

Library: `numpy`, `matplotlib`, `sympy`, `customtkinter` (Tkinter bawaan Python;
di Linux mungkin perlu `sudo apt install python3-tk`).

## Struktur Project

| File | Fungsi |
|------|--------|
| `main.py` | Titik masuk, menjalankan aplikasi |
| `secant.py` | Perhitungan metode Secant (tanpa tampilan) |
| `parser_fungsi.py` | Mengubah teks f(x) menjadi fungsi yang bisa dihitung |
| `gui.py` | Tampilan: input, hasil, tabel iterasi, grafik |
| `screenshots/` | Tangkapan layar hasil perhitungan |

## Penjelasan Kode

- **`secant.py`** — fungsi `secant(f, x0, x1, tol, maks_iter)` mengulang rumus Secant,
  mencatat tiap iterasi ke dalam daftar baris, lalu mengembalikan akar, error, jumlah
  iterasi, dan status.
  
- **`parser_fungsi.py`** — memakai SymPy untuk membaca teks seperti `x^3 - x - 1`
  (tanda `^` dianggap pangkat), memastikan hanya variabel `x` yang dipakai, lalu
  mengubahnya menjadi fungsi numerik dengan `lambdify`.
  
- **`gui.py`** — kelas `App` menyusun empat kartu (Input, Hasil, Tabel Iterasi, Grafik).
  Tombol **Hitung** membaca input, memvalidasinya, memanggil `secant`, lalu mengisi
  tabel, hasil, dan grafik Matplotlib.

## Lisensi

Belum ditentukan.
