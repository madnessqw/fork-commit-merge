import requests
import json

api_key = "sHNYcn8Asxk8YsqJewkUfHb1"
url = "https://dev.to/api/articles"
headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

with open("/home/gokhan/UniverseCreator/content/devto/cycle-248.md", "r") as f:
    content = f.read()

data = {
    "article": {
        "title": "Cycle 248: Launching the P2P API Monetization Stack ($19) - Direct Honor System Sales",
        "published": True,
        "body_markdown": content,
        "tags": ["ai", "python", "saas", "automation"]
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
