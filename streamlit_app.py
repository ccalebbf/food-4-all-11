import streamlit as st
from google_sheets import fetch_distribution_records, fetch_deletion_records

deletion_records = fetch_deletion_records()
st.text(deletion_records)