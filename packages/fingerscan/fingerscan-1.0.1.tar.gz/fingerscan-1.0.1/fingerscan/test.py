import base64
import json
from concurrent.futures import ThreadPoolExecutor

from util.socket import SocketSend, redis_client
from urllib.parse import urlparse, urljoin

import requests
import hashlib
import mmh3
import base64
from poc_tool.tools import tools
from util.agent import agent
from util.core.finger import finger
from util.core.cert import cert_ssl


def main(url):
    """
    socke TCP通信测试方法
    :param url:url地址
    :return:json
    """
    host_list = cert_ssl.get_domain_info(url)
    host = host_list.get('host')
    port = host_list.get('port')
    is_ssl = host_list.get('is_ssl')
    print(is_ssl)
    # try:
    data = SocketSend.send_tcp(host, port, is_ssl)
    if data:
        print(json.dumps(data, indent=4))
        print('\n')
        print(data.get('header'))
        print(data.get('body'))
    else:
        print("调用失败")
    # except Exception as e:
    #     print(e)


def is_rdp(ip, port):
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, int(port)))  # Convert port to integer
        print(123123123123123, result)
        sock.close()
        if result == 0:
            return True
        else:
            return False
    except socket.error as error:
        print("Socket connection error: " + str(error))
        return False


