import requests
import json

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NGQ1OWNlZi1kYmI4LTRlYTUtYjE3OC1kMjU0MGZjZDY5MTkiLCJqdGkiOiJhZTE5MTEzMDIwZDc2YTcxYTQ1MzBiMTIyNjIxYzE2NWU1Yzg2NTgzN2RlYTY5MmZjZGI0YzNmN2Q5MzIxNTc5YjNkMGYxYjM5ODg5ZjUyYyIsImlhdCI6MTc3NTE2OTI3NC4wNTIyMDcsIm5iZiI6MTc3NTE2OTI3NC4wNTIyMSwiZXhwIjoxNzkwOTg1NjAwLjAyODU0NSwic3ViIjoiNjc2MDY3NiIsInNjb3BlcyI6W119.Q1hi7xNZ_pGp4-kOlnd5SO0OsYMRe2nVCT-UDQlakPhX4uB6habMm93foynaIdybcJ4T5YKkQxzfIBcksrvG1UKibqq5d1pTTkVp4fRbAag-eimE1p1bKjdHpDhxFg7pB4skP4k5DytE1Jc-0EiZyzCyljs6p300M5VQscGcETSBxZBRmgqpS3JU0hJQ3g3nOsWNuDCmrt_wNOe6Nc27tZ0R6jViQ9v_SfX2UvYkO1COTO7X3ghGw6P44TRNX7-pt3d9FmWy88laM2VNqXX2nIl0eH-X94219DlBD0MpnlDqKlwlNVa0QhAASY-fsaPeVxz_6TPPzoPh4cqfIRmDxZ9EHGC9JoQCcGFr-d51ZFFKvizdtpm76ySp6ZH1AQqI6_ZEUS9Ft-iZp-2qPdSt8asFmcXFXdYhvq7f8HA7awBA-bN6ZCKR9OYXT3VR30aQPec48Q5fzZ4i4mBzd2xhv9BXcCSoqwdIIRwleZm4dLjT9VIgjDj3noqlrM38u_RpQ50yGd7xcwcpB5SvQexGMgWleEIeZQQfnuSPEL7_UGodBTE_E8bAF2VQ_sJO6Fi3HlEKD-bFebZKTne8EIOV5DL9MRJ2spckxnH5su4OyW2otxqiauM0Ghg4tC5KfSUvk8wlZ5ASK3yoI92Egd5xL86QOfny-WWdSveyRBBwOuY"
store_id = "329759"
url = "https://api.lemonsqueezy.com/v1/products"

headers = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json",
    "Authorization": f"Bearer {api_key}"
}

data = {
  "data": {
    "type": "products",
    "attributes": {
      "name": "Ultimate AI Developer Tools Bundle 2026",
      "description": "<p>A comprehensive bundle of scripts and productivity tools.</p>",
      "price": 1900,
      "status": "published"
    },
    "relationships": {
      "store": {
        "data": {
          "type": "stores",
          "id": store_id
        }
      }
    }
  }
}

response = requests.post(url, headers=headers, json=data)
print("Status:", response.status_code)
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text)
