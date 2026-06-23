#!/usr/bin/env python3
"""
主题预览器 - 生成10大风格对比预览页
用户可以一眼看到所有风格效果，选好了再生成
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_covers import (
    PLATFORMS, COLOR_SCHEMES, THEME_EMOJIS, THEME_KEYWORDS,
    detect_theme, get_scheme_by_theme, get_emojis,
    apply_highlights, hex_to_rgb, TWEMOJI_CDN
)

THEME_INFO = {
    "bold":    {"name": "大字醒目", "desc": "知识区/教程/干货", "icon": "📢", "best": "编程教程、知识科普、硬核干货"},
    "cyber":   {"name": "赛博朋克", "desc": "数码/科技/AI", "icon": "🌃", "best": "AI、编程、科技、服务器"},
    "anime":   {"name": "二次元动漫", "desc": "ACG/番剧/虚拟主播", "icon": "🌸", "best": "动漫、番剧、虚拟主播"},
    "funny":   {"name": "搞笑整活", "desc": "搞笑/整活/表情包", "icon": "😂", "best": "搞笑、沙雕、吐槽、鬼畜"},
    "luxury":  {"name": "黑金奢华", "desc": "评测/高端/开箱", "icon": "👑", "best": "数码评测、开箱、高端体验"},
    "fresh":   {"name": "清新治愈", "desc": "Vlog/生活/旅行", "icon": "🍃", "best": "Vlog、旅行、生活记录"},
    "gaming":  {"name": "游戏电竞", "desc": "游戏/电竞/直播", "icon": "🎮", "best": "游戏、电竞、通关攻略"},
    "food":    {"name": "美食暖调", "desc": "美食/探店/烹饪", "icon": "🍜", "best": "美食、探店、烹饪教程"},
    "cinema":  {"name": "影视悬疑", "desc": "影视/悬疑/解说", "icon": "🎬", "best": "电影解说、悬疑、剧情"},
    "cute":    {"name": "萌宠可爱", "desc": "宠物/萌系/卡通", "icon": "🐱", "best": "宠物、萌系、卡通、手帐"},
}

THEME_FONT_CSS = """
.theme-bold .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.05; text-shadow: none; }
.theme-bold .cv-main-title .hl-bold { display: inline; transform: none; }
.theme-bold .cv-badge { border-radius: 0; border: 2px solid currentColor; background: transparent; }
.theme-bold .cv-content { align-items: flex-start; text-align: left; }

.theme-cyber .cv-main-title { font-weight: 900; letter-spacing: 4px; line-height: 1.1; text-shadow: 0 0 15px rgba(0,255,255,0.3); }
.theme-cyber .cv-main-title .hl-cyber { display: inline-block; }
.theme-cyber .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,255,255,0.03) 3px, rgba(0,255,255,0.03) 4px);
  pointer-events: none;
}
.theme-cyber .cv-badge { border-radius: 0; clip-path: polygon(0 0, 100% 0, 95% 100%, 0 100%); }

.theme-anime .cv-main-title { font-weight: 800; letter-spacing: 3px; line-height: 1.15; }
.theme-anime .cv-main-title .hl-anime { display: inline-block; }
.theme-anime .cv-badge { border-radius: 25px; }
.theme-anime .cv-tag { border-radius: 25px; }

.theme-funny .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.2; }
.theme-funny .cv-main-title .hl-funny { display: inline-block; }
.theme-funny .cv-badge { border-radius: 0; transform: rotate(-3deg); }
.theme-funny .cv-tag { transform: rotate(2deg); }

.theme-luxury .cv-main-title { font-weight: 700; letter-spacing: 6px; line-height: 1.1; text-shadow: 0 2px 8px rgba(212,175,55,0.3); }
.theme-luxury .cv-main-title .hl-luxury { display: inline-block; }
.theme-luxury .cv-badge { border-radius: 0; border: 1px solid currentColor; background: transparent; letter-spacing: 3px; }
.theme-luxury .cv-content::before {
  content: ''; position: absolute; top: 20px; left: 20px; right: 20px; bottom: 20px;
  border: 1px solid rgba(212,175,55,0.2); pointer-events: none; z-index: 1;
}
.theme-luxury .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; }

.theme-fresh .cv-main-title { font-weight: 600; letter-spacing: 2px; line-height: 1.2; text-shadow: none; }
.theme-fresh .cv-main-title .hl-fresh { display: inline; }
.theme-fresh .cv-badge { border-radius: 20px; font-weight: 500; }
.theme-fresh .cv-tag { border-radius: 20px; font-weight: 500; }
.theme-fresh .cv-sub-title { font-weight: 400; }

