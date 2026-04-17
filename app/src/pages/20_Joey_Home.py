import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

first_name = st.session_state.get("first_name", "there")
st.title(f"Welcome, {first_name}")
st.write("Explore platform data, track growth trends, and generate reports for the founding team.")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("User Signups", use_container_width=True, type="primary"):
        st.switch_page("pages/21_User_Signups.py")
with col2:
    if st.button("Venue Dashboard", use_container_width=True):
        st.switch_page("pages/22_Venue_Dashboard.py")
with col3:
    if st.button("Coverage Gaps", use_container_width=True):
        st.switch_page("pages/23_Coverage_Gaps.py")

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("Review Volume", use_container_width=True):
        st.switch_page("pages/24_Review_Volume.py")
with col5:
    if st.button("User Retention", use_container_width=True):
        st.switch_page("pages/25_User_Retention.py")
with col6:
    if st.button("Summary Report", use_container_width=True):
        st.switch_page("pages/26_Summary_Report.py")
