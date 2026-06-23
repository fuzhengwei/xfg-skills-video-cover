#!/usr/bin/env python3
"""
视频封面生成器 v2.0 - 主脚本
支持多平台尺寸（B站/小红书/视频号）、20+套配色、卡通素材、多页输出。
"""

import argparse
import json
import re
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from extract_chapters import extract_chapters_from_html
except ImportError:
    def extract_chapters_from_html(content):
        return []


# ========== 平台尺寸 ==========
PLATFORMS = {
    "bilibili": {
        "name": "B站",
        "ratio": "16 / 9",
        "width": 1200,
        "height": 675,
        "title_size": 82,
        "subtitle_size": 28,
        "tag_size": 15,
        "badge_size": 14,
        "padding": 40,
    },
    "xiaohongshu": {
        "name": "小红书",
        "ratio": "3 / 4",
        "width": 900,
        "height": 1200,
        "title_size": 64,
        "subtitle_size": 24,
        "tag_size": 14,
        "badge_size": 13,
        "padding": 36,
    },
    "wechat": {
        "name": "微信视频号",
        "ratio": "9 / 16",
        "width": 1080,
        "height": 1920,
        "title_size": 56,
        "subtitle_size": 22,
        "tag_size": 13,
        "badge_size": 12,
        "padding": 32,
    },
}

