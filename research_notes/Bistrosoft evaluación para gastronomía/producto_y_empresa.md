# Bistrosoft: producto (módulos, integraciones, arquitectura) y empresa (PDS S.A.)

Notas de investigación. Fecha de relevamiento: 2026-11-03. Convención: **[VENDOR]** = afirmación del propio Bistrosoft (sitio, prensa reproducida en su sitio, notas con citas de sus directivos); **[3RO]** = fuente independiente (registro fiscal, prensa con firma propia, directorios, agregadores); **[CONTRADICCIÓN]** = fuentes que no coinciden. Todas las URLs de bistrosoft.com fueron descargadas y leídas el 2026-11-03 (sitio WordPress; la mayoría de los textos están en páginas con footer "© 2026 Bistrosoft").

---

## 1. ¿Qué módulos existen y qué hace cada uno?

### Takeaway
Bistrosoft es un POS gastronómico de origen Android (terminal táctil "BPOS" simple o doble pantalla, o tablet) con back office web ("Bistro Web", webaccess.bistrosoft.com) y módulos adicionales licenciados por dispositivo: Bistro Móvil (comandera en celular / Point de Mercado Pago), Bistro Salón (tablet fija para mozos), Bistro Cocina (KDS en tablet), Bistro Facturación (comprobantes electrónicos ARCA), Tienda Online, Autoservicio (kiosco) y gestión multilocal / centro de producción en el plan Premium. No existe un módulo de **reservas** ni de **compras a proveedores con órdenes de compra** documentado en el sitio: sólo un ABM de "Proveedores" dentro de Bistro Web y un módulo de costos/recetas con mermas.

### Cited Findings

