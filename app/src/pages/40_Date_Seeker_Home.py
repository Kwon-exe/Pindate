import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

first_name = st.session_state.get("first_name", "there")
st.title(f"Welcome, {first_name} (Date Seeker)")
st.write("This is the starter page for one user persona. Use the links for search and saved spots.")

col1, col2 = st.columns(2)
with col1:
	if st.button("Search Venues", use_container_width=True, type="primary"):
		st.switch_page("pages/41_Discover_Venues.py")
with col2:
	if st.button("Saved Venues", use_container_width=True):
		st.switch_page("pages/42_Lists_and_Saves.py")
