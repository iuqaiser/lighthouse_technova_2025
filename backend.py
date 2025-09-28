from fastapi import FastAPI, HTTPException, Depends
from snowflake.connector import connect, DictCursor, ProgrammingError
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

# ---- Load environment ----
load_dotenv()

app = FastAPI(title="Providers API")

# ---- Enable CORS for frontend ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Dependency to get a fresh Snowflake connection ----
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

# ---- Generic function to get unique values ----
def get_unique_values(column: str, conn):
    # Safety: prevent SQL injection by only allowing certain columns
    allowed_columns = {
        "provider_role": "PROVIDER_ROLE",
        "gender_identity": "GENDER_IDENTITY",
        "insurance": "INSURANCE",
        "session_options": "SESSION_OPTIONS",
        "specialized_support": "SPECIALIZED_SUPPORT",
        "services_offered": "SERVICES_OFFERED"
    }
    if column not in allowed_columns:
        raise ValueError("Invalid column")

    query = f"SELECT DISTINCT {allowed_columns[column]} FROM providers ORDER BY {allowed_columns[column]}"
    with conn.cursor(DictCursor) as cur:
        cur.execute(query)
        results = [row[allowed_columns[column]] for row in cur.fetchall()]
    return results

def get_unique_individual_values(column: str, conn):
    """Get unique values, splitting by commas if needed."""
    # First, get the raw unique values as before
    raw_values = get_unique_values(column, conn)
    
    all_values = set()
    for val in raw_values:
        if val:  # skip empty/null values
            # Split by comma and strip whitespace
            split_vals = [v.strip() for v in val.split(",")]
            all_values.update(split_vals)
    
    return sorted(all_values)

@app.get("/unique_split/{column_name}")
def unique_split_values(column_name: str, conn=Depends(get_snowflake_conn)):
    try:
        values = get_unique_individual_values(column_name, conn)
        return values
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Database error: {e}"}

# ---- Endpoints using the generic function ----
@app.get("/unique/{column_name}")
def unique_values(column_name: str, conn=Depends(get_snowflake_conn)):
    try:
        values = get_unique_values(column_name, conn)
        return values
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Database error: {e}"}

# ---- Flexible search endpoint ----
@app.get("/search/providers")
def search_providers(
    occupation: str = None,
    specialty: str = None,
    insurance: str = None,
    session: str = None,
    gender: str = None,
    services: str = None,
    rate_min: float = None,
    rate_max: float = None,
    city: str = None,
    limit: int = 5,
    conn=Depends(get_snowflake_conn)
):
    limit = min(limit, 50)  # safety cap
    query = "SELECT * FROM providers WHERE 1=1"
    params = []

    if occupation:
        query += " AND PROVIDER_ROLE ILIKE %s"
        params.append(f"%{occupation}%")
    if specialty:
        query += " AND SPECIALIZED_SUPPORT ILIKE %s"
        params.append(f"%{specialty}%")
    if insurance:
        query += " AND INSURANCE ILIKE %s"
        params.append(f"%{insurance}%")
    if session:
        query += " AND SESSION_OPTIONS ILIKE %s"
        params.append(f"%{session}%")
    if gender:
        query += " AND GENDER_IDENTITY ILIKE %s"
        params.append(f"%{gender}%")
    if services:
        query += " AND SERVICES_OFFERED ILIKE %s"
        params.append(f"%{services}%")
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
            results = cur.fetchall()
        return results
    except ProgrammingError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# ---- Placeholder endpoint for NLQ / RAG ----
@app.post("/query/providers")
def query_providers_placeholder():
    return {"message": "NLQ / RAG functionality not implemented yet."}
