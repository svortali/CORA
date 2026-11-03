"""Cabecera de cada factura PDF: fecha, CUIT emisor, tipo, CAE, neto y total."""
import re
from common import AMT, AMT_RE, CORA_CUIT, num, amounts, folder_month

# ---------------------------------------------------------------- totales
TOTAL_PATS = [
    ("ars_equiv", re.compile(r"Equivalente a pesos argentinos\s*\$?\s*" + AMT, re.I)),
    ("importe_total", re.compile(r"Importe\s+Total\s*:?\s*\$?\s*" + AMT, re.I)),
    ("total_pesos", re.compile(r"TOTAL\s+Pesos\s+" + AMT)),
    ("total_$", re.compile(r"(?<!Sub )(?<!Sub)\bTotal\s*:?\s*\$\s*" + AMT, re.I)),
    ("total_eol", re.compile(r"(?<!Sub )(?<!Sub)\bTOTAL[ \t]+\$?[ \t]*" + AMT + r"[ \t]*$", re.M)),
    ("total_line", re.compile(r"(?<!Sub )(?<!Sub)\bTotal\s*:?[ \t]+\$?[ \t]*" + AMT, re.I)),
    ("total_a_pagar", re.compile(r"Total\s+a\s+pagar\s*:?\s*\$?\s*" + AMT, re.I)),
]
NETO_PATS = [
    ("neto_gravado", re.compile(r"Importe\s+Neto\s+Gravado\s*:?\s*\$?\s*" + AMT, re.I)),
    ("untaxed", re.compile(r"Untaxed Amount\s+\$?\s*" + AMT)),
    ("total_neto", re.compile(r"Total Neto:\s*" + AMT)),
    ("neto", re.compile(r"^\s*NETO\s*:?[ \t]+\$?[ \t]*" + AMT, re.I | re.M)),
    ("subtotal_gravado", re.compile(r"Subtotal Gravado\s+\$\s*" + AMT)),
    ("subtotal", re.compile(r"Sub\s?total\s*:?[ \t]*\$?[ \t]*" + AMT, re.I)),
]

CUIT_RE = re.compile(r"\b(\d{2})-?(\d{8})-?(\d)\b")
CAE_RE = re.compile(r"C\.?A\.?E\.?\s*N?[°º]?\s*:?\s*(\d{14})", re.I)
COD_RE = re.compile(r"COD(?:IGO)?\.?\s*(?:N[°º]\s*)?0*(\d{1,2})\b", re.I)
TIPO = {"1": "A", "6": "B", "11": "C", "3": "NC-A", "8": "NC-B", "13": "NC-C"}
RAZON_RE = re.compile(r"Raz[oó]n Social:\s*(.+?)\s{2,}", re.I)

DATE_PATS = [  # (regex, orden de grupos d,m,y)
    (re.compile(r"Fecha(?:\s+de\s+Emisi[oó]n)?\s*:?\s*(\d{1,2})/(\d{1,2})/(\d{4})", re.I), (1, 2, 3)),
    (re.compile(r"FECHA\s+(\d{2})/(\d{2})/(\d{4})"), (1, 2, 3)),
    (re.compile(r"Date:\s*(\d{2})/(\d{2})/(\d{4})"), (2, 1, 3)),  # Odoo en inglés: MM/DD/YYYY
    (re.compile(r"FECHA\s*:?\s*(\d{1,2})\s+/?\s*(\d{1,2})\s+/?\s*(\d{2,4})"), (1, 2, 3)),
    (re.compile(r"\b(\d{2})/(\d{2})/(\d{4})\b"), (1, 2, 3)),
]


def first(pats, t):
    for name, pat in pats:
        m = pat.search(t)
        if m:
            return num(m.group(1)), name
    return None, None


def row_after(t, header_re, min_vals=4):
    """Primera línea con >= min_vals importes después del encabezado de una tabla de totales."""
    lines = t.splitlines()
    for i, l in enumerate(lines):
        if re.search(header_re, l):
            for l2 in lines[i + 1:i + 12]:
                vals = amounts(l2)
                if len(vals) >= min_vals:
                    return vals
    return None


def parse_date(t):
    for pat, (a, b, c) in DATE_PATS:
        m = pat.search(t)
        if m:
            d, mo, y = int(m.group(a)), int(m.group(b)), m.group(c)
            y = int("20" + y) if len(y) == 2 else int(y)
            if 1 <= d <= 31 and 1 <= mo <= 12 and y >= 2024:
                return f"{y:04d}-{mo:02d}-{d:02d}"
    return None


