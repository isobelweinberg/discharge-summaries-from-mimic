import sqlite3
import pandas as pd
import os

def create_database(data_path: str, db_path: str):
    # Create a new SQLite database (or connect to an existing one)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # # Folder containing the CSV files
    # folder_path = 'data/mimic-iv-clinical-database-demo-2.2/hosp/'

    # Iterate over all files in the folder
    for filename in os.listdir(data_path):
        if filename.endswith('.csv'):
            # Load the CSV file into a DataFrame
            file_path = os.path.join(data_path, filename)
            df = pd.read_csv(file_path)
            
            # Create a table name based on the CSV file name (without extension)
            table_name = os.path.splitext(filename)[0]
            
            # Load the DataFrame into the SQLite database
            df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()