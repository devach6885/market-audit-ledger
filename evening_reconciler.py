import yfinance as yf
import pandas as pd
import os
from datetime import datetime

print("📥 Pulling today's final exchange candlestick reality profiles...")

WATCHLIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", 
    "SBIN.NS", "ITC.NS", "WIPRO.NS", "TATAMOTORS.NS", "SUZLON.NS", "AXISBANK.NS"
]

def run_evening_audit():
    today_str = datetime.today().strftime("%Y-%m-%d")
    
    if not os.path.exists("morning_baseline.csv"):
        print("⚠️ Warning: No 10:00 AM forecast targets were locked for today session cycle.")
        return
        
    df_morning = pd.read_csv("morning_baseline.csv")
    
    # Download today's definitive intra-day boundary candles
    data = yf.download(tickers=WATCHLIST, period="1d", interval="1d", auto_adjust=False, progress=False)
    
    reconciled_rows = []
    
    for idx, row in df_morning.iterrows():
        ticker_symbol = row['Company Name'] + ".NS"
        
        if ticker_symbol in data.columns.levels:
            hist = data[ticker_symbol].dropna(subset=['Close'])
            if not hist.empty:
                # Extract extreme session limits achieved during active hours
                actual_high = float(hist['High'].iloc[-1])
                actual_low = float(hist['Low'].iloc[-1])
                
                target_selling_price = float(row['Selling Price'])
                stop_loss_price = float(row['Stop Loss at what Price'])
                
                # Definitive evaluation criteria matching your Yes/No spreadsheet logic columns
                if actual_high >= target_selling_price:
                    predicted_correctly = "Yes"
                else:
                    predicted_correctly = "No"
                    
                reconciled_rows.append({
                    "Date": today_str,
                    "Company Name": row['Company Name'],
                    "Buying Price": row['Buying Price'],
                    "Selling Price": row['Selling Price'],
                    "Stop at what Price": row['Stop Loss at what Price'],
                    "Profit Amount": row['Profit Amount'],
                    "% that this trade will do this profit": f"{row['% that this trade will do book profit']}%",
                    "Did the system predict the profit correctly Yes/No": predicted_correctly
                })
                
    if reconciled_rows:
        new_records_df = pd.DataFrame(reconciled_rows)
        ledger_file = "historical_ledger.csv"
        
        if os.path.exists(ledger_file) and os.stat(ledger_file).st_size > 50:
            existing_ledger_df = pd.read_csv(ledger_file)
            # Prevent pushing duplicate rows for the same date session
            existing_ledger_df = existing_ledger_df[existing_ledger_df['Date'] != today_str]
            final_ledger_df = pd.concat([existing_ledger_df, new_records_df], ignore_index=True)
        else:
            final_ledger_df = new_records_df
            
        final_ledger_df.to_csv(ledger_file, index=False)
        print(f"🎉 Successfully reconciled trade entries appended to historical ledger database records!")

if __name__ == '__main__':
    run_evening_audit()