**Estructura comercial de módulos (planes AR, página de precios, leída 2026-11-03)** [VENDOR]
- Tres planes para Argentina: "Licencia Web" ($21.600 + IVA/mes; anual $18.360/mes; pago único $216.240), "Avanzado" ($70.200 + IVA/mes; anual $59.670; pago único $703.800) y "Premium" ($101.800 + IVA/mes; anual $86.530; pago único $1.020.000). "Sin plazo mínimo de permanencia." Pago anual = 15 % de ahorro. — [Precios AR](https://bistrosoft.com/ar/precios/)
- **Licencia Web** incluye: comandas, facturación, gestión de stock, carta QR, 1 usuario, hasta 20 mesas, 1 comandera/impresora, 1 carta, reportes básicos, hasta 500 facturas/mes, atención por WhatsApp; "Acceso con cualquier computadora Windows". — [Precios AR](https://bistrosoft.com/ar/precios/)
- **Avanzado** (plan "recomendado") agrega: usuarios y mesas ilimitadas, tienda online propia (hasta 50 pedidos), múltiples impresoras, reportes avanzados, módulo de costos y recetas, Account Manager, "integración con PedidosYa, Rappi, Rappi Turbo y Mercado Pago", "integración con terminales de pago (Mercado Pago, Nave, Getnet y Kamipay)"; incluye Bistro Móvil, Bistro Salón y Bistro Cocina; "Comodato opcional para toda Argentina". — [Precios AR](https://bistrosoft.com/ar/precios/)
- **Premium** agrega: centro de producción, pedidos ilimitados en tienda online, múltiples cartas, gestión multilocal, gestor de pedidos delivery, facturación masiva vía web, acceso a API para integraciones. — [Precios AR](https://bistrosoft.com/ar/precios/)
- Extras con precio: "Facturación electrónica: $23.000/mes (hasta 500 facturas)"; Bistro Móvil, Bistro Salón y Bistro Cocina: $24.500/mes cada uno (incluidos en Avanzado y Premium). "Los módulos adicionales tienen un costo aparte." — [Precios AR](https://bistrosoft.com/ar/precios/)
- FAQ: "Las licencias de Bistrosoft incluyen las funciones básicas del sistema. Las licencias adicionales suman módulos como Tienda Online, Bistro Cocina, Autoservicio, Versión Móvil o Salón". Modelo: "suscripción mensual, lo cual incluye actualizaciones, mejoras de sistema y soporte técnico permanente. Solo necesitás tu propio equipamiento". — [Preguntas frecuentes](https://bistrosoft.com/ar/preguntas-frecuentes/)
- Menú de navegación del sitio (nov. 2026): Productos = Punto de Venta, Tienda Online, Comedores, "Bistro Kiosco – Muy pronto"; Soluciones = Gestión de Salón, Control de Negocio, Organiza tu Delivery, Análisis de Datos, Eventos; Integraciones = Pago, Delivery; Licencias adicionales = Bistro Móvil, Bistro Salón, Bistro Cocina, Bistro Facturación; Recursos = Academia, Blog, Preguntas frecuentes, Referidos; países: Argentina, México, España. — [Términos y condiciones (menú)](https://bistrosoft.com/ar/terminos-y-condiciones/)

**Punto de venta (POS) / gestión de salón** [VENDOR]
- "Software punto de venta para administrar tu salón. Gestioná mesas, cajas y comandas desde pantalla táctil o celular". Lista: "Control total de ventas, comandas, mesas y caja"; "Múltiples cartas, menú digital y tienda online"; "Comanderas móviles compatibles con Mercado Pago y celulares"; "Compatible con lector de códigos de barra y básculas"; "Facturación electrónica y conciliación automática"; "Stock, recetas e ingeniería de menú"; "Reportes y estadísticas de ventas en tiempo real"; "Gestión de clientes y programas de fidelización"; "Soporte y capacitaciones sin límite". — [Punto de Venta](https://bistrosoft.com/ar/bistrosoft/)
- Gestión de salón: "Menu QR", "Impresión de comandas en cocina y barras", "Ingreso de comandas en el salón", "Monitor de cocina", "Pedidos en la mesa", "Mercado Pago y Bistrosoft se unen para facilitar tu tarea". — [Gestión de salón](https://bistrosoft.com/ar/gestion-de-salon/)
- Caja: configuraciones de "caja ciega" (ocultar totales por medio de pago a vendedores, bloquear impresión de parciales, apertura/cierre por vendedores) — release notes sept. 2024; "Ticket promedio en cierre de caja" (sólo comandas de mesa) — sept. 2025; propinas declaradas en venta para Argentina — mayo 2025 ("ya existía en ESP y MEX"); "Cuenta Cliente" (cuentas corrientes) como medio de pago — nov. 2024; descuentos personalizados — sept. 2024 y abr. 2025. — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)

**Comandas / KDS (Bistro Cocina)** [VENDOR]
- "Recibí pedidos automáticamente, controlá tiempos de preparación y mejorá la comunicación con el salón". "El chef recibe, prepara y despacha tus pedidos en tiempo real"; "Impresión de platos despachados". Dispositivo: "Tablet. Pantalla táctil de 10,3″". — [Bistro Cocina](https://bistrosoft.com/ar/bistro-cocina/)
- Julio 2025: "En Bistro Cocina ahora se visualizan todas las órdenes (mesas o comandas) que contengan productos pertenecientes a una categoría marcada para imprimirse en cocina. Las comandas cobradas se mantienen visibles durante 1 hora… (Antes solo se mostraban las órdenes de mesa)". — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)
- Mayo 2025: "Buscador de Comanderas en Red: ahora se puede escanear la red local para identificar automáticamente las comanderas". — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)

**Mozos / app de mesas (Bistro Móvil y Bistro Salón)** [VENDOR]
- Bistro Móvil: "Tomá pedidos desde la mesa… Descargá la app directo desde Play Store en tu dispositivo Android y empezá a operar." Funciones: "Tomá pedidos en las mesas", "Cierre de las mesas desde el dispositivo", "Cobranza en la mesa con tarjetas y QR". Dispositivos: "Celular. Consultá la compatibilidad de los diferentes modelos" y "Mercado Pago Point. Ahora podés tomar pedidos y cobrar desde tu terminal de Mercado Pago". — [Bistro Móvil](https://bistrosoft.com/ar/bistro-movil/)
- Nota de prensa (Circuito Gastronómico, 4-dic-2025, reproducida en el sitio): terminal portátil con impresora o sin impresora, "pantalla de 5 pulgadas y batería de más de 12 horas"; el cobro directo desde Bistro Móvil figura como "próximo". — [Circuito Bistro Móvil](https://bistrosoft.com/prensa/circuito-bistro-movil/)
- Bistro Salón: "Estación fija para mozos… Tablet de 10.1″"; "Cobrá en la mesa con tarjetas y QR — Muy pronto". — [Bistro Salón](https://bistrosoft.com/ar/bistro-salon/)
- Nov. 2024: solapas por origen (Salón, Vereda, Terraza) en Móvil y Salón; abr. 2025: productos pesables en Móvil y Salón; oct. 2024: selección de mozo al abrir mesa desde Bistro Salón. — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)
- [VENDOR, sitio MX] "Bistro Móvil es un módulo de toma de pedidos que debe conectarse a tu punto de venta principal Bistrosoft para sincronizar mapa de mesas, menú, precios y facturación… necesita conexión a internet"; "cada dispositivo necesita una licencia extra". — [Bistro Móvil MX](https://bistrosoft.com/mx/bistro-movil/) (citado vía resultado de búsqueda; no leído completo)

**Stock, insumos, recetas, costos** [VENDOR]
- Avanzado incluye "módulo de costos y recetas"; Web incluye "gestión de stock". — [Precios AR](https://bistrosoft.com/ar/precios/)
- Oct. 2024: "Alerta de Stock Mínimo"; "Merma de ingredientes: desde Productos > Costos de mercaderías puedes editar los costos de los ingredientes y definir un porcentaje de merma". Mayo 2024: "Costo de producción: receta de producción que descuenta stock de los ingredientes al hacer ingreso de stock". Nov. 2025: "gestión de stock por producto" en Licencia Web. — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)
- Bistro Web lista "Proveedores" y "Stock" y "Precios" entre sus secciones. — [Punto de Venta](https://bistrosoft.com/ar/bistrosoft/)
- Premium: "centro de producción" ("Centro de producción para controlar entrega de stock" a sucursales). — [Cadenas y franquicias](https://bistrosoft.com/ar/software-para-cadenas-franquicias/)

**Delivery propio y take-away / Tienda Online** [VENDOR]
- Tienda Online (lanzada jun. 2024): "Publicá productos, gestioná pedidos y vendé sin comisiones"; acceso por URL o QR; "Todos los pedidos se integrarán… en tu punto de venta Bistrosoft"; pagos online "a través de Mercado Pago"; mail de confirmación y cambios de estado; formas de entrega "Retiro en el local" y "Delivery" con zonas y costo de envío. Marzo 2025: pago en efectivo en el local. — [Tienda Online](https://bistrosoft.com/ar/tienda-online/); [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)
- "Organiza tu delivery": "Administrá tu delivery propio y las principales apps desde un solo sistema"; "Administrá tu base de clientes"; "Panel de integraciones para apps de delivery". — [Organiza tu delivery](https://bistrosoft.com/ar/organiza-tu-delivery/)
- Premium incluye "gestor de pedidos delivery". — [Precios AR](https://bistrosoft.com/ar/precios/)

**Autoservicio / kiosco** [VENDOR]
- "Autoservicio": el cliente elige productos, personaliza, carga nombre, paga ("Pago online: Mercado Pago. Pago presencial: En caja con tarjeta o efectivo"; "Acepta Mercado Pago, Modo o pagos en caja"); el cajero acepta y la orden pasa a cocina. — [Autoservicio](https://bistrosoft.com/ar/autoservicio/)
- "Bistro Kiosco – Muy pronto" en el menú (nov. 2026). — [menú del sitio](https://bistrosoft.com/ar/terminos-y-condiciones/)

**Menú QR** [VENDOR]
- "Carta QR" incluida desde Licencia Web; "Menu QR" en gestión de salón; Tienda Online accesible por QR. — [Precios AR](https://bistrosoft.com/ar/precios/); [Gestión de salón](https://bistrosoft.com/ar/gestion-de-salon/)

**Reportes / Bistro Web (back office)** [VENDOR]
- "Más de 20 reportes predeterminados", "Tablero de control en tiempo real", "Control total de los movimientos desde tu celular". — [Control de negocio](https://bistrosoft.com/ar/control-de-negocio/)
- Bistro Web: "Productos, combos y adicionales; Múltiples cartas; Stock; Precios; Reportes en tiempo real; Control horario de personal; Ranking de ventas; Cierre de caja; Proveedores"; "Celular, PC o tablet". — [Punto de Venta](https://bistrosoft.com/ar/bistrosoft/)
- Control horario de empleados (entrada/salida, turnos, horas) — oct. 2024. — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)

**Multi-sucursal / cadenas y franquicias** [VENDOR]
- "Funcionalidad multilocal para el control de todas las sucursales", "Dashboard de resultados unificado", "Gestión centralizada de productos, recetas y precios", "configuraciones globales o por sucursal". — [Cadenas y franquicias](https://bistrosoft.com/ar/software-para-cadenas-franquicias/)
- Oct. 2024: "Local Principal… los Locales Hijos no editen nada, excepto el stock"; nov. 2025: "Opciones Multilocal… unificar los productos y el stock para todas las sucursales". — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)
- FAQ: "podés gestionar varios locales desde una sola cuenta, ver ventas por sucursal y asignar permisos a cada equipo". — [Preguntas frecuentes](https://bistrosoft.com/ar/preguntas-frecuentes/)
- Alianza con la consultora "Franquicias que Crecen" (ExpoFranquicias 2026, sept. 2026); "desde hace un año" también atienden panaderías, pastelerías y carnicerías. — [ExpoFranquicias 2026](https://bistrosoft.com/prensa/expofranquicias-2026/)

**Facturación electrónica (Bistro Facturación)** [VENDOR]
- Título de página: "Bistro Facturación cubre tus requerimientos frente a la AFIP"; cuerpo: "Tu facturación, siempre al día con ARCA. Emití comprobantes y facturas desde un solo sistema, reducí costos con QR digital"; "Impresión de comprobantes fiscales"; "2 en 1 comanda e imprime la factura de tu cliente desde la misma impresora"; "QR digital para ahorrar papel". — [Bistro Facturación](https://bistrosoft.com/ar/bistro-facturacion/)
- FAQ: "Bistrosoft emite comprobantes electrónicos conforme a la normativa vigente; la facturación está incluida en la licencia o disponible como módulo adicional". — [Preguntas frecuentes](https://bistrosoft.com/ar/preguntas-frecuentes/)
- Precio: "Facturación electrónica: $23.000/mes (hasta 500 facturas)"; Premium: "facturación masiva vía web". — [Precios AR](https://bistrosoft.com/ar/precios/)
- Cronista 2018: el sistema "se integra con impresoras fiscales". — [El Cronista, 26-sep-2018](https://www.cronista.com/infotechnology/entreprenerds/Foodtech-los-argentinos-que-ganan-miles-de-pesos-automatizando-restaurantes-20180926-0005.html) [3RO]

**Eventos y comedores** [VENDOR]
- Páginas "Bistro Eventos" y "Comedores corporativos" existen en el menú (no leídas en detalle). Córdoba: operaron "tres ediciones de MotoGP, dos ediciones de En Taza, Casa FOA y el Mundial en el Hipódromo de Córdoba". — [Circuito Gastronómico Córdoba, 25-sep-2026](https://bistrosoft.com/prensa/circuito-gastronomico-cordoba/)

### Inferences
- Los planes empaquetan por capacidad (mesas, usuarios, impresoras, facturas/mes) y por módulos; el "Avanzado" es el primer plan donde el producto es realmente un sistema de salón con comanderas, KDS e integraciones; el "Licencia Web" es un POS Windows liviano.
- El límite de "hasta 500 facturas/mes" tanto en Licencia Web como en el extra de facturación sugiere que el costo de facturación electrónica se escala por volumen de comprobantes (no confirmado para tramos superiores).
- "Ingeniería de menú" y "programas de fidelización" aparecen sólo como frases de marketing en la página de POS, sin página de detalle ni release note que los describa: probablemente son reportes de ranking y la "Cuenta Cliente", no módulos completos.

### Gaps
- **Reservas**: ninguna página del sitio, FAQ ni release note 2024-2025 menciona un módulo de reservas de mesas. Tracxn menciona "reservation… management" en su descripción genérica, pero no está respaldado por el sitio.
- **Compras / órdenes de compra a proveedores**: sólo se ve "Proveedores" como sección de Bistro Web; no hay documentación de órdenes de compra, recepción de mercadería ni cuentas a pagar.
- **Facturación: tipos de comprobante** (Factura A/B/C, consumidor final, nota de crédito), **controlador fiscal homologado vs. web services ARCA (WSFE)**, y qué pasa por encima de 500 facturas/mes: no documentado públicamente. El texto habla de "impresión de comprobantes fiscales" e "impresoras fiscales" (2018) y a la vez de "QR digital" y facturación "vía web", lo que sugiere soporte de ambas vías, pero no está confirmado.
- Páginas /ar/bistro-eventos/, /comedores-corporativos/, /ar/blog/ y /academia/ no fueron leídas en profundidad.

---

## 2. ¿Qué integraciones son reales y documentadas? ¿Nativas o por conector? ¿Costo extra?

### Takeaway
Documentadas por el propio vendor en 2024-2026: delivery nativo con PedidosYa y Rappi (Rappi Turbo en precios; Uber Eats y DiDi aparecen sólo en menciones sueltas); pagos con Mercado Pago (Point, QR, pagos online en Tienda Online), MODO/Nave (QR, mayo 2024), Getnet (jun. 2026, confirmado por prensa de terceros), kamiPay/Pix (ago.-nov. 2024) y SimpleFi (cripto, ago. 2024). **Contabilium** sólo figura en un listado de directorio (ComparaSoftware) que reproduce texto antiguo del vendor; no aparece en el sitio actual. No hay evidencia de Clover, Mobbex, Payway ni WhatsApp (salvo como canal de soporte). El sitio dice que las integraciones no tienen cargo extra pero exigen plan Avanzado o Premium (fuentes internas contradictorias sobre cuál).

### Cited Findings

**Delivery**
- [VENDOR] FAQ oficial: "Actualmente, nuestro sistema cuenta con integración nativa con PedidosYa y Rappi. Si usás una plataforma distinta… nuestro equipo técnico evaluará tu caso". Flujo: el pedido "aparece directamente en tu pantalla de Bistrosoft. Desde allí podés aceptarlo o rechazarlo. Al aceptar, el pedido se envía automáticamente a la impresora de cocina". Listas de precios diferenciadas para delivery; pausar productos sin stock desde Bistrosoft hacia la carta online; "la integración es tecnológica… los repartidores siguen siendo gestionados por cada plataforma". Tablero: "Apertura y cierre de tiendas desde un solo panel", "Resumen de pedidos aceptados, cancelados y errores de integración", "Gráfico de pedidos por plataforma en las últimas 24 horas". — [Integraciones Delivery](https://bistrosoft.com/ar/integraciones-delivery/)
- [VENDOR] **Costo**: "La funcionalidad de integración no tiene un costo adicional, pero requiere contar con nuestra Licencia Premium." — [Integraciones Delivery](https://bistrosoft.com/ar/integraciones-delivery/) **[CONTRADICCIÓN]** con la página de precios: "Desde Avanzado conectás PedidosYa, Rappi, Mercado Pago y terminales de pago" y Avanzado lista "integración con PedidosYa, Rappi, Rappi Turbo y Mercado Pago". — [Precios AR](https://bistrosoft.com/ar/precios/)
- [VENDOR] Página POS: "Apps de delivery: PedidosYa, Rappi y Uber Eats". — [Punto de Venta](https://bistrosoft.com/ar/bistrosoft/). Nota Córdoba (sept. 2026) también lista "PedidosYa, Rappi, UberEats". — [Circuito Córdoba](https://bistrosoft.com/prensa/circuito-gastronomico-cordoba/). Uber Eats no figura en la FAQ de "integración nativa".
- [VENDOR] Jun. 2024 (release notes): "MX Integración con DIDI, servicio de Delivery" (sólo México). — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)
- [3RO, histórico] En 2018 PedidosYa fue "socio" de Bistrosoft para terminales de pedidos (no cliente). — [El Cronista 2018](https://www.cronista.com/infotechnology/entreprenerds/Foodtech-los-argentinos-que-ganan-miles-de-pesos-automatizando-restaurantes-20180926-0005.html). Nota Córdoba 2026: los fundadores "primero construyeron tecnología para PedidosYa". — [Circuito Córdoba](https://bistrosoft.com/prensa/circuito-gastronomico-cordoba/)
- No se encontró a Bistrosoft en directorios públicos de partners de PedidosYa ni Rappi (búsqueda 2026-11-03 devolvió sólo Deliverect, Ordatic, Restroworks). [GAP]

**Pagos / terminales**
- [VENDOR] FAQ oficial de pagos: "¿Qué terminales de pago son compatibles con Bistrosoft? Actualmente… Mercado Pago, Modo y Nave". Mecánica: "al momento de seleccionar 'Pago con Tarjeta' en tu software, el importe se transfiere automáticamente a la terminal". Costo: "¡No, ninguno! La vinculación de tu terminal de pago con Bistrosoft es totalmente gratuita". Requisito: contratar la terminal con el proveedor primero; luego Atención al Cliente activa la conexión. — [Integraciones Pago](https://bistrosoft.com/ar/integraciones-pago/). La misma página muestra logos de Getnet (archivo subido nov. 2025), SimpleFi (feb. 2026) y otro logo de feb. 2026 — es decir, la FAQ está desactualizada respecto de los logos.
- [VENDOR] Página de precios (Avanzado): "integración con terminales de pago (Mercado Pago, Nave, Getnet y Kamipay)". — [Precios AR](https://bistrosoft.com/ar/precios/)
- [VENDOR] Página POS: "Pagos con Mercado Pago, Modo, Nave, Kamipay y Simplefi". — [Punto de Venta](https://bistrosoft.com/ar/bistrosoft/)
- [VENDOR] Mercado Pago: Bistro Móvil corre "desde tu terminal de Mercado Pago" (Point); Tienda Online y Autoservicio cobran online "a través de Mercado Pago"; "Mercado Pago y Bistrosoft se unen". — [Bistro Móvil](https://bistrosoft.com/ar/bistro-movil/); [Tienda Online](https://bistrosoft.com/ar/tienda-online/); [Gestión de salón](https://bistrosoft.com/ar/gestion-de-salon/)
- [VENDOR] MODO/Nave: mayo 2024 "Integración con MODO QR (NAVE – Procesador de Pago)… Cobra con código QR: te pagan con cualquier app". — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)
- [VENDOR] SimpleFi y kamiPay: ago. 2024 "Integración con SimpleFi y KamiPay… cobrá con crypto (Bitcoin, USDT, UXD y DOC)… kamiPay te permite cobrar a tu cliente de Brasil con PIX… recibe dólares digitales en el acto y 0% de comisión". España: integración con datáfono Dojo (ago. 2024). — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)
- [VENDOR/3RO] kamiPay: nota eBizLatam 22-nov-2024 cita a Gastón Ponteville (co-founder Bistrosoft) y Matías Gorganchian (co-founder kamiPay); caso Punto Panorámico, Bariloche. — [eBizLatam vía bistrosoft.com](https://bistrosoft.com/prensa/ebizlatam-kamipay-pix/)
- [3RO] **Getnet** (Santander): Revista Mercado, 23-jun-2026: "Getnet integra sus terminales de pago con el software gastronómico Bistrosoft"; "los pedidos creados en la plataforma de Bistrosoft se envían directamente a las terminales… el importe se transfiere automáticamente"; citas de Ezequiel Valentín (Head of Partnerships, Getnet Argentina) y Gastón Ponteville (Co-Founder, Bistrosoft). — [Revista Mercado](https://mercado.com.ar/ruta-digital/getnet-integra-sus-terminales-de-pago-con-el-software-gastronomico-bistrosoft). Somos Pymes, 24-jun-2026: "disponible para clientes del rubro que cumplan las condiciones comerciales de ambas plataformas". — [Somos Pymes](https://www.somospymes.com.ar/financiamiento-y-mercados/getnet-y-bistrosoft-se-integran-transformar-los-cobros-el-sector-gastronomico-n5403431)
- [VENDOR] Jul. 2024: "Nueva sección de integraciones… gestionar las integraciones con terceros desde configuraciones en BistroWeb"; oct. 2024: "Marketplace de integraciones… integraciones específicas para cada país, algunas automáticas y otras que nosotros configuramos para ti". — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)

**Contabilidad / Contabilium y otros**
- [3RO reproduciendo VENDOR] ComparaSoftware (ficha sin fecha; única reseña del 31-03-2024): "Nuestro partners son: Pedidos Ya, Mercado Pago, Rappi y Contabilium. 100% integrados al software"; "Somos la primer solución Android de Software gastronómico para Argentina"; incluye "Bistro Advance (doble pantalla touch), sistema android, mesa de ayuda 24hrs y Bistro Web". — [ComparaSoftware](https://www.comparasoftware.com/bistrosoft)
- Contabilium **no aparece** en ninguna página actual de bistrosoft.com leída (precios, integraciones pago/delivery, POS, release notes 2024-2025). No se encontró documentación de Contabilium sobre Bistrosoft. [GAP]
- Premium incluye "acceso a API para integraciones" — sin documentación pública de la API encontrada (hay un path /api/ en el sitio, no inspeccionado). — [Precios AR](https://bistrosoft.com/ar/precios/)
- WhatsApp: aparece sólo como canal de soporte/ventas (números +54 11 2739-8527, 2739-8593, 2734-4172, 3775-7552) y para compartir el link de Tienda Online; no hay integración de pedidos por WhatsApp documentada. — [Home AR](https://bistrosoft.com/ar/); [Tienda Online](https://bistrosoft.com/ar/tienda-online/)
- Clover, Mobbex, Payway, Google (reservas/pedidos): ninguna mención en el sitio ni en prensa relevada. [GAP]
- [3RO, 2018] "Se integra con herramientas de terceros como Spotify"; nube en Amazon. — [El Cronista 2018](https://www.cronista.com/infotechnology/entreprenerds/Foodtech-los-argentinos-que-ganan-miles-de-pesos-automatizando-restaurantes-20180926-0005.html)

### Inferences
- Las integraciones de delivery son nativas (API directa, con tablero de estado propio) y no vía Deliverect/Ordatic: el vendor habla de "integración nativa" y de "errores de integración" propios; además pide que el local esté dado de alta en la app y "nosotros nos encargamos de hacer la conexión".
- La integración con terminales es del tipo "POS envía importe a la terminal" (semi-integrada), con confirmación de pago de vuelta no explicitada.
- El catálogo de pagos crece por acuerdos comerciales (Nave 2024, kamiPay/SimpleFi 2024, Getnet 2026); la FAQ queda atrasada respecto de precios/logos, por lo que conviene pedir al vendor la lista vigente por escrito.
- La mención a Contabilium parece heredada de un período anterior (ficha de ComparaSoftware); hay que tratarla como no vigente hasta confirmación.

### Gaps
- Confirmación en los directorios de partners de PedidosYa, Rappi, Mercado Pago y Contabilium: no localizada.
- Si Uber Eats y Rappi Turbo están realmente activos en Argentina (aparecen en marketing pero no en la FAQ de "nativas").
- Si la integración Getnet requiere plan Avanzado o Premium: no aclarado.
- Documentación técnica de la API (Premium) y de la exportación contable: no pública.

---

## 3. Arquitectura técnica: web vs. desktop vs. Android/iOS; offline; tiendas de apps; hardware

### Takeaway
Arquitectura híbrida: terminal POS Android (hardware propio "BPOS" simple/doble pantalla o tablet Android) que opera offline y sincroniza a la nube (AWS según 2018) al menos una vez por día; back office "Bistro Web" en navegador (webaccess.bistrosoft.com); una "Licencia Web" que corre "con cualquier computadora Windows"; apps adicionales Android (Bistro Móvil en Play Store, Bistro Salón y Bistro Cocina en tablets). No hay app iOS: el único resultado en App Store ("Bistroft") es de otra empresa mexicana. No pude localizar el listado de Google Play ni su fecha de última actualización.

### Cited Findings
- [VENDOR] FAQ: "Bistrosoft funciona en tablets Android, notebooks y PCs"; "es necesario estar conectado a Wi-Fi para que la información se sincronice en tiempo real"; servidores seguros, backups automáticos, accesos personalizados. — [Preguntas frecuentes](https://bistrosoft.com/ar/preguntas-frecuentes/)
- [VENDOR, contractual] T&C: "El BPOS/TABLET podrá operar en forma off-line aunque es condición que el cliente tenga habilitado un servicio de internet vía wifi… para permitir que el dispositivo sincronice al menos una vez al día con el servidor en la nube y de esa manera que el cliente pueda acceder a la información vía la página https://webaccess.bistrosoft.com/login. Los datos del cliente serán almacenados por un plazo de 12 meses." — [Términos y condiciones](https://bistrosoft.com/ar/terminos-y-condiciones/)
- [VENDOR] Licencia Web: "Acceso con cualquier computadora Windows". — [Precios AR](https://bistrosoft.com/ar/precios/). Sitio MX: "Licencia Básica Web… Desde cualquier computadora". — [Academia Licencia México](https://bistrosoft.com/academia/licencia-mexico/)
- [VENDOR] Hardware vendido por Bistrosoft: "Nuevo Doble pantalla Pro: pantalla táctil de 15,6″ para el cajero y una segunda pantalla de 10″ para que tu cliente vea su pedido y el total; 4 conexiones: wifi, bluetooth, USB y ethernet"; "Doble pantalla"; "Simple pantalla 15″"; "Simple pantalla 10″". Accesorios: "Comandera: impresora térmica de 80 mm. Bluetooth, USB y ethernet"; "Cajón de dinero de acero… apertura automática desde Bistrosoft"; "Lector de código de barras"; "Balanza digital". — [Punto de Venta](https://bistrosoft.com/ar/bistrosoft/)
- [VENDOR] Academia / Instalación: "Equipo Principal: Pantalla doble o simple + Tablet"; "Periféricos: Comandera/Cajón/pistola"; kit de tablet incluye "Router TP-Link", impresora LAN y tablet; usuario ADMIN con clave por defecto 1234; configuración en "Configuración Técnica > Periféricos" con botón "Test"; "Es imprescindible contar con una red WiFi estable". — [Academia Instalación](https://bistrosoft.com/academia/instalacion/)
- [VENDOR] FAQ: recomienda dos impresoras, "una para las comandas de cocina y otra para el mostrador, que imprime pedidos y tickets fiscales"; "los dispositivos dependen de tu licencia y un asesor verifica la compatibilidad si usás tu propio equipo". — [Preguntas frecuentes](https://bistrosoft.com/ar/preguntas-frecuentes/)
- [VENDOR] Comodato: "En las licencias Bistrosoft Todo en Uno se incluye un dispositivo hardware denominado BPOS, entregado en comodato… plazo mínimo de permanencia de seis (6) meses"; reposición por pérdida/robo "USD 1.000 más IVA"; prohibido instalar apps o pendrives; compra de equipo con garantía de 12 meses en taller. — [Términos y condiciones](https://bistrosoft.com/ar/terminos-y-condiciones/)
- [VENDOR] Bistro Móvil: "Descargá la app directo desde Play Store en tu dispositivo Android"; corre también en Mercado Pago Point. — [Bistro Móvil](https://bistrosoft.com/ar/bistro-movil/)
- [VENDOR] Julio 2025: "MX Modo Retail: aplicación específica para locales de venta minorista"; junio 2025: "integración con básculas RHINO" (México). — [Mejoras y lanzamientos](https://bistrosoft.com/mejoras-y-lanzamientos/)
- [3RO, 2018] "Sistema de punto de venta que corre en tablets con un kernel Android personalizado"; "tablet de una pantalla… y tablet de doble pantalla que muestra al cliente su pedido"; "app para el dueño… almacena datos offline y sincroniza cuando vuelve la conexión"; "almacenamiento en la nube en Amazon". — [El Cronista 2018](https://www.cronista.com/infotechnology/entreprenerds/Foodtech-los-argentinos-que-ganan-miles-de-pesos-automatizando-restaurantes-20180926-0005.html)
- [3RO] ComparaSoftware clasifica despliegue "Nube, SaaS, Web" y reproduce "primer solución Android de Software gastronómico para Argentina". — [ComparaSoftware](https://www.comparasoftware.com/bistrosoft)
- [3RO] Capterra (ficha 1109312): "cloud-based restaurant management and POS software… supports payment integrations such as Mercado Pago, delivery apps, and electronic invoicing for Latin American markets… strong focus on Argentina and Mexico" (de snippets de búsqueda; las páginas de Capterra devolvieron HTTP 403). — [Capterra](https://www.capterra.in/software/1109312/Bistrosoft)
- **App Store**: la búsqueda "Bistrosoft" devuelve la app "Bistroft" (id1643937104), del vendedor "Adsum Soluciones Tecnologicas SA de CV" (México), para iPad, última versión 1.0.26 — **no es Bistrosoft**. — [App Store id1643937104](https://apps.apple.com/us/app/id1643937104). No se encontró ninguna app de PDS S.A./Bistrosoft en App Store.
- Portales de login por país: Argentina webaccess.bistrosoft.com; México mx.bistrosoft.com; España es.bistrosoft.com. — [Academia Licencia México](https://bistrosoft.com/academia/licencia-mexico/)

### Inferences
- El POS principal no es una web app: es software Android instalado en hardware controlado por el vendor (T&C prohíben modificar el software del BPOS). El modo offline está garantizado contractualmente sólo para el BPOS/tablet; Bistro Móvil requiere conexión al POS principal.
- "Licencia Web" es un producto distinto (cliente Windows/browser sin hardware Android), apuntado a locales chicos; nov. 2025 le agregaron mesas y stock.
- La retención de datos de 12 meses en nube es un punto relevante para auditoría contable y debería negociarse.

### Gaps
- **Listado de Google Play**: no localizado por búsqueda (nombre de desarrollador, package, fecha de última actualización e instalaciones desconocidos). Verificar manualmente en Play Store buscando "Bistro Móvil"/"Bistrosoft".
- Requisitos mínimos de Android/Windows, versiones soportadas y modelos de celular compatibles: el sitio remite a "consultá la compatibilidad".
- Si Bistro Cocina/Bistro Salón son apps instalables en tablets propias o sólo en tablets provistas.

---

## 4. La empresa: razón social, CUIT, fundadores, sede, año, equipo, financiación, clientes, prensa, ferias

### Takeaway
Bistrosoft es marca registrada de **PDS S.A., CUIT 33-70974610-9**, presidida por Renaud D. Darsonville, con domicilio en Av. Crámer 3226, piso 4, CABA. Fundada en 2017/2018 por Gastón Ponteville y Renaud Darsonville (ambos ex-industria de medios de pago), autofinanciada (USD 200.000 propios en 2018; "unfunded" según Tracxn), con 66 empleados en LinkedIn (sept. 2026) y oficinas declaradas en CABA, Ciudad de México y Barcelona. Las cifras de clientes son contradictorias dentro del propio sitio ("+4.000 usuarios, 3 países" en home vs. "más de 25.000 locales en más de 8 países" en Nosotros). Prensa: El Cronista (2018), Revista Mercado y Somos Pymes (jun. 2026, integración Getnet), Circuito Gastronómico (varias), eBizLatam/Ovrik (kamiPay 2024), Perfect Daily Grind (2022). Feria confirmada: ExpoFranquicias 2026. No se halló mención a Hotelga, Infobae, La Nación, Clarín, iProUP ni Ámbito.

### Cited Findings

**Identidad legal** [VENDOR, documento contractual]
- "PDS S.A., CUIT NRO 33-70974610-9 REPRESENTADA EN ESTE ACTO POR RENAUD D. DARSONVILLE, EN SU CARÁCTER DE PRESIDENTE Y CON DOMICILIO EN AV. CRAMER 3226, piso 4, Ciudad de Buenos Aires… es una empresa que diseña, instala, vende y comercializa un software de gestión especializado en la administración de gastronomía comercial. Entre estos productos Bistrosoft es un producto propio, original y registrado de PDS SA." — [Términos y condiciones](https://bistrosoft.com/ar/terminos-y-condiciones/)
- [3RO] CuitOnline: CUIT 33-70974610-9 corresponde a "Pds S.a.", persona jurídica, IVA Inscripto, empleador, Ganancias/Sicore (datos completos sólo para suscriptores; provincia y fecha de inscripción no visibles). — [CuitOnline](https://www.cuitonline.com/search.php?q=33-70974610-9)
- [VENDOR] Footer de todo el sitio: "Av. Crámer 3226, piso 4, CABA, Argentina"; redes: instagram.com/bistrosoft, facebook.com/bistrosoft, linkedin.com/company/bistrosoft, tiktok.com/@bistrosoft, youtube.com/@bistrosoftglobal. — [Nosotros](https://bistrosoft.com/ar/nosotros/)
- T&C: soporte por WhatsApp "+54 9 11 2739-8593" en horario "LU A LUN DE 8 A 1 AM" (sic); facturación mensual del 1 al 20 por "disponibilidad del servicio", débito automático, baja con un mes de anticipación mediante formulario, suspensión con mora > 2 días, intereses a tasa activa BNA; el cliente autoriza uso de datos anonimizados/agregados para estadística y mercado, con posibilidad de cesión. — [Términos y condiciones](https://bistrosoft.com/ar/terminos-y-condiciones/)

**Fundadores y origen**
- [3RO] El Cronista / Infotechnology, 26-sep-2018 (Juan Silvestrini): cofundadores **Gastón Ponteville** y **Renaud Darsonville**, ambos provenientes del mundo corporativo y de "soluciones de pago"; fundada en **2017**; inversión inicial US$ 200.000 de fondos propios; facturación estimada 2018: $450.000; abono de entonces $1.400-$1.800/mes con tablet en alquiler; "40 % de los clientes son food trucks"; cita: "Los puntos de venta gastronómicos estaban totalmente obsoletos" (Ponteville); "Buscamos llevarle al local gastronómico más pequeño una solución que antes era inaccesible" (Darsonville). (El artículo también escribe "Capdeville" en un pasaje, aparente errata.) — [El Cronista 2018](https://www.cronista.com/infotechnology/entreprenerds/Foodtech-los-argentinos-que-ganan-miles-de-pesos-automatizando-restaurantes-20180926-0005.html)
- [VENDOR] Circuito Gastronómico Córdoba (25-sep-2026): fundada "entre 2018 y 2019 por dos amigos de la industria de medios de pago", que "primero construyeron tecnología para PedidosYa". — [Circuito Córdoba](https://bistrosoft.com/prensa/circuito-gastronomico-cordoba/) **[CONTRADICCIÓN]** con 2017 (Cronista) y 2018 (LinkedIn/Tracxn).
- [VENDOR] Gastón Ponteville aparece como "Co-Founder" (2024, 2026) y como "CEO" (nota de jul. 2024, escrito "Pontevilles"). — [Prensa Bistrosoft](https://bistrosoft.com/prensa/); [eBizLatam](https://bistrosoft.com/prensa/ebizlatam-kamipay-pix/)
- [VENDOR] Francisco Arning, "Gerente comercial de Bistrosoft" (ExpoFranquicias 2026). — [ExpoFranquicias 2026](https://bistrosoft.com/prensa/expofranquicias-2026/)
- [3RO, agregadores] LinkedIn menciona a Hernán Zbucki como CTO; Datanyze lista a "Maria De Baere (Gerente General)" (no verificado en fuente primaria). — [búsqueda: LinkedIn](https://es.linkedin.com/company/bistrosoft); [Datanyze](https://www.datanyze.com/companies/bistrosoft/547018753)

**Sede, tamaño, financiación**
- [3RO] LinkedIn (leído 2026-11-03): sector "Desarrollo de software"; tamaño "51-200 empleados"; "66 empleados en LinkedIn"; sede CABA, "Crámer 3226"; otras ubicaciones: Ciudad de México y Barcelona; fundada 2018; 5.089 seguidores; especialidades "software, payments, foodtrucks, restaurant services, gastronómico, foodtech…". — [LinkedIn Bistrosoft](https://es.linkedin.com/company/bistrosoft)
- [3RO] Tracxn: Buenos Aires, fundada 2018, "Unfunded", 66 empleados (30-sep-2026), sin adquisiciones ni inversiones; ranking 691 entre 2.747 competidores (Toast, Olo, TouchBistro, etc.). — [Tracxn](https://tracxn.com/d/companies/bistrosoft/__aEmapNZQd4wnh18YaR2z4aAL2IekLcXYoVJ1A72OAWM)
- [3RO] Prospeo/Datanyze: Buenos Aires, fundada 2018. — [Prospeo](https://prospeo.io/c/bistrosoft)
- [VENDOR] "Estamos en México, Argentina, Uruguay y España"; sección "Trabajá con nosotros" / "Envía tu CV". — [Nosotros](https://bistrosoft.com/ar/nosotros/)

**Clientes y escala** **[CONTRADICCIÓN interna]**
- [VENDOR] Home AR: "+4.000 usuarios", "+10 M transacciones", "3 países". — [Home](https://bistrosoft.com/)
- [VENDOR] Nosotros: "En la última década, nosotros hemos entregado diversos servicios y soluciones a más de 25,000 locales gastronómicos en más de 8 países de Latinoamérica y Europa." — [Nosotros](https://bistrosoft.com/ar/nosotros/)
- [VENDOR] Integraciones: "Miles de clientes satisfechos en Mexico, Argentina, Uruguay y España". — [Integraciones Delivery](https://bistrosoft.com/ar/integraciones-delivery/)
- [VENDOR] Testimonios en video en home: "Matza, Chocolatta, Bagel, Martín Imán" (sin transcripción). — [Home](https://bistrosoft.com/)
- [VENDOR] Clientes nombrados en Córdoba: "Nostra, Burger Fan, Parque Pizzería, Brasería El Dorado"; eventos: MotoGP (3 ediciones), En Taza (2), Casa FOA, Mundial en el Hipódromo de Córdoba; asesora comercial en Córdoba: "Ruth". — [Circuito Córdoba](https://bistrosoft.com/prensa/circuito-gastronomico-cordoba/)
- [VENDOR] Caso kamiPay: "Punto Panorámico" (Bariloche). — [eBizLatam](https://bistrosoft.com/prensa/ebizlatam-kamipay-pix/)
- [VENDOR] Rubros del formulario de contacto: cafetería, bar-cervecería, pizzería-empanadas, restaurante, carnicería, food truck, fast food, confitería-panadería, franquicia, dietética, kiosko. — [Home](https://bistrosoft.com/)
- [3RO] ComparaSoftware: 1 reseña (31-03-2024, puntaje 2/5): "Atención al cliente, pesima". — [ComparaSoftware](https://www.comparasoftware.com/bistrosoft)

**Prensa y ferias**
- Índice de prensa del vendor (12 notas, 2022-2026): Circuito Gastronómico (25-sep-2026, 26-jun-2026, 4-dic-2025, 6-dic-2024, 20-nov-2024, 30-jul-2024), Noticias D / ExpoFranquicias 2026 (9-sep-2026), Somos Pymes (24-jun-2026), Revista Mercado (23-jun-2026), eBizLatam (22-nov-2024), Ovrik (8-nov-2024), Perfect Daily Grind (27-sep-2022). — [Prensa](https://bistrosoft.com/prensa/)
- [3RO] Originales verificados fuera del sitio: Revista Mercado (23-jun-2026) — [link](https://mercado.com.ar/ruta-digital/getnet-integra-sus-terminales-de-pago-con-el-software-gastronomico-bistrosoft); Somos Pymes (24-jun-2026) — [link](https://www.somospymes.com.ar/financiamiento-y-mercados/getnet-y-bistrosoft-se-integran-transformar-los-cobros-el-sector-gastronomico-n5403431); El Cronista (26-sep-2018) — [link](https://www.cronista.com/infotechnology/entreprenerds/Foodtech-los-argentinos-que-ganan-miles-de-pesos-automatizando-restaurantes-20180926-0005.html).
- Ferias: ExpoFranquicias 2026 (sept. 2026) confirmada por nota del vendor. — [ExpoFranquicias 2026](https://bistrosoft.com/prensa/expofranquicias-2026/). Hotelga: sin mención en ninguna fuente relevada.
- Programa de referidos y "Academia" (tutoriales de instalación) existen en el sitio. — [Academia Instalación](https://bistrosoft.com/academia/instalacion/)

**Rebranding, adquisiciones, relación con otras marcas POS**
- Tracxn: sin adquisiciones ni inversiones registradas. — [Tracxn](https://tracxn.com/d/companies/bistrosoft/__aEmapNZQd4wnh18YaR2z4aAL2IekLcXYoVJ1A72OAWM)
- El nombre "BistroSoft" ya se usaba en 2018 (Cronista); no se halló rebranding. El hardware se denomina "BPOS"/"Bistro Advance". Relación comercial histórica con PedidosYa (terminales, 2018). No se encontró vínculo con otras marcas de POS argentinas.

### Inferences
- La razón social PDS S.A. (CUIT 33-…, sociedad anónima) tiene prefijo "33" típico de personas jurídicas inscriptas antes de la era "30-7x"; la ficha de CuitOnline no muestra fecha de constitución, por lo que PDS S.A. podría preexistir a Bistrosoft (coherente con "en la última década" en Nosotros y con el pasado de los fundadores en medios de pago). Pendiente confirmar en IGJ/ARCA.
- La cifra "+25.000 locales / 8 países" probablemente acumula servicios previos de PDS S.A. (p. ej. terminales para PedidosYa), mientras que "+4.000 usuarios / 3 países" sería la base activa de Bistrosoft; ninguna de las dos está confirmada por terceros.
- Empresa autofinanciada, de tamaño mediano (50-70 personas), con expansión a México y España y presencia comercial en Córdoba; la crítica de soporte en ComparaSoftware es un dato aislado (n=1) pero el vendor insiste en "soporte humano", lo que sugiere que fue un punto de dolor.

### Gaps
- Fecha de inscripción, estado ante ARCA y actividad declarada de PDS S.A.: no visibles sin suscripción; verificar en constancia de inscripción ARCA / IGJ.
- Número verificado de clientes activos en Argentina: sólo cifras del vendor, contradictorias.
- Cadenas o franquicias clientes nombradas: ninguna en el sitio ni prensa (la alianza es con la consultora "Franquicias que Crecen").
- Cobertura en La Nación, Clarín, Infobae, iProUP, Ámbito; presencia en Hotelga/FEHGRA: no encontrada (búsquedas 2026-11-03 sin resultados).
- Perfil de Crunchbase: no localizado; YouTube "@bistrosoftglobal": no se pudo leer descripción ni cantidad de suscriptores (página bloqueada al fetch).
- Identidad de "Maria De Baere" y "Hernán Zbucki" (cargos) proviene de agregadores de datos; no verificada en fuente primaria.
