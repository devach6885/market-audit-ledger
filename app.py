import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Audit Ledger Hub", layout="wide")
st.title("📉 Strategic Reconciliation & Performance Audit Ledger")

DATA_FILE = "historical_ledger.csv"

if os.path.exists(DATA_FILE):
    try:
        df_ledger = pd.read_csv(DATA_FILE)
        correct_count = (df_ledger['Predict_Correct'] == 'Yes').sum()
        total_count = len(df_ledger)
        accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0.0
        
        st.sidebar.metric(label="🎯 10:00 AM Forecast Accuracy", value=f"{accuracy:.1f}%")
        st.sidebar.caption(f"Total Reviewed Cycles: {total_count} trades")
        
        st.subheader("📋 TABLE 1: THE 10 OFFICIAL 10:00 AM FORECAST TRACKS")
        st.dataframe(df_ledger, use_container_width=True)
    except Exception as e:
        st.error(f"Error accessing history blocks: {str(e)}")
else:
    st.info("💡 Awaiting Initial Evaluation Sync...")
