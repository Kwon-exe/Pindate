import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_delete, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Saved Venues")
st.caption("Template page using mock userId=1.")

user_id = 1

saved, err = api_get(f"/users/{user_id}/saved")
if err:
    show_api_error(err)
else:
    st.dataframe(pd.DataFrame(saved), use_container_width=True)

st.subheader("Remove a Saved Venue")
venue_to_remove = st.number_input("Venue ID to remove", min_value=1, value=1, step=1)
if st.button("Remove Venue", type="primary"):
    _, del_err = api_delete(f"/users/{user_id}/saved", {"venueId": int(venue_to_remove)})
    if del_err:
        show_api_error(del_err)
    else:
        st.success("Saved venue removed.")
