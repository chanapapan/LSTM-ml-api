import json
from re import L
import requests

with open('../input.json', encoding="utf8") as json_file:
    data = json.load(json_file)

URL = "http://127.0.0.1:5000/inference"

r = requests.post(URL, json=data)
print(str(r.content, 'utf-8'))