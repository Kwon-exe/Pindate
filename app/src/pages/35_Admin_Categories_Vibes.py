import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks
from modules.api_client import api_get, api_post, api_put, api_delete, show_api_error

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("Manage Categories & Vibes")
st.write("Add, rename, or remove the tags that help users discover date spots.")

categories, c_err = api_get("/categories")
vibes,      v_err = api_get("/vibes")

col1, col2 = st.columns(2)

# ── Categories ────────────────────────────────────────────────────────────────
with col1:
    st.subheader("Categories")
    if c_err:
        show_api_error(c_err)
    elif categories:
        df_c = pd.DataFrame(categories)
        df_c.columns = ["Category ID", "Name"]
        st.dataframe(df_c, use_container_width=True, hide_index=True)

    with st.form("add_category_form"):
        new_cat = st.text_input("New category name")
        if st.form_submit_button("Add Category", type="primary"):
            if not new_cat.strip():
                st.warning("Name is required.")
            else:
                _, err = api_post("/categories", {"name": new_cat.strip()})
                if err:
                    show_api_error(err)
                else:
                    st.success(f"Category '{new_cat}' added.")
                    st.rerun()

    with st.expander("Rename a Category"):
        with st.form("rename_category_form"):
            r_cat_id   = st.number_input("Category ID", min_value=1, value=1, step=1)
            r_cat_name = st.text_input("New name")
            if st.form_submit_button("Rename", type="primary"):
                _, err = api_put(f"/categories/{int(r_cat_id)}", {"name": r_cat_name.strip()})
                if err:
                    show_api_error(err)
                else:
                    st.success("Category renamed.")
                    st.rerun()

    with st.expander("Delete a Category"):
        with st.form("delete_category_form"):
            d_cat_id = st.number_input("Category ID to delete", min_value=1, value=1, step=1)
            if st.form_submit_button("Delete Category", type="primary"):
                _, err = api_delete(f"/categories/{int(d_cat_id)}")
                if err:
                    show_api_error(err)
                else:
                    st.success("Category deleted.")
                    st.rerun()

# ── Vibes ─────────────────────────────────────────────────────────────────────
with col2:
    st.subheader("Vibes")
    if v_err:
        show_api_error(v_err)
    elif vibes:
        df_v = pd.DataFrame(vibes)
        df_v.columns = ["Vibe ID", "Name"]
        st.dataframe(df_v, use_container_width=True, hide_index=True)

    with st.form("add_vibe_form"):
        new_vibe = st.text_input("New vibe name")
        if st.form_submit_button("Add Vibe", type="primary"):
            if not new_vibe.strip():
                st.warning("Name is required.")
            else:
                _, err = api_post("/vibes", {"name": new_vibe.strip()})
                if err:
                    show_api_error(err)
                else:
                    st.success(f"Vibe '{new_vibe}' added.")
                    st.rerun()

    with st.expander("Rename a Vibe"):
        with st.form("rename_vibe_form"):
            r_vibe_id   = st.number_input("Vibe ID", min_value=1, value=1, step=1)
            r_vibe_name = st.text_input("New name")
            if st.form_submit_button("Rename", type="primary"):
                _, err = api_put(f"/vibes/{int(r_vibe_id)}", {"name": r_vibe_name.strip()})
                if err:
                    show_api_error(err)
                else:
                    st.success("Vibe renamed.")
                    st.rerun()

    with st.expander("Delete a Vibe"):
        with st.form("delete_vibe_form"):
            d_vibe_id = st.number_input("Vibe ID to delete", min_value=1, value=1, step=1)
            if st.form_submit_button("Delete Vibe", type="primary"):
                _, err = api_delete(f"/vibes/{int(d_vibe_id)}")
                if err:
                    show_api_error(err)
                else:
                    st.success("Vibe deleted.")
                    st.rerun()
