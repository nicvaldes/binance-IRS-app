import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Conversión USD a CLP", layout="centered")

st.title("💸 Calculadora de Conversión USD a CLP")
st.markdown("""
Esta calculadora simula la conversión de USD a CLP considerando comisiones y que el cliente reciba el 85% del monto solicitado convertido al valor actual del dólar.
""")

# Entradas del usuario
monto_usd = st.number_input("Monto en USD a transformar", min_value=1.0, value=100.0, step=1.0)
tipo_cambio_usdt_clp = st.number_input("Valor actual del dólar (USDT a CLP)", min_value=500.0, value=940.0, step=1.0)

# Parámetros fijos
comision_porcentual = 0.0549
tarifa_binance_usdt = 2
porcentaje_pago_cliente = 0.85  # Cliente recibe el 85% del monto solicitado

def calcular_conversion(
    monto_usd,
    comision_porcentual,
    tarifa_binance_usdt,
    tipo_cambio_usdt_clp,
    porcentaje_pago_cliente
):
    # Comisiones
    comision_aplicada = monto_usd * comision_porcentual
    perdida_total_usd = comision_aplicada + tarifa_binance_usdt

    # USD netos luego de comisiones
    monto_neto_usdt = monto_usd - perdida_total_usd
    monto_clp_obtenido = monto_neto_usdt * tipo_cambio_usdt_clp

    # Pago al cliente: 85% del monto original
    pago_cliente_deseado = (monto_usd * porcentaje_pago_cliente) * tipo_cambio_usdt_clp

    # Valor ideal sin comisiones
    valor_referencia_clp = monto_usd * tipo_cambio_usdt_clp

    # Recalcular métricas
    ganancia_total = monto_clp_obtenido - pago_cliente_deseado
    margen_requerido = ganancia_total / monto_clp_obtenido
    porcentaje_perdida_cliente_objetivo = (1 - (pago_cliente_deseado / valor_referencia_clp)) * 100

    resultados = pd.DataFrame({
        'Parámetro': [
            'USD a CLP',
            'Monto Solicitado (USD)',
            'Comisión Aplicada (USD) (OneInfinite)',
            'Tarifa Envío Binance (USDT)',
            'USD Netos Tras Comisiones',
            'CLP Obtenido Final',
            'Pago al Cliente (85%) en CLP',
            'Valor Ideal sin Comisiones (CLP)',
            'Ganancia Total (CLP)',
            'Margen de Utilidad (%)',
            'Pérdida Total del Cliente (%)'
        ],
        'Valor': [
            round(tipo_cambio_usdt_clp, 2),
            round(monto_usd, 2),
            round(comision_aplicada, 2),
            round(tarifa_binance_usdt, 2),
            round(monto_neto_usdt, 2),
            round(monto_clp_obtenido, 2),
            round(pago_cliente_deseado, 2),
            round(valor_referencia_clp, 2),
            round(ganancia_total, 2),
            round(margen_requerido * 100, 2),
            round(porcentaje_perdida_cliente_objetivo, 2)
        ]
    })

    return resultados.set_index('Parámetro')

# Mostrar resultados
if st.button("Calcular"):
    df_resultado = calcular_conversion(
        monto_usd,
        comision_porcentual,
        tarifa_binance_usdt,
        tipo_cambio_usdt_clp,
        porcentaje_pago_cliente
    )
    st.subheader("📊 Resultados de la Conversión")
    st.dataframe(df_resultado, use_container_width=True)
