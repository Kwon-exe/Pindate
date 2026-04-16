import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Browse Venue Reviews")
st.write("Read dating-relevant reviews and see what a spot is really like before you go.")

# ── Venue selector ────────────────────────────────────────────────────────────
venue_id = st.number_input("Enter a Venue ID", min_value=1, value=1, step=1)
load = st.button("Load Venue", type="primary")

if load or "loaded_venue_id" in st.session_state:
    if load:
        st.session_state["loaded_venue_id"] = int(venue_id)

    vid = st.session_state["loaded_venue_id"]

    # ── Venue details ─────────────────────────────────────────────────────────
    venue, err = api_get(f"/venues/{vid}")
    if err:
        show_api_error(err)
        st.stop()

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(venue.get("name", "Unknown Venue"))
        st.caption(f"{venue.get('address', '')} · {venue.get('city', '')}")
        if venue.get("description"):
            st.write(venue["description"])

    with col2:
        avg = venue.get("avgReviewRating") or venue.get("rating")
        if avg:
            st.metric("Avg Rating", f"{float(avg):.1f} / 5.0")
        min_p = venue.get("minPrice")
        max_p = venue.get("maxPrice")
        if min_p and max_p:
            st.metric("Price Range", f"${float(min_p):.0f} – ${float(max_p):.0f}")

    # Date-relevant tags (vibes + categories)
    vibes = venue.get("vibes")
    categories = venue.get("categories")

    if vibes:
        st.markdown("**Vibes:** " + "  ".join(
            f"`{v.strip()}`" for v in vibes.split(",")
        ))
    if categories:
        st.markdown("**Categories:** " + "  ".join(
            f"`{c.strip()}`" for c in categories.split(",")
        ))

    st.divider()

    # ── Reviews ───────────────────────────────────────────────────────────────
    st.subheader("What People Are Saying")

    reviews, rev_err = api_get(f"/venues/{vid}/reviews")
    if rev_err:
        show_api_error(rev_err)
    elif not reviews:
        st.info("No reviews yet for this venue.")
    else:
        for r in reviews:
            rating = float(r.get("rating", 0))
            stars = "⭐" * round(rating)
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{r.get('username', 'Anonymous')}** {stars}")
                    st.write(r.get("comment") or "_No comment left._")
                with c2:
                    st.metric("Rating", f"{rating:.1f}")
                    st.caption(str(r.get("createdAt", ""))[:10])

    st.divider()

    # ── Venue posts / events ──────────────────────────────────────────────────
    st.subheader("Upcoming Events & Updates")

    posts, post_err = api_get(f"/venues/{vid}/posts")
    if post_err:
        show_api_error(post_err)
    elif not posts:
        st.info("No events or updates posted for this venue.")
    else:
        for p in posts:
            with st.container(border=True):
                st.write(p.get("content", ""))
                st.caption(f"Posted by {p.get('ownerUsername', 'owner')} · {str(p.get('postDate', ''))[:10]}")
