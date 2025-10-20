import os
import json
import logging
import csv
import requests
from bs4 import BeautifulSoup

# 配置日志
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
languages = [
    'ZH',  # 中文
    # 'EN', # 英文
    # 'JP', # 日语
]  # 默认中文

def generate_start_urls_from_regions():
    """从regions_raw_data.json生成起始URL列表"""
    urls = []
        
    # 查找regions_raw_data.json文件
    json_file_paths = [
        'regions_raw_data.json',  # 当前目录
        '../regions_raw_data.json',  # 上级目录
        '../../regions_raw_data.json',  # 上上级目录
        os.path.join(os.path.dirname(__file__), '../../regions_raw_data.json'),  # 相对于爬虫文件
    ]
    
    regions_data = None
    json_file = None
    
    for file_path in json_file_paths:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    regions_data = json.load(f)
                json_file = file_path
                break
        except Exception as e:
            logger.warning(f"无法读取 {file_path}: {e}")
            continue
    
    if not regions_data:
        logger.warning("未找到regions_raw_data.json文件，使用默认URL")
        return ['https://avibase.bsc-eoc.org/checklist.jsp?region=WORLD&lang=ZH']
    
    logger.info(f"从 {json_file} 读取到 {len(regions_data)} 个地区")
    
    # 使用默认配置
    min_bird_count = 100  # 默认最少鸟类数量
    region_types = [1, 2, 3]  # 默认地区类型
    max_urls = 1000  # 默认最大URL数量
    
    for region in regions_data:
        region_code = region.get('region', '')
        region_name = region.get('regionName', '')
        dst_count = region.get('dstCount', 0)
        region_type = region.get('regionType', 0)
        
        # 过滤条件
        if not region_code or dst_count < 1:
            continue
        
        # 根据配置选择地区类型
        if region_type in region_types:
            for lang in languages:
                url = f'https://avibase.bsc-eoc.org/checklist.jsp?region={region_code}&lang={lang}'
                urls.append(url)
                
                # 记录URL对应的地区信息
                logger.debug(f"添加URL: {url} ({region_name}, {dst_count} 种鸟类)")
    
    # 如果没有生成任何URL，使用默认的
    if not urls:
        logger.warning("没有生成任何URL，使用默认URL")
        urls = ['https://avibase.bsc-eoc.org/checklist.jsp?region=WORLD&lang=ZH']
    
    # # 限制URL数量，避免过多请求
    # if len(urls) > max_urls:
    #     logger.info(f"URL数量 ({len(urls)}) 超过限制，只使用前 {max_urls} 个")
    #     urls = urls[:max_urls]
    
    return urls


def write_birds_to_csv(data_arr, file_name='bird_list.csv'):
    # 打开CSV文件
    with open(file_name, mode='a+', newline='') as file:
        writer = csv.writer(file)
        # 写入表头
        # writer.writerow(['学名', '英文名', '详情链接', '中文名', '保护状态', '地区代码', '语言'])
        # 按行写入数据
        writer.writerow(data_arr)
    # print("CSV文件已成功创建")


def write_birds_to_csv2(bird_data, filename='bird_list.csv', append_mode=True):
    """将鸟类数据写入CSV文件（支持增量写入）
    
    Args:
        bird_data: 单个data_row列表或鸟类数据列表的列表
        filename: CSV文件名
        append_mode: True为增量模式，False为覆盖模式
    """
    if not bird_data:
        logger.warning("没有数据可写入CSV")
        return False
    
    # 处理单个data_row的情况
    if isinstance(bird_data[0], str):
        # 如果第一个元素是字符串，说明传入的是单个data_row
        bird_data = [bird_data]
    
    try:
        # 检查文件是否存在
        file_exists = os.path.exists(filename)
        
        # 如果是增量模式且文件存在，读取现有数据避免重复
        existing_data = set()
        if append_mode and file_exists:
            try:
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader, None)  # 跳过表头
                    for row in reader:
                        if len(row) >= 2:
                            # 使用学名和英文名作为唯一标识
                            existing_data.add((row[0], row[1]))
                logger.debug(f"读取到 {len(existing_data)} 条现有记录")
            except Exception as e:
                logger.warning(f"读取现有CSV文件时出错: {e}")
        
        # 过滤重复数据
        new_data = []
        duplicate_count = 0
        for row in bird_data:
            if len(row) >= 2:
                key = (row[0], row[1])  # 学名和英文名
                if key not in existing_data:
                    new_data.append(row)
                    existing_data.add(key)
                else:
                    duplicate_count += 1
        
        if duplicate_count > 0:
            logger.debug(f"跳过 {duplicate_count} 条重复记录")
        
        if not new_data:
            logger.debug("没有新数据需要写入")
            return True
        
        # 确定写入模式
        if append_mode and file_exists:
            mode = 'a'  # 追加模式
        else:
            mode = 'w'  # 覆盖模式
        
        with open(filename, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # 如果是新文件或覆盖模式，写入表头
            if mode == 'w':
                headers = ['学名', '英文名', '详情链接', '中文名', '保护状态', '地区代码', '语言']
                writer.writerow(headers)
            
            # 写入新数据
            writer.writerows(new_data)
            
        action = "追加" if mode == 'a' else "写入"
        logger.debug(f"成功{action} {len(new_data)} 条新记录到 {filename}")
        return True
        
    except Exception as e:
        logger.error(f"写入CSV文件失败: {e}")
        return False

def get_bird_lists():
    """获取鸟类列表数据"""
    urls_list = generate_start_urls_from_regions()
    all_bird_data = []  # 存储所有URL的鸟类数据
    
    for url in urls_list:
        print('正在获取鸟类数据:', url)
        logger.info(f"正在获取鸟类数据: {url}")
        
        # 从URL中解析region和lang参数
        import urllib.parse
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        region = query_params.get('region', [''])[0]
        lang = query_params.get('lang', [''])[0]
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            trs = soup.select('.table .highlight1')
            logger.info(f"找到 {len(trs)} 条鸟类记录")
            
            bird_data = []
            for tr in trs:
                try:
                    tds = tr.select('td')
                    if len(tds) >= 3:
                        first_name = tds[0].text.strip() or ''  # 学名
                        second_name = tds[1].text.strip() or ''  # 英文名
                        
                        # 获取鸟类详情链接
                        bird_url = ''
                        link_elem = tds[1].select('a')
                        if link_elem:
                            href = link_elem[0].get('href', '').strip()
                            if href.startswith('http'):
                                bird_url = href
                            else:
                                bird_url = f'https://avibase.bsc-eoc.org/{href}&region={region}&lang={lang}'
                        
                        name = tds[2].text.strip() or ''  # 中文名
                        
                        # 鸟类类型（如果有的话）
                        bird_type = ''
                        if len(tds) > 3:
                            bird_type = tds[3].text.strip() or ''
                        
                        data_row = [first_name, second_name, bird_url, name, bird_type, region, lang]
                        write_birds_to_csv(data_row, 'bird_list.csv')
                        bird_data.append(data_row)
                except Exception as e:
                    logger.warning(f"解析行数据时出错: {e}")
                    continue
            
            # 记录当前URL处理的结果
            if bird_data:
                logger.info(f"成功处理 {len(bird_data)} 条鸟类记录")
                all_bird_data.extend(bird_data)
            
        except Exception as e:
            logger.error(f"获取鸟类数据失败: {e}")
            continue  # 继续处理下一个URL
    
    logger.info(f"总共处理了 {len(all_bird_data)} 条鸟类记录")
    return all_bird_data


# 使用示例（注释掉，供手动调用）
if __name__ == "__main__":
    get_bird_lists()
