import os
import json
import logging
import csv
import requests
from bs4 import BeautifulSoup
import time
import re

# 配置日志
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# eBird支持的语言代码映射
EBIRD_LANGUAGES = {
    'en': 'English',           # 英语
    'zh': 'Chinese (Simplified)',  # 中文简体
    'zh-TW': 'Chinese (Traditional)',  # 中文繁体
    'fr': 'French',            # 法语
    'de': 'German',            # 德语
    'it': 'Italian',           # 意大利语
    'es': 'Spanish',           # 西班牙语
    'ja': 'Japanese',          # 日语
    'ko': 'Korean'             # 韩语
}

def get_ebird_species_names(species_code, languages=None):
    """从eBird获取鸟类的多语言名称
    
    Args:
        species_code: eBird物种代码，如 'thitin1'
        languages: 要获取的语言列表，默认获取所有支持的语言
    
    Returns:
        dict: 包含多语言名称的字典
    """
    if languages is None:
        languages = list(EBIRD_LANGUAGES.keys())
    
    species_names = {
        'species_code': species_code,
        'url': f'https://ebird.org/species/{species_code}',
        'names': {}
    }
    
    logger.info(f"正在获取物种 {species_code} 的多语言名称")
    
    for lang_code in languages:
        try:
            # 构建带语言参数的URL
            if lang_code == 'en':
                # 英语是默认语言，不需要特殊参数
                url = f'https://ebird.org/species/{species_code}'
            else:
                # 其他语言需要添加语言参数
                url = f'https://ebird.org/species/{species_code}?locale={lang_code}'
            
            logger.info(f"正在获取 {EBIRD_LANGUAGES[lang_code]} 名称: {url}")
            
            # 设置请求头，模拟浏览器访问
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': f'{lang_code},en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取鸟类名称 - eBird通常在h1标签或特定的class中显示物种名称
            species_name = extract_species_name(soup, lang_code)
            
            if species_name:
                species_names['names'][lang_code] = {
                    'language': EBIRD_LANGUAGES[lang_code],
                    'name': species_name,
                    'url': url
                }
                logger.info(f"成功获取 {EBIRD_LANGUAGES[lang_code]} 名称: {species_name}")
            else:
                logger.warning(f"未能提取 {EBIRD_LANGUAGES[lang_code]} 名称")
            
            # 添加延迟，避免请求过于频繁
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"获取 {EBIRD_LANGUAGES[lang_code]} 名称失败: {e}")
            continue
    
    return species_names

def extract_species_name(soup, lang_code):
    """从eBird页面提取物种名称
    
    Args:
        soup: BeautifulSoup对象
        lang_code: 语言代码
    
    Returns:
        str: 提取到的物种名称
    """
    # 尝试多种选择器来提取物种名称
    selectors = [
        'h1.Heading-main',  # 主标题
        'h1[data-testid="species-name"]',  # 物种名称测试ID
        'h1.SpeciesHeader-title',  # 物种头部标题
        '.SpeciesHeader-commonName',  # 通用名称
        '.species-name',  # 物种名称类
        'h1',  # 通用h1标签
        '.Heading--h1',  # 标题类
    ]
    
    for selector in selectors:
        try:
            element = soup.select_one(selector)
            if element:
                name = element.get_text().strip()
                # 清理名称，移除多余的空白和特殊字符
                name = re.sub(r'\s+', ' ', name)
                name = name.replace('\n', ' ').replace('\t', ' ')
                if name and len(name) > 1:
                    return name
        except Exception as e:
            continue
    
    # 如果上述方法都失败，尝试从页面标题提取
    try:
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            # eBird的标题通常格式为 "Species Name - eBird"
            if ' - eBird' in title_text:
                return title_text.replace(' - eBird', '').strip()
            elif ' | eBird' in title_text:
                return title_text.split(' | eBird')[0].strip()
    except Exception as e:
        pass
    
    return None

