"""
@Project ：指纹识别 
@File    ：get_icon.py
@IDE     ：PyCharm 
@Author  ：zhizhuo
@Date    ：2023/10/16 15:44 
"""
import base64
import random
import time
import mmh3
import requests
from poc_tool.tools import tools
from poc_tool.log import log


class GetIconClass:
    """
    获取icon hash的相关操作
    """

    def __init__(self):
        """
        初始化相关操作
        """
        self.headers = {
            'Accept': 'application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, '
                      'application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
            'User-agent': tools.get_random_ua(),
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Connection': 'close'
        }
        self.file_header = ['89504E470', '89504e470', '000001000', '474946383', 'FFD8FFE00', 'FFD8FFE10', '3c7376672']

    def get_icon_hash(self, icon_url, retries: int = 3):
        """
        获取icon的hash值
        :param icon_url:url地址
        :param retries:重试次数
        :return:hash
        """
        log.debug(f"icon url地址 {icon_url}")
        icon_hash = None
        for _ in range(retries):
            try:
                resp = requests.get(url=icon_url, headers=self.headers, verify=False,
                                    allow_redirects=False, timeout=30)
                if resp.status_code == 200 and len(resp.content) != 0:
                    for fh in self.file_header:
                        if resp.content.hex().startswith(fh):
                            icon_hash = mmh3.hash(base64.encodebytes(resp.content))
                            break
                break
            except Exception as e:
                log.debug(f'icon获取报错，错误信息 {e}')
                time.sleep(random.randint(1, 3))
                continue
        return icon_hash


icon = GetIconClass()
