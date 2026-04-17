import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Admin Action Log")
st.write("Track every admin action taken on the platform for accountability and traceability.")

logs, err = api_get("/log")
if err:
    show_api_error(err)
    st.stop()

if not logs:
    st.info("No admin actions logged yet.")
    st.stop()

df = pd.DataFrame(logs)

col1, col2 = st.columns(2)
col1.metric("Total Actions Logged", len(df))
col2.metric("Admins Active", df["adminId"].nunique())

st.divider()

action_filter = st.selectbox(
    "Filter by action type",
    ["All"] + sorted(df["action"].unique().tolist()),
)

filtered = df if action_filter == "All" else df[df["action"] == action_filter]

display = filtered[["logId", "adminName", "action", "targetTable", "targetId", "performedAt", "notes"]].copy()
display.columns = ["Log ID", "Admin", "Action", "Target Table", "Target ID", "Performed At", "Notes"]
st.dataframe(display, use_container_width=True, hide_index=True)

st.divider()
st.subheader("View Log Entry Details")

log_id = st.number_input("Log ID", min_value=1, value=1, step=1)
if st.button("Load Entry"):
    entry, l_err = api_get(f"/log/{int(log_id)}")
    if l_err:
        show_api_error(l_err)
    elif entry:
        with st.container(border=True):
            st.markdown(f"**Admin:** {entry.get('adminName')}")
            st.markdown(f"**Action:** {entry.get('action')}")
            st.markdown(f"**Target:** {entry.get('targetTable')} ID {entry.get('targetId')}")
            st.markdown(f"**Notes:** {entry.get('notes') or '—'}")
            st.caption(f"Performed at: {str(entry.get('performedAt',''))[:19]}")
