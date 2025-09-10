# 调整颜色饱和度的 Python 脚本
# 输入：HEX 颜色列表、饱和度调整比例
# 输出：调整后的 HEX 颜色列表

import colorsys
import sys

# 从命令行参数获取颜色和饱和度
colors = sys.argv[1].split()  # 颜色列表（HEX 格式，如 #A3BFFA）
saturation = float(sys.argv[2])  # 饱和度调整比例（如 1.2）

adjusted_colors = []
for color in colors:
    # 移除 # 前缀，转换为 RGB
    hex_color = color.lstrip('#')
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
    hex_color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
    adjusted_colors.append(hex_color)

# 输出调整后的颜色（空格分隔）
print(' '.join(adjusted_colors))
