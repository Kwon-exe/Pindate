import streamlit as st
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=False)


def _parse_ts(dt_str):
    s = str(dt_str).replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        # Flask's default JSON provider emits HTTP-date: 'Sun, 20 Apr 2026 14:23:17 GMT'
        dt = parsedate_to_datetime(str(dt_str))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def time_ago(dt_str):
    if not dt_str:
        return ""
    try:
        dt = _parse_ts(dt_str)
        diff = datetime.now(timezone.utc) - dt
        d, secs = diff.days, diff.seconds
        if d >= 30:
            n = d // 30
            return f"{n} month{'s' if n > 1 else ''} ago"
        if d >= 1:
            return f"{d} day{'s' if d > 1 else ''} ago"
        if secs >= 3600:
            n = secs // 3600
            return f"{n} hour{'s' if n > 1 else ''} ago"
        n = max(1, secs // 60)
        return f"{n} minute{'s' if n > 1 else ''} ago"
    except Exception:
        return str(dt_str)[:10]


def stars_str(rating):
    r = int(round(rating or 0))
    return "★" * r + "☆" * (5 - r)


def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


# ── Guard: must have a selected venue ─────────────────────────────────────────
venue_id = st.session_state.get("selected_venue_id")
if not venue_id:
    st.info("No venue selected. Head back to Discover and pick one.")
    if st.button("← Back to Discover", type="primary"):
        st.switch_page("pages/41_Discover_Venues.py")
    st.stop()


# ── Back button ───────────────────────────────────────────────────────────────
if st.button("← Back"):
    st.switch_page("pages/41_Discover_Venues.py")


# ── Fetch data ────────────────────────────────────────────────────────────────
venue, v_err = api_get(f"/venues/{venue_id}")
if v_err:
    show_api_error(v_err)
    st.stop()
if not venue:
    st.error("Venue not found.")
    st.stop()

reviews, _ = api_get(f"/venues/{venue_id}/reviews")
posts,   _ = api_get(f"/venues/{venue_id}/posts")
reviews = reviews or []
posts   = posts   or []


# ── Header card ───────────────────────────────────────────────────────────────
rating    = safe_float(venue.get("avgReviewRating") or venue.get("rating")) or 0.0
price_min = safe_float(venue.get("minPrice"))
price_max = safe_float(venue.get("maxPrice"))
if price_min is not None and price_max is not None:
    price_str = f" · \\${int(price_min)}–\\${int(price_max)}"
elif price_min is not None:
    price_str = f" · From \\${int(price_min)}"
else:
    price_str = ""

with st.container(border=True):
    img_col, info_col = st.columns([1, 5])
    with img_col:
        st.markdown(
            """<div style="background:#e8e0f0;border-radius:12px;height:140px;
               display:flex;align-items:center;justify-content:center;font-size:3rem;">🏛️</div>""",
            unsafe_allow_html=True,
        )
    with info_col:
        st.markdown(f"## {venue.get('name', 'Venue')}")
        st.markdown(f"{stars_str(rating)} **{round(rating, 1)}**{price_str}")
        addr_parts = [venue.get("address"), venue.get("city")]
        addr = ", ".join(p for p in addr_parts if p)
        if addr:
            st.caption(f"📍 {addr}")
        if venue.get("phoneNum"):
            st.caption(f"📞 {venue['phoneNum']}")

        tags = []
        if venue.get("categories"):
            tags += [f"🏷 {c.strip()}" for c in venue["categories"].split(",")]
        if venue.get("vibes"):
            tags += [f"✨ {b.strip()}" for b in venue["vibes"].split(",")]
        if tags:
            st.markdown(" &nbsp; ".join([f"`{t}`" for t in tags]), unsafe_allow_html=True)


# ── Description ───────────────────────────────────────────────────────────────
if venue.get("description"):
    st.divider()
    st.subheader("About")
    st.write(venue["description"])


# ── Reviews ───────────────────────────────────────────────────────────────────
st.divider()
st.subheader(f"Reviews ({len(reviews)})")

if not reviews:
    st.info("No reviews yet. Be the first to leave one!")
else:
    for r in reviews:
        rev_rating = safe_float(r.get("rating")) or 0.0
        stars      = stars_str(rev_rating)
        username   = r.get("username") or "Anonymous"
        ago        = time_ago(r.get("createdAt"))
        is_flagged = bool(r.get("isFlagged"))

        with st.container(border=True):
            st.markdown(f"**{username}**")
            st.caption(f"{stars} {rev_rating:.0f}/5  ·  {ago}")
            if is_flagged:
                st.markdown("_[ Review hidden — inappropriate content ]_")
            else:
                st.write(r.get("comment") or "_No comment._")


# ── Owner posts ───────────────────────────────────────────────────────────────
st.divider()
st.subheader(f"Updates from the Venue ({len(posts)})")

if not posts:
    st.info("No posts yet.")
else:
    for p in posts:
        content_full = p.get("content", "")
        lines        = content_full.split("\n", 1)
        title        = lines[0][:80]
        body         = lines[1].strip() if len(lines) > 1 else content_full
        post_date    = str(p.get("postDate", ""))[:10]

        with st.container(border=True):
            st.markdown(f"**{title}**")
            if post_date:
                st.caption(f"Posted {post_date}")
            st.write(body)