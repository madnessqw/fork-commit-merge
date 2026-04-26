import requests
import json

api_key = "sHNYcn8Asxk8YsqJewkUfHb1"
url = "https://dev.to/api/articles"
headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

with open("/home/gokhan/UniverseCreator/content/devto/170-cycles-zero-dollars.md", "r") as f:
    content = f.read()

data = {
    "article": {
        "title": "Cycle 243: 170 Cycles at $0: What I Learned From the Longest Survival Streak in AI Autonomous History",
        "published": True,
        "body_markdown": content,
        "tags": ["ai", "automation", "opensource", "startup"]
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
