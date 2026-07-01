import pandas as pd
from src.pipeline import generar_analisis_pagos


def test_generar_analisis_pagos_agrega_y_calcula_participacion():
    """
    Test 5: la capa de análisis une las 3 tablas y agrega por estado × método.
    Verifica el conteo, el ticket promedio y que la participación por estado sume 100%.
    """
    df_pagos = pd.DataFrame({
        'order_id': ['o1', 'o2', 'o3'],
        'payment_value': [100.0, 200.0, 50.0],
        'payment_installments': [1, 2, 1],
        'payment_type': ['credit_card', 'credit_card', 'boleto'],
    })
    df_ordenes = pd.DataFrame({
        'order_id': ['o1', 'o2', 'o3'],
        'customer_id': ['c1', 'c2', 'c3'],
        'order_status': ['delivered', 'delivered', 'delivered'],
    })
    df_clientes = pd.DataFrame({
        'customer_id': ['c1', 'c2', 'c3'],
        'customer_state': ['SP', 'SP', 'SP'],
    })

    reporte, df_completo = generar_analisis_pagos(df_pagos, df_ordenes, df_clientes)

    # 1. Estructura esperada del reporte de salida
    for col in ['customer_state', 'payment_type', 'pedidos',
                'ticket_promedio', 'cuotas_promedio', 'participacion_%']:
        assert col in reporte.columns, f"Falta la columna '{col}' en el reporte"

    # 2. En SP, credit_card agrupa 2 pedidos con ticket promedio (100+200)/2 = 150
    fila_credito = reporte[
        (reporte['customer_state'] == 'SP') & (reporte['payment_type'] == 'credit_card')
    ].iloc[0]
    assert fila_credito['pedidos'] == 2
    assert fila_credito['ticket_promedio'] == 150.0

    # 3. La participación porcentual dentro de un estado debe sumar 100%
    total_pct_sp = reporte[reporte['customer_state'] == 'SP']['participacion_%'].sum()
    assert round(total_pct_sp, 2) == 100.0