def get_species_code_from_url(url):
    """从eBird URL中提取物种代码
    
    Args:
        url: eBird物种URL
    
    Returns:
        str: 物种代码
    """
    # 从URL中提取物种代码
    # 例如: https://ebird.org/species/thitin1 -> thitin1
    match = re.search(r'/species/([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    return None

def write_multilingual_names_to_csv(species_data_list, filename='ebird_multilingual_names.csv'):
    """将多语言名称数据写入CSV文件
    
    Args:
        species_data_list: 包含多语言名称的物种数据列表
        filename: CSV文件名
    """
    if not species_data_list:
        logger.warning("没有数据可写入CSV")
        return False
    
    try:
        # 检查文件是否存在
        file_exists = os.path.exists(filename)
        
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            # 创建表头
            fieldnames = ['species_code', 'url']
            # 为每种语言添加字段
            for lang_code in EBIRD_LANGUAGES.keys():
                fieldnames.append(f'name_{lang_code}')
                fieldnames.append(f'url_{lang_code}')
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # 如果是新文件，写入表头
            if not file_exists:
                writer.writeheader()
            
            # 写入数据
            for species_data in species_data_list:
                row = {
                    'species_code': species_data['species_code'],
                    'url': species_data['url']
                }
                
                # 添加各语言的名称和URL
                for lang_code in EBIRD_LANGUAGES.keys():
                    if lang_code in species_data['names']:
                        row[f'name_{lang_code}'] = species_data['names'][lang_code]['name']
                        row[f'url_{lang_code}'] = species_data['names'][lang_code]['url']
                    else:
                        row[f'name_{lang_code}'] = ''
                        row[f'url_{lang_code}'] = ''
                
                writer.writerow(row)
            
        logger.info(f"成功写入 {len(species_data_list)} 条多语言数据到 {filename}")
        return True
        
    except Exception as e:
        logger.error(f"写入CSV文件失败: {e}")
        return False

def batch_process_ebird_species(species_codes, max_species=10):
    """批量处理eBird物种的多语言名称
    
    Args:
        species_codes: eBird物种代码列表
        max_species: 最大处理数量
    
    Returns:
        list: 包含多语言名称的物种数据列表
    """
    if not species_codes:
        logger.warning("没有物种代码可处理")
        return []
    
    processed_data = []
    success_count = 0
    error_count = 0
    
    print(f"\n=== 开始批量处理 eBird 物种多语言名称 ===")
    print(f"目标处理数量: {min(len(species_codes), max_species)} 条")
    print(f"目标语言: {list(EBIRD_LANGUAGES.values())}")
    print("=" * 50)
    
    for i, species_code in enumerate(species_codes[:max_species]):
        try:
            print(f"\n[{i+1}/{min(len(species_codes), max_species)}] 正在处理: {species_code}")
            
            # 获取多语言名称
            species_data = get_ebird_species_names(species_code)
            
            if species_data['names']:
                print(f"✓ 成功获取 {len(species_data['names'])} 种语言的名称")
                # 显示部分语言名称
                for lang_code in ['en', 'zh', 'fr', 'es', 'ja']:
                    if lang_code in species_data['names']:
                        name = species_data['names'][lang_code]['name']
                        lang_name = EBIRD_LANGUAGES[lang_code]
                        print(f"  {lang_name}: {name}")
                
                processed_data.append(species_data)
                success_count += 1
            else:
                print(f"✗ 未能获取任何语言的名称")
                error_count += 1
            
            # 添加延迟，避免请求过于频繁
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"处理物种 {species_code} 时出错: {e}")
            error_count += 1
            continue
    
    print("\n" + "=" * 50)
    print(f"=== 批量处理完成 ===")
    print(f"成功数量: {success_count}")
    print(f"失败数量: {error_count}")
    if success_count + error_count > 0:
        print(f"成功率: {success_count/(success_count+error_count)*100:.1f}%")
    
    # 保存到CSV
    if processed_data:
        write_multilingual_names_to_csv(processed_data)
        print(f"多语言数据已保存到: ebird_multilingual_names.csv")
    
    return processed_data

def get_ebird_codes_from_scientific_names(scientific_names):
    """根据学名推测eBird物种代码
    
    Args:
        scientific_names: 学名列表
    
    Returns:
        list: 推测的eBird物种代码列表
    
    Note:
        这是一个简化的实现，实际的eBird代码可能需要通过API或其他方式获取
    """
    ebird_codes = []
    
    for scientific_name in scientific_names:
        try:
            # 简化的代码生成逻辑（实际情况可能更复杂）
            # 通常eBird代码由属名前几个字母 + 种名前几个字母 + 数字组成
            parts = scientific_name.lower().split()
            if len(parts) >= 2:
                genus = parts[0][:3]  # 属名前3个字母
                species = parts[1][:3]  # 种名前3个字母
                code = genus + species + '1'  # 添加数字1
                ebird_codes.append(code)
            
        except Exception as e:
            logger.warning(f"无法为 {scientific_name} 生成eBird代码: {e}")
            continue
    
    return ebird_codes

def test_ebird_multilingual():
    """测试函数 - 获取示例物种的多语言名称"""
    # 测试单个物种
    test_species_code = 'thitin1'  # Highland Tinamou
    
    print(f"\n=== 测试获取 eBird 物种多语言名称 ===")
    print(f"物种代码: {test_species_code}")
    print(f"目标语言: {list(EBIRD_LANGUAGES.values())}")
    print("=" * 50)
    
    # 获取多语言名称
    species_data = get_ebird_species_names(test_species_code)
    
    if species_data['names']:
        print(f"\n✓ 成功获取 {len(species_data['names'])} 种语言的名称:")
        for lang_code, data in species_data['names'].items():
            print(f"  {data['language']}: {data['name']}")
        
        # 保存到CSV
        write_multilingual_names_to_csv([species_data])
        print(f"\n=== 数据已保存到 ebird_multilingual_names.csv ===")
    else:
        print("✗ 未能获取任何语言的名称")
    
    # 测试批量处理
    print(f"\n=== 测试批量处理功能 ===")
    test_species_codes = ['thitin1', 'gretit1', 'littit1']  # 示例物种代码
    batch_process_ebird_species(test_species_codes, max_species=2)
    
    return species_data

# 使用示例
if __name__ == "__main__":
    test_ebird_multilingual()
