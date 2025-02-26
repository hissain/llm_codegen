# filename: arxiv_search.py
try:
    import arxiv
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "arxiv"], check=True)
    import arxiv

import datetime

search = arxiv.Search(
    query='"ANC" AND ("earbuds" OR "AirPods")',  # Improved query for better results
    max_results=5,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
)


results = list(search.results())

for result in results:
    print(f"Title: {result.title}")
    print(f"Authors: {', '.join(author.name for author in result.authors)}")
    print(f"Abstract: {result.summary.replace('\n', ' ')}") # Removing newline characters for cleaner output
    print(f"Published: {result.published}")
    print(f"PDF URL: {result.pdf_url}")
    print("---")
