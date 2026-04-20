# Persona: Maya Chen (CUSTOMER)
# Maya-1: Search & filter venues by name, city, category, vibe, price  [Discover tab]
# Maya-2: Save venues to personal lists                                  [My Lists > Saved tab]
# Maya-5: Mark venues as visited / unmark                               [My Lists > Visited tab]
# Maya-6: Find similar venues based on a saved spot                     [My Lists > Similar Venues tab]
import streamlit as st

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_post, api_delete, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=False)

user_id = st.session_state.get("user_id", 1)

if "save_msgs" not in st.session_state:
    st.session_state.save_msgs = {}
if "list_msgs" not in st.session_state:
    st.session_state.list_msgs = {}
if "active_vibes" not in st.session_state:
    st.session_state.active_vibes = set()

# Fetch the user's custom lists once per render — needed by every venue card's
# "Save to list" popover as well as the My Lists tab.
# The backend auto-creates a reserved Lists row named 'Visited' to back the
# Visited bucket — hide it so it doesn't show up as a duplicate custom tab.
RESERVED_LIST_NAMES = {"Visited"}
user_lists, _ = api_get(f"/users/{user_id}/lists")
user_lists = [l for l in (user_lists or []) if l.get("name") not in RESERVED_LIST_NAMES]


@st.dialog("Create New List")
def create_list_dialog():
    with st.form("new_list_form", clear_on_submit=True):
        title = st.text_input("Title *", max_chars=255)
        description = st.text_area("Description (optional)")
        c1, c2 = st.columns(2)
        with c1:
            submitted = st.form_submit_button("Save", type="primary", use_container_width=True)
        with c2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)
    if submitted:
        if not title.strip():
            st.error("Title is required.")
            return
        if title.strip() in RESERVED_LIST_NAMES:
            st.error(f"'{title.strip()}' is a reserved name. Pick another.")
            return
        _, err = api_post(f"/users/{user_id}/lists", {
            "name": title.strip(),
            "description": description.strip() or None,
        })
        if err:
            show_api_error(err)
        else:
            st.rerun()
    if cancelled:
        st.rerun()


def save_to_list_popover(vid, key_prefix):
    """Save-to-list dropdown: 'Saved' default bucket + every custom list."""
    save_key = f"{key_prefix}_{vid}"
    with st.popover("🔖 Save to list", use_container_width=True):
        if st.button("🔖 Saved (default)", key=f"{save_key}_savedflat", use_container_width=True):
            _, err = api_post(f"/users/{user_id}/saved", {"venueId": vid})
            if err:
                if "Duplicate" in err or "1062" in err:
                    st.session_state.save_msgs[save_key] = ("info", "Already in Saved!")
                else:
                    st.session_state.save_msgs[save_key] = ("error", err)
            else:
                st.session_state.save_msgs[save_key] = ("success", "Saved!")
            st.rerun()
        if user_lists:
            st.divider()
            for lst in user_lists:
                if st.button(
                    f"📁 {lst['name']}",
                    key=f"{save_key}_addto_{lst['listId']}",
                    use_container_width=True,
                ):
                    _, err = api_post(f"/lists/{lst['listId']}/venues", {"venueId": vid})
                    if err:
                        if "409" in err or "Duplicate" in err or "1062" in err or "already" in err.lower():
                            st.session_state.save_msgs[save_key] = ("info", f"Already in {lst['name']}!")
                        else:
                            st.session_state.save_msgs[save_key] = ("error", err)
                    else:
                        st.session_state.save_msgs[save_key] = ("success", f"Added to {lst['name']}!")
                    st.rerun()
        else:
            st.caption("No custom lists yet. Create one from **My Lists**.")
    msg = st.session_state.save_msgs.get(save_key)
    if msg:
        if msg[0] == "success":
            st.success(msg[1])
        elif msg[0] == "info":
            st.info(msg[1])
        else:
            st.error(msg[1])

st.title("Venues")

