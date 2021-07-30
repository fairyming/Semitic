# encoding:utf-8
from lib.logger import LOGGER

# log
logger = LOGGER

# rule_dict
rule_key = {
    "2000121201": "tcp",
    "2000121202": "udp",
    "2000121203": "dns",
    "2000121207": "smb",
    "2000121208": "http",
    "2000121209": "tls"
}

# 漏洞告警规则id 2020000001-2030000001

# 服务规则id 1020000001-1030000001

# ioc
ioc = ["domain", "email", "hash", "ip", "url"]


# proto
proto = ["dns", "tls", "http", "tcp", "udp"]


my_email = "czm9976@gamil.com"
