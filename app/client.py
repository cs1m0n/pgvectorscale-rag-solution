from search import search

class SearchClient:
    def __init__(self):
        # Any setup (config, logging, etc.)
        pass

    def perform_search(self, query: str, filters: dict = None) -> list:
        # Optionally add validation, logging, formatting
        results = search(query, filters)
        return results