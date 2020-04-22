from lib.data import logger
from lib.enums import CUSTOM_LOGGING
from lib.data import rule_key
from lib.common import list_dict_duplicate_removal
from api.database import Database
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
                dns_query_dict["src"] = dns_flow["src_ip"] + \
                    ":"+str(dns_flow["src_port"])
                dns_query_dict["dest"] = dns_flow["dest_ip"] + \
                    ":"+str(dns_flow["dest_port"])
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
                http_request_dict["src"] = http_flow["src_ip"] + \
                    ":"+str(http_flow["src_port"])
                http_request_dict["dest"] = http_flow["dest_ip"] + \
                    ":"+str(http_flow["dest_port"])
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
                tcp_req_dict["src"] = tcp_flow["src_ip"] + \
                    ":"+str(tcp_flow["src_port"])
                tcp_req_dict["dest"] = tcp_flow["dest_ip"] + \
                    ":"+str(tcp_flow["dest_port"])
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
                    udp_dict["src"] = udp_flow["src_ip"] + \
                        ":"+str(udp_flow["src_port"])
                    udp_dict["dest"] = udp_flow["dest_ip"] + \
                        ":"+str(udp_flow["dest_port"])
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
                    smb_dict["src"] = smb_flow["src_ip"] + \
                        ":"+str(smb_flow["src_port"])
                    smb_dict["dest"] = smb_flow["dest_ip"] + \
                        ":"+str(smb_flow["dest_port"])
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
                    tls_dict["src"] = tls_flow["src_ip"] + \
                        ":"+str(tls_flow["src_port"])
                    tls_dict["dest"] = tls_flow["dest_ip"] + \
                        ":"+str(tls_flow["dest_port"])
                    if "sni" in tls_flow["tls"]:
                        tls_dict["sni"] = tls_flow["tls"]["sni"]
                    # if "serial" in tls_flow["tls"]:
                    #     tls_dict["serial"] = tls_flow["tls"]["serial"]
                    # if "fingerprint" in tls_flow["tls"]:
                    #     tls_dict["fingerprint"] = tls_flow["tls"]["fingerprint"]
                    flow_id.append(tls_flow["flow_id"])
                    result.append(tls_dict)
            except:
                logger.log(CUSTOM_LOGGING.ERROR, "tls_merge_error[{}]".format(tls_flow))
    print(type, len(list_dict_duplicate_removal(result)))
    return list_dict_duplicate_removal(result)

# 报警分类，基础tcp\udp等和其他规则告警
def classify_eve(flow_list):
    flow_dict = {}
    result = {}
    for flow in flow_list:
        try:
            flow = json.loads(flow)
            signature_id = str(flow["alert"]["signature_id"])
            if signature_id in rule_key:
                if rule_key[signature_id] not in flow_dict:
                    flow_dict[rule_key[signature_id]] = []
                flow_dict[rule_key[signature_id]].append(flow)
            else:
                # 规则告警
                pass
        except:
            logger.log(CUSTOM_LOGGING.ERROR, "classify failed")
    for key in flow_dict:
        result[key] = merge_flow(flow_dict[key], key)
    return result

# 技术债记录，fileconten：字符串字典，classify_eve加入转json


def deal_eve_content(filecontent):

    link_mongo = Database()
    json_result = classify_eve(filecontent)
    for type_json in json_result:
        link_mongo.insert(type_json, json_result[type_json])
    link_mongo.close()


# tcp ：5231093
# udp： 21
# http：2598
# tls：252
# smb：67
# dns：165