from fuzzywuzzy import fuzz, process
from streamlit_searchbox import st_searchbox


items = ["example1", "example2", "example3"]


def search(query: str) -> list[str]:
    matches = process.extract(query, items, scorer=fuzz.token_sort_ratio)
    sorted_matches = sorted(matches, key=lambda x: x[1], reverse=True)
    result = [match[0] for match in sorted_matches]
    return result
