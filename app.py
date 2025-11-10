import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Football Analytics Dashboard", layout="wide")

st.title("🏈 Football Analytics Dashboard")
st.markdown("Upload your game data to analyze offensive and defensive efficiency.")

uploaded_file = st.file_uploader("Upload CSV file with play data", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # Example expected columns: play_type, formation, down, distance, yards_gained, success, defense_front, coverage
    if all(col in df.columns for col in ["play_type", "formation", "yards_gained", "success", "defense_front"]):
        st.subheader("Offensive Success Rates by Formation")
        success_rates = (
            df.groupby("formation")["success"].mean().reset_index().sort_values(by="success", ascending=False)
        )
        fig = px.bar(success_rates, x="formation", y="success", title="Success Rate by Formation")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Yards Gained by Play Type")
        fig2 = px.box(df, x="play_type", y="yards_gained", title="Yards per Play Type")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Defensive Efficiency vs. Play Type")
        defense_eff = (
            df.groupby(["defense_front", "play_type"])["success"].mean().reset_index()
        )
        fig3 = px.bar(defense_eff, x="defense_front", y="success", color="play_type",
                      title="Defensive Front vs Play Type Success")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Your CSV must include columns: play_type, formation, yards_gained, success, and defense_front.")
else:
    st.info("Upload a CSV file to get started.")
