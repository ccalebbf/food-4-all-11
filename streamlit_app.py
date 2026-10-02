import streamlit as st
from google_sheets import fetch_distribution_records, fetch_deletion_records

distributions = fetch_deletion_records()
st.write(distributions)