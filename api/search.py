from api.database import Database
import requests
import json


class Search():
    def __init__(self, data):
        self.link = Database("Intelligence")
        self.search_type = list(data.keys())[0]
        self.search_value = data[self.search_type]
        self.result = {}
        self.result["data"] = []
        super().__init__()

    def search_local(self):
        result_local = {}
        result_local["from"] = "local"
        result_local["type"] = self.search_type
        result_local["value"] = self.search_value
        try:
            local = self.link.select(self.search_type, query={
                                     self.search_type: self.search_value})[0]
            result_local["result"] = "success"
            result_local["tags"] = local["tags"]
            # result_local["time"] = local["disclosure_time"]
        except:
            result_local["result"] = "fail"
        self.link.close()
        return(result_local)

    def search_venuseye(self):
        check_url = {
            "ip": "https://www.venuseye.com.cn/ve/ip/ioc",
            "email": "https://www.venuseye.com.cn/ve/email/ioc",
            "domain": "https://www.venuseye.com.cn/ve/domain/ioc",
            "hash": {
                "sha256": "https://www.venuseye.com.cn/ve/sample/sha256",
                "sha1": "https://www.venuseye.com.cn/ve/sample/sha1",
                "md5": "https://www.venuseye.com.cn/ve/sample/md5"
            }
        }
        venuseye_reslut = {}
        venuseye_reslut["from"] = "venuseye"
        venuseye_reslut["type"] = self.search_type
        venuseye_reslut["value"] = self.search_value
        try:
            if self.search_type == "hash":
                if len(self.search_value) == 32:
                    venuseye = json.loads(requests.post(check_url["hash"]["md5"], {
                                          "target": self.search_value}).content)
                elif len(self.search_value) == 40:
                    venuseye = json.loads(requests.post(check_url["hash"]["sha1"], {
                                          "target": self.search_value}).content)
                elif len(self.search_value) == 64:
                    venuseye = json.loads(requests.post(check_url["hash"]["sha256"], {
                                          "target": self.search_value}).content)

                venuseye_reslut["tags"] = venuseye["data"]["tags"]
            else:
                venuseye = json.loads(requests.post(check_url[self.search_type], {
                                      "target": self.search_value}).content)
                venuseye_reslut["result"] = "success"
                venuseye_reslut["tags"] = []
                for ioc in venuseye["data"]["ioc"]:
                    for tag in ioc["categories"]:
                        venuseye_reslut["tags"].append(tag)
                venuseye_reslut["tags"] = [
                    x for x in set(venuseye_reslut["tags"])]
        except:
            venuseye_reslut["result"] = "fail"
        return venuseye_reslut

    def get_reslut(self):
        self.result["data"].append(self.search_local())
        self.result["data"].append(self.search_venuseye())
        return self.result
