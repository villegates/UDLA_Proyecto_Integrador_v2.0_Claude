# Pipeline de Producción ETL: Análisis de Métodos de Pago (Olist Brasil)
**DPL1046 · Unidad 2: Manipulación y Transformación de Datos con Python**

> De un script analítico aislado a un programa automatizado, robusto e idempotente para la toma de decisiones financieras.

Este proyecto consolida de forma segura los datos transaccionales del ecommerce de Olist (Pagos, Órdenes y Clientes). Su objetivo es limpiar anomalías operativas, mitigar el ruido de transacciones canceladas y asegurar contratos de calidad para generar un reporte ejecutivo automatizado sobre el comportamiento y rendimiento de los métodos de pago.

## 🚀 Instalación
```bash
pip install -r requirements.txt
```

Nota: Asegúrate de tener los archivos fuentes del dataset de Olist dentro de la carpeta `data/`.

## 📂 Arquitectura del Proyecto (Por Capas)

Siguiendo las buenas prácticas de producción vistas en clase, el código se modularizó para separar responsabilidades en lugar de usar un script monolítico.

| Archivo | Capa / Módulo | Buenas Prácticas de Producción Aplicadas |
|---|---|---|
| `config.yaml` | Configuración Externa | Parámetros y reglas de negocio fuera del código (sin hardcodeo): rutas de origen y parámetros de reintento (`intentos_backoff`, `espera_inicial`). |
| `main.py` | Orquestador Principal | Centraliza el flujo completo, maneja errores críticos globales y controla las rutas relativas. |
| `src/extract.py` | Extracción (Ingesta) | Resiliencia mediante simulación de fallos, reintentos (retry) y tolerancia a fallos con try-except-continue aplicando Exponential Backoff, con parámetros leídos desde `config.yaml`. |
| `src/transform.py` | Transformación y Calidad | Aislamiento de datos sucios y verificación estricta de Contratos de Datos (`assert`). |
| `src/pipeline.py` | Lógica de Negocio / KPI | Cruzado de tablas (`merge`), agregaciones (`groupby`, `crosstab`), Idempotencia y respuestas analíticas automáticas. |
| `tests/test_transform.py` | Pruebas de Transformación | Tests de la capa de limpieza y de los contratos de datos (incluye caso negativo con `pytest.raises`). |
| `tests/test_pipeline.py` | Pruebas de Análisis | Test de la agregación por estado × método (`merge` + `groupby`). |

> **Cobertura:** 5 pruebas automatizadas con `pytest` (supera el mínimo de 3), cubriendo casos válidos, casos de borde y casos negativos.

## ⚙️ Cómo Correr el Proyecto

Para garantizar la correcta resolución de rutas relativas y módulos internos (`src`) de manera portable entre diferentes entornos y sistemas operativos sin alterar la estructura del proyecto, se debe utilizar el contexto del intérprete de Python para ejecutar las pruebas.

Ejecuta las pruebas de calidad y luego el orquestador principal desde la terminal raíz:

```bash
# 1. Ejecutar los tests automáticos utilizando el contexto de ruta del directorio actual
python -m pytest -v

# 2. Ejecutar el pipeline completo de inicio a fin
python main.py

# 3. Prueba de Idempotencia (Córrelo por segunda vez inmediata)
python main.py
```

Nota técnica: Se utiliza `python -m pytest -v` en lugar de `pytest` directo para forzar al intérprete a incluir el directorio raíz actual dentro del mapa de búsqueda de Python (`sys.path`), evitando problemas de importación con el módulo `src`.

Al correrlo por segunda vez, notarás que el programa detecta el reporte existente y finaliza de forma segura sin volver a gastar recursos de cómputo innecesariamente.

> **Nota de entrega:** el proyecto se entrega con la carpeta `output/` vacía a propósito. La **primera** ejecución de `python main.py` genera el reporte; la **segunda** demuestra la idempotencia. La carpeta se crea automáticamente si no existe.

## 🧪 Pruebas Unitarias Aprobadas (Pytest Output)

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: ...\pipeline-analisis-pagos
collected 5 items

tests/test_pipeline.py::test_generar_analisis_pagos_agrega_y_calcula_participacion PASSED [ 20%]
tests/test_transform.py::test_aislamiento_datos_sucios PASSED            [ 40%]
tests/test_transform.py::test_filtrado_ordenes_canceladas PASSED         [ 60%]
tests/test_transform.py::test_comportamiento_tipos_y_columnas PASSED     [ 80%]
tests/test_transform.py::test_contratos_rechazan_datos_invalidos PASSED  [100%]

============================== 5 passed in 1.12s ==============================
```
