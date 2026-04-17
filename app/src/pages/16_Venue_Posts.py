import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_post, api_put, api_delete, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Venue Posts & Events")
st.write("Keep your customers informed with updates, specials, and upcoming events.")

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

# ── Existing posts ────────────────────────────────────────────────────────────
st.divider()
st.subheader(f"Posts for {selected_name}")

posts, post_err = api_get(f"/venues/{venue_id}/posts")
if post_err:
    show_api_error(post_err)
elif not posts:
    st.info("No posts yet for this venue.")
else:
    for p in posts:
        with st.container(border=True):
            st.write(p.get("content", ""))
            st.caption(f"Post ID: {p['postId']} · {str(p.get('postDate', ''))[:10]}")

st.divider()

# ── Create a new post ─────────────────────────────────────────────────────────
st.subheader("Create a New Post")

with st.form("create_post_form"):
    content = st.text_area("Content", placeholder="e.g. Wine tasting this Friday — 20% off all bottles!")
    create_submitted = st.form_submit_button("Post Update", type="primary")

if create_submitted:
    if not content.strip():
        st.warning("Post content cannot be empty.")
    else:
        _, c_err = api_post(f"/venues/{venue_id}/posts", {
            "ownerId": user_id,
            "content": content.strip(),
        })
        if c_err:
            show_api_error(c_err)
        else:
            st.success("Post published!")
            st.rerun()

st.divider()

# ── Edit a post ───────────────────────────────────────────────────────────────
with st.expander("Edit a Post"):
    with st.form("edit_post_form"):
        edit_id = st.number_input("Post ID to edit", min_value=1, value=1, step=1)
        new_content = st.text_area("New content", placeholder="Updated announcement...")
        edit_submitted = st.form_submit_button("Save Changes", type="primary")

    if edit_submitted:
        if not new_content.strip():
            st.warning("Content cannot be empty.")
        else:
            _, e_err = api_put(f"/posts/{int(edit_id)}", {"content": new_content.strip()})
            if e_err:
                show_api_error(e_err)
            else:
                st.success("Post updated!")
                st.rerun()

# ── Delete a post ─────────────────────────────────────────────────────────────
with st.expander("Delete a Post"):
    delete_id = st.number_input("Post ID to delete", min_value=1, value=1, step=1)
    if st.button("Delete Post", type="primary"):
        _, d_err = api_delete(f"/posts/{int(delete_id)}")
        if d_err:
            show_api_error(d_err)
        else:
            st.success("Post deleted.")
            st.rerun()
