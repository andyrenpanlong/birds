#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check1.py - 筛选鸟类数据脚本

从bird.txt读取鸟类名称作为数据1，从明细分类-含url.xlsx读取详细信息作为数据2，
筛选出数据2中first_name包含数据1中鸟类名称的记录，并输出匹配的信息。
"""

import pandas as pd
import re
from typing import List, Tuple, Set
import requests
from bs4 import BeautifulSoup


headers = {
    'authority': 'ebird.org',
    'method': 'GET',
    # 'path': '/region/world/bird-list',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '_08023=31eac253469abad9; I18N_LANGUAGE=zh-CN; is-region-session=eyJ1c2VyIjp7InVzZXJJZCI6IlVTRVI2MzMwMjYwIiwidXNlcm5hbWUiOiJyZW5wYW5sb25nIiwiZmlyc3ROYW1lIjoi5Lu7IiwibGFzdE5hbWUiOiLmvZjpvpkiLCJmdWxsTmFtZSI6IuS7uyDmvZjpvpkiLCJyb2xlcyI6W10sInByZWZzIjp7IlBSSVZBQ1lfUE9MSUNZX0FDQ0VQVEVEIjoidHJ1ZSIsIkFMRVJUU19PUFRfT1VUIjoiZmFsc2UiLCJFTUFJTF9DUyI6InRydWUiLCJESVNQTEFZX05BTUVfUFJFRiI6Im4iLCJWSVNJVFNfT1BUX09VVCI6InRydWUiLCJESVNQTEFZX0NPTU1PTl9OQU1FIjoidHJ1ZSIsIkRJU1BMQVlfU0NJRU5USUZJQ19OQU1FIjoiZmFsc2UiLCJTSE9XX0NPTU1FTlRTIjoiZmFsc2UiLCJUT1AxMDBfT1BUX09VVCI6InRydWUiLCJSRUdJT05fUFJFRiI6IndvcmxkIiwiQ09NTU9OX05BTUVfTE9DQUxFIjoiZW5fVVMiLCJzcHBQcmVmIjoiY29tbW9uIn19fQ==; is-region-session.sig=VOGoh-BNI0LrkLGJ2-Q8hfLumRU; _9bf17=6e42028364b40cc5; EBIRD_SESSIONID=31175A8EB1C52E106F6EFCEDCDF115E4',
    # 'if-none-match': '"ec3eac-uGmzkrvY3Q9hiHiYYmCfi2JFvbs"',
    'priority': 'u=0, i',
    # 'referer': 'https://ebird.org/region/world/bird-list',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

def read_bird_names(file_path: str) -> List[str]:
    """
    从bird.txt文件读取鸟类名称列表
    
    Args:
        file_path: bird.txt文件路径
        
    Returns:
        鸟类名称列表
    """
    bird_names = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # 跳过空行
                    bird_names.append(line)
        print(f"成功读取 {len(bird_names)} 个鸟类名称")
        return bird_names
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
        return []
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []


def read_excel_data(file_path: str) -> pd.DataFrame:
    """
    从Excel文件读取详细分类数据
    
    Args:
        file_path: Excel文件路径
        
    Returns:
        包含url, first_name, second_name, descript列的DataFrame
    """
    try:
        df = pd.read_excel(file_path)
        print(f"成功读取Excel文件，共 {len(df)} 条记录")
        print(f"列名: {df.columns.tolist()}")
        return df
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
        return pd.DataFrame()
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        return pd.DataFrame()


def find_matches(bird_names: List[str], excel_data: pd.DataFrame) -> List[Tuple[str, str, str]]:
    """
    查找匹配的记录
    
    Args:
        bird_names: 鸟类名称列表
        excel_data: Excel数据DataFrame
        
    Returns:
        匹配结果列表，每个元素为(数据1中的鸟名, 数据2中的first_name, url)
    """
    matches = []
    
    if excel_data.empty:
        print("Excel数据为空，无法进行匹配")
        return matches
    
    # 确保first_name列存在
    if 'first_name' not in excel_data.columns:
        print("错误: Excel文件中没有找到 'first_name' 列")
        return matches
    
    # 为了提高效率，先将所有first_name转换为小写进行比较
    excel_data_copy = excel_data.copy()
    excel_data_copy['first_name_lower'] = excel_data_copy['first_name'].astype(str).str.lower()
    
    print("开始匹配...")
    
    for bird_name in bird_names:
        if not bird_name:
            continue
            
        bird_name_lower = bird_name.lower()
        
        # 查找包含当前鸟名的记录
        mask = excel_data_copy['first_name_lower'].str.contains(bird_name_lower, na=False, regex=False)
        matching_rows = excel_data_copy[mask]
        
        for _, row in matching_rows.iterrows():
            matches.append((
                bird_name,
                row['first_name'],
                row['url'] if 'url' in row and pd.notna(row['url']) else 'N/A'
            ))
    
    print(f"找到 {len(matches)} 个匹配项")
    return matches


def save_results(matches: List[Tuple[str, str, str]], output_file: str = 'matching_results.txt'):
    """
    保存匹配结果到文件
    
    Args:
        matches: 匹配结果列表
        output_file: 输出文件名
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("匹配结果\n")
            f.write("=" * 80 + "\n")
            f.write(f"{'数据1中的鸟名':<30} {'数据2中的first_name':<40} {'URL'}\n")
            f.write("-" * 80 + "\n")
            
            for bird_name, first_name, url in matches:
                f.write(f"{bird_name:<30} {first_name:<40} {url}\n")
        
        print(f"结果已保存到 {output_file}")
    except Exception as e:
        print(f"保存结果时出错: {e}")


