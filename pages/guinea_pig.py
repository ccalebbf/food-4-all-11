import streamlit as st
import transaction
from db import load_db_data
from google_sheets import get_gspread_client, fetch_distribution_records, fetch_deletion_records

connection, db, neighbourhood = load_db_data()

if connection:
    try:
        connection.sync()
        neighbourhood = connection.root().get('neighbourhood', None)
    except Exception as e:
        st.warning(f"DB sync error: {e}")

if neighbourhood is None or not hasattr(neighbourhood, 'blocks'):
    st.warning("Synchronizing database connection...")
    if connection:
        connection.sync()
    st.rerun()
    st.stop()

for block in neighbourhood.blocks:
    for distribution in block.distributions:
        st.write(distribution)