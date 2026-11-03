"""Utilidades compartidas del pipeline de facturas de Cora."""
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "INPUT" / "2026"
CACHE = ROOT / "cache" / "txt" / "2026"
DATA = ROOT / "data"
CORA_CUIT = "33718678019"

# Importe con 2 decimales en formato AR (1.234,56 / 1234,56) o US (1,234.56)
AMT = r"((?:\d{1,3}(?:[.,]\d{3})+|\d+)[.,]\d{2})"
AMT_RE = re.compile(AMT)

MONTHS = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
          "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def num(s):
    """Importe monetario con decimales: '1.234,56' | '1,234.56' | '1234,56' -> float.
    El último separador seguido de 2 o 4 dígitos es el decimal."""
    s = s.strip().replace("$", "").replace(" ", "")
    if not s:
        return None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            return num_ar(s)
        return num_us(s)
    if "," in s:
        return num_ar(s)
    return num_us(s)


def num_ar(s):
    """Formato argentino: punto de miles, coma decimal."""
    return float(s.strip().replace("$", "").replace(" ", "").replace(".", "").replace(",", "."))


def num_us(s):
    """Formato inglés: coma de miles, punto decimal."""
    return float(s.strip().replace("$", "").replace(" ", "").replace(",", ""))


def amounts(line):
    return [num(m) for m in AMT_RE.findall(line)]


def folder_month(rel):
    """'9. Septiembre/...' -> 9"""
    m = re.match(r"^\s*(\d+)", rel)
    return int(m.group(1)) if m else None


def extract_all():
    """pdftotext -layout de todos los PDF de INPUT/2026 que falten en cache."""
    n = 0
    for pdf in INPUT.rglob("*"):
        if pdf.suffix.lower() != ".pdf":
            continue
        rel = pdf.relative_to(INPUT)
        out = CACHE / rel.with_suffix(".txt")
        if out.exists() and out.stat().st_mtime >= pdf.stat().st_mtime:
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftotext", "-layout", str(pdf), str(out)], check=False)
        n += 1
    return n


def iter_pdf_texts():
    for pdf in sorted(INPUT.rglob("*")):
        if pdf.suffix.lower() != ".pdf":
            continue
        rel = pdf.relative_to(INPUT)
        txt = CACHE / rel.with_suffix(".txt")
        text = txt.read_text(encoding="utf-8", errors="replace") if txt.exists() else ""
        yield str(rel), text