# ========== 20+套爆款配色 ==========
COLOR_SCHEMES = {
    # --- 科技主题 ---
    "tech_1": {"bg": "#0f0e17", "accent1": "#ff8906", "accent2": "#f25f4c", "name": "暗夜火焰", "theme": "tech"},
    "tech_2": {"bg": "#1a1a2e", "accent1": "#e94560", "accent2": "#0f3460", "name": "赛博朋克", "theme": "tech"},
    "tech_3": {"bg": "#0d1117", "accent1": "#58a6ff", "accent2": "#7ee787", "name": "极客绿", "theme": "tech"},
    "tech_4": {"bg": "#1a1a2e", "accent1": "#e74c3c", "accent2": "#f39c12", "name": "科技红橙", "theme": "tech"},
    "tech_5": {"bg": "#0a0e27", "accent1": "#00d9ff", "accent2": "#9d4edd", "name": "电光紫蓝", "theme": "tech"},

    # --- 热情活力 ---
    "hot_1": {"bg": "#2d0a0a", "accent1": "#fbbf24", "accent2": "#f87171", "name": "火焰金红", "theme": "hot"},
    "hot_2": {"bg": "#3d0a0a", "accent1": "#ff6b6b", "accent2": "#ffd93d", "name": "热情黄红", "theme": "hot"},
    "hot_3": {"bg": "#2a0a0a", "accent1": "#fb923c", "accent2": "#f97316", "name": "压测火焰", "theme": "hot"},
    "hot_4": {"bg": "#1a0505", "accent1": "#ef4444", "accent2": "#f59e0b", "name": "爆裂红金", "theme": "hot"},

    # --- 清爽冷色 ---
    "cool_1": {"bg": "#0d1b2a", "accent1": "#00b4d8", "accent2": "#90e0ef", "name": "深海蓝青", "theme": "cool"},
    "cool_2": {"bg": "#0a2e0a", "accent1": "#4ade80", "accent2": "#86efac", "name": "森林绿", "theme": "cool"},
    "cool_3": {"bg": "#0f1c2e", "accent1": "#06b6d4", "accent2": "#67e8f9", "name": "冰蓝青", "theme": "cool"},
    "cool_4": {"bg": "#0d2818", "accent1": "#10b981", "accent2": "#6ee7b7", "name": "翡翠绿", "theme": "cool"},

    # --- 温暖柔和 ---
    "warm_1": {"bg": "#2e0a1a", "accent1": "#f9a8d4", "accent2": "#ec4899", "name": "玫瑰粉", "theme": "warm"},
    "warm_2": {"bg": "#1a0a2e", "accent1": "#f72585", "accent2": "#4cc9f0", "name": "品红蓝紫", "theme": "warm"},
    "warm_3": {"bg": "#2e1a0a", "accent1": "#fbbf24", "accent2": "#fb7185", "name": "暖阳金粉", "theme": "warm"},
    "warm_4": {"bg": "#1e1b4b", "accent1": "#fbbf24", "accent2": "#818cf8", "name": "靛蓝紫金", "theme": "warm"},

    # --- 暗黑酷炫 ---
    "dark_1": {"bg": "#0a0a0a", "accent1": "#fbbf24", "accent2": "#ffffff", "name": "黑金奢华", "theme": "dark"},
    "dark_2": {"bg": "#111111", "accent1": "#ef4444", "accent2": "#6b7280", "name": "暗血红灰", "theme": "dark"},
    "dark_3": {"bg": "#0a0a0a", "accent1": "#22d3ee", "accent2": "#a3e635", "name": "黑客霓虹", "theme": "dark"},

    # --- 渐变潮流 ---
    "gradient_1": {"bg": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "accent1": "#ffd700", "accent2": "#ffffff", "name": "紫金渐变", "theme": "gradient", "is_gradient": True},
    "gradient_2": {"bg": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", "accent1": "#ffd700", "accent2": "#ffffff", "name": "粉红渐变", "theme": "gradient", "is_gradient": True},
    "gradient_3": {"bg": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)", "accent1": "#ffffff", "accent2": "#ffe066", "name": "天蓝渐变", "theme": "gradient", "is_gradient": True},
    "gradient_4": {"bg": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)", "accent1": "#ffffff", "accent2": "#7c2d12", "name": "日落渐变", "theme": "gradient", "is_gradient": True},
}

# ========== 主题关键词匹配 ==========
THEME_KEYWORDS = {
    "tech": ["AI", "Shell", "API", "代码", "编程", "程序", "服务器", "云", "IDE", "CLI", "Key", "密钥", "模型", "Ollama", "qwen", "GPT"],
    "hot": ["教程", "入门", "实战", "安装", "部署", "上线", "新手", "快速"],
    "cool": ["Docker", "容器", "MySQL", "Redis", "数据库", "缓存", "Portainer", "Nginx"],
    "warm": ["对话", "客服", "设计", "生活", "沟通", "SSE", "流式"],
    "dark": ["安全", "黑客", "高级", "硬核", "渗透", "密码"],
    "gradient": ["时尚", "创意", "爆款", "热门", "推荐"],
}

# ========== 主题 Emoji 匹配 ==========
THEME_EMOJIS = {
    "tech": [("1f680", "🚀"), ("26a1", "⚡"), ("1f4bb", "💻"), ("1f310", "🌐"), ("1f527", "🔧"), ("1f4e1", "📡")],
    "hot": [("1f525", "🔥"), ("2b50", "⭐"), ("1f4a5", "💥"), ("1f3af", "🎯"), ("1f389", "🎉"), ("26a1", "⚡")],
    "cool": [("1f433", "🐳"), ("1f4e6", "📦"), ("1f5c3", "🗄️"), ("1f510", "🔐"), ("1f4be", "💾"), ("1f4ca", "📊")],
    "warm": [("1f49b", "💛"), ("1f4ac", "💬"), ("1f917", "🤗"), ("1f4f1", "📱"), ("2728", "✨"), ("1f4ad", "💭")],
    "dark": [("1f576", "🕶️"), ("1f512", "🔒"), ("1f480", "💀"), ("1f451", "👑"), ("1f9e0", "🧠"), ("1f4a1", "💡")],
    "gradient": [("2728", "✨"), ("1f308", "🌈"), ("1f4ab", "💫"), ("1f31f", "🌟"), ("1f48e", "💎"), ("1f3a7", "🎧")],
}

# 通用 emoji（任意主题可用）
GENERAL_EMOJIS = [
    ("1f680", "🚀"), ("26a1", "⚡"), ("1f4bb", "💻"), ("1f310", "🌐"),
    ("1f525", "🔥"), ("2b50", "⭐"), ("2728", "✨"), ("1f4a1", "💡"),
    ("1f3af", "🎯"), ("1f389", "🎉"), ("1f4aa", "💪"), ("1f9e0", "🧠"),
]

# Twemoji CDN
TWEMOJI_CDN = "https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/svg"


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return "255,255,255"
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"{r},{g},{b}"


def detect_theme(title, tags=None):
    """根据标题和标签智能匹配主题"""
    text = (title or "").lower()
    if tags:
        text += " " + " ".join(tags).lower()
    
    scores = {}
    for theme, keywords in THEME_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw.lower() in text:
                score += 1
        if score > 0:
            scores[theme] = score
    
    if scores:
        return max(scores, key=scores.get)
    return "tech"  # 默认科技


def get_scheme_by_theme(theme, index=0):
    """根据主题获取配色方案"""
    theme_schemes = [k for k, v in COLOR_SCHEMES.items() if v["theme"] == theme]
    if not theme_schemes:
        theme_schemes = list(COLOR_SCHEMES.keys())
    return theme_schemes[index % len(theme_schemes)]


def get_emojis_for_theme(theme, count=2, index=0):
    """获取主题对应的 emoji"""
    emojis = THEME_EMOJIS.get(theme, GENERAL_EMOJIS)
    start = index * 2
    e1 = emojis[start % len(emojis)]
    e2 = emojis[(start + 1) % len(emojis)]
    # 如果主题emoji不够2个，补充通用emoji
    if len(emojis) < 2:
        e1 = GENERAL_EMOJIS[index % len(GENERAL_EMOJIS)]
        e2 = GENERAL_EMOJIS[(index + 5) % len(GENERAL_EMOJIS)]
    return e1, e2


def get_twemoji_url(codepoint):
    """获取 Twemoji SVG CDN URL"""
    return f"{TWEMOJI_CDN}/{codepoint}.svg"


def generate_single_cover(cover_config, platform_key="bilibili", index=0):
    """生成单个封面页的 HTML"""
    
    pf = PLATFORMS.get(platform_key, PLATFORMS["bilibili"])
    
    title = cover_config.get("title", "")
    highlight_words = cover_config.get("highlight_words", [])
    subtitle = cover_config.get("subtitle", "")
    tags = cover_config.get("tags", [])
    badge = cover_config.get("badge", "")
    quote = cover_config.get("quote", "")
    theme = cover_config.get("theme", "auto")
    
    # 自动检测主题
    if theme == "auto":
        theme = detect_theme(title, tags)
    
    # 获取配色
    scheme_key = cover_config.get("scheme")
    if not scheme_key:
        scheme_key = get_scheme_by_theme(theme, index)
    scheme = COLOR_SCHEMES[scheme_key]
    
    bg_color = cover_config.get("bg_color", scheme["bg"])
    accent1 = cover_config.get("accent1", scheme["accent1"])
    accent2 = cover_config.get("accent2", scheme["accent2"])
    is_gradient = scheme.get("is_gradient", False)
    
    # 获取 emoji
    emoji1, emoji2 = get_emojis_for_theme(theme, 2, index)
    emoji1_char = emoji1[1]
    emoji2_char = emoji2[1]
    emoji1_url = get_twemoji_url(emoji1[0])
    emoji2_url = get_twemoji_url(emoji2[0])
    
    # 处理高亮词
    display_title = title
    for i, word in enumerate(highlight_words):
        color = accent1 if i % 2 == 0 else accent2
        display_title = display_title.replace(
            word,
            f'<span class="highlight" style="color:{color};">{word}</span>'
        )
    
    # 生成标签
    tags_html = ""
    for i, tag in enumerate(tags):
        tag_color = [accent1, accent2, accent1, accent2][i % 4]
        opacity = 0.25 if i % 2 == 0 else 0.20
        tags_html += f'        <span class="cv-tag" style="background:rgba({hex_to_rgb(tag_color)},{opacity});color:{tag_color};">{tag}</span>\n'
    
    # 背景样式
    if is_gradient:
        bg_style = f"background: {bg_color};"
    else:
        bg_style = f"background: {bg_color};"
    
    ts = pf["title_size"]
    ss = pf["subtitle_size"]
    tgs = pf["tag_size"]
    bs = pf["badge_size"]
    pd = pf["padding"]
    
    # emoji 装饰尺寸
    emoji1_size = int(ts * 1.1)
    emoji2_size = int(ts * 0.8)
    
    html = f'''  <div class="cover-card cover-{platform_key}" data-platform="{pf["name"]}" data-index="{index+1}" style="--bg-color: {bg_color}; --accent1: {accent1}; --accent2: {accent2};">
    <div class="cv-bg-decoration">
      <div class="cv-bg-circle" style="width:{350+index*20}px;height:{350+index*20}px;background:{accent1};top:-{80+index*10}px;left:-{80+index*10}px;"></div>
      <div class="cv-bg-circle" style="width:{260+index*15}px;height:{260+index*15}px;background:{accent2};bottom:-60px;right:-60px;"></div>
      <img class="cv-emoji-deco cv-emoji-1" src="{emoji1_url}" alt="{emoji1_char}" style="top:{15+index*3}%;left:6%;width:{emoji1_size}px;height:{emoji1_size}px;" onerror="this.style.display='none'">
      <img class="cv-emoji-deco cv-emoji-2" src="{emoji2_url}" alt="{emoji2_char}" style="bottom:{12+index*3}%;right:8%;width:{emoji2_size}px;height:{emoji2_size}px;" onerror="this.style.display='none'">
    </div>
    <div class="cv-content">
      <div class="cv-badge" style="background:rgba({hex_to_rgb(accent1)},0.2);color:{accent1};border:1px solid rgba({hex_to_rgb(accent1)},0.4);">{emoji1_char} {badge}</div>
      <div class="cv-main-title" style="font-size:{ts}px;">
        {display_title}
      </div>
      <div class="cv-sub-title" style="font-size:{ss}px;">{subtitle}</div>
      <div class="cv-tag-row">
{tags_html}      </div>
    </div>
    <div class="cv-bottom-bar"><span>{emoji2_char} {quote}</span><span>{pf["name"]} · {index+1}</span></div>
  </div>'''
    
    return html


def generate_full_html(covers, platform="bilibili", theme="auto"):
    """生成完整的 HTML 文件"""
    
    # 确定要生成的平台列表
    if platform == "all":
        platform_keys = ["bilibili", "xiaohongshu", "wechat"]
    else:
        platform_keys = [platform]
    
    # 为每个 cover 生成每个平台的页面
    all_pages = []
    page_labels = []
    
    for cover_idx, cover in enumerate(covers):
        # 如果是单个 cover 且 platform=all，用同一个 cover 生成3个平台
        for pf_key in platform_keys:
            # 对于多cover+all的情况，每个cover都生成3个平台页
            page_html = generate_single_cover(cover, pf_key, cover_idx)
            all_pages.append(page_html)
            pf_name = PLATFORMS[pf_key]["name"]
            page_labels.append(f"{pf_name}")
    
    covers_html = "\n\n".join(all_pages)
    
    # 生成多平台 CSS
    platform_css = ""
    for pk, pv in PLATFORMS.items():
        platform_css += f"""
  .cover-{pk} {{
    aspect-ratio: {pv["ratio"]};
    max-width: {pv["width"]}px;
  }}"""
    
    # 需要的最大标题尺寸
    max_ts = max(pf["title_size"] for pf in PLATFORMS.values())
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>视频封面 · 多平台预览</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;900&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0a0a0f;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 32px;
    padding: 40px 20px;
    min-height: 100vh;
  }}

  .page-label {{
    color: rgba(255,255,255,0.3);
    font-size: 14px;
    font-weight: 600;
    margin-top: -20px;
    margin-bottom: -12px;
    letter-spacing: 2px;
  }}

  .cover-card {{
    width: 94vw;
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    text-align: center;
    background: var(--bg-color, #1a1a2e);
  }}
{platform_css}

  .cv-bg-decoration {{
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
  }}

  .cv-bg-circle {{
    position: absolute;
    border-radius: 50%;
    opacity: 0.06;
  }}

  .cv-content {{
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    padding: 40px;
  }}

  .cv-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 16px;
  }}

  .cv-main-title {{
    font-weight: 900;
    line-height: 1.08;
    letter-spacing: 2px;
    margin-bottom: 10px;
    text-shadow: 0 4px 20px rgba(0,0,0,0.4);
    max-width: 90%;
  }}

  .cv-main-title .highlight {{
    display: inline-block;
    transform: rotate(-3deg);
  }}

  .cv-sub-title {{
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 1px;
    max-width: 85%;
  }}

  .cv-tag-row {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 14px;
  }}

  .cv-tag {{
    padding: 6px 18px;
    border-radius: 16px;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}

  .cv-emoji-deco {{
    position: absolute;
    opacity: 0.10;
    z-index: 1;
    object-fit: contain;
  }}

  .cv-bottom-bar {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 36px;
    background: rgba(0,0,0,0.35);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    font-size: 13px;
    color: rgba(255,255,255,0.5);
    z-index: 4;
    backdrop-filter: blur(4px);
  }}

  /* 小红书 竖版调整 */
  .cover-xiaohongshu .cv-content {{
    padding: 36px 32px;
  }}
  .cover-xiaohongshu .cv-main-title {{
    line-height: 1.12;
  }}

  /* 微信视频号 全竖屏调整 */
  .cover-wechat .cv-content {{
    padding: 32px 28px;
  }}
  .cover-wechat .cv-main-title {{
    line-height: 1.15;
  }}
  .cover-wechat .cv-badge {{
    margin-bottom: 24px;
  }}

  /* 渐变背景 */
  .cover-card[style*="linear-gradient"] {{
    background: var(--bg-color);
  }}
