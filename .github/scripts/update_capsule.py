#!/usr/bin/env python3
# update_capsule.py - 自动更新胶囊渐变效果

import json
import random
import urllib.parse
import re
import sys
import os
import time
from datetime import datetime

# 添加 scripts 目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# 现在可以正常导入
from adjust_colors import adjust_color_saturation

# 常量定义
CACHE_FILE = '.gradient_cache.json'
STATS_FILE = '.gradient_stats.json'

def validate_config(config):
    """验证配置文件格式"""
    print("开始验证配置文件...")
    
    # 检查必需的主键
    required_keys = ['gradient', 'header']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"❌ 缺少必需的配置项: {key}")
    
    # 检查 gradient 配置
    gradient = config['gradient']
    gradient_required = ['candidate_colors', 'count', 'saturation']
    for key in gradient_required:
        if key not in gradient:
            raise ValueError(f"❌ gradient 中缺少配置项: {key}")
    
    # 检查 header 配置
    header = config['header']
    header_required = ['text', 'desc']
    for key in header_required:
        if key not in header:
            raise ValueError(f"❌ header 中缺少配置项: {key}")
    
    # 验证颜色格式
    candidate_colors = gradient['candidate_colors']
    if not isinstance(candidate_colors, list) or len(candidate_colors) < 2:
        raise ValueError("❌ candidate_colors 必须是一个包含至少2个颜色的列表")
    
    for i, color in enumerate(candidate_colors):
        if not isinstance(color, str) or not color.startswith('#') or len(color) != 7:
            raise ValueError(f"❌ 颜色格式错误 (索引 {i}): {color}。必须是 #RRGGBB 格式")
        try:
            int(color[1:], 16)  # 验证是有效的十六进制
        except ValueError:
            raise ValueError(f"❌ 无效的十六进制颜色 (索引 {i}): {color}")
    
    # 验证数值范围
    if not isinstance(gradient['count'], int) or gradient['count'] < 2 or gradient['count'] > 10:
        raise ValueError("❌ count 必须是 2-10 之间的整数")
    
    if not isinstance(gradient['saturation'], (int, float)) or gradient['saturation'] < 0.1 or gradient['saturation'] > 3.0:
        raise ValueError("❌ saturation 必须是 0.1-3.0 之间的数字")
    
    # 验证选择的颜色数量不超过候选颜色数量
    if gradient['count'] > len(candidate_colors):
        raise ValueError(f"❌ count ({gradient['count']}) 不能大于候选颜色数量 ({len(candidate_colors)})")
    
    print("✅ 配置文件验证通过")

