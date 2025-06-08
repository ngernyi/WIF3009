"""	
#Task 4: Correlation Analysis

#Data found (for US and China)
1. GDP Growth
- Indicator Name : GDP growth (annual %)
- Indicator Code : NY.GDP.MKTP.KD.ZG
2. Inflation Rate
- Indicator Name : Inflation, consumer prices (annual %)
- Indicator Code : FP.CPI.TOTL.ZG
3. Employment Rate
- Indicator Name : Employment to population ratio, 15+, total (%) (modeled ILO estimate)
- Indicator Code : SL.EMP.TOTL.SP.ZS
4. Stock Market
- Shanghai Shenzhen CSI 300
- Shanghai Composite
- Hang Seng Index
- S&P 500
- Dow Jones Industrial Average
- NASDAQ Composite
"""

import pandas as pd
import streamlit as st


def load_index_csv(filename, index_name):
    df = pd.read_csv(filename)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Price'] = df['Price'].str.replace(',', '').astype(float)
    df = df[['Date', 'Price']].rename(columns={'Price': index_name})
    df = df.set_index('Date').sort_index()
    return df

# === Load all stock indices ===
df_csi300     = load_index_csv('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/Shanghai%20Shenzhen%20CSI%20300%20Historical%20Data.csv', 'CSI 300')
df_shanghai   = load_index_csv('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/Shanghai%20Composite%20Historical%20Data.csv', 'Shanghai Composite')
df_hang_seng  = load_index_csv('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/Hang%20Seng%20Historical%20Data%20(1).csv', 'Hang Seng')
df_sp500      = load_index_csv('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/S%26P%20500%20Historical%20Data.csv', 'S&P 500')
df_dow_jones  = load_index_csv('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/Dow%20Jones%20Industrial%20Average%20Historical%20Data.csv', 'Dow Jones')
df_nasdaq     = load_index_csv('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/NASDAQ%20Composite%20Historical%20Data.csv', 'NASDAQ')

# === Merge all into a single DataFrame ===
df_stock = pd.concat([
    df_csi300,
    df_shanghai,
    df_hang_seng,
    df_sp500,
    df_dow_jones,
    df_nasdaq
], axis=1)

# === Handle missing values (optional) ===
df_stock = df_stock.ffill().bfill()

# === Preview the merged DataFrame ===
print(df_stock.head())

import pandas as pd

def load_and_expand_indicator(file_path, countries, indicator_name, start_year=2020, end_year=2024):
    """
    Load a World Bank CSV file and expand yearly data into monthly rows.
    Returns a DataFrame: [Date, Country_Indicator, Value]
    """
    df = pd.read_csv(file_path)
    df_filtered = df[df['Country Name'].isin(countries)]

    years = [str(y) for y in range(start_year, end_year + 1)]
    df_filtered = df_filtered[['Country Name'] + years]

    df_long = df_filtered.melt(id_vars='Country Name',
                               value_vars=years,
                               var_name='Year',
                               value_name='Value')

    # Expand to monthly
    expanded_rows = []
    for _, row in df_long.iterrows():
        for month in range(1, 13):
            date = f"{int(row['Year'])}-{month:02d}"
            column = f"{row['Country Name'].replace(' ', '_')}_{indicator_name}"
            expanded_rows.append({
                'Date': date,
                'Country_Indicator': column,
                'Value': row['Value']
            })

    df_expanded = pd.DataFrame(expanded_rows)

    # Pivot to wide format: Date x Columns
    df_pivot = df_expanded.pivot(index='Date', columns='Country_Indicator', values='Value').reset_index()

    return df_pivot

# === Settings ===
target_countries = [
    'United States',
    'China',
    'Malaysia',
    'Germany',
    'Korea, Rep.',
    'Viet Nam',
    'Canada'
]

