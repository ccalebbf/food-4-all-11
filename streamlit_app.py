import streamlit as st
from db import load_db_data
from sync import data_to_db
from streamlit_autorefresh import st_autorefresh

count = st_autorefresh(interval=30000, key="datarefresh")

pearl_garden = {98: 460098, 99: 460099, 
                100: 460100, 101: 460101, 
                102: 460102, 103: 460103, 
                104: 460104, 105: 460105, 
                106: 460106}

st.set_page_config(page_title="Food Distribution Database", layout="wide")

connection, db, neighbourhood = load_db_data()

if connection:
    try:
        data_to_db(connection, 'Pearl Garden', pearl_garden)
    except Exception as e:
        st.error(f"Sync failed on startup: {e}")

    connection.sync()
    neighbourhood = connection.root().get('neighbourhood', None)

# -- Define Pages --
home_page = st.Page("pages/home.py", title = "Home", icon = '🏠', default = True)
pg_page = st.Page("pages/pearl_garden.py", title = "Pearl Garden Neighbourhood Records", icon = '🏘️')
indi_page = st.Page("pages/block_records.py", title = "Individual Block Records", icon = "🏡")
g_pig = st.Page("pages/guinea_pig.py", title = "Print Debugging Purposes", icon = "🧪")

## -- Page Navigator --
nav = st.navigation([home_page, pg_page, indi_page, g_pig])
nav.run()