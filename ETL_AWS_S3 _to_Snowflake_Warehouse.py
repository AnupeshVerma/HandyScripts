# pip install snowflake-connector-python

import pandas as pd
import snowflake.connector as sf
import boto3
from snowflake.connector.pandas_tools import write_pandas
 
 # Configuration for S3 bucket
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='',
    aws_secret_access_key=''
)
 
 # Extract the content of the S3 buckets into a list
df_list = []
for obj in s3.Bucket('demo-bucket-2025-04-25').objects.all():
    df_list.append(pd.read_csv(obj.get()['Body']))
 
print(df_list)
employees_df = df_list[1]
 
 # Extract and apply transformations on the extracted data
employees_df[['dept_no', 'emp_no', 'hire_date', 'leaving_date']] = employees_df[['dept_no', 'emp_no', 'hire_date', 'leaving_date']].astype('string')
employees_df.columns = employees_df.columns.str.upper()
employees_df.dtypes
 

 # Configuration for snowflake
user="AnupeshMNNIT"
password=""
account="pvlrzux-tt91304"
database="demo_s3"
warehouse="COMPUTE_WH"
schema="public"
role="ACCOUNTADMIN"
 
 # Make a connection to snowflake
try:
    conn=sf.connect(user=user,password=password,account=account)
except Exception as e:
    print(e)
 
def run_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
 
 
statement_1='USE WAREHOUSE ' + warehouse
statement3="USE DATABASE " + database
statement4="USE ROLE" + role
run_query(conn,statement_1)
run_query(conn,statement3)
run_query(conn,statement4)
 
 # Write content to snowflake table using Pandas (Keep table name capital)
try:
    write_pandas(conn, employees_df, 'EMPLOYEES')
except Exception as e:
    print(e)
