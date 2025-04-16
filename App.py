import streamlit as st
import requests

st.set_page_config(page_title="Top compradores USDT", layout="centered")
st.title("🔍 Mejores compradores de USDT en Binance P2P (CLP)")

# Campo para ingresar el monto de USDT a vender
monto_usdt = st.number_input("💵 Ingrese el monto de USDT que desea vender:", min_value=0.0, step=0.01)

if st.button("Buscar compradores"):
    if monto_usdt <= 0:
        st.warning("Por favor, ingrese un monto válido de USDT.")
    else:
        with st.spinner("Consultando Binance P2P..."):
            url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
            payload = {
                "asset": "USDT",
                "fiat": "CLP",
                "tradeType": "BUY",
                "page": 1,
                "rows": 5,
                "payTypes": [],
                "proMerchantAds": False,
                "shieldMerchantAds": False
            }
            headers = {
                "Content-Type": "application/json"
            }

            try:
                response = requests.post(url, json=payload, headers=headers)
                data = response.json()

                if not data['data']:
                    st.warning("No se encontraron compradores activos.")
                else:
                    for i, anuncio in enumerate(data['data'], start=1):
                        precio = float(anuncio['adv']['price'])
                        comprador = anuncio['advertiser']['nickName']
                        advertiser_id = anuncio['advertiser']['userNo']
                        link = f"https://p2p.binance.com/es/advertiserDetail?advertiserNo={advertiser_id}"
                        trade_count = anuncio['advertiser'].get('tradeCount', 'No disponible')
                        completion_rate = anuncio['advertiser'].get('completionRate', 'No disponible')
                        avg_release_time = anuncio['advertiser'].get('avgReleaseTime', 'No disponible')

                        monto_total = precio * monto_usdt

                        st.markdown(f"""
                        ### 🥇 #{i} - {comprador}
                        - 💰 **Precio:** {precio} CLP
                        - 📈 **Operaciones completadas:** {trade_count}
                        - ✅ **Tasa de completitud:** {completion_rate}%
                        - ⏱️ **Tiempo promedio de liberación:** {avg_release_time} minutos
                        - 💸 **Monto total a recibir:** {monto_total:,.2f} CLP
                        - 🔗 [Ver anuncio]({link})
                        """)
            except Exception as e:
                st.error(f"Error al consultar Binance: {e}")
