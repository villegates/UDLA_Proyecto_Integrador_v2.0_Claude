# 🎤 Guion de Presentación — Proyecto Integrador DPL1046
### "Análisis de Métodos de Pago en Olist" · Pablo Villegas y Genesis

> **Formato:** 15 min de exposición + 5 min de preguntas.
> **Meta de tiempo:** ~14:00 de exposición (deja ~1 min de colchón).
> **Regla de oro:** las slides son apoyo, NO libreto. No leas la pantalla: mirá al profe y contá.
> Abrir `Presentacion_Final.html` en el navegador y presionar **F** (pantalla completa). Navegar con **← →**.

---

## ⏱️ Reparto de tiempos (resumen)

| # | Slide | Tiempo | Quién |
|---|---|---|---|
| 1 | Portada | 0:30 | Pablo |
| 2 | *(divisor)* El problema | 0:05 | — |
| 3 | ¿Qué problema resuelve? | 1:30 | Pablo |
| 4 | Los datos (3 tablas) | 1:00 | Pablo |
| 5 | *(divisor)* Arquitectura | 0:05 | — |
| 6 | Flujo del pipeline | 1:30 | Genesis |
| 7 | Decisiones técnicas | 1:45 | Genesis |
| 8 | *(divisor)* Demo | 0:05 | — |
| 9 | **Demo en vivo** | 2:30 | Genesis |
| 10 | *(divisor)* Resultados | 0:05 | — |
| 11 | Hallazgos | 1:30 | Pablo |
| 12 | Gráfico | 1:00 | Pablo |
| 13 | IA como copiloto | 1:00 | Genesis |
| 14 | *(divisor)* Valor | 0:05 | — |
| 15 | Valor de negocio | 1:00 | Pablo |
| 16 | Aprendizajes | 0:45 | Ambos |
| 17 | Cierre → preguntas | 0:20 | Pablo |
| | **TOTAL** | **~14:00** | |

> El reparto Pablo/Genesis es una sugerencia. Lo importante: **los dos hablan** y **los dos pueden responder cualquier pregunta** (eso lo evalúa la rúbrica).

---

## 📝 Guion slide por slide

### 1 · Portada — *0:30 · Pablo*
> "Buenas, somos Pablo y Genesis. Nuestro proyecto integrador es un **pipeline de datos que analiza los métodos de pago del ecommerce Olist de Brasil**. En los próximos 15 minutos les mostramos el problema, cómo lo construimos, una demo en vivo y qué encontramos."

Arranca con energía. No te quedes en la portada.

---

### 3 · ¿Qué problema resuelve? — *1:30 · Pablo*
- "Olist mueve **más de 100.000 pagos**, pero no tiene una foto clara de **cómo paga su gente**: ¿tarjeta o boleto? ¿en cuántas cuotas? ¿cambia según la región?"
- "Eso lo necesitan **Comercial y Finanzas**: para negociar comisiones con los medios de pago, diseñar promociones y **gestionar el riesgo del crédito en cuotas**."
- Cierra con la frase de la derecha: "En una frase: convertimos los datos crudos de pagos en un **reporte automático y confiable** de cómo, cuánto y dónde paga la gente."

💡 *Traducí el problema a plata/decisiones, no a código. Que un gerente lo entienda.*

---

### 4 · Los datos — *1:00 · Pablo*
- "Usamos **3 tablas de Olist** — supera el mínimo de 2 que pedía el proyecto."
- Señalá la tabla: "**Pagos** (103 mil filas) nos da método, monto y cuotas; **Órdenes** (99 mil) el estado, para sacar las canceladas; y **Clientes** (99 mil) el estado geográfico."
- "Las cruzamos por `order_id` y `customer_id`."

💡 *No leas cada fila; apuntá con el dedo y resumí.*

---

### 6 · Flujo del pipeline — *1:30 · Genesis*
- "La arquitectura sigue **3 etapas**, cada una en su módulo — no es un script monolítico."
- **Ingesta** (`extract.py`): "lee los 3 CSV con **reintentos y backoff exponencial**, y valida un **contrato de datos** antes de dejar pasar nada."
- **Transformación** (`transform.py` + `pipeline.py`): "limpia, filtra, une las tablas con `merge` y agrega con `groupby` y `crosstab`."
- **Salida** (`main.py`): "genera un CSV consolidado y un reporte ejecutivo en consola."
- Remate: "Todo corre **local en Python, con un solo comando. Sin nube.**"

---

### 7 · Decisiones técnicas — *1:45 · Genesis*
Recorré los 4 puntos, uno por uno, sin leerlos textual:
- **Validación:** "un **contrato de datos** con `assert`: si un pago viene negativo o sin columna clave, el pipeline lo aísla o se detiene."
- **Errores y logging:** "usamos `try/except` **específicos por capa** — no un `except` genérico — y **logging con niveles**, no `print`."
- **Seguridad:** "no hay credenciales porque son archivos locales; los parámetros van en `config.yaml`, fuera del código. Si hubiera secretos, irían en variables de entorno."
- **Tests:** "**5 pruebas con pytest**, incluyendo un caso negativo." → señalá la caja verde de la derecha.

💡 *Este slide es clave para "calidad de código". Mostrá seguridad.*

---

### 9 · DEMO EN VIVO — *2:30 · Genesis* 🔴 *(lo más importante)*
1. Terminal en la carpeta del proyecto. **Primero los tests:**
   ```
   python -m pytest -v
   ```
   → "5 passed. Los tests cubren la limpieza, los contratos y la agregación."
2. **Después el pipeline:**
   ```
   python main.py
   ```
   → Mientras corre, narrá: "acá se ven los **reintentos con backoff**… ahora **aísla 11 filas inválidas**… **excluye 625 órdenes canceladas**… valida los contratos… y genera el reporte."
