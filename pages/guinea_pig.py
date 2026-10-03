from google_sheets import get_gspread_client, fetch_distribution_records
import streamlit as st
     
gc = get_gspread_client


all_rows = fetch_distribution_records(gc)

for row in all_rows:

    blocks_covered = [int(x.strip()) for x in row["Blocks Covered"].split(",")]

    st.write(blocks_covered)