import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_put, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Manage Report Tickets")
st.write("Review and resolve tickets submitted by users and venue owners.")

STATUSES = ["PENDING", "UNDER REVIEW", "RESOLVED", "DISMISSED"]

status_filter = st.selectbox("Filter by status", ["All"] + STATUSES)
params = {}
if status_filter != "All":
    params["status"] = status_filter

tickets, err = api_get("/tickets", params=params)
if err:
    show_api_error(err)
    st.stop()

if not tickets:
    st.info("No tickets found.")
    st.stop()

df = pd.DataFrame(tickets)[["reportId", "reporterUsername", "reviewId", "reason", "status", "createdAt"]]
df.columns = ["Ticket ID", "Reporter", "Review ID", "Reason", "Status", "Created"]
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("View Ticket Details")

ticket_id = st.number_input("Ticket ID", min_value=1, value=1, step=1)
if st.button("Load Ticket"):
    ticket, t_err = api_get(f"/tickets/{int(ticket_id)}")
    if t_err:
        show_api_error(t_err)
    elif ticket:
        with st.container(border=True):
            st.markdown(f"**Reason:** {ticket.get('reason')}")
            st.markdown(f"**Status:** {ticket.get('status')}")
            st.markdown(f"**Description:** {ticket.get('description') or '—'}")
            st.markdown(f"**Review Comment:** {ticket.get('reviewComment') or '—'}")
            st.caption(f"Reported by: {ticket.get('reporterUsername', '—')} · {str(ticket.get('createdAt',''))[:10]}")

st.divider()
st.subheader("Update Ticket Status")

with st.form("update_ticket_form"):
    update_id     = st.number_input("Ticket ID to update", min_value=1, value=1, step=1)
    new_status    = st.selectbox("New Status", STATUSES)
    update_submit = st.form_submit_button("Update Ticket", type="primary")

if update_submit:
    _, u_err = api_put(f"/tickets/{int(update_id)}", {"status": new_status})
    if u_err:
        show_api_error(u_err)
    else:
        st.success(f"Ticket {int(update_id)} updated to {new_status}.")
        st.rerun()
