# 🧠 Memoria de Sesión — Proyecto Integrador DPL1046 (Pipeline de Pagos Olist)
**Fecha:** 30-jun-2026 · **Curso:** DPL1046 "Programación en Python y Manipulación de Datos" — Diplomado en Ingeniería de Datos con Python, UDLA · **Equipo:** Pablo Villegas y Genesis

---

## 1. Objetivo de la tarea
El **Proyecto Integrador = Examen (100% de la nota)**. Consiste en construir un **pipeline de datos ETL 100% local en Python** sobre el dataset **Olist**, y presentarlo en **15 min + 5 de preguntas** (fecha en el template: 07-07-2026).

**Objetivo explícito de Pablo:** que la tarea pase **transversal por TODO el material de clases**, para que el profe valide que aprendieron.

**Rúbrica — 4 criterios:**
| Criterio | Peso |
|---|---|
| Funcionalidad del pipeline | 35% |
| Calidad del código | 30% |
| Buenas prácticas | 15% |
| Presentación y valor de negocio | 20% |

---

## 2. El proyecto
Pipeline ETL que analiza los **métodos de pago** del ecommerce Olist (Brasil), integrando 3 tablas:
- `olist_order_payments_dataset.csv` (103.886 filas) — método, monto, cuotas.
- `olist_orders_dataset.csv` (99.441) — estado de la orden (para excluir canceladas).
- `olist_customers_dataset.csv` (99.441) — estado geográfico del cliente.

**Arquitectura por capas:** `config.yaml` (config externa) · `main.py` (orquestador, idempotente) · `src/extract.py` (ingesta con retry/backoff) · `src/transform.py` (limpieza + contratos de datos) · `src/pipeline.py` (merge/groupby/crosstab + análisis) · `tests/`.

---

## 3. Cronología y diagnóstico

### v1 (primera entrega) — tenía 2 BUGS CRÍTICOS
Al correrla de verdad se detectó:
1. 🔴 **Los 3 tests pytest FALLABAN** — los fixtures no incluían la columna `payment_type` que el contrato `validar_contrato_pagos` exige. Y el README mostraba un output de pytest **VERDE inventado** (riesgo de integridad).
2. 🔴 **El CSV de salida salía SIN la columna `payment_type`** — `to_csv(index=False)` sobre un `groupby` que tenía `payment_type` como índice → el entregable principal quedaba inservible.
Otros: `config.yaml` casi decorativo (extract.py hardcodeaba todo), README malformado.

### v2.0 (segunda entrega) — los 2 críticos YA venían resueltos
Verificado corriendo el código:
- ✅ 3 tests PASS.
- ✅ CSV con `customer_state,payment_type,...` (usa `reset_index`).
- ✅ `config.yaml` ahora SÍ se usa (rutas + backoff).
- ✅ Excepciones específicas por capa.
- ✅ **Nuevo:** análisis geográfico (groupby estado+método, `pd.crosstab` sobre 27 estados).

