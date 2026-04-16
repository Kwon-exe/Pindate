import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")
st.title('PinDate')
st.write('### Find, Rate, and Share Your Next Date Spot')
st.write('##### Select a user to log in as:')

st.divider()

# Persona 1: Maya Chen (Regular User)
if st.button("Login as Maya Chen - Date Planner", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'date_planner'
    st.session_state['first_name'] = 'Maya'
    st.session_state['user_id'] = 1
    logger.info("Logging in as Date Planner: Maya Chen")
    st.switch_page('pages/40_Date_Seeker_Home.py')

# Persona 2: Marcus Rivera (Venue Owner)
if st.button("Login as Marcus Rivera - Venue Owner", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'venue_owner'
    st.session_state['first_name'] = 'Marcus'
    st.session_state['user_id'] = 4
    logger.info("Logging in as Venue Owner: Marcus Rivera")
    st.switch_page('pages/40_Date_Seeker_Home.py')

# Persona 3: Joey Maple (Data Analyst)
if st.button("Login as Joey Maple - Data Analyst", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'data_analyst'
    st.session_state['first_name'] = 'Joey'
    st.session_state['user_id'] = 9
    logger.info("Logging in as Data Analyst: Joey Maple")
    st.switch_page('pages/40_Date_Seeker_Home.py')

# Persona 4: Josh Doe (Platform Admin)
if st.button("Login as Josh Doe - Platform Admin", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'admin'
    st.session_state['first_name'] = 'Josh'
    st.session_state['user_id'] = 7
    logger.info("Logging in as Admin: Josh Doe")
    st.switch_page('pages/40_Date_Seeker_Home.py')
