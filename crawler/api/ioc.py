from api.Database import Database

def ioc_push(ioc_list):
    link_ioc_mongo = Database()
    tags = ["domain", "ip", "url", "email", "hash"]
    for ioc in ioc_list:
        for tag in tags:
            if tag in ioc:
                link_ioc_mongo.insert(tag, ioc)
    link_ioc_mongo.close()