**Ubicación v2.0:** `...\Modulo 2\Tarea_v2.0\pipeline-analisis-pagos\`

---

## 4. Parte A — Arreglos de código aplicados (esta sesión)
Sobre `Tarea_v2.0\pipeline-analisis-pagos\`, todos verificados:

1. **CSV shippeado eliminado.** El reporte venía incluido en la entrega → la 1ª corrida del profe era un no-op por idempotencia. Se borró; `output/` queda con `.gitkeep` (vacía). La 1ª corrida ahora ejecuta completo.
2. **Hallazgo 3 corregido** (`src/pipeline.py`). Antes tomaba el estado de *menor crédito* y lo llamaba "mayor boleto" (impreciso). Ahora usa `idxmax()` real de la columna boleto → **RR (28,89%)**. Verificado corriendo.
3. **README saneado.** Se quitó la ruta `C:\Users\Genesis\Desktop\...` del output de pytest y se agregó una nota explicando que `output/` se genera sola.
4. **Basura eliminada.** `.Rhistory` (residuo de RStudio), `output/pipeline.log` viejo (loguru hoy escribe solo a consola, no a archivo) y cachés.

---

## 5. Parte B — Presentación
Se creó **`Presentacion_Final.html`** (copia rellenada del template oficial, sin tocar el original):
- **17 slides** (se borró la slide-guía "cómo usar el template").
- Los 18 placeholders rellenados con contenido real: problema → datos → arquitectura → decisiones → demo → resultados → gráfico → IA → valor → aprendizajes → cierre.
- **Gráfico de barras CSS** embebido (participación nacional por método).
- Output real de pytest (5 tests) en el slide de decisiones técnicas.
- Verificado renderizando: **0 slides con desborde** a 1280px.

Además se escribió **`GUION_PRESENTACION.md`** (script de 15 min con reparto de tiempos Pablo/Genesis + preparación de las preguntas probables).

---

## 6. Tests — se sumaron 2 (ahora 5 en total, todos PASS)
- `test_transform.py`:
  1. `test_aislamiento_datos_sucios`
  2. `test_filtrado_ordenes_canceladas`
  3. `test_comportamiento_tipos_y_columnas`
  4. **`test_contratos_rechazan_datos_invalidos`** ← NUEVO (caso negativo: los contratos LANZAN `AssertionError` con `pytest.raises`).
- `tests/test_pipeline.py` (NUEVO):
  5. **`test_generar_analisis_pagos_agrega_y_calcula_participacion`** ← NUEVO (verifica merge + groupby + que la participación por estado sume 100%).

`python -m pytest -v` → **5 passed in 1.12s**.

---

## 7. Datos y hallazgos clave (números reales)
**Nacional** (103.214 transacciones válidas; se aislaron 11 filas inválidas y 625 órdenes canceladas):
| Método | Transacciones | Ticket prom. | Cuotas | Participación |
|---|---|---|---|---|
| credit_card | 76.349 | $163,00 | 3,51 | **73,97%** |
| boleto | 19.689 | $144,85 | 1,00 | **19,08%** |
| voucher | 5.654 | $62,57 | 1,00 | **5,48%** |
| debit_card | 1.522 | $141,44 | 1,00 | **1,47%** |

**Geográfico:** estado con más crédito = **AM (Amazonas) 80,52%**; estado con más boleto = **RR (Roraima) 28,89%**. → brecha de bancarización regional.

**Los 3 hallazgos de negocio:** (1) la tarjeta domina (74%); (2) el crédito se financia (3,5 cuotas); (3) la geografía manda (AM tarjeta vs RR boleto).

---

## 8. Entregables y ubicaciones
**TODO lo desarrollado vive en una sola carpeta canónica:** `...\Modulo 2\Claude\`
  - `pipeline-analisis-pagos/` (proyecto limpio, 5 tests PASS, listo para empaquetar)
  - `Presentacion_Final.html`
  - `GUION_PRESENTACION.md` (guion detallado, 15 min)
  - `GUION_RESUMEN.md` (versión express de 1 página, para tener al lado al presentar)
  - `MEMORIA_SESION.md` (este archivo)
  - `README.md` + `.gitignore` (para el repositorio)

**📦 Repositorio GitHub (privado):** https://github.com/villegates/UDLA_Proyecto_Integrador_v2.0_Claude — todo el contenido de `Claude\` está publicado en la rama `main`.

Los **fuentes/originales** quedan en `...\Modulo 2\`: `Rubrica_Proyecto_Integrador.html`, `Template_Presentacion_Final.html/.pptx`, y los `.rar` fuente (`pipeline-analisis-pagos.rar` = v1; `Tarea_v2.0\pipeline-analisis-pagos_final.rar` = v2). El 30-jun se **borraron los duplicados**: la extracción v1 (con su venv, 169 MB) y las copias de trabajo en `Tarea_v2.0\` (proyecto + presentación), que ya estaban en `Claude\`.

Estructura final del proyecto (limpia):
```
pipeline-analisis-pagos/
├── config.yaml
├── main.py
├── README.md
├── requirements.txt
├── data/    (3 CSV Olist)
├── src/     (extract · transform · pipeline · __init__)
├── tests/   (test_transform.py · test_pipeline.py)
└── output/  (.gitkeep — vacío, se llena en la 1ª corrida)
```

---

## 9. Gotchas técnicos (importante)
- **La presentación se debe ver a ≥1280px o en pantalla completa (tecla F).** El `.deck` del template es un flex-child con `width:1280px` pero SIN `flex-shrink:0`: en ventana angosta se encoge y el texto se reflowa/desborda. Es un falso positivo del preview chico; a tamaño presentación entra perfecto.
- **Entorno:** para validar se reutilizó el venv de v1 (`...\pipeline-analisis-pagos\pipeline-analisis-pagos\.venv`, Python 3.13, pandas 3.0.3). Para el profe, basta `pip install -r requirements.txt`.
- **Correr los tests con `python -m pytest`** (no `pytest` pelado) para que `src` resuelva en el `sys.path`.

---

## 10. Pendientes / opcionales
- ⏳ **Completar el apellido de Genesis** en la portada y el cierre de la presentación (hoy dice "Pablo Villegas · Genesis").
- (Opcional) Antes de empaquetar el `.zip`, confirmar que `output/` esté vacía (solo `.gitkeep`).
- **Para la defensa:** los dos deben poder explicar las partes AI-idiomáticas (`crosstab`, `transform`, el diseño del retry/backoff, los contratos). Ver la sección de preguntas del `GUION_PRESENTACION.md`.

---

## 11. Estado final
✅ Código: pipeline corre end-to-end con un comando, 5 tests en verde, reproducible, config externalizada, excepciones específicas, idempotente. Cubre transversalmente el material de clases (ingesta, validación, contratos, pandas avanzado, logging, tests, buenas prácticas).
✅ Presentación: 17 slides completas con datos reales + gráfico + guion de 15 min.
⏳ Solo falta el apellido de Genesis y ensayar la demo cronometrada.
