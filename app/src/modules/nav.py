# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has functions to add links to the left sidebar based on the user's role.

import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def about_page_nav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


# ---- Role: date seeker ------------------------------------------------------

def date_seeker_home_nav():
    st.sidebar.page_link(
        "pages/40_Date_Seeker_Home.py", label="Date Seeker Home", icon="💖"
    )


def date_seeker_pages_nav():
    st.sidebar.page_link("pages/41_Discover_Venues.py", label="Discover Venues", icon="🔍")
    st.sidebar.page_link("pages/42_Lists_and_Saves.py", label="Saved Venues", icon="🔖")
    st.sidebar.page_link("pages/43_My_Reviews.py", label="My Reviews", icon="⭐")
    st.sidebar.page_link("pages/44_Venue_Reviews.py", label="Browse Reviews", icon="💬")


# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    """
    Renders sidebar navigation links based on the logged-in user's role.
    The role is stored in st.session_state when the user logs in on Home.py.
    """

    # Show title in sidebar for a simple but clear project identity.
    st.sidebar.markdown("## PinDate")

    # If no one is logged in, send them to the Home (login) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:
        role = st.session_state.get("role")
        if role in ("date_planner", "date_seeker"):
            date_seeker_home_nav()
            date_seeker_pages_nav()

    # About link appears at the bottom for all roles
    about_page_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
