import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

first_name = st.session_state.get("first_name", "there")
st.title(f"Welcome, {first_name}")
st.write("Manage tickets, moderate users, review venue applications, and keep the platform clean.")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Manage Tickets", use_container_width=True, type="primary"):
        st.switch_page("pages/31_Manage_Tickets.py")
with col2:
    if st.button("Moderate Users", use_container_width=True):
        st.switch_page("pages/32_Moderate_Users.py")
with col3:
    if st.button("Venue Applications", use_container_width=True):
        st.switch_page("pages/33_Venue_Applications.py")

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("Duplicate Venues", use_container_width=True):
        st.switch_page("pages/34_Duplicate_Venues.py")
with col5:
    if st.button("Categories & Vibes", use_container_width=True):
        st.switch_page("pages/35_Admin_Categories_Vibes.py")
with col6:
    if st.button("Admin Log", use_container_width=True):
        st.switch_page("pages/36_Admin_Log.py")
