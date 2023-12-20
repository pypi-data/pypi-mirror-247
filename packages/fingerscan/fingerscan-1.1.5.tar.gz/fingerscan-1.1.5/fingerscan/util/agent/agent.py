"""
@Project ：指纹识别 
@File    ：agent.py
@IDE     ：PyCharm 
@Author  ：zhizhuo
@Date    ：2023/10/16 16:25 
"""
import json
import random
import re
import time
import warnings
from urllib.parse import urlparse, urljoin

import requests
from poc_tool.tools import tools
from urllib3.exceptions import InsecureRequestWarning

from util.core.icon import icon
from util.core.finger import finger
from util.core.finger import tcp_finger
from util.core.cdn import cdn
from util.core.cert import cert_ssl
from util.socket import SocketSend, redis_client
from poc_tool.log import log

# 解决requests的ssl证书warning提示
warnings.filterwarnings('ignore', category=InsecureRequestWarning)


class FingerAgent:
    """
    指纹识别agent
    """

    def __init__(self):
        """
        初始化数据
        """
        self.headers = {
            'Accept': 'application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, '
                      'application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
            'User-agent': tools.get_random_ua(),
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Connection': 'close'
        }

    @staticmethod
    def verify_data(url: str):
        """
        数据验证
        :param url:url地址
        :return:http or https url
        """
        if url.startswith(('http://', 'https://')):
            return url
        if url.endswith(':80'):
            return f'http://{url[:-3]}'
        if url.endswith(':443'):
            return f'https://{url[:-4]}'
        return f'https://{url}'

    @staticmethod
    def _get_title(res):
        """
        获取站点的title
        :param res:响应数据
        :return:json
        """
        try:
            title_list = re.findall(r'<title>(.*?)</title>', res.text, re.I | re.M | re.S)
            title = None if not title_list else str(title_list[0]).translate(str.maketrans("", "", "\r\n\t")).replace(
                "  ", "")
            log.debug(f"识别到title：{title}")
        except Exception as e:
            log.debug(f"识别title出错，{e}")
            title = None
        return title

    @staticmethod
    def _get_icon_url(url, html):
        """
        获取icon的url地址
        :param html:响应body数据流
        :return:url
        """
        # 解析URL
        parsed_url = urlparse(url)
        # 获取基础URL
        base_url = f'{parsed_url.scheme}://{parsed_url.netloc}/'
        # 默认favicon地址
        favicon_url = base_url + "favicon.ico"
        # icon_link_pattern = r'<link rel="(shortcut )?icon" .*?href="([^"]+)"'
        # matches = re.findall(icon_link_pattern, html, re.I | re.M | re.S)
        # if matches:
        #     favicon_path = matches[0][1]
        #     favicon_url = urljoin(base_url, favicon_path.lstrip('/'))
        # return favicon_url
        # 查找icon链接
        icon_index = html.find("<link rel=\"icon\"")
        # 查找shortcut icon链接
        shortcut_index = html.find("<link rel=\"shortcut icon\"")
        # 正则匹配所有href链接
        icon_list = re.findall('href="(.*?)">', html.replace(' ', ''), re.I | re.M | re.S)
        # 如果没有找到icon链接
        if icon_index == -1 and shortcut_index == -1:
            # 筛选出ico或icon后缀的链接
            image_extensions = ['ico', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'icon']
            ic = [ico for ico in icon_list if ico.split(".")[-1].lower() in image_extensions]
            # 如果有符合条件的链接，更新favicon地址
            if ic:
                favicon_url = base_url + ic[0]
        else:
            # 如果找到icon链接，获取该链接标签
            if icon_index != -1:
                link_tag = html[icon_index:html.find(">", icon_index)]
            else:
                # 如果找到shortcut icon链接，获取该链接标签
                link_tag = html[shortcut_index:html.find(">", shortcut_index)]
            # 从链接标签中提取favicon路径
            favicon_path = re.search('href="([^"]+)"', link_tag)
            if favicon_path:
                favicon_path = favicon_path.group(1)
                # 拼接完整的favicon URL
                favicon_url = urljoin(base_url, favicon_path.lstrip('/'))
        return favicon_url

    def _echo_data(self, url: str, resp: requests.models.Response):
        """
        处理生成最后的返回语句
        :param resp:response数据
        :return:json
        """
        redirect_url = url
        redirect_num = 0
        old_resp = resp
        if 300 <= resp.status_code < 400:
            redirect_num += 1
            redirect_url = resp.headers.get('Location', '/')
            redirect_url = urljoin(url, redirect_url)
            try:
                resp = requests.get(url=redirect_url, headers=self.headers, timeout=5, verify=False,
                                    allow_redirects=True)
            except Exception as e:
                log.debug(f"30X重定向失败 {e}")
                pass
        patterns = [
            (r"window.top.location.href='(.*?)';", 'window.top.location.href'),
            (r'window.location="(.*?)"', 'window.location'),
            (r'content=.*?;url=(.*?)>', '<meta http-equiv=refresh content='),
            (r'content=.*?;url=(.*?)"/>', '<meta http-equiv="refresh" content='),
            (r'content="0;URL=(.*?)">', 'content="0;URL=')
        ]
        black_js_redirect = ["script>", "\">", "href=", ".css", ".js", "><"]
        for pattern, text in patterns:
            if text in resp.text:
                redirect_url_list = re.findall(pattern, resp.text.replace(' ', ''), re.I | re.M | re.S)
                if redirect_url_list:
                    redirect_url = redirect_url_list[0].replace("'", "")
                    if all(substring not in redirect_url for substring in black_js_redirect):
                        redirect_url = urljoin(url, redirect_url.lstrip('/'))
                        redirect_num += 1
                        log.debug('js重定向:' + redirect_url)
                        if redirect_url.startswith("http://") and url.startswith("https://"):
                            redirect_url = url
                        else:
                            # js和30x重定向完成之后最后一次跟随重定向
                            try:
                                resp = requests.get(url=redirect_url, headers=self.headers, timeout=5, verify=False,
                                                    allow_redirects=True)
                            except Exception as e:
                                log.debug(f"30X重定向失败 {e}")
                                pass
                        break
                    else:
                        redirect_url = url
        resp.encoding = resp.apparent_encoding
        if (redirect_url.startswith("https://") and url.startswith("http://")) and 300 <= old_resp.status_code < 400:
            resp = old_resp
            redirect_url = url
        # 获取title
        title = self._get_title(resp)
        icon_hash = icon.get_icon_hash(self._get_icon_url(redirect_url, resp.text))
        cms = finger.get_finger(resp, dict(title=title, icon_hash=icon_hash))
        res_headers = tools.get_res_header(resp)
        server = resp.headers.get('Server')
        is_cdn = cdn.is_cdn(redirect_url)
        cert = cert_ssl.get_ssl_cert_info(redirect_url)
        return dict(title=title, redirect_num=redirect_num, url=redirect_url, icon_hash=icon_hash, cms=cms,
                    status_code=resp.status_code, server=server, is_cdn=is_cdn,
                    res_headers=res_headers, cert=cert)

    @staticmethod
    def _send_tcp(url, retries: int = 3):
        """
        发送tcp请求
        :param url:url
        :param retries:重试次数
        :return:json
        """
        _res = dict(header="", length=0, body="")
        host_list = cert_ssl.get_domain_info(url)
        host = host_list.get('host')
        port = host_list.get("port")
        is_ssl = host_list.get("is_ssl")
        for _ in range(retries):
            try:
                time.sleep(random.randint(1, 3))
                _res = SocketSend.send_tcp(host=host, port=port, is_ssl=is_ssl)
                break
            except Exception as e:
                log.debug(f"try error agent tcp {e}")
                continue
        return _res

    def _send_http(self, urls, retries: int = 3):
        """
        发送http请求
        :param urls:url
        :param retries:重试次数
        :return:json
        """
        url = self.verify_data(urls)
        is_cdn = cdn.is_cdn(url)
        result = None
        for _ in range(retries):
            try:
                resp = self._request_data(url)
                result = self._echo_data(url, resp)
                break
            except Exception as e:
                log.debug(f'http error {e}')
                time.sleep(random.randint(1, 3))
                continue
        if result is None:
            result = self._tcp_client(url, is_cdn)
            if not result.get('res_headers'):
                result = None
        return result

    def _send_https(self, url, retries: int = 3):
        """
        发送https请求
        :param url:url
        :param retries:重试次数
        :return:json
        """
        is_cdn = cdn.is_cdn(url)
        result = None
        for _ in range(retries):
            try:
                result = self._echo_data(url, self._request_data(url))
                break
            except Exception as e:
                log.debug(f'https error {e}')
                time.sleep(random.randint(1, 3))
                continue
        if result is None:
            result = self._tcp_client(url, is_cdn)
            if not result.get('res_headers'):
                result = None
        return result

    def _request_data(self, url):
        """
        http请求client
        :param url:url
        :return:response
        """
        return requests.get(url=url, headers=self.headers, allow_redirects=False, timeout=5, verify=False)

    @staticmethod
    def _get_tcp_res_status_code(res_headers):
        """
        获取TCP请求响应的状态码
        :param res_headers:tcp请求响应头
        :return:响应状态吗
        """
        server_info = None
        status_code = None
        http_version = None
        status_description = None
        if res_headers.startswith("HTTP"):
            lines = res_headers.split('\n')
            status_line = lines[0]
            parts = status_line.split(' ', 2)
            if len(parts) == 3:
                http_version, status_code, status_description = parts

            server_info = next((line.split("Server:")[1].strip() for line in lines if line.startswith('Server:')), None)
        return dict(http_version=http_version, status_code=status_code, status_description=status_description,
                    server=server_info)

    def _tcp_client(self, url, is_cdn):
        """
        tcp请求client
        :param url:url
        :param is_cdn:True or False
        :return:json
        """
        res = self._send_tcp(url)
        res_headers = res.get("header")
        server = self._get_tcp_res_status_code(res_headers).get("server")
        status_code = self._get_tcp_res_status_code(res_headers).get("status_code")
        finger_tcp = tcp_finger.get_tcp_finger(res)
        title = finger_tcp.get("title")
        cms = finger_tcp.get("cms")
        return dict(title=title, redirect_num=0,
                    url=url,
                    icon_hash=None,
                    cms=cms,
                    status_code=status_code, server=server, is_cdn=is_cdn,
                    res_headers=res_headers, cert=dict())

    def _verify_server(self, url, result):
        """
        协议验证
        :param url:url地址
        :param result:请求识别结果
        :return:json
        """
        if result is None:
            return None
        cms = result.get("cms")
        res_headers = result.get("res_headers")
        scheme = None
        if cms == "Redis":
            log.debug("try client redis to get data")
            redis_url = result.get("url")
            if redis_url:
                res = json.loads(redis_client.send_redis_tcp(self.verify_data(redis_url)))
                result.update({"title": None, "res_headers": res.get("header")})
        if res_headers and res_headers.startswith("HTTP"):
            scheme_url = result.get("url")
            if scheme_url and scheme_url.startswith('http'):
                scheme = urlparse(scheme_url).scheme
        result.update(dict(scheme=scheme, host=urlparse(url).netloc))
        return result

    def _http_scan(self, url):
        """
        http格式的数据请求
        :param url:url地址
        :return:json
        """
        if url.endswith(':443'):
            return None
        url = self.verify_data(url).replace('https://', 'http://')
        log.debug(f'http scan url: {url}')
        return self._verify_server(url, self._send_http(url))

    def _https_scan(self, url):
        """
        https格式的数据请求
        :param url:url地址
        :return:json
        """
        if url.endswith(':80'):
            return None
        url = self.verify_data(url).replace('http://', 'https://')
        log.debug(f'https scan url: {url}')
        return self._verify_server(url, self._send_https(url))

    def run(self, url):
        """
        指纹扫描的启动函数
        :param url:url
        :return:json
        """
        # 这里http和https都进行扫描，优先扫描https，http的tcp请求和https的tcp属于同一种类型，
        # 如果res_headers为空，默认返回None
        result = [self._https_scan(url), self._http_scan(url)]
        # result = [self._https_scan(url)]
        return json.dumps(list(filter(None, result)), ensure_ascii=False)


agent = FingerAgent()
