import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Review Volume Monitor")
st.write("Track review submission volume per venue over time. Spot unusual spikes that may indicate review bombing.")

data, err = api_get("/analytics/reviews/volume")
if err:
    show_api_error(err)
    st.stop()

if not data:
    st.info("No review data available.")
    st.stop()

df = pd.DataFrame(data)
df["reviewCount"] = df["reviewCount"].astype(int)
df["avgRating"]   = df["avgRating"].astype(float)
df["period"]      = df["reviewYear"].astype(str) + "-" + df["reviewMonth"].astype(str).str.zfill(2)

# Flag potential anomalies: venues with unusually high monthly review counts
mean_count = df["reviewCount"].mean()
std_count  = df["reviewCount"].std()
threshold  = mean_count + (2 * std_count) if std_count > 0 else mean_count + 1
df["anomaly"] = df["reviewCount"] > threshold

anomalies = df[df["anomaly"]]

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df))
col2.metric("Venues Tracked", df["venueId"].nunique())
col3.metric("Anomalies Detected", len(anomalies))

if not anomalies.empty:
    st.warning(f"**{len(anomalies)} anomalous month(s) detected** — unusually high review volume (>{threshold:.0f} reviews/month).")
    anom_display = anomalies[["name", "period", "reviewCount", "avgRating"]].copy()
    anom_display.columns = ["Venue", "Period", "Reviews", "Avg Rating"]
    st.dataframe(anom_display, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Review Volume by Venue & Period")

venue_names = ["All"] + sorted(df["name"].unique().tolist())
selected_venue = st.selectbox("Filter by venue", venue_names)

filtered = df if selected_venue == "All" else df[df["name"] == selected_venue]

display = filtered[["name", "period", "reviewCount", "avgRating", "anomaly"]].copy()
display.columns = ["Venue", "Period", "Review Count", "Avg Rating", "Anomaly"]
st.dataframe(display, use_container_width=True, hide_index=True)
