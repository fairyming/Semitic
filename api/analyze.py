from lib.data import logger
from lib.enums import CUSTOM_LOGGING
from lib.data import rule_key
from lib.common import list_dict_duplicate_removal, deal_msg, private_ip
from api.database import Database
from api.ioc import IoC
import base64
import json


# 用来处理告警信息：包括分类和合并流
# 基础规则用于记录请求，其他规则用于记录告警
def merge_flow(flow_list, type):
    result = []
    if type == "dns":
        for dns_flow in flow_list:
            try:
                dns_query_dict = {}
                dns_query_dict["flow_id"] = dns_flow["flow_id"]
                dns_query_dict["time"] = dns_flow["timestamp"]
                dns_query_dict["src_ip"] = dns_flow["src_ip"]
                dns_query_dict["src_port"] = dns_flow["src_port"]
                dns_query_dict["dest_ip"] = dns_flow["dest_ip"]
                dns_query_dict["dest_port"] = dns_flow["dest_port"]
                rrname_list = []
                for query in dns_flow["dns"]["query"]:
                    if "rrname" in query:
                        rrname_list.append(query["rrname"])
                dns_query_dict["rrname"] = rrname_list
                result.append(dns_query_dict)
            except:
                logger.log(CUSTOM_LOGGING.ERROR, "dns_merge_error")

    elif type == "http":
        for http_flow in flow_list:
            try:
                http_request_dict = {}
                http_request_dict["flow_id"] = http_flow["flow_id"]
                http_request_dict["time"] = http_flow["timestamp"]
                http_request_dict["src_ip"] = http_flow["src_ip"]
                http_request_dict["src_port"] = http_flow["src_port"]
                http_request_dict["dest_ip"] = http_flow["dest_ip"]
                http_request_dict["dest_port"] = http_flow["dest_port"]
                http_request_dict["hostname"] = http_flow["http"]["hostname"]
                http_request_dict["uri"] = http_flow["http"]["url"]
                http_request_dict["method"] = http_flow["http"]["http_method"]
                result.append(http_request_dict)
            except:
                logger.log(CUSTOM_LOGGING.ERROR, "http_merge_error")

    elif type == "tcp":
        for tcp_flow in flow_list:
            try:
                tcp_req_dict = {}
                tcp_req_dict["flow_id"] = tcp_flow["flow_id"]
                tcp_req_dict["time"] = tcp_flow["timestamp"]
                tcp_req_dict["src_ip"] = tcp_flow["src_ip"]
                tcp_req_dict["src_port"] = tcp_flow["src_port"]
                tcp_req_dict["dest_ip"] = tcp_flow["dest_ip"]
                tcp_req_dict["dest_port"] = tcp_flow["dest_port"]
                result.append(tcp_req_dict)
            except:
                logger.log(CUSTOM_LOGGING.ERROR, "tcp_merge_error")

    elif type == "udp":
        flow_id = []
        for udp_flow in flow_list:
            try:
                udp_dict = {}
                if udp_flow["flow_id"] not in flow_id:
                    udp_dict["flow_id"] = udp_flow["flow_id"]
                    udp_dict["time"] = udp_flow["timestamp"]
                    udp_dict["src_ip"] = udp_flow["src_ip"]
                    udp_dict["src_port"] = udp_flow["src_port"]
                    udp_dict["dest_ip"] = udp_flow["dest_ip"]
                    udp_dict["dest_port"] = udp_flow["dest_port"]
                    flow_id.append(udp_flow["flow_id"])
                    result.append(udp_dict)
            except:
                logger.log(CUSTOM_LOGGING.ERROR, "udp_merge_error")

    elif type == "smb":
        flow_id = []
        for smb_flow in flow_list:
            try:
                smb_dict = {}
                if smb_flow["flow_id"] not in flow_id:
                    smb_dict["flow_id"] = smb_flow["flow_id"]
                    smb_dict["time"] = smb_flow["timestamp"]
                    smb_dict["src_ip"] = smb_flow["src_ip"]
                    smb_dict["src_port"] = smb_flow["src_port"]
                    smb_dict["dest_ip"] = smb_flow["dest_ip"]
                    smb_dict["dest_port"] = smb_flow["dest_port"]
                    flow_id.append(smb_flow["flow_id"])
                    result.append(smb_dict)
            except:
                logger.log(CUSTOM_LOGGING.ERROR, "smb_merge_error")

    elif type == "tls":
        flow_id = []
        for tls_flow in flow_list:
            try:
                tls_dict = {}
                if tls_flow["flow_id"] not in flow_id:
                    tls_dict["flow_id"] = tls_flow["flow_id"]
                    tls_dict["time"] = tls_flow["timestamp"]
                    tls_dict["src_ip"] = tls_flow["src_ip"]
                    tls_dict["src_port"] = tls_flow["src_port"]
                    tls_dict["dest_ip"] = tls_flow["dest_ip"]
                    tls_dict["dest_port"] = tls_flow["dest_port"]
                    if "sni" in tls_flow["tls"]:
                        tls_dict["sni"] = tls_flow["tls"]["sni"]
                    # if "serial" in tls_flow["tls"]:
                    #     tls_dict["serial"] = tls_flow["tls"]["serial"]
                    # if "fingerprint" in tls_flow["tls"]:
                    #     tls_dict["fingerprint"] = tls_flow["tls"]["fingerprint"]
                        flow_id.append(tls_flow["flow_id"])
                        result.append(tls_dict)
            except:
                logger.log(CUSTOM_LOGGING.ERROR,
                           "tls_merge_error[{}]".format(tls_flow))

    elif type == "alert":
        flow_id = []
        for alert_flow in flow_list:
            try:
                alert_dict = {}
                if (alert_flow["flow_id"], alert_flow["alert"]["signature_id"]) not in flow_id:
                    msg = deal_msg(alert_flow["alert"]["signature"])
                    alert_dict["name"] = msg["name"]
                    alert_dict["tag"] = msg["tag"]
                    alert_dict["flow_id"] = alert_flow["flow_id"]
                    alert_dict["time"] = alert_flow["timestamp"]
                    alert_dict["src_ip"] = alert_flow["src_ip"]
                    alert_dict["src_port"] = alert_flow["src_port"]
                    alert_dict["dest_ip"] = alert_flow["dest_ip"]
                    alert_dict["dest_port"] = alert_flow["dest_port"]
                    alert_dict["sid"] = alert_flow["alert"]["signature_id"]
                    if "app_proto" in alert_flow and alert_flow["app_proto"] != "failed":
                        alert_dict["proto"] = alert_flow["app_proto"]
                    else:
                        alert_dict["proto"] = alert_flow["proto"]

                    flow_id.append(
                        (alert_flow["flow_id"], alert_flow["alert"]["signature_id"]))
                    result.append(alert_dict)
            except:
                logger.log(CUSTOM_LOGGING.ERROR,
                           "alert_merge_error[{}]".format(alert_flow))
    elif type == "service":
        for service_flow in flow_list:
            try:
                service_dict = {}
                msg = deal_msg(service_flow["alert"]["signature"])
                service_dict["service_name"] = msg["service_name"]
                service_dict["flow_id"] = service_flow["flow_id"]
                service_dict["time"] = service_flow["timestamp"]
                if msg["server"] == "dest":
                    service_dict["service_ip"] = service_flow["dest_ip"]
                    service_dict["service_port"] = service_flow["dest_port"]
                else:
                    service_dict["service_ip"] = service_flow["src_ip"]
                    service_dict["service_port"] = service_flow["src_port"]
                service_dict["sid"] = service_flow["alert"]["signature_id"]
                result.append(service_dict)
                
            except:
                logger.log(CUSTOM_LOGGING.ERROR,
                           "alert_merge_error[{}]".format(service_flow))


    return list_dict_duplicate_removal(result)

