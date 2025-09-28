from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import traceback
import requests
from snowflake.connector import connect, DictCursor
from dotenv import load_dotenv
import os
import time

# ---- Load environment ----
load_dotenv()

app = FastAPI()

# ---- Snowflake connection ----
conn = connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

# ---- OAuth Token Management ----
_token_cache = {"access_token": None, "expires_at": 0}


def get_snowflake_token():
    """Fetch a fresh OAuth token from Snowflake (cached until expiry)."""
    now = int(time.time())
    if _token_cache["access_token"] and now < _token_cache["expires_at"]:
        return _token_cache["access_token"]

    token_url = f"https://{os.getenv('SNOWFLAKE_ACCOUNT')}.snowflakecomputing.com/oauth/token-request"
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("OAUTH_CLIENT_ID"),
        "client_secret": os.getenv("OAUTH_CLIENT_SECRET")
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        resp = requests.post(token_url, data=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        access_token = data["access_token"]

        # Cache token with expiry
        _token_cache["access_token"] = access_token
        _token_cache["expires_at"] = now + data.get("expires_in", 3600)

        return access_token
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Snowflake token: {e}")


# ---- Cortex Analyst configuration ----
CORTEX_ANALYST_API_URL = f"https://{os.getenv('SNOWFLAKE_ACCOUNT')}.snowflakecomputing.com/api/v2/cortex/analyst/message"
SEMANTIC_MODEL_PATH = "@yourdb.yourschema.yourstage/providers_model.yaml"

# ---- Pydantic model for NLQ ----
class NLQuery(BaseModel):
    nl_query: str


# ---- Natural language query endpoint ----
@app.post("/query/providers")
async def query_providers(query: NLQuery):
    try:
        nl_query = query.nl_query
        token = get_snowflake_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [
                {"role": "system", "content": "You are an assistant that writes Snowflake SQL."},
                {"role": "user", "content": nl_query}
            ],
            "semantic_model_file": SEMANTIC_MODEL_PATH
        }

        # Send request to Cortex Analyst
        response = requests.post(CORTEX_ANALYST_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        sql_query = data.get("sql")
        if not sql_query:
            raise HTTPException(status_code=400, detail="No SQL query generated")

        # Safety check — only allow queries against the providers table
        if "providers" not in sql_query.lower():
            raise HTTPException(status_code=400, detail="Query must target providers table")

        # Execute SQL
        with conn.cursor(DictCursor) as cur:
            cur.execute(sql_query)
            results = cur.fetchall()

        return results

    except Exception:
        traceback_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Internal error:\n{traceback_str}")


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

    query += " LIMIT %s"
    params.append(limit)

    with conn.cursor(DictCursor) as cur:
        cur.execute(query, params)
        results = cur.fetchall()

    return results