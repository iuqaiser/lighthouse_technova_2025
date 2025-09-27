#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 09:13:29 2025

@author: angelinachen
"""
from fastapi import FastAPI, Query
from typing import List, Optional
import snowflake.connector



app = FastAPI()

def get_conn():
    return snowflake.connector.connect(
        user="YOUR_USER",
        password="YOUR_PASS",
        account="YOUR_ACCOUNT",
        warehouse="YOUR_WH",
        database="YOUR_DB",
        schema="PUBLIC"
    )

@app.get("/search/providers")
def search_providers(
    q: Optional[str] = None,
    specialties: Optional[List[str]] = Query(None),
    insurances: Optional[List[str]] = Query(None),
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: float = 50
):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
    SELECT provider_id, name, city, province, rating
    FROM providers
    WHERE 1=1
    """
    params = {}

    if q:
        sql += " AND LOWER(name) ILIKE '%' || :q || '%'"
        params["q"] = q.lower()

    if specialties:
        conds = []
        for i, sp in enumerate(specialties):
            key = f"sp{i}"
            conds.append(f"ARRAY_CONTAINS(:{key}, specialties)")
            params[key] = sp
        sql += " AND (" + " OR ".join(conds) + ")"

    if insurances:
        conds = []
        for i, ins in enumerate(insurances):
            key = f"in{i}"
            conds.append(f"ARRAY_CONTAINS(:{key}, insurances)")
            params[key] = ins
        sql += " AND (" + " OR ".join(conds) + ")"

    if lat and lon:
        sql += """
        AND ST_DISTANCE(location_point, TO_GEOGRAPHY('POINT(' || :lon || ' ' || :lat || ')')) <= :radius_m
        """
        params["lat"] = lat
        params["lon"] = lon
        params["radius_m"] = radius_km * 1000

    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {"results": [dict(zip(["id","name","city","province","rating"], r)) for r in rows]}

