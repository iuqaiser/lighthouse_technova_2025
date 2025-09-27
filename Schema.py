#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 22:09:52 2025

@author: angelinachen
"""
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cur = conn.cursor()

# Create table
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

# Insert multiple rows using INSERT ... SELECT
cur.execute("""
INSERT INTO therapists
(full_name, gender, specialization, therapy_types, trauma_focus, insurance_accepted,
 session_cost, location_city, location_state, contact_email, contact_phone, license_number)
SELECT 'Dr. Jane Smith', 'Female', 'Clinical Psychology',
       ARRAY_CONSTRUCT('CBT','EMDR'), ARRAY_CONSTRUCT('PTSD','Grief'), ARRAY_CONSTRUCT('BlueCross','SunLife'),
       150.00, 'Toronto', 'ON', 'jane.smith@example.com', '555-123-4567', 'PSY12345'
UNION ALL
SELECT 'Dr. Mark Lee', 'Male', 'Counseling Psychology',
       ARRAY_CONSTRUCT('DBT','Mindfulness'), ARRAY_CONSTRUCT('Depression','Anxiety'), ARRAY_CONSTRUCT('Manulife','GreenShield'),
       120.00, 'Vancouver', 'BC', 'mark.lee@example.com', '555-987-6543', 'PSY67890'
UNION ALL
SELECT 'Dr. Aisha Patel', 'Female', 'Marriage & Family Therapy',
       ARRAY_CONSTRUCT('Gottman','CBT'), ARRAY_CONSTRUCT('Relationship Issues','Family Conflict'), ARRAY_CONSTRUCT('SunLife','BlueCross'),
       140.00, 'Calgary', 'AB', 'aisha.patel@example.com', '555-333-2222', 'MFT11223'
UNION ALL
SELECT 'Dr. Carlos Gomez', 'Male', 'Clinical Social Work',
       ARRAY_CONSTRUCT('Trauma Therapy','Narrative Therapy'), ARRAY_CONSTRUCT('Abuse','Grief','PTSD'), ARRAY_CONSTRUCT('Aetna','SunLife'),
       110.00, 'Montreal', 'QC', 'carlos.gomez@example.com', '555-444-9999', 'SW99887'
UNION ALL
SELECT 'Dr. Emily Wong', 'Non-binary', 'Child Psychology',
       ARRAY_CONSTRUCT('Play Therapy','CBT'), ARRAY_CONSTRUCT('ADHD','Behavioral Issues'), ARRAY_CONSTRUCT('BlueCross','GreenShield'),
       130.00, 'Ottawa', 'ON', 'emily.wong@example.com', '555-111-2222', 'PSY44556'
""")

# Commit
conn.commit()

# Query and print
cur.execute("SELECT full_name, therapy_types, trauma_focus, session_cost FROM therapists")
for row in cur.fetchall():
    name, therapy_arr, trauma_arr, cost = row
    print(name, therapy_arr, trauma_arr, cost)

cur.close()
conn.close()
