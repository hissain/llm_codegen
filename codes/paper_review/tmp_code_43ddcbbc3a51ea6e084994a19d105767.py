import arxiv
import re
from fpdf import FPDF

def search_arxiv(query, max_results=10):
    """Searches arXiv for papers matching a query and returns a list of summaries."""

    client = arxiv.Client() #Use the client object for searching
    search = client.results(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)


    papers = []
    for result in search:
        try:
            paper_summary = {
                "title": result.title,
                "authors": ", ".join([author.name for author in result.authors]),
                "abstract": result.summary,
                "link": result.entry_id,  #This is still the ID, needs formatting to a URL
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
        review += f"**Link:** {paper['link']}\n\n" #This is still just the ID.  You would need to construct a URL from it.
    return review


def create_pdf(review_document, filename="quantum_machine_learning_review.pdf"):
    """Creates a PDF from the review document."""

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=review_document)
    try:
        pdf.output(filename)
        print(f"PDF created successfully: {filename}")
        return "PDF creation successful"
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return f"PDF creation failed: {e}"



# Example usage:
query = "quantum machine learning"
papers = search_arxiv(query)
review_document = create_review_document(papers)
pdf_creation_status = create_pdf(review_document)
print(pdf_creation_status)
