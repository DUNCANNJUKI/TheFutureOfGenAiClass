import streamlit as st
import requests

st.title("NewSystem — Starter UI")

if st.button("Check backend health"):
    try:
        r = requests.get("http://127.0.0.1:8001/health", timeout=3)
        st.success(f"Backend responded: {r.json()}")
    except Exception as e:
        st.error(f"Backend not reachable: {e}")

st.write("This is a minimal Streamlit starter app.")
