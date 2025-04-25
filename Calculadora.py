import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora TUCUPOENDOLAR.COM", layout="centered")

st.title("💸 Calculadora de Conversión USD a CLP")
st.markdown("""
Simula la conversión de USD a CLP para que el cliente reciba el 85% del monto solicitado convertido al valor del dólar del minuto
""")

# Entradas del usuario
monto_usd = st.number_input("Monto Solicitado en USD", min_value=1.0, value=100.0, step=1.0)
tipo_cambio_usdt_clp = st.number_input("USD a CLP", min_value=500.0, value=940.0, step=1.0)

# Parámetros fijos
comision_porcentual = 0.0549
tarifa_binance_usdt = 2
porcentaje_pago_cliente = 0.85

def calcular_conversion(
    monto_usd,
    comision_porcentual,
    tarifa_binance_usdt,
    tipo_cambio_usdt_clp,
    porcentaje_pago_cliente
):
    # Comisiones y pérdida
    comision_aplicada = monto_usd * comision_porcentual
    perdida_total_usd = comision_aplicada + tarifa_binance_usdt

    # Neto recibido en Binance (USDT)
    monto_neto_usdt = monto_usd - perdida_total_usd
    monto_clp_obtenido = monto_neto_usdt * tipo_cambio_usdt_clp

    # Pago al cliente (85%)
    pago_cliente_deseado = (monto_usd * porcentaje_pago_cliente) * tipo_cambio_usdt_clp

    # Métricas
    ganancia_total = monto_clp_obtenido - pago_cliente_deseado
    margen_requerido = ganancia_total / monto_clp_obtenido

    return {
        'monto_usd': round(monto_usd, 2),
        'tipo_cambio_usdt_clp': round(tipo_cambio_usdt_clp, 2),
        'pago_cliente_deseado': round(pago_cliente_deseado, 2),
        'ganancia_total': round(ganancia_total, 2),
        'margen_requerido': round(margen_requerido * 100, 2)
    }

# Mostrar resultados
if st.button("Calcular"):
    resultado = calcular_conversion(
        monto_usd,
        comision_porcentual,
        tarifa_binance_usdt,
        tipo_cambio_usdt_clp,
        porcentaje_pago_cliente
    )

    # Tabla 1
    tabla_1 = pd.DataFrame([{
        'Monto a Cambiar USD': resultado['monto_usd'],
        'USD/CLP': resultado['tipo_cambio_usdt_clp'],
        'Monto a Recibir CLP': resultado['pago_cliente_deseado']
    }])

    # Tabla 2
    tabla_2 = pd.DataFrame([{
        'Monto USD': resultado['monto_usd'],
        'Pago al Cliente CLP': resultado['pago_cliente_deseado'],
        'Ganancia Total CLP': resultado['ganancia_total'],
        'Margen Utilidad (%)': resultado['margen_requerido']
    }])

    st.subheader("📋 Tabla 1: Conversión básica")
    st.dataframe(tabla_1, use_container_width=True)

    st.subheader("📈 Tabla 2: Resultados de negocio")
    st.dataframe(tabla_2, use_container_width=True)

