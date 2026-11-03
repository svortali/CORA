"""Propone data/mapeo_ingredientes.csv a partir de los renglones de data/dashboard.json.

Cada fila dice a qué insumo corresponde una descripción de proveedor y cuántas unidades base
(kg, lt o unidad) trae cada unidad facturada. Las filas con revisado=si no se tocan, así que el
archivo se puede corregir a mano y volver a correr.

Uso:  python3 pipeline/build_data.py && python3 pipeline/propose_mapping.py && python3 pipeline/build_data.py
"""
import csv
import json
import re
from collections import defaultdict, Counter
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "mapeo_ingredientes.csv"

KG = "kg"   # factor: 1 si el renglón viene en kg; N si dice "CAJA 18 KG"; vacío si es bolsa/atado
PACK = "pack"  # factor: N de "X 50UN" / "X 5LTS"; 1 si no hay presentación

# (regex sobre la descripción, regex de proveedor o None, insumo, grupo, unidad_base, factor)
RULES = [
    # --- reglas por proveedor primero
    (r"GRANOLA 1/2 KG", "Leo Pastelera", "GRANOLA", "Almacén", "kg", 0.5),
    (r"^CHIPA$", "Leo Pastelera", "CHIPA PRENSADO", "Pastelería comprada", "u", 1),
    (r"^CAJAS?$", "Leo Pastelera", "CAJAS PASTELERÍA", "Descartables", "u", 1),
    (r"LAMI?N?I?A?N?DOS|PANADERIA", "Cuadra", "LAMINADOS Y PANADERÍA (CUADRA)", "Pastelería comprada", None, None),
    (r"DELIVERY|ENVIO|ENVÍO|FLETE|LOGISTICA", None, "ENVÍOS Y LOGÍSTICA", "Envíos", None, None),
    (r"EVENTO|TORTA CUMPLE", "Leo Pastelera", "PASTELERÍA PARA EVENTOS", "Pastelería comprada", None, None),
    (r".", "Leo Pastelera", "__DESC__", "Pastelería comprada", "u", 1),
    (r"TARTAS", "Celeste Ure", "TARTAS", "Pastelería comprada", None, None),
    (r".", "Umami", "VINO", "Almacén", "u", 1),
    (r".", "Volf|Domestic Boom", "VAJILLA Y EQUIPAMIENTO", "Equipamiento", None, None),
    (r"SERVICIO TECNICO|CAFIZA|GOMA|FILTRO TRIPLE|PRE FILTRO|DUCHA|GASKET|JUNTA", "Puerto Blest", "MANTENIMIENTO MÁQUINA DE CAFÉ", "Mantenimiento", None, None),
    (r"RESINA", None, "RESINAS (OBRA)", "Mantenimiento", None, None),
    (r"FRAMBUESA", "Avila", "FRAMBUESAS", "Almacén", None, None),
    # --- café y barra
    (r"CAFE .*1/4", None, "CAFÉ EN GRANO FILTRADO", "Café y barra", "kg", 0.25),
    (r"CAFE .*(X ?1 ?KG|X KG)", None, "CAFÉ EN GRANO TOLVA", "Café y barra", "kg", 1),
    (r"FILTROS? DE PAPEL V60.*X100", None, "FILTROS V60", "Café y barra", "u", 100),
    (r"AZUCAR EN SOBRE.*X800", None, "AZÚCAR EN SOBRES", "Café y barra", "u", 800),
    (r"EDULCORANTE.*X 400", None, "EDULCORANTE EN SOBRES", "Café y barra", "u", 400),
    (r"OATLY.*X6", None, "CAJON OATLY", "Café y barra", "lt", 6),
    (r"LECHE DE AVENA BARISTA NUDE", None, "LECHE DE AVENA MUY BUENO", "Café y barra", "u", 1),
    (r"ALMENDRAS SABOR ORIGINAL", None, "CAJON AMANDE", "Café y barra", "u", 1),
    (r"\bVERD\b|TE VERDE", "Pei Chen", "TE VERDE", "Café y barra", "kg", 1),
    (r"ROJO", "Pei Chen", "TE ROJO", "Café y barra", "kg", 1),
    (r"BLANCO", "Pei Chen", "TE BLANCO", "Café y barra", "kg", 1),
    (r"AGUA CON GAS.*X12", None, "AGUA CON GAS 500 ML", "Café y barra", "u", 12),
    (r"AGUA SIN GAS.*X12", None, "AGUA SIN GAS 500 ML", "Café y barra", "u", 12),
    (r"SIFON", None, "SIFON 1.5 LT", "Café y barra", "u", 1),
    # --- lácteos y huevos
    (r"ZERO LAC|REDUC LACTO|SIN LACTOSA", None, "LECHE SIN LACTOSA", "Lácteos y huevos", "lt", 1),
    (r"LECHE .*(DESCREMADA|P\.?DESC|PARC\.?DESC)", None, "LECHE DESCREMADA", "Lácteos y huevos", "lt", 1),
    (r"LECHE .*ENTERA", None, "LECHE ENTERA", "Lácteos y huevos", "lt", 1),
    (r"YOGU.*3\.?8 ?KG", None, "YOGURT", "Lácteos y huevos", "kg", 3.8),
    (r"MANTECA.*200 ?GR", None, "MANTECA PILON", "Lácteos y huevos", "kg", 0.2),
    (r"MANTECA", None, "MANTECA PILON", "Lácteos y huevos", "kg", 1),
    (r"DULCE DE LECHE.*400 ?GR", None, "DDL", "Lácteos y huevos", "kg", 0.4),
    (r"DULCE DE LECHE", None, "DDL", "Lácteos y huevos", "kg", 1),
    (r"CREMA.*200 ?CC", None, "CREMA", "Lácteos y huevos", "kg", 0.2),
    (r"CREMA DE LECHE|\bCREMA\b(?!.*(QUESO|CIF|BOTELLA))", None, "CREMA", "Lácteos y huevos", "kg", 1),
    (r"PASTORIL", None, "HUEVOS PASTORILES", "Lácteos y huevos", "u", 180),
    (r"MEDIO CAJON", None, "HUEVOS", "Lácteos y huevos", "u", 180),
    (r"CAJON HUEVO", None, "HUEVOS", "Lácteos y huevos", "u", 360),
    # --- quesos
    (r"CUARTIROLO", None, "QUESO CUARTIROLO", "Quesos", "kg", 1),
    (r"SARDO", None, "QUESO SARDO", "Quesos", "kg", 1),
    (r"BRANDSEN", None, "QUESO BRANDSEN", "Quesos", "kg", 1),
    (r"BRIE", None, "QUESO BRIE", "Quesos", "kg", 1),
    (r"TYBO", None, "QUESO TYBO", "Quesos", "kg", 1),
    (r"PATAGONZOLA", None, "PATAGONZOLA", "Quesos", "kg", 1),
    (r"QUESO CREMA.*500 ?GR", None, "QUESO CREMA", "Quesos", "kg", 0.5),
    (r"QUESO CREMA", None, "QUESO CREMA", "Quesos", "kg", 1),
    (r"RICOT.*500 ?GR", None, "RICOTA", "Quesos", "kg", 0.5),
    (r"RICOT", None, "RICOTA", "Quesos", "kg", 1),
    # --- fiambres
    (r"PROSCIUTTO COTTO|JAMON COCIDO", None, "JAMON COCIDO", "Fiambres", "kg", 1),
    (r"JAMON CRUDO", None, "JAMON CRUDO", "Fiambres", "kg", 1),
    (r"MORTADEL", None, "MORTADELA PISTACHO", "Fiambres", "kg", 1),
    (r"CHORIZO", None, "CHORIZO ESPANOL", "Fiambres", "kg", 1),
    (r"ASADITO", None, "ASADITO FETEADO", "Fiambres", "kg", 1),
    (r"SPIANATA", None, "SPIANATA", "Fiambres", "kg", 1),
    # --- verduras y frutas (por kg cuando se puede)
    (r"TOMATE", None, "TOMATE", "Verduras y frutas", "kg", KG),
    (r"\bLIMON", None, "LIMON", "Verduras y frutas", "kg", KG),
    (r"NARANJA", None, "NARANJA", "Verduras y frutas", "kg", KG),
    (r"ESPINACA", None, "ESPINACA", "Verduras y frutas", "kg", KG),
    (r"CEBOLL", None, "CEBOLLA MORADA", "Verduras y frutas", "kg", KG),
    (r"KIWI", None, "KIWI", "Verduras y frutas", "kg", KG),
    (r"\bPERA\b", None, "PERA", "Verduras y frutas", "kg", KG),
    (r"MANZANA|RED ELEGIDA", None, "MANZANA", "Verduras y frutas", "kg", KG),
    (r"MEZCLUM|MEZLCUM", None, "MEZCLUM", "Verduras y frutas", "kg", KG),
    (r"\bLIMA\b", None, "LIMA", "Verduras y frutas", "kg", KG),
    (r"POMELO", None, "POMELO", "Verduras y frutas", "kg", KG),
    (r"PALTA", None, "PALTA", "Verduras y frutas", "kg", KG),
    (r"JENGIBRE|JENJIBRE", None, "JENGIBRE", "Verduras y frutas", "kg", KG),
    (r"FRUTILLA X 250", None, "FRUTILLA", "Verduras y frutas", "kg", 0.25),
    (r"FRUTILLA", None, "FRUTILLA", "Verduras y frutas", "kg", KG),
    (r"CHAMPI", None, "CHAMPIÑON", "Verduras y frutas", "kg", KG),
    (r"BERENJENA", None, "BERENJENA", "Verduras y frutas", "kg", KG),
    (r"LECHUGA MORADA", None, "LECHUGA MORADA", "Verduras y frutas", "kg", KG),
    (r"FRANCESA", None, "LECHUGA FRANCESA", "Verduras y frutas", "kg", KG),
    (r"DURAZNO", None, "DURAZNO", "Verduras y frutas", "kg", KG),
    (r"ALBAHACA", None, "ALBAHACA", "Verduras y frutas", "u", 1),
    (r"MENTA", None, "MENTA", "Verduras y frutas", "u", 1),
    (r"RABANITO", None, "BROTES DE RABANITO", "Verduras y frutas", "u", 1),
    (r"BROTES", None, "MIX BROTES", "Verduras y frutas", "u", 1),
    (r"FLORES", None, "FLORES", "Verduras y frutas", "u", 1),
    (r"RUCULA", None, "RUCULA", "Verduras y frutas", "u", 1),
    (r"CIBULLETTE|KALE|ENELDO|PEREJIL|CILANTRO|VERDEO", None, None, "Verduras y frutas", "u", 1),
    # --- almacén
    (r"ACEITE DE OLIVA", None, "ACEITE OLIVA", "Almacén", "lt", 3),
    (r"ACEITUNA.*(1/2 ?KG|500 ?G)", None, "ACEITUNAS DESCAROZADA", "Almacén", "kg", 0.5),
    (r"ALMENDRA NON PAREIL", None, "ALMENDRAS", "Almacén", "kg", KG),
    (r"CASTANAS DE CAJU", None, "CASTAÑAS DE CAJÚ", "Almacén", "kg", KG),
    (r"\bNUEZ", None, "NUECES", "Almacén", "kg", KG),
    (r"\bMANI\b", None, "MANÍ", "Almacén", "kg", KG),
    (r"CHIA", None, "CHIA", "Almacén", "kg", KG),
    (r"MOSTAZA ALEMANA", None, "MOSTAZA ALEMANA", "Almacén", "kg", 1),
    (r"MOSTAZA CLASICA", None, "MOSTAZA CLASICA", "Almacén", "kg", 1),
    (r"AJI MOLIDO", None, "AJI", "Almacén", "kg", 1),
    (r"FINAS HIERBAS", None, "FINAS HIERBAS", "Almacén", "kg", 1),
    (r"\bMIEL\b", None, "MIEL", "Almacén", "kg", 1),
    (r"GRANOLA 1/2 KG", None, "GRANOLA", "Almacén", "kg", 0.5),
    # --- pastelería comprada (precio por pieza)
    (r"MEDIALUNA", None, "MEDIALUNA", "Pastelería comprada", "u", 1),
    (r"FOSFORITO", None, "FOSFORITO", "Pastelería comprada", "u", 1),
    (r"PALMERA", None, "PALMERA", "Pastelería comprada", "u", 1),
    (r"\bROLL\b", None, "ROLL DE CANELA", "Pastelería comprada", "u", 1),
    (r"BAGELS", None, "BAGEL", "Pastelería comprada", "u", 12),
    # --- descartables y limpieza (precio por unidad o por litro según presentación)
    (r"TAPA.*12 ?OZ", None, "TAPA VASO 12 OZ", "Descartables", "u", PACK),
    (r"TAPA.*8 ?(OZ|ONZAS)", None, "TAPA VASO 8 OZ", "Descartables", "u", PACK),
    (r"VASO.*12 ?(OZ|ONZAS)", None, "VASO 12 OZ", "Descartables", "u", PACK),
    (r"VASO.*8 ?(OZ|ONZAS)", None, "VASO 8 OZ", "Descartables", "u", PACK),
    (r"SERVILLETA", None, "SERVILLETAS", "Descartables", "u", PACK),
    (r"BOBINA|DOBLE HOJA THAMES", None, "BOBINA DE PAPEL", "Descartables", "u", PACK),
    (r"DRAYHAND|TOALLA", None, "TOALLAS DE MANO", "Descartables", "u", PACK),
    (r"BOLSA CONSORCIO|CONSORCIO BD|BOLSA RESIDUOS", None, "BOLSAS DE RESIDUOS", "Descartables", "u", PACK),
    (r"KRAFT", None, "BOLSAS KRAFT", "Descartables", "u", PACK),
    (r"GUANTE", None, "GUANTES DE NITRILO", "Descartables", "u", PACK),
    (r"ROLLO TERMICO", None, "ROLLO TÉRMICO", "Descartables", "u", PACK),
    (r"PAPEL HIGIENICO|PAP HIG", None, "PAPEL HIGIÉNICO", "Descartables", "u", None),
    (r"FILM", None, "FILM", "Descartables", "u", None),
    (r"LAVANDINA", None, "LAVANDINA", "Limpieza", "lt", PACK),
    (r"DETERGENTE(?!.*CAFIZA)", None, "DETERGENTE", "Limpieza", "lt", PACK),
    (r"ALCOHOL", None, "ALCOHOL", "Limpieza", "lt", PACK),
    (r"(DESINFECTANTE|DESODORANTE).*PISO|PISO.*(DESINF|DESOD)", None, "LIMPIADOR DE PISOS", "Limpieza", "lt", PACK),
]


