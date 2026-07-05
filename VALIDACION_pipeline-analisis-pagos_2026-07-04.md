# Validación del proyecto integrador — `pipeline-analisis-pagos`

**Fecha:** 04-07-2026 · **Repo:** https://github.com/ashley-toloza/pipeline-analisis-pagos (commit `04443f3`)
**Contra:** rúbrica y checklist de clase-08 (DPL1046, Prof. Rozas) + cobertura de clases 1–7
**Método:** clon fresco del repo, lectura completa del código, ejecución real de `main.py` y `pytest` (venv del diplomado, Python 3.13).

---

## Veredicto en una frase

El proyecto está **bien construido y cubre la rúbrica en lo conceptual**, pero tiene **2 problemas críticos que se ven apenas el profesor clona el repo**: (1) en un clon fresco `python main.py` **no ejecuta nada** (el guard de idempotencia se activa porque `output/` viene commiteado), y (2) el **`.env` con token está subido a GitHub público** — exactamente lo que evalúa el criterio de buenas prácticas. Ambos se arreglan en 15 minutos. Hay además un **bug de negocio**: las "640 órdenes críticas (canceladas o no disponibles)" de la presentación **no contienen ninguna cancelada**.

---

## Checklist del profesor (clase 8)

| Ítem | Estado | Nota |
|---|---|---|
| Pipeline corre completo con un comando | ⚠️ | Corre completo **solo si `output/` no existe**. En clon fresco se frena en 0.2 s sin procesar nada (verificado). |
| ≥2 fuentes reales | ✅ | 3 CSVs Olist + API `mindicador.cl` (con reintentos y fallback 180 CLP). |
| Tests en verde | ✅ | `3 passed in 2.57s` (pytest 9.1.1). El mínimo era 3 — van justos, sin holgura. |
| README claro | ⚠️ | Claro y completo, pero **miente en 2 puntos**: dice que `data/` está "Ignorados en Git" (está commiteado, 32 MB) y que `ordenes_criticas.csv` es "reporte de órdenes canceladas" (no contiene ninguna). |
| No duplica al re-correr | ⚠️ | Técnicamente no duplica (se detiene), pero no es la idempotencia del ejemplo del profe (re-correr y obtener el mismo resultado). Ver hallazgo 1. |
| Presentación con template | ✅ | 17 slides con el template UDLA, sin corchetes pendientes, sin slide de guía. Equipo: Mijael Inostroza · Ashley Toloza · Felipe Vallejos · Pablo Villegas. Incluye slide de uso de IA. |
| Explican su código | ⚠️ | Riesgos concretos de Q&A listados abajo. |

---

## Hallazgos críticos (arreglar antes del martes 07-07)

### 1. En un clon fresco, `python main.py` no hace nada 🔴

`output/` está commiteado en el repo. `main.py:69` frena si `output/resumen_ejecutivo.csv` existe:

```
WARNING |  ↳ El reporte ejecutivo 'resumen_ejecutivo.csv' ya existe en almacenamiento.
SUCCESS | ✅ El sistema detiene la ejecución de forma segura...
```

Eso es lo **primero** que verá el profesor si clona y corre. La demo en vivo muestra "funcionalidad cero" (35% de la nota). Además el guard no es idempotencia real: la carga SQLite ya es idempotente por sí sola (`if_exists="replace"`); el guard solo impide correr.

**Fix (elegir):**
- Mínimo: sacar `output/` de git (comandos abajo). El pipeline correrá siempre en clon fresco, y para la demo de "segunda corrida idempotente" corren dos veces seguidas.
- Mejor: reemplazar el "frenado" por re-generación (borrar el guard de `main.py:68-72`); la idempotencia la garantiza el `to_sql(..., if_exists="replace")` y el `to_csv` que sobreescribe — mismo input ⇒ mismo output, que es la definición que usó el profe.

### 2. `.env` con token commiteado en GitHub público 🔴

`git ls-files` incluye `.env`:

```
API_CLIENTES_URL="https://api.olist.com/v1/customers_secure"
API_AUTH_TOKEN="oll_live_7a8b9c2d3e4f5g6h7i8j"
```

Es el anti-patrón exacto que evalúa "Buenas prácticas (15%): Seguridad (.env)". Peor combinación posible: el README presume "Resguardo seguro de credenciales sensibles" y el log imprime el prefijo del token en consola. Riesgo extra de Q&A: **ese token no se usa en ninguna parte del código** y `mindicador.cl` no requiere autenticación — si el profe pregunta "¿qué protege ese token?", la respuesta honesta es "nada". Sugerencia: mover la **URL de la API** al `.env` (`API_URL=https://mindicador.cl/api/dolar`) para que el `.env` tenga un rol real, y borrar el token ficticio.

### 3. No existe `.gitignore` 🔴

Commiteados: `data/` (32 MB de CSVs), `output/`, `__pycache__/` (×2), `pipeline.log`, `.env`, `.Rhistory`. La rúbrica del proyecto de ejemplo dice explícitamente "datos en .gitignore".

**Comandos de arreglo (2-3):**

```bash
# en la raíz del repo
git rm -r --cached data output src/__pycache__ tests/__pycache__ .env pipeline.log .Rhistory
```

Crear `.gitignore`:

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

Commit + push. En el README, agregar al "Cómo correrlo" el paso "descargar los CSVs de Kaggle a `data/`" (como hace el profe). *Nota: el token queda en el historial de git; para la nota del curso basta con sacarlo del HEAD, pero que sepan que un token real habría que rotarlo.*

