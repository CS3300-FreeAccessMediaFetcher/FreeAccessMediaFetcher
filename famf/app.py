from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from scraper_components import web_scraper

# GLOBAL VARS #
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
# Input from URL submission field
@app.route('/web-scrape-submission-handler', methods=['POST'])
def handleWebScraperInput():
    try:

        # Retrieve data POSTed from frontend as strings
        url = str(request.values["url"])
        data_type = str(request.values["data_type"])
        res = {}

        # Run scraping function on backend
        if data_type in web_scraper.validDataTypes:
            res = web_scraper.webScraperInput(url, data_type)
        else:
            res["Error"] = f"Got an invalid data type: {data_type}"

        # Send response as JSON object back to Javascript
        if "DataList" in res:
            web_scraper.webScraperDictionaryClear()
            return jsonify(res["DataList"])
        elif "Error" in res:
            return jsonify(res["Error"])
        else:
            return {}
    except Exception as e:
        res["Error"] = str(e)
        return jsonify(res) 

# Download scraped files
@app.route('/download-handler', methods=['POST'])
def handleDownloadRaw():
    try:

        # Retrieve data POSTed from frontend as a dictionary
        request_data = request.get_json()
        download_type = request_data["download_type"]
        data = request_data["data"]
        res = {}

        # Run download function on the backend
        res = web_scraper.downloadData(download_type, data)
        return jsonify(res) 

    except Exception as e:
        res["Error"] = str(e)
        return jsonify(res) 


# Start Flask
if __name__ == "__main__":
    app.run(host=HOST_NAME, port=LOCAL_PORT, debug=False)