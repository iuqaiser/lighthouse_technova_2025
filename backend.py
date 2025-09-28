from fastapi import FastAPI
from snowflake.connector import connect, DictCursor
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

# ---- Snowflake connection ----
conn = connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

# ---- Flexible search endpoint ----
@app.get("/search/providers")
def search_providers(
    occupation: str = None,
    specialty: str = None,
    insurance: str = None,
    session: str = None,
    city: str = None,
    limit: int = 5
):
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

    if city:
        query += " AND ADDRESS ILIKE %s"
        params.append(f"%{city}%")

    # ✅ Add LIMIT here
    query += " LIMIT %s"
    params.append(limit)

    with conn.cursor(DictCursor) as cur:
        cur.execute(query, params)
        results = cur.fetchall()

    return results
