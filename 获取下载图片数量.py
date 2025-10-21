def get_file_pics():
    import os
    # directory_path = './downloaded_images'
    # directory_path = './downloaded_images_202410'
    directory_path = './pic_20241107'
    pic_list = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            # print(os.path.join(root, file_name))
            pic_list.append(file_name.replace('.jpg', ''))
    return pic_list

print(len(get_file_pics()))