def get_cached_gradient():
    """获取缓存的渐变配置"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                # 检查缓存是否过期（24小时）
                if time.time() - cache_data.get('timestamp', 0) < 86400:
                    print("📦 使用缓存的渐变配置")
                    return cache_data
                else:
                    print("📦 缓存已过期，生成新的渐变")
    except Exception as e:
        print(f"⚠️  读取缓存失败: {e}")
    return None

def cache_gradient(colors, timestamp):
    """缓存当前渐变配置"""
    try:
        cache_data = {
            'colors': colors,
            'timestamp': timestamp,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hex_colors': [color.lstrip('#') for color in colors]
        }
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
        print("💾 渐变配置已缓存")
    except Exception as e:
        print(f"⚠️  缓存保存失败: {e}")

def update_stats(success=True, colors_count=0):
    """更新运行统计"""
    stats = {
        'total_runs': 0,
        'successful_runs': 0,
        'failed_runs': 0,
        'last_run': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'last_status': 'success' if success else 'failed',
        'history': []
    }
    
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                stats = json.load(f)
    except Exception as e:
        print(f"⚠️  读取统计文件失败: {e}")
    
    stats['total_runs'] += 1
    if success:
        stats['successful_runs'] += 1
    else:
        stats['failed_runs'] += 1
    stats['last_run'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    stats['last_status'] = 'success' if success else 'failed'
    
    # 添加历史记录
    stats['history'].append({
        'time': stats['last_run'],
        'status': 'success' if success else 'failed',
        'colors_count': colors_count,
        'timestamp': int(time.time())
    })
    
    # 只保留最近20次记录
    stats['history'] = stats['history'][-20:]
    
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print("📊 运行统计已更新")
    except Exception as e:
        print(f"⚠️  保存统计失败: {e}")

def main():
    try:
        print("🚀 开始更新胶囊渐变效果...")
        print(f"📅 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 检查缓存
        cache = get_cached_gradient()
        if cache:
            # 使用缓存的颜色
            adjusted_colors = [f"#{color}" for color in cache['hex_colors']]
            timestamp = cache['timestamp']
            print(f"🎯 使用缓存颜色: {adjusted_colors}")
        else:
            # 读取配置文件
            config_path = 'config.json'
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"❌ 配置文件不存在: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证配置
            validate_config(config)
            
            # 获取配置参数
            candidate_colors = config['gradient']['candidate_colors']
            count = config['gradient']['count']
            saturation = config['gradient']['saturation']
            header_text = config['header']['text']
            header_desc = config['header']['desc']
            
            print(f"📊 配置参数: count={count}, saturation={saturation}")
            print(f"🎨 候选颜色数量: {len(candidate_colors)}")
            
            # 随机选择颜色
            random.shuffle(candidate_colors)
            selected_colors = candidate_colors[:count]
            
            print(f"✅ 选择的颜色: {selected_colors}")
            
            # 调整颜色饱和度
            adjusted_colors = []
            for color in selected_colors:
                adjusted_color = adjust_color_saturation(color, saturation)
                adjusted_colors.append(adjusted_color)
            
            print(f"🎯 调整后的颜色: {adjusted_colors}")
            
            # 生成时间戳
            timestamp = int(time.time())
            
            # 缓存新的渐变配置
            cache_gradient(adjusted_colors, timestamp)
        
        # 构建胶囊渐变颜色参数（使用冒号分隔）
        color_param = ""
        for i, color in enumerate(adjusted_colors):
            position = i * 100 // (len(adjusted_colors) - 1) if len(adjusted_colors) > 1 else 0
            color_param += f"{position}:{color.lstrip('#')},"
        color_param = color_param.rstrip(',')

        # 构建GitHub Stats背景渐变参数（使用冒号分隔位置和颜色）
        stats_bg_param = ""
        for i, color in enumerate(adjusted_colors):
            position = i * 100 // (len(adjusted_colors) - 1) if len(adjusted_colors) > 1 else 0
            stats_bg_param += f"{position}:{color.lstrip('#')},"
        stats_bg_param = stats_bg_param.rstrip(',')

        # URL编码文本
        encoded_text = urllib.parse.quote(header_text)
        encoded_desc = urllib.parse.quote(header_desc)
        
        # 生成新的URL
        new_header_url = f"https://capsule-render.vercel.app/api?type=waving&height=200&section=header&fontSize=40&fontAlignY=35&text={encoded_text}&desc={encoded_desc}&descAlignY=55&color={color_param}&t={timestamp}"
        new_footer_url = f"https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&color={color_param}&t={timestamp}"
        new_stats_url = f"https://github-readme-stats-bay.vercel.app/api?username=BlueSeagull-CHN&hide_title=true&hide_border=true&show_icons=true&include_all_commits=true&line_height=21&bg_color={stats_bg_param}&theme=graywhite"
        
        print(f"🔗 新的Header URL: {new_header_url}")
        print(f"🔗 新的Footer URL: {new_footer_url}")
        print(f"📊 新的Stats URL: {new_stats_url}")
        
        # 读取并更新README
        readme_path = 'README.md'
        if not os.path.exists(readme_path):
            raise FileNotFoundError(f"❌ README.md 不存在: {readme_path}")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
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
        
        # 替换GitHub Stats背景（使用更精确的匹配）
        stats_pattern = r'https://github-readme-stats-bay\.vercel\.app/api\?[^"]*bg_color=[^"&]*[^"]*'
        content = re.sub(stats_pattern, new_stats_url, content)
        
        # 写回README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("🎉 README 更新成功！")
        print("📋 摘要:")
        print(f"   - 使用了 {len(adjusted_colors)} 种颜色")
        print(f"   - 时间戳: {timestamp}")
        
        # 更新统计（成功）
        update_stats(success=True, colors_count=len(adjusted_colors))
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        # 更新统计（失败）
        update_stats(success=False, colors_count=0)
        sys.exit(1)

if __name__ == "__main__":
    main()
