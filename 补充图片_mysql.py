import json

import requests
from bs4 import BeautifulSoup


url = 'https://media.ebird.org/api/v2/search?mediaType=photo&taxonCode=chtjuf1&birdOnly=true&initialCursorMark=MjAyNC0wNC0wOVQxMjo1Nzo1MS4yMTkwMjJfXzYxNzEzODQyMw'


url2 = 'https://media.ebird.org/api/v2/search?mediaType=photo&taxonCode=chtjuf1&birdOnly=true&initialCursorMark=MjAyMy0xMi0xN1QwMzo1MTo1My44OTkyMTJfXzYxMjMyNTc1OQ'


url3 = 'https://media.ebird.org/api/v2/search?mediaType=photo&taxonCode=chtjuf1&birdOnly=true&initialCursorMark=MjAyMy0xMC0wOFQyMjowMDoxMS42OTYxMjBfXzYwOTczMjUyOA'


headers = {
    'x-xss-protection': '0',
    'authority': 'media.ebird.org',
    'method': 'GET',
    'path': '/api/v2/search?mediaType=photo&taxonCode=chtjuf1&birdOnly=true&initialCursorMark=MjAyMy0xMC0wOFQyMjowMDoxMS42OTYxMjBfXzYwOTczMjUyOA',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_d0371=b9f60534702d9ec8; i18n_redirected=en; ml-search-session=eyJ1c2VyIjp7InVzZXJJZCI6IlVTRVI2MzMwMjYwIiwidXNlcm5hbWUiOiJyZW5wYW5sb25nIiwiZmlyc3ROYW1lIjoi5Lu7IiwibGFzdE5hbWUiOiLmvZjpvpkiLCJmdWxsTmFtZSI6IuS7uyDmvZjpvpkiLCJyb2xlcyI6W10sInByZWZzIjp7IlBSSVZBQ1lfUE9MSUNZX0FDQ0VQVEVEIjoidHJ1ZSIsIkFMRVJUU19PUFRfT1VUIjoiZmFsc2UiLCJFTUFJTF9DUyI6InRydWUiLCJESVNQTEFZX05BTUVfUFJFRiI6Im4iLCJWSVNJVFNfT1BUX09VVCI6InRydWUiLCJESVNQTEFZX0NPTU1PTl9OQU1FIjoidHJ1ZSIsIkRJU1BMQVlfU0NJRU5USUZJQ19OQU1FIjoiZmFsc2UiLCJTSE9XX0NPTU1FTlRTIjoiZmFsc2UiLCJUT1AxMDBfT1BUX09VVCI6InRydWUiLCJSRUdJT05fUFJFRiI6IndvcmxkIiwiQ09NTU9OX05BTUVfTE9DQUxFIjoiZW5fVVMiLCJzcHBQcmVmIjoiY29tbW9uIn19fQ==; ml-search-session.sig=0aFpoqpqf46_87kUxKD-zIIHcwY',
    'priority': 'u=1, i',
    'referer': 'https://media.ebird.org/catalog?mediaType=photo&taxonCode=chtjuf1',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

def save_json(data_to_write):
    with open('data.json', 'a+') as file:
        # 将文件指针移动到文件开头，以便读取现有内容
        file.seek(0)
        try:
            existing_data = json.load(file)
        except json.JSONDecodeError:
            # 如果文件为空或格式不正确，初始化一个空的数据结构（例如空列表或字典）
            existing_data = []

        # 将新数据添加到现有数据中
        if isinstance(existing_data, list):
            existing_data.append(data_to_write)
        elif isinstance(existing_data, dict):
            key = "new_key"
            existing_data[key] = data_to_write

        # 将文件指针移动回文件末尾，准备写入更新后的数据
        file.seek(0, 2)
        json.dump(existing_data, file, indent=4)

def save_data(row):
    import csv
    with open('pic_message.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def get_bird_url(url, keywords, bird_name):
    try:
        print('请求地址：', url, keywords, bird_name)
        response = requests.get(url, headers=headers)
        # print(response.text)
        data_list = json.loads(response.text)
        for i in data_list:
            print('13124:', i)
            assetId = i['assetId']
            category = str(i['taxonomy']['category']).replace(',', '，').replace('\r', '').replace('\n', '').replace('\t', '')
            comName = str(i['taxonomy']['comName']).replace(',', '，').replace('\r', '').replace('\n', '').replace('\t', '')
            reportAs = str(i['taxonomy']['reportAs']).replace(',', '，').replace('\r', '').replace('\n', '').replace('\t', '')
            sciName = str(i['taxonomy']['sciName']).replace(',', '，').replace('\r', '').replace('\n', '').replace('\t', '')
            speciesCode = str(i['taxonomy']['speciesCode']).replace(',', '，').replace('\r', '').replace('\n', '').replace('\t', '')
            userDisplayName = str(i['userDisplayName']).replace(',', '，').replace('\r', '').replace('\n', '').replace('\t', '')
            userId = str(i['userId']).replace(',', '，').replace('\r', '').replace('\n', '').replace('\t', '')
            countryCode = str(i['location']['countryCode']).replace(',', '，').replace('\r', '').replace('\n', '').replace('\t', '')
            countryName = str(i['location']['countryName']).replace(',', '，').replace('\r', '').replace('\n', '').replace('\t', '')
            bird_imgs_url_480 = 'https://cdn.download.ams.birds.cornell.edu/api/v2/asset/{}/480'.format(assetId)
            bird_imgs_url_640 = 'https://cdn.download.ams.birds.cornell.edu/api/v2/asset/{}/640'.format(assetId)
            bird_imgs_url_900 = 'https://cdn.download.ams.birds.cornell.edu/api/v2/asset/{}/900'.format(assetId)
            bird_imgs_url_1200 = 'https://cdn.download.ams.birds.cornell.edu/api/v2/asset/{}/1200'.format(assetId)
            bird_imgs_url_1800 = 'https://cdn.download.ams.birds.cornell.edu/api/v2/asset/{}/1800'.format(assetId)
            bird_imgs_url_2400 = 'https://cdn.download.ams.birds.cornell.edu/api/v2/asset/{}/2400'.format(assetId)
            pdata = [keywords, assetId, category, comName, reportAs, sciName, speciesCode, userDisplayName, userId, countryCode, countryName, bird_name, bird_imgs_url_480, bird_imgs_url_640, bird_imgs_url_900, bird_imgs_url_1200, bird_imgs_url_1800, bird_imgs_url_2400]
            print('pdata:', pdata)
            save_data(pdata)
            # i['keywords1'] = keywords
            # i['bird_name1'] = bird_name
            # print('json_data:', i)
            # save_json(i)
    except:
        get_bird_url(url, keywords, bird_name)


# 品类名称
# keywords = 'chtjuf1'

# 获取第一页
# get_bird_url(url, keywords)

# 获取第二页
# get_bird_url(url2, keywords)


def get_birds_list():
    import pymysql
    # 连接到 MySQL 数据库
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='12345678', database='spider')
    with connection.cursor() as cursor:
        # 执行查询语句，这里假设查询表名为 your_table 的所有数据
        sql = "SELECT * FROM spider.birds where url not in (SELECT distinct CONCAT_WS('', 'https://ebird.org/species/', keywords_1) as url FROM spider.pic_message);"
        cursor.execute(sql)
        results = cursor.fetchall()
        print('剩余的长度：', len(results))
        for row in results:
            print(row)
            bird_name = row[1]
            bird_url = row[2]
            bird_num = row[3]
            data_times = row[4]
            observer = row[5]
            data = [bird_name, bird_url, bird_num, data_times, observer]
            print('清单：', data)
            keywords = bird_url.split('/')[-1]
            url_1 = 'https://media.ebird.org/api/v2/search?mediaType=photo&taxonCode={}&birdOnly=true&initialCursorMark=MjAyNC0wNC0wOVQxMjo1Nzo1MS4yMTkwMjJfXzYxNzEzODQyMw'.format(keywords)
            url_2 = 'https://media.ebird.org/api/v2/search?mediaType=photo&taxonCode={}&birdOnly=true&initialCursorMark=MjAyMy0xMi0xN1QwMzo1MTo1My44OTkyMTJfXzYxMjMyNTc1OQ'.format(keywords)
            url_3 = 'https://media.ebird.org/api/v2/search?mediaType=photo&taxonCode={}&birdOnly=true'.format(keywords)
            # 获取第一页
            get_bird_url(url_1, keywords, bird_name)
            # 获取第二页
            get_bird_url(url_2, keywords, bird_name)
            # 获取第0页，珍稀鸟类图片较少
            get_bird_url(url_3, keywords, bird_name)


get_birds_list()