import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_post, api_delete, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Places I've Visited")
st.write("Track every spot you've been to so you never repeat a date by accident.")

user_id = st.session_state.get("user_id", 1)

# ── Visited venues list ───────────────────────────────────────────────────────
visited, err = api_get(f"/users/{user_id}/visited")
if err:
    show_api_error(err)
else:
    if not visited:
        st.info("You haven't marked any venues as visited yet.")
    else:
        st.subheader(f"Visited Spots ({len(visited)})")
        df = pd.DataFrame(visited)[["venueId", "name", "city", "address", "rating"]]
        df.columns = ["Venue ID", "Name", "City", "Address", "Rating"]
        st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ── Mark as visited ───────────────────────────────────────────────────────────
st.subheader("Mark a Venue as Visited")

with st.form("mark_visited_form"):
    venue_id = st.number_input("Venue ID", min_value=1, value=1, step=1)
    mark_submitted = st.form_submit_button("Mark as Visited", type="primary")

if mark_submitted:
    _, err = api_post(f"/users/{user_id}/visited", {"venueId": int(venue_id)})
    if err:
        show_api_error(err)
    else:
        st.success(f"Venue {int(venue_id)} marked as visited!")
        st.rerun()

st.divider()

# ── Remove from visited ───────────────────────────────────────────────────────
st.subheader("Remove a Venue from Visited")

remove_id = st.number_input("Venue ID to remove", min_value=1, value=1, step=1)
if st.button("Remove", type="primary"):
    _, err = api_delete(f"/users/{user_id}/visited", {"venueId": int(remove_id)})
    if err:
        show_api_error(err)
    else:
        st.success(f"Venue {int(remove_id)} removed from visited.")
        st.rerun()
