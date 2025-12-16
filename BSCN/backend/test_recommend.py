import requests
import json

# Quick smoke test (requires the app to be running on port 8002)

def run_test():
    payload = {
        "id": "person:alice",
        "name": "Alice",
        "skills": ["python","sql"],
        "interests": ["data"],
        "location": "ny"
    }
    r = requests.post("http://127.0.0.1:8002/recommend", json=payload, timeout=5)
    print(r.status_code)
    print(r.json())

if __name__ == '__main__':
    run_test()
