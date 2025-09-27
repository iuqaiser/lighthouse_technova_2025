#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 09:13:29 2025

@author: angelinachen
"""
from fastapi import FastAPI, Query
from typing import List, Optional
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


def get_conn():
    """
    Establishes a connection to Snowflake using environment variables.
    """
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )


@app.get("/")
def root():
    return {"message": "Backend is running!"}


@app.get("/search/providers")
def search_providers(
    q: Optional[str] = None,
    specialties: Optional[List[str]] = Query(None),
    insurances: Optional[List[str]] = Query(None),
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: float = 50
):
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Base query (using lowercase column names)
        sql = """
        SELECT provider_id, full_name, location_city, location_state, session_cost
        FROM providers
        WHERE 1=1
        """
        params = {}

        # Free-text search on full_name
        if q:
            sql += ' AND LOWER(full_name) LIKE '%' || :q || '%''
            params["q"] = q.lower()

        # Filter by specialties (therapy_types array)
        if specialties:
            conds = []
            for i, sp in enumerate(specialties):
                key = f"sp{i}"
                conds.append(f"ARRAY_CONTAINS(therapy_types, :{key})")
                params[key] = sp
            sql += " AND (" + " OR ".join(conds) + ")"

        # Filter by insurance_accepted array
        if insurances:
            conds = []
            for i, ins in enumerate(insurances):
                key = f"in{i}"
                conds.append(f"ARRAY_CONTAINS(insurance_accepted, :{key})")
                params[key] = ins
            sql += " AND (" + " OR ".join(conds) + ")"

        # Optional geolocation filter
        if lat and lon:
            sql += """
            AND ST_DISTANCE(
                location_point,
                TO_GEOGRAPHY('POINT(' || :lon || ' ' || :lat || ')')
            ) <= :radius_m
            """
            params["lat"] = lat
            params["lon"] = lon
            params["radius_m"] = radius_km * 1000

        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Return results
        results = [
            {
                "provider_id": r[0],
                "full_name": r[1],
                "city": r[2],
                "state": r[3],
                "session_cost": float(r[4])
            } for r in rows
        ]

        return {"results": results}

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}
