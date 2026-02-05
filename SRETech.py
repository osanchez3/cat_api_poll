import redis as redis_lib
import requests
import sys

def run_sync():
    # 1. Connection Setup
    redis = redis_lib.Redis(host='localhost', port=6379, decode_responses=True)

    # Connection Check
    try:
        redis.ping()
        print("--> Connected to Redis successfully")
    except:
        print("*** ERROR: Could not connect to Redis. ***")
        sys.exit(1)

    # 2. API Polling
    api_url = "https://catfact.ninja/fact"

    try:
        response = requests.get(api_url, timeout=10)
        cat_data = response.json()
        fact_text = str(cat_data.get('fact'))
        record_key = "latest_cat_fact"
    except Exception as e:
        print("ERROR: API Error: " + str(e))
        return

    # 3. GET
    existing_value = redis.get(record_key)

    if existing_value:
        print("UPDATING: Replacing old fact.")
    else:
        print("SET: Creating new entry.")

    # 4. SET/UPDATE
    redis.set(record_key, fact_text)

    print("SUCCESS: New fact stored: " + fact_text)
    print("--> Please note: Momo is the best cat ever!")

run_sync()
