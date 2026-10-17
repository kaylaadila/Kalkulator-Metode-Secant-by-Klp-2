"""Mengubah teks f(x) dari pengguna menjadi fungsi Python yang bisa dihitung."""
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor,
)

x = sp.Symbol("x")
TRANSFORMASI = standard_transformations + (implicit_multiplication_application, convert_xor)


def buat_fungsi(teks):
    """Contoh teks: 'x**3 - x - 1', 'x**2 - 2', 'cos(x) - x'."""
    teks = teks.strip()
    if not teks:
        raise ValueError("Fungsi f(x) belum diisi.")
    try:
        ekspresi = parse_expr(teks, local_dict={"x": x}, transformations=TRANSFORMASI)
    except Exception:
        raise ValueError("Fungsi tidak dapat dibaca. Contoh: x**3 - x - 1")
    if not isinstance(ekspresi, sp.Expr):
        raise ValueError("Fungsi harus berupa ekspresi matematika, bukan persamaan atau pertidaksamaan.")
    if ekspresi.free_symbols - {x}:
        raise ValueError("Fungsi hanya boleh memakai variabel x.")
    try:
        fungsi = sp.lambdify(x, ekspresi, modules="numpy")
    except Exception:
        raise ValueError("Fungsi tidak dapat diubah menjadi perhitungan numerik.")
    return fungsi, str(ekspresi)
