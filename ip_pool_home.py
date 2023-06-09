# 建立属于自己的开放代理IP池
import requests
import random
import time

from fake_useragent import UserAgent
from lxml import etree
from fake_user_agent import user_agent



class IpPool:
    def __init__(self):
        self.test_url = 'http://httpbin.org/get'  # 测试ip是否可用的 url
        self.url = 'https://www.89ip.cn/index_{}.html'   # 获取IP的目标 url
        self.headers = {'User-Agent': UserAgent(verify_ssl=False).random}   # 获取随机的UA
        self.file = open('ip_pool_home.txt', 'a+')  # 存储可用的ip

    def get_html(self, url):
        '''获取页面'''
        html = requests.get(url=url, headers=self.headers).text

        return html

    def get_proxy(self, url):
        # 获取ip 和端口
        html = self.get_html(url=url)
        elemt = etree.HTML(html)

        ips_list = elemt.xpath('//table/tbody/tr/td[1]/text()')
        ports_list = elemt.xpath('//table/tbody/tr/td[2]/text()')

        for ip, port in zip(ips_list, ports_list):
            # 拼接ip与port
            proxy = ip.strip() + ":" + port.strip()
            self.test_proxy(proxy)

    def test_proxy(self, proxy):
        """
        测试代理IP是否可用
        # 参数类型
        # proxies = {'协议': '协议://IP:端口号'}
        # timeout 超时设置 网页响应时间3秒 超过时间会抛出异常
        """
        proxies = {
            'http': 'http://{}'.format(proxy),
            'https': 'https://{}'.format(proxy),
        }
        try:
            resp = requests.get(url=self.test_url, proxies=proxies, headers=self.headers, timeout=3)
            # 状态码为200 的就写入文件并输出到控制台
            if resp.status_code == 200:
                print(proxy, '\033[31m可用\033[0m')
                self.file.write(proxy + '\n')     # 可以的IP 写入文本以便后续使用，写入后换行
            else:
                print(proxy, '不可用')
        except Exception as e:
            print(proxy, '不可用')

    # 执行函数
    def crawl(self):
        # 这里只获取前150页提供的免费代理IP测试
        for i in range(1, 150):
            page_url = self.url.format(i)  # 拼接完整的url
            time.sleep(random.randint(1, 4))  # 控制抓取频率
            self.get_proxy(url=page_url)

        # 执行完毕关闭文本
        self.file.close()


if __name__ == '__main__':
    ip = IpPool()
    ip.crawl()
