# import time
# import urllib.request
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# # 设置Chrome浏览器驱动路径（根据实际情况修改）
# driver_path = 'chromedriver.exe'
# driver = webdriver.Chrome(executable_path=driver_path)
#
# # 打开网页
# driver.get('https://media.ebird.org/catalog?mediaType=photo')
#
# # 用于存储图片链接
# image_links = []
#
# while True:
#     # 查找所有图片元素
#     images = driver.find_elements(By.CSS_SELECTOR, 'img')
#     for image in images:
#         link = image.get_attribute('src')
#         if link and link.startswith('https'):
#             image_links.append(link)
#
#     # 查找下一页按钮
#     next_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next page"]')
#     if next_button.is_enabled():
#         next_button.click()
#         time.sleep(2)  # 等待页面加载
#     else:
#         break
#
# # 关闭浏览器
# driver.quit()
#
# # 下载图片（可以根据需要调整下载路径和文件名）
# for index, link in enumerate(image_links):
#     try:
#         urllib.request.urlretrieve(link, f'image_{index}.jpg')
#     except Exception as e:
#         print(f"下载图片时出错: {e}")
#

import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By

# 创建Chrome浏览器驱动实例
driver = webdriver.Chrome()

# 打开目标网页
driver.get('https://media.ebird.org/catalog?mediaType=photo')

# 用于存储图片链接的列表
image_links = []

while True:
    # 使用CSS选择器找到所有图片元素
    images = driver.find_elements(By.CSS_SELECTOR, 'img')
    for image in images:
        link = image.get_attribute('src')
        if link and link.startswith('https'):
            print(link)
            image_links.append(link)

    # 查找下一页按钮
    next_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next page"]')
    if next_button.is_enabled():
        next_button.click()
        time.sleep(2)  # 给页面加载留出时间
    else:
        break

# 关闭浏览器驱动
driver.quit()
