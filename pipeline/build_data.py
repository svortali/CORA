"""Arma data/dashboard.json y los CSV de salida a partir de INPUT/2026.

Uso:  python3 pipeline/build_data.py
"""
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict, Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DATA, INPUT, ROOT, MONTHS, extract_all, iter_pdf_texts, folder_month  # noqa: E402
from parse_invoices import parse_header  # noqa: E402
from parse_items import parse_items  # noqa: E402
from suppliers import RUBROS, NO_ITEMS, supplier  # noqa: E402

MAPEO = DATA / "mapeo_ingredientes.csv"
FOTOS = DATA / "fotos_manual.csv"
EXCEL = INPUT / "Costos" / "CostoDeIngredientes_actualizado.xlsx"


def norm(desc):
    s = unicodedata.normalize("NFKD", desc).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"^\(\d{2}/\d{2}\)\s*", "", s)          # "(22/01) JAMON COCIDO"
    s = re.sub(r"^\*\s*", "", s)                        # "* 30500 LECHE ..." (La Serenísima)
    s = re.sub(r"^(?:\d{2,}|[A-Z]?-?SEIQ)\s+(?=[A-Z])", "", s)  # código de artículo inicial
    s = re.sub(r"\s+", " ", s).strip(" .-")
    return s


def load_photos():
    heads, items = {}, []
    if not FOTOS.exists():
        return heads, items
    for r in csv.DictReader(FOTOS.open(encoding="utf-8")):
        rel = r["archivo_rel"]
        d, m, y = r["fecha"].split("/")
        heads.setdefault(rel, dict(
            archivo=rel, carpeta_mes=folder_month(rel),
            carpeta_proveedor=rel.split("/")[1], fecha=f"{y}-{m}-{d}",
            cuit=r["cuit_emisor"], razon_social=r["razon_social"], tipo=r["tipo"],
            cae=None, nro=r["nro_comprobante"], neto=float(r["neto"]), total=float(r["total"]),
            metodo="foto", fuente="foto", nota="Transcripta de la foto"))
        items.append(dict(archivo=rel, descripcion=r["descripcion"], cantidad=float(r["cantidad"]),
                          unidad=r["unidad"], precio_unitario=float(r["precio_unitario"]),
                          bonif=0.0, importe=float(r["importe"])))
    return heads, items


def load_mapping():
    m = {}
    if MAPEO.exists():
        for r in csv.DictReader(MAPEO.open(encoding="utf-8-sig")):
            m[(r["proveedor"], r["descripcion"])] = r
    return m


def load_excel():
    try:
        import openpyxl
    except ImportError:
        return []
    wb = openpyxl.load_workbook(EXCEL, data_only=True)
    out = []
    for row in list(wb.worksheets[0].iter_rows(values_only=True))[1:]:
        if not row or not row[1]:
            continue
        cat, ing, sku, uni, costo, merma = (list(row) + [None] * 7)[:6]
        uni = {"KG": "kg", "LT": "lt", "L": "lt"}.get(str(uni).upper(), "u") if uni else "u"
        out.append(dict(ingrediente=str(ing).strip(), sku=sku, unidad=uni, costo=costo or 0,
                        merma=merma or 0))
    return out


def month_key(fecha):
    return fecha[:7] if fecha else None