### 4. Bug de negocio: las "órdenes críticas" no contienen canceladas 🟠

- `transform.py:70` elimina **todas** las órdenes `canceled` (625) antes del merge.
- `pipeline.py:56` después filtra `order_status.isin(["canceled", "unavailable"])` — pero las canceladas ya no existen.
- Resultado verificado: `ordenes_criticas.csv` = **640 filas, todas `unavailable`, 0 canceladas**.

La presentación afirma: *"Detectamos 640 órdenes críticas (canceladas o no disponibles)"* y el README la describe como "Reporte de órdenes canceladas". Si el profe abre el CSV o pregunta cuántas canceladas hay, el hallazgo estrella se cae.

**Fix (elegir):**
- **(a) Correcto y más valioso:** en `pipeline.py`, construir `ordenes_criticas` desde el `df_orders` *original* (antes del filtro), manteniendo las canceladas fuera solo de las métricas de ingresos. Quedarían ~625 canceladas + 640 unavailable ≈ 1.265 órdenes críticas.
- **(b) Rápido:** cambiar README + slide a "órdenes no disponibles (unavailable)" y ajustar la narrativa.

---

## Hallazgos menores (pulir si hay tiempo)

1. **`config.yaml:18` comentario de borrador:** *"Tu variable de prueba. Cámbiala a 0.19 cuando termines el test"* — huele a copy-paste de IA/debug; borrarlo (dominio del código es parte del 30%).
2. **`extract.py:52` busca `config["paths"]["data_dir"]` pero el YAML define `rutas:`** → siempre cae al default `"data"`. Funciona de casualidad. Además las rutas por archivo (`rutas.pagos`, etc.) del YAML no se usan: los nombres están hardcodeados en `extract.py:55-57`, contradiciendo la slide "nada hardcodeado".
3. **Tabla 3 de consola** (`pipeline.py:127`) hardcodea 4 encabezados de métodos de pago; hoy calza porque `not_defined` se filtra (pagos = 0), pero es frágil.
4. **"Transacciones" = filas de payments**, no órdenes (una orden pagada con 3 vouchers cuenta 3). Defendible, pero que el equipo lo sepa explicar (103.886 pagos vs 99.441 órdenes).
5. **Hallazgo 3 de consola es texto fijo**, no calculado desde los datos — si preguntan "¿de dónde sale?", decir que es lectura de la Tabla 3, no un cálculo.
6. **Fallback y factor:** la API entrega USD→CLP; el factor BRL→USD 0,19 está fijo en YAML. Correcto hoy (1 BRL ≈ 175 CLP, verificado en vivo: $921,70 × 0,19), pero que sepan justificar el 0,19.
7. **Entorno de la demo:** el venv del diplomado no tenía `pytest` ni `pyyaml` (los instalé hoy). Verificar en la máquina que presenta: `pip install -r requirements.txt` antes del martes.

---

## Cobertura de las clases 1–7 (plan: que la respuesta abarque las 7)

| Clase | Tema | ¿Presente en el proyecto? |
|---|---|---|
| 1 | Setup, GitHub, VS Code | ✅ Repo GitHub público, estructura de proyecto, requirements.txt |
| 3 | Estructuras, funciones, validación, refactor | ✅ Código modular en `src/`, contratos con asserts, tests |
| 4 | Leer formatos, consumir API, API segura (.env), PII | ✅ CSV + API con reintentos; `.env` presente **pero mal usado** (hallazgo 2). PII: pueden mencionar en Q&A que Olist ya viene anonimizado |
| 5 | Pandas: filtrar, limpiar, combinar, agrupar | ✅ Filtros de calidad, 2 merges, groupby, crosstab |
| 6 | Script→programa, robustez, logging, config, producción | ✅ Orquestador `main.py`, loguru consola+archivo, config.yaml, try/except, fallback |
| 7 | APIs, combinar fuentes, API→DB, IA | ✅ API en vivo, SQLite con query SQL de auditoría, slide "Cómo usaste la IA" |

**Conclusión de cobertura: sí, el proyecto integra las 7 clases.** La única pieza de clase 7 no usada es el enriquecimiento con IA en el pipeline (opcional — la rúbrica dice explícitamente que no hay criterio de IA aparte).

---

## Estimación contra la rúbrica (estado actual → con fixes)

| Criterio | Peso | Hoy | Con fixes 1–4 |
|---|---|---|---|
| Funcionalidad | 35% | ⚠️ en riesgo (clon fresco no corre) | ✅ sólido |
| Calidad del código | 30% | ✅ bueno (modular, loguru, 3 tests verdes) | ✅ |
| Buenas prácticas | 15% | 🔴 comprometido (.env público, sin .gitignore, README inexacto) | ✅ |
| Presentación y valor | 20% | ✅ bueno (template completo, hallazgos claros) | ✅ (corrigiendo el "640 canceladas") |

## Prioridades para los 3 días que quedan

1. **Hoy:** `.gitignore` + `git rm --cached` (hallazgos 2 y 3) — 15 min.
2. **Hoy/mañana:** decidir fix del guard de idempotencia (hallazgo 1) y de órdenes críticas (hallazgo 4) — 30-60 min + re-correr tests y pipeline.
3. **Antes del martes:** actualizar README y slide de hallazgos con las cifras finales; ensayar respuestas a: "¿qué protege el .env?", "¿por qué 0,19?", "¿transacciones u órdenes?", "¿dónde están las canceladas?".
