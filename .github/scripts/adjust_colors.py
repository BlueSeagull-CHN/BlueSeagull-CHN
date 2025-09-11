import colorsys
import sys

colors = sys.argv[1].split()
saturation = float(sys.argv[2])

adjusted_colors = []
for color in colors:
    hex_color = color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = min(max(s * saturation, 0.0), 1.0)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    
    adjusted_colors.append(f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}')

print(' '.join(adjusted_colors))
