"""Renglones de cada factura PDF por consistencia aritmética: cantidad x precio = importe.

No hay un parser por proveedor. En cada línea con descripción e importes se busca un par
(cantidad, precio) cuyo producto coincida con algún importe de la misma línea.
"""
import re
from common import num_ar, num_us
from suppliers import US_FORMAT, NO_ITEMS

NUM_TOKEN = re.compile(r"(?<![\w/])-?\d[\d.,]*\d|(?<![\w/.,])\d(?![\w/])")
SKIP = re.compile(
    r"^\s*i\.?v\.?a\.?\b|\b(sub\s?total|total|neto|iva\s*:|vat\s|untaxed|percep|perc\.|cae|"
    r"importe\s+otros|son\s+pesos|tipo\s+de\s+cambio|saldo|vencimiento|bultos\s*:|cuit|"
    r"remito|ingresos\s+brutos|fecha|cbu|tel[:.]|alias|c[oó]digo\s+de\s+pago|pedido#|"
    r"facturas\s+pendientes|importe\s+actual|página|p[aá]g\.)",
    re.I,
)
UNIT_RE = re.compile(r"\b(kg|kgs|kilogramo|kilogramos|kilo|lt|lts|litro|litros|bol|u|un|unid|unidades|bts)\b\.?", re.I)
COPY_WORDS = re.compile(r"\b(ORIGINAL|DUPLICADO|TRIPLICADO|CUADRUPLICADO)\b")


def unique_pages(text):
    pages, seen = [], set()
    for p in text.split("\f"):
        key = re.sub(r"\s+", " ", COPY_WORDS.sub("", p)).strip()
        if key and key not in seen:
            seen.add(key)
            pages.append(p)
    return pages


def tokens(line, us):
    # Los códigos entre corchetes ([PBTS-30.065]) no son números de la factura
    clean = re.sub(r"\[[^\]]*\]", lambda m: " " * len(m.group(0)), line)
    out = []
    for m in NUM_TOKEN.finditer(clean):
        s = m.group(0)
        try:
            v = num_us(s) if us else num_ar(s)
        except ValueError:
            continue
        out.append((m.start(), m.end(), s, v))
    return out


def has_money_format(s, us):
    """Un importe tiene 2 o 4 decimales con el separador decimal del formato."""
    sep = "." if us else ","
    return bool(re.search(re.escape(sep) + r"\d{2}(\d{2})?$", s))


def describe(line, toks, used=(), us=False):
    """Texto del renglón sin cantidad, precio, importes ni números de lote."""
    desc = re.sub(r"\[[^\]]*\]", lambda m: " " * len(m.group(0)), line)  # [CODIGO]
    is_used = [any(abs(abs(v) - u) < 1e-6 for u in used if u) for (_, _, _, v) in toks]
    m_letter = re.search(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]{2,}", desc)
    first_letter = m_letter.start() if m_letter else 0
    # columnas numéricas a la derecha de la descripción (la cantidad al inicio de línea no cuenta)
    first_used = min((t[0] for t, u in zip(toks, is_used) if u and t[0] > first_letter), default=len(line))
    for k in range(len(toks) - 1, -1, -1):
        a, b, s, v = toks[k]
        before_used = k + 1 < len(toks) and is_used[k + 1] and not line[b:toks[k + 1][0]].strip()
        leading_code = not line[:a].strip() and re.fullmatch(r"\d{2,}", s) and not is_used[k]
        drop = (has_money_format(s, us) or is_used[k] or len(re.sub(r"\D", "", s)) >= 6
                or (a > first_used) or (before_used and re.fullmatch(r"\d+", s)) or leading_code)
        if drop:
            desc = desc[:a] + " " * (b - a) + desc[b:]
    desc = re.sub(r"\$|%|\bIVA\b|U\$s|\(copia\)", " ", desc)
    desc = re.sub(r"^\s*[*\-]?\s*[A-Z0-9]{2,}-[\w-]*\s+", " ", desc)       # DB-DRIPPER-V02, DROV-
    desc = re.sub(r"^\s*[A-Z]\d{2}[A-Z]\b\s*-?", " ", desc)                 # N42K - (Puerto Blest)
    desc = re.sub(r"^\s*[A-Z]{2,}[A-Z0-9]*\d[A-Z0-9-]*\s+(?=[A-Z])", " ", desc)  # PAPBOB266024002
    desc = re.sub(r"\b(unidades|kilogramo|kilogramos)\b", " ", desc, flags=re.I)
    desc = re.sub(r"\s+-\s+", " ", desc)
    desc = re.sub(r"\s+", " ", desc).strip(" -.:")
    return desc


