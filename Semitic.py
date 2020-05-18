from flask import Flask, request, jsonify, Response
import json
from lib.data import logger, ioc, proto
from lib.enums import CUSTOM_LOGGING
from api.analyze import deal_eve_content
from api.display import Display_Semitic, Display_Intelligence, Visualization
from api.search import Search
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


@app.route("/api/display/alert/rule", methods=["GET"])
def dispaly_alert_rule():
    print(Display_Semitic().display_alert_rule())
    return jsonify(Display_Semitic().display_alert_rule())


@app.route("/api/display/alert/ioc", methods=["GET"])
def display_alert_ioc():
    print(Display_Semitic().display_alert_ioc())
    return jsonify(Display_Semitic().display_alert_ioc())


@app.route("/api/display/ioc", methods=["GET"])
def display_ioc():
    ioc_type = request.args.get("type")
    if ioc_type in ioc:
        return jsonify(Display_Intelligence().display_ioc(ioc_type))
    else:
        return jsonify({"data": "无当前种类ioc"})


@app.route("/api/display/proto", methods=["GET"])
def display_proto():
    proto_type = request.args.get("type")
    tmp = Display_Semitic().display_proto(proto_type)
    tmp["data"] = tmp["data"][1]
    print(tmp)
    if proto_type in proto:
        return jsonify(Display_Semitic().display_proto(proto_type))
    else:
        return jsonify({"data": "暂不支持当前协议"})

@app.route("/api/display/service", methods=["GET"])
def display_service():
    print(Display_Semitic().display_service())
    return jsonify(Display_Semitic().display_service())

@app.route("/api/search/ioc", methods=["POST"])
def search_ioc():
    # ip\domain\url\email\hash
    # eg:{"ip":"123.123.123.123"}
    data = request.get_json()
    print(Search(data).get_reslut())
    return jsonify(Search(data).get_reslut())


@app.route("/api/display/visualization", methods=["GET"])
def visualization():
    # 返回当前库中ioc种类及每个种类个数，及所有ioc个数
    # 返回告警数，ioc告警数及规则告警数
    # 返回流量协议分布
    print(Visualization().display())
    return jsonify(Visualization().display())


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
