import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About")

st.markdown(
    """
    Welcome to PinDate, the data-driven date discovery platform!

    PinDate is a platform built for people who are tired of sifting through generic reviews
    just to find somewhere worth going on a Friday night. Whether you're planning a first date, an anniversary dinner,
    or just a casual night out, PinDate helps you search by vibe, save spots to a personal wishlist, and get recommendations
    powered by a community that actually cares about the experience. Venue owners can claim and manage their listings to reach
    the right audience, while behind the scenes, real usage data drives smarter recommendations and surfaces what's trending
    in your area.

    Date night, sorted. That's PinDate!
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")



    