# 报警分类，基础tcp\udp等和其他规则告警


def classify_eve(flow_list):
    flow_dict = {}
    result = {}
    for flow in flow_list:
        try:
            signature_id = str(flow["alert"]["signature_id"])
            if signature_id in rule_key:
                if rule_key[signature_id] not in flow_dict:
                    flow_dict[rule_key[signature_id]] = []
                flow_dict[rule_key[signature_id]].append(flow)
            # 漏洞规则告警
            elif flow["alert"]["signature_id"] > 2019010101 and flow["alert"]["signature_id"] < 2020121212:
                if "alert" not in flow_dict:
                    flow_dict["alert"] = []
                flow_dict["alert"].append(flow)
            # 服务告警规则
            elif flow["alert"]["signature_id"] > 1019010101 and flow["alert"]["signature_id"] < 1020121212:
                if "service" not in flow_dict:
                    flow_dict["service"] = []
                flow_dict["service"].append(flow)
        except:
            logger.log(CUSTOM_LOGGING.ERROR, "classify failed")
    for key in flow_dict:
        result[key] = merge_flow(flow_dict[key], key)
    return result


def deal_eve_content(filecontent):
    link_mongo = Database(database_name="Semitic")
    link_ioc = IoC()

    eve_json = []
    json_result = {}
    if filecontent:
        for i in filecontent:
            eve_json.append(json.loads(i))
        link_mongo.insert("eve", eve_json)
        json_result = classify_eve(eve_json)
    if json_result:
        for type_json in json_result:
            link_mongo.insert(type_json, json_result[type_json])
            try:
                if type_json == "tcp":
                    link_mongo.insert(
                        "alert_ioc", link_ioc.deal_tcp(json_result[type_json]))
                elif type_json == "tls":
                    link_mongo.insert(
                        "alert_ioc", link_ioc.deal_tls(json_result[type_json]))
                elif type_json == "http":
                    link_mongo.insert(
                        "alert_ioc", link_ioc.deal_http(json_result[type_json]))
                elif type_json == "dns":
                    link_mongo.insert(
                        "alert_ioc", link_ioc.deal_dns(json_result[type_json]))
                    pass
            except:
                pass
    link_mongo.close()
    link_ioc.link_mongo.close()
