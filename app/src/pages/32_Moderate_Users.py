import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_delete, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Moderate Users")
st.write("Identify users with flagged reviews and take action to keep the platform safe.")

users, err = api_get("/users")
if err:
    show_api_error(err)
    st.stop()

if not users:
    st.info("No users found.")
    st.stop()

df = pd.DataFrame(users)[["accountId", "username", "email", "city", "role", "createdAt"]]
df.columns = ["User ID", "Username", "Email", "City", "Role", "Joined"]
st.subheader("All Users")
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Flagged Review Activity")
st.caption("Enter a User ID to see their flagged reviews.")

check_id = st.number_input("User ID", min_value=1, value=1, step=1)
if st.button("Check Flagged Reviews"):
    flagged, f_err = api_get(f"/users/{int(check_id)}/flagged-reviews")
    if f_err:
        show_api_error(f_err)
    elif not flagged:
        st.success("No flagged reviews for this user.")
    else:
        st.warning(f"{len(flagged)} flagged review(s) found.")
        fdf = pd.DataFrame(flagged)[["reviewId", "venueName", "rating", "comment", "createdAt"]]
        fdf.columns = ["Review ID", "Venue", "Rating", "Comment", "Date"]
        st.dataframe(fdf, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Ban a User")
st.caption("This permanently deletes the user account.")

with st.form("ban_user_form"):
    ban_id     = st.number_input("User ID to ban", min_value=1, value=1, step=1)
    confirm    = st.checkbox("I confirm I want to permanently ban this user")
    ban_submit = st.form_submit_button("Ban User", type="primary")

if ban_submit:
    if not confirm:
        st.warning("Please confirm before banning.")
    else:
        _, b_err = api_delete(f"/users/{int(ban_id)}")
        if b_err:
            show_api_error(b_err)
        else:
            st.success(f"User {int(ban_id)} has been banned and removed.")
            st.rerun()
