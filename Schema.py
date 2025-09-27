#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 22:09:52 2025

@author: angelinachen
"""
import snowflake.connector

# Connect to Snowflake
conn = snowflake.connector.connect(
    user="ACHEN374",
    password="SnowflakeTrial1",
    account="lphqjyd-tu39148",
    warehouse="COMPUTE_WH",
    database="SNOWFLAKE_LEARNING_DB",
    schema="PUBLIC"
)
cur = conn.cursor()

# Ensure the table exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS therapists (
        therapist_id       INT AUTOINCREMENT PRIMARY KEY,
        full_name          STRING NOT NULL,
        gender             STRING,
        specialization     STRING,
        therapy_types      ARRAY,
        trauma_focus       ARRAY,
        insurance_accepted ARRAY,
        session_cost       NUMBER(10,2),
        location_city      STRING,
        location_state     STRING,
        contact_email      STRING,
        contact_phone      STRING,
        license_number     STRING
    )
""")

# Insert a therapist
cur.execute("""
    INSERT INTO therapists 
    (full_name, gender, specialization, therapy_types, trauma_focus, insurance_accepted, session_cost, location_city, location_state, contact_email, contact_phone, license_number)
    SELECT
        'Dr. Jane Smith',
        'Female',
        'Clinical Psychology',
        ARRAY_CONSTRUCT('CBT','EMDR'),
        ARRAY_CONSTRUCT('PTSD','Grief'),
        ARRAY_CONSTRUCT('BlueCross','SunLife'),
        150.00,
        'Toronto',
        'ON',
        'jane.smith@example.com',
        '555-123-4567',
        'PSY12345'
""")

# Query therapists
cur.execute("SELECT full_name, therapy_types, session_cost FROM therapists")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()


    