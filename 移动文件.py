import os
import shutil

def move_files(source_directory, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_directory, file)
            shutil.move(source_path, destination_path)
            print(f"Moved {source_path} to {destination_path}")

# 示例用法
source_dir = '/Users/renpanlong/python/eBird/sp_pics/'
destination_dir = '/Users/renpanlong/python/eBird/downloaded_images/'

move_files(source_dir, destination_dir)