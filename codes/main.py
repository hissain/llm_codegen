import os
import json
import autogen
from typing import List, Dict, Any, Optional
from utils import search_arxiv, create_pdf

# Configuration for the agents
config_list = [
    {
        "model": "gpt-4-turbo",
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "temperature": 0.2
    }
]

# Create a UserProxyAgent with a better configuration for function execution
user_proxy = autogen.UserProxyAgent(
    name="User",
    system_message="A human user who needs a technical review document.",
    code_execution_config={
        "last_n_messages": 3, 
        "work_dir": "paper_review",
        "use_docker": False  # Set to True if you want to use Docker for isolation
    },
    human_input_mode="NEVER"
)

# Researcher agent with improved system message
researcher = autogen.AssistantAgent(
    name="Researcher",
    system_message="""You are a researcher specialized in finding relevant research papers.
    You're expert at retrieving and analyzing scientific publications.
    When asked to search for papers, ALWAYS import and use the search_arxiv function from utils.py
    by writing a Python script that imports and calls this function with appropriate parameters.
    Format your findings as a structured report with clear sections and paper summaries.
    """,
    llm_config={"config_list": config_list}
)

# Writer agent
writer = autogen.AssistantAgent(
    name="Writer",
    system_message="""You are a technical writer specialized in creating comprehensive review documents.
    You take research papers and organize them into a structured review document.
    Your reviews include:
    1. Executive summary
    2. Introduction to the field
    3. Analysis of current research directions
    4. Detailed summaries of key papers
    5. Comparison of methodologies
    6. Future research directions
    7. Conclusion
    8. References (in IEEE format)
    Your writing is clear, precise, and technical but accessible.""",
    llm_config={"config_list": config_list}
)

# PDF creator agent
pdf_creator = autogen.AssistantAgent(
    name="PDFCreator",
    system_message="""You are an expert in creating PDF documents using Python.
    You take the final review document content and format it into a professional PDF.
    ALWAYS import and use the create_pdf function from utils.py by writing a script
    that imports and calls this function with appropriate content structure.""",
    llm_config={"config_list": config_list}
)

# Create a function to run the entire workflow
def run_review_workflow(topic: str) -> str:
    """
    Execute the complete workflow to generate a technical review document.
    
    Args:
        topic: The research topic to generate a review for
        
    Returns:
        Path to the generated PDF
    """
    # Create the working directory
    # os.makedirs("paper_review", exist_ok=True)
    
    # Copy utils.py to the working directory to ensure it's accessible
    # import shutil
    # shutil.copy("utils.py", os.path.join("paper_review", "utils.py"))
    
    # Create a group chat
    groupchat = autogen.GroupChat(
        agents=[user_proxy, researcher, writer, pdf_creator],
        messages=[],
        max_round=20  # Increase max rounds to allow for more interaction
    )
    
    # Create a group chat manager
    manager = autogen.GroupChatManager(groupchat=groupchat)
    
    # Start the chat with clear instructions
    user_proxy.initiate_chat(
        manager,
        message=f"""
        I need a comprehensive technical review document on "{topic}".
        
        Follow these steps exactly:
        
        1. Researcher: Search for the most relevant papers on this topic by writing code to import and use the search_arxiv function from utils.py.
           For example:
           ```python
           from utils import search_arxiv
           
           # Search for papers
           papers = search_arxiv("{topic}", max_results=15)
           # Analyze the papers here
           ```
           
        2. Researcher: Analyze the results and identify the 5-7 most important papers.
        
        3. Writer: Create a comprehensive technical review based on these papers.
        
        4. PDFCreator: Create a PDF by writing code to import and use the create_pdf function from utils.py:
           ```python
           from utils import create_pdf
           
           # Create the PDF
           pdf_path = create_pdf({{
               "title": "Technical Review: {topic}",
               "executive_summary": "...",
               "introduction": "...",
               "current_research": "...",
               "key_papers": "...",
               "methodology_comparison": "...",
               "future_directions": "...",
               "conclusion": "...",
               "references": "..."
           }}, filename="{topic.replace(' ', '_')}_review.pdf")
           ```
           
        The final output should be a PDF file saved in the working directory.
        """
    )
    
    # Return the expected filename
    return f"{topic.replace(' ', '_')}_review.pdf"

# Usage example
if __name__ == "__main__":
    # Set your OpenAI API key as an environment variable before running
    # os.environ["OPENAI_API_KEY"] = "your-api-key"
    
    topic = "quantum machine learning"
    pdf_path = run_review_workflow(topic)
    print(f"Workflow completed. Review document should be at: {pdf_path}")