#!/usr/bin/env python3
"""
视频封面生成器 - 主脚本
支持从 PPT/HTML 提取章节、从文本描述生成、从 JSON 配置批量生成。
"""

import argparse
import json
import re
import sys
import os
from pathlib import Path

# Add scripts dir to path for sibling imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from extract_chapters import extract_chapters_from_html
except ImportError:
    # Fallback if extract_chapters is not available
    def extract_chapters_from_html(content):
        return []


# === 配色方案 ===
COLOR_SCHEMES = [
    {"bg": "#1a1a2e", "accent1": "#e74c3c", "accent2": "#f39c12", "name": "深蓝红橙"},
    {"bg": "#0d1b2a", "accent1": "#00b4d8", "accent2": "#90e0ef", "name": "深海蓝青"},
    {"bg": "#1a0a2e", "accent1": "#f72585", "accent2": "#4cc9f0", "name": "深紫品红"},
    {"bg": "#2d0a0a", "accent1": "#fbbf24", "accent2": "#f87171", "name": "深红金黄"},
    {"bg": "#0a2e0a", "accent1": "#4ade80", "accent2": "#86efac", "name": "深绿亮绿"},
    {"bg": "#1e1b4b", "accent1": "#fbbf24", "accent2": "#818cf8", "name": "靛蓝紫"},
    {"bg": "#2a0a0a", "accent1": "#fb923c", "accent2": "#f97316", "name": "深棕橙红"},
    {"bg": "#0a1a2e", "accent1": "#38bdf8", "accent2": "#7dd3fc", "name": "深蓝天蓝"},
    {"bg": "#2e0a1a", "accent1": "#f9a8d4", "accent2": "#ec4899", "name": "深玫红粉"},
]

# === Emoji 装饰库 ===
EMOJI_DECORATIONS = ["🚀", "⚡", "🐳", "📦", "🗄️", "🔐", "💾", "🔥", "📊", "🤖", "🧠", "💬", "💻", "🌐", "✨", "💡", "🎯", "🎉"]


def generate_single_cover(cover_config, index=0):
    """生成单个封面页的 HTML"""
    
    title = cover_config.get("title", "")
    highlight_words = cover_config.get("highlight_words", [])
    subtitle = cover_config.get("subtitle", "")
    tags = cover_config.get("tags", [])
    chapter = cover_config.get("chapter", index + 1)
    badge = cover_config.get("badge", "")
    quote = cover_config.get("quote", "")
    bg_color = cover_config.get("bg_color", COLOR_SCHEMES[index % len(COLOR_SCHEMES)]["bg"])
    accent1 = cover_config.get("accent1", COLOR_SCHEMES[index % len(COLOR_SCHEMES)]["accent1"])
    accent2 = cover_config.get("accent2", COLOR_SCHEMES[index % len(COLOR_SCHEMES)]["accent2"])
    
    # 处理高亮词
    display_title = title
    for word in highlight_words:
        color = accent1 if highlight_words.index(word) % 2 == 0 else accent2
        display_title = display_title.replace(
            word,
            f'<span class="highlight" style="color:{color};">{word}</span>'
        )
    
    # 生成标签
    tags_html = ""
    for i, tag in enumerate(tags):
        tag_color = [accent1, accent2, accent1, accent2][i % 4]
        opacity = 0.25 if i % 2 == 0 else 0.20
        tags_html += f'''        <span class="bili-tag" style="background:rgba({hex_to_rgb(tag_color)},{opacity});color:{tag_color};">{tag}</span>\n'''
    
    # 印章类型
    stamp_type = "实战"
    if chapter >= 9:
        stamp_type = "完结"
    elif chapter >= 7:
        stamp_type = "进阶"
    elif chapter == 6:
        stamp_type = "上线"
    
    # emoji 装饰
    emoji1 = EMOJI_DECORATIONS[index % len(EMOJI_DECORATIONS)]
    emoji2 = EMOJI_DECORATIONS[(index + 7) % len(EMOJI_DECORATIONS)]
    
    html = f'''  <div class="slide-card slide-bili-cover" id="cover-{index+1}" style="--bg-color: {bg_color};">
    <div class="bili-bg-decoration">
      <div class="bili-bg-circle" style="width:{350+index*20}px;height:{350+index*20}px;background:{accent1};top:-{80+index*10}px;left:-{80+index*10}px;"></div>
      <div class="bili-bg-circle" style="width:{260+index*15}px;height:{260+index*15}px;background:{accent2};bottom:-60px;right:-60px;"></div>
      <div class="bili-emoji-deco" style="top:{15+index*3}%;left:8%;font-size:{80+index*5}px;">{emoji1}</div>
      <div class="bili-emoji-deco" style="bottom:{15+index*3}%;right:10%;font-size:{60+index*5}px;">{emoji2}</div>
    </div>
    <div class="bili-stamp" style="border-color:{accent2};color:{accent2};">第{chapter:02d}节<br>{stamp_type}</div>
    <div class="bili-content">
      <div class="bili-badge" style="background:rgba({hex_to_rgb(accent1)},0.2);color:{accent1};border:1px solid rgba({hex_to_rgb(accent1)},0.4);">{emoji1} {badge}</div>
      <div class="bili-main-title">
        {display_title}
      </div>
      <div class="bili-sub-title">{subtitle}</div>
      <div class="bili-tag-row">
{tags_html}      </div>
    </div>
    <div class="bili-bottom-bar"><span>{emoji2} {quote}</span><span>Cover {index+1}</span></div>
  </div>'''
    
    return html


