import time
import requests
import redis
from bs4 import BeautifulSoup

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 设置最小的阈值，默认20
# Default_Proxies_len = 10000000
Default_Proxies_len = 1000

url = 'https://www.89ip.cn/index_1.html'

# 获取ip总页数
def get_ip_page(url):
    print('proxies spider 89IP start ...', url)
    try:
        response = requests.get(url)
        # print(response.text)
        bs = BeautifulSoup(response.text, 'html5lib')
        a_arr = bs.select('.layui-table tbody tr')
        next_page = bs.select('.layui-laypage-next')[0].get('href')
        max_len = len(a_arr)
        for i in a_arr:
            proxies = 'http://{}:{}'.format(i.select('td')[0].text.replace('\r', '').replace('\n', '').replace('\t', '').strip(), i.select('td')[1].text.replace('\r', '').replace('\n', '').replace('\t', '').strip())
            print(proxies)
            save_redis(proxies)
        # print(max_len, next_page, bs.select('.layui-laypage-next'))
        if max_len > 0:
            url_2 = 'https://www.89ip.cn/{}'.format(next_page)
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
