import streamlit as st
import requests
import pandas as pd

# Obtener el promedio de los 10 mejores precios de USDT en CLP
def obtener_precio_promedio_p2p_usdt_clp():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    payload = {
        "asset": "USDT",
        "fiat": "CLP",
        "tradeType": "SELL",
        "page": 1,
        "rows": 10,
        "payTypes": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    precios = [float(item['adv']['price']) for item in data['data']]
    promedio = sum(precios) / len(precios) if precios else 0
    return promedio

# Lógica principal de cálculo
def calcular_margen_para_perdida_objetivo(
    monto_usd,
    comision_porcentual=0.0549,
    tarifa_binance_usdt=2,
    tipo_cambio_usdt_clp=900,
    porcentaje_perdida_cliente_objetivo=0.15
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
            'USD a CLP (Promedio 10 mejores)',
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

    return resultados

# Streamlit App
st.set_page_config(page_title="Calculadora Margen USDT", layout="centered")
st.title("📊 Calculadora de Margen USDT - Binance P2P")

st.markdown("Esta app calcula el margen necesario para asegurar una pérdida controlada del cliente al vender USDT vía Binance.")

# Inputs
monto_usd_input = st.number_input("Monto en USD a recibir (cliente):", min_value=1.0, value=100.0, step=10.0)
st.caption("La comisión fija por servicio es del 5.49% + 2 USDT de tarifa por Binance.")

# Obtener tipo de cambio promedio
precio_p2p_promedio = obtener_precio_promedio_p2p_usdt_clp()

# Calcular resultados
df_resultado = calcular_margen_para_perdida_objetivo(
    monto_usd=monto_usd_input,
    tipo_cambio_usdt_clp=precio_p2p_promedio
)

# Mostrar resultados
st.dataframe(df_resultado.set_index('Parámetro'), use_container_width=True)
