# filename: publication_stats.py
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import datetime

def get_publication_count(keyword, start_year):
    """
    Retrieves the approximate number of publications for a given keyword on Google Scholar
    within the last 5 years.

    Args:
        keyword (str): The keyword to search for.
        start_year (int): The starting year for the search (last 5 years).

    Returns:
        int: The approximate number of publications.
    """
    end_year = datetime.datetime.now().year
    url = f"https://scholar.google.com/scholar?q={keyword}&hl=en&as_sdt=0,5&as_ylo={start_year}&as_yhi={end_year}"
    try:
        response = requests.get(url, timeout=10)  # Added timeout
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, "html.parser")
        result_stats = soup.find(id="gs_ab_md")

        if result_stats:
            text = result_stats.get_text()
            parts = text.split("About")
            if len(parts) > 1:
                parts = parts[1].split("results")
                if len(parts) > 0:
                    count_str = parts[0].strip().replace(",", "")
                    try:
                        count = int(float(count_str))  # Handle cases like "About 123000 results"
                        return count
                    except ValueError:
                        print(f"Could not parse publication count from: {text}")
                        return 0
            else:
                print(f"Unexpected format: {text}")
                return 0
        else:
            print("Result stats container not found.")
            return 0
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

if __name__ == "__main__":
    keywords = ["wearables", "smartphone", "personal PC"]
    start_year = datetime.datetime.now().year - 5

    publication_counts = {}
    for keyword in keywords:
        publication_counts[keyword] = get_publication_count(keyword, start_year)
        print(f"{keyword}: {publication_counts[keyword]}")

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.bar(publication_counts.keys(), publication_counts.values(), color=['blue', 'green', 'red'])
    plt.xlabel("Keywords")
    plt.ylabel("Number of Publications (Approximate)")
    plt.title("Number of Publications on Wearables, Smartphones, and Personal PCs (Last 5 Years)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.savefig("result.png")
    plt.show()