def hex_to_rgb(hex_color):
    """十六进制颜色转 RGB 字符串"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"{r},{g},{b}"


def generate_full_html(covers, style="bilibili"):
    """生成完整的 HTML 文件"""
    
    covers_html = "\n\n".join(
        generate_single_cover(cover, i) for i, cover in enumerate(covers)
    )
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>视频封面集合</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;900&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #111318;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
    padding: 40px 20px;
    min-height: 100vh;
  }}

  .slide-card {{
    width: 94vw;
    max-width: 1200px;
    aspect-ratio: 16 / 9;
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 8px 40px rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  /* B站封面样式 */
  .slide-bili-cover {{
    background: var(--bg-color, #1a1a2e);
    color: #fff;
    text-align: center;
    overflow: hidden;
  }}

  .bili-bg-decoration {{
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
  }}

  .bili-bg-circle {{
    position: absolute;
    border-radius: 50%;
    opacity: 0.06;
  }}

  .bili-content {{
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

  .bili-badge {{
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

  .bili-main-title {{
    font-size: 82px;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: 2px;
    margin-bottom: 10px;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3);
  }}

  .bili-main-title .highlight {{
    display: inline-block;
    transform: rotate(-3deg);
  }}

  .bili-sub-title {{
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 1px;
  }}

  .bili-tag-row {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 14px;
  }}

  .bili-tag {{
    padding: 6px 18px;
    border-radius: 16px;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}

  .bili-emoji-deco {{
    position: absolute;
    opacity: 0.08;
    z-index: 1;
  }}

  .bili-stamp {{
    position: absolute;
    top: 30px;
    right: 30px;
    width: 80px;
    height: 80px;
    border: 3px solid;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 900;
    text-align: center;
    line-height: 1.2;
    transform: rotate(15deg);
    z-index: 3;
  }}

  .bili-bottom-bar {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 36px;
    background: rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    font-size: 13px;
    color: rgba(255,255,255,0.5);
    z-index: 4;
  }}
</style>
</head>
<body>

{covers_html}

</body>
</html>'''
    
    return html


def covers_from_chapters(chapters):
    """从提取的章节信息生成封面配置"""
    covers = []
    for i, ch in enumerate(chapters):
        scheme = COLOR_SCHEMES[i % len(COLOR_SCHEMES)]
        cover = {
            "title": ch.get("title", f"第{ch.get('number', i+1)}节"),
            "highlight_words": ch.get("highlight_words", []),
            "subtitle": ch.get("subtitle", ch.get("description", "")),
            "tags": ch.get("tags", []),
            "chapter": ch.get("number", i + 1),
            "badge": ch.get("badge", f"第{ch.get('number', i+1)}节"),
            "quote": ch.get("quote", ""),
            "bg_color": scheme["bg"],
            "accent1": scheme["accent1"],
            "accent2": scheme["accent2"],
        }
        covers.append(cover)
    return covers


def main():
    parser = argparse.ArgumentParser(
        description="B站/YouTube 视频封面生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从 PPT 提取章节生成封面
  python3 generate_covers.py --input ppt.html --output covers.html

  # 从文本描述生成单个封面
  python3 generate_covers.py --title "AI Shell 连接" --subtitle "运维效率10倍" --tags "AI,Shell"

  # 从 JSON 配置批量生成
  python3 generate_covers.py --config covers.json --output covers.html

  # 仅提取章节信息（不生成HTML）
  python3 generate_covers.py --input ppt.html --extract-only
        """
    )
    
    parser.add_argument("--input", "-i", help="PPT/HTML 输入文件路径")
    parser.add_argument("--output", "-o", default="video-covers.html", help="输出 HTML 文件路径")
    parser.add_argument("--config", "-c", help="JSON 配置文件路径（批量生成）")
    parser.add_argument("--style", "-s", default="bilibili", choices=["bilibili", "youtube", "minimal"], help="封面风格")
    parser.add_argument("--extract-only", action="store_true", help="仅提取章节信息，不生成HTML")
    
    # 单页生成参数
    parser.add_argument("--title", "-t", help="主标题")
    parser.add_argument("--subtitle", help="副标题")
    parser.add_argument("--tags", help="标签（逗号分隔）")
    parser.add_argument("--chapter", type=int, default=1, help="章节编号")
    parser.add_argument("--badge", help="Badge 文本")
    parser.add_argument("--quote", help="底部金句")
    parser.add_argument("--bg-color", help="背景色（十六进制）")
    parser.add_argument("--accent-color", help="主色调（十六进制）")
    parser.add_argument("--highlight", help="高亮词（逗号分隔）")
    
    args = parser.parse_args()
    
    # === 模式1：从 PPT 提取 ===
    if args.input:
        if not os.path.exists(args.input):
            print(f"错误：文件不存在 - {args.input}", file=sys.stderr)
            sys.exit(1)
        
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
        
        chapters = extract_chapters_from_html(content)
        
        if not chapters:
            print("警告：未提取到章节信息，尝试按页面分割", file=sys.stderr)
            # Fallback: 按slide分割
            slides = re.findall(r'class="[^"]*slide[^"]*"[^>]*>(.*?)(?=class="[^"]*slide[^"]*"|$)', content, re.DOTALL)
            for i, slide in enumerate(slides):
                title_match = re.search(r'<h[12][^>]*>(.*?)</h[12]>', slide, re.DOTALL)
                if title_match:
                    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                    if title:
                        chapters.append({"number": i + 1, "title": title})
        
        if args.extract_only:
            print(json.dumps(chapters, ensure_ascii=False, indent=2))
            return
        
        if not chapters:
            print("错误：无法从文件中提取章节信息", file=sys.stderr)
            sys.exit(1)
        
        covers = covers_from_chapters(chapters)
        html = generate_full_html(covers, args.style)
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ 成功生成 {len(covers)} 个封面 → {args.output}")
        return
    
    # === 模式2：从 JSON 配置生成 ===
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        covers = config.get("covers", [])
        style = config.get("style", args.style)
        
        if not covers:
            print("错误：配置文件中没有 covers 数组", file=sys.stderr)
            sys.exit(1)
        
        html = generate_full_html(covers, style)
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ 成功生成 {len(covers)} 个封面 → {args.output}")
        return
    
    # === 模式3：从命令行参数生成单页 ===
    if args.title:
        highlight_words = args.highlight.split(",") if args.highlight else []
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        
        cover = {
            "title": args.title,
            "highlight_words": highlight_words,
            "subtitle": args.subtitle or "",
            "tags": tags,
            "chapter": args.chapter,
            "badge": args.badge or f"第{args.chapter}节",
            "quote": args.quote or "",
            "bg_color": args.bg_color or COLOR_SCHEMES[(args.chapter - 1) % len(COLOR_SCHEMES)]["bg"],
            "accent1": args.accent_color or COLOR_SCHEMES[(args.chapter - 1) % len(COLOR_SCHEMES)]["accent1"],
            "accent2": COLOR_SCHEMES[(args.chapter - 1) % len(COLOR_SCHEMES)]["accent2"],
        }
        
        html = generate_full_html([cover], args.style)
        
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ 成功生成封面 → {args.output}")
        return
    
    # 没有提供任何参数
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