3. Mostrá la tabla nacional + la matriz de 27 estados que imprime en consola.
4. **Idempotencia:** corré `python main.py` **otra vez** → "fíjense que ahora detecta que el reporte ya existe y **se detiene solo, para no malgastar cómputo**."

⚠️ **Ensayá esto antes.** Si el equipo del profe es lento, tené **capturas de respaldo**. Una demo que se cuelga baja la nota.

---

### 11 · Hallazgos — *1:30 · Pablo*
- "Tres hallazgos concretos, todos respaldados con números:"
- "**Uno: la tarjeta de crédito domina** — 73,97% de las transacciones y el ticket más alto, 163 dólares."
- "**Dos: ese crédito se financia** — 3,5 cuotas promedio. Hay una dependencia fuerte del pago diferido."
- "**Tres: la geografía manda** — en Amazonas el 80% paga con tarjeta; en Roraima casi el 29% usa boleto. Hay una **brecha de bancarización** entre regiones."
- Dato clave (derecha): "el número que nos quedó grabado: **casi 3 de cada 4 pagos son con crédito**."

---

### 12 · Gráfico — *1:00 · Pablo*
- "Este gráfico resume el hallazgo principal: la barra de `credit_card` aplasta a las demás."
- "Boleto es segundo con 19%, y voucher y débito son marginales."
- "Son **103 mil transacciones válidas** después de limpiar."

💡 *Un gráfico se explica en 3 frases. No te extiendas.*

---

### 13 · IA como copiloto — *1:00 · Genesis*
- "Usamos IA como **asistente de código**, como permite el curso — pero el pipeline es nuestro y lo entendemos."
- "**Nos ayudó** con el andamiaje de funciones y el manejo de excepciones."
- "**Revisamos y corregimos**: por ejemplo, un bug donde el CSV perdía la columna del método de pago, y la lógica de un hallazgo geográfico que estaba mal calculada."
- "Lo que **dominamos**: `merge`, `groupby`, `crosstab`, el backoff, los contratos y los tests — podemos explicar cada decisión."

💡 *Este slide te blinda contra la pregunta "¿esto lo hicieron ustedes?". Sé honesto y seguro.*

---

### 15 · Valor de negocio — *1:00 · Pablo*
- "¿Qué habilita esto? **Negociar comisiones** con los proveedores de tarjeta, que son el 73% del volumen, y **ofrecer boleto** donde más se usa."
- "**Reemplaza** el análisis manual en Excel por un reporte **reproducible con un comando**."
- "El siguiente paso sería llevarlo a una base de datos y **agendarlo** para que corra solo."

---

### 16 · Aprendizajes — *0:45 · Ambos*
- Pablo: "Lo más difícil fue pasar de un script suelto a un **pipeline de verdad**: modular, con contratos, tests e idempotencia."
- Genesis: "Lo que haríamos distinto: escribir los **tests desde el inicio**. Y lo que nos llevamos: cómo se construye **software de datos de producción**."

---

### 17 · Cierre — *0:20 · Pablo*
> "Eso es todo: de un CSV crudo a un reporte automático que responde una pregunta de negocio real. **Gracias, quedamos atentos a sus preguntas.**"

---

## ❓ Preparación para las preguntas (5 min)

Ensayen estas respuestas — son las que el profe suele pinchar:

**"¿Por qué el pipeline 'falla' a propósito en cada corrida?"**
> "Es una **simulación didáctica** para demostrar el reintento con backoff exponencial. Los errores reales —archivo inexistente o CSV corrupto— NO reintentan: fallan al toque. Solo el 'fallo de red' simulado amerita reintentar."

**"La columna se llama 'pedidos', ¿son pedidos únicos?"**
> "Buena observación: en realidad cuenta **líneas de pago**, no pedidos únicos — un pedido puede tener voucher + tarjeta. Para análisis de métodos de pago es lo correcto (cada línea tiene un método), pero el nombre podría ser 'transacciones'."

**"¿Qué es un 'contrato de datos'?"**
> "Un conjunto de reglas con `assert` que los datos deben cumplir antes de seguir: columnas obligatorias, tipos correctos, montos ≥ 0, cuotas ≥ 1. Si no se cumplen, el pipeline se detiene con un error claro en vez de producir basura."

**"¿Por qué `merge` con `inner` y no `left`?"**
> "Con `inner` nos quedamos solo con pagos que tienen orden válida y cliente válido. Descarta huérfanos y, como las órdenes ya vienen sin canceladas, no inflamos las métricas."

**"¿Qué hace `crosstab`?"**
> "Arma la matriz estado × método de pago, normalizada por fila, para ver el **% de cada método dentro de cada estado**. Así comparamos regiones."

**"¿Qué es idempotencia y por qué importa?"**
> "Que correr el pipeline dos veces no corrompe ni duplica nada. Si el reporte ya existe, se detiene. En producción evita reprocesar y gastar cómputo."

**"¿Cómo separan datos buenos de malos?"**
> "Un filtro booleano aísla los pagos con monto ≤ 0 o cuotas < 1 (aislamos 11), y excluimos las 625 órdenes canceladas. Lo dejamos registrado en el log."

---

## ✅ Checklist antes de presentar
- [ ] Completar el **apellido de Genesis** en portada y cierre.
- [ ] Abrir la presentación en **pantalla completa (F)**, ventana ≥ 1280px.
- [ ] Terminal lista en la carpeta del proyecto, con el entorno instalado (`pip install -r requirements.txt`).
- [ ] Borrar `output/reporte_metodos_pago.csv` antes de la demo (para que la 1ª corrida sea completa).
- [ ] Tener **capturas de respaldo** de la demo por si falla en vivo.
- [ ] Ensayar cronometrado al menos una vez.
