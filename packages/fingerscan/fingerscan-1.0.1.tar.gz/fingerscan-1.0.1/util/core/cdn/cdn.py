"""
@Project ：指纹识别 
@File    ：cdn.py
@IDE     ：PyCharm 
@Author  ：zhizhuo
@Date    ：2023/10/18 16:05 
"""
import json
import socket
import ipaddress
from urllib.parse import urlparse
from poc_tool.log import log


class GetCdnClass:
    """
    用来判断是不是cdn资产
    """

    def __init__(self):
        """
        初始化操作
        """
        cdn_file = "config/cdn_ip_cidr.json"
        with open(cdn_file, 'r', encoding='utf-8') as file:
            self.cdn_finger = json.load(file)

    @staticmethod
    def get_host(url):
        return urlparse(url).hostname

    def is_cdn(self, url):
        """
        判断是不是cdn资产
        :param url:url地址
        :return:True or False
        """
        ip_list = list()
        try:
            host = self.get_host(url)
            items = socket.getaddrinfo(host, None)
            for ip in items:
                if ip[4][0] not in ip_list:
                    ip_list.append(ip[4][0])
            if len(ip_list) > 1:
                return dict(is_cdn=1, ip_list=ip_list)
            else:
                for cdn_ip in self.cdn_finger:
                    if ipaddress.ip_address(ip_list[0]) in ipaddress.ip_network(cdn_ip):
                        return dict(is_cdn=1, ip_list=ip_list)
            return dict(is_cdn=0, ip_list=ip_list)
        except Exception as e:
            log.debug(f'cdn error {e}')
            return dict(is_cdn=0, ip_list=ip_list)


cdn = GetCdnClass()
