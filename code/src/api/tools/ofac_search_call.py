from utils.ofac_search_utils import main

search_term = "Lashkar"

result = main(search_term)

print("Search results = ", result)