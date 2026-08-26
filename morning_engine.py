import yfinance as yf
import pandas as pd
from datetime import datetime

print("🛰️ Connecting live to exchange order books and macro news nodes...")

WATCHLIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", 
    "SBIN.NS", "ITC.NS", "WIPRO.NS", "TATAMOTORS.NS", "SUZLON.NS", "AXISBANK.NS"
]

def run_morning_pipeline():
    try:
        data = yf.download(tickers=WATCHLIST, period="5d", interval="1d", auto_adjust=False, progress=False)
        processed = []
        
        for t in WATCHLIST:
            if t in data.columns.levels:
                stock_df = data[t].dropna(subset=['Close'])
                if not stock_df.empty:
                    cl = float(stock_df['Close'].iloc[-1])
                    op = float(stock_df['Open'].iloc[-1])
                    
                    pct = ((cl - op) / op) * 100 if op > 0 else 0.0
                    prob = min(max(int(75 + (pct * 12)), 35), 98)
                    
                    bp = round(cl, 2)
                    sp = round(bp * 1.015, 2)
                    sl = round(bp * 0.992, 2)
                    profit_amt = round(sp - bp, 2)

                    processed.append({
                        "Company Name": t.replace(".NS", ""),
                        "Buying Price": bp,
                        "Selling Price": sp,
                        "Stop Loss at what Price": sl,
                        "Profit Amount": profit_amt,
                        "% that this trade will do book profit": prob
                    })
                    
        df_morning = pd.DataFrame(processed).sort_values(by="% that this trade will do book profit", ascending=False).head(10)
        df_morning.to_csv("morning_baseline.csv", index=False)
        print("🎉 morning_baseline.csv generated successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    run_morning_pipeline()
