import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Knicks Lineup Intelligence",
    page_icon="🏀",
    layout="wide"
)

CLUSTERED_PATH = Path("data/processed/knicks_lineups_clustered.csv")
COMPARISON_PATH = Path("data/processed/knicks_lineup_regular_vs_playoffs.csv")
PLAYOFF_DELTA_PATH = Path("data/processed/knicks_shared_playoff_lineups.csv")


@st.cache_data
def load_data():
    clustered = pd.read_csv(CLUSTERED_PATH)

    comparison = (
        pd.read_csv(COMPARISON_PATH)
        if COMPARISON_PATH.exists()
        else pd.DataFrame()
    )

    playoff_delta = (
        pd.read_csv(PLAYOFF_DELTA_PATH)
        if PLAYOFF_DELTA_PATH.exists()
        else pd.DataFrame()
    )

    return clustered, comparison, playoff_delta


df, comparison_df, playoff_delta_df = load_data()

if not playoff_delta_df.empty:
    playoff_delta_df.columns = [
        "_".join([str(i) for i in col if i != ""]).strip("_")
        if isinstance(col, tuple)
        else col
        for col in playoff_delta_df.columns
    ]


# ---------------------------------------------------
# CSS
# ---------------------------------------------------

css = """
<style>
.stApp {
    background-color: #f8fafc;
    color: #0f172a;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e2e8f0;
}

section[data-testid="stSidebar"] * {
    color: #0f172a !important;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e2e8f0;
    padding: 22px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.06);
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #1d4ed8 !important;
    font-weight: 900;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: white;
    border-radius: 999px;
    color: #334155;
    padding: 10px 18px;
    border: 1px solid #cbd5e1;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #f97316, #2563eb);
    color: white !important;
    border: none;
}

.hero-card {
    padding: 42px;
    border-radius: 24px;
    background: linear-gradient(90deg, #1d4ed8, #f97316);
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(15,23,42,0.12);
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    color: white;
    line-height: 1.2;
    margin-bottom: 14px;
}

.hero-subtitle {
    font-size: 18px;
    color: #fff7ed;
    line-height: 1.6;
    max-width: 900px;
}

.insight-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #f97316;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 6px 18px rgba(15,23,42,0.06);
}

.insight-title {
    font-size: 24px;
    font-weight: 700;
    color: #1d4ed8;
    margin-bottom: 10px;
}

.insight-text {
    color: #475569;
    font-size: 16px;
    line-height: 1.7;
}

.footer {
    color: #64748b;
    font-size: 13px;
    margin-top: 35px;
    text-align: center;
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)


# ---------------------------------------------------
# HERO HEADER
# ---------------------------------------------------

hero_html = """
<div class="hero-card">
    <div class="hero-title">Knicks Lineup Intelligence Dashboard</div>
    <div class="hero-subtitle">
        Machine learning-powered lineup clustering, playoff comparison analysis,
        and advanced Knicks lineup intelligence.
    </div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Dashboard Filters")

archetypes = sorted(df["lineup_archetype"].dropna().unique())

selected_archetypes = st.sidebar.multiselect(
    "Lineup Archetype",
    archetypes,
    default=archetypes
)

min_minutes = st.sidebar.slider(
    "Minimum Minutes Played",
    min_value=float(df["min"].min()),
    max_value=float(df["min"].max()),
    value=float(df["min"].min())
)

filtered_df = df[
    df["lineup_archetype"].isin(selected_archetypes)
    & (df["min"] >= min_minutes)
].copy()


# ---------------------------------------------------
# KPIS
# ---------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Lineups Analyzed", f"{len(filtered_df):,}")
c2.metric("Avg Net Rating", f"{filtered_df['net_rating'].mean():.2f}")
c3.metric("Best Net Rating", f"{filtered_df['net_rating'].max():.2f}")
c4.metric("Avg Offensive Rating", f"{filtered_df['off_rating'].mean():.2f}")


# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Overview",
        "Cluster Explorer",
        "Playoff Analysis",
        "Archetype Insights",
        "Data Explorer"
    ]
)


