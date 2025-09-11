# adjust_colors.py - 调整颜色饱和度
import colorsys

def adjust_color_saturation(hex_color, saturation):
    """调整单个颜色的饱和度"""
    try:
        # 验证输入
        if not isinstance(hex_color, str) or not hex_color.startswith('#') or len(hex_color) != 7:
            raise ValueError(f"无效的颜色格式: {hex_color}")
        
        if not isinstance(saturation, (int, float)) or saturation <= 0:
            raise ValueError(f"无效的饱和度值: {saturation}")
        
        hex_color = hex_color.lstrip('#')
        
        # 验证十六进制颜色
        try:
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
        except ValueError:
            raise ValueError(f"无效的十六进制颜色: #{hex_color}")
        
        # RGB -> HSL
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        
        # 调整饱和度，限制在 0-1
        s = min(max(s * saturation, 0.0), 1.0)
        
        # HSL -> RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        
        # 转换为 HEX
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
    
    except Exception as e:
        raise ValueError(f"调整颜色饱和度时出错: {e}")

# 保留命令行接口
if __name__ == "__main__":
    import sys
    try:
        # 从命令行参数获取颜色和饱和度
        if len(sys.argv) < 3:
            print("用法: python adjust_colors.py '<颜色列表>' <饱和度>")
            print("示例: python adjust_colors.py '#C1E1C1 #F8C8DC' 1.2")
            sys.exit(1)
        
        colors = sys.argv[1].split()
        saturation = float(sys.argv[2])
        
        if not colors:
            raise ValueError("未提供颜色参数")
        
        adjusted_colors = []
        for color in colors:
            adjusted_color = adjust_color_saturation(color, saturation)
            adjusted_colors.append(adjusted_color)
        
        # 输出调整后的颜色（空格分隔）
        print(' '.join(adjusted_colors))
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
