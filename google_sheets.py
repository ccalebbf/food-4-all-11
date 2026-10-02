# -- File that deals with all things related to collecting Google Sheet data -- 
import gspread
import streamlit as st

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
@st.cache_data(ttl=300, show_spinner = False)
def fetch_distribution_records():
    gc = get_gspread_client()
    spreadsheet = gc.open("Food Distribution Logging Form (Responses)")
    distributions_records = spreadsheet.worksheet("Form Responses 2") 
    return distributions_records.get_all_records(numericise_ignore=['all'])

# Helper to retrieve deleted Distribution IDs (Failsafe for site reboots)
@st.cache_data(ttl=300, show_spinner = False)
def fetch_deletion_records():
    gc = get_gspread_client()
    spreadsheet = gc.open("Food Distribution Logging Form (Responses)")
    deletion_records = spreadsheet.worksheet("DeletedIDs") 
    return deletion_records.get_all_records(numericise_ignore=['all'])