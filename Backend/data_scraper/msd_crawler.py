# Import standard libraries for file system handling, web requests, HTML parsing, and time management
import os
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

# URL of the MSD Monthly Housing Reporting page
BASE_URL = "https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/statistics/housing/monthly-housing-reporting.html"

# Define where downloaded files should be stored (relative to this script)
DATA_DIR = os.path.join("..", "..", "Data", "MSD")

# Create the output directory if it doesn't already exist
os.makedirs(DATA_DIR, exist_ok=True)

# Custom User-Agent header to identify this script to the server
# Best practice: include contact info or project name
HEADERS = {
    "User-Agent": "MJ-Homes-Dashboard-Crawler/1.0 (student use; contact@example.com)"
}

# Path to the log file that will track crawl activity
LOG_FILE = os.path.join(DATA_DIR, "crawl_log.txt")

def log(message: str):
    """
    Logs a timestamped message to both the console and a log file.

    Args:
        message (str): The message to log.
    """
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")  # Format current time
    full_message = f"{timestamp} {message}"
    print(full_message)  # Print to terminal
    with open(LOG_FILE, "a") as f:
        f.write(full_message + "\n")  # Append to log file

def fetch_and_save_reports():
    """
    Connects to the MSD monthly housing page,
    parses file download links, and saves valid files locally.
    """
    try:
        # Send a GET request to the target URL with the custom headers
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()  # Raise an error if the status code is not 200 OK

        # Parse the HTML response using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <a> tags on the page that contain an 'href' attribute
        links = soup.find_all("a")

        # Define file types that should be downloaded
        allowed_ext = (".pdf", ".xls", ".xlsx")

        # Loop through all anchor tags found on the page
        for link in links:
            href = link.get("href")  # Get the URL from the anchor
            if href and href.lower().endswith(allowed_ext):
                # Create full URL in case it’s a relative link
                full_url = urljoin(BASE_URL, href)

                # Get just the filename from the full URL
                file_name = os.path.basename(full_url)

                # Build the full file path to save to local disk
                file_path = os.path.join(DATA_DIR, file_name)

                # Skip download if the file already exists locally
                if os.path.exists(file_path):
                    log(f"Skipping (already downloaded): {file_name}")
                    continue

                try:
                    # Download the file content
                    file_response = requests.get(full_url, headers=HEADERS)
                    file_response.raise_for_status()  # Raise an error if file can't be downloaded

                    # Save the content to a local file
                    with open(file_path, "wb") as f:
                        f.write(file_response.content)

                    # Log the successful download
                    log(f"Downloaded: {file_name}")

                except Exception as e:
                    # Log any error that occurred while trying to download
                    log(f"Failed to download {file_name}: {e}")

                # Wait 1 second to avoid overloading the server (ethical crawling)
                time.sleep(1)

    except Exception as e:
        # Log any error that occurred while fetching the main page
        log(f"Error during crawl: {e}")

# Run the script only if it's the main program (not being imported)
if __name__ == "__main__":
    log("=== Starting MSD Housing Report Crawl ===")
    fetch_and_save_reports()
    log("=== Crawl Completed ===\n")
