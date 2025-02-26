# filename: download_pdf.py
import requests
import os

url = "http://arxiv.org/pdf/2409.18705v1"  # Corrected URL
filename = "speech_boosting.pdf"
timeout_seconds = 60  # Increased timeout

try:
    response = requests.get(url, stream=True, timeout=timeout_seconds)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"PDF downloaded successfully as {filename}")

except requests.exceptions.RequestException as e:
    print(f"Error downloading PDF: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