# Left-align the text inside venue-name buttons (wrapped in st.container(key="venue-name-btn-*"))
st.markdown(
    """
    <style>
    div[class*="st-key-venue-name-btn-"] button p {
        font-weight: 700 !important;
        font-size: 1.15rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load Saved/Visited once so both the My Lists and Similar Venues tabs can use them.
saved, saved_err = api_get(f"/users/{user_id}/saved")
visited, visited_err = api_get(f"/users/{user_id}/visited")
saved = saved or []
visited = visited or []

tab_discover, tab_lists, tab_similar = st.tabs(["🔍 Discover", "🔖 My Lists", "✨ Similar Venues"])


# ── Helpers ───────────────────────────────────────────────────────────────────
def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def stars_str(rating):
    r = int(round(rating))
    return "★" * r + "☆" * (5 - r)

def venue_card(v, key_prefix):
    vid = v["venueId"]
    rating = safe_float(v.get("rating")) or 0.0
    price_min = safe_float(v.get("minPrice"))
    price_max = safe_float(v.get("maxPrice"))
    price_str = ""
    if price_min is not None and price_max is not None:
        price_str = f" · \\${int(price_min)}–\\${int(price_max)}"
    elif price_min is not None:
        price_str = f" · From \\${int(price_min)}"

    with st.container(border=True):
        left, right = st.columns([4, 1])
        with left:
            img_col, info_col = st.columns([1, 3])
            with img_col:
                st.markdown(
                    """<div style="background:#e8e0f0;border-radius:12px;height:110px;
                       display:flex;align-items:center;justify-content:center;font-size:2rem;">🏛️</div>""",
                    unsafe_allow_html=True,
                )
            with info_col:
                with st.container(key=f"venue-name-btn-{key_prefix}-{vid}"):
                    if st.button(v["name"], key=f"{key_prefix}_open_{vid}"):
                        st.session_state["selected_venue_id"] = vid
                        st.switch_page("pages/42_Venue_Details.py")
                st.markdown(f"{stars_str(rating)} **{round(rating, 1)}**{price_str}")
                st.caption(f"📍 {v.get('city', '')}  {v.get('address', '')}")
                if v.get("description"):
                    desc = v["description"]
                    st.write(desc[:160] + ("…" if len(desc) > 160 else ""))
                tags = []
                if v.get("categories"):
                    tags += [f"🏷 {c.strip()}" for c in v["categories"].split(",")]
                if v.get("vibes"):
                    tags += [f"✨ {b.strip()}" for b in v["vibes"].split(",")]
                if tags:
                    st.markdown(" &nbsp; ".join([f"`{t}`" for t in tags]), unsafe_allow_html=True)
        with right:
            st.markdown("<br>", unsafe_allow_html=True)
            save_to_list_popover(vid, key_prefix)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DISCOVER
