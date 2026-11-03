"""Exporta los CSV que lee el tablero (data/tablero/*.csv) desde data/dashboard.json."""
import csv
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "tablero"


def write(name, cols, rows):
    OUT.mkdir(exist_ok=True)
    with (OUT / f"{name}.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if r.get(c) is None else r.get(c) for c in cols])
    return OUT / f"{name}.csv"


def main():
    d = json.loads((DATA / "dashboard.json").read_text())
    f = d["facturas"]
    write("facturas", ["fecha", "mes", "proveedor", "rubro", "tipo", "neto", "total", "fuente",
                       "detalle", "archivo", "nota"],
          [dict(r, detalle={"ok": "completo", "servicio": "servicio", "no_cierra": "no cierra",
                            "sin_detalle": "sin detalle"}.get(r["renglones"], r["renglones"]),
                fuente="foto" if r["fuente"] == "foto" else "PDF",
                neto=round(r["neto"] or 0, 2), total=round(r["total"] or 0, 2)) for r in f])
    write("renglones", ["id", "fecha", "mes", "proveedor", "grupo", "insumo", "descripcion", "cantidad", "unidad",
                        "importe", "unidad_base", "cantidad_base", "precio_base", "atipico", "archivo"],
          [dict(r, id=f"r{n}", insumo=r["ingrediente"], atipico="si" if r.get("atipico") else "no")
           for n, r in enumerate(d["renglones"], 1)])
    write("costos_excel", ["ingrediente", "sku", "unidad", "costo"],
          [dict(e, sku=str(e["sku"]) if e["sku"] else "") for e in d["costos_excel"]])

    c = d["calidad"]
    issues = []
    for x in c["carpetas_no_descargadas"]:
        issues.append(dict(tema="Carpeta que OneDrive no descargó", archivo=x, proveedor=x.split("/")[-1],
                           detalle="Faltan sus facturas en la copia local"))
    for x in c["duplicados"]:
        issues.append(dict(tema="Factura repetida", archivo=x["archivo"], proveedor="Eggs Hons",
                           detalle="Mismo CAE que " + x["duplicado_de"] + ". Se cuenta una sola vez"))
    for x in c["fotos"]:
        issues.append(dict(tema="Factura solo en foto", archivo=x, proveedor=x.split("/")[1],
                           detalle="Transcripta a mano desde la imagen"))
    for x in c["facturas_en_otro_mes"]:
        tema = "Factura de 2025" if x["fecha"] < "2026" else "Archivada en otro mes"
        issues.append(dict(tema=tema, archivo=x["archivo"], proveedor=x["proveedor"],
                           detalle=f"Emitida el {x['fecha']}, guardada en la carpeta del mes {x['carpeta_mes']}"))
    for prov, folders in c["proveedor_en_varias_carpetas"].items():
        issues.append(dict(tema="Proveedor en varias carpetas", archivo="", proveedor=prov,
                           detalle=" · ".join(folders)))
    for x in c["notas"]:
        if "crédito" in x["nota"] or "prorrateados" in x["nota"] or "dólares" in x["nota"]:
            tema = ("Nota de crédito" if "crédito" in x["nota"] else
                    "Factura en dólares" if "dólares" in x["nota"] else "Descuento global prorrateado")
            issues.append(dict(tema=tema, archivo=x["archivo"], proveedor=x["archivo"].split("/")[1] if x["archivo"].count("/") > 1 else "",
                               detalle=x["nota"]))
    ex = c["excel"]
    for i in ex["costo_cero"]:
        issues.append(dict(tema="Excel: ingrediente con costo en cero", archivo="Costos/CostoDeIngredientes_actualizado.xlsx", proveedor="", detalle=i))
    for i in ex["sin_sku"]:
        issues.append(dict(tema="Excel: ingrediente sin código", archivo="Costos/CostoDeIngredientes_actualizado.xlsx", proveedor="", detalle=i))
    for i in ex["duplicados"]:
        issues.append(dict(tema="Excel: ingrediente repetido", archivo="Costos/CostoDeIngredientes_actualizado.xlsx", proveedor="", detalle=i))
    for n, x in enumerate(issues, 1):
        x["id"] = f"c{n}"
    write("calidad", ["id", "tema", "proveedor", "detalle", "archivo"], issues)
    for p in sorted(OUT.glob("*.csv")):
        print(p.name, p.stat().st_size)


if __name__ == "__main__":
    main()
