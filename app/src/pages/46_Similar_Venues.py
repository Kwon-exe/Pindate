import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_post, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Discover Similar Venues")
st.write("Pick a spot you've saved and we'll find similar venues you haven't tried yet.")

user_id = st.session_state.get("user_id", 1)

# ── Saved venues ──────────────────────────────────────────────────────────────
st.subheader("Your Saved Venues")

saved, err = api_get(f"/users/{user_id}/saved")
if err:
    show_api_error(err)
    st.stop()

if not saved:
    st.info("You have no saved venues yet. Save some spots first to get recommendations.")
    st.stop()

df_saved = pd.DataFrame(saved)[["venueId", "name", "city", "rating"]]
df_saved.columns = ["Venue ID", "Name", "City", "Rating"]
st.dataframe(df_saved, use_container_width=True, hide_index=True)

st.divider()

# ── Similar venues ────────────────────────────────────────────────────────────
st.subheader("Find Similar Spots")

venue_id = st.number_input(
    "Enter a Venue ID from your saved list above",
    min_value=1,
    value=int(saved[0]["venueId"]) if saved else 1,
    step=1,
)
search = st.button("Find Similar Venues", type="primary")

if search or "similar_venue_id" in st.session_state:
    if search:
        st.session_state["similar_venue_id"] = int(venue_id)

    base_id = st.session_state["similar_venue_id"]
    base_name = next((v["name"] for v in saved if v["venueId"] == base_id), f"Venue {base_id}")

    similar, sim_err = api_get(f"/venues/{base_id}/similar")
    if sim_err:
        show_api_error(sim_err)
    elif not similar:
        st.info(f"No similar venues found for **{base_name}**.")
    else:
        st.write(f"Venues similar to **{base_name}**:")

        saved_ids = {v["venueId"] for v in saved}

        for v in similar:
            already_saved = v["venueId"] in saved_ids
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{v['name']}**")
                    st.caption(f"{v.get('city', '')} · {v.get('address', '')}")
                with col2:
                    rating = v.get("rating")
                    st.metric("Rating", f"{float(rating):.1f}" if rating else "N/A")
                with col3:
                    if already_saved:
                        st.success("Saved")
                    else:
                        if st.button("Save", key=f"save_{v['venueId']}"):
                            _, save_err = api_post(
                                f"/users/{user_id}/saved",
                                {"venueId": v["venueId"]},
                            )
                            if save_err:
                                show_api_error(save_err)
                            else:
                                st.success("Saved!")
                                st.rerun()
