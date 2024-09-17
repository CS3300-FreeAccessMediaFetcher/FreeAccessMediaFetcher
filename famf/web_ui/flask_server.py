from flask import Flask
from flask import render_template

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


# Start Flask
if __name__ == "__main__":
    app.run(host=HOST_NAME, port=LOCAL_PORT, debug=False)