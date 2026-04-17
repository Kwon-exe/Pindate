import streamlit as st

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Platform Summary Report")
st.write("A snapshot of key platform statistics for the founding team.")

data, err = api_get("/analytics/summary")
if err:
    show_api_error(err)
    st.stop()

if not data:
    st.info("No summary data available.")
    st.stop()

st.divider()
st.subheader("Platform Health")

col1, col2, col3 = st.columns(3)
col1.metric("Total Users",    data.get("totalUsers", 0))
col2.metric("Total Venues",   data.get("totalVenues", 0))
col3.metric("Total Reviews",  data.get("totalReviews", 0))

col4, col5, col6 = st.columns(3)
col4.metric("Platform Avg Rating", f"{float(data.get('platformAvgRating') or 0):.2f}")
col5.metric("Total Saves",         data.get("totalSaves", 0))
col6.metric("Total Customers",     data.get("totalCustomers", 0))

st.divider()
st.subheader("Pending Actions")

col7, col8, col9 = st.columns(3)
col7.metric("Pending Applications", data.get("pendingApplications", 0))
col8.metric("Pending Tickets",      data.get("pendingTickets", 0))
col9.metric("Venue Owners",         data.get("totalOwners", 0))

st.divider()
st.info("This report reflects live data from the PinDate database. Share with the founding team for business decisions.")
