import time
import requests
import redis
from bs4 import BeautifulSoup
import ssl
import certifi
import urllib3
ssl._create_default_https_context = ssl._create_unverified_context
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())
ssl_context.load_default_certs()
urllib3.disable_warnings()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 设置最小的阈值，默认20
Default_Proxies_len = 10000000
headers = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
url = 'https://ip.jiangxianli.com/?page=1'

# 获取ip总页数
def get_ip_page(url):
    print('proxies spider jiangxianli start ...', url)
    try:
        response = requests.get(url, headers=headers, verify=False)
        bs = BeautifulSoup(response.text, 'html5lib')
        a_arr = bs.select('.layui-table tr')
        for i in a_arr:
            if len(i.select('td')) > 4:
                if i.select('td')[3].text.strip() == 'HTTP':
                    proxies = 'http://{}:{}'.format(i.select('td')[0].text.replace('\r', '').replace('\n', '').replace('\t', '').strip(), i.select('td')[1].text.replace('\r', '').replace('\n', '').replace('\t', '').strip())
                    print(proxies)
                    save_redis(proxies)
        next_page = int(url.split('=')[1]) + 1
        if len(a_arr) > 0:
            url_2 = 'https://ip.jiangxianli.com/?page={}'.format(next_page)
            get_ip_page(url_2)
    except:
        pass

# 将采集的proxies存入redis
def save_redis(data_obj):
    # 添加到列表左边rpushx（最右边）
    # lpushx(name, value)只有键存在时，才添加。若键不存在则不添加，也不新创建列表
    r.rpush('proxies', data_obj)
    #19.List lpop 删除左边的第一个值 rpop（右边）
    # lpop(name) 返回值：被删除元素的值

# 获取proxies长度，如果小于阈值就重新采集
def get_proxieslen():
    proxieslen = r.llen('proxies')
    print('剩余代理池长度：', proxieslen)
    if proxieslen < Default_Proxies_len:
        get_ip_page(url)


while True:
    get_proxieslen()
    time.sleep(30)
