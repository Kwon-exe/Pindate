import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Coverage Gaps")
st.write("Find cities with high user activity but low venue listings — opportunities to grow the platform.")

data, err = api_get("/analytics/coverage")
if err:
    show_api_error(err)
    st.stop()

if not data:
    st.info("No coverage data available.")
    st.stop()

df = pd.DataFrame(data)
df["totalUsers"]   = df["totalUsers"].astype(int)
df["totalVenues"]  = df["totalVenues"].astype(int)
df["totalReviews"] = df["totalReviews"].astype(int)

# Gap score: high users + high reviews relative to low venues
df["gapScore"] = df["totalUsers"] + df["totalReviews"] - (df["totalVenues"] * 5)

col1, col2, col3 = st.columns(3)
col1.metric("Cities Tracked", len(df))
col2.metric("Cities with 0 Venues", int((df["totalVenues"] == 0).sum()))
col3.metric("Highest Gap Score", int(df["gapScore"].max()))

st.divider()
st.subheader("Users vs Venues by City")
chart_df = df.set_index("city")[["totalUsers", "totalVenues"]].head(15)
st.bar_chart(chart_df)

st.divider()
st.subheader("Coverage Gap Table (sorted by gap score)")
display = df.sort_values("gapScore", ascending=False)[
    ["city", "totalUsers", "totalVenues", "totalReviews", "gapScore"]
].copy()
display.columns = ["City", "Total Users", "Total Venues", "Total Reviews", "Gap Score"]
st.dataframe(display, use_container_width=True, hide_index=True)
