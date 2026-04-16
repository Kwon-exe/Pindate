import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_put, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Manage My Venue")
st.write("View and update your venue's details so customers always see accurate information.")

user_id = st.session_state.get("user_id", 4)

# ── My venues ─────────────────────────────────────────────────────────────────
my_venues, err = api_get(f"/users/{user_id}/venues")
if err:
    show_api_error(err)
    st.stop()

if not my_venues:
    st.info("You don't have any venues listed yet.")
    st.stop()

st.subheader("My Venues")
df = pd.DataFrame(my_venues)[["venueId", "name", "city", "address", "rating", "minPrice", "maxPrice"]]
df.columns = ["Venue ID", "Name", "City", "Address", "Rating", "Min Price", "Max Price"]
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ── Edit a venue ──────────────────────────────────────────────────────────────
st.subheader("Update Venue Details")

venue_options = {v["name"]: v for v in my_venues}
selected_name = st.selectbox("Select a venue to edit", list(venue_options.keys()))
venue = venue_options[selected_name]
venue_id = venue["venueId"]

with st.form("update_venue_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Name", value=venue.get("name", ""))
        new_address = st.text_input("Address", value=venue.get("address", ""))
        new_city = st.text_input("City", value=venue.get("city", ""))
        new_phone = st.text_input("Phone", value=venue.get("phoneNum") or "")
    with col2:
        new_min = st.number_input(
            "Min Price ($)", min_value=0.0, value=float(venue.get("minPrice") or 0), step=1.0
        )
        new_max = st.number_input(
            "Max Price ($)", min_value=0.0, value=float(venue.get("maxPrice") or 0), step=1.0
        )
        new_description = st.text_area(
            "Description", value=venue.get("description") or "", height=120
        )

    save = st.form_submit_button("Save Changes", type="primary")

if save:
    payload = {
        "name": new_name or None,
        "description": new_description or None,
        "address": new_address or None,
        "city": new_city or None,
        "phoneNum": new_phone or None,
        "minPrice": new_min if new_min > 0 else None,
        "maxPrice": new_max if new_max > 0 else None,
    }
    _, update_err = api_put(f"/venues/{venue_id}", payload)
    if update_err:
        show_api_error(update_err)
    else:
        st.success("Venue updated successfully!")
        st.rerun()
