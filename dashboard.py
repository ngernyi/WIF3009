import streamlit as st
from EDA import show_trade_balance_charts
from product_analysis import plot_trade_balances
from introduction_Q1 import display_project_scope_justification
from correlation_analysis import display_correlation_analysis
from introduction_Q4 import display_correlation_analysis_intro

st.title("Impact Analysis of US-China Tariffs")

if "section" not in st.session_state:
    st.session_state.section = "Data Collection & Cleaning"

def set_section(new_section):
    st.session_state.section = new_section

with st.sidebar:
    st.markdown("## Navigation")
    if st.button("Data Collection & Cleaning"):
        set_section("Data Collection & Cleaning")
    if st.button("Exploratory Data Analysis"):
        set_section("Exploratory Data Analysis")
    if st.button("Sentiment Analysis"):
        set_section("Sentiment Analysis")
    if st.button("Correlation Analysis"):
        set_section("Correlation Analysis")
    if st.button("Predictive Modeling"):
        set_section("Predictive Modeling")
    if st.button("Visualization of Findings"):
        set_section("Visualization of Findings")
    if st.button("Conclusion & Recommendations"):
        set_section("Conclusion & Recommendations")

section = st.session_state.section

st.write(f"### {section}")


if section == "Data Collection & Cleaning":
    display_project_scope_justification()
elif section == "Exploratory Data Analysis":
    show_trade_balance_charts()
    plot_trade_balances()
elif section == "Sentiment Analysis":
    st.write("Content about sentiment analysis...")
elif section == "Correlation Analysis":
    display_correlation_analysis_intro()
    display_correlation_analysis()
elif section == "Predictive Modeling":
    st.write("Content about predictive modeling...")
elif section == "Visualization of Findings":
    st.write("Content about visualization...")
elif section == "Conclusion & Recommendations":
    st.write("Content about conclusions and recommendations...")