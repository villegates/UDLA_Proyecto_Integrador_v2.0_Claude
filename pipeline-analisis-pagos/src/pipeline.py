from pathlib import Path
import pandas as pd
from loguru import logger

BASE_PIPELINE = Path(__file__).resolve().parent.parent / "output"

def generar_analisis_pagos(
    df_payments: pd.DataFrame, 
    df_orders: pd.DataFrame, 
    df_customers: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Une las fuentes de datos de Olist y genera las métricas de negocio agrupadas.
    Retorna (reporte_agrupado, df_completo) eliminando por completo las variables globales.
    """
    logger.info("📊 Iniciando agregaciones lógicas y análisis de negocio...")
    try:
        df_unido = pd.merge(df_payments, df_orders, on="order_id", how="inner")
        df_completo = pd.merge(df_unido, df_customers, on="customer_id", how="inner")

        # Agrupación por Estado y Método de Pago (para el CSV de salida)
        reporte = df_completo.groupby(["customer_state", "payment_type"]).agg(
            pedidos=("order_id", "count"),
            ticket_promedio=("payment_value", "mean"),
            cuotas_promedio=("payment_installments", "mean")
        ).reset_index()

        reporte["ticket_promedio"] = reporte["ticket_promedio"].round(2)
        reporte["cuotas_promedio"] = reporte["cuotas_promedio"].round(2)

        # Cálculo de participación porcentual interna (vectorización con Pandas)
        total_por_estado = reporte.groupby("customer_state")["pedidos"].transform("sum")
        reporte["participacion_%"] = ((reporte["pedidos"] / total_por_estado) * 100).round(2)

        # Ordenar para una visualización más lógica
        reporte = reporte.sort_values(by=["pedidos"], ascending=False).reset_index(drop=True)

        logger.info("✅ Procesamiento analítico y uniones de Pandas completados.")
        return reporte, df_completo

    except KeyError as e:
        # Error específico: Alguna columna del merge o groupby no existe en las fuentes (Clase 3)
        logger.error(f"❌ Error de Estructura: No se encontró una columna clave en las tablas: {e}")
        raise e
    except ValueError as e:
        # Error específico: Incompatibilidad al calcular tipos o agregaciones (Clase 3)
        logger.error(f"❌ Error de Operación: Conflicto en el procesamiento de tipos de datos: {e}")
        raise e


def responder_preguntas_negocio(df_reporte: pd.DataFrame, df_completo_geo: pd.DataFrame) -> None:
    """
    Imprime las respuestas ejecutivas en la consola usando parámetros limpios aislados.
    """
    logger.info("📋 Generando visualización del reporte ejecutivo en consola...")
    
    print("\n" + "="*85)
    print(" 💼 REPORTE EXECUTIVE ANÁLISIS MÉTODOS DE PAGO - OLIST ECOMMERCE ")
    print("="*85)

    # --- TABLA 1: PERSPECTIVA NACIONAL ---
    print("\n📊 1. RESUMEN MÉTODOS DE PAGO (PERSPECTIVA NACIONAL)")
    print("-"*85)
    df_nacional = df_completo_geo.groupby("payment_type").agg(
        pedidos=("order_id", "count"),
        ticket_promedio=("payment_value", "mean"),
        cuotas_promedio=("payment_installments", "mean")
    ).sort_values(by="pedidos", ascending=False)
    
    df_nacional["ticket_promedio"] = df_nacional["ticket_promedio"].round(2)
    df_nacional["cuotas_promedio"] = df_nacional["cuotas_promedio"].round(2)
    df_nacional["participacion_%"] = ((df_nacional["pedidos"] / df_nacional["pedidos"].sum()) * 100).round(2)
    
    df_nacional.index.name = None
    df_nacional = df_nacional.rename_axis("payment_type", axis=1)
    print(df_nacional)
    print("-"*85)

    # --- TABLA 2: MATRIZ GEOGRÁFICA (27 ESTADOS) ---
    ct = pd.crosstab(df_completo_geo['customer_state'], df_completo_geo['payment_type'], normalize='index') * 100
    ct = ct.round(2)
    
    columnas_ordenadas = [c for c in df_nacional.index if c in ct.columns]
    ct = ct[columnas_ordenadas]
    df_tasas_completo = ct.sort_values(by="credit_card", ascending=False).reset_index()

    print("\n🌎 2. MATRIZ DE PARTICIPACIÓN REGIONAL COMPLETA (ORDENADA POR % DE CRÉDITO)")
    print("-"*85)
    print(df_tasas_completo.to_string(index=False))
    print("-"*85)
    
    # --- RESPUESTAS DEL TEMPLATE EXIGIDO ---
    print("\n🔍 RESPUESTAS ESTRATÉGICAS DE NEGOCIO (HALLAZGOS)")
    print("="*85)
    
    metodo_lider = df_nacional.index[0]
    pct_lider = df_nacional.iloc[0]["participacion_%"]
    print(f"📌 Hallazgo 1: ¿Cuál es el método de pago líder a nivel nacional?")
    print(f"   ↳ Es '{metodo_lider}' concentrando de manera sólida el {pct_lider}% de las transacciones.")
    print(f"     Impacto: Es el pilar transaccional del ecommerce (verificable en Tabla 1).")
    
    cuotas_p = df_nacional.loc["credit_card", "cuotas_promedio"] if "credit_card" in df_nacional.index else 0
    print(f"\n📌 Hallazgo 2: ¿Cómo se comportan las compras financiadas en el canal principal?")
    print(f"   ↳ Las compras con tarjeta de crédito se difieren a un promedio nacional de {cuotas_p} cuotas.")
    print(f"     Impacto: Indica una dependencia crítica del financiamiento a plazos para sostener los tickets altos.")

    # Estado con MAYOR preferencia por crédito (máximo real de la columna)
    fila_top_credito = df_tasas_completo.loc[df_tasas_completo['credit_card'].idxmax()]
    top_credit_state = fila_top_credito['customer_state']
    pct_credit_val = fila_top_credito['credit_card']

    # Estado con MAYOR preferencia por boleto/efectivo (máximo real, NO el inverso del crédito)
    fila_top_boleto = df_tasas_completo.loc[df_tasas_completo['boleto'].idxmax()]
    top_boleto_state = fila_top_boleto['customer_state']
    pct_boleto_val = fila_top_boleto['boleto']
    
    print(f"\n📌 Hallazgo 3: ¿Cómo influye la geografía en la preferencia interna de pago?")
    print(f"   ↳ El estado con mayor preferencia por crédito es '{top_credit_state}' ({pct_credit_val}% elige tarjeta).")
    print(f"   ↳ El estado con mayor preferencia por boleto (pago en efectivo) es '{top_boleto_state}' ({pct_boleto_val}% elige 'boleto').")
    print(f"     Impacto: Revela brechas de bancarización regionales en el uso de crédito vs. efectivo.")
        
    print("="*85 + "\n")
    logger.info("🚀 Reporte ejecutivo desplegado correctamente en pantalla.")