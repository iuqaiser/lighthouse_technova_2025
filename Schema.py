#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 22:09:52 2025

@author: angelinachen
"""

from snowflake.connector import connect
import pandas as pd
import os
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

# Step 1: Connect
conn = connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
cur = conn.cursor()

# Step 2: Create table (modify columns as needed)
cur.execute("""
CREATE OR REPLACE TABLE providers (
    id INT,
    provider_role STRING,
    first_name STRING,
    last_name STRING,
    gender_identity STRING,
    insurance STRING,
    hourly_rate FLOAT,
    session_options STRING,
    specialized_support STRING,
    services_offered STRING,
    registration_number STRING,
    email STRING,
    address STRING
)
""")

# Step 3: Read CSV file into Pandas
df = pd.read_csv("providers.csv")
df['id'] = range(1, len(df) + 1)
df = df[['id'] + [col for col in df.columns if col != 'id']]
df.columns = [c.upper() for c in df.columns]

# Step 4: Insert rows into Snowflake
write_pandas(conn, df, 'PROVIDERS')
print("✅ Data loaded from CSV into Snowflake!")

cur.close()
conn.close()


