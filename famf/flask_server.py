from flask import Flask
from flask import render_template
from flask import request
from scraper_components import web_scraper

# GLOBAL VARS#
HOST_NAME = "localhost"
LOCAL_PORT = 3000

app = Flask(__name__)

# WEB PAGE HANDLING #
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")


# HANDLE DATA FROM FRONTEND #
@app.route('/web-scrape-submission-handler', methods=['POST'])
def handleWebScraperInput():
    url = str(request.values["user_input"][0])
    data_type = str(request.values["user_input"][1])

    if data_type in web_scraper.validDataTypes:
        web_scraper.webScraperInput(url, data_type)
    else:
        return "Got an invalid data type"


# Start Flask
if __name__ == "__main__":
    app.run(host=HOST_NAME, port=LOCAL_PORT, debug=False)