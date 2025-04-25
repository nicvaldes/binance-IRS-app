import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora TUCUPOENDOLAR.COM", layout="centered")

st.title("💸 Calculadora de Conversión USD a CLP")
st.markdown("""
Simula la conversión de USD a CLP para que el cliente reciba el 85% del monto solicitado convertido al valor del dólar del minuto.
""")

# Entradas del usuario
monto_usd = st.number_input("Monto en USD a transformar", min_value=1.0, value=100.0, step=1.0)
tipo_cambio_usdt_clp = st.number_input("Valor actual del dólar (USDT a CLP)", min_value=500.0, value=940.0, step=1.0)

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
    # Comisiones
    comision_aplicada = monto_usd * comision_porcentual
    perdida_total_usd = comision_aplicada + tarifa_binance_usdt

    # USDT neto recibido en Binance
    monto_neto_usdt = monto_usd - perdida_total_usd
    monto_clp_obtenido = monto_neto_usdt * tipo_cambio_usdt_clp

    # Pago al cliente: 85%
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

    # Tabla 1 (vertical)
    tabla_1 = pd.DataFrame({
        'Parámetro': ['Monto a Solicitar USD', 'USDT/CLP', 'Monto a Recibir (CLP)'],
        'Valor': [resultado['monto_usd'], resultado['tipo_cambio_usdt_clp'], resultado['pago_cliente_deseado']]
    })

    # Tabla 2 (vertical)
    tabla_2 = pd.DataFrame({
        'Parámetro': ['Monto USD', 'Pago al Cliente (CLP)', 'Ganancia Total (CLP)', 'Margen Utilidad (%)'],
        'Valor': [
            resultado['monto_usd'],
            resultado['pago_cliente_deseado'],
            resultado['ganancia_total'],
            resultado['margen_requerido']
        ]
    })

    st.subheader("📋 Tabla 1: Conversión básica")
    st.dataframe(tabla_1, use_container_width=True)

    st.subheader("📈 Tabla 2: Resultados de negocio")
    st.dataframe(tabla_2, use_container_width=True)