.theme-gaming .cv-main-title { font-weight: 900; letter-spacing: 1px; line-height: 1.05; text-shadow: 2px 2px 0 #000, 0 0 15px rgba(255,255,255,0.2); }
.theme-gaming .cv-main-title .hl-gaming { display: inline-block; }
.theme-gaming .cv-badge { clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%); border: none; }
.theme-gaming .cv-content { align-items: flex-start; text-align: left; }
.theme-gaming .cv-bg-decoration::after {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, var(--accent1), var(--accent2), var(--accent1));
  z-index: 3;
}

.theme-food .cv-main-title { font-weight: 800; letter-spacing: 2px; line-height: 1.1; }
.theme-food .cv-main-title .hl-food { display: inline-block; }
.theme-food .cv-badge { border-radius: 50px; }
.theme-food .cv-bg-circle { filter: blur(20px); opacity: 0.12; }

.theme-cinema .cv-main-title { font-weight: 700; letter-spacing: 5px; line-height: 1.1; text-shadow: 0 0 20px rgba(0,0,0,0.8); }
.theme-cinema .cv-main-title .hl-cinema { display: inline-block; }
.theme-cinema .cv-content::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 40px;
  background: linear-gradient(180deg, rgba(0,0,0,0.6), transparent); z-index: 3; pointer-events: none;
}
.theme-cinema .cv-content::after {
  content: ''; position: absolute; bottom: 36px; left: 0; right: 0; height: 40px;
  background: linear-gradient(0deg, rgba(0,0,0,0.6), transparent); z-index: 3; pointer-events: none;
}
.theme-cinema .cv-badge { border-radius: 0; background: transparent; border-left: 3px solid currentColor; padding-left: 12px; }

.theme-cute .cv-main-title { font-weight: 800; letter-spacing: 1px; line-height: 1.15; text-shadow: 2px 2px 0 rgba(255,255,255,0.5); }
.theme-cute .cv-main-title .hl-cute { display: inline-block; }
.theme-cute .cv-badge { border-radius: 50px; }
.theme-cute .cv-tag { border-radius: 50px; }
.theme-cute .cv-bg-circle { filter: blur(15px); opacity: 0.15; }

.theme-tech .cv-main-title { font-weight: 900; letter-spacing: 2px; line-height: 1.08; text-shadow: 0 4px 20px rgba(0,0,0,.4); }
.theme-hot .cv-main-title { font-weight: 900; letter-spacing: 2px; line-height: 1.08; }
.theme-cool .cv-main-title { font-weight: 900; letter-spacing: 2px; line-height: 1.08; }

