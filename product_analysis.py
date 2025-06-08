import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

CSV_SOURCE_FILES = [
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_12_CN.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_12_US.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_39_CN.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_39_US.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_84_CN.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_84_US.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_85_CN.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_85_US.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_87_CN.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_87_US.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_90_CN.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_90_US.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_94_CN.csv",
    "https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/combined_94_US.csv",
]

CUSTOM_TITLES = {
    "combined_12_CN": "Trade Balance of *HS Code 12 (Seed, fruit and other grains)* - China Towards Other Countries",
    "combined_12_US": "Trade Balance of *HS Code 12 (Seed, fruit and other grains)* - US Towards Other Countries",
    "combined_39_CN": "Trade Balance of *HS Code 39 (Plastics and articles thereof)* - China Towards Other Countries",
    "combined_39_US": "Trade Balance of *HS Code 39 (Plastics and articles thereof)* - US Towards Other Countries",
    "combined_84_CN": "Trade Balance of *HS Code 84 (Machinery & Boilers)* - China Towards Other Countries",
    "combined_84_US": "Trade Balance of *HS Code 84 (Machinery & Boilers)* - US Towards Other Countries",
    "combined_85_CN": "Trade Balance of *HS Code 85 (Electrical Machinery)* - China Towards Other Countries",
    "combined_85_US": "Trade Balance of *HS Code 85 (Electrical Machinery)* - US Towards Other Countries",
    "combined_87_CN": "Trade Balance of *HS Code 87 (Vehicles excluding rail)* - China Towards Other Countries",
    "combined_87_US": "Trade Balance of *HS Code 87 (Vehicles excluding rail)* - US Towards Other Countries",
    "combined_90_CN": "Trade Balance of *HS Code 90 (Precision Instruments)* - China Towards Other Countries",
    "combined_90_US": "Trade Balance of *HS Code 90 (Precision Instruments)* - US Towards Other Countries",
    "combined_94_CN": "Trade Balance of *HS Code 94 (Furniture and Lighting)* - China Towards Other Countries",
    "combined_94_US": "Trade Balance of *HS Code 94 (Furniture and Lighting)* - US Towards Other Countries",
}

INSIGHTS = {
    "combined_12_CN": (
        "China shows a **consistent negative trade balance** in HS 12 (agriculture), "
        "indicating heavy reliance on imports for seeds, fruits, and grains."
    ),
    "combined_12_US": (
        "The US maintains a **strong positive trade balance** in HS 12, "
        "confirming its role as a major exporter of agricultural products."
    ),
    "combined_39_CN": (
        "China exhibits a **steady positive trade balance** in plastics (HS 39), "
        "reflecting strong export capacity and manufacturing dominance."
    ),
    "combined_39_US": (
        "The US shows **fluctuating and mostly negative balances** in plastics (HS 39), "
        "highlighting import reliance in this sector."
    ),
    "combined_84_CN": (
        "China holds a **strong and increasing trade surplus** in machinery (HS 84), "
        "reflecting leadership in manufacturing and exports."
    ),
    "combined_84_US": (
        "The US has **mostly negative or balanced trade balances** in machinery (HS 84), "
        "indicating import dependence."
    ),
    "combined_85_CN": (
        "China has a **strong positive trade balance** in electrical machinery (HS 85), "
        "showcasing export strength."
    ),
    "combined_85_US": (
        "The US shows **mixed and often negative trade balances** in electrical machinery (HS 85), "
        "demonstrating import reliance."
    ),
    "combined_87_CN": (
        "China shows a **growing surplus** in vehicles (HS 87), indicating expanding exports."
    ),
    "combined_87_US": (
        "The US experiences a **negative trade balance** in vehicles (HS 87), "
        "showing dependence on vehicle imports."
    ),
    "combined_90_CN": (
        "China has **moderate positive trade balances** in precision instruments (HS 90), "
        "suggesting emerging competitiveness."
    ),
    "combined_90_US": (
        "The US shows **variable trade balances** in precision instruments (HS 90), "
        "reflecting a competitive and fluctuating market."
    ),
    "combined_94_CN": (
        "China maintains a **solid positive trade balance** in furniture and lighting (HS 94), "
        "dominating exports."
    ),
    "combined_94_US": (
        "The US generally holds a **negative trade balance** in furniture and lighting (HS 94), "
        "relying on imports."
    ),
}

def plot_trade_balances():
    for url in CSV_SOURCE_FILES:
        try:
            df = pd.read_csv(url)
            if "Partners" not in df.columns:
                st.warning(f"Skipping {url}: 'Partners' column not found.")
                continue

            df_melted = df.melt(id_vars=["Partners"], var_name="Date", value_name="Trade Balance")
            df_melted[["Year", "Month"]] = df_melted["Date"].str.extract(r"(\d{4})-M(\d{2})")
            df_melted["Date"] = pd.to_datetime(df_melted["Year"] + "-" + df_melted["Month"], format="%Y-%m")
            df_pivot = df_melted.pivot(index="Date", columns="Partners", values="Trade Balance")

            file_name = url.split("/")[-1].replace(".csv", "")
            title = CUSTOM_TITLES.get(file_name, f"Trade Balance for {file_name}")

            st.markdown(f"### {title}")

            fig, ax = plt.subplots(figsize=(14, 6))
            for country in df_pivot.columns:
                ax.plot(df_pivot.index, df_pivot[country], label=country)
            ax.set_xlabel("Month-Year")
            ax.set_ylabel("Trade Balance")
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
            plt.xticks(rotation=45)
            ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
            plt.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

            # Display insight below each plot
            insight_text = INSIGHTS.get(file_name, "No specific insights available for this dataset.")
            st.markdown(f"**Insight:** {insight_text}")

        except Exception as e:
            st.error(f"Error processing {url}: {e}")

    # Optional: Overall summary insights at the end
    st.markdown("## 📊 Summary Insights & Conclusion")
    st.markdown("""
    ### 🟢 China
    - Strong **positive trade balances** in:
      - HS 39: Plastics
      - HS 84 & 85: Machinery & Electrical equipment
      - HS 87: Vehicles
    - **Negative trade balance** in:
      - HS 12 (agriculture): Heavy importer

    ### 🔵 United States
    - **Positive trade balances** in:
      - HS 12: Agriculture (strong exporter)
    - **Mixed or negative balances** in:
      - HS 39, 84, 85, 87: Indicates reliance on imports
      - HS 90 & 94: Competitive but fluctuating

    ---

    ### ✅ Final Conclusion:
    - **China dominates in manufacturing-related exports** (machinery, electronics, vehicles).
    - **US leads in agriculture**, but is **less competitive** in manufactured goods.
    - Trade imbalances align with each country’s **industrial strengths and dependencies**.
    """)
