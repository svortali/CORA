# CORA: costos de Cora (café) a partir de las facturas de proveedores

Este archivo lo lee Claude Code al abrir la carpeta. Está pensado para retomar el proyecto sin el historial de chat anterior.
Hablar en español rioplatense (voseo). El repo es **público**.

## Qué es
Se leen las facturas de compra de 2026 (PDF y fotos de WhatsApp) y se arma un tablero de costos: gasto por mes, rubro y proveedor, y precio por kilo/litro/unidad de cada insumo. El tablero es un artifact de claude.ai de tipo Dashboard llamado **Costos Cora 2026**.

## Regla de oro: este repo es público
**Nunca commitear** facturas, CSV, `data/`, `cache/`, `reports/`, análisis con montos, ni el CUIT o los costos de la empresa. Todo eso está en `.gitignore`. Antes de cada `git add`, mirar `git status`.
En el repo solo van: `pipeline/`, `site/`, `research_notes/`, este archivo y el README.

## Qué hay en el repo y qué NO
| Carpeta | Contenido | ¿En git? |
|---|---|---|
| `pipeline/` | Scripts Python del flujo | Sí |
| `site/` | Página del tablero (`index.html`) y su especificación (`tablero_spec.json`) | Sí |
| `research_notes/` | Evaluación de Bistrosoft y competidores | Sí |
| `INPUT/2026/` | Facturas: `<N. Mes>/<Proveedor - tipo>/*.pdf` o `.jpeg` | No |
| `INPUT/2026/Costos/CostoDeIngredientes_actualizado.xlsx` | Excel de costos de ingredientes | No |
| `data/` | Salidas y archivos manuales (ver abajo) | No |
| `cache/txt/` | Texto extraído de cada PDF | No |

Las facturas las tiene Mauri (carpeta de OneDrive). Hay que copiarlas a `INPUT/2026/` con esa misma estructura.
Dos archivos de `data/` son trabajo manual que **no se regenera solo** y hay que pasar aparte, por un canal privado:
- `data/fotos_manual.csv`: transcripción a mano de las 20 fotos JPEG (no se pueden leer con `pdftotext`).
- `data/mapeo_ingredientes.csv`: a qué insumo corresponde cada descripción de proveedor. Las filas con `revisado=si` no se pisan.
Si no están, `build_data.py` y `propose_mapping.py` los rearman, pero se pierde la revisión hecha y las fotos quedan fuera.

## Requisitos
- Python 3, `pdftotext` (`brew install poppler`) y `openpyxl` (`pip3 install openpyxl`).
- Ojo: sin `openpyxl` el script **no falla**, simplemente no lee el Excel y sigue con la lista vacía.

## Flujo (correr desde la raíz del repo)
```bash
python3 pipeline/build_data.py            # lee INPUT/2026, extrae texto de los PDF, arma data/dashboard.json y CSV
python3 pipeline/propose_mapping.py       # propone data/mapeo_ingredientes.csv (insumo, unidad base, factor)
python3 pipeline/build_data.py            # vuelve a armar usando el mapeo
python3 pipeline/export_dashboard.py      # escribe data/tablero/{facturas,renglones,costos_excel,calidad}.csv
```
Los cuatro CSV de `data/tablero/` son lo único que consume el tablero.

## Dónde se edita cada cosa
- `pipeline/suppliers.py`: CUIT del proveedor → nombre corto y rubro. Para reclasificar un proveedor o sumar uno nuevo.
- `pipeline/propose_mapping.py`: reglas (regex) que proponen el insumo de cada renglón.
- `data/mapeo_ingredientes.csv`: correcciones a mano; marcar `revisado=si` para que no se pisen.
- `pipeline/parse_invoices.py` y `parse_items.py`: lectura de cabecera y renglones. No hay un parser por proveedor: los renglones se detectan por consistencia aritmética (cantidad × precio = importe).
- `pipeline/common.py`: rutas, formatos de importe argentino y estadounidense.

## El tablero (artifact)
- La página está en `site/index.html` y sus datos salen de los cuatro CSV. Detalle de títulos y descripciones en `site/tablero_spec.json`.
- Es un artifact de tipo **Dashboard**: la página y los datos viven en el almacén del propio artifact, no en un archivo publicado. Se carga con la herramienta `ArtifactData`.
- Para crearlo en una cuenta nueva: hacer `Artifact quickstart` con intent `other`, crear desde el tipo Dashboard, subir los cuatro CSV como datasets de tipo archivo (ids `facturas`, `renglones`, `costos_excel`, `calidad`), escribir `files/index.html` con el contenido de `site/index.html`, `dash/meta` con el título y `dash/params` con `params_iniciales` del spec.
- La página abre con `<meta name="dash-one-writer">`: antes de tocarla, leer `artifact-type/reference/one-writer.md` del artifact.
- Para actualizar datos: volver a correr el flujo y subir cada CSV nuevo como versión del dataset, sin tocar la página.
- Si cambia la página en el artifact, copiar el cambio a `site/index.html` y commitear.

## Pendientes conocidos
- OneDrive no bajó tres carpetas: `2. Febrero/La Meson - A`, `4. Abril/Contador - A`, `6. Junio/El Abascay - A`. Faltan sus facturas, y abril y junio no tienen alquiler.
- El detalle de problemas del archivo (duplicados, fotos, facturas en otro mes, filas del Excel sin costo) sale en `data/tablero/calidad.csv`.
- Noviembre 2026 recién empieza: hay que sumar facturas a medida que lleguen.
