import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_post, api_put, api_delete, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("My Reviews")
st.write("Write, edit, or delete reviews for date spots you've visited.")

user_id = st.session_state.get("user_id", 1)

# ── My existing reviews ───────────────────────────────────────────────────────
st.subheader("My Past Reviews")

reviews, err = api_get(f"/users/{user_id}/reviews")
if err:
    show_api_error(err)
elif not reviews:
    st.info("You haven't written any reviews yet.")
else:
    df = pd.DataFrame(reviews)[["reviewId", "venueName", "rating", "comment", "createdAt"]]
    df.columns = ["Review ID", "Venue", "Rating", "Comment", "Date"]
    st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ── Write a new review ────────────────────────────────────────────────────────
st.subheader("Write a New Review")

with st.form("write_review_form"):
    venue_id = st.number_input("Venue ID", min_value=1, value=1, step=1)
    rating = st.slider("Rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
    comment = st.text_area("Comment", placeholder="Share your experience...")
    submitted = st.form_submit_button("Submit Review", type="primary")

if submitted:
    _, err = api_post(
        f"/venues/{int(venue_id)}/reviews",
        {"userId": user_id, "rating": rating, "comment": comment},
    )
    if err:
        show_api_error(err)
    else:
        st.success("Review submitted!")
        st.rerun()

st.divider()

# ── Edit a review ─────────────────────────────────────────────────────────────
with st.expander("Edit a Review"):
    with st.form("edit_review_form"):
        edit_id = st.number_input("Review ID to edit", min_value=1, value=1, step=1)
        new_rating = st.slider("New Rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
        new_comment = st.text_area("New Comment", placeholder="Updated thoughts...")
        edit_submitted = st.form_submit_button("Save Changes", type="primary")

    if edit_submitted:
        _, err = api_put(
            f"/reviews/{int(edit_id)}",
            {"rating": new_rating, "comment": new_comment},
        )
        if err:
            show_api_error(err)
        else:
            st.success("Review updated!")
            st.rerun()

# ── Delete a review ───────────────────────────────────────────────────────────
with st.expander("Delete a Review"):
    delete_id = st.number_input("Review ID to delete", min_value=1, value=1, step=1)
    if st.button("Delete Review", type="primary"):
        _, err = api_delete(f"/reviews/{int(delete_id)}")
        if err:
            show_api_error(err)
        else:
            st.success("Review deleted.")
            st.rerun()
