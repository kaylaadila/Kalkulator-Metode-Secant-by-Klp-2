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

Kalkulator penyelesaian persamaan nonlinier f(x) = 0 dengan **metode Secant**,
dibuat dengan Python (GUI CustomTkinter). Program menampilkan akar, proses setiap
iterasi, nilai error, jumlah iterasi, dan grafik fungsi.

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


## Cara Menjalankan

```bash
git clone https://github.com/kaylaadila/Kalkulator-Metode-Secant-by-Klp-2.git
cd Kalkulator-Metode-Secant-by-Klp-2
pip install -r requirements.txt
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

## Lisensi

Belum ditentukan.
