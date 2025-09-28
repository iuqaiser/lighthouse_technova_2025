import requests
import json

# ----- Replace with your running FastAPI URL -----
BASE_URL = "http://127.0.0.1:8000"

# NLQ you want to test
nl_query = "Show me the top 5 providers who specialize in Grief counseling"

# Prepare the payload
payload = {
    "nl_query": nl_query
}

# Send POST request to your NLQ endpoint
response = requests.post(f"{BASE_URL}/query/providers", json=payload)

# Check if the request was successful
if response.status_code == 200:
    results = response.json()
    print("Results:")
    print(json.dumps(results, indent=2))
else:
    print(f"Error {response.status_code}: {response.text}")
