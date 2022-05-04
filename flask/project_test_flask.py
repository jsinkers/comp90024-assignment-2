import requests

BASE = 'http://127.0.0.1:5000/'  # server

test_get_URL = "/api/analytics/diversity"
response = requests.get(BASE + test_get_URL)

print(response.json())
