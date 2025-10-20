import os
import json
import logging
import csv
import requests
from bs4 import BeautifulSoup

# 配置日志
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_detail(url):
    """从鸟类详情页面采集数据
    
    Args:
        url: 鸟类详情页面URL，例如 https://avibase.bsc-eoc.org/species.jsp?avibaseid=66C31E09F8C285D6&region=NAM&lang=ZH
    
    Returns:
        dict: 包含鸟类详细信息的字典
    """
    logger.info(f"正在获取鸟类详情: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 初始化数据字典
        bird_detail = {
            'url': url,
            'scientific_name': '',
            'common_name': '',
            'chinese_name': '',
            'family': '',
            'order': '',
            'genus': '',
            'status': '',
            'description': '',
            'habitat': '',
            'distribution': '',
            'images': [],
            'sounds': []
        }
        
        # 提取鸟类基本信息
        title_elem = soup.find('title')
        lang_name_elem = soup.find('h2') 
        if title_elem:
            bird_detail['scientific_name'] = title_elem.get_text().strip()
        if lang_name_elem:
            bird_detail['chinese_name'] = lang_name_elem.get_text().strip()
        
        # 查找描述信息
        description = soup.select_one('#card-body p')
        if description:
            bird_detail['description'] = description.get_text().strip()

        # 查找分类信息 - 根据你提供的HTML结构
        # 寻找 id="taxoninfo" 的div元素
        taxon_info_div = soup.find('div', id='taxoninfo')
        if taxon_info_div:
            html_content = str(taxon_info_div)
            print(f"找到分类信息div: {html_content}")
            
            # 使用正则表达式提取信息，基于实际HTML结构
            import re
            
            # 提取目 (Order)
            # 实际格式: <b>目:</b><br/>   Tinamiformes <br/>
            order_pattern = r'<b>目:</b><br/>\s*([^<\n]+)'
            order_match = re.search(order_pattern, html_content)
            if order_match:
                bird_detail['order'] = order_match.group(1).strip()
                print(f"提取到目: {bird_detail['order']}")
            else:
                print("未找到目信息")
            
            # 提取科 (Family)
            # 实际格式: <b>科:</b><br/>   <a href="...">Tinamidae</a><br/>
            family_pattern = r'<b>科:</b><br/>\s*(?:<a[^>]*>([^<]+)</a>|([^<\n]+))'
            family_match = re.search(family_pattern, html_content)
            if family_match:
                bird_detail['family'] = (family_match.group(1) or family_match.group(2)).strip()
                print(f"提取到科: {bird_detail['family']}")
            else:
                print("未找到科信息")
            
            # 提取属 (Genus)
            # 实际格式: <b>属:</b><br/>    <a href="...">Nothocercus</a><br/>
            genus_pattern = r'<b>属:</b><br/>\s*(?:<a[^>]*>([^<]+)</a>|([^<\n]+))'
            genus_match = re.search(genus_pattern, html_content)
            if genus_match:
                bird_detail['genus'] = (genus_match.group(1) or genus_match.group(2)).strip()
                print(f"提取到属: {bird_detail['genus']}")
            else:
                print("未找到属信息")
            
            # 提取学名 (Scientific name)
            # 实际格式: <b>学名:</b><br/>   <i>Nothocercus bonapartei</i>
            scientific_pattern = r'<b>学名:</b><br/>\s*<i>([^<]+)</i>'
            scientific_match = re.search(scientific_pattern, html_content)
            if scientific_match:
                bird_detail['scientific_name'] = scientific_match.group(1).strip()
                print(f"提取到学名: {bird_detail['scientific_name']}")
            else:
                print("未找到学名信息")
        else:
            print("未找到 id='taxoninfo' 的div元素")

        # 查找图片
        images = soup.find_all('img')
        for img in images:
            src = img.get('src', '')
            if src and ('bird' in src.lower() or 'species' in src.lower() or src.startswith('http')):
                if not src.startswith('http'):
                    src = f"https://avibase.bsc-eoc.org/{src}"
                bird_detail['images'].append(src)
        
        # 查找录音链接
        # 查找所有可能的音频链接
        sound_links = []
        
        # 1. 查找直接的音频文件链接 (.mp3, .wav, .ogg等)
        audio_links = soup.find_all('a', href=True)
        for link in audio_links:
            href = link.get('href', '')
            if any(ext in href.lower() for ext in ['.mp3', '.wav', '.ogg', '.m4a', '.aac']):
                if not href.startswith('http'):
                    href = f"https://avibase.bsc-eoc.org/{href}"
                sound_links.append({
                    'url': href,
                    'text': link.get_text().strip(),
                    'type': 'direct_audio'
                })
        
        # 2. 查找指向外部音频网站的链接 (如 xeno-canto, eBird等)
        external_audio_sites = ['xeno-canto', 'ebird', 'macaulaylibrary', 'sounds.org']
        for link in audio_links:
            href = link.get('href', '')
            text = link.get_text().lower()
            if any(site in href.lower() or site in text for site in external_audio_sites):
                sound_links.append({
                    'url': href,
                    'text': link.get_text().strip(),
                    'type': 'external_site'
                })
        
        # 3. 查找包含"声音"、"录音"、"听"等关键词的链接
        sound_keywords = ['声音', '录音', '听', 'sound', 'audio', 'call', 'song', 'recording']
        for link in audio_links:
            text = link.get_text().lower()
            if any(keyword in text for keyword in sound_keywords):
                href = link.get('href', '')
                if href and not any(existing['url'] == href for existing in sound_links):
                    sound_links.append({
                        'url': href,
                        'text': link.get_text().strip(),
                        'type': 'keyword_match'
                    })
        
        # 4. 查找HTML5 audio标签
        audio_elements = soup.find_all('audio')
        for audio in audio_elements:
            src = audio.get('src', '')
            if src:
                if not src.startswith('http'):
                    src = f"https://avibase.bsc-eoc.org/{src}"
                sound_links.append({
                    'url': src,
                    'text': 'HTML5 Audio',
                    'type': 'html5_audio'
                })
            
            # 检查audio标签内的source元素
            sources = audio.find_all('source')
            for source in sources:
                src = source.get('src', '')
                if src:
                    if not src.startswith('http'):
                        src = f"https://avibase.bsc-eoc.org/{src}"
                    sound_links.append({
                        'url': src,
                        'text': f"Audio Source ({source.get('type', 'unknown')})",
                        'type': 'html5_source'
                    })
        
        # 尝试从外部源获取录音
        scientific_name = bird_detail.get('scientific_name', '')
        if scientific_name:
            # 从Xeno-canto获取录音
            xeno_sounds = get_xeno_canto_sounds(scientific_name)
            sound_links.extend(xeno_sounds)
            
            # 从URL中提取avibase_id来获取eBird录音
            import re
            avibase_match = re.search(r'avibaseid=([A-F0-9]+)', url)
            if avibase_match:
                avibase_id = avibase_match.group(1)
                ebird_sounds = get_ebird_sounds(avibase_id)
                sound_links.extend(ebird_sounds)
        
        bird_detail['sounds'] = sound_links
        if sound_links:
            print(f"找到 {len(sound_links)} 个音频链接:")
            for sound in sound_links:
                source = sound.get('source', sound.get('type', 'unknown'))
                print(f"  - {source}: {sound['text']} -> {sound['url']}")
        else:
            print("未找到音频链接")
        
        # 查找分布信息
        distribution_elem = soup.find(string=lambda text: text and ('distribution' in text.lower() or '分布' in text))
        if distribution_elem:
            parent = distribution_elem.parent
            if parent:
                bird_detail['distribution'] = parent.get_text().strip()
        
        logger.info(f"成功获取鸟类详情: {bird_detail.get('scientific_name', 'Unknown')}")
        return bird_detail
        
    except Exception as e:
        logger.error(f"获取鸟类详情失败: {e}")
        return None

def write_detail_to_csv(bird_detail, filename='bird_details.csv'):
    """将鸟类详情数据写入CSV文件
    
    Args:
        bird_detail: 鸟类详情字典
        filename: CSV文件名
    """
    if not bird_detail:
        logger.warning("没有详情数据可写入CSV")
        return False
    
    try:
        # 检查文件是否存在
        file_exists = os.path.exists(filename)
        
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['url', 'scientific_name', 'common_name', 'chinese_name', 
                         'family', 'order', 'genus', 'status', 'description', 'habitat', 
                         'distribution', 'images', 'sounds']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # 如果是新文件，写入表头
            if not file_exists:
                writer.writeheader()
            
            # 处理列表数据，转换为字符串
            detail_copy = bird_detail.copy()
            detail_copy['images'] = '; '.join(bird_detail.get('images', []))
            
            # 处理sounds列表，转换为可读的字符串格式
            sounds = bird_detail.get('sounds', [])
            if sounds:
                sound_strings = []
                for sound in sounds:
                    sound_strings.append(f"{sound['text']} ({sound['type']}): {sound['url']}")
                detail_copy['sounds'] = '; '.join(sound_strings)
            else:
                detail_copy['sounds'] = ''
            
            writer.writerow(detail_copy)
            
        logger.info(f"成功写入详情数据到 {filename}")
        return True
        
    except Exception as e:
        logger.error(f"写入详情CSV文件失败: {e}")
        return False

def get_ebird_sounds(avibase_id, region='NAM'):
    """获取eBird录音数据
    
    Args:
        avibase_id: Avibase ID
        region: 地区代码
    
    Returns:
        list: 录音信息列表
    """
    try:
        # 尝试获取eBird数据的API或页面
        ebird_url = f"https://avibase.bsc-eoc.org/ebird.jsp?avibaseid={avibase_id}&region={region}"
        logger.info(f"正在获取eBird录音数据: {ebird_url}")
        
        response = requests.get(ebird_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        sounds = []
        
        # 查找录音链接
        # 1. 查找指向Macaulay Library的链接
        macaulay_links = soup.find_all('a', href=True)
        for link in macaulay_links:
            href = link.get('href', '')
            text = link.get_text().strip()
            if 'macaulaylibrary' in href.lower() or 'ml' in href.lower():
                sounds.append({
                    'url': href,
                    'text': text,
                    'source': 'Macaulay Library',
                    'type': 'external_recording'
                })
        
        # 2. 查找xeno-canto链接
        xeno_links = soup.find_all('a', href=True)
        for link in xeno_links:
            href = link.get('href', '')
            text = link.get_text().strip()
            if 'xeno-canto' in href.lower():
                sounds.append({
                    'url': href,
                    'text': text,
                    'source': 'Xeno-canto',
                    'type': 'external_recording'
                })
        
        return sounds
        
    except Exception as e:
        logger.error(f"获取eBird录音数据失败: {e}")
        return []

def get_xeno_canto_sounds(scientific_name):
    """从Xeno-canto获取录音
    
    Args:
        scientific_name: 鸟类学名
    
    Returns:
        list: 录音信息列表
    """
    try:
        # Xeno-canto API
        api_url = f"https://xeno-canto.org/api/2/recordings?query={scientific_name.replace(' ', '+')}"
        logger.info(f"正在从Xeno-canto获取录音: {api_url}")
        
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        sounds = []
        if 'recordings' in data:
            for recording in data['recordings'][:5]:  # 限制前5个录音
                sounds.append({
                    'url': recording.get('file', ''),
                    'text': f"{recording.get('type', 'call')} - {recording.get('loc', 'unknown location')}",
                    'source': 'Xeno-canto',
                    'type': 'direct_audio',
                    'quality': recording.get('q', 'unknown'),
                    'country': recording.get('cnt', 'unknown')
                })
        
        return sounds
        
    except Exception as e:
        logger.error(f"从Xeno-canto获取录音失败: {e}")
        return []

def download_bird_sounds(bird_detail, download_dir='bird_sounds'):
    """下载鸟类录音文件
    
    Args:
        bird_detail: 包含录音信息的鸟类详情字典
        download_dir: 下载目录
    
    Returns:
        list: 成功下载的文件路径列表
    """
    if not bird_detail or not bird_detail.get('sounds'):
        logger.warning("没有录音数据可下载")
        return []
    
    # 创建下载目录
    os.makedirs(download_dir, exist_ok=True)
    
    downloaded_files = []
    scientific_name = bird_detail.get('scientific_name', 'unknown').replace(' ', '_')
    
    # 从URL中提取avibaseid
    avibase_id = 'unknown'
    detail_url = bird_detail.get('url', '')
    if detail_url:
        import re
        avibase_match = re.search(r'avibaseid=([A-F0-9]+)', detail_url)
        if avibase_match:
            avibase_id = avibase_match.group(1)
    
    for i, sound in enumerate(bird_detail['sounds']):
        if sound['type'] == 'direct_audio':  # 只下载直接的音频文件
            try:
                url = sound['url']
                # 获取文件扩展名
                file_ext = url.split('.')[-1].lower()
                if file_ext not in ['mp3', 'wav', 'ogg', 'm4a', 'aac']:
                    file_ext = 'mp3'  # 默认扩展名
                
                # 生成包含avibaseid的文件名
                filename = f"{scientific_name}_{avibase_id}_{i+1}.{file_ext}"
                filepath = os.path.join(download_dir, filename)
                
                # 下载文件
                logger.info(f"正在下载录音: {url}")
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                downloaded_files.append(filepath)
                logger.info(f"录音下载成功: {filepath}")
                
            except Exception as e:
                logger.error(f"下载录音失败 {sound['url']}: {e}")
    
    return downloaded_files

def get_detai():
    """批量处理函数 - 从bird_list.csv读取数据并处理前100条"""
    csv_file = 'bird_list.csv'
    max_records = 100
    
    if not os.path.exists(csv_file):
        logger.error(f"找不到文件: {csv_file}")
        return []
    
    processed_details = []
    success_count = 0
    error_count = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            print(f"\n=== 开始批量处理鸟类详情数据 ===")
            print(f"目标处理数量: {max_records} 条")
            print(f"数据源文件: {csv_file}")
            print("=" * 50)
            
            for i, row in enumerate(reader):
                if i >= max_records:
                    break
                
                # 获取详情链接
                detail_url = row.get('详情链接', '').strip()
                chinese_name = row.get('中文名', '').strip()
                english_name = row.get('英文名', '').strip()
                
                if not detail_url:
                    logger.warning(f"第 {i+1} 条记录缺少详情链接，跳过")
                    error_count += 1
                    continue
                
                print(f"\n[{i+1}/{max_records}] 正在处理: {chinese_name} ({english_name})")
                print(f"URL: {detail_url}")
                
                try:
                    # 获取详情数据
                    detail = get_detail(detail_url)
                    
                    if detail:
                        # 补充从CSV中获取的基础信息
                        if not detail.get('chinese_name') and chinese_name:
                            detail['chinese_name'] = chinese_name
                        if not detail.get('common_name') and english_name:
                            detail['common_name'] = english_name
                        
                        # 显示获取结果
                        print(f"✓ 成功获取详情:")
                        print(f"  学名: {detail.get('scientific_name', 'N/A')}")
                        print(f"  中文名: {detail.get('chinese_name', 'N/A')}")
                        print(f"  目: {detail.get('order', 'N/A')}")
                        print(f"  科: {detail.get('family', 'N/A')}")
                        print(f"  属: {detail.get('genus', 'N/A')}")
                        
                        # 统计录音信息
                        sounds = detail.get('sounds', [])
                        direct_sounds = [s for s in sounds if s.get('type') == 'direct_audio']
                        if direct_sounds:
                            print(f"  录音: 找到 {len(direct_sounds)} 个可下载的录音")
                        else:
                            print(f"  录音: 未找到可下载的录音")
                        
                        # 保存到CSV
                        write_detail_to_csv(detail)
                        processed_details.append(detail)
                        success_count += 1
                        
                        # 下载录音
                        if direct_sounds:
                            downloaded = download_bird_sounds(detail)
                            if downloaded:
                                print(f"  下载: 成功下载 {len(downloaded)} 个录音文件")
                            else:
                                print(f"  下载: 录音下载失败")
                        
                    else:
                        print(f"✗ 获取详情失败")
                        error_count += 1
                        
                except Exception as e:
                    logger.error(f"处理第 {i+1} 条记录时出错: {e}")
                    error_count += 1
                    continue
                
                # 添加延迟，避免请求过于频繁
                import time
                time.sleep(1)  # 1秒延迟
            
            print("\n" + "=" * 50)
            print(f"=== 批量处理完成 ===")
            print(f"总处理数量: {i+1}")
            print(f"成功数量: {success_count}")
            print(f"失败数量: {error_count}")
            print(f"成功率: {success_count/(success_count+error_count)*100:.1f}%")
            print(f"详情数据已保存到: bird_details.csv")
            
    except Exception as e:
        logger.error(f"读取CSV文件失败: {e}")
        return []
    
    return processed_details


# 使用示例（注释掉，供手动调用）
if __name__ == "__main__":
    get_detai()
