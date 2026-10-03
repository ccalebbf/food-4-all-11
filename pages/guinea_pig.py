from google_sheets import get_gspread_client
     
gc = get_gspread_client


all_rows = fetch_distribution_records(gc)

for row in all_rows:

    blocks_covered = [int(x.strip()) for x in row["Blocks Covered"].split(",")]

    st.write(blocks_covered)