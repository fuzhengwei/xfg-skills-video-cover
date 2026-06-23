#!/usr/bin/env python3
"""
视频封面生成器 v2.2 - 主脚本
PPT风格底部缩略图导航 · 多平台/24套配色/Twemoji素材
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from extract_chapters import extract_chapters_from_html
except ImportError:
    def extract_chapters_from_html(content):
        return []

# ========== 平台尺寸 ==========
PLATFORMS = {
    "bilibili": {"name": "B站", "icon": "📺", "ratio": "16 / 9", "width": 1200, "height": 675,
                 "title_size": 82, "subtitle_size": 28, "tag_size": 15, "badge_size": 14},
    "xiaohongshu": {"name": "小红书", "icon": "📕", "ratio": "3 / 4", "width": 900, "height": 1200,
                     "title_size": 64, "subtitle_size": 24, "tag_size": 14, "badge_size": 13},
    "wechat": {"name": "微信视频号", "icon": "📱", "ratio": "9 / 16", "width": 1080, "height": 1920,
               "title_size": 56, "subtitle_size": 22, "tag_size": 13, "badge_size": 12},
    "mobile": {"name": "手机竖版", "icon": "📲", "ratio": "9 / 19.5", "width": 1080, "height": 2106,
             "title_size": 52, "subtitle_size": 20, "tag_size": 12, "badge_size": 11},
}

# ========== 24套爆款配色 ==========
COLOR_SCHEMES = {
    "tech_1": {"bg": "#0f0e17", "accent1": "#ff8906", "accent2": "#f25f4c", "name": "暗夜火焰", "theme": "tech"},
    "tech_2": {"bg": "#1a1a2e", "accent1": "#e94560", "accent2": "#0f3460", "name": "赛博朋克", "theme": "tech"},
    "tech_3": {"bg": "#0d1117", "accent1": "#58a6ff", "accent2": "#7ee787", "name": "极客绿", "theme": "tech"},
    "tech_4": {"bg": "#1a1a2e", "accent1": "#e74c3c", "accent2": "#f39c12", "name": "科技红橙", "theme": "tech"},
    "tech_5": {"bg": "#0a0e27", "accent1": "#00d9ff", "accent2": "#9d4edd", "name": "电光紫蓝", "theme": "tech"},
    "hot_1": {"bg": "#2d0a0a", "accent1": "#fbbf24", "accent2": "#f87171", "name": "火焰金红", "theme": "hot"},
    "hot_2": {"bg": "#3d0a0a", "accent1": "#ff6b6b", "accent2": "#ffd93d", "name": "热情黄红", "theme": "hot"},
    "hot_3": {"bg": "#2a0a0a", "accent1": "#fb923c", "accent2": "#f97316", "name": "压测火焰", "theme": "hot"},
    "hot_4": {"bg": "#1a0505", "accent1": "#ef4444", "accent2": "#f59e0b", "name": "爆裂红金", "theme": "hot"},
    "cool_1": {"bg": "#0d1b2a", "accent1": "#00b4d8", "accent2": "#90e0ef", "name": "深海蓝青", "theme": "cool"},
    "cool_2": {"bg": "#0a2e0a", "accent1": "#4ade80", "accent2": "#86efac", "name": "森林绿", "theme": "cool"},
    "cool_3": {"bg": "#0f1c2e", "accent1": "#06b6d4", "accent2": "#67e8f9", "name": "冰蓝青", "theme": "cool"},
    "cool_4": {"bg": "#0d2818", "accent1": "#10b981", "accent2": "#6ee7b7", "name": "翡翠绿", "theme": "cool"},
    "warm_1": {"bg": "#2e0a1a", "accent1": "#f9a8d4", "accent2": "#ec4899", "name": "玫瑰粉", "theme": "warm"},
    "warm_2": {"bg": "#1a0a2e", "accent1": "#f72585", "accent2": "#4cc9f0", "name": "品红蓝紫", "theme": "warm"},
    "warm_3": {"bg": "#2e1a0a", "accent1": "#fbbf24", "accent2": "#fb7185", "name": "暖阳金粉", "theme": "warm"},
    "warm_4": {"bg": "#1e1b4b", "accent1": "#fbbf24", "accent2": "#818cf8", "name": "靛蓝紫金", "theme": "warm"},
    "dark_1": {"bg": "#0a0a0a", "accent1": "#fbbf24", "accent2": "#ffffff", "name": "黑金奢华", "theme": "dark"},
    "dark_2": {"bg": "#111111", "accent1": "#ef4444", "accent2": "#6b7280", "name": "暗血红灰", "theme": "dark"},
    "dark_3": {"bg": "#0a0a0a", "accent1": "#22d3ee", "accent2": "#a3e635", "name": "黑客霓虹", "theme": "dark"},
    "gradient_1": {"bg": "linear-gradient(135deg,#667eea 0%,#764ba2 100%)", "accent1": "#ffd700", "accent2": "#fff", "name": "紫金渐变", "theme": "gradient", "is_gradient": True},
    "gradient_2": {"bg": "linear-gradient(135deg,#f093fb 0%,#f5576c 100%)", "accent1": "#ffd700", "accent2": "#fff", "name": "粉红渐变", "theme": "gradient", "is_gradient": True},
    "gradient_3": {"bg": "linear-gradient(135deg,#4facfe 0%,#00f2fe 100%)", "accent1": "#fff", "accent2": "#ffe066", "name": "天蓝渐变", "theme": "gradient", "is_gradient": True},
    "gradient_4": {"bg": "linear-gradient(135deg,#fa709a 0%,#fee140 100%)", "accent1": "#fff", "accent2": "#7c2d12", "name": "日落渐变", "theme": "gradient", "is_gradient": True},
}

THEME_KEYWORDS = {
    "tech": ["AI","Shell","API","代码","编程","程序","服务器","云","IDE","CLI","Key","密钥","模型","Ollama","qwen","GPT"],
    "hot": ["教程","入门","实战","安装","部署","上线","新手","快速"],
    "cool": ["Docker","容器","MySQL","Redis","数据库","缓存","Portainer","Nginx"],
    "warm": ["对话","客服","设计","生活","沟通","SSE","流式"],
    "dark": ["安全","黑客","高级","硬核","渗透","密码"],
    "gradient": ["时尚","创意","爆款","热门","推荐"],
}

THEME_EMOJIS = {
    "tech": [("1f680","🚀"),("26a1","⚡"),("1f4bb","💻"),("1f310","🌐"),("1f527","🔧"),("1f4e1","📡")],
    "hot": [("1f525","🔥"),("2b50","⭐"),("1f4a5","💥"),("1f3af","🎯"),("1f389","🎉")],
    "cool": [("1f433","🐳"),("1f4e6","📦"),("1f5c3","🗄️"),("1f510","🔐"),("1f4be","💾")],
    "warm": [("1f49b","💛"),("1f4ac","💬"),("1f917","🤗"),("1f4f1","📱"),("2728","✨")],
    "dark": [("1f576","🕶️"),("1f512","🔒"),("1f480","💀"),("1f451","👑"),("1f9e0","🧠")],
    "gradient": [("2728","✨"),("1f308","🌈"),("1f4ab","💫"),("1f31f","🌟"),("1f48e","💎")],
}
GENERAL_EMOJIS = [("1f680","🚀"),("26a1","⚡"),("1f4bb","💻"),("1f310","🌐"),
                  ("1f525","🔥"),("2b50","⭐"),("2728","✨"),("1f4a1","💡"),
                  ("1f3af","🎯"),("1f389","🎉"),("1f4aa","💪")]

TWEMOJI_CDN = "https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/svg"


def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) != 6: return "255,255,255"
    return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"


def detect_theme(title, tags=None):
    text = ((title or "") + " " + (tags and " ".join(tags) or "")).lower()
    scores = {t: sum(1 for k in kw if k.lower() in text) for t, kw in THEME_KEYWORDS.items()}
    return max(scores, key=scores.get) if any(scores.values()) else "tech"


def get_scheme_by_theme(theme, idx=0):
    ss = [k for k,v in COLOR_SCHEMES.items() if v["theme"]==theme]
    return ss[idx % len(ss)] if ss else list(COLOR_SCHEMES.keys())[idx % len(COLOR_SCHEMES)]


def get_emojis(theme, idx=0):
    em = THEME_EMOJIS.get(theme, GENERAL_EMOJIS)
    s = idx * 2
    e1 = em[s % len(em)]
    e2 = em[(s+1) % len(em)]
    if len(em) < 2:
        e1 = GENERAL_EMOJIS[idx % len(GENERAL_EMOJIS)]
        e2 = GENERAL_EMOJIS[(idx+5) % len(GENERAL_EMOJIS)]
    return e1, e2


def generate_single_cover(cfg, pf_key="bilibili", index=0):
    pf = PLATFORMS[pf_key]
    title = cfg.get("title", "")
    highlights = cfg.get("highlight_words", [])
    subtitle = cfg.get("subtitle", "")
    tags = cfg.get("tags", [])
    badge = cfg.get("badge", "")
    quote = cfg.get("quote", "")
    theme = cfg.get("theme", "auto")
    if theme == "auto":
        theme = detect_theme(title, tags)

    sk = cfg.get("scheme") or get_scheme_by_theme(theme, index)
    sc = COLOR_SCHEMES[sk]
    bg = cfg.get("bg_color", sc["bg"])
    a1 = cfg.get("accent1", sc["accent1"])
    a2 = cfg.get("accent2", sc["accent2"])

    e1, e2 = get_emojis(theme, index)
    ec1, ec2 = e1[1], e2[1]
    eu1, eu2 = f"{TWEMOJI_CDN}/{e1[0]}.svg", f"{TWEMOJI_CDN}/{e2[0]}.svg"

    dt = title
    for i, w in enumerate(highlights):
        c = a1 if i%2==0 else a2
        dt = dt.replace(w, f'<span class="highlight" style="color:{c};">{w}</span>')

    th = ""
    for i, t in enumerate(tags):
        tc = [a1,a2,a1,a2][i%4]
        op = 0.25 if i%2==0 else 0.20
        th += f'        <span class="cv-tag" style="background:rgba({hex_to_rgb(tc)},{op});color:{tc};">{t}</span>\n'

    ts, ss = pf["title_size"], pf["subtitle_size"]
    es1, es2 = int(ts*1.1), int(ts*0.8)

    return f'''<div class="cover-card cover-{pf_key}" data-platform="{pf['name']}" data-index="{index+1}" style="--bg-color:{bg};--accent1:{a1};--accent2:{a2};">
  <div class="cv-bg-decoration">
    <div class="cv-bg-circle" style="width:{350+index*20}px;height:{350+index*20}px;background:{a1};top:-{80+index*10}px;left:-{80+index*10}px;"></div>
    <div class="cv-bg-circle" style="width:{260+index*15}px;height:{260+index*15}px;background:{a2};bottom:-60px;right:-60px;"></div>
    <img class="cv-emoji-deco cv-emoji-1" src="{eu1}" alt="{ec1}" style="top:{15+index*3}%;left:6%;width:{es1}px;height:{es1}px;" onerror="this.style.display='none'">
    <img class="cv-emoji-deco cv-emoji-2" src="{eu2}" alt="{ec2}" style="bottom:{12+index*3}%;right:8%;width:{es2}px;height:{es2}px;" onerror="this.style.display='none'">
  </div>
  <div class="cv-content">
    <div class="cv-badge" style="background:rgba({hex_to_rgb(a1)},0.2);color:{a1};border:1px solid rgba({hex_to_rgb(a1)},0.4);">{ec1} {badge}</div>
    <div class="cv-main-title" style="font-size:{ts}px;">{dt}</div>
    <div class="cv-sub-title" style="font-size:{ss}px;">{subtitle}</div>
    <div class="cv-tag-row">
{th}    </div>
  </div>
  <div class="cv-bottom-bar"><span>{ec2} {quote}</span><span>{pf['name']} · {index+1}</span></div>
</div>'''


def generate_full_html(covers, platform="bilibili", theme="auto"):
    """生成 PPT 风格：顶部标题栏 + 中间大图 + 底部缩略图导航条"""
    pks = ["bilibili","xiaohongshu","wechat","mobile"] if platform == "all" else [platform]

    slides = []
    thumbs = []
    total = len(pks) * len(covers)
    si = 0

    for pk in pks:
        pf = PLATFORMS[pk]
        pn = pf["name"]
        for ci, c in enumerate(covers):
            si += 1
            first = si == 1
            # 缩略图标签 = 平台名
            t = c.get("title", f"{pn}{ci+1}")
            label = pf.get("icon", "📄") + " " + pf["name"]
            # 获取配色用于缩略图边框色
            th = c.get("theme", "auto")
            if th == "auto": th = detect_theme(t, c.get("tags"))
            sk = get_scheme_by_theme(th, ci)
            sc = COLOR_SCHEMES[sk]

            act = ' active' if first else ''
            slides.append(f'      <div class="slide{act}" data-slide="{si}">\n{generate_single_cover(c, pk, ci)}\n      </div>')
            thumbs.append(f'''        <button class="thumb-btn{act}" onclick="goSlide({si})" title="{t}">
          <span class="thumb-label">{label}</span>
          <span class="thumb-num">{si}</span>
        </button>''')

    slide_html = "\n".join(slides)
    thumb_html = "\n".join(thumbs)

    pf_css = "\n".join(f"  .cover-{pk} {{ aspect-ratio: {v['ratio']}; max-width: {v['width']}px; }}"
                       for pk, v in PLATFORMS.items())

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>视频封面预览</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}

body{{
  font-family:'Noto Sans SC',-apple-system,BlinkMacSystemFont,sans-serif;
  background:#0d1117;
  display:flex;flex-direction:column;
  height:100vh;width:100vw;overflow:hidden;
}}

/* ===== 顶部标题栏 ===== */
.topbar{{
  flex-shrink:0;
  display:flex;align-items:center;justify-content:space-between;
  padding:10px 28px;
  background:#161b22;border-bottom:1px solid rgba(255,255,255,0.08);
  color:rgba(255,255,255,0.65);
  font-size:13px;z-index:20;
}}
.topbar-title{{font-weight:600;color:rgba(255,255,255,0.85);font-size:14px;}}
.topbar-page{{font-family:'SF Mono',Monaco,monospace;font-size:12px;color:rgba(255,255,255,0.35);}}

/* ===== 中间幻灯片区域 ===== */
.stage{{
  flex:1;display:flex;align-items:center;justify-content:center;
  padding:20px 40px;overflow:hidden;position:relative;
}}
.slide{{display:none;width:100%;height:100%;align-items:center;justify-content:center;animation:slideIn .3s ease;}}
.slide.active{{display:flex;}}
@keyframes slideIn{{from{{opacity:0;transform:scale(.96)}}to{{opacity:1;transform:scale(1)}}}}

/* ===== 封面卡片 ===== */
.cover-card{{
  width:94%;max-height:92%;
  border-radius:8px;overflow:hidden;position:relative;
  box-shadow:0 12px 48px rgba(0,0,0,.5);
  display:flex;align-items:center;justify-content:center;
  color:#fff;text-align:center;background:var(--bg-color,#1a1a2e);
}}
{pf_css}

.cv-bg-decoration{{position:absolute;inset:0;pointer-events:none;z-index:0;}}
.cv-bg-circle{{position:absolute;border-radius:50%;opacity:.06;}}
.cv-content{{
  position:relative;z-index:2;display:flex;flex-direction:column;
  align-items:center;justify-content:center;width:100%;height:100%;padding:40px;
}}
.cv-badge{{
  display:inline-flex;align-items:center;gap:6px;
  padding:6px 18px;border-radius:20px;
  font-size:14px;font-weight:700;letter-spacing:1px;margin-bottom:16px;
}}
.cv-main-title{{
  font-weight:900;line-height:1.08;letter-spacing:2px;margin-bottom:10px;
  text-shadow:0 4px 20px rgba(0,0,0,.4);max-width:90%;
}}
.cv-main-title .highlight{{display:inline-block;transform:rotate(-3deg);}}
.cv-sub-title{{font-weight:600;margin-bottom:16px;letter-spacing:1px;max-width:85%;}}
.cv-tag-row{{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:14px;}}
.cv-tag{{padding:6px 18px;border-radius:16px;font-size:15px;font-weight:700;letter-spacing:.5px;}}
.cv-emoji-deco{{position:absolute;opacity:.10;z-index:1;object-fit:contain;}}
.cv-bottom-bar{{
  position:absolute;bottom:0;left:0;right:0;height:36px;
  background:rgba(0,0,0,.35);backdrop-filter:blur(4px);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 28px;font-size:13px;color:rgba(255,255,255,.5);z-index:4;
}}
.cover-xiaohongshu .cv-content{{padding:36px 32px;}}
.cover-xiaohongshu .cv-main-title{{line-height:1.12;}}
.cover-wechat .cv-content{{padding:32px 28px;}}
.cover-wechat .cv-main-title{{line-height:1.15;}}
.cover-wechat .cv-badge{{margin-bottom:24px;}}
.cover-mobile .cv-content{{padding:28px 24px;}}
.cover-mobile .cv-main-title{{line-height:1.18;letter-spacing:1px;}}
.cover-mobile .cv-badge{{margin-bottom:28px;padding:5px 14px;font-size:12px;}}
.cover-mobile .cv-sub-title{{font-size:19px;margin-bottom:12px;}}
.cover-mobile .cv-tag{{padding:5px 14px;font-size:13px;}}
.cover-card[style*="linear-gradient"]{{background:var(--bg-color);}}

/* ===== 底部缩略图导航条（PPT风格）===== */
.navbar{{
  flex-shrink:0;
  display:flex;align-items:center;gap:6px;
  padding:10px 20px 14px;
  background:#161b22;border-top:1px solid rgba(255,255,255,0.08);
  overflow-x:auto;overflow-y:hidden;
  -webkit-overflow-scrolling:touch;
  scrollbar-width:none;
}}
.navbar::-webkit-scrollbar{{display:none;}}

.thumb-btn{{
  flex-shrink:0;
  display:flex;align-items:center;gap:6px;
  padding:7px 14px;border-radius:6px;
  border:1.5px solid rgba(255,255,255,.12);
  background:rgba(255,255,255,.04);
  color:rgba(255,255,255,.55);
  font-family:inherit;font-size:12px;font-weight:600;
  cursor:pointer;transition:all .2s ease;white-space:nowrap;
  min-width:0;
}}
.thumb-btn:hover{{
  background:rgba(255,255,255,.08);
  color:rgba(255,255,255,.75);
  border-color:rgba(255,255,255,.2);
}}
.thumb-btn.active{{
  background:rgba(245,158,11,.15);
  color:#f59e0b;
  border-color:rgba(245,158,11,.5);
  box-shadow:0 0 12px rgba(245,158,11,.15);
}}
.thumb-label{{font-weight:700;white-space:nowrap;}}
.thumb-num{{
  font-size:10px;font-weight:600;
  min-width:16px;height:16px;line-height:16px;
  border-radius:4px;text-align:center;
  background:currentColor;color:transparent;
  -webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3'/%3E%3C/svg%3E") center/contain no-repeat;
  mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3'/%3E%3C/svg%3E") center/contain no-repeat;
}}
.thumb-btn.active .thumb-num{{
  background:#f59e0b;color:#fff;
  -webkit-mask:none;mask:none;
}}
</style>
</head>
<body>

<!-- 顶部标题栏 -->
<div class="topbar">
  <span class="topbar-title">视频封面预览</span>
  <span class="topbar-page"><span id="curPage">1</span> / {total}</span>
</div>

<!-- 幻灯片区域 -->
<div class="stage">
{slide_html}
</div>

<!-- 底部缩略图导航条 -->
<nav class="navbar">
{thumb_html}
</nav>

<script>
var cur = 1, total = {total};
function goSlide(n){{
  if(n<1||n>total)return;
  cur=n;
  document.querySelectorAll('.slide').forEach(s=>s.classList.remove('active'));
  document.querySelector('.slide[data-slide="'+n+'"]').classList.add('active');
  document.querySelectorAll('.thumb-btn').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.thumb-btn')[n-1].classList.add('active');
  document.getElementById('curPage').textContent=n;
}}
// 键盘左右切换
document.addEventListener('keydown',function(e){{
  if(e.key==='ArrowLeft'||e.key==='ArrowUp') goSlide(cur-1);
  if(e.key==='ArrowRight'||e.key==='ArrowDown') goSlide(cur+1);
}});
</script>

</body>
</html>'''


def covers_from_chapters(chapters, theme="auto"):
    return [{
        "title": ch.get("title", f"第{ch.get('number', i+1)}节"),
        "highlight_words": ch.get("highlight_words", []),
        "subtitle": ch.get("subtitle", ch.get("description", "")),
        "tags": ch.get("tags", []),
        "badge": ch.get("badge", f"第{ch.get('number', i+1)}节"),
        "quote": ch.get("quote", ""),
        "theme": theme,
    } for i, ch in enumerate(chapters)]


def main():
    p = argparse.ArgumentParser(
        description="视频封面生成器 v2.2 - PPT风格底部缩略图导航",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\n示例:\n  python3 generate_covers.py --title 'Docker一装，运维轻松10倍'\n  python3 generate_covers.py --title '给爷来个Key' --platform all\n  python3 generate_covers.py --input ppt.html --output covers.html --platform all\n  python3 generate_covers.py --config covers.json")
    p.add_argument("--input","-i")
    p.add_argument("--output","-o",default="video-covers.html")
    p.add_argument("--config","-c")
    p.add_argument("--platform","-p",default="bilibili",choices=["bilibili","xiaohongshu","wechat","mobile","all"])
    p.add_argument("--theme",default="auto",choices=["auto","tech","hot","cool","warm","dark","gradient"])
    p.add_argument("--extract-only",action="store_true")
    p.add_argument("--title","-t")
    p.add_argument("--subtitle")
    p.add_argument("--tags")
    p.add_argument("--badge")
    p.add_argument("--quote")
    p.add_argument("--highlight")
    p.add_argument("--bg-color")
    p.add_argument("--accent-color")
    a = p.parse_args()

    if a.input:
        if not os.path.exists(a.input): print(f"错误：文件不存在 - {a.input}",file=sys.stderr); sys.exit(1)
        with open(a.input,"r",encoding="utf-8") as f: content=f.read()
        chapters = extract_chapters_from_html(content)
        if a.extract_only: print(json.dumps(chapters,ensure_ascii=False,indent=2)); return
        if not chapters: print("警告：未提取到章节信息",file=sys.stderr); chapters=[{"number":1,"title":"视频封面"}]
        covers = covers_from_chapters(chapters, a.theme)
        html = generate_full_html(covers, a.platform, a.theme)
        with open(a.output,"w",encoding="utf-8") as f: f.write(html)
        pc = 4 if a.platform=="all" else 1
        print(f"✅ 成功生成 {len(covers)} 个封面 × {pc} 平台 → {a.output}")
        return

    if a.config:
        with open(a.config,"r",encoding="utf-8") as f: cfg=json.load(f)
        covers = cfg.get("covers",[])
        pl = cfg.get("platform", a.platform)
        th = cfg.get("theme", a.theme)
        if not covers: print("错误：配置文件中没有 covers",file=sys.stderr); sys.exit(1)
        html = generate_full_html(covers, pl, th)
        with open(a.output,"w",encoding="utf-8") as f: f.write(html)
        pc = 4 if pl=="all" else 1
        print(f"✅ 成功生成 {len(covers)} 个封面 × {pc} 平台 → {a.output}")
        return

    if a.title:
        hw = [w.strip() for w in a.highlight.split(",")] if a.highlight else []
        tg = [t.strip() for t in a.tags.split(",")] if a.tags else []
        cover = {"title":a.title,"highlight_words":hw,"subtitle":a.subtitle or "",
                 "tags":tg,"badge":a.badge or "","quote":a.quote or "","theme":a.theme}
        if a.bg_color: cover["bg_color"]=a.bg_color
        if a.accent_color: cover["accent1"]=a.accent_color
        html = generate_full_html([cover], a.platform, a.theme)
        with open(a.output,"w",encoding="utf-8") as f: f.write(html)
        pc = 4 if a.platform=="all" else 1
        print(f"✅ 成功生成 1 个封面 × {pc} 平台 → {a.output}")
        return

    p.print_help(); sys.exit(1)

if __name__ == "__main__":
    main()
