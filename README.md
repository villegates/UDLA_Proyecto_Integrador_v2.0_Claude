# Proyecto Integrador DPL1046 — Análisis de Métodos de Pago (Olist)

**Diplomado en Ingeniería de Datos con Python · UDLA · 2026**
Equipo: **Pablo Villegas** y **Genesis**

Entrega completa del Proyecto Integrador (Examen): un **pipeline ETL 100% local en Python** que analiza los métodos de pago del ecommerce Olist (Brasil), más la presentación final y el material de apoyo.

## 📦 Contenido del repositorio

| Elemento | Descripción |
|---|---|
| [`pipeline-analisis-pagos/`](pipeline-analisis-pagos/) | El pipeline ETL: código, datos e **5 tests**. Ver su [`README.md`](pipeline-analisis-pagos/README.md) para instalar y correr. |
| [`Presentacion_Final.html`](Presentacion_Final.html) | Presentación final (17 slides). Abrir en el navegador y presionar **`F`** para pantalla completa. |
| [`GUION_PRESENTACION.md`](GUION_PRESENTACION.md) | Guion detallado de 15 min (reparto de tiempos + preparación de preguntas). |
| [`GUION_RESUMEN.md`](GUION_RESUMEN.md) | Guion express de 1 página (para tener al lado al presentar). |
| [`MEMORIA_SESION.md`](MEMORIA_SESION.md) | Bitácora técnica del desarrollo (diagnóstico, arreglos, decisiones). |

## 🚀 Cómo correr el pipeline

```bash
cd pipeline-analisis-pagos

# 1. Entorno (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Tests (5 en verde)
python -m pytest -v

# 3. Pipeline completo (genera output/reporte_metodos_pago.csv + reporte en consola)
python main.py
```

> En Linux/Mac, activar el entorno con `source .venv/bin/activate`.

## 📊 Qué hace
Integra 3 tablas de Olist (pagos, órdenes y clientes), valida la calidad con **contratos de datos**, limpia y transforma con **pandas**, y genera un **reporte ejecutivo** del comportamiento de los métodos de pago a nivel nacional y por estado.

**Hallazgo principal:** `credit_card` concentra el **73,97%** de las transacciones con un promedio de **3,5 cuotas**.

---
*Desarrollado con asistencia de IA (Claude) como copiloto de código, según lo permitido por el curso. El equipo entiende y puede explicar cada parte del pipeline.*
