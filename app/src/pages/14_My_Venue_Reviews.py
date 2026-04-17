import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("My Venue Reviews")
st.write("Read customer feedback across all your venues to understand what's working and what isn't.")

user_id = st.session_state.get("user_id", 4)

# ── Load owner's venues ───────────────────────────────────────────────────────
my_venues, err = api_get(f"/users/{user_id}/venues")
if err:
    show_api_error(err)
    st.stop()

if not my_venues:
    st.info("You have no venues listed yet.")
    st.stop()

# ── Venue selector ────────────────────────────────────────────────────────────
venue_options = {v["name"]: v for v in my_venues}
selected_name = st.selectbox("Select a venue", list(venue_options.keys()))
venue = venue_options[selected_name]
venue_id = venue["venueId"]

# ── Venue summary ─────────────────────────────────────────────────────────────
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Overall Rating", f"{float(venue.get('rating') or 0):.1f} / 5.0")
with col2:
    st.metric("Price Range", f"${float(venue.get('minPrice') or 0):.0f} – ${float(venue.get('maxPrice') or 0):.0f}")
with col3:
    st.metric("City", venue.get("city", "—"))

# ── Reviews ───────────────────────────────────────────────────────────────────
st.divider()
st.subheader(f"Customer Reviews for {selected_name}")

reviews, rev_err = api_get(f"/venues/{venue_id}/reviews")
if rev_err:
    show_api_error(rev_err)
    st.stop()

if not reviews:
    st.info("No reviews yet for this venue.")
    st.stop()

# Summary stats
df = pd.DataFrame(reviews)
avg = df["rating"].astype(float).mean()
flagged_count = int(df["isFlagged"].sum())
total = len(df)

m1, m2, m3 = st.columns(3)
m1.metric("Total Reviews", total)
m2.metric("Average Rating", f"{avg:.2f}")
m3.metric("Flagged Reviews", flagged_count)

st.divider()

# Rating filter
min_r, max_r = st.slider(
    "Filter by rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1
)
show_flagged = st.checkbox("Show flagged reviews only")

filtered = [
    r for r in reviews
    if min_r <= float(r["rating"]) <= max_r
    and (not show_flagged or r["isFlagged"])
]

if not filtered:
    st.info("No reviews match the current filters.")
else:
    for r in filtered:
        rating = float(r.get("rating", 0))
        stars = "⭐" * round(rating)
        flagged_badge = " 🚩 *Flagged*" if r.get("isFlagged") else ""
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{r.get('username', 'Anonymous')}**{flagged_badge}  {stars}")
                st.write(r.get("comment") or "_No comment left._")
            with c2:
                st.metric("Rating", f"{rating:.1f}")
                st.caption(str(r.get("createdAt", ""))[:10])
