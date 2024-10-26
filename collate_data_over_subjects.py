# Iterate over patients and generate output files
import sqlite3
import os

def create_model_inputs(db_path: str, output_dir: str):

    headings = get_table_headings(db_path)
    tables_with_subj_id_in = [a for a in headings if 'subject_id' in headings[a]]

    conn = sqlite3.connect(db_path)
    cursor=conn.cursor()
    cursor2=conn.cursor()
    cursor.execute('SELECT subject_id FROM patients')

    for patient in cursor:
        for t in tables_with_subj_id_in:
            cursor2.execute(f'SELECT * FROM {t} WHERE subject_id = ?', (patient[0],))

            # output_dir = 'data/mimic-iv-clinical-database-demo-2.2/subject-data'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Write output
            with open(os.path.join(output_dir, f'{patient[0]}.txt'), 'a') as f:
                for row in cursor2.fetchall():
                    f.write(str(row) + '\n')

    conn.close()

def get_table_headings(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get the list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
  
    table_headings = {}
    
    # Iterate through the tables and get the headings
    for table in tables:
        table_name = table[0]
        # cursor.execute(f"PRAGMA table_info({table_name});")
        # columns = cursor.fetchall()
        # headings = [column[1] for column in columns]
        cursor = conn.execute('select * from ' + table_name)
        headings = [description[0] for description in cursor.description]
        table_headings[table_name] = headings
    
    # Close the connection
    conn.close()
    
    return table_headings