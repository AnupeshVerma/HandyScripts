import psycopg2 as pg
import pandas as pd
import pandas.io.sql as psql


# Make connection with the local postgres database
conn = pg.connect("dbname=SuperMart_DB user=postgres password=postgres")

# Check for the records in the table 
cur = conn.cursor()
result = cur.execute("SELECT * FROM customer")
records = cur.fetchall()
print(records)


# Convert the table in to dataframe
query = "SELECT * FROM customer"
dataframe = psql.read_sql_query(query, conn)
print(dataframe)
