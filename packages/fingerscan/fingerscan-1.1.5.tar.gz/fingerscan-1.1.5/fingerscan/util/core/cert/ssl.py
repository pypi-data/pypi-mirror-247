"""
@Project ：指纹识别 
@File    ：ssl.py
@IDE     ：PyCharm
@Author  ：zhizhuo
@Date    ：2023/10/19 10:16
"""
import random

import OpenSSL
import socket
import hashlib
import time
from urllib.parse import urlparse
from poc_tool.log import log


class GetSSLInfoClass:
    """
    获取ssl证书信息
    """

    def __init__(self):
        """
        初始化数据
        """

    # def test_ssl_cert_info(self, host, port):
    #     context = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
    #     conn = OpenSSL.SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    #     conn.connect((host, 443))
    #     conn.do_handshake()
    #     cert = conn.get_peer_certificate()
    #
    #     issuer_components = cert.get_issuer().get_components()
    #     issuer_info = {component[0].decode("UTF-8"): component[1].decode("UTF-8") for component in issuer_components}
    #
    #     cert_info = {
    #         '版本': str(cert.get_version() + 1),
    #         '序列号': str(cert.get_serial_number()),
    #         '组织信息': str(cert.get_subject().organizationName),
    #         '颁发机构': issuer_info,
    #         '颁发者': str(cert.get_issuer().commonName),
    #         '有效期从': str(cert.get_notBefore().decode()),
    #         '过期时间': str(cert.get_notAfter().decode()),
    #         '是否过期': str(cert.has_expired()),
    #         '主题': str(cert.get_subject().CN),
    #         '证书中使用的签名算法': cert.get_signature_algorithm().decode("UTF-8"),
    #         '公钥长度': cert.get_pubkey().bits(),
    #         '公钥': OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey()).decode("utf-8"),
    #         '公钥SHA256指纹': hashlib.sha256(
    #             OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())).hexdigest(),
    #         '证书SHA256指纹': hashlib.sha256(
    #             OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)).hexdigest(),
    #     }
    #
    #     return cert_info

    @staticmethod
    def get_domain_info(domain):
        """
        获取url中的host地址和端口号
        :param domain:
        :return:
        """
        is_ssl = False
        port = 443
        parsed_url = urlparse(domain)
        if parsed_url.port:
            if parsed_url.scheme == "https":
                is_ssl = True
            port = parsed_url.port
        elif parsed_url.scheme == "https" and parsed_url.port is None:
            port = 443
            is_ssl = True
        elif parsed_url.scheme == "http" and parsed_url.port is None:
            port = 80
        return dict(host=parsed_url.hostname, port=port, is_ssl=is_ssl)

    def get_ssl_cert_info(self, url, retries: int = 3, timeout: int = 10):
        """
        获取ssl证书信息
        :param url:url地址
        :param retries:重试次数
        :param timeout:请求超时时间（秒）
        :return:json
        """
        for _ in range(retries):
            try:
                domain = self.get_domain_info(url)
                host = domain.get('host')
                port = domain.get('port')
                if str(port) == '80' or url.startswith('http://'):
                    break
                log.debug(f"获取ssl证书 {host} {port}")
                context = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
                conn = OpenSSL.SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                conn.settimeout(timeout)
                conn.connect((host, port))
                conn.do_handshake()
                cert = conn.get_peer_certificate()

                issuer_components = cert.get_issuer().get_components()
                issuer_info = {component[0].decode("UTF-8"): component[1].decode("UTF-8") for component in
                               issuer_components}

                return dict(
                    version=str(cert.get_version() + 1),
                    serial_number=str(cert.get_serial_number()),
                    organization_info=str(cert.get_subject().organizationName),
                    issuer_info=issuer_info,
                    issuer=str(cert.get_issuer().commonName),
                    valid_from=str(cert.get_notBefore().decode()),
                    expiration_date=str(cert.get_notAfter().decode()),
                    is_expired=str(cert.has_expired()),
                    subject=str(cert.get_subject().CN),
                    signature_algorithm=cert.get_signature_algorithm().decode("UTF-8"),
                    public_key_length=cert.get_pubkey().bits(),
                    public_key=OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey()).decode(
                        "utf-8"),
                    public_key_sha256_fingerprint=hashlib.sha256(
                        OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey())).hexdigest(),
                    certificate_sha256_fingerprint=hashlib.sha256(
                        OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)).hexdigest(),
                )
            except OpenSSL.SSL.Error:
                break
            except Exception as e:
                log.debug(f'ssl error {e}')
                time.sleep(random.randint(1, 3))
                continue
        return dict()


cert_ssl = GetSSLInfoClass()
