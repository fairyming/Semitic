from flask import Flask, request, jsonify, Response, render_template
import json
from lib.data import logger, ioc, proto
from lib.enums import CUSTOM_LOGGING
from api.analyze import deal_eve_content
from api.display import Display_Semitic, Display_Intelligence, Visualization
from api.search import Search
from flask_paginate import Pagination, get_page_parameter
from lib.data import my_email
from lib.common import list_dict_duplicate_removal
app = Flask(__name__)

@app.route("/api/upload_eve", methods=["POST"])
def upload_eve():
    client_addr = request.remote_addr
    filename = request.files['clientfile'].filename
    filecontent = request.files['clientfile'].readlines()
    deal_eve_content(filecontent)
    logger.log(CUSTOM_LOGGING.SUCCESS, "客户端{client_addr},提交日志{filename}, 告警日志{allow_num}条".format(
        client_addr=client_addr, filename=filename, allow_num=len(filecontent)))
    return "upload sucess"

@app.route("/")
def hello_world():
    server_ip,server_port = request.headers.get("Host").split(":")
    server_info = {
        "server_ip" : server_ip,
        "server_port": server_port,
        "server_email": my_email
    }
    context = {
        "server_info": server_info,
        "server_data": Visualization().display()
    }
    return render_template("index.html", **context)

@app.route("/alert_rule", methods=["GET"])
def dispaly_alert_rule():
    all_rule_alert = Display_Semitic().display_alert_rule()["data"]
    all = len(all_rule_alert)
    pre_page = 20
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, per_page = pre_page, total=all)
    alert_rule = all_rule_alert[start:end]
    context = {
        'pagination': pagination,
        'alert_rule': alert_rule
    }

    return render_template('alert_rule.html', **context)

@app.route("/alert_ioc", methods=["GET"])
def display_alert_ioc():
    all_ioc_alert = Display_Semitic().display_alert_ioc()["data"]
    all = len(all_ioc_alert)
    pre_page = 20
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, per_page = pre_page, total=all)
    alert_ioc = all_ioc_alert[start:end]
    context = {
        'pagination': pagination,
        'alert_ioc': alert_ioc
    }
    return render_template('alert_ioc.html', **context)

@app.route("/ioc", methods=["GET"])
def display_ioc():
    ioc_type = request.args.get("type")
    if ioc_type in ioc:
        all_ioc = Display_Intelligence().display_ioc(ioc_type)["data"]
        all = len(all_ioc)
        pre_page = 20
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page-1) * pre_page
        end = start + pre_page
        pagination = Pagination(bs_version=3, page=page, per_page = pre_page, total=all)
        iocs = all_ioc[start:end]
        context = {
            'pagination': pagination,
            'iocs': iocs
        }
        return render_template('ioc_{}.html'.format(ioc_type), **context)
        # return render_template('ioc_{}.html'.format(ioc_type))
    else:
        return jsonify({"data": "无当前种类ioc"})

@app.route("/proto", methods=["GET"])
def display_proto():
    proto_type = request.args.get("type")
    if proto_type in proto:
        all_proto = Display_Semitic().display_proto(proto_type)["data"]
        all = len(all_proto)
        pre_page = 20
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page-1) * pre_page
        end = start + pre_page
        pagination = Pagination(bs_version=3, page=page, per_page = pre_page, total=all)
        protos = all_proto[start:end]
        context = {
            'pagination': pagination,
            'protos': protos
        }
        return render_template(proto_type + '.html', **context)
    else:
        return jsonify({"data": "暂不支持当前协议"})

@app.route("/service", methods=["GET"])
def display_service():
    # return jsonify(Display_Semitic().display_service())
    all_service = Display_Semitic().display_service()["data"]
    all = len(all_service)
    pre_page = 20
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1) * pre_page
    end = start + pre_page
    pagination = Pagination(bs_version=3, page=page, per_page = pre_page, total=all)
    services = all_service[start:end]
    context = {
        'pagination': pagination,
        'services': services
    }
    return render_template('service.html', **context)

@app.route("/api/search/ioc", methods=["POST"])
def search_ioc():
    # ip\domain\url\email\hash
    # eg:{"ip":"123.123.123.123"}
    data = request.get_json()
    return jsonify(Search(data).get_reslut())

@app.route("/api/display/visualization", methods=["GET"])
def visualization():
    # 返回当前库中ioc种类及每个种类个数，及所有ioc个数
    # 返回告警数，ioc告警数及规则告警数
    # 返回流量协议分布
    return jsonify(Visualization().display())


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
