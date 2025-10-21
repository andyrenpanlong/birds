import os
import shutil

def create_directories_and_move_files(source_directory):
    for filename in os.listdir(source_directory):
        if os.path.isfile(os.path.join(source_directory, filename)):
            # 提取文件名（不包括扩展名）作为目录名
            directory_name = os.path.splitext(filename)[0].split('_')[0]
            new_directory = os.path.join('/Users/renpanlong/python/eBird/sp_pics/', directory_name)
            print(directory_name, new_directory)
            # 创建目录
            if not os.path.exists(new_directory):
                os.makedirs(new_directory)
            # 移动文件到新目录
            shutil.move(os.path.join(source_directory, filename), new_directory)

# 示例用法
source_directory = './downloaded_images'
create_directories_and_move_files(source_directory)