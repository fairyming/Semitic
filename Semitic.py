from flask import Flask, request
from lib.data import logger
from lib.enums import CUSTOM_LOGGING
from api.analyze import deal_eve_content
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello Semitic"


@app.route("/api/upload_eve", methods=["POST"])
def upload_eve():
    client_addr = request.remote_addr
    filename = request.files['clientfile'].filename
    filecontent = request.files['clientfile'].readlines()
    deal_eve_content(filecontent)
    logger.log(CUSTOM_LOGGING.SUCCESS, "客户端{client_addr},提交日志{filename}, 告警日志{allow_num}条".format(
        client_addr=client_addr, filename=filename, allow_num=len(filecontent)))
    return "upload sucess"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