# === Load and process each indicator ===
df_gdp = load_and_expand_indicator('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/Gdp%20Growth.csv', target_countries, 'GDP')
df_inflation = load_and_expand_indicator('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/Inflation%20Rate.csv', target_countries, 'Inflation')
df_employment = load_and_expand_indicator('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/Employment%20Rate.csv', target_countries, 'Employment')

# === Merge all data by Date ===
df_combined = df_gdp.merge(df_inflation, on='Date').merge(df_employment, on='Date')

# === Show combined result ===
print(df_combined.head(13))

import pandas as pd

# === Step 1: Load the CSV file ===
df = pd.read_csv('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/us-china-trade-war-tariffs.csv', encoding='ISO-8859-1')

# === Step 2: Rename columns for simplicity ===
df = df.rename(columns={
    'Date': 'Date',
    'Chinese tariffs on ROW exports': 'CN_to_ROW',
    'Chinese tariffs on US exports': 'CN_to_US',
    'US tariffs on Chinese exports': 'US_to_CN',
    'US tariffs on ROW exports': 'US_to_ROW'
})

# === Step 3: Convert 'Date' to datetime and sort ===
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')  # just in case
df = df.sort_values('Date')

# === Step 4: Create a full monthly time series ===
date_range = pd.date_range(start=df['Date'].min(), end='2025-01-01', freq='MS')
monthly_df = pd.DataFrame({'Date': date_range})

# === Step 5: Merge with tariff data and forward-fill ===
monthly_df = monthly_df.merge(df[['Date', 'US_to_ROW', 'CN_to_ROW', 'US_to_CN', 'CN_to_US']], how='left', on='Date')
monthly_df.fillna(method='ffill', inplace=True)

# === Step 6: Format date to Year-Month ===
monthly_df['Date'] = monthly_df['Date'].dt.strftime('%Y-%m')

# === Step 7: Show and/or export ===
print(monthly_df.head(12))  # Show first 12 months


# monthly_df.to_csv('monthly_tariff_timeseries.csv', index=False)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === Step 1: Format all date columns ===
df_stock = df_stock.reset_index()
df_stock['Date'] = df_stock['Date'].dt.to_period('M').dt.to_timestamp()
df_combined['Date'] = pd.to_datetime(df_combined['Date']).dt.to_period('M').dt.to_timestamp()
monthly_df['Date'] = pd.to_datetime(monthly_df['Date']).dt.to_period('M').dt.to_timestamp()

# === Step 2: Merge all datasets ===
merged_df = df_stock.merge(df_combined, on='Date', how='outer')
merged_df = merged_df.merge(monthly_df, on='Date', how='outer')

# === Step 3: Sort by Date and forward-fill ===
merged_df = merged_df.sort_values('Date').reset_index(drop=True)
merged_df = merged_df.ffill()

# === Step 4: Drop rows before 2020 if they contain any NaNs ===
mask_before_2020 = merged_df['Date'] < pd.Timestamp('2020-01-01')
merged_df = pd.concat([
    merged_df[mask_before_2020].dropna(),
    merged_df[~mask_before_2020]
], ignore_index=True)

# === Step 5: Correlation analysis ===
correlation_matrix = merged_df.drop(columns=['Date']).corr(numeric_only=True)

# === Step 6: Display correlation matrix ===
print("=== Correlation Matrix ===")
print(correlation_matrix)

# === Step 7: Optional heatmap visualization ===
plt.figure(figsize=(18, 12))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
plt.title('Correlation Heatmap: Stock Indices, Macro Indicators, and Tariffs', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# method to display in the streamlit
def display_correlation_analysis():
    # Correlation matrix calculation
    correlation_matrix = merged_df.drop(columns=['Date']).corr(numeric_only=True)

    st.write("### Correlation Matrix")
    st.dataframe(correlation_matrix)  # show as table

    # Plot heatmap
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(18,12))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, ax=ax)
    plt.xticks(rotation=45, ha='right')
    plt.title('Correlation Heatmap: Stock Indices, Macro Indicators, and Tariffs', fontsize=14)
    plt.tight_layout()

    st.pyplot(fig)
