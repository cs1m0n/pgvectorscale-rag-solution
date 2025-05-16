from fastapi import FastAPI, Depends, Query
from typing import Optional, Dict
from client import SearchClient

app = FastAPI()

def get_search_client():
    return SearchClient()

@app.get("/search")
def search_endpoint(
    q: str = Query(..., description="Search query"),
    lang: Optional[str] = Query(None, description="Optional language filter"),
    client: SearchClient = Depends(get_search_client)
):
    filters = {}
    if lang:
        filters["lang"] = lang

    return client.perform_search(q, filters)