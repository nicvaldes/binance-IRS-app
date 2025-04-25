import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Conversión USD a CLP", layout="centered")

st.title("💸 Calculadora de Conversión USD a CLP")
st.markdown("""
Esta calculadora te permite simular la conversión de USD a CLP considerando comisiones fijas y un porcentaje fijo de pérdida para el cliente.
""")

# Entradas del usuario
monto_usd = st.number_input("Monto Solictado (USD)", min_value=1.0, value=100.0, step=1.0)
tipo_cambio_usdt_clp = st.number_input("Valor actual del dólar", min_value=500.0, value=940.0, step=1.0)

# Parámetros fijos
comision_porcentual = 0.0549
tarifa_binance_usdt = 2
porcentaje_perdida_cliente_objetivo = 0.15

def calcular_margen_para_perdida_objetivo(
    monto_usd,
    comision_porcentual,
    tarifa_binance_usdt,
    tipo_cambio_usdt_clp,
    porcentaje_perdida_cliente_objetivo
):
    comision_aplicada = monto_usd * comision_porcentual
    perdida_total_usd = comision_aplicada + tarifa_binance_usdt
    porcentaje_perdida = (perdida_total_usd / monto_usd) * 100

    monto_neto_usdt = monto_usd - perdida_total_usd
    monto_clp_obtenido = monto_neto_usdt * tipo_cambio_usdt_clp
    valor_referencia_clp = monto_usd * tipo_cambio_usdt_clp
    pago_cliente_deseado = valor_referencia_clp * (1 - porcentaje_perdida_cliente_objetivo)
    margen_requerido = 1 - (pago_cliente_deseado / monto_clp_obtenido)
    ganancia_total = monto_clp_obtenido - pago_cliente_deseado

    resultados = pd.DataFrame({
        'Parámetro': [
            'USD a CLP',
            'Monto a Cobrar (USD)',
            'Comisión Aplicada (USD) (OneInfinite)',
            'Tarifa Envío Binance (USDT)',
            'Porcentaje de Pérdida Sobre Monto Original (%)',
            'Monto Neto en USDT (Binance)',
            'Monto CLP Obtenido',
            'Valor Referencia (sin comisiones)',
            'Pago Final del Cliente (CLP)',
            'Comisión Total por Servicio (%)',
            'Ganancia Total (CLP)',
            'Margen Utilidad (%)',
        ],
        'Valor': [
            round(tipo_cambio_usdt_clp, 2),
            round(monto_usd, 2),
            round(comision_aplicada, 2),
            round(tarifa_binance_usdt, 2),
            round(porcentaje_perdida, 2),
            round(monto_neto_usdt, 2),
            round(monto_clp_obtenido, 2),
            round(valor_referencia_clp, 2),
            round(pago_cliente_deseado, 2),
            round(porcentaje_perdida_cliente_objetivo * 100, 2),
            round(ganancia_total, 2),
            round(margen_requerido * 100, 2),
        ]
    })

    return resultados.set_index('Parámetro')

# Mostrar resultados al presionar botón
if st.button("Calcular"):
    df_resultado = calcular_margen_para_perdida_objetivo(
        monto_usd,
        comision_porcentual,
        tarifa_binance_usdt,
        tipo_cambio_usdt_clp,
        porcentaje_perdida_cliente_objetivo
    )
    st.subheader("📊 Resultados de la Conversión")
    st.dataframe(df_resultado, use_container_width=True)
