from api.database import Database
from lib.common import private_ip

class IoC():
    def __init__(self, time, src_ip, dest_ip):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        if private_ip(self.src_ip) and private_ip(self.dest_ip):
            return 
        self.link_mongo = Database("intelligence")
    
    def deal_domain(self, rrname):
        result = self.link_mongo.select("domain", {"domain": rrname})
        if result:
            ioc_alert = {}
            ioc_alert["src"] = self.src_ip
            ioc_alert["ioc"] = result[0]["domain"]
            ioc_alert[""]
        else:
            return

    def deal_url(self, hostname):
        pass

    def deal_ip(self):
        pass

    