</style>
</head>
<body>

{covers_html}

</body>
</html>'''
    
    return html


def covers_from_chapters(chapters, theme="auto"):
    """从提取的章节信息生成封面配置"""
    covers = []
    for i, ch in enumerate(chapters):
        cover = {
            "title": ch.get("title", f"第{ch.get('number', i+1)}节"),
            "highlight_words": ch.get("highlight_words", []),
            "subtitle": ch.get("subtitle", ch.get("description", "")),
            "tags": ch.get("tags", []),
            "badge": ch.get("badge", f"第{ch.get('number', i+1)}节"),
            "quote": ch.get("quote", ""),
            "theme": theme,
        }
        covers.append(cover)
    return covers


def main():
    parser = argparse.ArgumentParser(
        description="视频封面生成器 v2.0 - 多平台/多主题/卡通素材",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从文本生成（B站单页）
  python3 generate_covers.py --title "Docker一装，运维轻松10倍" --platform bilibili

  # 从文本生成（全平台3页）
  python3 generate_covers.py --title "给爷来个Key" --platform all --theme tech

  # 从 PPT 提取章节生成
  python3 generate_covers.py --input ppt.html --output covers.html --platform all

  # 从 JSON 配置批量生成
  python3 generate_covers.py --config covers.json --output covers.html
        """
    )
    
    parser.add_argument("--input", "-i", help="PPT/HTML 输入文件路径")
    parser.add_argument("--output", "-o", default="video-covers.html", help="输出 HTML 文件路径")
    parser.add_argument("--config", "-c", help="JSON 配置文件路径")
    parser.add_argument("--platform", "-p", default="bilibili", choices=["bilibili", "xiaohongshu", "wechat", "all"], help="平台尺寸")
    parser.add_argument("--theme", default="auto", choices=["auto", "tech", "hot", "cool", "warm", "dark", "gradient"], help="配色主题")
    parser.add_argument("--extract-only", action="store_true", help="仅提取章节信息")
    
    # 单页生成参数
    parser.add_argument("--title", "-t", help="主标题")
    parser.add_argument("--subtitle", help="副标题")
    parser.add_argument("--tags", help="标签（逗号分隔）")
    parser.add_argument("--badge", help="Badge 文本")
    parser.add_argument("--quote", help="底部金句")
    parser.add_argument("--highlight", help="高亮词（逗号分隔）")
    parser.add_argument("--bg-color", help="背景色（十六进制或渐变）")
    parser.add_argument("--accent-color", help="主色调（十六进制）")
    
    args = parser.parse_args()
    
    # === 模式1：从 PPT 提取 ===
    if args.input:
        if not os.path.exists(args.input):
            print(f"错误：文件不存在 - {args.input}", file=sys.stderr)
            sys.exit(1)
        
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
        
        chapters = extract_chapters_from_html(content)
        
        if args.extract_only:
            print(json.dumps(chapters, ensure_ascii=False, indent=2))
            return
        
        if not chapters:
            print("警告：未提取到章节信息", file=sys.stderr)
            chapters = [{"number": 1, "title": "视频封面"}]
        
        covers = covers_from_chapters(chapters, args.theme)
        html = generate_full_html(covers, args.platform, args.theme)
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        
        pf_count = 3 if args.platform == "all" else 1
        print(f"✅ 成功生成 {len(covers)} 个封面 × {pf_count} 平台 = {len(covers)*pf_count} 页 → {args.output}")
        return
    
    # === 模式2：从 JSON 配置 ===
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        covers = config.get("covers", [])
        platform = config.get("platform", args.platform)
        theme = config.get("theme", args.theme)
        
        if not covers:
            print("错误：配置文件中没有 covers", file=sys.stderr)
            sys.exit(1)
        
        html = generate_full_html(covers, platform, theme)
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        
        pf_count = 3 if platform == "all" else 1
        print(f"✅ 成功生成 {len(covers)} 个封面 × {pf_count} 平台 = {len(covers)*pf_count} 页 → {args.output}")
        return
    
    # === 模式3：从命令行参数生成 ===
    if args.title:
        highlight_words = [w.strip() for w in args.highlight.split(",")] if args.highlight else []
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        
        cover = {
            "title": args.title,
            "highlight_words": highlight_words,
            "subtitle": args.subtitle or "",
            "tags": tags,
            "badge": args.badge or "",
            "quote": args.quote or "",
            "theme": args.theme,
        }
        
        if args.bg_color:
            cover["bg_color"] = args.bg_color
        if args.accent_color:
            cover["accent1"] = args.accent_color
        
        html = generate_full_html([cover], args.platform, args.theme)
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        
        pf_count = 3 if args.platform == "all" else 1
        print(f"✅ 成功生成 1 个封面 × {pf_count} 平台 = {pf_count} 页 → {args.output}")
        return
    
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
