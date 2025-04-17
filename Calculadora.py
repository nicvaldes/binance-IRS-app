import streamlit as st
import requests
import pandas as pd

# Obtener promedio de los 10 mejores precios P2P de USDT a CLP
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
    return sum(precios) / len(precios) if precios else 0

# Función de cálculo principal
def calcular_metricas(
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

    # Tabla 1
    tabla1 = pd.DataFrame({
        'Parámetro': [
            'Precio promedio USDT/CLP (P2P)',
            'Monto a cambiar (USD)',
            'Monto que recibe el cliente (CLP)'
        ],
        'Valor': [
            round(tipo_cambio_usdt_clp, 2),
            round(monto_usd, 2),
            round(pago_cliente_deseado, 2)
        ]
    })

    # Tabla 2
    tabla2 = pd.DataFrame({
        'Parámetro': [
            'Pérdida del cliente (%)',
            'Comisión total por servicio (%)',
            'Ganancia total (CLP)',
            'Margen utilidad (%)'
        ],
        'Valor': [
            round(porcentaje_perdida_cliente_objetivo * 100, 2),
            round(porcentaje_perdida, 2),  # ahora en %
            round(ganancia_total, 2),
            round(margen_requerido * 100, 2)
        ]
    })

    return tabla1, tabla2

# Streamlit App
st.set_page_config(page_title="Calculadora de Margen USDT", layout="centered")
st.title("📊 Calculadora de Margen USDT - Binance P2P")

st.markdown("Calcula cuánto recibirá el cliente y cuánto ganas tú al vender USDT por Binance P2P.")

# Inputs
monto_usd_input = st.number_input("Monto a recibir en USD:", min_value=1.0, value=100.0, step=10.0)
st.caption("Se considera una comisión del 5.49% + 2 USDT de envío.")

# Obtener tipo de cambio actual
precio_p2p_promedio = obtener_precio_promedio_p2p_usdt_clp()

# Calcular tablas
tabla_1, tabla_2 = calcular_metricas(
    monto_usd=monto_usd_input,
    tipo_cambio_usdt_clp=precio_p2p_promedio
)

# Mostrar tablas
st.subheader("📌 Resumen Transacción")
st.dataframe(tabla_1.set_index('Parámetro'), use_container_width=True)

st.subheader("📈 Detalles Financieros")
st.dataframe(tabla_2.set_index('Parámetro'), use_container_width=True)
