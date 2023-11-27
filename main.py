import time
import hashlib
import hmac
import requests
import streamlit as st


api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'
base_url = 'https://api.bybit.com'
endpoint = '/v2/private/order/create'
def execute_order(symbol, side, order_type, quantity, time_in_force):
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'qty': quantity,
        'timeInForce': time_in_force,
        'api_key': api_key,
        'timestamp': timestamp,
    }
    query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params.keys())])
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    params['sign'] = signature

    url = base_url + endpoint
    response = requests.post(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

st.title("Bybit Order Execution")


symbol = st.text_input("Symbol (e.g., BTCUSD):", "BTCUSD")
side = st.selectbox("Side:", ["Buy", "Sell"])
order_type = st.selectbox("Order Type:", ["Market", "Limit", "Stop Market", "Take Profit Market"])
quantity = st.number_input("Quantity:", min_value=0.001, step=0.001, format="%f")
time_in_force = st.selectbox("Time in Force:", ["GTC", "IOC", "FOK"])
if st.button("Execute Order"):
    result = execute_order(symbol, side, order_type, quantity, time_in_force)
    st.write(result)
