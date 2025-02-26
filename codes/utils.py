import arxiv
import fpdf
from datetime import datetime
from typing import List, Dict, Any, Optional

def search_arxiv(topic: str, max_results: int = 15) -> List[Dict[Any, Any]]:
    """
    Search arXiv for papers on a given topic and return results.
    
    Args:
        topic: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        List of dictionaries containing paper information
    """
    print(f"Searching arXiv for: {topic}")
    topic = f"%22{topic}%22"
    client = arxiv.Client()
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    results = []
    for paper in client.results(search):
        paper_dict = {
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "summary": paper.summary,
            "published": paper.published.strftime("%Y-%m-%d"),
            "url": paper.pdf_url,
            "arxiv_id": paper.get_short_id(),
            "categories": paper.categories
        }
        results.append(paper_dict)
    
    print(f"Found {len(results)} papers on arXiv")
    return results

def create_pdf(content: Dict[str, str], filename: str = "technical_review.pdf") -> str:
    pdf = fpdf.FPDF()
    
    # Title page
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, content["title"], ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Created: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    
    # Table of contents
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Table of Contents", ln=True)
    pdf.set_font("Arial", "", 12)
    
    y_position = pdf.get_y()
    for section in ["executive_summary", "introduction", "current_research", "key_papers", 
                   "methodology_comparison", "future_directions", "conclusion", "references"]:
        if section in content:
            section_title = section.replace("_", " ").title()
            pdf.cell(0, 8, f"{section_title}", ln=True)
    
    # Add content sections
    sections = [
        ("Executive Summary", content.get("executive_summary", "")),
        ("Introduction", content.get("introduction", "")),
        ("Current Research Directions", content.get("current_research", "")),
        ("Key Papers", content.get("key_papers", "")),
        ("Methodology Comparison", content.get("methodology_comparison", "")),
        ("Future Research Directions", content.get("future_directions", "")),
        ("Conclusion", content.get("conclusion", "")),
        ("References", content.get("references", ""))
    ]
    
    for title, text in sections:
        if text:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, title, ln=True)
            pdf.set_font("Arial", "", 12)
            
            # Split text into paragraphs and add to PDF
            paragraphs = text.split("\n\n")
            for para in paragraphs:
                pdf.multi_cell(0, 8, para)
                pdf.ln(4)
    
    # Save the PDF
    import os
    filepath = os.path.abspath(filename)
    pdf.output(filename)
    print(f"PDF created at: {filepath}")
    return filepath

res = search_arxiv("Adaptive ANC")
print(res)