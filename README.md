# FreeAccessMediaFetcher
Github repository housing code and dependencies for UCCS CS3300 software engineering project "Free Access Media Fetcher." This application allows users to enter a web URL and scrape the website for text and images. The scraped data can then be downloaded to the user's local machine.

## Installation
Follow these steps to install and run the application locally:

- Ensure **Python 3.10 or higher** is installed on your machine
- Install required dependencies using the provided **requirements.txt** file:
  - **pip3 install -r requirements.txt**
- Run **app.py**:
  - **python3 app.py**
- Open a web browser and navigate to **localhost:3000**

## Usage
1. Enter the URL of the site you wish to scrape into the URL input field on the Home page.
2. Select the type of data you would like to scrape and then click the "Search" button. The table on the right side of the page will be populated with all results that were found.
3. Select the data you wish to download from the table of results and click the "Download" button above the table to download it to your local machine.
