# 🧠 Memoria de Sesión — Validación repo grupal + PPT final (Proyecto Integrador DPL1046)

**Fecha:** 04-jul-2026 · **Curso:** DPL1046 — Diplomado en Ingeniería de Datos con Python, UDLA (Prof. Juan Manuel Rozas)
**Equipo:** Mijael Inostroza · Ashley Toloza · Felipe Vallejos · Pablo Villegas · **Presentan: martes 07-07-2026** (10-12 min + 5 Q&A)

> **Para replicar en otra cuenta/IA:** todo lo necesario está en esta memoria + el repo público
> `https://github.com/ashley-toloza/pipeline-analisis-pagos` (commit validado: `04443f3`) — los CSVs de Olist
> (~32 MB) vienen commiteados en el repo, así que un `git clone` basta. No hay insumos no descargables.
> Entregables de esta sesión (acompañan a esta memoria en `Proyecto\Claude\`):
> `VALIDACION_pipeline-analisis-pagos_2026-07-04.md` y `Presentacion_Final_Pipeline_Pagos_Claude.html` (la PPT FINAL, corregida).

---

## 1. Contexto (resumen de la sesión 30-jun, para autosuficiencia)

- Proyecto Integrador = **Examen 100%** del curso. Pipeline ETL local en Python sobre dataset Olist.
- Rúbrica: Funcionalidad 35% / Calidad código 30% / Buenas prácticas 15% / Presentación y valor 20%.
- Checklist del profe (clase 8): pipeline corre completo con 1 comando · ≥2 fuentes reales · tests en verde ·
  README claro · no duplica al re-correr · presentación con su template HTML · explicar cualquier parte del código.
- En sesión 30-jun se había arreglado una versión propia (v2.0 Claude, repo
  `villegates/UDLA_Proyecto_Integrador_v2.0_Claude`): 5 tests, output/ fuera de git, hallazgo 3 calculado.
  **El grupo NO incorporó esos fixes**: la entrega oficial es otro codebase (de Ashley) que evolucionó
  (merge con customers, loguru, auditoría SQL) pero **reintrodujo los mismos errores ya corregidos**.

## 2. Qué se hizo en esta sesión (04-jul)

1. **Validación completa del repo grupal** contra la rúbrica/checklist de clase-08 y cobertura de clases 1–7:
   clon fresco + lectura de todo el código + ejecución real (`main.py` y `pytest`).
2. **Informe** → `VALIDACION_pipeline-analisis-pagos_2026-07-04.md` (misma carpeta).
3. **PPT final en HTML** → `Presentacion_Final_Pipeline_Pagos_Claude.html`: copia de la del repo (17 slides,
   template UDLA del profe) con 3 correcciones de texto (ver §5).
4. Memoria interna de Claude actualizada (equipo real, repo oficial, hallazgos).
5. En curso al cierre: reemplazar el contenido de `villegates/UDLA_Proyecto_Integrador_v2.0_Claude` por lo de esta
   sesión (proyecto grupal validado + entregables Claude; v2.0 del 30-jun queda en el historial git).

## 3. Resultado de la validación — cifras exactas (para verificar réplica)

**Entorno:** Python 3.13.5, venv del diplomado (`diplomado-idsdata-juanmarozas\.venv`). **OJO:** le faltaban
`pytest` y `pyyaml` → los instalé (`pip install pytest pyyaml`). En la máquina de la demo: `pip install -r requirements.txt`.

- Tests: **3/3 PASSED** (`test_aislamiento_datos_sucios`, `test_filtrado_ordenes_canceladas`,
  `test_comportamiento_tipos_y_columnas`) en 2.57s, pytest 9.1.1.
- Pipeline (tras borrar `output/`): corre completo. 11 filas de pagos aisladas (montos ≤0 / cuotas <1);
  órdenes 98.816 válidas de 99.441 (excluye 625 `canceled`); API viva: 1 USD = $921,70 CLP × factor 0,19
  → 1 BRL ≈ $175,12 CLP (fallback si API cae: 180,0).
- Top estado: São Paulo — 43.267 transacciones, 5.942.338,42 BRL, 1.040.640.131 CLP.
- Método dominante: credit_card — 76.349 transacciones, 78,4% del monto.
- `ordenes_criticas.csv`: **640 filas, TODAS `unavailable`, 0 canceladas** (ver hallazgo C4).
- Segunda corrida de `main.py`: se detiene por el guard ("El reporte ejecutivo ya existe").
- Cobertura clases 1–7: **completa** (GitHub c1 · funciones/contratos c3 · API+.env c4 · pandas merge/groupby/crosstab c5 ·
  logging/config/robustez c6 · API→SQLite+SQL+slide IA c7). La rúbrica no exige IA ni cloud aparte.

## 4. Los 4 hallazgos críticos (detalle completo en el informe)

| # | Hallazgo | Fix recomendado |
|---|---|---|
| C1 | `output/` commiteado → **en clon fresco `python main.py` es NO-OP** (guard de "idempotencia" en `main.py:69`). Primera impresión del profe = pipeline no hace nada. | Sacar `output/` de git; idealmente borrar el guard (`main.py:68-72`) — la idempotencia real ya la da `to_sql(if_exists="replace")` + `to_csv` que sobreescribe. |
| C2 | **`.env` con token commiteado en GitHub público** (`API_AUTH_TOKEN="oll_live_..."`). Además el token es decorativo: no se usa en el código y mindicador.cl no requiere auth. | Borrar del repo, `.gitignore`. Darle rol real al `.env` (p.ej. `API_URL=`). El token queda en el historial — si fuera real habría que rotarlo. |
| C3 | **No hay `.gitignore`**: data/ (32 MB), `__pycache__`, `pipeline.log`, `.Rhistory`, `.env` versionados. README miente ("data/ ... Ignorados en Git"). | Ver comandos abajo. |
| C4 | **"640 órdenes críticas (canceladas o no disponibles)" es falso**: `transform.py:70` elimina todas las canceladas antes del merge → las 640 son solo `unavailable`. | (a) construir `ordenes_criticas` desde `df_orders` original (~625 canceled + 640 unavailable), o (b) corregir la narrativa a "no disponibles" (aplicado en la PPT corregida). |

**Comandos del fix C2+C3:**
```bash
git rm -r --cached data output src/__pycache__ tests/__pycache__ .env pipeline.log .Rhistory
```
`.gitignore`:
```gitignore
.env
data/
output/
__pycache__/
*.pyc
.pytest_cache/
pipeline.log
.Rhistory
.venv/
```

**Menores:** comentario de borrador en `config.yaml:18` ("Tu variable de prueba...") · `extract.py:52` busca
`config["paths"]` pero el YAML usa `rutas:` (siempre cae al default, funciona de casualidad; rutas por archivo
hardcodeadas) · Tabla 3 de consola hardcodea 4 encabezados de métodos · "transacciones" = filas de payments
(103.886) no órdenes (99.441) · hallazgo 3 de consola es texto fijo, no calculado.

## 5. Toolchain portable — patch de la PPT (anexo, código completo)

La PPT corregida (`Presentacion_Final_Pipeline_Pagos_Claude.html`) se regenera desde el repo con este script
(3 reemplazos, se asertan únicos):

```python
# patch_presentacion.py — regenera Presentacion_Final_Pipeline_Pagos_Claude.html corregida
# Uso: clonar el repo, ajustar rutas src/dst, correr con Python 3.x (sin dependencias)
src = "pipeline-analisis-pagos/Presentacion_Final_Pipeline_Pagos.html"   # del repo
dst = "Presentacion_Final_Pipeline_Pagos_Claude.html"                    # corregida (PPT FINAL)
s = open(src, encoding="utf-8").read()

edits = [
 # 1. Slide contexto: no prometer "canceladas" que el pipeline excluye
 ("cuántas transacciones críticas (canceladas o no disponibles) están en riesgo?",
  "cuántas órdenes en estado crítico (no disponibles) ponen flujo de caja en riesgo?"),
 # 2. Slide buenas prácticas: el .env no guarda credenciales reales
 ("<b>Seguridad:</b> credenciales fuera del código, cargadas desde .env con python-dotenv (nunca hardcodeadas en los scripts).",
  "<b>Seguridad:</b> configuración sensible fuera del código, cargada desde .env con python-dotenv (nunca hardcodeada en los scripts) y excluida del repositorio vía .gitignore."),
 # 3. Slide hallazgos: 640 = solo unavailable; canceladas se excluyen por diseño
 ("Detectamos 640 órdenes críticas (canceladas o no disponibles) que representan flujo de caja en riesgo y quedan aisladas en un reporte aparte para seguimiento operativo.",
  "Detectamos 640 órdenes en estado crítico <b>unavailable</b> (no disponibles), flujo de caja en riesgo que queda aislado en un reporte aparte para seguimiento operativo; las órdenes canceladas se excluyen antes del análisis para no inflar las métricas de ingreso."),
]
for old, new in edits:
    assert s.count(old) == 1, f"string no único o ausente: {old[:60]}"
    s = s.replace(old, new)

open(dst, "w", encoding="utf-8").write(s)
print("OK:", dst, len(s), "bytes")   # esperado: 62.867 bytes (original 62.719)
```

Gotchas del deck (heredados de la sesión 30-jun): presentar a **≥1280px o fullscreen (tecla F)** — el `.deck`
se encoge en ventanas angostas y el texto desborda (falso positivo). Navegación ← →.

## 6. Otros frentes (multi-IA) — estado al cierre de esta sesión

- **Antigravity** trabaja en `Proyecto\AntiG\` (copia del proyecto con fixes propios aplicados, dice tener 8 tests
  PASS y un componente de IA con fallback) y generó **su propio deck** `Presentacion_Final_AntiGravity.html`
  (diseño propio "OLIST PAYMENTS", NO usa el template del profe — ojo con el checklist "presentación con template").
  Llegó a escribir dentro de `Proyecto\Claude\` (borró esta memoria y puso su deck como `..._Claude.html`);
  Pablo le pidió quedarse en AntiG. Esta memoria fue restaurada desde la sesión Claude.
- **SVC** (`Proyecto\SVC\`): otro frente con `validacion_desarrollo.md` y decks propios — no revisado por Claude.
- **La PPT final designada por Pablo es la de Claude**: `Proyecto\Claude\Presentacion_Final_Pipeline_Pagos_Claude.html`
  (template del profe + 3 correcciones).

## 7. Pendientes / decisiones abiertas

1. ⏳ Reemplazar contenido de `villegates/UDLA_Proyecto_Integrador_v2.0_Claude` por lo de esta sesión (ordenado por Pablo; en curso).
2. ⏳ Grupo aplica fixes C1–C3 en el repo grupal de GitHub (15 min) — **antes del martes 07-07**.
3. ⏳ Decidir C4: si adoptan fix (a) (incluir canceladas → ~1.265 órdenes críticas), actualizar la cifra en la
   slide de hallazgos y en el README. La PPT corregida asume la opción (b) = código actual.
4. ⏳ Si eliminan el guard de idempotencia (C1 opción "mejor"), actualizar 2 textos de la PPT: bullet
   "Idempotencia" (buenas prácticas) y "Segunda corrida: ...se detiene" (slide demo) — hoy describen el código actual.
5. ⏳ Ensayar Q&A: ¿qué protege el .env? · ¿por qué factor 0,19? · ¿transacciones u órdenes? ·
   ¿dónde están las canceladas? · ¿por qué loguru y no logging?
