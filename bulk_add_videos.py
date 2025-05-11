import json
import requests

CATEGORIZED_FILE = "playlist_58353859-cfbc-4d37-9796-11877808c8fb_categorized.json"
BASE_URL = "http://localhost:8000/categories/{}/videos/fetch?url={}"

with open(CATEGORIZED_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for category, videos in data["categories"].items():
    for video in videos:
        url = video["url"]
        endpoint = BASE_URL.format(category, url)
        response = requests.post(endpoint)
        print(f"POST {endpoint} -> {response.status_code}")
