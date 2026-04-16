import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_post, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Search Venues")
st.write("Search a simple starter list of date spots by city and minimum rating.")

if "last_search" not in st.session_state:
    st.session_state.last_search = {"city": "Boston", "min_rating": 4.0}

with st.form("venue_search_form"):
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("City", value=st.session_state.last_search["city"])
    with col2:
        min_rating = st.slider(
            "Minimum rating",
            min_value=0.0,
            max_value=5.0,
            value=float(st.session_state.last_search["min_rating"]),
            step=0.1,
        )

    search_pressed = st.form_submit_button("Search Venues", type="primary")

if search_pressed:
    st.session_state.last_search = {"city": city, "min_rating": min_rating}

search_params = st.session_state.last_search
venues, err = api_get("/venues/search", params=search_params)
if err:
    show_api_error(err)
else:
    st.caption(f"Showing results for city={search_params['city']} and min_rating={search_params['min_rating']}")
    if not venues:
        st.info("No venues matched these filters.")
    else:
        st.dataframe(pd.DataFrame(venues), use_container_width=True)

st.subheader("Save a Venue")
user_id = 1
venue_id = st.number_input("Venue ID to save", min_value=1, value=1, step=1)
if st.button("Save Venue", type="primary"):
    _, save_err = api_post(f"/users/{user_id}/saved", {"venueId": int(venue_id)})
    if save_err:
        show_api_error(save_err)
    else:
        st.success("Venue saved.")