def test_finger():
    config = {"host": "222.92.101.93", "status": 1,
              "result": [{"port": "801/tcp", "status": "open", "service": "device", "scan_type": "syn-ack"},
                         {"port": "1006/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "1007/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "2089/tcp", "status": "open", "service": "sep", "scan_type": "syn-ack"},
                         {"port": "6379/tcp", "status": "open", "service": "redis", "scan_type": "syn-ack"},
                         {"port": "6602/tcp", "status": "open", "service": "wsscomfrmwk", "scan_type": "syn-ack"},
                         {"port": "6603/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "6604/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "6605/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "6607/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "6609/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "6616/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "8003/tcp", "status": "open", "service": "mcreport", "scan_type": "syn-ack"},
                         {"port": "8081/tcp", "status": "open", "service": "blackice-icecap", "scan_type": "syn-ack"},
                         {"port": "8082/tcp", "status": "open", "service": "blackice-alerts", "scan_type": "syn-ack"},
                         {"port": "8848/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "8989/tcp", "status": "open", "service": "sunwebadmins", "scan_type": "syn-ack"},
                         {"port": "9001/tcp", "status": "open", "service": "tor-orport", "scan_type": "syn-ack"},
                         {"port": "9002/tcp", "status": "open", "service": "dynamid", "scan_type": "syn-ack"},
                         {"port": "11527/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "18081/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "36888/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "36999/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "40001/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "40002/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "50000/tcp", "status": "open", "service": "ibm-db2", "scan_type": "syn-ack"},
                         {"port": "50044/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
                         {"port": "50048/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"}]}
    # config = {"host": "180.97.199.237", "status": 1,
    #           "result": [{"port": "81/tcp", "status": "open", "service": "hosts2-ns", "scan_type": "syn-ack"},
    #                      {"port": "84/tcp", "status": "open", "service": "ctf", "scan_type": "syn-ack"},
    #                      {"port": "3080/tcp", "status": "open", "service": "stm_pproc", "scan_type": "syn-ack"},
    #                      {"port": "5002/tcp", "status": "open", "service": "rfe", "scan_type": "syn-ack"},
    #                      {"port": "5007/tcp", "status": "open", "service": "wsm-server-ssl", "scan_type": "syn-ack"},
    #                      {"port": "8180/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "8788/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "8888/tcp", "status": "open", "service": "sun-answerbook", "scan_type": "syn-ack"},
    #                      {"port": "8991/tcp", "status": "open", "service": "https-wmap", "scan_type": "syn-ack"},
    #                      {"port": "8997/tcp", "status": "open", "service": "oracle-ms-ens", "scan_type": "syn-ack"},
    #                      {"port": "9000/tcp", "status": "open", "service": "cslistener", "scan_type": "syn-ack"},
    #                      {"port": "9002/tcp", "status": "open", "service": "dynamid", "scan_type": "syn-ack"},
    #                      {"port": "9003/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9004/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9005/tcp", "status": "open", "service": "golem", "scan_type": "syn-ack"},
    #                      {"port": "9006/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9007/tcp", "status": "open", "service": "ogs-client", "scan_type": "syn-ack"},
    #                      {"port": "9008/tcp", "status": "open", "service": "ogs-server", "scan_type": "syn-ack"},
    #                      {"port": "9009/tcp", "status": "open", "service": "pichat", "scan_type": "syn-ack"},
    #                      {"port": "9010/tcp", "status": "open", "service": "sdr", "scan_type": "syn-ack"},
    #                      {"port": "9011/tcp", "status": "open", "service": "d-star", "scan_type": "syn-ack"},
    #                      {"port": "9012/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9014/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9015/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9016/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9017/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9018/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9019/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9020/tcp", "status": "open", "service": "tambora", "scan_type": "syn-ack"},
    #                      {"port": "9021/tcp", "status": "open", "service": "panagolin-ident", "scan_type": "syn-ack"},
    #                      {"port": "9022/tcp", "status": "open", "service": "paragent", "scan_type": "syn-ack"},
    #                      {"port": "9023/tcp", "status": "open", "service": "swa-1", "scan_type": "syn-ack"},
    #                      {"port": "9024/tcp", "status": "open", "service": "swa-2", "scan_type": "syn-ack"},
    #                      {"port": "9025/tcp", "status": "open", "service": "swa-3", "scan_type": "syn-ack"},
    #                      {"port": "9027/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9028/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9029/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9031/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9032/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9033/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9034/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9035/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9036/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9040/tcp", "status": "open", "service": "tor-trans", "scan_type": "syn-ack"},
    #                      {"port": "9041/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9042/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9090/tcp", "status": "open", "service": "zeus-admin", "scan_type": "syn-ack"},
    #                      {"port": "9980/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "9998/tcp", "status": "open", "service": "distinct32", "scan_type": "syn-ack"},
    #                      {"port": "10002/tcp", "status": "open", "service": "documentum", "scan_type": "syn-ack"},
    #                      {"port": "10004/tcp", "status": "open", "service": "emcrmirccd", "scan_type": "syn-ack"},
    #                      {"port": "12907/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"},
    #                      {"port": "18081/tcp", "status": "open", "service": "unknown", "scan_type": "syn-ack"}],
    #           "start_time": "2023-10-23 11:46:57.178349+00:00", "end_time": "2023-10-23 11:47:20.200960+00:00"}
    host = config.get("host")
    port_list = config.get("result")
    print(len(port_list))
    result_data = list()
    if len(port_list) > 0:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for port in port_list:
                url = host + ":" + port.get("port").split("/")[0]
                futures.append(executor.submit(agent.run, url))
            for future in futures:
                res = future.result()
                print('结果', res)
                result_data.append(dict(finger=json.loads(res)))
    print("运行结束=====")
    return json.dumps(
        [dict(finger=item) for entry in result_data if entry.get('finger') for item in entry.get('finger')],
        ensure_ascii=False)


def udp_test():
    send_data = "test"
    res = SocketSend.send_udp('2.35.116.13', 62201, is_ssl=False, send_data=send_data)
    print(res)


def tcp_test():
    res = SocketSend.send_tcp('180.97.199.237', 9042, is_ssl=False)
    print(res)


def header_hash(url):
    # url = 'http://' + url
    url = "https://hcintg-nacos.meitiancars.com/nacos"
    url = urljoin(url, '/')
    print(url)
    resp = requests.get(url)
    header = tools.get_res_header(resp).encode()
    print(tools.get_res_header(resp))
    print(header.decode())
    hash = mmh3.hash(base64.encodebytes(header))
    print(hash)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # print(udp_test())
    # print(tcp_test())
    # print(test_finger())
    print("====运行结束=====")
    # host = "101.42.156.174"
    # host = "217.91.14.163"
    # host = "127.0.0.1"
    # port = 8080
    # print(tools.get_random_ua())
    # main(host, port)
    # print(get_icon_hash("https://www.baidu.com"))
    test = "www.baidu.com"
    # test = "http://192.168.5.210:8080"
    # test = "ik.smile-space.com:655"
    # test = "https://www.butian.net/"
    # test = "101.42.156.174:6379"
    # test = "https://www.ksgh.org/"
    # test = "https://ztsit.hbunion.com:9443"
    # test = "cbt1.szcu.edu.cn:80"
    # test = "117.185.252.44:3089"
    # print(redis_client.send_redis_tcp("http://" + test))
    # print(is_rdp("ik.smile-space.com", "33899"))
    # test = "58.210.186.80:9443"
    # test = "34.36.219.238"
    # test = "www.cetc.com.cn"
    # test = "oa.hypergryph.com:1443"
    result = agent.run(test)
    print(result)
    # test = "http://172.18.7.15:10811"
    # result = agent.test(test)
    # result = main(test)
    # print(result)
    # result = json.loads(result)
    # print(f"命中指纹：{result.get('cms')}")
    # print(result.get('res_headers'))
    # print(finger.get_finger(1))
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
