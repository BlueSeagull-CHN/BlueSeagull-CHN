# 动态渐变系统使用说明

## 文件结构
- `.github/scripts/update_capsule.py` - 主更新脚本
- `.github/scripts/adjust_colors.py` - 颜色调整工具
- `config.json` - 配置文件
- `.github/workflows/update-gradient.yml` - GitHub Actions工作流

## 配置选项
- `candidate_colors`: 候选颜色池
- `count`: 每次选择的颜色数量
- `saturation`: 饱和度调整
- `schedule`: 自动更新频率
