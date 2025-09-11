import colorsys
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python adjust_colors.py '<colors>' <saturation>")
        return
    
    colors = sys.argv[1].split()
    saturation = float(sys.argv[2])
    
    adjusted = []
    for color in colors:
        # 确保颜色有 # 前缀
        if not color.startswith('#'):
            color = '#' + color
        hex_color = color[1:]
        
        # 转换RGB
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        
        # 调整饱和度
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        s = max(0.0, min(s * saturation, 1.0))
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        
        # 转换回HEX
        adjusted.append(f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}')
    
    print(' '.join(adjusted))

if __name__ == "__main__":
    main()
