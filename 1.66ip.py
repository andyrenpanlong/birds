#!/usr/bin/python
# coding=utf-8
import time
import requests
import redis
from bs4 import BeautifulSoup

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# r = redis.Redis(host='10.219.1.249', port=6379)
# r = redis.Redis(host='10.200.4.21', port=6379)

# 设置最小的阈值，默认20
Default_Proxies_len = 10000

# 获取ip总页数
def get_ip_page():
    print('proxies spider 66ip start ...')
    url = 'http://www.66ip.cn/1.html'
    try:
        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'html5lib')
        a_arr = bs.select('#PageList a')
        # print(a_arr)
        max_len = len(a_arr)
        max_num = int(a_arr[max_len - 2].text)
        for i in range(1, max_num + 1):
            url_2 = 'http://www.66ip.cn/{}.html'.format(i)
            get_url_list(url_2)
        print('proxies close and waiting ...')
    except:
        pass


# 获取url list
def get_url_list(url):
    try:
        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'html5lib')
        a_arr = bs.select('table')[2].select('tr')
        for i in a_arr:
            if 'ip' not in i.select('td')[0].text:
                proxies = 'http://{}:{}'.format(i.select('td')[0].text, i.select('td')[1].text)
                print(proxies)
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

# import time
# import requests
# import redis
# from bs4 import BeautifulSoup
#
# r = redis.Redis(host='localhost', port=6379, decode_responses=True)
#
# # 设置最小的阈值，默认20
# Default_Proxies_len = 10000
#
#
# # 获取ip总页数
# def get_ip_page():
#     print('proxies spider 66ip start ...')
#     url = 'http://www.66ip.cn/1.html'
#     try:
#         response = requests.get(url)
#         bs = BeautifulSoup(response.text, 'html5lib')
#         a_arr = bs.select('#PageList a')
#         # print(a_arr)
#         max_len = len(a_arr)
#         max_num = int(a_arr[max_len - 2].text)
#         for i in range(1, max_num + 1):
#             url_2 = 'http://www.66ip.cn/{}.html'.format(i)
#             get_url_list(url_2)
#         print('proxies close and waiting ...')
#     except:
#         pass
#
#
# # 获取url list
# def get_url_list(url):
#     try:
#         response = requests.get(url)
#         bs = BeautifulSoup(response.text, 'html5lib')
#         a_arr = bs.select('table')[2].select('tr')
#         for i in a_arr:
#             if 'ip' not in i.select('td')[0].text:
#                 proxies = 'http://{}:{}'.format(i.select('td')[0].text, i.select('td')[1].text)
#                 print(proxies)
#                 save_redis(proxies)
#     except:
#         pass
#
#
# # 将采集的proxies存入redis
# def save_redis(data_obj):
#     # 添加到列表左边rpushx（最右边）
#     # lpushx(name, value)只有键存在时，才添加。若键不存在则不添加，也不新创建列表
#     r.rpush('proxies', data_obj)
#     # 19.List lpop 删除左边的第一个值 rpop（右边）
#     # lpop(name) 返回值：被删除元素的值
#
#
# # 获取proxies长度，如果小于阈值就重新采集
# def get_proxieslen():
#     proxieslen = r.llen('proxies')
#     print('剩余代理池长度：', proxieslen)
#     if proxieslen < Default_Proxies_len:
#         get_ip_page()
#
#
# while True:
#     get_proxieslen()
#     time.sleep(30)
