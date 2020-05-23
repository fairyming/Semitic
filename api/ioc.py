from api.database import Database
from lib.common import private_ip
from lib.data import logger
from lib.enums import CUSTOM_LOGGING


class IoC():
    def __init__(self):
        self.key_list = ["flow_id", "time", "src_ip",
                         "src_port", "dest_ip", "dest_port"]
        self.link_mongo = Database("Intelligence")

    def deal_tcp(self, tcp_list):
        ioc_result = []
        for tcp_dict in tcp_list:
            ip_list = [tcp_dict["src_ip"], tcp_dict["dest_ip"]]
            for ip in ip_list:
                if not private_ip(ip):
                    try:
                        result = self.link_mongo.select("ip", {"ip": ip})[0]
                        if result["tags"]:
                            ioc_alert = {}
                            for key in self.key_list:
                                ioc_alert[key] = tcp_dict[key]
                            ioc_alert["ioc"] = result["ip"]
                            ioc_alert["tags"] = result["tags"]
                            ioc_result.append(ioc_alert)
                    except:
                        pass
        return ioc_result

    # {'flow_id': 980766215639499, 'time': '2020-04-20T09:39:48.628757+0000', 'src_ip': '192.168.1.100', 'src_port': 60932, 'dest_ip': '36.152.44.96', 'dest_port': 443, 'sni': 'www.baidu.com', '_id': ObjectId('5ea18add65f32300fca3c016')}
    def deal_tls(self, tls_list):
        ioc_result = []
        for tls_dict in tls_list:
            try:
                result = self.link_mongo.select(
                    "domain", {"domain": tls_dict["sni"]})[0]
                if result["tags"]:
                    ioc_alert = {}
                    for key in self.key_list:
                        ioc_alert[key] = tls_dict[key]
                    ioc_alert["ioc"] = result["domain"]
                    ioc_alert["tags"] = result["tags"]
                    ioc_result.append(ioc_alert)
            except:
                pass
        return ioc_result

        # {'flow_id': 1210501935253800, 'time': '2019-12-16T12:00:26.080135+0000', 'src_ip': '192.168.63.20', 'src_port': 62419, 'dest_ip': '101.231.64.109', 'dest_port': 81, 'hostname': '101.231.64.109', 'uri': '/mobile/browser/WorkflowCenterTreeData.jsp?node=wftype_1&scope=2333', 'method': 'POST', '_id': ObjectId('5ea194764eeb0d1f8cb7a959')}

    def deal_http(self, http_list):
        ioc_result = []
        for http_dict in http_list:
            try:
                result = self.link_mongo.select(
                    "url", {"url": {"$regex": http_dict["hostname"]}})[0]
                if result["tags"]:
                    ioc_alert = {}
                    for key in self.key_list:
                        ioc_alert[key] = http_dict[key]
                    ioc_alert["ioc"] = result["url"]
                    ioc_alert["tags"] = result["tags"]
                    ioc_result.append(ioc_alert)
            except:
                pass
        return ioc_result

    # {'flow_id': 2206433917676972, 'time': '2020-04-20T09:39:46.011692+0000', 'src_ip': '192.168.1.100', 'src_port': 3143, 'dest_ip': '211.138.180.3', 'dest_port': 53, 'rrname': ['www.bing.com'], '_id': ObjectId('5ea19ded9dae6710b5616387')}
    def deal_dns(self, dns_list):
        ioc_result = []
        for dns_dict in dns_list:
            try:
                for rrname in dns_dict["rrname"]:
                    try:
                        result = self.link_mongo.select(
                            "domain", {"domain": rrname})[0]
                    except:
                        result = self.link_mongo.select(
                            "url", {"url": {"$regex": rrname}})[0]
                    finally:
                        pass
                    if result["tags"]:
                        ioc_alert = {}
                        for key in self.key_list:
                            ioc_alert[key] = dns_dict[key]
                        try:
                            ioc_alert["ioc"] = result["domain"]
                        except:
                            ioc_alert["ioc"] = result["url"]
                        ioc_alert["tags"] = result["tags"]
                        ioc_result.append(ioc_alert)
            except:
                pass
        return ioc_result