# ══════════════════════════════════════════════════════════════════════════════
with tab_discover:
    st.caption("Find your next perfect date spot")

    search_q = st.text_input("", placeholder="Search restaurants, bars, parks...", label_visibility="collapsed", key="dv_search")

    VIBE_LABELS = ["Romantic", "Cozy", "Adventurous", "Casual", "Fancy"]
    vibes_data, _ = api_get("/vibes")
    vibe_map = {v["name"]: v["vibeId"] for v in vibes_data} if vibes_data else {}

    st.markdown("**Vibe**")
    vibe_cols = st.columns(len(VIBE_LABELS))
    for i, label in enumerate(VIBE_LABELS):
        with vibe_cols[i]:
            active = label in st.session_state.active_vibes
            if st.button(label, key=f"vibe_{label}", type="primary" if active else "secondary", use_container_width=True):
                st.session_state.active_vibes = set() if active else {label}
                st.rerun()

    f1, f2, f3 = st.columns(3)
    with f1:
        price_range = st.selectbox("Price Range", ["Any", "$", "$$", "$$$", "$$$$"])
    with f2:
        cats_data, _ = api_get("/categories")
        cat_map = {}
        cat_options = ["Any"]
        if cats_data:
            cat_map = {c["name"]: c["categoryId"] for c in cats_data}
            cat_options += list(cat_map.keys())
        date_type = st.selectbox("Date Type", cat_options)
    with f3:
        city_filter = st.text_input("City", placeholder="e.g. Boston", key="dv_city")

    params = {}
    if search_q.strip():
        params["q"] = search_q.strip()
    if city_filter.strip():
        params["city"] = city_filter.strip()
    if date_type != "Any":
        params["category_id"] = cat_map.get(date_type)
    if st.session_state.active_vibes:
        chosen_vibe = next(iter(st.session_state.active_vibes))
        if chosen_vibe in vibe_map:
            params["vibe_id"] = vibe_map[chosen_vibe]
    if price_range != "Any":
        params["max_price"] = {"$": 25, "$$": 50, "$$$": 75, "$$$$": 999}[price_range]

    st.divider()

    if params:
        # Active search — show filtered results
        venues, err = api_get("/venues/search", params=params)
        if err:
            show_api_error(err)
            st.stop()
        st.markdown(f"**{len(venues) if venues else 0} venues found**")
        if not venues:
            st.info("No venues match your filters. Try broadening your search.")
        else:
            for v in venues:
                venue_card(v, "search")
    else:
        # No filters — show community picks as default
        st.markdown("### 🌟 Community Picks")
        st.caption("Top-rated spots across all PinDate users — search or filter above to find your own")
        top, _ = api_get("/venues/search", params={"min_rating": 4.5})
        if top:
            for v in top:
                venue_card(v, "comm")
        else:
            st.info("No top-rated venues yet.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MY LISTS
# ══════════════════════════════════════════════════════════════════════════════
with tab_lists:
    cnl_col, _ = st.columns([1, 5])
    with cnl_col:
        if st.button("➕ Create New List", type="primary", use_container_width=True):
            create_list_dialog()

    tab_labels = [
        f"🔖 Saved ({len(saved)})",
        f"📍 Visited ({len(visited)})",
    ] + [f"📁 {lst['name']}" for lst in user_lists]

    sub_tabs      = st.tabs(tab_labels)
    sub_saved     = sub_tabs[0]
    sub_visited   = sub_tabs[1]
    sub_customs   = sub_tabs[2:]

    # ── Saved ──────────────────────────────────────────────────────────────────
    with sub_saved:
        if saved_err:
            show_api_error(saved_err)
        elif not saved:
            st.info("You haven't saved any venues yet. Use Discover to find some!")
        else:
            for v in saved:
                vid = v["venueId"]
                rating = safe_float(v.get("rating")) or 0.0

                with st.container(border=True):
                    top_left, top_right = st.columns([5, 1])
                    with top_left:
                        img_col, info_col = st.columns([1, 4])
                        with img_col:
                            st.markdown(
                                """<div style="background:#e8e0f0;border-radius:12px;height:90px;
                                   display:flex;align-items:center;justify-content:center;font-size:2rem;">🏛️</div>""",
                                unsafe_allow_html=True,
                            )
                        with info_col:
                            with st.container(key=f"venue-name-btn-saved-{vid}"):
                                if st.button(v["name"], key=f"saved_open_{vid}"):
                                    st.session_state["selected_venue_id"] = vid
                                    st.switch_page("pages/42_Venue_Details.py")
                            st.markdown(f"{stars_str(rating)} **{round(rating, 1)}**")
                            st.caption(f"📍 {v.get('city', '')}  {v.get('address', '')}")
                            saved_at = str(v.get("savedAt", ""))[:10]
                            if saved_at:
                                st.caption(f"Saved on {saved_at}")
                    with top_right:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("✅ Visited", key=f"vis_{vid}", use_container_width=True):
                            _, v_err = api_post(f"/users/{user_id}/visited", {"venueId": vid})
                            if v_err and "Duplicate" not in v_err and "1062" not in v_err:
                                st.session_state.list_msgs[f"vis_{vid}"] = ("error", v_err)
                            else:
                                st.session_state.list_msgs[f"vis_{vid}"] = ("success", "Marked visited!")
                            st.rerun()
                        if st.button("🗑 Remove", key=f"unsave_{vid}", use_container_width=True):
                            _, d_err = api_delete(f"/users/{user_id}/saved", {"venueId": vid})
                            if d_err:
                                st.session_state.list_msgs[f"unsave_{vid}"] = ("error", d_err)
                            else:
                                st.session_state.list_msgs[f"unsave_{vid}"] = ("success", "Removed!")
                            st.rerun()
                        for key in [f"vis_{vid}", f"unsave_{vid}"]:
                            msg = st.session_state.list_msgs.get(key)
                            if msg:
                                if msg[0] == "success":
                                    st.success(msg[1])
                                else:
                                    st.error(msg[1])

                    with st.expander("📝 My Notes"):
                        note_key = f"note_{vid}"
                        note_text = st.text_area(
                            "Note",
                            value=st.session_state.get(note_key, ""),
                            key=f"note_input_{vid}",
                            placeholder="e.g. Great for anniversaries, ask for the corner table",
                            label_visibility="collapsed",
                        )
                        if st.button("Save Note", key=f"save_note_{vid}"):
                            st.session_state[note_key] = note_text
                            st.success("Note saved!")

    # ── Visited ────────────────────────────────────────────────────────────────
    with sub_visited:
        if visited_err:
            show_api_error(visited_err)
        elif not visited:
            st.info("You haven't marked any venues as visited yet.")
        else:
            for v in visited:
                vid = v["venueId"]
                rating = safe_float(v.get("rating")) or 0.0

                with st.container(border=True):
                    img_col, info_col, action_col = st.columns([1, 4, 1])
                    with img_col:
                        st.markdown(
                            """<div style="background:#d0f0e8;border-radius:12px;height:90px;
                               display:flex;align-items:center;justify-content:center;font-size:2rem;">✅</div>""",
                            unsafe_allow_html=True,
                        )
                    with info_col:
                        with st.container(key=f"venue-name-btn-visited-{vid}"):
                            if st.button(v["name"], key=f"visited_open_{vid}"):
                                st.session_state["selected_venue_id"] = vid
                                st.switch_page("pages/42_Venue_Details.py")
                        st.markdown(f"{stars_str(rating)} **{round(rating, 1)}**")
                        st.caption(f"📍 {v.get('city', '')}  {v.get('address', '')}")
                    with action_col:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("↩ Unmark", key=f"unvis_{vid}", use_container_width=True):
                            _, uv_err = api_delete(f"/users/{user_id}/visited", {"venueId": vid})
                            if uv_err:
                                st.session_state.list_msgs[f"unvis_{vid}"] = ("error", uv_err)
                            else:
                                st.session_state.list_msgs[f"unvis_{vid}"] = ("success", "Unmarked!")
                            st.rerun()
                        msg = st.session_state.list_msgs.get(f"unvis_{vid}")
                        if msg:
                            if msg[0] == "success":
                                st.success(msg[1])
                            else:
                                st.error(msg[1])

    # ── Custom lists ───────────────────────────────────────────────────────────
    for lst, tab in zip(user_lists, sub_customs):
        list_id = lst["listId"]
        with tab:
            hdr_left, hdr_right = st.columns([5, 1])
            with hdr_left:
                st.markdown(f"### 📁 {lst['name']}")
            with hdr_right:
                dl_key = f"dellist_{list_id}"
                if st.button("🗑 Delete list", key=dl_key, use_container_width=True):
                    _, dl_err = api_delete(f"/lists/{list_id}")
                    if dl_err:
                        st.session_state.list_msgs[dl_key] = ("error", dl_err)
                    else:
                        st.session_state.list_msgs[dl_key] = ("success", "List deleted!")
                    st.rerun()
                msg = st.session_state.list_msgs.get(dl_key)
                if msg:
                    if msg[0] == "success":
                        st.success(msg[1])
                    else:
                        st.error(msg[1])

            if lst.get("description"):
                st.markdown(f"_{lst['description']}_")

            list_venues, lv_err = api_get(f"/lists/{list_id}")
            if lv_err:
                show_api_error(lv_err)
                continue
            list_venues = list_venues or []

            if not list_venues:
                st.info("No venues in this list yet. Use the Discover tab to add some.")
                continue

            for v in list_venues:
                vid = v["venueId"]
                rating = safe_float(v.get("rating")) or 0.0
                with st.container(border=True):
                    img_col, info_col, action_col = st.columns([1, 4, 1])
                    with img_col:
                        st.markdown(
                            """<div style="background:#e8e0f0;border-radius:12px;height:90px;
                               display:flex;align-items:center;justify-content:center;font-size:2rem;">🏛️</div>""",
                            unsafe_allow_html=True,
                        )
                    with info_col:
                        with st.container(key=f"venue-name-btn-list-{list_id}-{vid}"):
                            if st.button(v["name"], key=f"list_{list_id}_open_{vid}"):
                                st.session_state["selected_venue_id"] = vid
                                st.switch_page("pages/42_Venue_Details.py")
                        st.markdown(f"{stars_str(rating)} **{round(rating, 1)}**")
                        st.caption(f"📍 {v.get('city', '')}  {v.get('address', '')}")
                    with action_col:
                        st.markdown("<br>", unsafe_allow_html=True)
                        vis_key = f"lvis_{list_id}_{vid}"
                        if st.button("✅ Visited", key=vis_key, use_container_width=True):
                            _, vis_err = api_post(f"/users/{user_id}/visited", {"venueId": vid})
                            if vis_err and "Duplicate" not in vis_err and "1062" not in vis_err:
                                st.session_state.list_msgs[vis_key] = ("error", vis_err)
                            else:
                                st.session_state.list_msgs[vis_key] = ("success", "Marked visited!")
                            st.rerun()
                        rm_key = f"rmlist_{list_id}_{vid}"
                        if st.button("🗑 Remove", key=rm_key, use_container_width=True):
                            _, rm_err = api_delete(f"/lists/{list_id}/venues", {"venueId": vid})
                            if rm_err:
                                st.session_state.list_msgs[rm_key] = ("error", rm_err)
                            else:
                                st.session_state.list_msgs[rm_key] = ("success", "Removed!")
                            st.rerun()
                        for k in (vis_key, rm_key):
                            msg = st.session_state.list_msgs.get(k)
                            if msg:
                                if msg[0] == "success":
                                    st.success(msg[1])
                                else:
                                    st.error(msg[1])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SIMILAR VENUES
# ══════════════════════════════════════════════════════════════════════════════
with tab_similar:
    st.caption("Pick one of your saved spots and we'll find similar venues.")
    if not saved:
        st.info("Save some venues first to get recommendations.")
    else:
        sim_options = {f"{v['name']} ({v.get('city', '')})": v["venueId"] for v in saved}
        sim_selected = st.selectbox("Base your recommendations on:", list(sim_options.keys()), key="sim_select")
        base_id = sim_options[sim_selected]

        similar, sim_err = api_get(f"/venues/{base_id}/similar")
        if sim_err:
            show_api_error(sim_err)
        elif not similar:
            st.info(f"No similar venues found for **{sim_selected}**.")
        else:
            st.markdown(f"**Venues similar to {sim_selected}:**")
            for v in similar:
                vid = v["venueId"]
                rating = safe_float(v.get("rating")) or 0.0
                with st.container(border=True):
                    c1, c2 = st.columns([5, 1])
                    with c1:
                        with st.container(key=f"venue-name-btn-sim-{vid}"):
                            if st.button(v["name"], key=f"sim_open_{vid}"):
                                st.session_state["selected_venue_id"] = vid
                                st.switch_page("pages/42_Venue_Details.py")
                        st.markdown(f"{stars_str(rating)} **{round(rating, 1)}**")
                        st.caption(f"📍 {v.get('city', '')}  {v.get('address', '')}")
                    with c2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        save_to_list_popover(vid, "sim")
