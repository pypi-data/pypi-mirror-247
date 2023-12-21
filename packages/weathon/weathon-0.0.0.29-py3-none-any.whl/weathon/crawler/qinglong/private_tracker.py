# -- coding: utf-8 --
# @Time    : 2022/10/7 23:28
import time
import random
import ast
import json
import requests
from lxml import etree
from typing import List

from weathon.utils import  get_environ


class PtSign:

    def __init__(self):

        self.session = requests.Session()
        self.sites: list[str] = []

    def signin(self, cookie, signin_url, user_agent) -> str:
        headers: dict[str, str] = {'cookie': cookie, 'user-agent': user_agent}

        response = self.session.get(signin_url, headers=headers)
        html = etree.HTML(response.text)
        signin_msg = html.xpath(
            '//td[@class="embedded"]/h2/text()|//td[@class="embedded"]//p//text()|//*[@class="embedded"]//*[@class="text"]//text()')
        signin_msg = signin_msg[0] + ',' + ''.join(signin_msg[1:]) + '\n'
        try:
            msg1 = ''.join(html.xpath('//*[@id="outer"]//a/font/text()|//*[@id="outer"]//a/font/span/text()'))
            if '未' in msg1:
                signin_msg += msg1
        except Exception as e:
            print(e)
            pass
        return signin_msg.strip()

    def signin_all(self) -> List[str]:
        messages = []
        for site in self.sites:
            site = ast.literal_eval(site)
            messages.append(site["website"] + '->' + self.signin(cookie=site["cookie"], signin_url=site["signin_url"],
                                                                 user_agent=site["user_agent"]))
        return messages


if __name__ == '__main__':
    # time.sleep(random.randint(1, 3600))
    pt_sign = PtSign()
    # pt_sign.sites.append(get_environ("HDFANS"))
    pt_sign.sites.append(get_environ("PTTIME","{'user_agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36','website': 'hdfans','signin_url': 'https://www.pttime.org/attendance.php?uid=91617','cookie': 'c_lang_folder=chs; c_secure_uid=OTE2MTc%3D; c_secure_ssl=eWVhaA%3D%3D; c_secure_tracker_ssl=eWVhaA%3D%3D; c_secure_pass=b6612420f97343913cc8140aa0fd32e3; c_secure_login=bm9wZQ%3D%3D; cf_clearance=m6DfpvCy02bnnJz6ju9557iWQuP7gLEItsVRxnlP1TI-1703077508-0-1-cd4c6de0.3b2dfb92.9a4d3200-0.2.1703077508'}"))
    messages = pt_sign.signin_all()
    print(messages)