.theme-cute .cv-main-title { font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; }
.theme-fresh .cv-main-title { font-family: 'Ma Shan Zheng', 'Noto Sans SC', sans-serif; font-weight: 400; }
.theme-anime .cv-main-title { font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; }
"""


def make_mini_cover(theme, title, subtitle, tags, badge, quote, highlights):
    """生成单个主题的小预览卡片"""
    sk = get_scheme_by_theme(theme, 0)
    sc = COLOR_SCHEMES[sk]
    bg = sc["bg"]
    a1 = sc["accent1"]
    a2 = sc["accent2"]
    text_color = sc.get("text_color", "#ffffff")
    is_gradient = sc.get("is_gradient", False)

    e1, e2 = get_emojis(theme, 0)
    ec1, ec2 = e1[1], e2[1]
    eu1, eu2 = f"{TWEMOJI_CDN}/{e1[0]}.svg", f"{TWEMOJI_CDN}/{e2[0]}.svg"

    dt = apply_highlights(title, highlights, theme, a1, a2)

    th = ""
    for i, t in enumerate(tags):
        tc = [a1,a2,a1,a2][i%4]
        op = 0.25 if i%2==0 else 0.20
        th += f'<span class="cv-tag" style="background:rgba({hex_to_rgb(tc)},{op});color:{tc};">{t}</span>'

    info = THEME_INFO.get(theme, {"name":theme,"desc":"","icon":"📄","best":""})

    bg_style = f"background:{bg};" if not is_gradient else f"background:{bg};"

    return f'''<div class="theme-card" data-theme="{theme}" onclick="selectTheme('{theme}')">
  <div class="theme-preview theme-{theme}" style="--bg-color:{bg};--accent1:{a1};--accent2:{a2};--text-color:{text_color};{bg_style}">
    <div class="cv-bg-decoration">
      <div class="cv-bg-circle" style="width:180px;height:180px;background:{a1};top:-40px;left:-40px;"></div>
      <div class="cv-bg-circle" style="width:140px;height:140px;background:{a2};bottom:-30px;right:-30px;"></div>
      <img class="cv-emoji-deco" src="{eu1}" alt="{ec1}" style="top:8%;left:4%;width:36px;height:36px;" onerror="this.style.display='none'">
      <img class="cv-emoji-deco" src="{eu2}" alt="{ec2}" style="bottom:8%;right:4%;width:28px;height:28px;" onerror="this.style.display='none'">
    </div>
    <div class="cv-content">
      <div class="cv-badge" style="background:rgba({hex_to_rgb(a1)},0.2);color:{a1};border:1px solid rgba({hex_to_rgb(a1)},0.4);">{ec1} {badge}</div>
      <div class="cv-main-title" style="font-size:22px;color:{text_color};">{dt}</div>
      <div class="cv-sub-title" style="font-size:11px;color:{text_color};">{subtitle}</div>
      <div class="cv-tag-row">{th}</div>
    </div>
  </div>
  <div class="theme-info">
    <div class="theme-name">{info["icon"]} {info["name"]} <code>--theme {theme}</code></div>
    <div class="theme-desc">{info["desc"]}</div>
    <div class="theme-best">适合：{info["best"]}</div>
  </div>
</div>'''


def generate_theme_picker(title="给爷来个Key！自建中转站让AI自己找Key吃",
                          subtitle="AI IDE × Skills = 全自动密钥供给",
                          tags=None, badge="硬核教程", quote="",
                          highlights=None):
    tags = tags or ["自建中转站","AI IDE","Skills"]
    highlights = highlights or ["给爷来个Key","自己找Key吃"]

    cards = []
    for theme in ["bold","cyber","anime","funny","luxury","fresh","gaming","food","cinema","cute"]:
        cards.append(make_mini_cover(theme, title, subtitle, tags, badge, quote, highlights))

    cards_html = "\n".join(cards)

    # 检测自动匹配
    auto_theme = detect_theme(title, tags)
    auto_info = THEME_INFO.get(auto_theme, {"name":auto_theme,"icon":"🤖"})

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>选择封面风格 - 视频封面生成器</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800;900&family=ZCOOL+KuaiLe&family=Ma+Shan+Zheng&display=swap');
* {{ margin:0; padding:0; box-sizing:border-box; }}

body {{
  font-family:'Noto Sans SC',-apple-system,sans-serif;
  background:#0d1117; color:rgba(255,255,255,0.8);
  min-height:100vh; padding:24px;
}}

.header {{
  text-align:center; margin-bottom:28px; padding:20px;
  background:linear-gradient(135deg,rgba(99,102,241,0.1),rgba(236,72,153,0.1));
  border-radius:16px; border:1px solid rgba(255,255,255,0.08);
}}
.header h1 {{ font-size:28px; font-weight:800; margin-bottom:8px; }}
.header p {{ color:rgba(255,255,255,0.5); font-size:14px; }}
.header .auto-match {{
  margin-top:12px; padding:8px 20px; display:inline-block;
  background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.3);
  border-radius:8px; font-size:14px; color:#4ade80;
}}

.grid {{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
  gap:20px; max-width:1400px; margin:0 auto;
}}

.theme-card {{
  background:#161b22; border:1px solid rgba(255,255,255,0.08);
  border-radius:12px; overflow:hidden; cursor:pointer;
  transition:all 0.25s ease;
}}
.theme-card:hover {{
  border-color:rgba(245,158,11,0.4);
  transform:translateY(-4px);
  box-shadow:0 12px 32px rgba(0,0,0,0.4);
}}
.theme-card.selected {{
  border-color:#f59e0b;
  box-shadow:0 0 0 2px rgba(245,158,11,0.3),0 12px 32px rgba(245,158,11,0.15);
}}

.theme-preview {{
  width:100%; aspect-ratio:16/9;
  position:relative; overflow:hidden;
  display:flex; align-items:center; justify-content:center;
  color:#fff; text-align:center;
}}

.cv-bg-decoration {{ position:absolute; inset:0; pointer-events:none; z-index:0; }}
.cv-bg-circle {{ position:absolute; border-radius:50%; opacity:.06; }}
.cv-content {{
  position:relative; z-index:2; display:flex; flex-direction:column;
  align-items:center; justify-content:center; width:100%; height:100%; padding:16px;
}}
.cv-badge {{
  display:inline-flex; align-items:center; gap:4px;
  padding:3px 10px; border-radius:12px;
  font-size:10px; font-weight:700; letter-spacing:0.5px; margin-bottom:8px;
}}
.cv-main-title {{
  font-weight:900; line-height:1.1; letter-spacing:1px; margin-bottom:4px;
  max-width:90%; color:var(--text-color,#fff);
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;
}}
.cv-sub-title {{ font-weight:600; font-size:11px; opacity:0.7; margin-bottom:6px; max-width:85%; color:var(--text-color,#fff); }}
.cv-tag-row {{ display:flex; gap:4px; flex-wrap:wrap; justify-content:center; }}
.cv-tag {{ padding:2px 8px; border-radius:10px; font-size:9px; font-weight:700; }}
.cv-emoji-deco {{ position:absolute; opacity:.10; z-index:1; object-fit:contain; }}
.cv-bottom-bar {{ display:none; }}

/* 浅色背景 */
.theme-preview[style*="#fff"] .cv-emoji-deco,
.theme-preview[style*="#fbbf24"] .cv-emoji-deco,
.theme-preview[style*="#e0f2fe"] .cv-emoji-deco,
.theme-preview[style*="#f0fdf4"] .cv-emoji-deco,
.theme-preview[style*="#fefce8"] .cv-emoji-deco,
.theme-preview[style*="#fff7ed"] .cv-emoji-deco,
.theme-preview[style*="#fdf2f8"] .cv-emoji-deco,
.theme-preview[style*="#ecfeff"] .cv-emoji-deco,
.theme-preview[style*="#fff0f5"] .cv-emoji-deco {{ opacity:0.15; }}

{THEME_FONT_CSS}

.theme-cute .cv-main-title {{ font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif; }}
.theme-fresh .cv-main-title {{ font-family:'Ma Shan Zheng','Noto Sans SC',sans-serif; font-weight:400; }}
.theme-anime .cv-main-title {{ font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif; }}

.theme-info {{
  padding:14px 16px;
}}
.theme-name {{
  font-size:16px; font-weight:700; margin-bottom:4px;
  display:flex; align-items:center; justify-content:space-between;
}}
.theme-name code {{
  font-family:'SF Mono',Monaco,monospace; font-size:11px;
  background:rgba(255,255,255,0.08); padding:2px 8px; border-radius:4px;
  color:rgba(255,255,255,0.6); font-weight:500;
}}
.theme-card.selected .theme-name code {{
  background:rgba(245,158,11,0.15); color:#f59e0b;
}}
.theme-desc {{ font-size:13px; color:rgba(255,255,255,0.5); margin-bottom:4px; }}
.theme-best {{ font-size:12px; color:rgba(255,255,255,0.35); }}

.footer {{
  text-align:center; margin-top:32px; padding:20px;
  color:rgba(255,255,255,0.3); font-size:13px;
}}
.footer code {{
  font-family:'SF Mono',Monaco,monospace; font-size:12px;
  background:rgba(255,255,255,0.06); padding:4px 12px; border-radius:6px;
  color:rgba(255,255,255,0.6);
}}
</style>
</head>
<body>

<div class="header">
  <h1>🎨 选择封面风格</h1>
  <p>10大B站爆款风格，点击选择你喜欢的主题</p>
  <div class="auto-match">🤖 自动匹配：<strong>{auto_info["icon"]} {auto_info["name"]}</strong>（基于标题关键词检测）</div>
</div>

<div class="grid">
{cards_html}
</div>

<div class="footer">
  选好后用对应命令生成：<br>
  <code>python3 generate_covers.py --title "你的标题" --theme &lt;主题名&gt; --platform all</code>
</div>

<script>
function selectTheme(theme){{
  document.querySelectorAll('.theme-card').forEach(c=>c.classList.remove('selected'));
  const card = document.querySelector('.theme-card[data-theme="'+theme+'"]');
  if(card) card.classList.add('selected');
  console.log('已选择主题:', theme);
}}
// 默认选中自动匹配
selectTheme('{auto_theme}');
</script>

</body>
</html>'''


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="主题选择器 - 预览所有风格")
    p.add_argument("--title","-t",default="给爷来个Key！自建中转站让AI自己找Key吃")
    p.add_argument("--subtitle",default="AI IDE × Skills = 全自动密钥供给")
    p.add_argument("--tags",default="自建中转站,AI IDE,Skills")
    p.add_argument("--badge",default="硬核教程")
    p.add_argument("--highlight",default="给爷来个Key,自己找Key吃")
    p.add_argument("--output","-o",default="theme-picker.html")
    a = p.parse_args()

    html = generate_theme_picker(
        title=a.title, subtitle=a.subtitle,
        tags=[t.strip() for t in a.tags.split(",")],
        badge=a.badge,
        highlights=[h.strip() for h in a.highlight.split(",")],
    )
    with open(a.output,"w",encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 主题选择器已生成 → {a.output}")
    print(f"   打开后可预览10种风格效果，点击选择喜欢的主题")
