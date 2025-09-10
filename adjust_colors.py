# 调整颜色饱和度的 Python 脚本
import colorsys
import sys

def adjust_color_saturation(hex_color, saturation):
    """调整单个颜色的饱和度"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    
    # RGB -> HSL
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # 调整饱和度，限制在 0-1
    s = min(max(s * saturation, 0.0), 1.0)
    
    # HSL -> RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    
    # 转换为 HEX
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

if __name__ == "__main__":
    # 从命令行参数获取颜色和饱和度
    colors = sys.argv[1].split() if len(sys.argv) > 1 else []
    saturation = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

    adjusted_colors = []
    for color in colors:
        adjusted_color = adjust_color_saturation(color, saturation)
        adjusted_colors.append(adjusted_color)

    # 输出调整后的颜色（空格分隔）
    print(' '.join(adjusted_colors))
