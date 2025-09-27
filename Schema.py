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



