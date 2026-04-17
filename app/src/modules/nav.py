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
    st.sidebar.page_link("pages/45_Visited_Places.py", label="Visited Places", icon="📍")
    st.sidebar.page_link("pages/46_Similar_Venues.py", label="Similar Venues", icon="✨")


# ---- Role: venue owner ------------------------------------------------------

def venue_owner_home_nav():
    st.sidebar.page_link("pages/10_Marcus_Home.py", label="Venue Owner Home", icon="🏪")


def venue_owner_pages_nav():
    st.sidebar.page_link("pages/11_Manage_Venue.py", label="Manage My Venue", icon="✏️")
    st.sidebar.page_link("pages/12_Venue_Categorize.py", label="Categories & Vibes", icon="🏷️")
    st.sidebar.page_link("pages/13_Flag_Reviews.py", label="Flag & Report Reviews", icon="🚩")
    st.sidebar.page_link("pages/14_My_Venue_Reviews.py", label="My Venue Reviews", icon="💬")
    st.sidebar.page_link("pages/15_New_Application.py", label="Submit Application", icon="📋")
    st.sidebar.page_link("pages/16_Venue_Posts.py", label="Posts & Events", icon="📣")


# ---- Role: data analyst -----------------------------------------------------

def data_analyst_home_nav():
    st.sidebar.page_link("pages/20_Joey_Home.py", label="Analyst Home", icon="📊")


def data_analyst_pages_nav():
    st.sidebar.page_link("pages/21_User_Signups.py",    label="User Signups",    icon="📈")
    st.sidebar.page_link("pages/22_Venue_Dashboard.py", label="Venue Dashboard", icon="🏆")
    st.sidebar.page_link("pages/23_Coverage_Gaps.py",   label="Coverage Gaps",   icon="🗺️")
    st.sidebar.page_link("pages/24_Review_Volume.py",   label="Review Volume",   icon="🔍")
    st.sidebar.page_link("pages/25_User_Retention.py",  label="User Retention",  icon="👥")
    st.sidebar.page_link("pages/26_Summary_Report.py",  label="Summary Report",  icon="📋")


# ---- Role: admin ------------------------------------------------------------

def admin_home_nav():
    st.sidebar.page_link("pages/30_Josh_Home.py", label="Admin Home", icon="🛡️")


def admin_pages_nav():
    st.sidebar.page_link("pages/31_Manage_Tickets.py",          label="Manage Tickets",      icon="🎫")
    st.sidebar.page_link("pages/32_Moderate_Users.py",          label="Moderate Users",      icon="👤")
    st.sidebar.page_link("pages/33_Venue_Applications.py",      label="Venue Applications",  icon="📝")
    st.sidebar.page_link("pages/34_Duplicate_Venues.py",        label="Duplicate Venues",    icon="🔁")
    st.sidebar.page_link("pages/35_Admin_Categories_Vibes.py",  label="Categories & Vibes",  icon="🏷️")
    st.sidebar.page_link("pages/36_Admin_Log.py",               label="Admin Log",           icon="📜")


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
        elif role == "venue_owner":
            venue_owner_home_nav()
            venue_owner_pages_nav()
        elif role == "data_analyst":
            data_analyst_home_nav()
            data_analyst_pages_nav()
        elif role == "admin":
            admin_home_nav()
            admin_pages_nav()

    # About link appears at the bottom for all roles
    about_page_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
