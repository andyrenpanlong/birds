import pymysql
import pandas as pd

# 连接到 MySQL 数据库
connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='12345678', database='spider')

# 创建游标对象
cursor = connection.cursor()

def base_bird_table():
    # 读取 CSV 文件
    data = pd.read_csv('example.csv')
    # # 假设你的表名为 your_table，列名与 CSV 文件中的列名对应
    # for index, row in data.iterrows():
    #     query = "INSERT INTO birds (bird_name, url, num, date_time, author) VALUES (%s, %s, %s, s, %s)"
    #     values = (row['bird_name'], row['url'], row['num'], row['date_time'], row['author'])
    #     print(values)
    #     cursor.execute(query, values)

    # 假设你的表名为 your_table，列名与 CSV 文件中的列名对应
    values_list = []
    for index, row in data.iterrows():
        bird_name = str(row['bird_name']).strip()
        url = str(row['url']).strip()
        num = str(row['num']).replace('# 数量:  ', '').strip()
        date_time = str(row['date_time']).strip()
        author = str(row['author']).replace('观察者:  ', '').strip()
        if author != 'nan':
            author = author
        else:
            author = ''
        values = (bird_name, url, num, date_time, author)
        values_list.append(values)

    # 使用 executemany 进行批量插入
    query = "INSERT INTO birds (bird_name, url, num, date_time, author) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(query, values_list)

    # 提交事务
    connection.commit()

    # 关闭游标和连接
    cursor.close()
    connection.close()


def base_detail_1_table():
    # 读取 CSV 文件
    data = pd.read_csv('detail.csv')

    # 假设你的表名为 your_table，列名与 CSV 文件中的列名对应
    values_list = []
    for index, row in data.iterrows():
        url = str(row['url']).strip()
        first_name = str(row['first_name']).strip()
        second_name = str(row['second_name']).strip()
        bird_type = str(row['bird_type']).strip()
        descript = str(row['descript']).replace('\r', '').replace('\n', '').replace('\t', '').strip()
        values = (url, first_name, second_name, bird_type, descript)
        values_list.append(values)

    # 使用 executemany 进行批量插入
    query = "INSERT INTO detail_1 (url, first_name, second_name, bird_type, descript) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(query, values_list)

    # 提交事务
    connection.commit()

    # 关闭游标和连接
    cursor.close()
    connection.close()


# base_detail_1_table()


def base_detail_2_table():
    # 读取 CSV 文件
    data = pd.read_csv('detail2.csv')

    # 假设你的表名为 your_table，列名与 CSV 文件中的列名对应
    values_list = []
    for index, row in data.iterrows():
        url = str(row['url']).strip()
        first_name = str(row['first_name']).strip()
        second_name = str(row['second_name']).strip()
        bird_type = str(row['bird_type']).strip()
        descript = str(row['descript']).replace('\r', '').replace('\n', '').replace('\t', '').strip()
        img_url = str(row['img_url']).strip()
        values = (url, first_name, second_name, bird_type, descript, img_url)
        values_list.append(values)

    # 使用 executemany 进行批量插入
    query = "INSERT INTO detail_2 (url, first_name, second_name, bird_type, descript, img_url) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, values_list)

    # 提交事务
    connection.commit()

    # 关闭游标和连接
    cursor.close()
    connection.close()


# base_detail_2_table()

def base_pic_message_table():
    # 读取 CSV 文件
    data = pd.read_csv('pic_message.csv')

    # 假设你的表名为 your_table，列名与 CSV 文件中的列名对应
    values_list = []
    for index, row in data.iterrows():
        keywords = str(row['keywords']).strip()
        assetId = str(row['assetId']).strip()
        category = str(row['category']).strip()
        comName = str(row['comName']).strip()
        reportAs = str(row['reportAs']).strip()
        sciName = str(row['sciName']).strip()
        speciesCode = str(row['speciesCode']).strip()
        userDisplayName = str(row['userDisplayName']).strip()
        userId = str(row['userId']).strip()
        countryCode = str(row['countryCode']).strip()
        countryName = str(row['countryName']).strip()
        bird_name = str(row['bird_name']).strip()
        bird_imgs_url_480 = str(row['bird_imgs_url_480']).strip()
        bird_imgs_url_640 = str(row['bird_imgs_url_640']).strip()
        bird_imgs_url_900 = str(row['bird_imgs_url_900']).strip()
        bird_imgs_url_1200 = str(row['bird_imgs_url_1200']).strip()
        bird_imgs_url_1800 = str(row['bird_imgs_url_1800']).strip()
        bird_imgs_url_2400 = str(row['bird_imgs_url_2400']).strip()
        values = (keywords, assetId, category, comName, reportAs, sciName, speciesCode, userDisplayName, userId,
                 countryCode, countryName, bird_name, bird_imgs_url_480, bird_imgs_url_640, bird_imgs_url_900,
                 bird_imgs_url_1200, bird_imgs_url_1800, bird_imgs_url_2400)
        values_list.append(values)
    # print(values_list)
    # 使用 executemany 进行批量插入
    query = "INSERT INTO pic_message (keywords_1, assetId, category, comName, reportAs, sciName, speciesCode, userDisplayName, userId,countryCode, countryName, bird_name, bird_imgs_url_480, bird_imgs_url_640, bird_imgs_url_900,bird_imgs_url_1200, bird_imgs_url_1800, bird_imgs_url_2400) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, values_list)

    # 提交事务
    connection.commit()

    # 关闭游标和连接
    cursor.close()
    connection.close()


base_pic_message_table()