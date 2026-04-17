import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_delete, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Duplicate Venue Detection")
st.write("Find venue listings that share the same name and remove confirmed duplicates.")

dupes, err = api_get("/venues/duplicates")
if err:
    show_api_error(err)
    st.stop()

if not dupes:
    st.success("No duplicate venue names detected.")
    st.stop()

df = pd.DataFrame(dupes)
dupe_names = df["name"].unique()

st.warning(f"**{len(dupe_names)} venue name(s)** appear more than once across {len(df)} listings.")

for name in dupe_names:
    group = df[df["name"] == name][["venueId", "name", "city", "address", "rating", "ownerId"]]
    group.columns = ["Venue ID", "Name", "City", "Address", "Rating", "Owner ID"]
    with st.expander(f"**{name}** — {len(group)} listings"):
        st.dataframe(group, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Delete a Duplicate Venue")
st.caption("Permanently removes a venue listing by ID.")

with st.form("delete_venue_form"):
    del_id     = st.number_input("Venue ID to delete", min_value=1, value=1, step=1)
    confirm    = st.checkbox("I confirm this venue is a duplicate and should be removed")
    del_submit = st.form_submit_button("Delete Venue", type="primary")

if del_submit:
    if not confirm:
        st.warning("Please confirm before deleting.")
    else:
        _, d_err = api_delete(f"/venues/{int(del_id)}")
        if d_err:
            show_api_error(d_err)
        else:
            st.success(f"Venue {int(del_id)} deleted.")
            st.rerun()
