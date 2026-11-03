"""Proveedores conocidos: CUIT -> (nombre corto, rubro). Editar acá para reclasificar."""

RUBROS = [
    "Café e insumos de barra",
    "Lácteos, quesos y fiambres",
    "Pastelería y panificados",
    "Verdulería y frutas",
    "Almacén, secos y vinos",
    "Descartables y limpieza",
    "Equipamiento y vajilla",
    "Alquiler y expensas",
    "Servicios y terceros",
]

SUPPLIERS = {
    # Café e insumos de barra
    "30714833479": ("Puerto Blest", "Café e insumos de barra"),
    "30718544196": ("Porto Espresso", "Café e insumos de barra"),
    "30718540417": ("Oatly (Chealimentos)", "Café e insumos de barra"),
    "30715996878": ("Muy Bueno Co", "Café e insumos de barra"),
    "30715435981": ("Amande", "Café e insumos de barra"),
    "20954558186": ("Pei Chen Tea Palace", "Café e insumos de barra"),
    "30717576922": ("Morgade", "Café e insumos de barra"),
    # Lácteos, quesos y fiambres
    "30714335894": ("Abascay", "Lácteos, quesos y fiambres"),
    "33606956849": ("Las Dinas", "Lácteos, quesos y fiambres"),
    "30647506190": ("El Puente", "Lácteos, quesos y fiambres"),
    "30708248238": ("La Meson", "Lácteos, quesos y fiambres"),
    "30715067605": ("La Delfina", "Lácteos, quesos y fiambres"),
    "30707210385": ("La Serenísima", "Lácteos, quesos y fiambres"),
    "30716347415": ("Eggs Hons", "Lácteos, quesos y fiambres"),
    "30716712628": ("Tuetano (Corte)", "Lácteos, quesos y fiambres"),
    # Pastelería y panificados
    "20400103209": ("Leo Pastelera", "Pastelería y panificados"),
    "30719110017": ("Cuadra (Obrador BA)", "Pastelería y panificados"),
    "30717314251": ("Cuadra (Pibil)", "Pastelería y panificados"),
    "27291958627": ("Celeste Ure", "Pastelería y panificados"),
    "20442615498": ("Franco Groppo", "Pastelería y panificados"),
    "27416215338": ("Tout Gluten Free", "Pastelería y panificados"),
    "20430310993": ("El Massa", "Pastelería y panificados"),
    "27355969709": ("Avila Frenkel (mermeladas)", "Pastelería y panificados"),
    "30713351802": ("Sheikob's", "Pastelería y panificados"),
    # Verdulería y frutas
    "30708808322": ("La Nueva de Palermo", "Verdulería y frutas"),
    "30707702334": ("Cidel Orgánica", "Verdulería y frutas"),
    # Almacén, secos y vinos
    "30715347020": ("Quercus", "Almacén, secos y vinos"),
    "30708210680": ("Olivos Patagónicos", "Almacén, secos y vinos"),
    "30710858000": ("Consultora Umami (vinos)", "Almacén, secos y vinos"),
    # Descartables y limpieza
    "30716409798": ("Papelera Rodes", "Descartables y limpieza"),
    "30715272659": ("Distrigama", "Descartables y limpieza"),
    # Equipamiento y vajilla
    "30504363879": ("Volf", "Equipamiento y vajilla"),
    "30636491213": ("Domestic Boom", "Equipamiento y vajilla"),
    # Alquiler y expensas
    "20253851415": ("Alquiler Florida 1045 (Paragamian)", "Alquiler y expensas"),
    "30536235554": ("Expensas Consorcio Florida 1065", "Alquiler y expensas"),
    # Servicios y terceros
    "27248506208": ("Limpieza (Fernández)", "Servicios y terceros"),
    "23131809239": ("Electricista (Cassino)", "Servicios y terceros"),
    "27417792703": ("Diseño (Fornieles)", "Servicios y terceros"),
    "20324374664": ("Honorarios (Jaraj)", "Servicios y terceros"),
    "27342586665": ("Contadora (García)", "Servicios y terceros"),
    "33709746109": ("Bistrosoft", "Servicios y terceros"),
    "20245604239": ("Gráfica (Ariza)", "Servicios y terceros"),
    "30709937932": ("Resilent (resinas)", "Servicios y terceros"),
}

# Proveedores cuyos PDF usan formato numérico inglés (1,234.56)
US_FORMAT = {"30647506190", "33606956849", "30708248238", "33709746109",
             "30710858000", "30636491213", "27342586665", "30717576922"}

# Proveedores de servicios: no tienen renglones de materias primas
NO_ITEMS = {"20253851415", "30536235554", "27248506208", "23131809239", "27417792703",
            "20324374664", "27342586665", "33709746109", "20245604239"}


def supplier(cuit, fallback=""):
    return SUPPLIERS.get(cuit, (fallback or cuit or "Sin identificar", "Sin clasificar"))
