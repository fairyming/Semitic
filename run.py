from flask import Flask, request, jsonify, Response, render_template
import json
from lib.data import logger, ioc, proto
from lib.enums import CUSTOM_LOGGING
from api.analyze import deal_eve_content
from api.display import Display_Semitic, Display_Intelligence, Visualization
from api.search import Search
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
