import time

import requests
from bs4 import BeautifulSoup

headers = {
    'authority': 'ebird.org',
    'method': 'GET',
    'path': '/region/world/bird-list?rank=lrec',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '_9bf17=44e806051217901; EBIRD_SESSIONID=21D9236552838908E02018ECF7575CDF; _08023=fdc604a7bd027d8d; I18N_LANGUAGE=zh-CN; is-region-session=eyJ1c2VyIjp7InVzZXJJZCI6IlVTRVI2MzMwMjYwIiwidXNlcm5hbWUiOiJyZW5wYW5sb25nIiwiZmlyc3ROYW1lIjoi5Lu7IiwibGFzdE5hbWUiOiLmvZjpvpkiLCJmdWxsTmFtZSI6IuS7uyDmvZjpvpkiLCJyb2xlcyI6W10sInByZWZzIjp7IlBSSVZBQ1lfUE9MSUNZX0FDQ0VQVEVEIjoidHJ1ZSIsIkFMRVJUU19PUFRfT1VUIjoiZmFsc2UiLCJFTUFJTF9DUyI6InRydWUiLCJESVNQTEFZX05BTUVfUFJFRiI6Im4iLCJWSVNJVFNfT1BUX09VVCI6InRydWUiLCJESVNQTEFZX0NPTU1PTl9OQU1FIjoidHJ1ZSIsIkRJU1BMQVlfU0NJRU5USUZJQ19OQU1FIjoiZmFsc2UiLCJTSE9XX0NPTU1FTlRTIjoiZmFsc2UiLCJUT1AxMDBfT1BUX09VVCI6InRydWUiLCJSRUdJT05fUFJFRiI6IndvcmxkIiwiQ09NTU9OX05BTUVfTE9DQUxFIjoiZW5fVVMiLCJzcHBQcmVmIjoiY29tbW9uIn19fQ==; is-region-session.sig=VOGoh-BNI0LrkLGJ2-Q8hfLumRU',
    'if-none-match': '"ec3eac-uGmzkrvY3Q9hiHiYYmCfi2JFvbs"',
    'priority': 'u=0, i',
    'referer': 'https://ebird.org/region/world/bird-list?yr=curM&rank=lrec',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}


def ebird_api():
    url = 'https://api.ebird.org/v2/ref/region/info/CH'
    headers = {
        'X-eBirdApiToken': '5mfpqd8njkpj',
    }
    response = requests.get(url, headers=headers)
    print(response.text)


def save_data(row):
    import csv
    with open('example2.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)


def save_detail(row):
    import csv
    with open('detail2.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)


def get_bird_url():
    import pymysql
    # 连接到 MySQL 数据库
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='12345678', database='spider')
    with connection.cursor() as cursor:
        # 执行查询语句，这里假设查询表名为 your_table 的所有数据
        sql = "SELECT * FROM spider.birds where url not in (select distinct url FROM spider.detail_2);"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row)
            bird_name = row[1]
            bird_url = row[2]
            bird_num = row[3]
            data_times = row[4]
            observer = row[5]
            data = [bird_name, bird_url, bird_num, data_times, observer]
            print('清单：', data)
            # bird_url = 'https://ebird.org/species/talrai1'
            # 获取详情，描述
            get_bird_detail(bird_url)

    # # 关闭连接
    # connection.close()


def save_pic(url, image_name):
    from PIL import Image
    from io import BytesIO
    # 图片的 URL
    # url = 'https://example.com/image.jpg'
    print('图片URL：', url, image_name)
    # 发送 GET 请求获取图片数据
    response = requests.get(url)
    # print('tup:', response.content)
    # 使用 BytesIO 将获取到的数据转换为字节流
    image_data = BytesIO(response.content)
    # 打开图片
    image = Image.open(image_data)
    # 如果图像是 RGBA 模式，则转换为 RGB 模式
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    # 将模式 P 转换为 RGB 模式
    if image.mode == 'P':
        image = image.convert('RGB')
    # 保存图片
    image.save('./imgs/{}.jpg'.format(image_name))


def get_bird_detail(url):
    # url = 'https://ebird.org/species/eutspa'
    # url = 'https://ebird.org/species/santer1'
    # url = 'https://ebird.org/species/louflo1'
    print('详情页：', url)
    # time.sleep(5)
    try:
        response = requests.get(url, headers=headers)
        # print(response.text)
        bs = BeautifulSoup(response.text, 'html5lib')
        bird_info = bs.select('#content')[0]
        first_name = bird_info.select('span')[0].text.strip()
        second_name = bird_info.select('span')[1].text.strip()
        bird_type = bs.select('#conservation-status')[0].text.strip()
        descript = bs.select('.u-stack-sm')[0].text.replace('\r', '').replace('\n', '').replace('\t', '').strip()
        pics = bs.select('.CarouselResponsive .CarouselResponsive-slide')
        if len(pics) < 1:
            # pics = bs.select('.ImageAspectRatio')
            pics = bs.select('.AspectRatioContent')
        print('图片数量：', len(pics))
        for i in range(0, len(pics)):
            print(pics[i])
            print(pics[i].select('img')[0].get('src'))
            try:
                pic_url = pics[i].select('img')[0].get('srcset').split()[-2]
            except:
                pic_url = pics[i].select('img')[0].get('data-srcset').split()[-2]
            image_name = '{}_{}'.format(first_name, i + 1)
            # save_pic(pic_url, image_name)
            row = [url, first_name, second_name, bird_type, descript, pic_url]
            save_detail(row)
            # print(first_name, second_name, bird_type, descript)
            print('1231341：', row)
    except:
        get_bird_detail(url)


get_bird_url()
# get_bird_detail('')
# save_pic('https://cdn.download.ams.birds.cornell.edu/api/v1/asset/219756941/2400', 'Reddish Scops-Owl_3')
