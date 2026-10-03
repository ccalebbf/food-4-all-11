# -- File with all things related to syncing data --

# Library Imports
import gspread
import streamlit as st
import transaction
import time
from datetime import datetime, date
from ZODB import DB
from ZODB.FileStorage import FileStorage
from persistent.list import PersistentList

#Module Imports
from db import get_db, load_db_data
from models import Distribution, Block, Neighbourhood
from google_sheets import get_gspread_client, fetch_distribution_records, fetch_deletion_records

# Arguments: neighbourhood - name of neighbourhood, blocks - dictionary mapping block numbers to postal codes
def data_to_db(connection, neighbourhood, blocks):
    if connection is None:
        return

    gc = get_gspread_client()
    db_root = connection.root()
    connection.sync()

    if 'neighbourhood' not in db_root or db_root.get(neighbourhood) is None:
        # Make dictionary class
        pg = Neighbourhood(neighbourhood, PersistentList(Block(key, blocks[key]) for key in blocks))
        db_root['neighbourhood'] = pg

        transaction.commit()
        #connection.transaction_manager.commit()
        connection.sync()

    n = db_root.get('neighbourhood')

    #for block in n.blocks:

        #fetch_deletion_records(gc, block, block.deleted_distributions)

        #time.sleep(1)

    try:
        all_rows = fetch_distribution_records(gc)
    except Exception as e:
        return

    for row in all_rows:

        blocks_covered = [int(x.strip()) for x in row["Blocks Covered"].split(",")]

        dist_id = datetime.strptime(row["Timestamp"], "%m/%d/%Y %H:%M:%S").strftime("%y%m%d%H%M%S")

        for block in n.blocks:

            if block.block in blocks_covered:

                existing_ids = PersistentList(d for d in block.distributions)

                if dist_id not in block.deleted_distributions and dist_id not in existing_ids:
                    new_dist = Distribution(row["Name of organisation"], 
                                            row["Date of distribution"], 
                                            row["Type of Food distributed"], 
                                            row["Number of people catered to (estimate)"], 
                                            row["Were the food distributed halal certified?"])
                    block.log_distribution(dist_id, new_dist)

    transaction.commit()
    #connection.transaction_manager.commit()
    connection.sync()