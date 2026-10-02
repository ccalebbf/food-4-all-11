# -- File with all things related to syncing data --

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