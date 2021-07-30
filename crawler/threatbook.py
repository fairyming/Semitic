import requests
from bs4 import BeautifulSoup
from api.ioc import ioc_push

class Threatbook():
    def __init__(self):
        self.url_list = []
        self.header = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "user-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.24"
        }
        pass

    def get_url_list(self):
        html = requests.get("https://x.threatbook.cn/nodev4/getAllList?currentPage=0", headers = self.header).content
        soup = BeautifulSoup(html, "html5lib")
        latest_url = soup.select_one("body > div:nth-child(1) > div > div.title > a").get("href")
        latest_id = latest_url.split("=")[-1]
        for i in range(1, int(latest_id)):
            self.url_list.append("https://x.threatbook.cn/nodev4/vb4/article?threatInfoID={}".format(i))
    
    def get_ioc(self, url):
        self.result_ioc = []
        self.tags = []
        html = requests.get(url, headers = self.header).content
        try:
            soup = BeautifulSoup(html, "html5lib")
            tags_html = soup.select("#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.brief > div.top-bar.clearfix > div.cTag-list.pull-left")[0].find_all("span")
            for tag in tags_html:
                if tag.getText() != "求分析":
                    self.tags.append(tag.getText())
            time = soup.find_all('span', 'time')[0].getText().strip()
        except:
            pass
        try:
            domains = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.domain")
            for tr in domains.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    ioc['domain'] = tmp[0].getText().strip()
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    ioc['tags'] = self.tags
                    self.result_ioc.append(ioc)
        except:
            pass
        try:
            ips = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.ip")
            for tr in ips.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    ioc['ip'] = tmp[0].getText().strip()
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    ioc['tags'] = self.tags
                    self.result_ioc.append(ioc)
        except:
            pass

        try:
            urls = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.url")
            for tr in urls.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    ioc['url'] = tmp[0].getText().strip()
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    ioc['tags'] = self.tags
                    self.result_ioc.append(ioc)
        except:
            pass

        try:
            hashs = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.hash")
            for tr in hashs.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    try:
                        ioc['filename'] = tmp[0].find_all(
                            'span', 'file-name cutWhenTooLong')[0].getText()
                    except:
                        pass
                    hash = tmp[0].find_all(
                        'span', 'file-hash')[0].getText().strip()
                    # if len(hash) == 32:
                    #     ioc['md5'] = hash
                    # elif len(hash) == 40:
                    #     ioc['sha1'] == hash
                    # else:
                    #     ioc['sha256'] = hash
                    ioc['hash'] = hash
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    ioc['tags'] = self.tags
                    self.result_ioc.append(ioc)
        except:
            pass

        try:
            emails = soup.select_one(
                "#wrapper > div.article.J-article-page > div.content > div.part-left > div.threat-details.box-shadow > div.ioc-list > div > div.ioc-list-body > div.email")
            for tr in emails.select('tr'):
                ioc = {}
                tmp = tr.select('td')
                if tmp and tmp[0].getText().strip():
                    ioc['email'] = tmp[0].getText().strip()
                    ioc['disclosure_time'] = time
                    ioc['reference'] = url
                    ioc['tags'] = self.tags
                    self.result_ioc.append(ioc)
        except:
            pass


    def run(self):
        self.get_url_list()
        # self.url_list = ["https://x.threatbook.cn/nodev4/vb4/article?threatInfoID=2620"]
        for url in self.url_list:
            self.get_ioc(url)
            ioc_push(self.result_ioc)

Threatbook().run()
