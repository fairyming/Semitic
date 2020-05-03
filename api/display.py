from api.database import Database
from lib.data import ioc, proto

class Display_Semitic():
    def __init__(self):
        self.link = Database("Semitic")
        super().__init__()
    
    def display_alert_rule(self):
        result = {}
        result["data"] = []
        select_result = self.link.select("alert",query={})
        if select_result:
            for alert in select_result:
                alert.pop("_id")
                result["data"].append(alert)
        self.link.close()
        return result

    def display_alert_ioc(self):
        result = {}
        result["data"] = []
        select_result = self.link.select("alert_ioc",query={})
        if select_result:
            for alert in select_result:
                alert.pop("_id")
                result["data"].append(alert)
        self.link.close()
        return result
    
    def display_proto(self, type):
        result = {}
        result["data"] = []
        select_result = self.link.select(type, query={})
        for proto in select_result:
            proto.pop("_id")
            result["data"].append(proto)
        self.link.close
        return result


    def alert_count(self):
        result = {}
        result["rule_count"] = self.link.count("alert")
        result["ioc_count"] = self.link.count("alert_ioc")
        result["count"] = result["rule_count"] + result["ioc_count"]
        self.link.close()
        return result
    
    def proto_count(self):
        result = {}
        count = 0
        for proto_type in proto:
            result[proto_type] = self.link.count(proto_type)
            count += self.link.count(proto_type)
        result["count"] = result["tcp"] + result['udp']
        self.link.close()
        return result



class Display_Intelligence():
    def __init__(self):
        self.link = Database("Intelligence")
        super().__init__()
    
    def display_ioc(self, type):
        result = {}
        result["data"] = []
        select_result = self.link.select(type,query={})
        if select_result:
            for alert in select_result:
                alert.pop("_id")
                result["data"].append(alert)
        self.link.close()
        return result
    
    def ioc_count(self):
        result = {}
        count = 0
        for ioc_type in ioc:
            result[ioc_type] = self.link.count(ioc_type)
            count += count + result[ioc_type]
        result["count"] = count
        self.link.close()
        return result
    



class Visualization():
    def display(self):
        result = {}
        result["data"] = {}
        # 告警总数
        result["alert"] = Display_Semitic().alert_count()
        # ioc统计
        result["ioc"] = Display_Intelligence().ioc_count()
        # 协议分布
        result['proto'] = Display_Semitic().proto_count()
        return result