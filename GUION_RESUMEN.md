# 🎯 Guion Express (1 página) — Métodos de Pago Olist · DPL1046
**15 min · Abrir `Presentacion_Final.html` → tecla `F` (pantalla completa) · navegar con `← →`**
*(Versión de bolsillo. El guion detallado está en `GUION_PRESENTACION.md`.)*

---

## ⏱️ Tiempos
| Slide | min | Quién |
|---|---|---|
| 1 Portada | 0:30 | Pablo |
| 3 Problema | 1:30 | Pablo |
| 4 Datos | 1:00 | Pablo |
| 6 Arquitectura | 1:30 | Genesis |
| 7 Decisiones técnicas | 1:45 | Genesis |
| 9 **DEMO** | 2:30 | Genesis |
| 11 Hallazgos | 1:30 | Pablo |
| 12 Gráfico | 1:00 | Pablo |
| 13 IA copiloto | 1:00 | Genesis |
| 15 Valor | 1:00 | Pablo |
| 16 Aprendizajes | 0:45 | Ambos |
| 17 Cierre | 0:20 | Pablo |

---

## 🗣️ Una frase por slide
1. **Portada** — "Somos Pablo y Genesis; un pipeline que analiza los métodos de pago de Olist."
3. **Problema** — "Olist mueve +100.000 pagos pero no sabe cómo, cuánto ni dónde paga su gente. Comercial y Finanzas lo necesitan."
4. **Datos** — "3 tablas Olist (pagos, órdenes, clientes), cruzadas por `order_id` y `customer_id`."
6. **Arquitectura** — "3 etapas en módulos separados: ingesta → transformación → salida. Todo local, un comando."
7. **Decisiones** — "Contratos con `assert`, `try/except` por capa, logging con niveles, 5 tests. Sin secretos en el código."
9. **DEMO** — *(ver abajo)*.
11. **Hallazgos** — "Tarjeta domina (74%); se financia (3,5 cuotas); la geografía manda (AM tarjeta vs RR boleto)."
12. **Gráfico** — "La barra de crédito aplasta al resto. 103 mil transacciones válidas."
13. **IA** — "La IA nos asistió, pero el pipeline es nuestro: revisamos, corregimos bugs y lo entendemos."
15. **Valor** — "Negociar comisiones de tarjeta (73% del volumen) y ofrecer boleto donde más se usa. Reemplaza el Excel manual."
16. **Aprendizajes** — "De un script suelto a un pipeline de producción: modular, testeado, idempotente."
17. **Cierre** — "Gracias, quedamos atentos a sus preguntas."

---

## 🔴 DEMO EN VIVO (2:30) — ensayar antes
1. `python -m pytest -v` → **"5 passed"**
2. `python main.py` → narrar: **backoff** → aísla **11 filas** → excluye **625 canceladas** → **contratos OK** → reporte
3. Mostrar la **tabla nacional + matriz de 27 estados** en consola
4. `python main.py` **otra vez** → **"detecta el reporte y se detiene: idempotencia"**

*(Antes: borrar `output/reporte_metodos_pago.csv` para que la 1ª corrida sea completa. Tener capturas de respaldo.)*

---

## 📊 Números clave (memorizar)
**credit_card 73,97%** · boleto 19,08% · voucher 5,48% · debit 1,47% · **3,5 cuotas** en crédito · ticket $163
**Geo:** AM 80,5% tarjeta (máx) · RR 28,9% boleto (máx) · 11 filas aisladas · 625 canceladas

---

## ❓ Preguntas — respuesta en 1 línea
- **¿Falla a propósito?** → demo didáctico de backoff; los errores reales (archivo/CSV) NO reintentan.
- **¿'pedidos' son únicos?** → no, son **líneas de pago** (un pedido puede tener 2 métodos); correcto para este análisis.
- **¿Contrato de datos?** → reglas con `assert` (columnas, tipos, montos≥0, cuotas≥1) antes de procesar.
- **¿`merge` inner?** → descarta pagos huérfanos y no infla métricas (canceladas ya fuera).
- **¿`crosstab`?** → matriz estado × método normalizada por fila = % de cada método por estado.
- **¿Idempotencia?** → correr 2 veces no corrompe ni duplica; si el reporte existe, se detiene.

---

## ✅ Antes de empezar
- [ ] Apellido de Genesis en portada y cierre.
- [ ] Presentación en **pantalla completa (F)**, pantalla ≥ 1280px.
- [ ] Terminal en la carpeta, entorno instalado (`pip install -r requirements.txt`).
- [ ] `output/` vacía (borrar el CSV si quedó de una prueba).
- [ ] Capturas de respaldo de la demo.
- [ ] Un ensayo cronometrado.
