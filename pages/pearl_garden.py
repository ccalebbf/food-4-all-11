# -- Page for Summarised Pearl Garden neighbourhood records --

import streamlit as st
from db import load_db_data

connection, db, neighbourhood = load_db_data()

if connection:
    try:
        connection.sync()
        neighbourhood = connection.root().get('neighbourhood', None)
    except Exception as e:
        st.warning(f"DB sync error: {e}")

if neighbourhood:

    st.title(f"Summary of {neighbourhood.name} Records")
    
    for block in neighbourhood.blocks:
        
        if block.latest_distribution is None:
            ld = "No Record"
            pd = 0
        else:
            ld = block.latest_distribution
            pd = len(block.distributions) - 1

        st.header(f"Block {block.block}")

        st.subheader("Latest Distribution 📦")

        st.text(f"{ld}")

        st.subheader("Days Since Latest Distribution 🗓️")

        st.text(f"{block.time_since_last_distribution()}")

        st.subheader("Number of Past Distributions 📖")

        st.text(f"{pd}")

if st.sidebar.button("🔄 Fetch Fresh Data"):
    st.cache_data.clear()
    st.sidebar.success("Cache cleared!")
    st.rerun()