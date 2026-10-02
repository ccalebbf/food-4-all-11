import streamlit as st
from google_sheets import fetch_distribution_records, fetch_deletion_records

distribution = fetch_deletion_records()
st.write(distribution)