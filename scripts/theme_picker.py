#!/usr/bin/env python3
"""
主题选择器 v2.0 - 点击主题卡片直接跳转4平台详细预览
单文件输出，所有风格+所有平台全打包
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_covers import (
    PLATFORMS, COLOR_SCHEMES, THEME_EMOJIS, THEME_KEYWORDS,
    detect_theme, get_scheme_by_theme, get_emojis,
    apply_highlights, hex_to_rgb, TWEMOJI_CDN,
    THEME_FONT_CSS, generate_single_cover,
    get_decoration_assets,
)

THEME_INFO = {
    # ===== 科技知识类 =====
    "bold":    {"name": "大字醒目", "desc": "知识区/教程/干货", "icon": "📢", "best": "编程教程、知识科普、硬核干货", "category": "科技知识"},
    "cyber":   {"name": "赛博朋克", "desc": "数码/科技/AI", "icon": "🌃", "best": "AI、编程、科技、服务器", "category": "科技知识"},
    "minimal": {"name": "极简主义", "desc": "设计/商务/美学", "icon": "⬜", "best": "知识科普、商务、设计美学", "category": "科技知识"},
    "magazine":{"name": "杂志风", "desc": "商业/深度/报道", "icon": "📰", "best": "商业财经、深度报道、行业分析", "category": "科技知识"},
    "pixel":   {"name": "像素复古", "desc": "复古/游戏/极客", "icon": "👾", "best": "复古游戏、极客、街机怀旧", "category": "科技知识"},
    # ===== 生活娱乐类 =====
    "funny":   {"name": "搞笑整活", "desc": "搞笑/整活/表情包", "icon": "😂", "best": "搞笑、沙雕、吐槽、鬼畜", "category": "生活娱乐"},
    "food":    {"name": "美食暖调", "desc": "美食/探店/烹饪", "icon": "🍜", "best": "美食、探店、烹饪教程", "category": "生活娱乐"},
    "gaming":  {"name": "游戏电竞", "desc": "游戏/电竞/直播", "icon": "🎮", "best": "游戏、电竞、通关攻略", "category": "生活娱乐"},
    "variety": {"name": "综艺弹幕", "desc": "热点/吐槽/反应", "icon": "💬", "best": "热点、吃瓜、名场面、反应", "category": "生活娱乐"},
    "cute":    {"name": "萌宠可爱", "desc": "宠物/萌系/卡通", "icon": "🐱", "best": "宠物、萌系、卡通、手帐", "category": "生活娱乐"},
    # ===== 视觉冲击类 =====
    "paper":   {"name": "撕纸拼贴", "desc": "评测/攻略/安利", "icon": "✂️", "best": "安利推荐、攻略对比、排行盘点", "category": "视觉冲击"},
    "dopamine":{"name": "多巴胺撞色", "desc": "潮流/撞色/快乐", "icon": "🌈", "best": "潮流穿搭、夏日、元气活力", "category": "视觉冲击"},
    "doodle":  {"name": "手绘涂鸦", "desc": "文创/手绘/创意", "icon": "🖍️", "best": "文创、手绘、创意DIY", "category": "视觉冲击"},
    "luxury":  {"name": "黑金奢华", "desc": "评测/高端/开箱", "icon": "👑", "best": "数码评测、开箱、高端体验", "category": "视觉冲击"},
    # ===== 文艺清新类 =====
    "fresh":   {"name": "清新治愈", "desc": "Vlog/生活/旅行", "icon": "🍃", "best": "Vlog、旅行、生活记录", "category": "文艺清新"},
    "anime":   {"name": "二次元动漫", "desc": "ACG/番剧/虚拟主播", "icon": "🌸", "best": "动漫、番剧、虚拟主播", "category": "文艺清新"},
    "cinema":  {"name": "影视悬疑", "desc": "影视/悬疑/解说", "icon": "🎬", "best": "电影解说、悬疑、剧情", "category": "文艺清新"},
    "journal": {"name": "手账风", "desc": "笔记/记录/手写", "icon": "📓", "best": "手账、笔记、日记、打卡", "category": "文艺清新"},
    "guochao": {"name": "国潮风", "desc": "国风/传统/文化", "icon": "🏮", "best": "国风、汉服、传统文化、非遗", "category": "文艺清新"},
    # ===== 新增11种风格 =====
    "vaporwave": {"name": "蒸汽波", "desc": "复古/迷幻/80s", "icon": "👾", "best": "复古、迷幻、音乐、80s怀旧", "category": "视觉冲击"},
    "acid":      {"name": "酸性设计", "desc": "液态/荧光/前卫", "icon": "💥", "best": "前卫艺术、音乐、潮流、实验", "category": "视觉冲击"},
    "memphis":   {"name": "孟菲斯", "desc": "几何/波点/撞色", "icon": "🎨", "best": "活泼、卡通、教育、年轻化", "category": "视觉冲击"},
    "comic":     {"name": "漫画风", "desc": "描边/气泡/热血", "icon": "💬", "best": "漫画解说、热血、战斗、搞笑", "category": "视觉冲击"},
    "neon":      {"name": "霓虹灯", "desc": "暗夜/发光/荧光", "icon": "⚡", "best": "夜店、音乐、赛博、暗夜", "category": "视觉冲击"},
    "clay":      {"name": "黏土风", "desc": "3D/圆润/童趣", "icon": "👶", "best": "儿童、萌系、教程、可爱", "category": "生活娱乐"},
    "glass":     {"name": "玻璃拟态", "desc": "模糊/半透/质感", "icon": "🔹", "best": "科技、产品、高端、设计", "category": "科技知识"},
    "aurora":    {"name": "弥散光", "desc": "极光/光晕/梦幻", "icon": "🌌", "best": "梦幻、星空、科幻、宇宙", "category": "科技知识"},
    "sticker":   {"name": "贴纸风", "desc": "白边/手绘/可爱", "icon": "🎀", "best": "手绘、可爱、装饰、日记", "category": "文艺清新"},
    "retro":     {"name": "复古风", "desc": "胶片/做旧/怀旧", "icon": "📷", "best": "怀旧、老歌、胶片、回忆", "category": "文艺清新"},
    "collage":   {"name": "拼贴风", "desc": "剪报/胶带/混合", "icon": "📌", "best": "文艺、剪报、手做、混搭", "category": "文艺清新"},
    # ===== 新增20种风格 v6 =====
    "ink":         {"name": "水墨风", "desc": "国画/书法/写意", "icon": "🎨", "best": "书法、国画、东方美学、文化", "category": "文艺清新"},
    "stamp":       {"name": "印章风", "desc": "篆刻/朱印/传统", "icon": "📠", "best": "传统文化、篆刻、收藏、鉴定", "category": "文艺清新"},
    "newspaper":   {"name": "报纸风", "desc": "新闻/头条/社论", "icon": "📰", "best": "新闻、报道、评论、时事", "category": "文艺清新"},
    "polaroid":    {"name": "拍立得", "desc": "白边/相框/回忆", "icon": "📷", "best": "旅行、回忆、日常、Vlog", "category": "文艺清新"},
    "risograph":   {"name": "Riso印刷", "desc": "双色/颗粒/独立出版", "icon": "📄", "best": "独立出版、设计、艺术、Zine", "category": "文艺清新"},
    "film":        {"name": "胶片风", "desc": "胶卷/帧/放映", "icon": "🎞️", "best": "电影、摄影、胶片相机、怀旧", "category": "文艺清新"},
    "ribbon":      {"name": "缎带风", "desc": "丝带/横幅/颁奖", "icon": "🎀", "best": "颁奖、典礼、表彰、节日", "category": "文艺清新"},
    "pastel":      {"name": "莫兰迪", "desc": "低饱和/高级灰/柔和", "icon": "💛", "best": "家居、穿搭、高级感、内敛", "category": "文艺清新"},
    "kraft":       {"name": "牛皮纸", "desc": "纸袋/手工/质朴", "icon": "📄", "best": "手工、包装、质朴、原生态", "category": "文艺清新"},
    "washi":       {"name": "和纸胶带", "desc": "日式/纸胶带/装饰", "icon": "🎀", "best": "手帐、日式、拼贴、装饰", "category": "文艺清新"},
    "graffiti":    {"name": "涂鸦街头", "desc": "喷漆/街头/野生", "icon": "💥", "best": "街头文化、嘻哈、滑板、反叛", "category": "视觉冲击"},
    "gradientmesh": {"name": "网格渐变", "desc": "柔和/多色/梦幻", "icon": "🌈", "best": "梦幻、柔和、品牌、壁纸", "category": "视觉冲击"},
    "brutalist":   {"name": "粗野主义", "desc": "原始/混凝土/粗犷", "icon": "◼️", "best": "建筑、结构、极简粗野、设计", "category": "视觉冲击"},
    "popart":      {"name": "波普艺术", "desc": "撞色/网点/大众艺术", "icon": "🎨", "best": "波普、明星、消费、撞色", "category": "生活娱乐"},
    "holographic": {"name": "全息彩虹", "desc": "镭射/幻彩/偏光", "icon": "✨", "best": "潮流、镭射、炫彩、未来", "category": "视觉冲击"},
    "carnival":    {"name": "嘉年华", "desc": "马戏团/彩旗/狂欢", "icon": "🎪", "best": "庆典、派对、节日、游乐园", "category": "生活娱乐"},
    "blueprint":   {"name": "蓝图风", "desc": "工程图/制图/蓝底白线", "icon": "📐", "best": "建筑、工程、技术制图、设计", "category": "科技知识"},
    "starfield":   {"name": "星空宇宙", "desc": "深空/银河/星海", "icon": "🌌", "best": "天文、科幻、宇宙、探索", "category": "科技知识"},
    "typewriter":  {"name": "打字机", "desc": "等宽/手稿/复古", "icon": "⌨", "best": "手稿、文稿、复古、文字", "category": "科技知识"},
    "terrarium":   {"name": "玻璃生态", "desc": "植物/微景观/通透", "icon": "🌱", "best": "植物、自然、微景观、生态", "category": "文艺清新"},
    # ===== v7 新增5种「真实派」风格 — 点击率最高 =====
    "screenshot": {"name": "真实截图", "desc": "PPT/代码/演示", "icon": "💻", "best": "教程、源码、实操、案例", "category": "视觉冲击"},
    "portrait":   {"name": "真人出镜", "desc": "经验/职业/分享", "icon": "👤", "best": "经验、职业、面试、转型分享", "category": "视觉冲击"},
    "product":    {"name": "实物产品", "desc": "测评/开箱/工具", "icon": "📱", "best": "开箱、测评、工具、硬件", "category": "视觉冲击"},
    "contrast":   {"name": "对比冲击", "desc": "对比/vs/盘点", "icon": "🆚", "best": "对比、区别、选择、TOP排行", "category": "视觉冲击"},
    "zoom":       {"name": "局部放大", "desc": "细节/重点/特写", "icon": "🔍", "best": "细节、重点、特写、深入", "category": "视觉冲击"},
}


def make_mini_card(theme, title, subtitle, tags, badge, quote, highlights):
    """生成主题选择页的迷你卡片"""
    sk = get_scheme_by_theme(theme, 0)
    sc = COLOR_SCHEMES[sk]
    bg = sc["bg"]
    a1 = sc["accent1"]
    a2 = sc["accent2"]
    text_color = sc.get("text_color", "#ffffff")
    is_gradient = sc.get("is_gradient", False)

    # 使用 iconfont 卡通素材
    deco_assets = get_decoration_assets(theme, 0)
    (da1_url, da1_name), (da2_url, da2_name) = deco_assets[0], deco_assets[1] if len(deco_assets) > 1 else (deco_assets[0][0], deco_assets[0][1])

    # 风格对应的 emoji（用于 badge）
    theme_emoji_list = THEME_EMOJIS.get(theme, THEME_EMOJIS.get("cyber", []))
    badge_emoji = theme_emoji_list[0][1] if theme_emoji_list else ""

    dt = apply_highlights(title, highlights, theme, a1, a2)

    th = ""
    for i, t in enumerate(tags):
        tc = [a1,a2,a1,a2][i%4]
        op = 0.25 if i%2==0 else 0.20
        th += f'<span class="cv-tag" style="background:rgba({hex_to_rgb(tc)},{op});color:{tc};">{t}</span>'

    info = THEME_INFO.get(theme, {"name":theme,"desc":"","icon":"📄","best":""})
    bg_style = f"background:{bg};"

    return f'''<div class="theme-card" data-theme="{theme}" onclick="goDetail('{theme}')">
  <div class="theme-preview theme-{theme}" style="--bg-color:{bg};--accent1:{a1};--accent2:{a2};--text-color:{text_color};{bg_style}">
    <div class="cv-bg-decoration">
      <div class="cv-bg-circle" style="width:180px;height:180px;background:{a1};top:-40px;left:-40px;"></div>
      <div class="cv-bg-circle" style="width:140px;height:140px;background:{a2};bottom:-30px;right:-30px;"></div>
      <img class="cv-emoji-deco cv-iconfont-deco" src="{da1_url}" alt="{da1_name}" style="top:8%;left:4%;width:36px;height:36px;filter:drop-shadow(1px 1px 2px rgba(0,0,0,0.15));" onerror="this.style.display='none'">
      <img class="cv-emoji-deco cv-iconfont-deco" src="{da2_url}" alt="{da2_name}" style="bottom:8%;right:4%;width:28px;height:28px;filter:drop-shadow(1px 1px 2px rgba(0,0,0,0.15));" onerror="this.style.display='none'">
      <!-- 迷你卡通角色预览 -->
      <img class="cv-mascot" src="{da1_url}" alt="{da1_name}" style="right:2%;bottom:8%;width:25%;height:auto;opacity:0.88;filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.2));" onerror="this.style.display='none'">
    </div>
    <div class="cv-content">
      <div class="cv-badge" style="background:rgba({hex_to_rgb(a1)},0.2);color:{a1};border:1px solid rgba({hex_to_rgb(a1)},0.4);">{badge_emoji} {badge}</div>
      <div class="cv-main-title" style="font-size:22px;color:{text_color};">{dt}</div>
      <div class="cv-sub-title" style="font-size:11px;color:{text_color};">{subtitle}</div>
      <div class="cv-tag-row">{th}</div>
    </div>
  </div>
  <div class="theme-info">
    <div class="theme-name">{info["icon"]} {info["name"]} <span class="theme-tag">点击查看4平台效果 →</span></div>
    <div class="theme-desc">{info["desc"]} · 适合：{info["best"]}</div>
  </div>
</div>'''


def generate_picker_html(title, subtitle, tags, badge, quote, highlights, photo_url="", photo_position="right"):
    """生成主题选择首页 + 所有风格详情页（单文件）"""

    # 生成19个主题卡片，按分类分组
    all_themes = ["bold","cyber","minimal","magazine","pixel","glass","aurora","blueprint","typewriter","starfield",
                  "funny","food","gaming","variety","cute","clay","carnival","popart",
                  "paper","dopamine","doodle","luxury","vaporwave","acid","memphis","comic","neon","graffiti","brutalist","holographic","gradientmesh",
                  "screenshot","portrait","product","contrast","zoom",
                  "fresh","anime","cinema","journal","guochao","sticker","retro","collage","ink","stamp","newspaper","polaroid","risograph","film","ribbon","pastel","kraft","washi","terrarium"]
    # 按分类分组
    categories = {}
    for theme in all_themes:
        info = THEME_INFO.get(theme, {})
        cat = info.get("category", "其他")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(theme)
    
    cards_html = ""
    cat_icons = {"科技知识":"🚀","生活娱乐":"🎉","视觉冲击":"💥","文艺清新":"🍃"}
    for cat, themes in categories.items():
        icon = cat_icons.get(cat, "📄")
        cards_html += f'    <div class="category-section">\n      <div class="category-title">{icon} {cat}</div>\n      <div class="category-grid">\n'
        for theme in themes:
            cards_html += make_mini_card(theme, title, subtitle, tags, badge, quote, highlights) + "\n"
        cards_html += '      </div>\n    </div>\n'

    # 自动匹配
    auto_theme = detect_theme(title, tags)
    auto_info = THEME_INFO.get(auto_theme, {"name":auto_theme,"icon":"🤖"})

    # 为每个主题生成4平台详情页的HTML（内嵌为隐藏div）
    detail_pages = []
    for theme in all_themes:
        cover_cfg = {
            "title": title, "highlight_words": highlights,
            "subtitle": subtitle, "tags": tags,
            "badge": badge, "quote": quote, "theme": theme,
            "photo_url": photo_url, "photo_position": photo_position,
        }

        # 生成4平台的slides
        pks = ["bilibili","xiaohongshu","wechat","mobile"]
        slides = []
        thumbs = []
        si = 0
        for pk in pks:
            pf = PLATFORMS[pk]
            si += 1
            first = si == 1
            t = title
            label = pf.get("icon","📄") + " " + pf["name"]
            act = ' active' if first else ''
            slide_html = generate_single_cover(cover_cfg, pk, 0)
            slides.append(f'      <div class="slide{act}" data-slide="{si}">\n{slide_html}\n      </div>')
            thumbs.append(f'''        <button class="thumb-btn{act}" onclick="goSlide('{theme}',{si})" title="{t}">
          <span class="thumb-label">{label}</span>
          <span class="thumb-num">{si}</span>
        </button>''')

        slide_html_str = "\n".join(slides)
        thumb_html_str = "\n".join(thumbs)
        info = THEME_INFO.get(theme, {})
        detail_pages.append(f'''<div class="detail-page" id="detail-{theme}" style="display:none;">
  <div class="detail-header">
    <button class="back-btn" onclick="goPicker()">← 返回选择风格</button>
    <span class="detail-title">{info.get("icon","")} {info.get("name","")} · 4平台封面预览</span>
    <span class="detail-page-num"><span id="curPage-{theme}">1</span> / 4</span>
  </div>
  <div class="stage">
{slide_html_str}
  </div>
  <nav class="navbar">
{thumb_html_str}
  </nav>
</div>''')

    detail_html = "\n".join(detail_pages)

    pf_css = "\n".join(f"  .cover-{pk} {{ aspect-ratio: {v['ratio']}; max-width: {v['width']}px; }}"
                       for pk, v in PLATFORMS.items())

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
  min-height:100vh;
}}

/* ===== 主题选择页 ===== */
#picker-page {{
  display:flex; flex-direction:column; min-height:100vh;
  padding:24px;
}}
#picker-page.hidden {{ display:none; }}

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

/* ===== 分类区块 ===== */
.category-section {{
  max-width:1400px; margin:0 auto 36px; width:100%;
}}
.category-title {{
  font-size:18px; font-weight:800; color:#f59e0b; margin-bottom:16px; padding-left:4px;
  border-left:3px solid #f59e0b; padding-left:12px;
}}
.category-grid {{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
  gap:20px;
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
.theme-card .theme-tag {{
  font-size:11px; color:#f59e0b; font-weight:500; float:right;
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

.theme-preview[style*="#fff"] .cv-emoji-deco,
.theme-preview[style*="#fbbf24"] .cv-emoji-deco,
.theme-preview[style*="#e0f2fe"] .cv-emoji-deco,
.theme-preview[style*="#f0fdf4"] .cv-emoji-deco,
.theme-preview[style*="#fefce8"] .cv-emoji-deco,
.theme-preview[style*="#fff7ed"] .cv-emoji-deco,
.theme-preview[style*="#fdf2f8"] .cv-emoji-deco,
.theme-preview[style*="#ecfeff"] .cv-emoji-deco,
.theme-preview[style*="#fff0f5"] .cv-emoji-deco,
.theme-preview[style*="#fef3c7"] .cv-emoji-deco {{ opacity:0.15; }}

{THEME_FONT_CSS}

.theme-cute .cv-main-title {{ font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif; }}
.theme-fresh .cv-main-title {{ font-family:'Ma Shan Zheng','Noto Sans SC',sans-serif; font-weight:400; }}
.theme-anime .cv-main-title {{ font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif; }}
.theme-doodle .cv-main-title {{ font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif; }}

.theme-info {{ padding:14px 16px; }}
.theme-name {{ font-size:16px; font-weight:700; margin-bottom:4px; }}
.theme-desc {{ font-size:13px; color:rgba(255,255,255,0.45); }}

/* ===== 详情页 ===== */
.detail-page {{
  display:flex; flex-direction:column;
  height:100vh; width:100vw;
}}
.detail-page[style*="display:none"] {{ display:none !important; }}

.detail-header {{
  flex-shrink:0;
  display:flex; align-items:center; justify-content:space-between;
  padding:10px 28px;
  background:#161b22; border-bottom:1px solid rgba(255,255,255,0.08);
  color:rgba(255,255,255,0.65); font-size:13px; z-index:20;
}}
.back-btn {{
  background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);
  color:rgba(255,255,255,0.7); padding:6px 16px; border-radius:8px;
  font-family:inherit; font-size:13px; font-weight:600; cursor:pointer;
  transition:all 0.2s;
}}
.back-btn:hover {{
  background:rgba(255,255,255,0.1); border-color:rgba(255,255,255,0.2);
  color:#fff;
}}
.detail-title {{ font-weight:600; color:rgba(255,255,255,0.85); font-size:14px; }}
.detail-page-num {{ font-family:'SF Mono',Monaco,monospace; font-size:12px; color:rgba(255,255,255,0.35); }}

.stage {{
  flex:1; display:flex; align-items:center; justify-content:center;
  padding:20px 40px; overflow:hidden; position:relative;
}}
.slide {{
  display:none; width:100%; height:100%;
  align-items:center; justify-content:center;
  animation:slideIn 0.3s ease;
}}
.slide.active {{ display:flex; }}
@keyframes slideIn {{ from{{opacity:0;transform:scale(.96)}} to{{opacity:1;transform:scale(1)}} }}

.cover-card {{
  width:94%; max-height:92%;
  border-radius:8px; overflow:hidden; position:relative;
  box-shadow:0 12px 48px rgba(0,0,0,.5);
  display:flex; align-items:center; justify-content:center;
  color:#fff; text-align:center; background:var(--bg-color,#1a1a2e);
}}
{pf_css}

.cover-card .cv-bg-decoration {{ position:absolute; inset:0; pointer-events:none; z-index:0; }}
.cover-card .cv-bg-circle {{ position:absolute; border-radius:50%; opacity:.06; }}
.cover-card .cv-content {{
  position:relative; z-index:2; display:flex; flex-direction:column;
  align-items:center; justify-content:center; width:100%; height:100%; padding:40px;
}}
.cover-card .cv-badge {{
  display:inline-flex; align-items:center; gap:6px;
  padding:6px 18px; border-radius:20px;
  font-size:14px; font-weight:700; letter-spacing:1px; margin-bottom:16px;
}}
.cover-card .cv-main-title {{
  font-weight:900; line-height:1.08; letter-spacing:2px; margin-bottom:10px;
  text-shadow:0 4px 20px rgba(0,0,0,.4); max-width:90%; color:var(--text-color,#fff);
}}
.cover-card .cv-sub-title {{
  font-weight:600; margin-bottom:16px; letter-spacing:1px; max-width:85%;
  color:var(--text-color,#fff); opacity:0.8;
}}
.cover-card .cv-tag-row {{ display:flex; gap:10px; flex-wrap:wrap; justify-content:center; margin-top:14px; }}
.cover-card .cv-tag {{ padding:6px 18px; border-radius:16px; font-size:15px; font-weight:700; letter-spacing:.5px; }}
.cover-card .cv-emoji-deco {{ position:absolute; opacity:.10; z-index:1; object-fit:contain; }}
.cover-card .cv-bottom-bar {{
  position:absolute; bottom:0; left:0; right:0; height:36px;
  background:rgba(0,0,0,.35); backdrop-filter:blur(4px);
  display:flex; align-items:center; justify-content:space-between;
  padding:0 28px; font-size:13px; color:rgba(255,255,255,.5); z-index:4;
}}

/* 平台适配 */
.cover-xiaohongshu .cv-content {{ padding:36px 32px; }}
.cover-xiaohongshu .cv-main-title {{ line-height:1.12; }}
.cover-wechat .cv-content {{ padding:32px 28px; }}
.cover-wechat .cv-main-title {{ line-height:1.15; }}
.cover-wechat .cv-badge {{ margin-bottom:24px; }}
.cover-mobile .cv-content {{ padding:28px 24px; }}
.cover-mobile .cv-main-title {{ line-height:1.18; letter-spacing:1px; }}
.cover-mobile .cv-badge {{ margin-bottom:28px; padding:5px 14px; font-size:12px; }}
.cover-mobile .cv-sub-title {{ font-size:19px; margin-bottom:12px; }}
.cover-mobile .cv-tag {{ padding:5px 14px; font-size:13px; }}
.cover-card[style*="linear-gradient"] {{ background:var(--bg-color); }}

/* 浅色背景 */
.cover-card[style*="#fff"] .cv-bottom-bar,
.cover-card[style*="#fbbf24"] .cv-bottom-bar,
.cover-card[style*="#e0f2fe"] .cv-bottom-bar,
.cover-card[style*="#f0fdf4"] .cv-bottom-bar,
.cover-card[style*="#fefce8"] .cv-bottom-bar,
.cover-card[style*="#fff7ed"] .cv-bottom-bar,
.cover-card[style*="#fdf2f8"] .cv-bottom-bar,
.cover-card[style*="#ecfeff"] .cv-bottom-bar,
.cover-card[style*="#fff0f5"] .cv-bottom-bar,
.cover-card[style*="#fef3c7"] .cv-bottom-bar {{
  background:rgba(0,0,0,.12); color:rgba(0,0,0,.4);
}}

.navbar {{
  flex-shrink:0;
  display:flex; align-items:center; gap:6px;
  padding:10px 20px 14px;
  background:#161b22; border-top:1px solid rgba(255,255,255,0.08);
  overflow-x:auto; overflow-y:hidden;
  -webkit-overflow-scrolling:touch;
  scrollbar-width:none;
}}
.navbar::-webkit-scrollbar {{ display:none; }}

.thumb-btn {{
  flex-shrink:0;
  display:flex; align-items:center; gap:6px;
  padding:7px 14px; border-radius:6px;
  border:1.5px solid rgba(255,255,255,.12);
  background:rgba(255,255,255,.04);
  color:rgba(255,255,255,.55);
  font-family:inherit; font-size:12px; font-weight:600;
  cursor:pointer; transition:all 0.2s ease; white-space:nowrap;
}}
.thumb-btn:hover {{
  background:rgba(255,255,255,.08); color:rgba(255,255,255,.75);
  border-color:rgba(255,255,255,.2);
}}
.thumb-btn.active {{
  background:rgba(245,158,11,.15); color:#f59e0b;
  border-color:rgba(245,158,11,.5);
  box-shadow:0 0 12px rgba(245,158,11,.15);
}}
.thumb-label {{ font-weight:700; white-space:nowrap; }}
.thumb-num {{
  font-size:10px; font-weight:600;
  min-width:16px; height:16px; line-height:16px;
  border-radius:4px; text-align:center;
  background:currentColor; color:transparent;
  -webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3'/%3E%3C/svg%3E") center/contain no-repeat;
  mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3'/%3E%3C/svg%3E") center/contain no-repeat;
}}
.thumb-btn.active .thumb-num {{
  background:#f59e0b; color:#fff;
  -webkit-mask:none; mask:none;
}}

.footer {{
  text-align:center; margin-top:32px; padding:20px;
  color:rgba(255,255,255,0.3); font-size:13px;
}}
</style>
</head>
<body>

<!-- ===== 主题选择页 ===== -->
<div id="picker-page">
  <div class="header">
    <h1>🎨 选择封面风格</h1>
    <p>30大B站爆款风格 · 4大分类 · 点击卡片查看4平台详细效果</p>
    <div class="auto-match">🤖 自动推荐：<strong>{auto_info["icon"]} {auto_info["name"]}</strong>（基于标题关键词检测）</div>
  </div>

  <div class="grid-container">
{cards_html}
  </div>

  <div class="footer">
    点击任意风格卡片 → 查看 B站 / 小红书 / 微信视频号 / 手机竖版 4种尺寸效果\n    · 键盘 ← → 翻页 · ESC 返回选择
  </div>
</div>

<!-- ===== 13个详情页（隐藏） ===== -->
{detail_html}

<script>
// 主题选择 → 详情页
function goDetail(theme) {{
  document.getElementById('picker-page').classList.add('hidden');
  document.querySelectorAll('.detail-page').forEach(d => d.style.display = 'none');
  const dp = document.getElementById('detail-' + theme);
  if (dp) {{
    dp.style.display = 'flex';
    // 重置到第一页
    goSlide(theme, 1);
  }}
}}

// 返回选择页
function goPicker() {{
  document.getElementById('picker-page').classList.remove('hidden');
  document.querySelectorAll('.detail-page').forEach(d => d.style.display = 'none');
}}

// 详情页内翻页
var slideState = {{}};
function goSlide(theme, n) {{
  const total = 4;
  if (n < 1 || n > total) return;
  slideState[theme] = n;
  const dp = document.getElementById('detail-' + theme);
  if (!dp) return;
  dp.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
  const slide = dp.querySelector('.slide[data-slide="' + n + '"]');
  if (slide) slide.classList.add('active');
  dp.querySelectorAll('.thumb-btn').forEach(b => b.classList.remove('active'));
  const btns = dp.querySelectorAll('.thumb-btn');
  if (btns[n-1]) btns[n-1].classList.add('active');
  const pg = document.getElementById('curPage-' + theme);
  if (pg) pg.textContent = n;
}}

// 键盘翻页（在详情页时生效）
document.addEventListener('keydown', function(e) {{
  // 找到当前显示的详情页
  let activeTheme = null;
  document.querySelectorAll('.detail-page').forEach(d => {{
    if (d.style.display === 'flex') {{
      activeTheme = d.id.replace('detail-', '');
    }}
  }});
  if (!activeTheme) return;
  
  const cur = slideState[activeTheme] || 1;
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') goSlide(activeTheme, cur - 1);
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') goSlide(activeTheme, cur + 1);
  if (e.key === 'Escape') goPicker();
}});
</script>

</body>
</html>'''


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="主题选择器 v2.0 - 点击跳转4平台详情")
    p.add_argument("--title","-t",default="都在写AI Agent项目，怎么拉开技术差距？")
    p.add_argument("--subtitle",default="阿里也在做的核心技术项目")
    p.add_argument("--tags",default="AI Agent,技术差距,阿里,核心项目")
    p.add_argument("--badge",default="深度解析")
    p.add_argument("--quote",default="")
    p.add_argument("--highlight",default="拉开技术差距,核心技术项目")
    p.add_argument("--output","-o",default="theme-picker.html")
    p.add_argument("--photo-url",default="",help="真人出镜照片URL或本地路径")
    p.add_argument("--photo-position",default="right",choices=["right","left","center"],help="照片位置")
    a = p.parse_args()

    html = generate_picker_html(
        title=a.title, subtitle=a.subtitle,
        tags=[t.strip() for t in a.tags.split(",")],
        badge=a.badge,
        quote=a.quote,
        highlights=[h.strip() for h in a.highlight.split(",")],
        photo_url=a.photo_url,
        photo_position=a.photo_position,
    )
    with open(a.output,"w",encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 主题选择器已生成 → {a.output}")
    print(f"   55种风格 · 4大分类 · 点击卡片跳转4平台详情页")
