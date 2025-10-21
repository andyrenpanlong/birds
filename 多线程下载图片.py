import requests
import concurrent.futures
import os

all_nums = 0

def download_and_rename_image(url, new_name, save_directory):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_path = os.path.join(save_directory, new_name)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"图片下载成功并命名为：{new_name}，保存路径：{save_path}")
        else:
            print(f"下载失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"下载出现错误：{e}")

def concurrent_download_and_rename(images_info, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url, new_name in images_info:
            executor.submit(download_and_rename_image, url, new_name, save_directory)

# 获取文件图片内容
def get_file_pics():
    import os
    directory_path = './downloaded_images'
    pic_list = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            # print(os.path.join(root, file_name))
            pic_list.append(file_name.replace('.jpg', ''))
    return pic_list

def get_birds_list():
    import pymysql
    # 连接到 MySQL 数据库
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='12345678', database='spider')
    over_download_pics = get_file_pics()
    print('已下载图片数量为：', len(over_download_pics))
    pic_down_lists = []
    with connection.cursor() as cursor:
        # 执行查询语句，这里假设查询表名为 your_table 的所有数据
        sql = """select bird_imgs_url_2400, CONCAT_WS('_', bird_name, assetId,  row_num) as bird_name2 from (
        select a.url2, a.assetId, a.bird_name, a.bird_imgs_url_2400, 
         ROW_NUMBER() OVER (PARTITION BY a.url2 ORDER BY  a.assetId, a.bird_name, a.bird_imgs_url_2400) AS row_num
         from (SELECT distinct keywords_1, CONCAT_WS('', 'https://ebird.org/species/', keywords_1)  as url2, assetId, category, comName, reportAs, sciName, speciesCode, userDisplayName, userId, countryCode, countryName, bird_name, bird_imgs_url_480, bird_imgs_url_640, bird_imgs_url_900, bird_imgs_url_1200, bird_imgs_url_1800, bird_imgs_url_2400 FROM spider.pic_message) a
        left join (SELECT * FROM spider.birds) b on a.url2 = b.url) c;
        """
        global all_nums
        cursor.execute(sql)
        results = cursor.fetchall()
        print('总长度：', len(results))
        for u1 in results:
            all_nums += 1
            url = u1[0]
            image_name = u1[1]
            if image_name not in over_download_pics:
                pic_down_lists.append((url, '{}.jpg'.format(image_name)))
    return pic_down_lists


# 示例用法
# images_info = [
#     ('https://example.com/image1.jpg', 'renamed_image1.jpg'),
#     ('https://example.com/image2.jpg', 'renamed_image2.jpg'),
#     ('https://example.com/image3.jpg', 'renamed_image3.jpg')
# ]
# print(get_birds_list())
images_info = get_birds_list()[-101:-1]

save_directory = 'downloaded_images'

concurrent_download_and_rename(images_info, save_directory)