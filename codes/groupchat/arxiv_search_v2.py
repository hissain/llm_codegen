# filename: arxiv_search_v2.py
import arxiv
import datetime

today = datetime.date.today()
past_three_months = today - datetime.timedelta(days=90)
past_three_months_str = past_three_months.strftime("%Y-%m-%d")
today_str = today.strftime("%Y-%m-%d")

search = arxiv.Search(
    query=f"((GPT-4) OR (Large Language Model) OR (LLM)) AND date-range:[{past_three_months_str} TO {today_str}]",
    max_results=100,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending,
)

for result in search.results():
    print(result.title)
    print(result.published)
    print(result.summary)
    print("------")
