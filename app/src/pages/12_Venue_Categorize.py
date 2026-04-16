import streamlit as st

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_put, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Categories & Vibes")
st.write("Tag your venue so date seekers can find you when searching by activity or atmosphere.")

user_id = st.session_state.get("user_id", 4)

# ── Load owner's venues, all categories, all vibes ────────────────────────────
my_venues, v_err = api_get(f"/users/{user_id}/venues")
all_categories, c_err = api_get("/categories")
all_vibes, vib_err = api_get("/vibes")

if v_err:
    show_api_error(v_err)
    st.stop()
if c_err:
    show_api_error(c_err)
    st.stop()
if vib_err:
    show_api_error(vib_err)
    st.stop()

if not my_venues:
    st.info("You don't have any venues listed yet.")
    st.stop()

# ── Venue selector ────────────────────────────────────────────────────────────
venue_options = {v["name"]: v for v in my_venues}
selected_name = st.selectbox("Select a venue", list(venue_options.keys()))
venue_id = venue_options[selected_name]["venueId"]

st.divider()

# ── Current tags ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    current_cats, cc_err = api_get(f"/venues/{venue_id}/categories")
    if cc_err:
        show_api_error(cc_err)
        current_cats = []

    st.subheader("Categories")
    cat_map = {c["name"]: c["categoryId"] for c in (all_categories or [])}
    current_cat_names = [c["name"] for c in (current_cats or [])]

    selected_cats = st.multiselect(
        "Select all that apply",
        options=list(cat_map.keys()),
        default=current_cat_names,
        key="cat_select",
    )

    if st.button("Save Categories", type="primary"):
        new_cat_ids = [cat_map[name] for name in selected_cats]
        _, err = api_put(f"/venues/{venue_id}/categories", {"categoryIds": new_cat_ids})
        if err:
            show_api_error(err)
        else:
            st.success("Categories updated!")
            st.rerun()

with col2:
    current_vibes, cv_err = api_get(f"/venues/{venue_id}/vibes")
    if cv_err:
        show_api_error(cv_err)
        current_vibes = []

    st.subheader("Vibes")
    vibe_map = {v["name"]: v["vibeId"] for v in (all_vibes or [])}
    current_vibe_names = [v["name"] for v in (current_vibes or [])]

    selected_vibes = st.multiselect(
        "Select all that apply",
        options=list(vibe_map.keys()),
        default=current_vibe_names,
        key="vibe_select",
    )

    if st.button("Save Vibes", type="primary"):
        new_vibe_ids = [vibe_map[name] for name in selected_vibes]
        _, err = api_put(f"/venues/{venue_id}/vibes", {"vibeIds": new_vibe_ids})
        if err:
            show_api_error(err)
        else:
            st.success("Vibes updated!")
            st.rerun()