def parse_header(rel, t):
    cuits = []
    for m in CUIT_RE.finditer(t):
        c = "".join(m.groups())
        if c != CORA_CUIT and c not in cuits:
            cuits.append(c)
    cuit = cuits[0] if cuits else None
    m = CAE_RE.search(t)
    cae = m.group(1) if m else None
    m = COD_RE.search(t)
    tipo = TIPO.get(m.group(1), "A") if m else "A"
    if re.search(r"FACTURA\s+C\b|\bC\s+FACTURA\b|COD\.\s*011", t):
        tipo = "C"
    if re.search(r"NOTA\s+DE\s+CR[EÉ]DITO", t, re.I):
        tipo = "NC-" + (tipo[-1] if tipo[-1] in "ABC" else "A")
    m = RAZON_RE.search(t)
    razon = m.group(1).strip() if m else None
    note = []
    total = neto = None
    how_t = how_n = None

    if "Consorcio de Propietarios" in t:  # liquidación de expensas
        m = re.search(r"^\s*0\s+1\s+PARAGAMIAN.*$", t, re.M)
        if m:
            total = neto = amounts(m.group(0))[-1]
        how_t = how_n = "expensas_uf1"
        cuit = "30536235554"
        tipo = "Expensas"
        note.append("Expensas UF 1, sin IVA")
    elif cuit == "30708808322":  # La Nueva (Delerma): fila Subtotal|Desc|Neto|IVA|NoGrav|Total
        v = row_after(t, r"Neto Gravado.*No Gravado")
        if v:
            neto, total = v[2], v[-1]
            how_t = how_n = "fila_totales"
    elif cuit == "30708248238":  # La Meson: Subtotal|Dscto|Subt.Gravado|Perc IIBB|Perc IVA|IVA..|Total
        v = row_after(t, r"Subt\.Gravado")
        if v:
            neto, total = v[2], v[-1]
            how_t = how_n = "fila_totales"
    elif cuit == "30715435981":  # Amande: SUBTOTAL|DESC|SUBTOTAL|IVA21|IVA0|TOTAL
        v = row_after(t, r"SUBTOTAL\s+DESCUENTO\s+SUBTOTAL", min_vals=5)
        if v:
            neto, total = v[2], v[-1]
            how_t = how_n = "fila_totales"
    elif cuit == "30715067605":  # La Delfina: "Total Neto" es en realidad el total con IVA
        m = re.search(r"SubTotal\s+" + AMT, t)
        neto = num(m.group(1)) if m else None
        m = re.search(r"Total Neto\s+" + AMT, t)
        total = num(m.group(1)) if m else None
        how_t = how_n = "la_delfina"
    elif cuit == "30710858000":  # Umami: dos "Subtotal", el segundo es el neto con descuento
        subs = re.findall(r"Subtotal\s+" + AMT, t)
        neto = num(subs[-1]) if subs else None
        total, how_t = first(TOTAL_PATS[3:], t)
        how_n = "umami"
    if total is None:
        total, how_t = first(TOTAL_PATS, t)
    if neto is None:
        if "U$s" in t and how_t == "ars_equiv":  # Oatly en dólares
            m1 = re.search(r"Subtotal Gravado\s+U\$s\s*" + AMT, t)
            m2 = re.search(r"TOTAL\s+U\$s\s*" + AMT, t)
            if m1 and m2:
                neto = round(total * num(m1.group(1)) / num(m2.group(1)), 2)
                how_n = "usd_proporcional"
                note.append("Factura en dólares, convertida al tipo de cambio impreso")
        elif tipo == "C":
            neto, how_n = total, "factura_c"
        else:
            neto, how_n = first(NETO_PATS, t)
    if tipo == "C":
        neto = total
    if tipo.startswith("NC"):
        total = -abs(total) if total else total
        neto = -abs(neto) if neto else neto
        note.append("Nota de crédito")
    if total and neto and not (0.70 <= neto / total <= 1.0001):
        note.append(f"Revisar: neto/total = {neto / total:.2f}")
    return dict(
        archivo=rel,
        carpeta_mes=folder_month(rel),
        carpeta_proveedor=rel.split("/")[1] if rel.count("/") >= 2 else "",
        fecha=parse_date(t),
        cuit=cuit,
        razon_social=razon,
        tipo=tipo,
        cae=cae,
        neto=neto,
        total=total,
        metodo=f"{how_n}/{how_t}",
        fuente="pdf",
        nota="; ".join(note),
    )
