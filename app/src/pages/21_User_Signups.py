import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("User Signups Over Time")
st.write("Track new user registrations and identify growth trends.")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", value=None)
with col2:
    end_date = st.date_input("End date", value=None)

params = {}
if start_date:
    params["start"] = str(start_date)
if end_date:
    params["end"] = str(end_date)

data, err = api_get("/analytics/signups", params=params)
if err:
    show_api_error(err)
    st.stop()

if not data:
    st.info("No signup data found for the selected range.")
    st.stop()

df = pd.DataFrame(data)
df["signupDate"] = pd.to_datetime(df["signupDate"])
df["newSignups"] = df["newSignups"].astype(int)

col1, col2, col3 = st.columns(3)
col1.metric("Total Signups", int(df["newSignups"].sum()))
col2.metric("Days with Signups", len(df))
col3.metric("Peak Day", int(df["newSignups"].max()))

st.divider()
st.subheader("Daily Signups")
st.line_chart(df.set_index("signupDate")["newSignups"])

st.divider()
st.subheader("Raw Data")
df.columns = ["Date", "New Signups"]
st.dataframe(df, use_container_width=True, hide_index=True)
