#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 22:09:52 2025

@author: angelinachen
"""
# Schema.py
import snowflake.connector

def get_connection():
    """
    Returns a Snowflake connection object.
    """
    return snowflake.connector.connect(
        user="ACHEN374",
        password="SnowflakeTrial1",
        account="lphqjyd-tu39148",
        warehouse="COMPUTE_WH",
        database="SNOWFLAKE_LEARNING_DB",
        schema="PUBLIC"
    )

def insert_sample_providers():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO providers
        (name, genders, specialties, therapy_types, focus_tags, insurances, price_min, price_max, city, province, contact_email, contact_phone, license_number)
        SELECT
            'Test Provider',
            ARRAY_CONSTRUCT('Female'),
            ARRAY_CONSTRUCT('CBT'),
            ARRAY_CONSTRUCT('Individual'),
            ARRAY_CONSTRUCT('PTSD'),
            ARRAY_CONSTRUCT('BlueCross'),
            100,
            100,
            'Toronto',
            'ON',
            'test@example.com',
            '555-000-0000',
            'LIC12345'
        """)
        conn.commit()
    finally:
        cur.close()
        conn.close()
        

def fetch_providers_from_db():
    """
    Fetch all providers from the 'providers' table and convert Snowflake ARRAYs into Python lists.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT
            provider_id,
            name,
            ARRAY_TO_STRING(genders, ',') AS genders,
            ARRAY_TO_STRING(specialties, ',') AS specialties,
            ARRAY_TO_STRING(therapy_types, ',') AS therapy_types,
            ARRAY_TO_STRING(focus_tags, ',') AS focus_tags,
            ARRAY_TO_STRING(insurances, ',') AS insurances,
            price_min,
            price_max,
            city,
            province,
            contact_email,
            contact_phone
        FROM providers
        ORDER BY name
    """)
    
    rows = cur.fetchall()
    cur.close()
    conn.close()

    providers = []
    for r in rows:
        providers.append({
            "provider_id": r[0],
            "name": r[1],
            "genders": list(r[2]) if r[2] else [],
            "specialties": list(r[3]) if r[3] else [],
            "therapy_types": list(r[4]) if r[4] else [],
            "focus_tags": list(r[5]) if r[5] else [],
            "insurances": list(r[6]) if r[6] else [],
            "price_min": r[7],
            "price_max": r[8],
            "city": r[9],
            "province": r[10],
            "contact_email": r[11],
            "contact_phone": r[12]
        })
    return providers



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
CREATE TABLE IF NOT EXISTS providers (
    provider_id        INT AUTOINCREMENT PRIMARY KEY,
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

# Insert sample rows only if table is empty
cur.execute("SELECT COUNT(*) FROM providers")
if cur.fetchone()[0] == 0:
    cur.execute("""
    INSERT INTO providers
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

conn.commit()
cur.close()
conn.close()
print("Schema created and sample data inserted (if empty).")

