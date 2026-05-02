import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TriGuard AI - Safe Mode", layout="wide")

st.title("🛡️ TriGuard AI - EMERGENCY SAFE MODE")
st.write("If you are seeing this, the environment is working, but the main dashboard has a library conflict.")

if os.path.exists("output.csv"):
    df = pd.read_csv("output.csv")
    st.success(f"✅ Data loaded successfully! Found {len(df)} tickets.")
    st.dataframe(df)
else:
    st.error("❌ output.csv not found. Please run 'python main.py' first.")

st.info("To fix the main dashboard, we may need to reinstall Plotly or Scikit-Learn.")
