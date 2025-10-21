#!/usr/bin/python
# coding=utf-8
import time
import requests
import redis
from bs4 import BeautifulSoup

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 设置最小的阈值
Default_Proxies_len = 10000

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}

# 获取ip总页数
def get_ip_page():
    print('proxies spider ihuan start ...')
    # 爬取多页数据
    for i in range(1, 6):  # 爬取前5页
        url = f'https://ip.ihuan.me/address/5Lit5Zu9.html?page={i}'
        get_url_list(url)
    print('proxies close and waiting ...')

# 获取url list
def get_url_list(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        bs = BeautifulSoup(response.text, 'html5lib')
        # 获取表格中的代理IP数据
        table = bs.find('table', attrs={'class': 'table table-hover table-bordered'})
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # 跳过表头
                cells = row.find_all('td')
                if len(cells) >= 2:
                    ip = cells[0].text.strip()
                    port = cells[1].text.strip()
                    proxies = f'http://{ip}:{port}'
                    print(proxies)
                    save_redis(proxies)
    except Exception as e:
        print(f"获取代理出错: {e}")

# 将采集的proxies存入redis
def save_redis(data_obj):
    r.rpush('proxies', data_obj)

# 获取proxies长度，如果小于阈值就重新采集
def get_proxieslen():
    proxieslen = r.llen('proxies')
    print('剩余代理池长度：', proxieslen)
    if proxieslen < Default_Proxies_len:
        get_ip_page()

if __name__ == "__main__":
    while True:
        get_proxieslen()
        time.sleep(30)
