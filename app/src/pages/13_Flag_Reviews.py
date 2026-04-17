import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_post, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Flag & Report Reviews")
st.write("Flag inaccurate or inappropriate reviews on your venues and submit tickets for admin review.")

user_id = st.session_state.get("user_id", 4)

# ── Venue selector ────────────────────────────────────────────────────────────
my_venues, err = api_get(f"/users/{user_id}/venues")
if err:
    show_api_error(err)
    st.stop()

if not my_venues:
    st.info("You have no venues listed yet.")
    st.stop()

venue_options = {v["name"]: v["venueId"] for v in my_venues}
selected_name = st.selectbox("Select a venue", list(venue_options.keys()))
venue_id = venue_options[selected_name]

# ── Reviews for selected venue ────────────────────────────────────────────────
st.divider()
st.subheader(f"Reviews for {selected_name}")

reviews, rev_err = api_get(f"/venues/{venue_id}/reviews")
if rev_err:
    show_api_error(rev_err)
    st.stop()

if not reviews:
    st.info("No reviews yet for this venue.")
    st.stop()

df = pd.DataFrame(reviews)[["reviewId", "username", "rating", "comment", "isFlagged", "createdAt"]]
df.columns = ["Review ID", "User", "Rating", "Comment", "Flagged", "Date"]
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ── Flag a review ─────────────────────────────────────────────────────────────
st.subheader("Flag a Review")
st.caption("Marks the review for admin attention.")

with st.form("flag_form"):
    flag_id = st.number_input("Review ID to flag", min_value=1, value=1, step=1)
    flag_submitted = st.form_submit_button("Flag Review", type="primary")

if flag_submitted:
    _, flag_err = api_post(f"/reviews/{int(flag_id)}/flag", {})
    if flag_err:
        show_api_error(flag_err)
    else:
        st.success(f"Review {int(flag_id)} has been flagged.")
        st.rerun()

st.divider()

# ── Submit a report ticket ────────────────────────────────────────────────────
st.subheader("Submit a Report Ticket")
st.caption("Opens a formal ticket for the admin to investigate.")

REASONS = [
    "Inaccurate Review",
    "Inappropriate Content",
    "Spam",
    "Fake Review",
    "Harassment",
    "Other",
]

with st.form("ticket_form"):
    ticket_review_id = st.number_input("Review ID", min_value=1, value=1, step=1)
    reason = st.selectbox("Reason", REASONS)
    description = st.text_area("Description", placeholder="Describe why this review should be investigated...")
    ticket_submitted = st.form_submit_button("Submit Ticket", type="primary")

if ticket_submitted:
    if not description.strip():
        st.warning("Please add a description before submitting.")
    else:
        _, t_err = api_post("/tickets", {
            "reporterId": user_id,
            "reviewId": int(ticket_review_id),
            "reason": reason,
            "description": description.strip(),
        })
        if t_err:
            show_api_error(t_err)
        else:
            st.success("Report ticket submitted. The admin will review it shortly.")
