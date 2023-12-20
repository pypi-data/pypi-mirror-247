"""
@Project ：指纹识别 
@File    ：tcp_finger.py
@IDE     ：PyCharm 
@Author  ：zhizhuo
@Date    ：2023/10/19 12:32 
"""
import re
from poc_tool.log import log


class TcpFingerClass:
    """
    tcp通信的结果指纹判断
    """

    def __init__(self):
        """
        初始化配置信息
        """

    @staticmethod
    def _get_finger_title(data):
        """
        获取title信息
        :param data:body数据
        :return:str
        """
        title = None
        try:
            if data is not None:
                title_list = re.findall(r'<title>(.*?)</title>', data, re.I | re.M | re.S)
                title = None if not title_list else str(title_list[0]).translate(
                    str.maketrans("", "", "\r\n\t")).replace(
                    "  ", "")
        except Exception as e:
            log.debug(f"获取tcp请求结果title出错 {e}")
            title = None
        return title

    def get_tcp_finger(self, res):
        """
        获取tcp响应指纹数据
        :param res:tcp 返回数据包json格式
        :return:json
        """
        _cms = None
        header = res.get("header")
        body = res.get("body")
        _title = self._get_finger_title(body)
        if _title is None:
            res.update({"header": ""})
        if 'SSH' in header:
            _cms = 'SSH'
        elif 'FTP' in header:
            _cms = 'FTP'
        elif 'mysql' in header or 'MYSQL' in header or 'MySQL' in header:
            _cms = "MYSQL"
        elif 'DENIED Redis' in header or 'CONFIG REWRITE' in header or 'NOAUTH Authentication' in header:
            _cms = "Redis"
        log.debug(f"tcp 命中指纹 {_cms}")
        return dict(cms=_cms, title=_title)


tcp_finger = TcpFingerClass()