def factor_for(spec, desc, units):
    if spec == KG:
        if re.search(r"\bBTS\b|\bU\b|\bPAQ\b|PROMO X$", desc):
            return None
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*(KG|KILOS?)\b", desc)
        if m and float(m.group(1).replace(",", ".")) >= 2:
            return float(m.group(1).replace(",", "."))
        m = re.search(r"(\d+)\s*GR?\b", desc)
        if m and int(m.group(1)) >= 100:
            return int(m.group(1)) / 1000
        return "kg"  # build_data lo aplica solo a renglones facturados en kg
    if spec == PACK:
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*(LTS?|LT|L)\b", desc)
        if m:
            return float(m.group(1).replace(",", "."))
        m = re.search(r"X\s*(\d+)\s*(UN|U)\b", desc)
        if m:
            return float(m.group(1))
        return None  # sin presentación: no se compara precio unitario
    return spec


def main():
    d = json.loads((DATA / "dashboard.json").read_text())
    agg = defaultdict(lambda: dict(n=0, gasto=0.0, units=Counter()))
    for r in d["renglones"]:
        a = agg[(r["proveedor"], r["desc_norm"])]
        a["n"] += 1
        a["gasto"] += r["importe"]
        a["units"][r["unidad"]] += 1
    existing = {}
    if OUT.exists():
        for r in csv.DictReader(OUT.open(encoding="utf-8-sig")):
            if r.get("revisado", "").strip().lower() in ("si", "sí", "s", "x"):
                existing[(r["proveedor"], r["descripcion"])] = r
    excel = {e["ingrediente"] for e in d["costos_excel"]}
    rows = []
    for (prov, desc), a in sorted(agg.items(), key=lambda kv: -kv[1]["gasto"]):
        if (prov, desc) in existing:
            row = existing[(prov, desc)]
            row.update(renglones=a["n"], gasto=round(a["gasto"]))
            rows.append(row)
            continue
        ing = grupo = ub = fac = None
        regla = ""
        for pat, prov_pat, i, g, u, f in RULES:
            if (prov_pat is None or re.search(prov_pat, prov)) and re.search(pat, desc):
                ing, grupo, ub = i, g, u
                fac = factor_for(f, desc, a["units"]) if f is not None else None
                regla = pat
                if ing == "__DESC__":
                    ing = desc
                if ing is None and g == "Verduras y frutas":
                    ing = desc.split()[0]
                break
        rows.append(dict(proveedor=prov, descripcion=desc, ingrediente=ing or "", grupo=grupo or "",
                         unidad_base=ub or "", factor="" if fac is None else fac,
                         en_excel="si" if ing in excel else "", regla=regla, revisado="",
                         renglones=a["n"], gasto=round(a["gasto"])))
    cols = ["proveedor", "descripcion", "ingrediente", "grupo", "unidad_base", "factor",
            "en_excel", "regla", "revisado", "renglones", "gasto"]
    with OUT.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    tot = sum(r["gasto"] for r in rows)
    mapped = sum(r["gasto"] for r in rows if r["ingrediente"])
    priced = sum(r["gasto"] for r in rows if r["ingrediente"] and str(r["factor"]) != "")
    print(f"{len(rows)} descripciones. Gasto mapeado {mapped / tot:.0%}, con precio unitario comparable {priced / tot:.0%}")
    print("Insumos:", len({r['ingrediente'] for r in rows if r['ingrediente']}))


if __name__ == "__main__":
    main()
