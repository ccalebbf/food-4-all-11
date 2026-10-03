import streamlit as st
import transaction
from db import load_db_data, get_db
from google_sheets import get_gspread_client, fetch_distribution_records, fetch_deletion_records


with st.expander("🔍 Live API & DB Diagnostics", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**1. Raw Google Sheets Data**")
        try:
            # Direct bypass test
            gc = get_gspread_client()
            sh = gc.open("Food Distribution Logging Form (Responses)")
            ws = sh.worksheet("Form Responses 2")
            records = ws.get_all_records(numericise_ignore=['all'])
            st.write(f"Total Rows in Sheet: `{len(records)}`")
            if records:
                st.write("Latest Row Timestamp:", records[-1].get('Timestamp'))
        except Exception as e:
            st.error(f"Gspread Error: {e}")

    with col2:
        st.markdown("**2. Raw ZODB Memory State**")
        try:
            db, connection = get_db()
            with connection as conn:
                conn.sync()
                root = conn.root()
                n = root.get('neighbourhood')
                if n and n.blocks:
                    block_0 = n.blocks[0]
                    st.write(f"Block `{block_0.block}` Total Distributions: `{len(block_0.distributions)}`")
                    st.write("Keys in ZODB:", list(block_0.distributions.keys())[-5:])
        except Exception as e:
            st.error(f"ZODB Read Error: {e}")
            
    if st.button("🚨 Force Trigger Sync"):
        # Run sync and rerun immediately
        data_to_db()
        st.rerun()