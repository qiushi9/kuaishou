import json
import re
from traceback import print_exc

from lxml import etree
import requests
class Spider(object):
    def __init__(self):
        pass

    def get_profile_info(self, profile_target):
        if isinstance(profile_target, list):
            profile_infos = []
            for target in profile_target:
                profile_infos.append(self.get_profile_info(target))
            return profile_infos

        for i in range(5):
            try:
                profile_info = {}
                proxies = self.get_proxy('H5F5781WU2N0004P','45255B6E05D53560')
                session = requests.session()
                headers = {
                    "Accept": "text/html,application/xhtml+xml,"
                              "application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)"
                                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"
                }
                response = session.get(url=profile_target, headers=headers, proxies=proxies)
                page_str = response.content.decode()
                page = etree.HTML(page_str)
                fans_follows_info = ''.join(page.xpath("//div[@class='fans-follows']/text()"))
                page_data = re.search("window.pageData= (.*?)</script>", page_str, re.S)
                page_data = page_data.group(1)
                page_info = json.loads(page_data)
                for table in page_info["pageTabs"]:
                    if table["name"] == "作品":
                        profile_info["aweme_num"] = table["count"]
                    elif table["name"] == "收藏":
                        profile_info["collection_num"] = table["count"]
                profile_info["nickname"] = ''.join(page.xpath('//div[@class="name-desc"]/div[@class="name"]/text()'))
                profile_info["city"] = ''.join(page.xpath('//div[@class="detail-info"]/span[@class="home"]/text()'))
                profile_info['uid'] = page_info["userIdInfo"]["userId"]
                profile_info["unique_id"] = page_info["userIdInfo"]["userEid"]
                fans_follows_info = fans_follows_info.split(" ")
                profile_info["follower_num"] = fans_follows_info[1]
                profile_info["focus_num"] = fans_follows_info[3]
                profile_info["avatar"] = page_info['share']["imgUrl"]
                profile_info["status"] = 0
                return profile_info
            except Exception as e:
                print(e)
        else:
            return {"status": 1}

    def get_proxy(self,proxyUser,proxyPass):
        proxyHost = "http-pro.abuyun.com"
        proxyPort = "9010"
        # 代理隧道验证信息
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        proxy_dict = {
            "http": proxyMeta,
            "https": proxyMeta,
            }
        return proxy_dict

def test():
   pass
if __name__ == '__main__':
    spider = Spider()
    print(spider.get_profile_info(profile_target=['https://v.kuaishou.com/8jGU1l']))
