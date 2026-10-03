# -- File that deals with all things related to collecting Google Sheet data -- 
import streamlit as st
import gspread
from gspread.utils import rowcol_to_a1

# Establish Connection with the Google Sheets
def get_gspread_client():
    if "gcp_service_account" in st.secrets:
        try:
            creds_dict = dict(st.secrets["gcp_service_account"])
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            return gspread.service_account_from_dict(creds_dict)
        except Exception as e:
            print(f"Failed to load, {e}")
    return gspread.service_account(filename = 'food_for_all.json')

# Helper to retrieve Distribution Data
@st.cache_data(ttl=60, show_spinner = False)
def fetch_distribution_records(_gc):
    spreadsheet = _gc.open("Food Distribution Logging Form (Responses)")
    distributions_records = spreadsheet.worksheet("Form Responses 2") 
    return distributions_records.get_all_records(numericise_ignore=['all'])

# Helper to retrieve deleted Distribution IDs (Failsafe for site reboots)
    # block - block to obtain deleted records for
    # del_dists - each block's unique PersistentList of deleted IDs
def fetch_deletion_records(gc, block, del_dists):
    spreadsheet = gc.open("Food Distribution Logging Form (Responses)")
    deletion_records = spreadsheet.worksheet("DeletedIDs") 

    header_cell = deletion_records.find(str(block), in_row = 1)

    if header_cell:
        
        col_values = deletion_records.col_values(header_cell.col)

        del_dists.extend([val for val in col_values[1:] if val.strip()])


# Helper to add deleted Distribution IDs to Google Sheet (Failsafe for site reboots)
    # block - block in which distribution is deleted
    # dist-id - id of deleted distribution
def add_deletion_records(block, dist_id):
    gc = get_gspread_client()
    spreadsheet = gc.open("Food Distribution Logging Form (Responses)")
    deletion_records = spreadsheet.worksheet("DeletedIDs") 

    deletion_values = deletion_records.get_all_values()

    header_row = deletion_values[0]

    try:
        index_with_block_0 = header_row.index(str(block))

        first_empty_row = None

        for row_index_0 in range(1, len(deletion_values)):

            row = deletion_values[row_index_0]

            if index_with_block_0 >= len(row) and row[index_w_block_0].strip():
                first_empty_row = row_index_0 + 1 # Converting row to 1-based index
                break
        
        if first_empty_row is None:
            first_empty_row = len(deletion_values) + 1

        #Converts 0-based indices to 1-based indices for gspread
        index_w_block_1 = index_w_block_0 + 1
        cell_address = rowcol_to_a1(first_empty_row, index_w_block_1)

        deletion_records.update_acell(cell_address, dist_id)
    except ValueError as e:
        print("Error: {e}")