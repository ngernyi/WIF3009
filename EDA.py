import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from data_cleaning import load_and_clean_china, load_and_clean_us
import pandas as pd


def plot_bar_chart(df, value_col, title, xlabel, top_n=3):
    fig, ax = plt.subplots(figsize=(10, 5))
    sorted_df = df.sort_values(value_col, ascending=True)
    colors = ['green' if val > 0 else 'red' for val in sorted_df[value_col]]

    bars = ax.barh(sorted_df.index, sorted_df[value_col], color=colors)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Partner Country")
    ax.set_title(title)

    # Annotate top N increases and decreases
    top_increases = sorted_df.sort_values(value_col, ascending=False).head(top_n)
    top_decreases = sorted_df.sort_values(value_col).head(top_n)

    for idx in top_increases.index:
        val = sorted_df.loc[idx, value_col]
        ax.annotate(f"\u25B2 {val:.2f}", xy=(val, idx), xytext=(5, 0), textcoords='offset points', va='center', fontsize=8, color='green')

    for idx in top_decreases.index:
        val = sorted_df.loc[idx, value_col]
        ax.annotate(f"\u25BC {val:.2f}", xy=(val, idx), xytext=(5, 0), textcoords='offset points', va='center', fontsize=8, color='red')

    plt.tight_layout()
    return fig


def show_trade_balance_charts():
    df_china = load_and_clean_china()
    df_us = load_and_clean_us()

    def melt_and_prepare(df):
        df_long = df.melt(id_vars="Partners", var_name="Year Month", value_name="Trade Balance")
        df_long["Date"] = pd.to_datetime(df_long["Year Month"], format="%Y %B")
        return df_long.sort_values("Date")

    df_china_long = melt_and_prepare(df_china)
    df_us_long = melt_and_prepare(df_us)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Trade Balance Over Time by Country (China)")
        fig, ax = plt.subplots(figsize=(10, 6))
        for partner in df_china_long["Partners"].unique():
            country_data = df_china_long[df_china_long["Partners"] == partner]
            ax.plot(country_data["Date"], country_data["Trade Balance"], label=partner)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.set_xlabel("Month")
        ax.set_ylabel("Trade Balance")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        latest_date = df_china_long["Date"].max()
        latest_data = df_china_long[df_china_long["Date"] == latest_date][["Partners", "Trade Balance"]].set_index("Partners")
        st.markdown(f"**Latest Trade Balance (as of {latest_date.strftime('%b %Y')}):**")
        st.table(latest_data)

        base = df_china_long[df_china_long["Year Month"] == "2020 June"].set_index("Partners")["Trade Balance"]
        recent = df_china_long[df_china_long["Year Month"] == "2025 March"].set_index("Partners")["Trade Balance"]
        comparison = pd.DataFrame({"2020 (Jun)": base, "2025 (Mar)": recent})
        comparison["Absolute Change"] = comparison["2025 (Mar)"] - comparison["2020 (Jun)"]
        comparison["% Change"] = (comparison["Absolute Change"] / comparison["2020 (Jun)"]) * 100

        st.markdown("### Trade Balance Change: June 2020 vs March 2025 (China)")
        st.dataframe(comparison.style.format({
            "2020 (Jun)": "{:.2f}",
            "2025 (Mar)": "{:.2f}",
            "Absolute Change": "{:.2f}",
            "% Change": "{:.2f}%"
        }).background_gradient(cmap="RdYlGn", subset=["Absolute Change", "% Change"]))

        st.markdown("#### \U0001F4CA Summary Stats (China)")
        st.metric("Mean Change", f"{comparison['Absolute Change'].mean():.2f}")
        st.metric("Median Change", f"{comparison['Absolute Change'].median():.2f}")

        st.markdown("**Visual: Absolute Change in Trade Balance (China)**")
        fig_abs = plot_bar_chart(comparison, "Absolute Change", "Absolute Change (2020 Jun vs 2025 Mar)", "Change", top_n=3)
        st.pyplot(fig_abs)

        st.markdown("**Visual: Percentage Change in Trade Balance (China)**")
        fig_pct = plot_bar_chart(comparison.dropna(), "% Change", "% Change (2020 Jun vs 2025 Mar)", "% Change", top_n=3)
        st.pyplot(fig_pct)

    with col2:
        st.subheader("Trade Balance Over Time by Country (US)")
        fig, ax = plt.subplots(figsize=(10, 6))
        for partner in df_us_long["Partners"].unique():
            country_data = df_us_long[df_us_long["Partners"] == partner]
            ax.plot(country_data["Date"], country_data["Trade Balance"], label=partner)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.set_xlabel("Month")
        ax.set_ylabel("Trade Balance")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        latest_date_us = df_us_long["Date"].max()
        latest_data_us = df_us_long[df_us_long["Date"] == latest_date_us][["Partners", "Trade Balance"]].set_index("Partners")
        st.markdown(f"**Latest Trade Balance (as of {latest_date_us.strftime('%b %Y')}):**")
        st.table(latest_data_us)

        base_us = df_us_long[df_us_long["Year Month"] == "2020 June"].set_index("Partners")["Trade Balance"]
        recent_us = df_us_long[df_us_long["Year Month"] == "2025 March"].set_index("Partners")["Trade Balance"]
        comparison_us = pd.DataFrame({"2020 (Jun)": base_us, "2025 (Mar)": recent_us})
        comparison_us["Absolute Change"] = comparison_us["2025 (Mar)"] - comparison_us["2020 (Jun)"]
        comparison_us["% Change"] = (comparison_us["Absolute Change"] / comparison_us["2020 (Jun)"]) * 100

        st.markdown("### Trade Balance Change: June 2020 vs March 2025 (US)")
        st.dataframe(comparison_us.style.format({
            "2020 (Jun)": "{:.2f}",
            "2025 (Mar)": "{:.2f}",
            "Absolute Change": "{:.2f}",
            "% Change": "{:.2f}%"
        }).background_gradient(cmap="RdYlGn", subset=["Absolute Change", "% Change"]))

        st.markdown("#### \U0001F4CA Summary Stats (US)")
        st.metric("Mean Change", f"{comparison_us['Absolute Change'].mean():.2f}")
        st.metric("Median Change", f"{comparison_us['Absolute Change'].median():.2f}")

        st.markdown("**Visual: Absolute Change in Trade Balance (US)**")
        fig_abs_us = plot_bar_chart(comparison_us, "Absolute Change", "Absolute Change (2020 Jun vs 2025 Mar)", "Change", top_n=3)
        st.pyplot(fig_abs_us)

        st.markdown("**Visual: Percentage Change in Trade Balance (US)**")
        fig_pct_us = plot_bar_chart(comparison_us.dropna(), "% Change", "% Change (2020 Jun vs 2025 Mar)", "% Change", top_n=3)
        st.pyplot(fig_pct_us)