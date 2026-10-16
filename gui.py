"""Tampilan kalkulator (CustomTkinter + Matplotlib), tema gelap burgundy-crimson."""
from tkinter import ttk
import math
import customtkinter as ctk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from parser_fungsi import buat_fungsi
from secant import secant

# Palet warna
BG, SIDEBAR, PANEL = "#10090C", "#210A12", "#1B1016"
ACCENT, HOVER = "#C8102E", "#E02D4F"
TEXT, MUTED = "#F8F0F3", "#C7AAB5"
BORDER, INPUT_BG, KOTAK = "#3A1F2A", "#140B10", "#2A0F1A"
HIJAU, MERAH, ORANYE = "#3DDC84", "#FF6B6B", "#FFB84D"

KOLOM = ("Iterasi", "x0", "x1", "f(x0)", "f(x1)", "x2", "f(x2)", "Error")
MAKS_ITERASI = 1000  # batas agar tabel tetap ringan


def nilai_aman(f, v):
    """Hitung f(v); hasil tak valid (log negatif, kompleks, inf) diganti nan."""
    try:
        with np.errstate(all="ignore"):
            hasil = float(f(v))
    except Exception:
        return float("nan")
    return hasil if math.isfinite(hasil) else float("nan")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Kalkulator Metode Secant")
        # ukuran awal menyesuaikan layar (laptop 1366x768 tetap muat)
        lebar = min(1280, self.winfo_screenwidth() - 40)
        tinggi = min(780, self.winfo_screenheight() - 90)
        self.geometry(f"{lebar}x{tinggi}+20+20")
        self.minsize(1000, 560)
        self.configure(fg_color=BG)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Sidebar (kiri): judul + input
        self.sidebar = ctk.CTkFrame(self, width=330, fg_color=SIDEBAR, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.pack_propagate(False)

        # Area utama (kanan): hasil, grafik, tabel
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=8)
        self.main.columnconfigure(0, weight=1)
        self.main.rowconfigure(1, weight=3)
        self.main.rowconfigure(2, weight=2)

        ctk.CTkLabel(self.sidebar, text="Metode Secant", font=("Segoe UI", 22, "bold"),
                     text_color=TEXT).pack(anchor="w", padx=24, pady=(18, 0))
        ctk.CTkLabel(self.sidebar, text="Akar persamaan non-linear", font=("Segoe UI", 12),
                     text_color=MUTED).pack(anchor="w", padx=24)
        ctk.CTkFrame(self.sidebar, height=2, fg_color=ACCENT).pack(fill="x", padx=24, pady=(10, 6))

        self._buat_input()
        self._buat_hasil()
        self._buat_tabel()
        self._buat_grafik()
        self.reset()

    # ---------- pembentuk tampilan ----------
    def _kartu(self, judul, baris):
        kartu = ctk.CTkFrame(self.main, fg_color=PANEL, corner_radius=14,
                             border_width=1, border_color=BORDER)
        kartu.grid(row=baris, column=0, sticky="nsew", padx=8, pady=8)
        ctk.CTkLabel(kartu, text=judul, font=("Segoe UI", 16, "bold"),
                     text_color=TEXT).pack(anchor="w", padx=16, pady=(14, 6))
        isi = ctk.CTkFrame(kartu, fg_color="transparent")
        isi.pack(fill="both", expand=True)
        return isi

    def _buat_input(self):
        # Tombol dipasang LEBIH DULU di dasar sidebar agar selalu terlihat;
        # kolom input berada di area scroll di atasnya.
        footer = ctk.CTkFrame(self.sidebar, fg_color=SIDEBAR, corner_radius=0)
        footer.pack(side="bottom", fill="x", padx=24, pady=(6, 16))
        footer.columnconfigure(0, weight=3)
        footer.columnconfigure(1, weight=2)
        ctk.CTkButton(footer, text="▶  Hitung", height=38, corner_radius=8, fg_color=ACCENT,
                      hover_color=HOVER, font=("Segoe UI", 14, "bold"),
                      command=self.hitung).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkButton(footer, text="Reset", height=38, corner_radius=8, fg_color="transparent",
                      border_width=1, border_color=BORDER, hover_color="#33121D",
                      text_color=TEXT, command=self.reset).grid(row=0, column=1, sticky="ew")

        box = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", corner_radius=0,
                                     scrollbar_button_color="#4A2535",
                                     scrollbar_button_hover_color=ACCENT)
        box.pack(side="top", fill="both", expand=True, padx=(10, 4))

        self.entri = {}
        daftar = [("f", "Fungsi f(x)"), ("x0", "Nilai awal x0"), ("x1", "Nilai awal x1"),
                  ("tol", "Toleransi (ε)"), ("maks", "Maksimum iterasi")]
        for kunci, label in daftar:
            ctk.CTkLabel(box, text=label, text_color=MUTED, font=("Segoe UI", 12)).pack(
                anchor="w", padx=14, pady=(6, 1))
            e = ctk.CTkEntry(box, height=32, corner_radius=8, fg_color=INPUT_BG,
                             border_width=1, border_color=BORDER, text_color=TEXT)
            e.pack(fill="x", padx=14)
            e.bind("<Return>", lambda _e: self.hitung())
            e.bind("<Key>", lambda ev, k=kunci: self._bersihkan_tanda(k, ev))
            self.entri[kunci] = e
            if kunci == "f":
                self._buat_petunjuk(box)

    def _buat_petunjuk(self, parent):
        """Petunjuk penulisan fungsi (hanya teks, bukan nilai input)."""
        kotak = ctk.CTkFrame(parent, fg_color=INPUT_BG, corner_radius=8,
                             border_width=1, border_color=BORDER)
        kotak.pack(fill="x", padx=14, pady=(6, 0))
        ctk.CTkLabel(kotak, text="Gunakan x sebagai variabel dan ** untuk pangkat.",
                     text_color=MUTED, font=("Segoe UI", 11), wraplength=230,
                     justify="left").pack(anchor="w", padx=10, pady=(6, 2))
        ctk.CTkLabel(kotak, text="Contoh:\nx**3 - x - 1\nx**2 - 2\ncos(x) - x",
                     text_color=TEXT, font=("Consolas", 11),
                     justify="left").pack(anchor="w", padx=10, pady=(0, 6))

    def _buat_hasil(self):
        isi = self._kartu("Hasil", 0)
        isi.columnconfigure(1, weight=1)
        kotak = ctk.CTkFrame(isi, fg_color=KOTAK, corner_radius=10,
                             border_width=1, border_color=ACCENT)
        kotak.grid(row=0, column=0, sticky="nsew", padx=(16, 12), pady=(0, 14))
        ctk.CTkLabel(kotak, text="Akar (perkiraan)", text_color=MUTED).pack(
            anchor="w", padx=16, pady=(12, 0))
        self.lbl_akar = ctk.CTkLabel(kotak, text="-", font=("Segoe UI", 30, "bold"),
                                     text_color=TEXT)
        self.lbl_akar.pack(anchor="w", padx=16, pady=(0, 12))

        rincian = ctk.CTkFrame(isi, fg_color="transparent")
        rincian.grid(row=0, column=1, sticky="nsew", padx=(0, 16), pady=(0, 14))
        self.hasil = {}
        for kunci, label in [("f_akar", "Nilai fungsi di akar"), ("iterasi", "Jumlah iterasi"),
                             ("error", "Error akhir"), ("status", "Status")]:
            baris = ctk.CTkFrame(rincian, fg_color="transparent")
            baris.pack(fill="x", pady=3)
            ctk.CTkLabel(baris, text=label, text_color=MUTED, width=160, anchor="w").pack(
                side="left", anchor="n")
            lbl = ctk.CTkLabel(baris, text="-", text_color=TEXT, anchor="w",
                               justify="left", wraplength=420)
            lbl.pack(side="left", fill="x")
            self.hasil[kunci] = lbl

    def _buat_tabel(self):
        isi = self._kartu("Tabel Iterasi", 2)
        gaya = ttk.Style()
        gaya.theme_use("clam")
        gaya.configure("Treeview", background=PANEL, fieldbackground=PANEL,
                       foreground=TEXT, rowheight=28, borderwidth=0)
        gaya.configure("Treeview.Heading", background="#2A0F1A", foreground=TEXT,
                       relief="flat", font=("Segoe UI", 10, "bold"))
        gaya.map("Treeview", background=[("selected", ACCENT)])
        gaya.map("Treeview.Heading", background=[("active", "#3A1424")])
        sb = ctk.CTkScrollbar(isi, button_color="#4A2535", button_hover_color=ACCENT)
        sb.pack(side="right", fill="y", padx=(0, 8), pady=(0, 12))
        self.tabel = ttk.Treeview(isi, columns=KOLOM, show="headings", yscrollcommand=sb.set)
        sb.configure(command=self.tabel.yview)
        for k in KOLOM:
            self.tabel.heading(k, text=k)
            self.tabel.column(k, width=90, minwidth=60, anchor="center")
        self.tabel.pack(side="left", fill="both", expand=True, padx=(16, 0), pady=(0, 12))

    def _buat_grafik(self):
        isi = self._kartu("Grafik Fungsi", 1)
        self.fig = Figure(figsize=(5, 3), dpi=100, facecolor=PANEL)
        self.ax = self.fig.add_subplot(111)
        self.kanvas = FigureCanvasTkAgg(self.fig, master=isi)
        self.kanvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # ---------- aksi ----------
    def _galat(self, kunci, pesan):
        """Tandai kolom bermasalah dengan border merah, lalu hentikan perhitungan."""
        self.entri[kunci].configure(border_color=MERAH)
        raise ValueError(pesan)

    def _bersihkan_tanda(self, kunci, event):
        """Hilangkan border merah saat pengguna mulai mengetik ulang."""
        if event.keysym != "Return":
            self.entri[kunci].configure(border_color=BORDER)

    def _angka(self, kunci, nama, tipe=float):
        teks = self.entri[kunci].get().strip().replace(",", ".")
        if not teks:
            self._galat(kunci, f"{nama} belum diisi.")
        try:
            nilai = tipe(teks)
        except ValueError:
            jenis = "bilangan bulat" if tipe is int else "angka"
            self._galat(kunci, f"{nama} harus berupa {jenis}.")
        if tipe is float and not math.isfinite(nilai):
            self._galat(kunci, f"{nama} harus berupa angka yang terhingga.")
        return nilai

    def hitung(self):
        self._kosongkan()
        try:
            try:
                f, teks = buat_fungsi(self.entri["f"].get())
            except ValueError as e:
                self._galat("f", str(e))
            x0 = self._angka("x0", "Nilai awal x0")
            x1 = self._angka("x1", "Nilai awal x1")
            tol = self._angka("tol", "Toleransi")
            maks = self._angka("maks", "Maksimum iterasi", int)
            if tol <= 0:
                self._galat("tol", "Toleransi harus lebih dari 0.")
            if maks < 1:
                self._galat("maks", "Maksimum iterasi minimal 1.")
            if maks > MAKS_ITERASI:
                self._galat("maks", f"Maksimum iterasi tidak boleh lebih dari {MAKS_ITERASI}.")
            if x0 == x1:
                self._galat("x1", "x0 dan x1 harus berbeda.")
            hasil = secant(f, x0, x1, tol, maks)
        except ValueError as e:
            return self._pesan(str(e), MERAH)
        except Exception as e:
            return self._pesan(f"Perhitungan gagal: {e}", MERAH)

        for b in hasil["baris"]:
            self.tabel.insert("", "end", values=(b[0], *[f"{v:.6f}" for v in b[1:7]],
                                                 f"{b[7]:.3e}"))
        if hasil["konvergen"]:
            self.lbl_akar.configure(text=f"{hasil['akar']:.6f}")
        if hasil["f_akar"] is not None:
            self.hasil["f_akar"].configure(text=f"≈ {hasil['f_akar']:.3e}")
        if hasil["error"] is not None:
            self.hasil["error"].configure(text=f"≈ {hasil['error']:.3e}")
        self.hasil["iterasi"].configure(text=str(hasil["iterasi"]))
        self._pesan(hasil["status"], HIJAU if hasil["konvergen"] else ORANYE)
        self._gambar(f, teks, hasil, x0, x1)

    def _gambar(self, f, teks, hasil, x0, x1):
        titik = [x0, x1] + [b[5] for b in hasil["baris"]]
        titik = [t for t in titik if math.isfinite(t)]
        lo, hi = min(titik), max(titik)
        m = max((hi - lo) * 0.5, 1.0)
        xs = np.linspace(lo - m, hi + m, 400)
        ys = np.array([nilai_aman(f, v) for v in xs])
        ada = np.isfinite(ys)

        ax = self.ax
        ax.clear()
        self._gaya_sumbu()
        ax.axhline(0, color="#5A3445", linewidth=1)
        ax.plot(xs, ys, color=HOVER, linewidth=2.2, label="f(x)")
        if ada.any():
            batas_bawah, batas_atas = np.percentile(ys[ada], [2, 98])
            batas_bawah, batas_atas = min(batas_bawah, 0), max(batas_atas, 0)
            pad = (batas_atas - batas_bawah) * 0.1 or 1
            ax.set_ylim(batas_bawah - pad, batas_atas + pad)
        if hasil["baris"]:
            ax.scatter([b[5] for b in hasil["baris"]], [b[6] for b in hasil["baris"]],
                       color=TEXT, edgecolors=ACCENT, zorder=5, s=30, label="Titik iterasi")
        if hasil["konvergen"]:
            r = hasil["akar"]
            ax.axvline(r, color=HIJAU, linestyle="--", linewidth=1.4, label="Akar (perkiraan)")
            ax.annotate(f"x ≈ {r:.6f}", (r, 0), xytext=(10, 18), textcoords="offset points",
                        color=HIJAU, bbox=dict(boxstyle="round", fc=PANEL, ec=HIJAU))
        ax.set_title(f"f(x) = {teks}", color=TEXT, fontsize=11)
        ax.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT, fontsize=8)
        self.fig.tight_layout()
        self.kanvas.draw()

    def _gaya_sumbu(self):
        ax = self.ax
        ax.set_facecolor(PANEL)
        ax.tick_params(colors=MUTED)
        ax.set_xlabel("x", color=MUTED)
        ax.set_ylabel("f(x)", color=MUTED)
        ax.grid(color="#2A1620", linewidth=0.6)
        for s in ax.spines.values():
            s.set_color(BORDER)

    def _pesan(self, teks, warna):
        self.hasil["status"].configure(text=teks, text_color=warna)

    def _kosongkan(self):
        """Bersihkan hasil, tabel, grafik, status, dan tanda error (input tidak disentuh)."""
        self.tabel.delete(*self.tabel.get_children())
        self.lbl_akar.configure(text="-")
        for lbl in self.hasil.values():
            lbl.configure(text="-", text_color=TEXT)
        for e in self.entri.values():
            e.configure(border_color=BORDER)
        self.ax.clear()
        self._gaya_sumbu()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.text(0.5, 0.5, "Grafik akan tampil setelah perhitungan", color=MUTED,
                     ha="center", va="center", transform=self.ax.transAxes)
        self.kanvas.draw()

    def reset(self):
        for e in self.entri.values():
            e.delete(0, "end")
        self._kosongkan()
