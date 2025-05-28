import pandas as pd
import json
import glob
import os
import re

SRC_BASE_DIR = 'data/'

os.environ.update({'DATABASE_URL' : 'postgresql://postgres:postgres@localhost:5432/itversity_retail_db'})

def get_column_names(schemas, table_name, sorting_key = 'column_position'):
    # Retrieved columns are in the form of a dict
    columns_details = schemas[table_name]
    columns = sorted(columns_details, key=lambda x: x[sorting_key])
    return [col['column_name'] for col in columns]


def read_csv(file, schemas):
    file_path_list = re.split('[/\\\]', file)
    table_name = file_path_list[-2]
    columns = get_column_names(schemas, table_name)
    df_reader = pd.read_csv(file, names=columns, chunksize=10000)
    return df_reader


def to_sql(df, db_conn_url, table_name):
    df.to_sql(
        table_name,
        db_conn_url,
        if_exists='append',
        index=False
    )


def db_loader(SRC_BASE_DIR, db_conn_url, table_name):
    schemas = json.load(open(f"{SRC_BASE_DIR}/schemas.json"))
    files = glob.glob(f"{SRC_BASE_DIR}/{table_name}/*")
    if(len(files) == 0):
        raise ValueError(f"No files found for dataset {table_name} in {SRC_BASE_DIR}")
    
    for file in files:
        df_reader = read_csv(file, schemas)
        for idx, df in enumerate(df_reader):
            to_sql(df, db_conn_url, table_name)
            print(f"Processed chunk {idx + 1} from file {file}")


def process_files(table_names = None):
    db_conn_uri = os.environ.get('DATABASE_URL')
    schemas = json.load(open(f"{SRC_BASE_DIR}/schemas.json"))
    
    # If no specific tables are provided, process all tables in schemas
    if table_names is None:
        table_names = schemas.keys()

    for table_name in table_names:
        print(f"Processing table: {table_name}")
        try:
            db_loader(SRC_BASE_DIR, db_conn_uri, table_name)
        except Exception as e:
            print(f"Error processing {table_name}: {e}")


if __name__ == "__main__":
    process_files(['orders'])
