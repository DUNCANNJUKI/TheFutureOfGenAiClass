import requests
import time

API = 'http://127.0.0.1:8002'

# wait for backend
for i in range(12):
    try:
        r = requests.get(API + '/docs', timeout=2)
        print('backend docs:', r.status_code)
        break
    except Exception as e:
        print('waiting for backend...', i)
        time.sleep(1)
else:
    print('backend did not respond; aborting')
    raise SystemExit(1)

text = 'Name: Duncan Njuki\nLocation: Nairobi\nSkills: Python, SQL, ETL\nInterests: data engineering, cloud'
print('\n--- POST /extract ---')
try:
    r = requests.post(API + '/extract', json={'raw_text': text}, timeout=10)
    print('status', r.status_code)
    print(r.text)
    if r.status_code == 200:
        ex = r.json()
        print('\n--- POST /recommend ---')
        r2 = requests.post(API + '/recommend', json=ex, timeout=10)
        print('status', r2.status_code)
        print(r2.text)
    else:
        print('extract failed')
except Exception as e:
    print('error during requests:', e)
