# filename: arxiv_search.py
import arxiv
import datetime

today = datetime.date.today()
past_month = today - datetime.timedelta(days=30)

search = arxiv.Search(
    query="GPT-4",
    max_results=50,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
)

for result in search.results():
    published_date = result.published.date()
    if published_date >= past_month:
      print(result.title)
      print(result.published)
      print(result.summary)
      print("------")