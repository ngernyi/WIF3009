import pandas as pd
import re

month_map = {
    "M01": "January", "M02": "February", "M03": "March", "M04": "April",
    "M05": "May", "M06": "June", "M07": "July", "M08": "August",
    "M09": "September", "M10": "October", "M11": "November", "M12": "December",
}

def rename_col(col):
    if col == "Partners":
        return col
    match = re.search(r'Balance in value in (\d{4})-(M\d{2})', col)
    if match:
        year = match.group(1)
        month_code = match.group(2)
        month_name = month_map.get(month_code, month_code)
        return f"{year} {month_name}"
    return col

def load_and_clean_china():
    df = pd.read_csv("https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_trade_balance_China.csv")
    df.columns = [rename_col(c) for c in df.columns]
    return df

def load_and_clean_us():
    df = pd.read_csv("https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_trade_balance_US.csv")
    df.columns = [rename_col(c) for c in df.columns]
    return df