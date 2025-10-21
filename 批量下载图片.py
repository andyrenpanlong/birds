import requests
import threading
import os


all_nums = 0

def download_image(url, save_name, save_directory):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_path = os.path.join(save_directory, save_name)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"图片 {save_name} 下载成功，保存路径：{save_path}")
        else:
            print(f"下载失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"下载出现错误：{e}")


def save_pic(url, image_name):
    try:
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
        image.save('./downloaded_images/{}.jpg'.format(image_name))
    except:
        pass
        # save_pic(url, image_name)

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


def download_images_multithreaded(image_urls_and_names, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    threads = []
    for url, name in image_urls_and_names:
        thread = threading.Thread(target=download_image, args=(url, name, save_directory))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def get_birds_list():
    import pymysql
    # 连接到 MySQL 数据库
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='12345678', database='spider')
    over_download_pics = get_file_pics()
    print('已下载图片数量为：', len(over_download_pics))
    with connection.cursor() as cursor:
        # 执行查询语句，这里假设查询表名为 your_table 的所有数据
        sql = """select bird_imgs_url_900, CONCAT_WS('_', bird_name, assetId,  row_num) as bird_name2 from (
        select a.url2, a.assetId, a.bird_name, a.bird_imgs_url_900, 
         ROW_NUMBER() OVER (PARTITION BY a.url2 ORDER BY  a.assetId, a.bird_name, a.bird_imgs_url_900) AS row_num
         from (SELECT distinct keywords_1, CONCAT_WS('', 'https://ebird.org/species/', keywords_1)  as url2, assetId, category, comName, reportAs, sciName, speciesCode, userDisplayName, userId, countryCode, countryName, bird_name, bird_imgs_url_480, bird_imgs_url_640, bird_imgs_url_900, bird_imgs_url_1200, bird_imgs_url_1800, bird_imgs_url_2400 FROM spider.pic_message) a
        left join (SELECT * FROM spider.birds) b on a.url2 = b.url) c;
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        print('总长度：', len(results))
        for u1 in results:
            global all_nums
            all_nums += 1
            url = u1[0]
            image_name = u1[1]
            if all_nums >= 550000:  # 从四十万开始
                if image_name not in over_download_pics:
                    print('图片下载到: {},图片名称为：{} 正在下载, 图片链接为：{}'.format( all_nums, image_name, url))
                    save_pic(url, image_name)


# 示例用法
# image_urls_and_names = [
#     ('https://example.com/image1.jpg', 'custom_name1.jpg'),
#     ('https://example.com/image2.jpg', 'custom_name2.jpg'),
#     ('https://example.com/image3.jpg', 'custom_name3.jpg')
# ]
save_directory = 'downloaded_images'

image_urls_and_names = get_birds_list()

# download_images_multithreaded(image_urls_and_names, save_directory)
