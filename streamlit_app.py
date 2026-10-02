import streamlit as st
from google_sheets import fetch_distribution_records, fetch_deletion_records

from models import Distribution, Block, Neighbourhood

st.write(Distribution('Food United', '2026-07-26', 'Dry', 130, 'Yes'))

st.write(Block(160, 460999))