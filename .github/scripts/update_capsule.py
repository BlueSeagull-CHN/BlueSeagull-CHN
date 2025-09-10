#!/usr/bin/env python3
# update_capsule.py - 自动更新胶囊渐变效果

import json
import random
import urllib.parse
import re
import sys
import os

# 添加 scripts 目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# 现在可以正常导入
from adjust_colors import adjust_color_saturation

def main():
    # 读取配置文件（现在在根目录）
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 获取配置参数
    candidate_colors = config['gradient']['candidate_colors']
    count = config['gradient']['count']
    saturation = config['gradient']['saturation']
    header_text = config['header']['text']
    header_desc = config['header']['desc']
    
    # 随机选择颜色
    random.shuffle(candidate_colors)
    selected_colors = candidate_colors[:count]
    
    print(f"Selected colors: {selected_colors}")
    
    # 调整颜色饱和度
    adjusted_colors = []
    for color in selected_colors:
        adjusted_color = adjust_color_saturation(color, saturation)
        adjusted_colors.append(adjusted_color)
    
    print(f"Adjusted colors: {adjusted_colors}")
    
    # 构建渐变颜色参数
    color_param = ""
    for i, color in enumerate(adjusted_colors):
        position = i * 100 // (len(adjusted_colors) - 1) if len(adjusted_colors) > 1 else 0
        color_param += f"{position}:{color.lstrip('#')},"
    color_param = color_param.rstrip(',')
    
    # URL编码文本
    encoded_text = urllib.parse.quote(header_text)
    encoded_desc = urllib.parse.quote(header_desc)
    
    # 生成时间戳
    import time
    timestamp = int(time.time())
    
    # 生成新的URL
    new_header_url = f"https://capsule-render.vercel.app/api?type=waving&height=200&section=header&fontSize=40&fontAlignY=35&text={encoded_text}&desc={encoded_desc}&descAlignY=55&color={color_param}&t={timestamp}"
    new_footer_url = f"https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&color={color_param}&t={timestamp}"
    
    print(f"New header URL: {new_header_url}")
    print(f"New footer URL: {new_footer_url}")
    
    # 读取并更新README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换header URL
    content = re.sub(
        r'src="https://capsule-render\.vercel\.app/api\?[^"]*section=header[^"]*"',
        f'src="{new_header_url}"',
        content
    )
    
    # 替换footer URL
    content = re.sub(
        r'src="https://capsule-render\.vercel\.app/api\?[^"]*section=footer[^"]*"',
        f'src="{new_footer_url}"',
        content
    )
    
    # 写回README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("README updated successfully!")

if __name__ == "__main__":
    main()
