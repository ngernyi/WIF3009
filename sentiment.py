import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np

def display_country_timeline_sentiment_dashboard():
    df = pd.read_csv('https://raw.githubusercontent.com/ngernyi/WIF3009/refs/heads/main/tariff_news_with_sentiment.csv', encoding='ISO-8859-1')
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')

    st.title("🌍 Country Sentiment Timeline Analysis - Tariff News")
    
    if 'sentiment_score' not in df.columns:
        st.error("Please run sentiment analysis first!")
        return
    
    # Ensure proper date processing
    if 'month' not in df.columns:
        if 'publishedAt' in df.columns:
            try:
                df['publishedAt'] = pd.to_datetime(df['publishedAt'])
                df['month'] = df['publishedAt'].dt.to_period('M')
                df['year_month'] = df['publishedAt'].dt.strftime('%Y-%m')
                df['year'] = df['publishedAt'].dt.year
                df['quarter'] = df['publishedAt'].dt.to_period('Q')
            except Exception as e:
                st.warning(f"Could not process dates: {e}")
                return
        else:
            st.warning("No 'publishedAt' column found.")
            return
    
    if 'country' not in df.columns:
        st.warning("No 'country' column found. Country analysis cannot be performed.")
        return
    
    # === OVERVIEW METRICS ===
    st.header("📊 Timeline Overview")
    
    # Time range info
    # date_range = f"{df['publishedAt'].min().strftime('%Y-%m-%d')} to {df['publishedAt'].max().strftime('%Y-%m-%d')}"
    total_months = len(df['month'].unique())
    total_countries = len(df['country'].unique())
    
    col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.metric("Date Range", date_range)
    with col1:
        st.metric("Total Months", total_months)
    with col2:
        st.metric("Countries Analyzed", total_countries)
    with col3:
        st.metric("Total Articles", len(df))
    
    # === COUNTRY SELECTION ===
    st.header("🎯 Country Selection & Filtering")
    
    # Get countries sorted by article count
    country_counts = df['country'].value_counts()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        # Multi-select for countries with smart defaults (top 10)
        default_countries = country_counts.head(10).index.tolist()
        selected_countries = st.multiselect(
            "Select countries to analyze (default: top 10 by article count):",
            options=country_counts.index.tolist(),
            default=default_countries,
            key="country_timeline_selector"
        )
    
    with col2:
        # Time granularity selection
        time_granularity = st.selectbox(
            "Time Granularity:",
            ["Monthly", "Quarterly", "Yearly"],
            index=0
        )
    
    if not selected_countries:
        st.warning("Please select at least one country to analyze.")
        return
    
    # Filter data
    filtered_df = df[df['country'].isin(selected_countries)].copy()
    
    # === MAIN TIMELINE VISUALIZATION ===
    st.header("📈 Country Sentiment Timeline - Full Analysis")
    
    # Prepare data based on granularity
    if time_granularity == "Monthly":
        time_col = 'year_month'
        time_period = 'month'
    elif time_granularity == "Quarterly":
        time_col = 'quarter'
        time_period = 'quarter'
        filtered_df['quarter'] = filtered_df['publishedAt'].dt.to_period('Q')
    else:  # Yearly
        time_col = 'year'
        time_period = 'year'
    
    # Create timeline data
    timeline_data = filtered_df.groupby(['country', time_period]).agg({
        'sentiment_score': ['mean', 'std', 'count'],
        'sentiment_label': lambda x: {
            'positive': (x == 'positive').sum(),
            'negative': (x == 'negative').sum(),
            'neutral': (x == 'neutral').sum()
        }
    }).reset_index()
    
    # Flatten columns
    timeline_data.columns = ['country', 'time_period', 'avg_sentiment', 'sentiment_std', 'article_count', 'sentiment_breakdown']
    
    # Extract sentiment breakdowns
    timeline_data['positive_count'] = timeline_data['sentiment_breakdown'].apply(lambda x: x['positive'])
    timeline_data['negative_count'] = timeline_data['sentiment_breakdown'].apply(lambda x: x['negative'])
    timeline_data['neutral_count'] = timeline_data['sentiment_breakdown'].apply(lambda x: x['neutral'])
    timeline_data['positive_pct'] = (timeline_data['positive_count'] / timeline_data['article_count'] * 100).round(1)
    timeline_data['negative_pct'] = (timeline_data['negative_count'] / timeline_data['article_count'] * 100).round(1)
    
    # Convert time_period to string for plotting
    timeline_data['time_str'] = timeline_data['time_period'].astype(str)
    
    # === 1. MAIN SENTIMENT TIMELINE (FULL WIDTH) ===
    st.subheader("🌍 Average Sentiment Score by Country Over Time")
    
    fig_main = px.line(
        timeline_data, 
        x='time_str', 
        y='avg_sentiment', 
        color='country',
        title=f"Country Sentiment Trends - {time_granularity} View",
        labels={'time_str': f'{time_granularity}', 'avg_sentiment': 'Average Sentiment Score'},
        markers=True,
        line_shape='spline'
    )
    
    # Add horizontal line at neutral (0)
    fig_main.add_hline(y=0, line_dash="dash", line_color="gray", 
                      annotation_text="Neutral Line", annotation_position="bottom right")
    
    # Enhance layout
    fig_main.update_layout(
        height=600,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Add hover information
    fig_main.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +
                     f"{time_granularity}: %{{x}}<br>" +
                     "Avg Sentiment: %{y:.3f}<br>" +
                     "<extra></extra>"
    )
    
    st.plotly_chart(fig_main, use_container_width=True)
    
    # === 2. ARTICLE VOLUME TIMELINE (FULL WIDTH) ===
    st.subheader("📰 Article Volume by Country Over Time")
    
    fig_volume = px.bar(
        timeline_data,
        x='time_str',
        y='article_count',
        color='country',
        title=f"Article Volume by Country - {time_granularity} View",
        labels={'time_str': f'{time_granularity}', 'article_count': 'Number of Articles'},
        barmode='group'
    )
    
    fig_volume.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_volume, use_container_width=True)
    
    # # === 3. SENTIMENT VOLATILITY ANALYSIS (FULL WIDTH) ===
    # st.subheader("📊 Sentiment Volatility by Country")
    
    # # Calculate volatility metrics
    # volatility_data = timeline_data.groupby('country').agg({
    #     'avg_sentiment': ['std', 'min', 'max', 'mean'],
    #     'article_count': 'sum'
    # }).reset_index()
    
    # volatility_data.columns = ['country', 'sentiment_std', 'min_sentiment', 'max_sentiment', 'overall_avg', 'total_articles']
    # volatility_data['sentiment_range'] = volatility_data['max_sentiment'] - volatility_data['min_sentiment']
    
    # fig_volatility = px.scatter(
    #     volatility_data,
    #     x='sentiment_std',
    #     y='sentiment_range',
    #     size='total_articles',
    #     color='overall_avg',
    #     hover_name='country',
    #     title="Country Sentiment Volatility Analysis",
    #     labels={
    #         'sentiment_std': 'Sentiment Standard Deviation',
    #         'sentiment_range': 'Sentiment Range (Max - Min)',
    #         'overall_avg': 'Overall Average Sentiment'
    #     },
    #     color_continuous_scale='RdYlGn'
    # )
    
    # fig_volatility.update_layout(height=500)
    # st.plotly_chart(fig_volatility, use_container_width=True)
    
    # # === 4. HEATMAP OF SENTIMENT BY COUNTRY AND TIME (FULL WIDTH) ===
    # st.subheader("🔥 Sentiment Heatmap - Country vs Time")
    
    # # Create pivot table for heatmap
    # heatmap_data = timeline_data.pivot(index='country', columns='time_str', values='avg_sentiment')
    
    # fig_heatmap = px.imshow(
    #     heatmap_data,
    #     title=f"Sentiment Heatmap: Countries vs {time_granularity}",
    #     labels=dict(x=f"{time_granularity}", y="Country", color="Avg Sentiment"),
    #     color_continuous_scale='RdYlGn',
    #     aspect='auto'
    # )
    
    # fig_heatmap.update_layout(height=600)
    # st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # === 5. POSITIVE/NEGATIVE SENTIMENT PERCENTAGES (FULL WIDTH) ===
    st.subheader("📊 Sentiment Distribution Timeline")
    
    # Create subplot for positive and negative percentages
    fig_sentiment_dist = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Positive Sentiment Percentage', 'Negative Sentiment Percentage'),
        vertical_spacing=0.1
    )
    
    # Add positive sentiment traces
    for country in selected_countries:
        country_data = timeline_data[timeline_data['country'] == country]
        fig_sentiment_dist.add_trace(
            go.Scatter(
                x=country_data['time_str'],
                y=country_data['positive_pct'],
                mode='lines+markers',
                name=f"{country} - Positive",
                line=dict(width=2),
                showlegend=True
            ),
            row=1, col=1
        )
        
        fig_sentiment_dist.add_trace(
            go.Scatter(
                x=country_data['time_str'],
                y=country_data['negative_pct'],
                mode='lines+markers',
                name=f"{country} - Negative",
                line=dict(width=2, dash='dash'),
                showlegend=True
            ),
            row=2, col=1
        )
    
    fig_sentiment_dist.update_xaxes(title_text=f"{time_granularity}", row=2, col=1)
    fig_sentiment_dist.update_yaxes(title_text="Positive %", row=1, col=1)
    fig_sentiment_dist.update_yaxes(title_text="Negative %", row=2, col=1)
    
    fig_sentiment_dist.update_layout(
        height=800,
        title_text="Sentiment Distribution Over Time by Country",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_sentiment_dist, use_container_width=True)
    
    # === DETAILED COUNTRY COMPARISON TABLE ===
    st.header("📋 Detailed Country Timeline Statistics")
    
    # Create comprehensive country statistics
    country_stats = filtered_df.groupby('country').agg({
        'sentiment_score': ['mean', 'std', 'min', 'max', 'count'],
        'sentiment_label': [
            lambda x: (x == 'positive').sum(),
            lambda x: (x == 'negative').sum(),
            lambda x: (x == 'neutral').sum()
        ]
    }).round(4)
    
    # Flatten column names
    country_stats.columns = [
        'Avg_Sentiment', 'Sentiment_StdDev', 'Min_Sentiment', 'Max_Sentiment', 'Total_Articles',
        'Positive_Count', 'Negative_Count', 'Neutral_Count'
    ]
    
    # Add percentage and derived metrics
    country_stats['Positive_Pct'] = (country_stats['Positive_Count'] / country_stats['Total_Articles'] * 100).round(1)
    country_stats['Negative_Pct'] = (country_stats['Negative_Count'] / country_stats['Total_Articles'] * 100).round(1)
    country_stats['Neutral_Pct'] = (country_stats['Neutral_Count'] / country_stats['Total_Articles'] * 100).round(1)
    country_stats['Sentiment_Range'] = (country_stats['Max_Sentiment'] - country_stats['Min_Sentiment']).round(4)
    country_stats['Volatility_Score'] = (country_stats['Sentiment_StdDev'] / country_stats['Total_Articles'] * 1000).round(2)
    
    # Add dominant sentiment
    country_stats['Dominant_Sentiment'] = country_stats[['Positive_Count', 'Negative_Count', 'Neutral_Count']].idxmax(axis=1)
    country_stats['Dominant_Sentiment'] = country_stats['Dominant_Sentiment'].str.replace('_Count', '').str.lower()
    
    # Sort by average sentiment
    country_stats = country_stats.sort_values('Avg_Sentiment', ascending=False)
    
    st.dataframe(country_stats, use_container_width=True)

    # === DETAILED INSIGHTS ===
    st.header("🔍 Detailed Insights")
    
    tab1, tab2, tab3 = st.tabs(["Top Articles", "Statistics", "Language Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Most Positive Articles")
            top_positive = df.nlargest(5, 'sentiment_score')[['title', 'sentiment_score'] + (['country'] if 'country' in df.columns else []) + (['publishedAt'] if 'publishedAt' in df.columns else [])]
            for idx, row in top_positive.iterrows():
                country_text = f" | {row['country']}" if 'country' in row else ""
                with st.expander(f"Score: {row['sentiment_score']:.3f}{country_text}"):
                    st.write(f"**Title:** {row['title']}")
                    if 'publishedAt' in row:
                        st.write(f"**Date:** {row['publishedAt'].strftime('%Y-%m-%d')}")
        
        with col2:
            st.subheader("Most Negative Articles")
            top_negative = df.nsmallest(5, 'sentiment_score')[['title', 'sentiment_score'] + (['country'] if 'country' in df.columns else []) + (['publishedAt'] if 'publishedAt' in df.columns else [])]
            for idx, row in top_negative.iterrows():
                country_text = f" | {row['country']}" if 'country' in row else ""
                with st.expander(f"Score: {row['sentiment_score']:.3f}{country_text}"):
                    st.write(f"**Title:** {row['title']}")
                    if 'publishedAt' in row:
                        st.write(f"**Date:** {row['publishedAt'].strftime('%Y-%m-%d')}")
    
    with tab2:
        st.subheader("Statistical Summary")
        
        # Summary by sentiment label
        stats_summary = df.groupby('sentiment_label')['sentiment_score'].describe()
        st.dataframe(stats_summary)
        
        # Box plot
        fig_box = px.box(
            df, x='sentiment_label', y='sentiment_score',
            title="Sentiment Score Distribution by Label",
            color='sentiment_label',
            color_discrete_map={
                'positive': '#2E8B57',
                'neutral': '#FFD700',
                'negative': '#DC143C'
            }
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with tab3:
        if 'lang' in df.columns:
            st.subheader("Analysis by Language")
            
            # Language distribution
            lang_counts = df['lang'].value_counts()
            fig_lang = px.bar(
                x=lang_counts.index,
                y=lang_counts.values,
                title="Number of Articles by Language",
                labels={'x': 'Language', 'y': 'Article Count'}
            )
            st.plotly_chart(fig_lang, use_container_width=True)
            
            # Sentiment by language
            lang_sentiment = df.groupby('lang')['sentiment_score'].mean().sort_values(ascending=False)
            st.write("**Average Sentiment Score by Language:**")
            for lang, score in lang_sentiment.items():
                st.write(f"- {lang}: {score:.3f}")
        else:
            st.info("No language data available for analysis.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Most Positive Countries")
        top_positive = country_stats.head(3)
        for idx, (country, row) in enumerate(top_positive.iterrows(), 1):
            with st.expander(f"{idx}. {country} (Score: {row['Avg_Sentiment']:.3f})"):
                st.write(f"**Positive Articles:** {row['Positive_Pct']:.1f}%")
                st.write(f"**Total Articles:** {int(row['Total_Articles'])}")
                st.write(f"**Volatility:** {row['Sentiment_StdDev']:.3f}")
                st.write(f"**Range:** {row['Min_Sentiment']:.3f} to {row['Max_Sentiment']:.3f}")
    
    with col2:
        st.subheader("📉 Most Negative Countries")
        bottom_negative = country_stats.tail(3)
        for idx, (country, row) in enumerate(bottom_negative.iterrows(), 1):
            with st.expander(f"{idx}. {country} (Score: {row['Avg_Sentiment']:.3f})"):
                st.write(f"**Negative Articles:** {row['Negative_Pct']:.1f}%")
                st.write(f"**Total Articles:** {int(row['Total_Articles'])}")
                st.write(f"**Volatility:** {row['Sentiment_StdDev']:.3f}")
                st.write(f"**Range:** {row['Min_Sentiment']:.3f} to {row['Max_Sentiment']:.3f}")
    
    # # === TIMELINE TRENDS ANALYSIS ===
    # st.subheader("📊 Timeline Trend Analysis")
    
    # # Calculate trends for each country
    # trend_analysis = []
    # for country in selected_countries:
    #     country_timeline = timeline_data[timeline_data['country'] == country].sort_values('time_str')
    #     if len(country_timeline) > 1:
    #         # Calculate trend using linear regression
    #         x_vals = np.arange(len(country_timeline))
    #         y_vals = country_timeline['avg_sentiment'].values
            
    #         if len(x_vals) > 1:
    #             trend_slope = np.polyfit(x_vals, y_vals, 1)[0]
    #             trend_direction = "📈 Improving" if trend_slope > 0.01 else "📉 Declining" if trend_slope < -0.01 else "➡️ Stable"
                
    #             recent_sentiment = country_timeline['avg_sentiment'].iloc[-1]
    #             early_sentiment = country_timeline['avg_sentiment'].iloc[0]
    #             overall_change = recent_sentiment - early_sentiment
                
    #             trend_analysis.append({
    #                 'Country': country,
    #                 'Trend_Direction': trend_direction,
    #                 'Trend_Slope': round(trend_slope, 4),
    #                 'Overall_Change': round(overall_change, 4),
    #                 'Recent_Sentiment': round(recent_sentiment, 3),
    #                 'Early_Sentiment': round(early_sentiment, 3)
    #             })
    
    # if trend_analysis:
    #     trend_df = pd.DataFrame(trend_analysis)
    #     trend_df = trend_df.sort_values('Trend_Slope', ascending=False)
        
    #     st.dataframe(trend_df, use_container_width=True)
        
    #     # Highlight key trends
    #     st.write("**🎯 Key Trend Observations:**")
        
    #     improving_countries = trend_df[trend_df['Trend_Slope'] > 0.01]['Country'].tolist()
    #     declining_countries = trend_df[trend_df['Trend_Slope'] < -0.01]['Country'].tolist()
        
    #     if improving_countries:
    #         st.success(f"**Improving Sentiment:** {', '.join(improving_countries)}")
        
    #     if declining_countries:
    #         st.error(f"**Declining Sentiment:** {', '.join(declining_countries)}")
        
    #     if len(trend_df[abs(trend_df['Trend_Slope']) <= 0.01]) > 0:
    #         stable_countries = trend_df[abs(trend_df['Trend_Slope']) <= 0.01]['Country'].tolist()
    #         st.info(f"**Stable Sentiment:** {', '.join(stable_countries)}")
    
    # === EXPORT SECTION ===
    st.header("📥 Export Timeline Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export timeline data
        timeline_export = timeline_data.drop('sentiment_breakdown', axis=1)
        timeline_csv = timeline_export.to_csv(index=False)
        st.download_button(
            label="📊 Download Timeline Data",
            data=timeline_csv,
            file_name=f"country_sentiment_timeline_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export country statistics
        country_stats_csv = country_stats.to_csv()
        st.download_button(
            label="📋 Download Country Statistics",
            data=country_stats_csv,
            file_name=f"country_sentiment_stats_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Display Summary in Point Form
    st.header("Summary")

    summary_points = [
        "**Canada** shows a significant **increase in article volume** starting from late 2024.",
        "- Very high negative sentiment in **Nov 2024 to Mar 2025** (e.g. 71, 80, 49, 46, 80 negative articles).",
        "- Positive sentiment also increased in the same period, peaking in **Feb 2025** with **55 positive articles**.",
        "- This suggests a surge of both **controversial and optimistic news** around that time.",
        "",
        "**China** maintains a relatively **balanced sentiment profile**:",
        "- Negative, neutral, and positive articles are distributed more evenly.",
        "- Noticeable **growth in neutral and positive sentiment** in **2024-2025**, especially **Feb 2025** with **36 neutral** and **34 positive** articles.",
        "- Low overall negative sentiment compared to other countries.",
        "",
        "**Germany** consistently has a **high volume of articles** every month:",
        "- Across all months, **positive articles generally outnumber negative ones**.",
        "- Peaks of positive sentiment observed in **2022-03 (75)**, **2023-03 (75)**, and **2023-05 (77)**.",
        "- Negative sentiment is stable but lower than positive in most months.",
        "",
        "**US** sentiment is **more volatile**:",
        "- Spikes in negative sentiment in **Nov 2024 (59 negative)** and **Jan 2025 (70 negative)**.",
        "- Positive sentiment increased notably during the same periods, but still **lags behind negative sentiment** in early 2025.",
        "- A general pattern of **polarized sentiment** emerges toward late 2024 and early 2025."
    ]

    # Print each point
    for point in summary_points:
        st.markdown(point)