def main():
    """主函数"""
    print("开始执行鸟类数据匹配程序...")
    
    # 文件路径
    bird_txt_path = 'bird.txt'
    excel_path = '明细分类-含url.xlsx'
    
    # 读取数据1：鸟类名称
    print("\n1. 读取bird.txt...")
    bird_names = read_bird_names(bird_txt_path)
    
    if not bird_names:
        print("没有读取到鸟类名称，程序退出")
        return
    
    # 读取数据2：Excel详细信息
    print("\n2. 读取Excel文件...")
    excel_data = read_excel_data(excel_path)
    
    if excel_data.empty:
        print("没有读取到Excel数据，程序退出")
        return
    
    # 查找匹配项
    print("\n3. 查找匹配项...")
    matches = find_matches(bird_names, excel_data)
    
    # 输出结果
    print("\n4. 输出结果...")
    if matches:
        print(f"\n找到 {len(matches)} 个匹配项:")
        print("=" * 100)
        print(f"{'数据1中的鸟名':<30} {'数据2中的first_name':<40} {'URL'}")
        print("-" * 100)
        
        for bird_name, first_name, url in matches:
            print(f"{bird_name:<30} {first_name:<40} {url}")
            get_bird_detail(url)
        # 保存结果到文件
        save_results(matches)
    else:
        print("没有找到匹配项")
    
    print("\n程序执行完成!")

def get_bird_detail(url):
    # url = 'https://ebird.org/species/eutspa'
    # url = 'https://ebird.org/species/santer1'
    # url = 'https://ebird.org/species/louflo1'
    try:
        print('详情页：', url)
        # try:
        response = requests.get(url, headers=headers)
        # print(response.text)
        bs = BeautifulSoup(response.text, 'html5lib')
        mu = bs.select('.Hero-content ul li')[0].text.strip()
        ke = bs.select('.Hero-content ul li')[1].text.strip()
        print(mu, ke)
        bird_info = bs.select('#content')[0]
        first_name = bird_info.select('span')[0].text.strip()
        second_name = bird_info.select('span')[1].text.strip()
        bird_type = bs.select('#conservation-status')[0].text.strip()
        descript = bs.select('.u-stack-sm')[0].text.replace('\r', '').replace('\n', '').replace('\t', '').strip()
        row = [url, mu, ke, first_name, second_name, bird_type, descript]
        save_detail(row)
    except:
        pass



def save_detail(row):
    import csv
    with open('detail-20250607.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

if __name__ == "__main__":
    main()
