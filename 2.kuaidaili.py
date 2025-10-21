import json
import math
import time
import requests
import redis
from bs4 import BeautifulSoup

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 设置最小的阈值，默认20
Default_Proxies_len = 1000000

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.kuaidaili.com',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}


# 获取ip总页数
def get_ip_page():
    print('proxies spider kuaidaili start ...')
    url = 'https://www.kuaidaili.com/free/inha/'
    try:
        response = requests.get(url, headers=headers)
        bs = BeautifulSoup(response.text, 'html5lib')
        num_all = 0
        for i in bs.select('script'):
            if 'let totalCount =' in str(i):
                for j in str(i).split('\n'):
                    if 'let totalCount =' in j:
                        num_all = j.split(';')[0].split('=')[1].replace("'", '')
        page_all = math.ceil(int(num_all) / 12) + 1
        print('213123:', page_all, num_all)
        for i in range(1, page_all):
            url_2 = 'https://www.kuaidaili.com/free/inha/{}/'.format(i)
            get_url_list(url_2)
        print('proxies close and waiting ...')
    except:
        pass

# 获取url list
def get_url_list(url):
    try:
        response = requests.get(url, headers=headers)
        bs = BeautifulSoup(response.text, 'html5lib')
        a_arr = bs.select('script')
        for i in a_arr:
            for j in str(i).split('\n'):
                if 'const fpsList' in j:
                    fpsList = json.loads(str(j).replace('const fpsList = ', '').replace(';', ''))
                    for k in fpsList:
                        proxies = 'http://{}:{}'.format(k['ip'], k['port'])
                        print(k, proxies)
                        save_redis(proxies)
    except:
        pass


# 将采集的proxies存入redis
def save_redis(data_obj):
    # 添加到列表左边rpushx（最右边）
    # lpushx(name, value)只有键存在时，才添加。若键不存在则不添加，也不新创建列表
    r.rpush('proxies', data_obj)
    # 19.List lpop 删除左边的第一个值 rpop（右边）
    # lpop(name) 返回值：被删除元素的值


# 获取proxies长度，如果小于阈值就重新采集
def get_proxieslen():
    proxieslen = r.llen('proxies')
    print('剩余代理池长度：', proxieslen)
    if proxieslen < Default_Proxies_len:
        get_ip_page()


while True:
    get_proxieslen()
    time.sleep(30)
