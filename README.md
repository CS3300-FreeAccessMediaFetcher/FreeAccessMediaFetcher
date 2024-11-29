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

## Developer Documentation
Free Access Media Fetcher is separated into three main components: **Web Scraper (Backend)**, **Web-Based UI (Frontend)**, and **Flask (API)**. 

At a high level, the user interacts with the Frontend UI and the Frontend sends POST requests (in JavaScript) to Flask. Flask serves as an API between the front and backend, and calls Python functions on the Backend to handle the user input by peforming whatever logical work need to be done. After the Backend function finishes, Flask gets the return value, which it can send to the Frontend to display results to the user. 

Each component is described in more detail below:

**Web Scraper (Backend)**

The Web Scraper is contained within the "scraper_components" directory. This directory is intended to contain Python sub-modules that perform the logical work of the application, such as scraping a website and downloading data. Future feature enhancements should be added here as new sub-modules. 

For example, a sub-module could be created called "file_converter.py" which contained logic to convert data file types. This sub-module could be imported into Flask (in "app.py") and any functions within the module can now be called directly from Flask inside of a POST request route.

**Web-Based UI (Frontend)**

The UI for this application is served up by Flask as HTML pages with JavaScript performing the logical work necessary to respond to user input and interact with the Flask API. HTML web pages are stored inside of the "templates" directory (*this is important for Flask to render them correctly!*) while CSS/JS files are stored in the "static" directory.

To add a new page, one simply needs to place the HTML file in the "templates" directory and add a new route to Flask (in "app.py") that renders it.

**Flask (API)**

The Flask Python library serves as an interface between the Frontend and Backend. Flask logic is started and contained entirely within "app.py", which is the entrypoint for this application. It runs on localhost:3000 by default. The port can easily be adjusted by changing the value of the "LOCAL_PORT" variable.

With Flask, we create several routes to handle serving up our web pages (or "templates" in Flask terminology) and a couple of other routes to handle POST requests. Flask allows us to handle these requests using native Python code, which makes it a great choice for working with a Python-based backend.

## Usage
1. Enter the URL of the site you wish to scrape into the URL input field on the Home page.
2. Select the type of data you would like to scrape and then click the "Search" button. The table on the right side of the page will be populated with all results that were found.
3. Select the data you wish to download from the table of results and click the "Download" button above the table to download it to your local machine.
