# -- File that deals with all things related to accessing database -- 
import streamlit as st
import transaction
from ZODB import DB
from ZODB.FileStorage import FileStorage

#@st.cache_resource
def get_db():
    try:
        storage = FileStorage('Data.fs')
        db = DB(storage)
        connection = db.open()
        return db, connection
    except Exception as e:
        st.error(f"Failed to access Data.fs: {e}")
        return None, None

def load_db_data():
    db, connection = get_db()
    if connection is None:
        return None, None, None
    
    connection.sync()
    
    try:
        db_root = connection.root()
        neighbourhood = db_root.get('neighbourhood', None)
        return connection, db, neighbourhood
    except Exception as e:
        st.error(f"Error reading database: {e}")
        return connection, db, None