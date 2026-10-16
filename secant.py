"""Logika metode Secant (murni perhitungan, tanpa tampilan)."""
import math
import warnings


def _nilai(f, v):
    """Hitung f(v). Mengembalikan None jika hasilnya tidak valid
    (error, kompleks, nan, atau tak terhingga)."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            hasil = float(f(v))
    except Exception:
        return None
    return hasil if math.isfinite(hasil) else None


def secant(f, x0, x1, tol=1e-6, maks_iter=50):
    """Mencari akar f(x) = 0 dengan metode Secant.

    Rumus : x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
    Error : |x2 - x1|
    Berhenti jika error <= tol (konvergen) atau iterasi mencapai maks_iter.
    """
    baris = []
    status = "Iterasi maksimum tercapai"
    konvergen = False
    akar, error = None, None

    for i in range(1, maks_iter + 1):
        f0, f1 = _nilai(f, x0), _nilai(f, x1)
        if f0 is None or f1 is None:
            titik = x0 if f0 is None else x1
            status = f"Berhenti: f(x) tidak terdefinisi di x = {titik:.6g}"
            break
        if f1 == f0:
            if f1 == 0:  # kedua nilai nol: x1 sudah akar
                baris.append((i, x0, x1, f0, f1, x1, f1, 0.0))
                akar, error = x1, 0.0
                status, konvergen = "Konvergen", True
            else:
                status = "Berhenti: f(x0) = f(x1), terjadi pembagian dengan nol"
            break

        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        if not math.isfinite(x2):
            status = "Berhenti: nilai x2 tidak terhingga (divergen)"
            break
        f2 = _nilai(f, x2)
        if f2 is None:
            status = f"Berhenti: f(x) tidak terdefinisi di x2 = {x2:.6g}"
            break

        error = abs(x2 - x1)
        akar = x2
        baris.append((i, x0, x1, f0, f1, x2, f2, error))
        if error <= tol:
            status, konvergen = "Konvergen", True
            break
        x0, x1 = x1, x2

    return {
        "akar": akar,
        "f_akar": baris[-1][6] if baris else None,
        "iterasi": len(baris),
        "error": error,
        "status": status,
        "konvergen": konvergen,
        "baris": baris,
    }
