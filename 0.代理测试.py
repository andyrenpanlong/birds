import redis
import requests
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# r = redis.Redis(host='10.219.1.249', port=6379, decode_responses=True)
# r = redis.Redis(host='10.200.4.21', port=6379, decode_responses=True)

# 从redis读取代理ip
def get_proxies():
    # proxies{'要请求网站的协议类型' , '"代理服务器类型(http/https/socks5)://代理服务器ip : 端口 '}
    proxies = r.lpop('proxies')
    proxies_obj = {
        'http': proxies
    }
    return proxies_obj

# 获取代理
def get_test_proxie():
    proxies = get_proxies()
    print(proxies)
    # response = requests.get('www.baidu.com')
    # print(response.text)

# 清除全部代理
def clear_proxies():
    proxieslen = r.llen('proxies')
    for i in range(0, proxieslen):
        get_test_proxie()
    print('剩余代理池长度：', proxieslen)

def get_proxieslen():
    proxieslen = r.llen('proxies')
    print('剩余代理池长度：', proxieslen)

# while True:
#     get_proxieslen()
#     time.sleep(1)

clear_proxies()
