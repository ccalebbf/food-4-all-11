# -- Page for Individual Block Records --

import streamlit as st
import transaction
from db import load_db_data
from sync import data_to_db
from google_sheets import get_gspread_client, fetch_distribution_records, fetch_deletion_records

connection, db, neighbourhood = load_db_data()

if connection:
    try:
        data_to_db(connection)
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

st.title("Records of Individual Block")

tab_labels = [f"Block {block.block}" for block in neighbourhood.blocks]

tabs = st.tabs(tab_labels)

for tab, block in zip(tabs, neighbourhood.blocks):

    with tab:

        if neighbourhood:

            sorted_distributions = dict(sorted(block.distributions.items(), key = lambda item: item[1].date))

            st.header(f"Block {block.block}")
            
            block_data = {
                "Distribution ID" : [key for key in sorted_distributions],
                "Date" : [value.date for value in sorted_distributions.values()],
                "Organisation" : [value.org for value in sorted_distributions.values()],
                "Type" : [value.type for value in sorted_distributions.values()],
                "Number of People (Approx.)" : [value.pax for value in sorted_distributions.values()],
                "Halal-Certified" : [value.isHalal for value in sorted_distributions.values()]
            }

            st.table(block_data, border="horizontal")

if st.sidebar.button("🔄 Fetch Fresh Data"):
    st.cache_data.clear()
    st.sidebar.success("Cache cleared!")
    st.rerun()