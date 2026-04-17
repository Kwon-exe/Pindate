import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks(show_home=False)

first_name = st.session_state.get("first_name", "there")
st.title(f"Welcome, {first_name}!")
st.write("Manage your venues, categorize your listing, and keep customers informed.")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✏️ My Venue", use_container_width=True, type="primary"):
        st.switch_page("pages/11_Manage_Venue.py")
with col2:
    if st.button("💬 Reviews & Reports", use_container_width=True, type="primary"):
        st.switch_page("pages/13_Flag_Reviews.py")
with col3:
    if st.button("📋 Submit Application", use_container_width=True, type="primary"):
        st.switch_page("pages/15_New_Application.py")
