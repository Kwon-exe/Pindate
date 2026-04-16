import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

first_name = st.session_state.get("first_name", "there")
st.title(f"Welcome, {first_name}")
st.write("Manage your venues, update your listings, and keep your customers informed.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("Manage My Venue", use_container_width=True, type="primary"):
        st.switch_page("pages/11_Manage_Venue.py")
with col2:
    if st.button("Categories & Vibes", use_container_width=True):
        st.switch_page("pages/12_Venue_Categorize.py")
