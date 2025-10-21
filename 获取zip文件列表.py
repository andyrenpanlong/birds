import zipfile
import os

def movefile(source_file_path, file_name):
    # 假设要把当前目录下的'source_file.txt'移动到'target_folder'文件夹中
    # source_file_path = "source_file.txt"
    # target_folder_path = "/Users/renpanlong/python/eBird/pic_20241104/"
    target_folder_path = "/Users/renpanlong/python/eBird/pic_20241107/"
    # target_folder_path = "/Users/renpanlong/python/eBird/downloaded_images_202410/"
    file_name = os.path.basename(source_file_path)
    target_file_path = os.path.join(target_folder_path, file_name)
    try:
        os.rename(source_file_path, target_file_path)
        print("文件移动成功")
    except FileNotFoundError:
        print("源文件不存在")
    except OSError as e:
        print(f"发生错误: {e}")

def get_zip_file_names(zip_file_path):
    file_names_list_id = []
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_names_list = zip_ref.namelist()
    for i in file_names_list:
        img_name = i.split('/')[-1].replace('.jpg', '')
        file_names_list_id.append(img_name)
    return file_names_list_id

zip_file_path = "downloaded_images_old.zip"  # 替换为实际的ZIP文件路径
file_names = get_zip_file_names(zip_file_path)
print(len(file_names))

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

# over_download_pics = get_file_pics()
# new_file_list = []
# num_tmp = 0
# for i in over_download_pics:
#     num_tmp += 1
#     if i not in file_names:
#         print('122312:该图片为新下载的：', i, "序号为:", num_tmp)
#         source_file_path = '/Users/renpanlong/python/eBird/downloaded_images/{}.jpg'.format(i)
#         file_name = '{}.jpg'.format(i)
#         movefile(source_file_path, file_name)

