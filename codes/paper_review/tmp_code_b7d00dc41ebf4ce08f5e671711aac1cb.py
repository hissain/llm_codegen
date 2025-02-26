import arxiv
import re

def search_arxiv(query, max_results=10):
    """Searches arXiv for papers matching a query and returns a list of summaries."""

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    papers = []
    for result in search.results():
        try:
            paper_summary = {
                "title": result.title,
                "authors": ", ".join([author.name for author in result.authors]),
                "abstract": result.summary,
                "link": result.entry_id, #This is the ID,  not a direct URL
            }
            papers.append(paper_summary)
        except AttributeError as e:
            print(f"Error processing paper: {e}. Skipping.")

    return papers


def create_review_document(papers):
    """Creates a review document from a list of papers."""

    review = "## Quantum Machine Learning Review\n\n"
    for i, paper in enumerate(papers):
        review += f"### Paper {i+1}\n"
        review += f"**Title:** {paper['title']}\n"
        review += f"**Authors:** {paper['authors']}\n"
        review += f"**Abstract:** {paper['abstract']}\n"
        review += f"**Link:** {paper['link']}\n\n" #Again, this is the ID.  Arxiv IDs need to be properly formatted into URLs
    return review


# Example usage:
query = "quantum machine learning"
papers = search_arxiv(query)
review_document = create_review_document(papers)
#print(review_document) #uncomment to see the generated review