with tab1:
    st.subheader("Executive Overview")

    summary = (
        filtered_df
        .groupby("lineup_archetype")
        .agg(
            lineup_count=("group_name", "count"),
            avg_net_rating=("net_rating", "mean"),
            avg_off_rating=("off_rating", "mean"),
            avg_def_rating=("def_rating", "mean")
        )
        .reset_index()
        .round(2)
    )

    fig = px.bar(
        summary,
        x="lineup_archetype",
        y="avg_net_rating",
        color="lineup_archetype",
        title="Average Net Rating by Archetype",
        template="plotly_white"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#0f172a",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(summary, use_container_width=True, hide_index=True)


with tab2:
    st.subheader("Lineup Cluster Visualization")

    fig = px.scatter(
        filtered_df,
        x="pca_1",
        y="pca_2",
        color="lineup_archetype",
        size="min",
        hover_name="group_name",
        title="KMeans Lineup Clustering",
        template="plotly_white"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#0f172a"
    )

    st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.subheader("Regular Season vs Playoff Analysis")

    if not comparison_df.empty:
        fig = px.box(
            comparison_df,
            x="season_type",
            y="net_rating",
            color="season_type",
            title="Regular Season vs Playoff Net Rating",
            template="plotly_white"
        )

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_color="#0f172a"
        )

        st.plotly_chart(fig, use_container_width=True)

    if not playoff_delta_df.empty and {
        "minutes_delta",
        "net_rating_delta"
    }.issubset(playoff_delta_df.columns):

        fig = px.scatter(
            playoff_delta_df,
            x="minutes_delta",
            y="net_rating_delta",
            hover_name="group_name",
            hover_data=[
                "off_rating_delta",
                "def_rating_delta"
            ],
            title="Playoff Lineup Performance Delta",
            template="plotly_white"
        )

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_color="#0f172a"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            playoff_delta_df.sort_values(
                "net_rating_delta",
                ascending=False
            ).head(10),
            use_container_width=True,
            hide_index=True
        )


with tab4:
    st.subheader("Lineup Archetype Insights")

    insights_html = """
    <div class="insight-card">
        <div class="insight-title">Balanced Elite Units</div>
        <div class="insight-text">
            Strong two-way lineups with efficient offense and elite defensive performance.
        </div>
    </div>

    <div class="insight-card">
        <div class="insight-title">High-Offense Scoring Units</div>
        <div class="insight-text">
            Explosive offensive lineups with strong shooting efficiency and scoring production.
        </div>
    </div>

    <div class="insight-card">
        <div class="insight-title">Ball-Movement Units</div>
        <div class="insight-text">
            Lineups emphasizing passing, spacing, and offensive flow.
        </div>
    </div>

    <div class="insight-card">
        <div class="insight-title">Low-Efficiency Units</div>
        <div class="insight-text">
            Lower-performing lineups with weaker overall efficiency indicators.
        </div>
    </div>
    """

    st.markdown(insights_html, unsafe_allow_html=True)


with tab5:
    st.subheader("Data Explorer")

    dataset_choice = st.selectbox(
        "Select Dataset",
        [
            "Clustered Lineups",
            "Regular vs Playoffs",
            "Playoff Delta Analysis"
        ]
    )

    if dataset_choice == "Clustered Lineups":
        display_df = filtered_df.copy()
    elif dataset_choice == "Regular vs Playoffs":
        display_df = comparison_df.copy()
    else:
        display_df = playoff_delta_df.copy()

    search = st.text_input("Search lineup/player")

    if search and "group_name" in display_df.columns:
        display_df = display_df[
            display_df["group_name"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv = display_df.to_csv(index=False)

    st.download_button(
        "Download Filtered Data",
        csv,
        "knicks_dashboard_export.csv",
        "text/csv"
    )


footer_html = """
<div class="footer">
    Built with Python, Streamlit, Plotly, scikit-learn, PCA,
    KMeans clustering, and NBA lineup data.
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)