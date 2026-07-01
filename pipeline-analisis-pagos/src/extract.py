import time
from pathlib import Path
import pandas as pd
from loguru import logger


def leer_csv_con_reintentos(
    ruta_archivo: Path,
    max_intentos: int = 3,
    espera_inicial: float = 0.5,
) -> pd.DataFrame:
    """
    Intenta leer un archivo aplicando Exponential Backoff.
    Simula fallos en los primeros intentos para demostrar robustez en consola.
    """
    for intento in range(1, max_intentos + 1):
        try:
            # ------------------------------------------------------------------
            # SIMULACIÓN DEL PROFESOR: Forzamos un error artificial si es el intento 1 o 2
            # Solo pasará con éxito cuando llegue al intento 3
            if intento < 3:
                raise RuntimeWarning("La fuente no respondió (simulado)")
            # ------------------------------------------------------------------

            # Intento real (se logra en el intento 3)
            df = pd.read_csv(ruta_archivo)
            logger.success(f"Fuente respondió en el intento {intento}")
            return df

        except FileNotFoundError as e:
            # Error específico y NO recuperable: el archivo simplemente no existe (Clase 3)
            logger.error(f"❌ Archivo no encontrado físicamente en el disco: {ruta_archivo}")
            raise e

        except pd.errors.ParserError as e:
            # Error específico: el CSV está roto o mal estructurado, no se arregla reintentando (Clase 3)
            logger.critical(f"❌ Error fatal de estructura: El archivo CSV está corrupto: {e}")
            raise e

        except RuntimeWarning as e:
            # Este es el fallo simulado de red del profesor que SÍ amerita reintento
            tiempo_espera = espera_inicial * (2 ** (intento - 1))
            logger.warning(f"Fallo de comunicación simulado ({e}). Reintento en {tiempo_espera}s")
            
            if intento < max_intentos:
                time.sleep(tiempo_espera)

    raise RuntimeError(f"No se pudo leer el archivo tras {max_intentos} intentos.")


def cargar_datos_pagos(config: dict, base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Orquesta la carga de las 3 tablas esenciales usando un bucle con control de flujo formal.
    """
    logger.info("📥 Iniciando proceso de extracción de datos (Ingesta)...")

    rutas_cfg = config["rutas"]
    parametros_cfg = config["parametros"]

    archivos_a_cargar = {
        "payments": base_dir / rutas_cfg["origen_payments"],
        "orders": base_dir / rutas_cfg["origen_orders"],
        "customers": base_dir / rutas_cfg["origen_customers"],
    }

    dataframes_cargados = {}

    for clave, ruta in archivos_a_cargar.items():
        try:
            logger.info(f"Intento 1 de leer la fuente... ({ruta.name})")
            df = leer_csv_con_reintentos(
                ruta,
                max_intentos=parametros_cfg["intentos_backoff"],
                espera_inicial=parametros_cfg["espera_inicial"],
            )
            dataframes_cargados[clave] = df

        except (RuntimeError, FileNotFoundError, pd.errors.ParserError) as error_fichero:
            # Captura únicamente los errores de lectura esperados tras los reintentos (Clase 3)
            logger.error(f"🚨 Error crítico al procesar el archivo '{ruta.name}': {error_fichero}")
            continue

    if len(dataframes_cargados) < len(archivos_a_cargar):
        raise RuntimeError("No se pudo completar el pipeline por falta de dependencias de datos.")

    logger.success(f"✅ Ingesta completada con éxito. Tablas listas para transformación.")

    return (
        dataframes_cargados["payments"],
        dataframes_cargados["orders"],
        dataframes_cargados["customers"],
    )