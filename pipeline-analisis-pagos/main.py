import sys
from pathlib import Path
from loguru import logger
import yaml

# --- Configuración estricta de rutas relativas (Portabilidad entre equipos) ---
BASE = Path(__file__).resolve().parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

# Importación modular de las capas del pipeline
from src.extract import cargar_datos_pagos
from src.transform import limpiar_y_validar_datos
from src.pipeline import generar_analisis_pagos, responder_preguntas_negocio


def configurar_logs():
    """Configura Loguru con un formato limpio y profesional."""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )


def cargar_configuracion() -> dict:
    """Lee de forma segura el archivo de configuración externo yaml."""
    ruta_config = BASE / "config.yaml"
    try:
        with open(ruta_config, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        # Captura específica de fallos de sintaxis en la configuración (Clase 3 y 6)
        logger.critical(f"🚨 Error crítico de formato en el archivo config.yaml: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logger.critical(f"🚨 Archivo config.yaml ausente en la raíz del proyecto.")
        sys.exit(1)


def ejecutar_pipeline():
    """Orquestador Principal del Pipeline ETL sin bloques de auditoría."""
    config = cargar_configuracion()
    
    # --- Control de Idempotencia ---
    ruta_salida = BASE / config["rutas"]["salida_reporte"]
    if ruta_salida.exists():
        logger.warning(f"⚠️ REGLA DE IDEMPOTENCIA DETECTADA:")
        logger.warning(f"   ↳ El reporte ejecutivo '{ruta_salida.name}' ya existe en almacenamiento.")
        logger.success("✅ El sistema detiene la ejecución de forma segura para no malgastar cómputo.\n")
        return

    # 1. CAPA DE EXTRACCIÓN (Ingesta resiliente externalizada)
    df_pagos, df_ordenes, df_clientes = cargar_datos_pagos(config, BASE)
    
    # 2. CAPA DE TRANSFORMACIÓN (Filtros y Contratos de Calidad)
    df_p_limpio, df_o_limpio = limpiar_y_validar_datos(df_pagos, df_ordenes)
    
    # 3. CAPA DE CARGA Y ANÁLISIS (Parámetros y contratos de firma limpios)
    reporte_final, df_completo = generar_analisis_pagos(df_p_limpio, df_o_limpio, df_clientes)
    
    # Guardamos el archivo físico CSV generado
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    reporte_final.to_csv(ruta_salida, index=False, encoding="utf-8")
    logger.success(f"💾 Reporte analítico guardado exitosamente en: {config['rutas']['salida_reporte']}")
    
    # --- Respuestas de Negocio automáticas impresas en consola ---
    responder_preguntas_negocio(reporte_final, df_completo)


if __name__ == "__main__":
    configurar_logs()
    logger.info("================ PIPELINE OLIST AUTOMATIZADO ================")
    try:
        ejecutar_pipeline()
    except Exception as e:
        # El except genérico se deja exclusivamente en el punto de entrada global como red de seguridad
        logger.critical(f"🚨 El pipeline colapsó debido a un fallo global inesperado: {e}")
        sys.exit(1)