# -- File with all things related to syncing data --

# Library Imports
import gspread
import streamlit as st
import transaction
from datetime import datetime, date
from ZODB import DB
from ZODB.FileStorage import FileStorage
from persistent.list import PersistentList

#Module Imports
# from models import Distribution, Block, Neighbourhood
from google_sheets import fetch_distribution_records, fetch_deletion_records

# Arguments: neighbourhood - name of neighbourhood, blocks - dictionary mapping block numbers to postal codes
def data_to_db(connection, neighbourhood, blocks):
    if connection is None:
        return

    db_root = connection.root()
    connection.sync()

    #if 'neighbourhood' not in db_root or db_root.get(neighbourhood) is None:
        # Make dictionary class


    n = db.root.get('neighbourhood')

    # Fetch deleted distributions first, sync them

    # Sync distributions, append those that have not been deleted