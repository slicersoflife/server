from fuzzywuzzy import fuzz


# fuzzy search logic
def perform_fuzzy_search(query, items):
    results = []
    for item in items:
        ratio = fuzz.token_set_ratio(query, item)
        if ratio > 50:  # Adjust the threshold as per your requirement
            results.append(item)
    return results
