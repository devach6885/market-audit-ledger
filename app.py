import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import os
from datetime import datetime

st.set_page_config(page_title="Exchange-Wide 3-State AI Engine", layout="wide")

st.sidebar.title("🎮 Engine Workspace")
page = st.sidebar.radio("Navigate Daily Sequence", [
    "🌅 1. Morning Baseline (10:00 AM)", 
    "⚡ 2. Real-Time Tracking Canvas", 
    "📉 3. EOD Audit & Discovery Ledger"
])

EXCHANGE_UNIVERSE = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS",
    "ITC.NS", "WIPRO.NS", "TATAMOTORS.NS", "SUZLON.NS", "AXISBANK.NS", "COALINDIA.NS", "SUNPHARMA.NS",
    "NTPC.NS", "ONGC.NS", "POWERGRID.NS", "ADANIENT.NS", "ZOMATO.NS", "JIOFIN.NS", "IRFC.NS"
]

def execute_exchange_scan():
    try:
        data = yf.download(tickers=EXCHANGE_UNIVERSE, period="1d", group_by="ticker", progress=False)
        processed = []
        for t in EXCHANGE_UNIVERSE:
            hist = data[t] if t in data.columns.levels else data
            if not hist.empty:
                op, cl = float(hist['Open'].iloc[-1]), float(hist['Close'].iloc[-1])
                hi, lo = float(hist['High'].iloc[-1]), float(hist['Low'].iloc[-1])
                pct = ((cl - op) / op) * 100
                prob = min(max(int(50 + (pct * 15)), 30), 98)
                processed.append({
                    "Company_Name": t.replace(".NS", ""), "Ticker": t.replace(".NS", ""),
                    "Current_Price": round(cl, 2), "Intraday_Momentum": round(pct, 2),
                    "AI_Probability": prob, "High": hi, "Low": lo,
                    "Last_Updated": datetime.now().strftime("%H:%M:%S")
                })
        return pd.DataFrame(processed).sort_values(by="AI_Probability", ascending=False).head(10)
    except Exception as e:
        st.error(f"Scan Error: {str(e)}")
        return pd.DataFrame()

# =====================================================================
# STATE 1: MORNING BASELINE (FROZEN DATA SHAPES)
# =====================================================================
if page == "🌅 1. Morning Baseline (10:00 AM)":
    st.title("🌅 Morning Baseline Execution Panel")
    st.write("Establishes and freezes your official morning prediction matrix at market open.")
    
    if st.button("🏁 Lock Morning 10:00 AM Baseline Run"):
        with st.spinner("Locking morning exchange-wide momentum baseline profiles..."):
            df_morning = execute_exchange_scan()
            if not df_morning.empty:
                df_morning.to_csv("morning_baseline.csv", index=False)
                st.success("🎉 Morning Baseline matrix successfully generated and locked!")

    if os.path.exists("morning_baseline.csv"):
        df_display = pd.read_csv("morning_baseline.csv")
        st.subheader("📋 Official Frozen 10:00 AM Target Watchlist")
        for idx, row in df_display.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"### {row['Company_Name']}")
                    st.slider(f"Position size (INR)", 1000, 50000, 1000, step=1000, key=f"m_{row['Ticker']}")
                with c2: st.markdown(f"**Win Probability**\n### {row['AI_Probability']}%")
                with c3: st.metric("Baseline Entry Limit", f"₹ {row['Current_Price']:.2f}")
                with c4: st.markdown(f"**Safety Stop-Loss**\n<h4 style='color:#da3633;'>₹ {row['Current_Price']*0.992:.2f}</h4>", unsafe_allowed_html=True)
                st.markdown("---")

# =====================================================================
# STATE 2: REAL-TIME TRACKING CANVAS (DYNAMIC MID-DAY UPDATES)
# =====================================================================
elif page == "⚡ 2. Real-Time Tracking Canvas":
    st.title("⚡ Dynamic Intraday Re-Scan Canvas")
    st.write("Recalculates exchange trends and tracks real-time shifts as they develop during active hours.")
    
    if st.button("⚡ Force Live Real-Time Market Re-Scan"):
        with st.spinner("AI Engine downloading real-time chart candles..."):
            df_rt = execute_exchange_scan()
            if not df_rt.empty:
                df_rt.to_csv("realtime_shift.csv", index=False)
                st.success("🎉 Real-time intraday tracking matrix updated live!")

    if os.path.exists("realtime_shift.csv"):
        df_rt_display = pd.read_csv("realtime_shift.csv")
        st.subheader(f"📊 Active Intraday Lead Scans (Updated: {df_rt_display['Last_Updated'].iloc[0]})")
        for idx, row in df_rt_display.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"### {row['Company_Name']}")
                    st.slider(f"Position size (INR)", 1000, 50000, 1000, step=1000, key=f"rt_{row['Ticker']}")
                with c2: st.markdown(f"**Live Volatility Score**\n### {row['AI_Probability']}%")
                with c3: st.metric("Live Market Price", f"₹ {row['Current_Price']:.2f}", delta=f"{row['Intraday_Momentum']:.2f}%")
                with c4: st.markdown(f"**Dynamic Stop-Loss**\n<h4 style='color:#da3633;'>₹ {row['Current_Price']*0.992:.2f}</h4>", unsafe_allowed_html=True)
                st.markdown("---")

# =====================================================================
# STATE 3: EOD AUDIT & DISCOVERY LEDGER (CHRONOLOGICAL RECONCILIATION)
# =====================================================================
else:
    st.title("📉 Strategic Reconciliation & Performance Audit Ledger")
    st.write("Review your morning baseline predictions versus closing reality, and find the top 10 runners you missed.")
    
    if os.environ.get("EXECUTE_EOD_TRIGGER") == "TRUE":
        st.info("🔄 Processing evening reconciliation data sheet calculations...")

    if os.path.exists("historical_ledger.csv"):
        df_ledger = pd.read_csv("historical_ledger.csv")
        available_dates = sorted(df_ledger['Date'].unique(), reverse=True)
        selected_date = st.selectbox("📅 Select Session Audit Date:", available_dates)
        
        df_day = df_ledger[df_ledger['Date'] == selected_date]
        col_l, col_r = st.columns(2)
        
        with col_l:
            st.subheader("🎯 10:00 AM Baseline Performance Outcomes")
            df_wl = df_day[df_day['Type'] == 'Watchlist Audit']
            if not df_wl.empty:
                st.dataframe(df_wl[['Company_Name', 'Ticker', 'Buy_Price', 'Sell_Price', 'Predict_Correct', 'Loss_Or_Gain', 'Fail_Reason_Or_Performance']], use_container_width=True)
            else: st.info("No morning prediction data logs match this session date.")
                
        with col_r:
            st.subheader("🔍 Top 10 Missed Outperformers (Exchange Winners)")
            df_ms = df_day[df_day['Type'] == 'Missed Outperformer']
            if not df_ms.empty:
                st.dataframe(df_ms[['Company_Name', 'Ticker', 'Buy_Price', 'Fail_Reason_Or_Performance']], use_container_width=True)
            else: st.info("No market outperformer discovery metrics match this session date.")
    else:
        st.info("💡 Awaiting initial evening evaluation pipeline run to generate historical ledger records.")
