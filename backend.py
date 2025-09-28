from fastapi import FastAPI, HTTPException, Depends, Query
from snowflake.connector import connect, DictCursor, ProgrammingError
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()
app = FastAPI(title="Providers API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_snowflake_conn():
    try:
        conn = connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )
        yield conn
    finally:
        conn.close()

# ---- Generic functions for unique values ----
allowed_columns = {
    "provider_role": "PROVIDER_ROLE",
    "gender_identity": "GENDER_IDENTITY",
    "insurance": "INSURANCE",
    "session_options": "SESSION_OPTIONS",
    "specialized_support": "SPECIALIZED_SUPPORT",
    "services_offered": "SERVICES_OFFERED"
}

def get_unique_values(column: str, conn):
    if column not in allowed_columns:
        raise ValueError("Invalid column")
    query = f"SELECT DISTINCT {allowed_columns[column]} FROM providers ORDER BY {allowed_columns[column]}"
    with conn.cursor(DictCursor) as cur:
        cur.execute(query)
        results = [row[allowed_columns[column]] for row in cur.fetchall()]
    return results

def get_unique_individual_values(column: str, conn):
    raw_values = get_unique_values(column, conn)
    all_values = set()
    for val in raw_values:
        if val:
            split_vals = [v.strip() for v in val.split(",")]
            all_values.update(split_vals)
    return sorted(all_values)

@app.get("/unique/{column_name}")
def unique_values(column_name: str, conn=Depends(get_snowflake_conn)):
    try:
        return get_unique_values(column_name, conn)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Database error: {e}"}

@app.get("/unique_split/{column_name}")
def unique_split_values(column_name: str, conn=Depends(get_snowflake_conn)):
    try:
        return get_unique_individual_values(column_name, conn)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Database error: {e}"}

# ---- Refactored search endpoint ----
@app.get("/search/providers")
def search_providers(
    occupation: list[str] = Query(None),
    specialty: list[str] = Query(None),
    insurance: list[str] = Query(None),
    session: list[str] = Query(None),
    gender: list[str] = Query(None),
    services: list[str] = Query(None),
    rate_min: float = None,
    rate_max: float = None,
    city: str = None,
    limit: int = 5,
    conn=Depends(get_snowflake_conn)
):
    limit = min(limit, 50)
    query = "SELECT * FROM providers WHERE 1=1"
    params = []

    filters = {
        "occupation": ("PROVIDER_ROLE", occupation),
        "specialty": ("SPECIALIZED_SUPPORT", specialty),
        "insurance": ("INSURANCE", insurance),
        "session": ("SESSION_OPTIONS", session),
        "gender": ("GENDER_IDENTITY", gender),
        "services": ("SERVICES_OFFERED", services),
    }

    for _, (column, values) in filters.items():
        if values:
            placeholders = " OR ".join([f"{column} ILIKE %s" for _ in values])
            query += f" AND ({placeholders})"
            params.extend([f"%{v}%" for v in values])

    if rate_max is not None:
        query += " AND HOURLY_RATE <= %s"
        params.append(rate_max)
    if rate_min is not None:
        query += " AND HOURLY_RATE >= %s"
        params.append(rate_min)
    if city:
        query += " AND ADDRESS ILIKE %s"
        params.append(f"%{city}%")

    query += " LIMIT %s"
    params.append(limit)

    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()
    except ProgrammingError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
