import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Venue Dashboard")
st.write("Explore the top-rated and most-saved venues. Filter by city or category.")

categories, c_err = api_get("/categories")
if c_err:
    categories = []

col1, col2 = st.columns(2)
with col1:
    city = st.text_input("Filter by city", placeholder="e.g. Boston")
with col2:
    cat_map = {"All": None}
    if categories:
        cat_map.update({c["name"]: c["categoryId"] for c in categories})
    selected_cat = st.selectbox("Filter by category", list(cat_map.keys()))

params = {}
if city.strip():
    params["city"] = city.strip()
if cat_map[selected_cat]:
    params["category_id"] = cat_map[selected_cat]

data, err = api_get("/analytics/venues/top", params=params)
if err:
    show_api_error(err)
    st.stop()

if not data:
    st.info("No venues found for the selected filters.")
    st.stop()

df = pd.DataFrame(data)

col1, col2, col3 = st.columns(3)
col1.metric("Venues Found", len(df))
col2.metric("Highest Avg Rating", f"{df['avgRating'].astype(float).max():.2f}")
col3.metric("Most Saves", int(df["totalSaves"].astype(int).max()))

st.divider()
st.subheader("Top Venues by Rating")
st.bar_chart(df.set_index("name")["avgRating"].astype(float).head(10))

st.divider()
st.subheader("Full Table")
display = df[["venueId", "name", "city", "avgRating", "totalReviews", "totalSaves"]].copy()
display.columns = ["Venue ID", "Name", "City", "Avg Rating", "Total Reviews", "Total Saves"]
st.dataframe(display, use_container_width=True, hide_index=True)
