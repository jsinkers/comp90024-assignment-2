import requests

BASE = 'http://127.0.0.1:5000/'  # server

<<<<<<< HEAD
# test_get_URL = "/api/analytics/diversity/sentiment/diversity"
# response = requests.get(BASE + test_get_URL)
# print(response.json())


test_get_URL = "/api/analytics/diversity/language"
response = requests.get(BASE + test_get_URL)
=======
test_get_URL = "/api/analytics/diversity"
response = requests.get(BASE + test_get_URL)

>>>>>>> 2dd6147f46f4cb2546e5c14e22f264573426777f
print(response.json())
