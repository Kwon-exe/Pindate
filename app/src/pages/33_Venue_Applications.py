import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_put, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Venue Applications")
st.write("Review, approve, or reject venue submissions from owners.")

status_filter = st.selectbox("Filter by status", ["All", "PENDING", "APPROVED", "REJECTED"])
params = {}
if status_filter != "All":
    params["status"] = status_filter

apps, err = api_get("/applications", params=params)
if err:
    show_api_error(err)
    st.stop()

if not apps:
    st.info("No applications found.")
    st.stop()

df = pd.DataFrame(apps)[["applicationId", "ownerUsername", "name", "address", "status", "createdAt"]]
df.columns = ["App ID", "Owner", "Venue Name", "Address", "Status", "Submitted"]
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("View Application Details")

app_id = st.number_input("Application ID", min_value=1, value=1, step=1)
if st.button("Load Application"):
    app, a_err = api_get(f"/applications/{int(app_id)}")
    if a_err:
        show_api_error(a_err)
    elif app:
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Name:** {app.get('name')}")
                st.markdown(f"**Address:** {app.get('address')}")
                st.markdown(f"**Phone:** {app.get('phone') or '—'}")
                st.markdown(f"**Owner:** {app.get('ownerUsername', '—')}")
            with col2:
                st.markdown(f"**Price Range:** ${app.get('minPrice', 0):.0f} – ${app.get('maxPrice', 0):.0f}")
                st.markdown(f"**Status:** {app.get('status')}")
                st.markdown(f"**Submitted:** {str(app.get('createdAt',''))[:10]}")
            if app.get("description"):
                st.markdown(f"**Description:** {app['description']}")

st.divider()
st.subheader("Approve or Reject")

with st.form("review_app_form"):
    review_id  = st.number_input("Application ID to review", min_value=1, value=1, step=1)
    decision   = st.selectbox("Decision", ["APPROVED", "REJECTED", "PENDING"])
    review_sub = st.form_submit_button("Submit Decision", type="primary")

if review_sub:
    _, r_err = api_put(f"/applications/{int(review_id)}", {"status": decision})
    if r_err:
        show_api_error(r_err)
    else:
        st.success(f"Application {int(review_id)} marked as {decision}.")
        st.rerun()