def best_match(toks, us, carry_qty=None):
    """(cantidad, precio, importe, bonif%) tal que cantidad x precio x (1 - bonif) = importe."""
    if not any(has_money_format(t[2], us) for t in toks):
        return None
    if toks and abs(toks[-1][3]) < 0.005 and has_money_format(toks[-1][2], us):
        return None  # renglón bonificado al 100 % (importe final 0)
    for ci in range(len(toks) - 1, 0, -1):
        imp = abs(toks[ci][3])
        if imp <= 0 or not has_money_format(toks[ci][2], us):
            continue
        tol = max(1.0, imp * 0.006)
        before = toks[:ci]
        bons = (0.0,) + tuple(abs(t[3]) for t in before if 0 < abs(t[3]) < 60)
        pairs = [(i, j) for i in range(len(before)) for j in range(len(before)) if i < j]
        pairs += [(j, i) for i, j in pairs]  # primero cantidad a la izquierda del precio
        for i, j in pairs:
            q, p = abs(before[i][3]), abs(before[j][3])
            if q <= 0 or p <= 0 or q > 100000:
                continue
            for bon in bons:
                if abs(q * p * (1 - bon / 100) - imp) <= tol:
                    return q, p, imp, bon
        if carry_qty:  # cantidad impresa en la línea anterior (Papelera Rodes)
            for t in before:
                if t[3] > 0 and abs(carry_qty * t[3] - imp) <= tol:
                    return carry_qty, t[3], imp, 0.0
    return None


def parse_items(rel, text, header):
    cuit = header.get("cuit")
    if cuit in NO_ITEMS or header.get("tipo") == "Expensas":
        return []
    us = cuit in US_FORMAT
    items = []
    sign = -1 if str(header.get("tipo", "")).startswith("NC") else 1
    has_letters = re.compile(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]{3,}")
    for page in unique_pages(text):
        prev_text, carry_qty = "", None
        for line in page.splitlines():
            if not line.strip():
                continue
            if SKIP.search(line):
                prev_text, carry_qty = "", None
                continue
            toks = tokens(line, us)
            m = best_match(toks, us, carry_qty) if len(toks) >= 2 else None
            if not m:
                mq = re.match(r"^\s*(\d{1,4})\s+\S+\s*$", line)  # "1 QUITDT313135L01"
                carry_qty = float(mq.group(1)) if mq else None
                if has_letters.search(line) and not mq:
                    prev_text = line
                continue
            q, p, imp, bon = m
            used = (q, p, imp, bon)
            desc = describe(line, toks, used, us)
            if not has_letters.search(desc) and prev_text:
                desc = describe(prev_text, tokens(prev_text, us), used, us)
            if not has_letters.search(desc):
                continue
            um = UNIT_RE.search(line)
            unit = um.group(1).lower() if um else "u"
            unit = {"kgs": "kg", "kilogramo": "kg", "kilogramos": "kg", "kilo": "kg",
                    "lts": "lt", "litro": "lt", "litros": "lt",
                    "un": "u", "unid": "u", "unidades": "u", "bts": "u", "bol": "u"}.get(unit, unit)
            items.append(dict(archivo=rel, descripcion=desc, cantidad=q, unidad=unit,
                              precio_unitario=round(p, 4), bonif=bon, importe=round(sign * imp, 2)))
            prev_text, carry_qty = "", None
    return items
