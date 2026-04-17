import streamlit as st
import pandas as pd
from datetime import datetime, timezone

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("User Retention")
st.write("Identify active vs. inactive users to understand retention and guide re-engagement efforts.")

data, err = api_get("/analytics/retention")
if err:
    show_api_error(err)
    st.stop()

if not data:
    st.info("No retention data available.")
    st.stop()

df = pd.DataFrame(data)
df["totalReviews"] = df["totalReviews"].astype(int)
df["totalSaves"]   = df["totalSaves"].astype(int)

# Classify activity
def classify(row):
    if row["lastReview"] is None and row["lastSave"] is None:
        return "Never Active"
    last = max(
        pd.Timestamp(row["lastReview"]) if row["lastReview"] else pd.Timestamp.min,
        pd.Timestamp(row["lastSave"])   if row["lastSave"]   else pd.Timestamp.min,
    )
    days_ago = (pd.Timestamp.now() - last).days
    if days_ago <= 30:
        return "Active"
    elif days_ago <= 90:
        return "At Risk"
    else:
        return "Inactive"

df["status"] = df.apply(classify, axis=1)

counts = df["status"].value_counts()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", len(df))
col2.metric("Active (≤30d)", int(counts.get("Active", 0)))
col3.metric("At Risk (31–90d)", int(counts.get("At Risk", 0)))
col4.metric("Inactive / Never", int(counts.get("Inactive", 0)) + int(counts.get("Never Active", 0)))

st.divider()
st.subheader("Activity Status Breakdown")
st.bar_chart(counts)

st.divider()
st.subheader("User Activity Table")

status_filter = st.selectbox("Filter by status", ["All", "Active", "At Risk", "Inactive", "Never Active"])
filtered = df if status_filter == "All" else df[df["status"] == status_filter]

display = filtered[["accountId", "username", "city", "lastReview", "lastSave", "totalReviews", "totalSaves", "status"]].copy()
display.columns = ["User ID", "Username", "City", "Last Review", "Last Save", "Reviews", "Saves", "Status"]
st.dataframe(display, use_container_width=True, hide_index=True)
