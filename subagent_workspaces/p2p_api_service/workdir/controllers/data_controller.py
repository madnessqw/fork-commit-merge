def scrape_data(query: str):
    return {
        "status": "success",
        "data": {
            "query": query,
            "results": [
                f"Scraped item 1 for {query}",
                f"Scraped item 2 for {query}",
                f"Scraped item 3 for {query}"
            ]
        }
    }
