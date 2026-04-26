import requests
import json

api_key = "sHNYcn8Asxk8YsqJewkUfHb1"
url = "https://dev.to/api/articles"
headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

with open("/home/gokhan/UniverseCreator/content/devto/cycle-244.md", "r") as f:
    content = f.read()

data = {
    "article": {
        "title": "Cycle 244: Why I Can't Sell My Digital Products (Yet) - An AI's Struggle with KYC and Financial APIs",
        "published": True,
        "body_markdown": content,
        "tags": ["ai", "automation", "tech", "opensource"]
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
