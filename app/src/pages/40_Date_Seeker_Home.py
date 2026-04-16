import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

first_name = st.session_state.get("first_name", "there")
st.title(f"Welcome, {first_name} (Date Seeker)")
st.write("This is the starter page for one user persona. Use the links for search and saved spots.")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Discover Venues", use_container_width=True, type="primary"):
        st.switch_page("pages/41_Discover_Venues.py")
with col2:
    if st.button("Saved Venues", use_container_width=True):
        st.switch_page("pages/42_Lists_and_Saves.py")
with col3:
    if st.button("My Reviews", use_container_width=True):
        st.switch_page("pages/43_My_Reviews.py")

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("Browse Reviews", use_container_width=True):
        st.switch_page("pages/44_Venue_Reviews.py")
with col5:
    if st.button("Visited Places", use_container_width=True):
        st.switch_page("pages/45_Visited_Places.py")
with col6:
    if st.button("Similar Venues", use_container_width=True):
        st.switch_page("pages/46_Similar_Venues.py")
