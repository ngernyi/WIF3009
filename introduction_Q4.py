# In your module file (e.g., task4.py)
import streamlit as st

def display_correlation_analysis_intro():
    st.write("## Correlation Analysis")

    st.markdown("""
    To explore the broader economic impact of the US-China trade war, we analyzed several key macroeconomic indicators and stock market indices from both countries. These datasets were selected to assess whether tariff changes correlate with shifts in economic performance.

    **Economic Indicators Considered:**

    1. **GDP Growth (NY.GDP.MKTP.KD.ZG)**  
    *Justification:* GDP growth reflects the overall economic health and productivity of a country. By analyzing this, we can evaluate how the trade war affected economic expansion in the US, China and other countries.

    2. **Inflation Rate (FP.CPI.TOTL.ZG)**  
    *Justification:* Tariffs can lead to higher import costs, which may fuel inflation. Tracking inflation helps us understand whether the tariffs had downstream effects on consumer prices.

    3. **Employment Rate (SL.EMP.TOTL.SP.ZS)**  
    *Justification:* Employment trends offer insight into how businesses are responding to trade pressures. Drops in employment could signal reduced production or investor uncertainty.

    **Stock Market Indices:**

    - **China:**
        - Shanghai Shenzhen CSI 300  
        - Shanghai Composite  
        - Hang Seng Index  

    - **United States:**
        - S&P 500  
        - Dow Jones Industrial Average  
        - NASDAQ Composite  

    *Justification:* Stock markets are sensitive to political and economic events. Analyzing key indices enables us to gauge investor sentiment and market volatility in response to tariff announcements and escalations.

    Together, these indicators provide a comprehensive view of how the trade war may have influenced both economies at a macro level.
    """)
