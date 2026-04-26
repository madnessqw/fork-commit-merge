import requests
import csv
import urllib.parse

def fetch_leads():
    # We will search for 'SaaS founder' or 'SaaS developer'
    query = 'SaaS founder OR "SaaS developer"'
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.github.com/search/users?q={encoded_query}&per_page=50"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Lead-Scraper/1.0"
    }
    
    print(f"Fetching leads from GitHub...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    items = data.get("items", [])
    
    leads = []
    print(f"Found {len(items)} users in search results. Extracting data...")
    
    for user in items:
        username = user.get("login")
        profile_url = user.get("html_url")
        user_type = user.get("type")
        
        leads.append({
            "Username": username,
            "Profile URL": profile_url,
            "Type": user_type
        })
        
        if len(leads) >= 50:
            break
            
    # If we didn't hit 50, let's fetch another page or another query
    if len(leads) < 50:
        query2 = '"P2P developer" OR "P2P API"'
        url2 = f"https://api.github.com/search/users?q={urllib.parse.quote(query2)}&per_page=50"
        print("Fetching more leads with alternative query...")
        resp2 = requests.get(url2, headers=headers)
        if resp2.status_code == 200:
            for user in resp2.json().get("items", []):
                leads.append({
                    "Username": user.get("login"),
                    "Profile URL": user.get("html_url"),
                    "Type": user.get("type")
                })
                if len(leads) >= 50:
                    break

    # Save to CSV
    csv_path = "/home/gokhan/UniverseCreator/leads.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Username", "Profile URL", "Type"])
        writer.writeheader()
        writer.writerows(leads)
        
    print(f"Successfully saved {len(leads)} leads to {csv_path}")

if __name__ == "__main__":
    fetch_leads()