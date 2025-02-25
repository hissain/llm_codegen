# filename: get_stock_data.py
import requests
from bs4 import BeautifulSoup
import datetime

today = datetime.date.today()
year = today.year

def get_ytd_gain(ticker):
    try:
        url = f"https://www.google.com/finance/quote/{ticker}:NASDAQ?hl=en"
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for any element containing "YTD" and a percentage.  This is a more generic approach.
        ytd_element = soup.find(lambda tag: tag.string and "YTD" in tag.string and "%" in tag.string)

        if ytd_element:
            ytd_text = ytd_element.string
            return ytd_text.strip()
        else:
            return "YTD data not found"

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

meta_ytd = get_ytd_gain("META")
tesla_ytd = get_ytd_gain("TSLA")

print(f"META YTD: {meta_ytd}")
print(f"TSLA YTD: {tesla_ytd}")