def main():
    n_new = extract_all()
    headers, items = [], []
    for rel, text in iter_pdf_texts():
        h = parse_header(rel, text)
        h["_text_has_desc"] = bool(re.search(r"descuento", text, re.I))
        headers.append(h)
        items.extend(parse_items(rel, text, h))
    ph, pi = load_photos()
    headers.extend(ph.values())
    items.extend(pi)

    # --- deduplicar por CAE
    seen, dupes, keep = {}, [], []
    for h in headers:
        if h.get("cae") and h["cae"] in seen:
            dupes.append(dict(archivo=h["archivo"], duplicado_de=seen[h["cae"]], cae=h["cae"]))
            continue
        if h.get("cae"):
            seen[h["cae"]] = h["archivo"]
        keep.append(h)
    headers = keep
    dupe_files = {d["archivo"] for d in dupes}
    items = [i for i in items if i["archivo"] not in dupe_files]

    by_file = defaultdict(list)
    for i in items:
        by_file[i["archivo"]].append(i)

    # --- enriquecer cabeceras y cerrar renglones contra el neto
    no_cierra = []
    for h in headers:
        name, rubro = supplier(h["cuit"], h.get("razon_social") or h["carpeta_proveedor"])
        h["proveedor"], h["rubro"] = name, rubro
        h["mes"] = month_key(h["fecha"])
        its = by_file.get(h["archivo"], [])
        s = sum(i["importe"] for i in its)
        neto = h["neto"] or 0
        h["n_renglones"] = len(its)
        if h["cuit"] in NO_ITEMS or h["tipo"] == "Expensas":
            h["renglones"] = "servicio"
        elif not its:
            h["renglones"] = "sin_detalle"
        elif abs(s - neto) <= max(2, abs(neto) * 0.01) or abs(s - (h["total"] or 0)) <= max(2, abs(h["total"] or 0) * 0.01):
            h["renglones"] = "ok"
        elif neto and s and ("dólares" in h["nota"] or (0.4 <= neto / s < 1 and h.get("_text_has_desc"))):
            f = neto / s
            for i in its:
                i["importe"] = round(i["importe"] * f, 2)
                i["precio_unitario"] = round(i["precio_unitario"] * f, 4)
            h["renglones"] = "ok"
            h["nota"] = "; ".join(x for x in [h["nota"], f"Renglones prorrateados x{f:.4f} (descuento global o moneda)"] if x)
        else:
            h["renglones"] = "no_cierra"
            no_cierra.append(dict(archivo=h["archivo"], proveedor=name, neto=neto, suma_renglones=round(s, 2)))
        h.pop("_text_has_desc", None)
        for i in its:
            i["proveedor"], i["rubro"], i["mes"], i["fecha"] = name, rubro, h["mes"], h["fecha"]

    # --- mapeo a ingredientes
    mapping = load_mapping()
    for i in items:
        i["desc_norm"] = norm(i["descripcion"])
        m = mapping.get((i["proveedor"], i["desc_norm"]))
        i["ingrediente"] = i["grupo"] = i["unidad_base"] = i["cantidad_base"] = i["precio_base"] = None
        if m and m.get("ingrediente"):
            i["ingrediente"], i["grupo"] = m["ingrediente"], m.get("grupo") or None
            spec = (m.get("factor") or "").strip().lower()
            if spec == "kg":   # vale solo para renglones facturados por kilo
                f = 1.0 if i["unidad"] == "kg" else None
            else:
                try:
                    f = float(spec.replace(",", ".")) if spec else None
                except ValueError:
                    f = None
            if f:
                i["unidad_base"] = m.get("unidad_base") or i["unidad"]
                i["cantidad_base"] = round(abs(i["cantidad"]) * f, 4)
                i["precio_base"] = round(abs(i["importe"]) / i["cantidad_base"], 2) if i["cantidad_base"] else None

    # precios atípicos: más de 3 veces lejos de la mediana del insumo
    by_ing = defaultdict(list)
    for i in items:
        if i["precio_base"]:
            by_ing[(i["ingrediente"], i["unidad_base"])].append(i["precio_base"])
    for i in items:
        i["atipico"] = False
        if i["precio_base"]:
            v = sorted(by_ing[(i["ingrediente"], i["unidad_base"])])
            med = v[len(v) // 2]
            i["atipico"] = not (med / 3 <= i["precio_base"] <= med * 3)

    # --- calidad de datos
    errors_file = INPUT.parent / "___All_Errors.txt"
    faltantes = []
    if errors_file.exists():
        faltantes = re.findall(r"^\d+\.\s*2026/(.+)$", errors_file.read_text(errors="replace"), re.M)
    carpetas_por_cuit = defaultdict(set)
    for h in headers:
        if h["fuente"] in ("pdf", "foto") and h["carpeta_proveedor"]:
            carpetas_por_cuit[h["proveedor"]].add(h["carpeta_proveedor"])
    desfasadas = []
    for h in headers:
        if h["fecha"] and h["carpeta_mes"]:
            fm = int(h["fecha"][5:7]) + (12 * (int(h["fecha"][:4]) - 2026))
            d = h["carpeta_mes"] - fm
            if d != 0:
                desfasadas.append(dict(archivo=h["archivo"], proveedor=h["proveedor"], fecha=h["fecha"],
                                       carpeta_mes=h["carpeta_mes"], meses_de_diferencia=d))
    excel = load_excel()
    calidad = dict(
        carpetas_no_descargadas=faltantes,
        duplicados=dupes,
        fotos=[h["archivo"] for h in headers if h["fuente"] == "foto"],
        facturas_en_otro_mes=desfasadas,
        renglones_que_no_cierran=no_cierra,
        proveedor_en_varias_carpetas={k: sorted(v) for k, v in carpetas_por_cuit.items() if len(v) > 1},
        excel=dict(
            ingredientes=len(excel),
            costo_cero=[e["ingrediente"] for e in excel if not e["costo"]],
            duplicados=[k for k, v in Counter(e["ingrediente"] for e in excel).items() if v > 1],
            sin_sku=[e["ingrediente"] for e in excel if not e["sku"]],
            merma_cargada=sum(1 for e in excel if e["merma"]),
        ),
        notas=[dict(archivo=h["archivo"], nota=h["nota"]) for h in headers if h.get("nota")],
    )

    # --- salida
    headers.sort(key=lambda h: (h["fecha"] or "", h["proveedor"]))
    hkeys = ["fecha", "mes", "proveedor", "rubro", "cuit", "tipo", "neto", "total", "fuente",
             "renglones", "n_renglones", "archivo", "carpeta_mes", "nota"]
    ikeys = ["fecha", "mes", "proveedor", "rubro", "descripcion", "desc_norm", "cantidad", "unidad",
             "precio_unitario", "bonif", "importe", "ingrediente", "grupo", "unidad_base", "cantidad_base",
             "precio_base", "atipico", "archivo"]
    bundle = dict(
        generado=date.today().isoformat(),
        rubros=RUBROS,
        facturas=[{k: h.get(k) for k in hkeys} for h in headers],
        renglones=[{k: i.get(k) for k in ikeys} for i in items],
        costos_excel=excel,
        calidad=calidad,
    )
    DATA.mkdir(exist_ok=True)
    (DATA / "dashboard.json").write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")))
    with (ROOT / "facturas_2026.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(hkeys)
        for h in bundle["facturas"]:
            w.writerow([str(h[k]).replace(".", ",") if isinstance(h[k], float) else ("" if h[k] is None else h[k]) for k in hkeys])
    with (ROOT / "renglones_2026.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(ikeys)
        for i in bundle["renglones"]:
            w.writerow([str(i[k]).replace(".", ",") if isinstance(i[k], float) else ("" if i[k] is None else i[k]) for k in ikeys])

    st = Counter(h["renglones"] for h in headers)
    mapped = sum(1 for i in items if i["ingrediente"])
    print(f"PDF nuevos extraídos: {n_new}")
    print(f"Facturas: {len(headers)} (duplicadas descartadas: {len(dupes)})  renglones: {len(items)}  mapeados: {mapped}")
    print(f"Estado de renglones: {dict(st)}")
    print(f"Neto: {sum(h['neto'] or 0 for h in headers):,.2f}   Total: {sum(h['total'] or 0 for h in headers):,.2f}")


if __name__ == "__main__":
    main()
