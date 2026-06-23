#!/usr/bin/env python3
"""
视频封面生成器 v3.2 - 主脚本
13大B站爆款风格 × 差异化字体排版 × 4平台 × 50+套配色

v3.2 更新：
- 新增3种风格：撕纸拼贴(paper) / 综艺弹幕(variety) / 手绘涂鸦(doodle)
- 优化5种现有风格：bold加描边 / cyber加网格线 / funny加混乱表情 / luxury加金线 / cinema加黑边
- 新增视觉箭头/指示元素
- 配色扩充至50+套
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
    "mobile": {"name": "手机竖版", "icon": "📲", "ratio": "440 / 710", "width": 440, "height": 710,
             "title_size": 52, "subtitle_size": 20, "tag_size": 12, "badge_size": 11},
}

# ========== 50+套B站爆款配色 ==========
COLOR_SCHEMES = {
    "bold_1": {"bg": "#ffffff", "accent1": "#fbbf24", "accent2": "#ef4444", "name": "纯白黄红", "theme": "bold", "text_color": "#000000"},
    "bold_2": {"bg": "#0a0a0a", "accent1": "#ffffff", "accent2": "#fbbf24", "name": "纯黑白字", "theme": "bold"},
    "bold_3": {"bg": "#fbbf24", "accent1": "#7c3aed", "accent2": "#ef4444", "name": "亮黄紫红", "theme": "bold", "text_color": "#000000"},
    "bold_4": {"bg": "#dc2626", "accent1": "#ffffff", "accent2": "#fbbf24", "name": "亮红白字", "theme": "bold"},
    "bold_5": {"bg": "#2563eb", "accent1": "#ffffff", "accent2": "#fde047", "name": "亮蓝白字", "theme": "bold"},
    "cyber_1": {"bg": "#1a0a2e", "accent1": "#ff00ff", "accent2": "#00ffff", "name": "霓虹紫粉", "theme": "cyber"},
    "cyber_2": {"bg": "#0d1117", "accent1": "#00ff41", "accent2": "#0080ff", "name": "电子蓝绿", "theme": "cyber"},
    "cyber_3": {"bg": "#0a0a0a", "accent1": "#ff006e", "accent2": "#3a86ff", "name": "故障红蓝", "theme": "cyber"},
    "cyber_4": {"bg": "#0a0e27", "accent1": "#00d9ff", "accent2": "#9d4edd", "name": "暗夜电光", "theme": "cyber"},
    "anime_1": {"bg": "#fff0f5", "accent1": "#ff69b4", "accent2": "#9370db", "name": "樱花粉白", "theme": "anime", "text_color": "#1a1a2e"},
    "anime_2": {"bg": "#1a1a3e", "accent1": "#ffd700", "accent2": "#ff85a2", "name": "夜空星空", "theme": "anime"},
    "anime_3": {"bg": "linear-gradient(135deg,#f093fb 0%,#f5576c 100%)", "accent1": "#ffffff", "accent2": "#ffd700", "name": "渐变梦幻", "theme": "anime", "is_gradient": True},
    "anime_4": {"bg": "#2d1b69", "accent1": "#a78bfa", "accent2": "#f0abfc", "name": "蓝紫二次元", "theme": "anime"},
    "funny_1": {"bg": "#fbbf24", "accent1": "#7c3aed", "accent2": "#ef4444", "name": "撞色黄紫", "theme": "funny", "text_color": "#1a1a2e"},
    "funny_2": {"bg": "#ef4444", "accent1": "#22c55e", "accent2": "#fbbf24", "name": "红绿撞色", "theme": "funny"},
    "funny_3": {"bg": "#0ea5e9", "accent1": "#f97316", "accent2": "#ffffff", "name": "蓝橙撞色", "theme": "funny"},
    "funny_4": {"bg": "#1a1a2e", "accent1": "#fbbf24", "accent2": "#ef4444", "name": "彩虹拼贴", "theme": "funny"},
    "luxury_1": {"bg": "#0a0a0a", "accent1": "#fbbf24", "accent2": "#ffffff", "name": "经典黑金", "theme": "luxury"},
    "luxury_2": {"bg": "#1c1410", "accent1": "#d4af37", "accent2": "#c0c0c0", "name": "深棕金", "theme": "luxury"},
    "luxury_3": {"bg": "#0d2818", "accent1": "#d4af37", "accent2": "#ffffff", "name": "墨绿金", "theme": "luxury"},
    "luxury_4": {"bg": "#1a0a2e", "accent1": "#ffd700", "accent2": "#c084fc", "name": "暗紫金", "theme": "luxury"},
    "fresh_1": {"bg": "#e0f2fe", "accent1": "#0284c7", "accent2": "#fbbf24", "name": "天空蓝白", "theme": "fresh", "text_color": "#0c4a6e"},
    "fresh_2": {"bg": "#f0fdf4", "accent1": "#16a34a", "accent2": "#f59e0b", "name": "薄荷绿白", "theme": "fresh", "text_color": "#14532d"},
    "fresh_3": {"bg": "#fefce8", "accent1": "#ca8a04", "accent2": "#ec4899", "name": "暖白米色", "theme": "fresh", "text_color": "#422006"},
    "fresh_4": {"bg": "#fff7ed", "accent1": "#ea580c", "accent2": "#ec4899", "name": "黄昏橙粉", "theme": "fresh", "text_color": "#7c2d12"},
    "gaming_1": {"bg": "#1a0505", "accent1": "#ef4444", "accent2": "#fbbf24", "name": "暗红电竞", "theme": "gaming"},
    "gaming_2": {"bg": "#0a0e27", "accent1": "#3b82f6", "accent2": "#fbbf24", "name": "暗蓝电竞", "theme": "gaming"},
    "gaming_3": {"bg": "#13091e", "accent1": "#a855f7", "accent2": "#22d3ee", "name": "暗紫电竞", "theme": "gaming"},
    "gaming_4": {"bg": "#0a1a0a", "accent1": "#22c55e", "accent2": "#fbbf24", "name": "暗绿电竞", "theme": "gaming"},
    "food_1": {"bg": "#2a0a0a", "accent1": "#f97316", "accent2": "#fbbf24", "name": "暖橙红", "theme": "food"},
    "food_2": {"bg": "#451a03", "accent1": "#fde047", "accent2": "#fb923c", "name": "奶油棕", "theme": "food"},
    "food_3": {"bg": "#ea580c", "accent1": "#ffffff", "accent2": "#fbbf24", "name": "鲜橙亮黄", "theme": "food"},
    "food_4": {"bg": "#7f1d1d", "accent1": "#fbbf24", "accent2": "#ef4444", "name": "红锅辣味", "theme": "food"},
    "cinema_1": {"bg": "#0a0a0a", "accent1": "#dc2626", "accent2": "#6b7280", "name": "暗红悬疑", "theme": "cinema"},
    "cinema_2": {"bg": "#0c1820", "accent1": "#06b6d4", "accent2": "#fbbf24", "name": "暗青电影", "theme": "cinema"},
    "cinema_3": {"bg": "#1a1410", "accent1": "#d4a373", "accent2": "#fefae0", "name": "复古胶片", "theme": "cinema"},
    "cinema_4": {"bg": "#0a1008", "accent1": "#22c55e", "accent2": "#ef4444", "name": "惊悚暗绿", "theme": "cinema"},
    "cute_1": {"bg": "#fdf2f8", "accent1": "#ec4899", "accent2": "#a78bfa", "name": "粉白萌系", "theme": "cute", "text_color": "#831843"},
    "cute_2": {"bg": "#fefce8", "accent1": "#f59e0b", "accent2": "#ec4899", "name": "奶黄萌系", "theme": "cute", "text_color": "#422006"},
    "cute_3": {"bg": "#ecfeff", "accent1": "#06b6d4", "accent2": "#fbbf24", "name": "薄荷蓝萌", "theme": "cute", "text_color": "#164e63"},
    "cute_4": {"bg": "linear-gradient(135deg,#fbcfe8 0%,#c4b5fd 100%)", "accent1": "#7c3aed", "accent2": "#ec4899", "name": "渐变粉紫", "theme": "cute", "is_gradient": True, "text_color": "#581c87"},
    # ===== 11. 撕纸拼贴风（paper）— 评测/攻略/安利 =====
    "paper_1": {"bg": "#fef3c7", "accent1": "#ef4444", "accent2": "#1a1a2e", "name": "撕纸黄红黑", "theme": "paper", "text_color": "#1a1a2e"},
    "paper_2": {"bg": "#e0f2fe", "accent1": "#0ea5e9", "accent2": "#f97316", "name": "撕纸蓝橙", "theme": "paper", "text_color": "#0c4a6e"},
    "paper_3": {"bg": "#fdf2f8", "accent1": "#ec4899", "accent2": "#8b5cf6", "name": "撕纸粉紫", "theme": "paper", "text_color": "#831843"},
    "paper_4": {"bg": "#f0fdf4", "accent1": "#22c55e", "accent2": "#fbbf24", "name": "撕纸绿黄", "theme": "paper", "text_color": "#14532d"},
    # ===== 12. 综艺弹幕风（variety）— 热点/吐槽/ reactions =====
    "variety_1": {"bg": "#1a1a2e", "accent1": "#fbbf24", "accent2": "#ff006e", "name": "综艺金粉", "theme": "variety"},
    "variety_2": {"bg": "#0f0e17", "accent1": "#ff8906", "accent2": "#f25f4c", "name": "综艺橙红", "theme": "variety"},
    "variety_3": {"bg": "#2d1b69", "accent1": "#00ffff", "accent2": "#ff00ff", "name": "综艺霓虹", "theme": "variety"},
    "variety_4": {"bg": "#1a0505", "accent1": "#fbbf24", "accent2": "#ef4444", "name": "综艺红金", "theme": "variety"},
    # ===== 13. 手绘涂鸦风（doodle）— 文创/手帐/趣味 =====
    "doodle_1": {"bg": "#fefce8", "accent1": "#7c3aed", "accent2": "#ec4899", "name": "涂鸦黄紫粉", "theme": "doodle", "text_color": "#1a1a2e"},
    "doodle_2": {"bg": "#e0f2fe", "accent1": "#0284c7", "accent2": "#f59e0b", "name": "涂鸦蓝黄", "theme": "doodle", "text_color": "#0c4a6e"},
    "doodle_3": {"bg": "#f0fdf4", "accent1": "#16a34a", "accent2": "#dc2626", "name": "涂鸦绿红", "theme": "doodle", "text_color": "#14532d"},
    "doodle_4": {"bg": "#fff7ed", "accent1": "#ea580c", "accent2": "#7c3aed", "name": "涂鸦橙紫", "theme": "doodle", "text_color": "#7c2d12"},
    "tech_1": {"bg": "#0f0e17", "accent1": "#ff8906", "accent2": "#f25f4c", "name": "暗夜火焰", "theme": "tech"},
    "tech_3": {"bg": "#0d1117", "accent1": "#58a6ff", "accent2": "#7ee787", "name": "极客绿", "theme": "tech"},
    "tech_5": {"bg": "#0a0e27", "accent1": "#00d9ff", "accent2": "#9d4edd", "name": "电光紫蓝", "theme": "tech"},
    "hot_1": {"bg": "#2d0a0a", "accent1": "#fbbf24", "accent2": "#f87171", "name": "火焰金红", "theme": "hot"},
    "hot_4": {"bg": "#1a0505", "accent1": "#ef4444", "accent2": "#f59e0b", "name": "爆裂红金", "theme": "hot"},
    "cool_1": {"bg": "#0d1b2a", "accent1": "#00b4d8", "accent2": "#90e0ef", "name": "深海蓝青", "theme": "cool"},
    "warm_1": {"bg": "#2e0a1a", "accent1": "#f9a8d4", "accent2": "#ec4899", "name": "玫瑰粉", "theme": "warm"},
    "dark_1": {"bg": "#0a0a0a", "accent1": "#fbbf24", "accent2": "#ffffff", "name": "黑金奢华旧", "theme": "dark"},
    "gradient_1": {"bg": "linear-gradient(135deg,#667eea 0%,#764ba2 100%)", "accent1": "#ffd700", "accent2": "#fff", "name": "紫金渐变", "theme": "gradient", "is_gradient": True},
    "gradient_3": {"bg": "linear-gradient(135deg,#4facfe 0%,#00f2fe 100%)", "accent1": "#fff", "accent2": "#ffe066", "name": "天蓝渐变", "theme": "gradient", "is_gradient": True},
}

THEME_KEYWORDS = {
    "bold": ["干货","教程","知识","必看","入门","指南","科普","总结","万字","硬核","速成","避坑"],
    "cyber": ["AI","赛博","未来","霓虹","代码","编程","程序","服务器","Shell","API","CLI","Key","密钥","模型","Ollama","qwen","GPT","IDE","云","大模型","Agent"],
    "anime": ["二次元","动漫","番剧","虚拟","萌","动画","日漫","cosplay"],
    "funny": ["搞笑","整活","沙雕","表情包","吐槽","鬼畜","名场面","爆笑","离谱","抽象"],
    "luxury": ["评测","高端","旗舰","Pro","Max","豪华","奢华","开箱","体验","深度","测评"],
    "fresh": ["Vlog","生活","旅行","日常","治愈","清新","慢生活","记录","日常"],
    "gaming": ["游戏","电竞","对战","吃鸡","王者","原神","Steam","FPS","MOBA","通关","攻略"],
    "food": ["美食","探店","烹饪","吃","做饭","料理","烘焙","食谱","吃货","外卖"],
    "cinema": ["电影","影视","悬疑","恐怖","解说","剧情","惊悚","科幻","影评","拆解"],
    "cute": ["可爱","宠物","猫","狗","熊猫","狐狸","卡通","萌宠","治愈系","手帐","动物"],
    "paper": ["安利","推荐","攻略","评测","对比","排行","盘点","合集","总结","撕"],
    "variety": ["热点","事件","吃瓜","反转","震惊","绝了","崩溃","反应","名场面","弹幕"],
    "doodle": ["手帐","手绘","涂鸦","文创","日记","笔记","创意","DIY","手作","画"],
    "tech": ["AI","Shell","API","代码","编程","程序","服务器","云","IDE","CLI","Key","密钥","模型","Ollama","qwen","GPT"],
    "hot": ["教程","入门","实战","安装","部署","上线","新手","快速"],
    "cool": ["Docker","容器","MySQL","Redis","数据库","缓存","Portainer","Nginx"],
    "warm": ["对话","客服","设计","生活","沟通","SSE","流式"],
    "dark": ["安全","黑客","高级","硬核","渗透","密码"],
    "gradient": ["时尚","创意","爆款","热门","推荐"],
    "animal": ["萌","可爱","治愈","动物","宠物","猫","狗","熊猫","狐狸","卡通"],
    "paper": ["安利","推荐","攻略","评测","对比","排行","盘点","合集","撕","拼贴"],
    "variety": ["热点","吃瓜","反转","震惊","弹幕","名场面","反应","绝了"],
    "doodle": ["手帐","手绘","涂鸦","文创","笔记","创意","DIY","手作"],
}

THEME_EMOJIS = {
    "bold": [("1f4a1","💡"),("2b50","⭐"),("1f3af","🎯"),("1f4da","📚")],
    "cyber": [("1f680","🚀"),("26a1","⚡"),("1f4bb","💻"),("1f310","🌐"),("1f527","🔧"),("1f4e1","📡"),("1f916","🤖")],
    "anime": [("1f31f","🌟"),("2728","✨"),("1f4ab","💫"),("1f308","🌈"),("1f496","💖")],
    "funny": [("1f602","😂"),("1f44c","👌"),("1f923","🤣"),("1f644","🙄"),("1f4a5","💥"),("1f389","🎉")],
    "luxury": [("1f451","👑"),("1f48e","💎"),("1f576","🕶️"),("1f3a9","🎩")],
    "fresh": [("1f343","🍃"),("2600","☀️"),("1f33b","🌻"),("1f4ab","💫"),("1f319","🌙")],
    "gaming": [("1f3ae","🎮"),("1f476","👶"),("1f3c6","🏆"),("1f525","🔥"),("26a1","⚡"),("1f4a5","💥")],
    "food": [("1f371","🍱"),("1f35a","🍚"),("1f35c","🍜"),("1f36a","🍪"),("1f37a","🍺"),("1f36d","🍬")],
    "cinema": [("1f3ac","🎬"),("1f39e","🎞️"),("1f4f7","📷"),("1f3a4","🎤"),("1f4fd","📽️")],
    "cute": [("1f431","🐱"),("1f436","🐶"),("1f98a","🦊"),("1f43c","🐼"),("1f428","🐨"),("1f42f","🐯"),("1f981","🦁"),("1f438","🐸"),("1f419","🐙"),("1f989","🦉"),("1f984","🦄"),("1f41d","🐝"),("1f98b","🦋")],
    "paper": [("2702","✂️"),("1f4c4","📄"),("1f4dd","📝"),("1f3af","🎯"),("2753","❓"),("2764","❤️"),("1f525","🔥")],
    "variety": [("1f4ac","💬"),("1f631","😱"),("1f62d","😭"),("1f60d","😍"),("1f633","😳"),("1f44f","👏"),("1f525","🔥"),("1f4a5","💥")],
    "doodle": [("1f58d","🖍️"),("270f","✏️"),("1f4d0","📐"),("1f3a8","🎨"),("2b50","⭐"),("1f4ab","💫"),("1f388","🎈")],
    "tech": [("1f680","🚀"),("26a1","⚡"),("1f4bb","💻"),("1f310","🌐"),("1f527","🔧"),("1f4e1","📡")],
    "hot": [("1f525","🔥"),("2b50","⭐"),("1f4a5","💥"),("1f3af","🎯"),("1f389","🎉")],
    "cool": [("1f433","🐳"),("1f4e6","📦"),("1f5c3","🗄️"),("1f510","🔐"),("1f4be","💾")],
    "warm": [("1f49b","💛"),("1f4ac","💬"),("1f917","🤗"),("1f4f1","📱"),("2728","✨")],
    "dark": [("1f576","🕶️"),("1f512","🔒"),("1f480","💀"),("1f451","👑"),("1f9e0","🧠")],
    "gradient": [("2728","✨"),("1f308","🌈"),("1f4ab","💫"),("1f31f","🌟"),("1f48e","💎")],
    "animal": [("1f431","🐱"),("1f436","🐶"),("1f98a","🦊"),("1f43c","🐼"),("1f428","🐨"),("1f42f","🐯"),("1f981","🦁"),("1f438","🐸"),("1f419","🐙"),("1f989","🦉"),("1f984","🦄"),("1f41d","🐝"),("1f98b","🦋")],
}

GENERAL_EMOJIS = [("1f680","🚀"),("26a1","⚡"),("1f4bb","💻"),("1f310","🌐"),
                  ("1f525","🔥"),("2b50","⭐"),("2728","✨"),("1f4a1","💡"),
                  ("1f3af","🎯"),("1f389","🎉"),("1f4aa","💪")]

TWEMOJI_CDN = "https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/svg"

# ========== Iconfont 本地卡通素材 ==========
ICONFONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "iconfont")

# 风格 → iconfont 分类映射
THEME_ICONFONT_MAP = {
    "cute":     "animal",   # 萌宠风格用动物卡通
    "animal":   "animal",
    "funny":    "animal",   # 搞笑风格也用动物增加趣味
    "cyber":    "coder",    # 赛博/科技用程序员图标
    "tech":     "tech",      # 科技用科技图标
    "bold":     "coder",     # 大字醒目用程序员图标（知识区）
    "gaming":   "tech",      # 游戏用科技图标
    "dark":     "coder",     # 黑暗风用黑客/代码图标
    "food":     "food",      # 美食用食物图标
    "fresh":    "animal",    # 清新用动物
    "doodle":   "emoji",     # 手绘用表情
    "variety":  "emoji",     # 综艺弹幕用表情
    "anime":    "animal",    # 二次元用动物
    "luxury":   "tech",      # 奢华用科技/芯片
    "cinema":   "tech",      # 影视用科技
    "paper":    "coder",     # 撕纸用代码
    "hot":      "tech",      # 热门用火箭等
    "cool":     "coder",     # 极客用服务器
    "warm":     "animal",    # 温暖用动物
    "gradient": "animal",    # 渐变用动物
}

def get_iconfont_svgs(theme, count=2):
    """根据风格返回本地 iconfont SVG 文件路径列表"""
    category = THEME_ICONFONT_MAP.get(theme, "tech")
    cat_dir = os.path.join(ICONFONT_DIR, category)
    if not os.path.isdir(cat_dir):
        return []
    svgs = [f for f in sorted(os.listdir(cat_dir)) if f.endswith('.svg')]
    if not svgs:
        return []
    # 根据主题名做简单 hash 来选择不同图标，保证同主题每次一致
    seed = sum(ord(c) for c in theme)
    start = seed % max(1, len(svgs) - count)
    result = []
    for i in range(count):
        idx = (start + i) % len(svgs)
        result.append(os.path.join(cat_dir, svgs[idx]))
    return result

def svg_to_data_uri(filepath):
    """将 SVG 文件转为 data URI 用于内联嵌入 HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            svg_content = f.read().strip()
        # URL encode the SVG
        import urllib.parse
        encoded = urllib.parse.quote(svg_content, safe='')
        return f"data:image/svg+xml,{encoded}"
    except Exception:
        return None


def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) != 6: return "255,255,255"
    return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"


def detect_theme(title, tags=None):
    text = ((title or "") + " " + (tags and " ".join(tags) or "")).lower()
    for theme in ["bold","cyber","anime","funny","luxury","fresh","gaming","food","cinema","cute","paper","variety","doodle"]:
        kws = THEME_KEYWORDS.get(theme, [])
        if any(kw.lower() in text for kw in kws):
            return theme
    for theme in ["tech","hot","cool","warm","dark","gradient","animal"]:
        kws = THEME_KEYWORDS.get(theme, [])
        if any(kw.lower() in text for kw in kws):
            return theme
    return "cyber"


def get_scheme_by_theme(theme, idx=0):
    ss = [k for k,v in COLOR_SCHEMES.items() if v["theme"]==theme]
    if not ss: ss = [k for k,v in COLOR_SCHEMES.items() if v["theme"] in ("cyber","tech")]
    return ss[idx % len(ss)] if ss else "cyber_1"


def get_emojis(theme, idx=0):
    em = THEME_EMOJIS.get(theme, GENERAL_EMOJIS)
    s = idx * 2
    e1 = em[s % len(em)]
    e2 = em[(s+1) % len(em)]
    if len(em) < 2:
        e1 = GENERAL_EMOJIS[idx % len(GENERAL_EMOJIS)]
        e2 = GENERAL_EMOJIS[(idx+5) % len(GENERAL_EMOJIS)]
    return e1, e2


def get_decoration_assets(theme, idx=0):
    """获取装饰素材：优先使用 iconfont 本地 SVG，fallback 到 Twemoji"""
    iconfont_svgs = get_iconfont_svgs(theme, count=2)
    assets = []
    for svg_path in iconfont_svgs:
        data_uri = svg_to_data_uri(svg_path)
        if data_uri:
            # 从文件名提取友好显示名称（去掉数字ID，只保留中文部分）
            raw = os.path.basename(svg_path).replace('.svg', '')
            # 去掉下划线后的数字ID部分，如 "键盘_5387387" → "键盘"
            import re
            friendly = re.sub(r'[_-]?\d+$', '', raw)  # 去掉末尾数字ID
            friendly = re.sub(r'[_-]\d+$', '', friendly)  # 再试一次
            # 如果还是太长或含英文ID，用风格对应的emoji代替
            if len(friendly) > 6 or re.match(r'^[a-zA-Z]', friendly):
                friendly = ''  # 标记为不显示文字
            assets.append((data_uri, friendly))
    
    # 如果 iconfont 不够，补充 Twemoji
    if len(assets) < 2:
        e1, e2 = get_emojis(theme, idx)
        tw_cdn = TWEMOJI_CDN
        while len(assets) < 2:
            if len(assets) == 0:
                assets.append((f"{tw_cdn}/{e1[0]}.svg", e1[1]))
            else:
                assets.append((f"{tw_cdn}/{e2[0]}.svg", e2[1]))
    
    return assets[:2]


# ========== 差异化高亮处理 ==========
def apply_highlights(title, highlights, theme, a1, a2):
    """根据主题风格，用不同方式处理高亮关键词"""
    dt = title
    for i, w in enumerate(highlights):
        if not w: continue
        c = a1 if i%2==0 else a2
        if theme == "bold":
            # 大字风：黄色背景框 + 黑色文字，像荧光笔划过
            dt = dt.replace(w, f'<span class="hl-bold" style="background:{c};color:#000;padding:0 8px;border-radius:4px;">{w}</span>')
        elif theme == "cyber":
            # 赛博风：霓虹发光 + 颜色填充
            dt = dt.replace(w, f'<span class="hl-cyber" style="color:{c};text-shadow:0 0 10px {c},0 0 20px {c},0 0 40px {c};">{w}</span>')
        elif theme == "anime":
            # 二次元：描边 + 倾斜
            dt = dt.replace(w, f'<span class="hl-anime" style="color:{c};-webkit-text-stroke:2px #fff;text-stroke:2px #fff;transform:rotate(-2deg);">{w}</span>')
        elif theme == "funny":
            # 搞笑：大小不一 + 旋转 + 下划线
            rot = -8 if i%2==0 else 8
            sz = 1.2 if i%2==0 else 0.9
            dt = dt.replace(w, f'<span class="hl-funny" style="color:{c};transform:rotate({rot}deg) scale({sz});text-decoration:underline wavy {c};">{w}</span>')
        elif theme == "luxury":
            # 奢华：金色 + 上边框装饰线
            dt = dt.replace(w, f'<span class="hl-luxury" style="color:{c};border-top:2px solid {c};border-bottom:2px solid {c};padding:2px 6px;">{w}</span>')
        elif theme == "fresh":
            # 清新：下划波浪线 + 颜色
            dt = dt.replace(w, f'<span class="hl-fresh" style="color:{c};border-bottom:3px wavy {c};">{w}</span>')
        elif theme == "gaming":
            # 游戏：斜切 + 发光
            dt = dt.replace(w, f'<span class="hl-gaming" style="color:{c};text-shadow:0 0 8px {c},2px 2px 0 #000;transform:skewX(-5deg);display:inline-block;">{w}</span>')
        elif theme == "food":
            # 美食：圆角背景 + 手写感
            dt = dt.replace(w, f'<span class="hl-food" style="background:rgba({hex_to_rgb(c)},0.2);color:{c};padding:2px 10px;border-radius:20px;">{w}</span>')
        elif theme == "cinema":
            # 影视：底部粗线 + 字间距
            dt = dt.replace(w, f'<span class="hl-cinema" style="color:{c};border-bottom:4px solid {c};letter-spacing:4px;padding-bottom:2px;">{w}</span>')
        elif theme == "cute":
            # 萌宠：气泡背景 + 圆角
            dt = dt.replace(w, f'<span class="hl-cute" style="background:{c};color:#fff;padding:2px 12px;border-radius:50px;transform:rotate(-3deg);display:inline-block;">{w}</span>')
        elif theme == "paper":
            # 撕纸拼贴：不规则边框 + 阴影 + 旋转
            rot = -3 if i%2==0 else 3
            dt = dt.replace(w, f'<span class="hl-paper" style="background:{c};color:#fff;padding:4px 12px;clip-path:polygon(2% 0,98% 0,100% 50%,98% 100%,2% 100%,0 50%);transform:rotate({rot}deg);display:inline-block;box-shadow:3px 3px 0 rgba(0,0,0,0.3);">{w}</span>')
        elif theme == "variety":
            # 综艺弹幕：花字效果 + 多层描边 + 旋转
            rot = -4 if i%2==0 else 4
            dt = dt.replace(w, f'<span class="hl-variety" style="color:{c};-webkit-text-stroke:3px #000;text-stroke:3px #000;transform:rotate({rot}deg) scale(1.15);display:inline-block;filter:drop-shadow(2px 2px 0 #000);">{w}</span>')
        elif theme == "doodle":
            # 手绘涂鸦：手写体 + 波浪下划线 + 圆圈标注
            dt = dt.replace(w, f'<span class="hl-doodle" style="color:{c};border-bottom:3px dashed {c};text-decoration:none;position:relative;display:inline-block;">{w}<span style="position:absolute;top:-6px;left:-4px;right:-4px;bottom:-6px;border:2px solid {c};border-radius:8px;opacity:0.4;pointer-events:none;"></span></span>')
        else:
            dt = dt.replace(w, f'<span class="highlight" style="color:{c};">{w}</span>')
    return dt


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
    text_color = sc.get("text_color", "#ffffff")

    # 获取装饰素材（优先 iconfont 本地 SVG，fallback Twemoji）
    deco_assets = get_decoration_assets(theme, index)
    (da1_url, da1_name), (da2_url, da2_name) = deco_assets[0], deco_assets[1] if len(deco_assets) > 1 else (deco_assets[0][0], deco_assets[0][0])

    dt = apply_highlights(title, highlights, theme, a1, a2)

    th = ""
    for i, t in enumerate(tags):
        tc = [a1,a2,a1,a2][i%4]
        op = 0.25 if i%2==0 else 0.20
        th += f'        <span class="cv-tag" style="background:rgba({hex_to_rgb(tc)},{op});color:{tc};">{t}</span>\n'

    ts, ss = pf["title_size"], pf["subtitle_size"]
    es1, es2 = int(ts*1.3), int(ts*1.0)  # iconfont 图标可以更大一些

    # ===== 大卡通角色元素 =====
    # 根据 iconfont SVG 生成大卡通角色（占封面 30-40% 面积）
    mascot_url = da1_url
    mascot_name = da1_name
    # 大卡通尺寸：根据平台调整
    mw = int(pf["width"] * 0.32)  # 宽度占封面32%
    mh = mw  # 正方形
    mascot_right = int(pf["width"] * 0.03)  # 右边距
    mascot_bottom = int(pf["height"] * 0.05)  # 底部距
    mascot_opacity = 0.18  # 大卡通半透明背景装饰
    mascot_solid_opacity = 0.92  # 实体卡通的不透明度

    # 获取风格对应的友好 emoji（用于 badge 和底部栏，替代文件名）
    theme_emoji = THEME_EMOJIS.get(theme, THEME_EMOJIS.get("cyber", []))
    badge_emoji = theme_emoji[index % len(theme_emoji)][1] if theme_emoji else ""
    bar_emoji = theme_emoji[(index+1) % len(theme_emoji)][1] if theme_emoji else ""

    return f'''<div class="cover-card cover-{pf_key} theme-{theme}" data-platform="{pf['name']}" data-index="{index+1}" style="--bg-color:{bg};--accent1:{a1};--accent2:{a2};--text-color:{text_color};">
  <div class="cv-bg-decoration">
    <div class="cv-bg-circle" style="width:{350+index*20}px;height:{350+index*20}px;background:{a1};top:-{80+index*10}px;left:-{80+index*10}px;"></div>
    <div class="cv-bg-circle" style="width:{260+index*15}px;height:{260+index*15}px;background:{a2};bottom:-60px;right:-60px;"></div>
    <!-- 大卡通角色：半透明背景装饰 -->
    <img class="cv-mascot-bg" src="{mascot_url}" alt="" style="position:absolute;right:{mascot_right}px;bottom:{mascot_bottom}px;width:{mw}px;height:{mh}px;opacity:{mascot_opacity};z-index:0;filter:blur(1px);" onerror="this.style.display='none'">
    <!-- 小装饰图标：左上角 -->
    <img class="cv-emoji-deco cv-emoji-1 cv-iconfont-deco" src="{da1_url}" alt="" style="top:{12+index*3}%;left:4%;width:{es1}px;height:{es1}px;filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.15));" onerror="this.style.display='none'">
    <img class="cv-emoji-deco cv-emoji-2 cv-iconfont-deco" src="{da2_url}" alt="" style="bottom:{10+index*3}%;right:5%;width:{es2}px;height:{es2}px;filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.15));" onerror="this.style.display='none'">
  </div>
  <!-- 大卡通角色：实体（右侧） -->
  <img class="cv-mascot" src="{mascot_url}" alt="" onerror="this.style.display='none'">
  <div class="cv-content">
    <div class="cv-badge" style="background:rgba({hex_to_rgb(a1)},0.2);color:{a1};border:1px solid rgba({hex_to_rgb(a1)},0.4);">{badge_emoji} {badge}</div>
    <div class="cv-main-title" style="font-size:{ts}px;color:{text_color};">{dt}</div>
    <div class="cv-sub-title" style="font-size:{ss}px;color:{text_color};">{subtitle}</div>
    <div class="cv-tag-row">
{th}    </div>
  </div>
  <div class="cv-bottom-bar"><span>{bar_emoji} {quote}</span><span>{pf['name']} · {index+1}</span></div>
</div>'''


# ========== 差异化字体排版CSS ==========
THEME_FONT_CSS = """
/* ===== iconfont 卡通装饰图标增强 ===== */
.cv-iconfont-deco { opacity: 0.85; transition: transform 0.3s ease; z-index: 1; }
.cover-card:hover .cv-iconfont-deco { transform: scale(1.08) rotate(3deg); }
.theme-cute .cv-iconfont-deco,
.theme-animal .cv-iconfont-deco,
.theme-fresh .cv-iconfont-deco { opacity: 0.95; filter: drop-shadow(3px 3px 6px rgba(0,0,0,0.18)) !important; }
.theme-funny .cv-iconfont-deco { animation: icon-bounce 3s ease-in-out infinite; }
@keyframes icon-bounce { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-8px); } }

/* ===== 大卡通角色（Mascot） ===== */
.cv-mascot {
  position: absolute;
  right: 2%;
  bottom: 8%;
  width: 28%;
  height: auto;
  z-index: 2;
  opacity: 0.85;
  filter: drop-shadow(4px 4px 8px rgba(0,0,0,0.25));
  transition: transform 0.4s ease, opacity 0.3s ease;
  pointer-events: none;
}
.cover-card:hover .cv-mascot {
  transform: scale(1.05) rotate(-2deg);
  opacity: 1;
}
/* 竖版封面：卡通角色放底部居中 */
.cover-wechat .cv-mascot,
.cover-mobile .cv-mascot {
  right: auto;
  left: 50%;
  transform: translateX(-50%);
  bottom: 8%;
  width: 28%;
}
.cover-wechat:hover .cv-mascot,
.cover-mobile:hover .cv-mascot {
  transform: translateX(-50%) scale(1.05) rotate(-2deg);
}
/* 小红书：卡通角色右下角稍小 */
.cover-xiaohongshu .cv-mascot {
  width: 26%;
  bottom: 10%;
}
/* 各风格卡通角色差异化 */
.theme-cute .cv-mascot,
.theme-animal .cv-mascot { opacity: 1; filter: drop-shadow(3px 3px 6px rgba(0,0,0,0.2)); }
.theme-funny .cv-mascot { animation: mascot-wobble 4s ease-in-out infinite; }
@keyframes mascot-wobble { 0%,100%{transform:rotate(0deg);} 25%{transform:rotate(3deg);} 75%{transform:rotate(-3deg);} }
.theme-cyber .cv-mascot { filter: drop-shadow(0 0 12px var(--accent1)) drop-shadow(0 0 24px var(--accent2)); opacity: 0.85; }
.theme-bold .cv-mascot { opacity: 0.75; }
.theme-luxury .cv-mascot { filter: drop-shadow(0 0 8px rgba(212,175,55,0.4)); opacity: 0.8; }
.theme-gaming .cv-mascot { filter: drop-shadow(0 0 10px var(--accent1)) brightness(1.1); }
.theme-food .cv-mascot { opacity: 0.95; }
.theme-fresh .cv-mascot { opacity: 0.9; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1)); }
.theme-paper .cv-mascot { transform: rotate(-5deg); filter: drop-shadow(3px 3px 0 rgba(0,0,0,0.2)); }
.theme-variety .cv-mascot { animation: mascot-pop 2s ease-in-out infinite; }
@keyframes mascot-pop { 0%,100%{transform:scale(1);} 50%{transform:scale(1.06);} }
.theme-doodle .cv-mascot { filter: drop-shadow(2px 2px 0 #000); opacity: 0.88; }

/* ===== bold: 大字醒目风 v3.2 描边增强 ===== */
.theme-bold .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.05; text-shadow: none; -webkit-text-stroke: 1px rgba(0,0,0,0.1); }
.theme-bold .cv-main-title .hl-bold { display: inline; transform: none; }
.theme-bold .cv-badge { border-radius: 0; border: 2px solid currentColor; background: transparent; }
.theme-bold .cv-content { align-items: center; text-align: center; }
.theme-bold .cv-content::after { content: '→'; position: absolute; bottom: 50px; right: 40px; font-size: 48px; color: var(--accent2); opacity: 0.3; font-weight: 900; }

/* ===== cyber: 赛博朋克风 v3.2 网格线增强 ===== */
.theme-cyber .cv-main-title { font-weight: 900; letter-spacing: 4px; line-height: 1.1; text-shadow: 0 0 15px rgba(0,255,255,0.3); }
.theme-cyber .cv-main-title .hl-cyber { display: inline-block; }
.theme-cyber .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background:
    repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,255,255,0.04) 3px, rgba(0,255,255,0.04) 4px),
    repeating-linear-gradient(90deg, transparent, transparent 40px, rgba(255,0,255,0.06) 40px, rgba(255,0,255,0.06) 41px);
  pointer-events: none;
}
.theme-cyber .cv-badge { border-radius: 0; clip-path: polygon(0 0, 100% 0, 95% 100%, 0 100%); }
.theme-cyber .cv-content::before { content: '>_'; position: absolute; top: 20px; left: 30px; font-family: 'SF Mono',Monaco,monospace; font-size: 20px; color: var(--accent1); opacity: 0.4; }

/* ===== anime: 二次元动漫风 ===== */
.theme-anime .cv-main-title { font-weight: 800; letter-spacing: 3px; line-height: 1.15; }
.theme-anime .cv-main-title .hl-anime { display: inline-block; }
.theme-anime .cv-badge { border-radius: 25px; }
.theme-anime .cv-tag { border-radius: 25px; }

/* ===== funny: 搞笑整活风 v3.2 混乱表情增强 ===== */
.theme-funny .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.2; }
.theme-funny .cv-main-title .hl-funny { display: inline-block; }
.theme-funny .cv-badge { border-radius: 0; transform: rotate(-3deg); }
.theme-funny .cv-tag { transform: rotate(2deg); }
.theme-funny .cv-emoji-deco { opacity: 0.18 !important; transform: rotate(15deg); }
.theme-funny .cv-content::before { content: '？？？'; position: absolute; top: 10px; right: 30px; font-size: 36px; font-weight: 900; color: var(--accent1); opacity: 0.25; transform: rotate(-10deg); }

/* ===== luxury: 黑金奢华风 ===== */
.theme-luxury .cv-main-title { font-weight: 700; letter-spacing: 6px; line-height: 1.1; text-shadow: 0 2px 8px rgba(212,175,55,0.3); }
.theme-luxury .cv-main-title .hl-luxury { display: inline-block; }
.theme-luxury .cv-badge { border-radius: 0; border: 1px solid currentColor; background: transparent; letter-spacing: 3px; }
.theme-luxury .cv-content::before {
  content: ''; position: absolute; top: 20px; left: 20px; right: 20px; bottom: 20px;
  border: 1px solid rgba(212,175,55,0.2); pointer-events: none; z-index: 1;
}
.theme-luxury .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; }

/* ===== fresh: 清新治愈风 ===== */
.theme-fresh .cv-main-title { font-weight: 600; letter-spacing: 2px; line-height: 1.2; text-shadow: none; }
.theme-fresh .cv-main-title .hl-fresh { display: inline; }
.theme-fresh .cv-badge { border-radius: 20px; font-weight: 500; }
.theme-fresh .cv-tag { border-radius: 20px; font-weight: 500; }
.theme-fresh .cv-sub-title { font-weight: 400; }

/* ===== gaming: 游戏电竞风 ===== */
.theme-gaming .cv-main-title { font-weight: 900; letter-spacing: 1px; line-height: 1.05; text-shadow: 2px 2px 0 #000, 0 0 15px rgba(255,255,255,0.2); }
.theme-gaming .cv-main-title .hl-gaming { display: inline-block; }
.theme-gaming .cv-badge { clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%); border: none; }
.theme-gaming .cv-content { align-items: center; text-align: center; }
.theme-gaming .cv-bg-decoration::after {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, var(--accent1), var(--accent2), var(--accent1));
  z-index: 3;
}

/* ===== food: 美食暖调风 ===== */
.theme-food .cv-main-title { font-weight: 800; letter-spacing: 2px; line-height: 1.1; }
.theme-food .cv-main-title .hl-food { display: inline-block; }
.theme-food .cv-badge { border-radius: 50px; }
.theme-food .cv-bg-circle { filter: blur(20px); opacity: 0.12; }

/* ===== cinema: 影视悬疑风 v3.2 电影黑边增强 ===== */
.theme-cinema .cv-main-title { font-weight: 700; letter-spacing: 5px; line-height: 1.1; text-shadow: 0 0 20px rgba(0,0,0,0.8); }
.theme-cinema .cv-main-title .hl-cinema { display: inline-block; }
.theme-cinema .cv-content::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 50px;
  background: linear-gradient(180deg, rgba(0,0,0,0.8), transparent); z-index: 3; pointer-events: none;
}
.theme-cinema .cv-content::after {
  content: ''; position: absolute; bottom: 36px; left: 0; right: 0; height: 50px;
  background: linear-gradient(0deg, rgba(0,0,0,0.8), transparent); z-index: 3; pointer-events: none;
}
.theme-cinema .cv-badge { border-radius: 0; background: transparent; border-left: 3px solid currentColor; padding-left: 12px; }
.theme-cinema .cv-bottom-bar { letter-spacing: 3px; }

/* ===== cute: 萌宠可爱风 ===== */
.theme-cute .cv-main-title { font-weight: 800; letter-spacing: 1px; line-height: 1.15; text-shadow: 2px 2px 0 rgba(255,255,255,0.5); }
.theme-cute .cv-main-title .hl-cute { display: inline-block; }
.theme-cute .cv-badge { border-radius: 50px; }
.theme-cute .cv-tag { border-radius: 50px; }
.theme-cute .cv-bg-circle { filter: blur(15px); opacity: 0.15; }

/* ===== 兼容旧主题 ===== */
.theme-tech .cv-main-title { font-weight: 900; letter-spacing: 2px; line-height: 1.08; text-shadow: 0 4px 20px rgba(0,0,0,.4); }
.theme-hot .cv-main-title { font-weight: 900; letter-spacing: 2px; line-height: 1.08; }
.theme-cool .cv-main-title { font-weight: 900; letter-spacing: 2px; line-height: 1.08; }
.theme-warm .cv-main-title { font-weight: 700; letter-spacing: 2px; line-height: 1.1; }
.theme-dark .cv-main-title { font-weight: 900; letter-spacing: 3px; line-height: 1.1; }
.theme-gradient .cv-main-title { font-weight: 900; letter-spacing: 2px; line-height: 1.08; }
.theme-animal .cv-main-title { font-weight: 800; letter-spacing: 1px; line-height: 1.12; }

/* ===== 11. paper: 撕纸拼贴风 ===== */
.theme-paper .cv-main-title { font-weight: 900; letter-spacing: 1px; line-height: 1.1; text-shadow: 2px 2px 0 rgba(0,0,0,0.15); }
.theme-paper .cv-main-title .hl-paper { display: inline-block; }
.theme-paper .cv-badge { border-radius: 0; clip-path: polygon(2% 0, 98% 0, 100% 50%, 98% 100%, 2% 100%, 0 50%); border: none; }
.theme-paper .cv-tag { clip-path: polygon(3% 0, 97% 0, 100% 50%, 97% 100%, 3% 100%, 0 50%); border: none; }
.theme-paper .cv-content { align-items: center; text-align: center; }
.theme-paper .cv-bg-decoration::after {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(0,0,0,0.02) 20px, rgba(0,0,0,0.02) 21px);
  pointer-events: none;
}
.theme-paper .cv-bg-circle { filter: blur(8px); opacity: 0.1; }

/* ===== 12. variety: 综艺弹幕风 ===== */
.theme-variety .cv-main-title { font-weight: 900; letter-spacing: 2px; line-height: 1.15; -webkit-text-stroke: 1px rgba(0,0,0,0.3); }
.theme-variety .cv-main-title .hl-variety { display: inline-block; }
.theme-variety .cv-badge { border-radius: 0; border: 3px solid currentColor; background: rgba(0,0,0,0.3); transform: rotate(-2deg); }
.theme-variety .cv-tag { border-radius: 0; border: 2px solid currentColor; background: rgba(0,0,0,0.2); transform: rotate(1deg); }
.theme-variety .cv-bg-decoration::before {
  content: '🔥 HOT'; position: absolute; top: 15px; right: 20px; z-index: 1;
  font-size: 14px; font-weight: 900; color: var(--accent1); opacity: 0.3;
  transform: rotate(15deg); letter-spacing: 2px;
}
.theme-variety .cv-emoji-deco { opacity: 0.2 !important; }

/* ===== 13. doodle: 手绘涂鸦风 ===== */
.theme-doodle .cv-main-title { font-weight: 700; letter-spacing: 1px; line-height: 1.2; font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; text-shadow: none; }
.theme-doodle .cv-main-title .hl-doodle { display: inline-block; }
.theme-doodle .cv-badge { border-radius: 20px; border: 2px dashed currentColor; background: transparent; }
.theme-doodle .cv-tag { border-radius: 16px; border: 2px dashed currentColor; background: transparent; }
.theme-doodle .cv-bg-decoration::after {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(circle at 15% 20%, var(--accent1) 1.5px, transparent 2px),
    radial-gradient(circle at 85% 80%, var(--accent2) 1.5px, transparent 2px),
    radial-gradient(circle at 50% 50%, var(--accent1) 1px, transparent 1.5px);
  background-size: 60px 60px, 80px 80px, 40px 40px;
  opacity: 0.08; pointer-events: none;
}
.theme-doodle .cv-bg-circle { border-style: dashed; }
"""


def generate_full_html(covers, platform="bilibili", theme="auto"):
    pks = ["bilibili","xiaohongshu","wechat","mobile"] if platform == "all" else [platform]

    slides = []
    thumbs = []
    total = len(pks) * len(covers)
    si = 0

    for pk in pks:
        pf = PLATFORMS[pk]
        for ci, c in enumerate(covers):
            si += 1
            first = si == 1
            t = c.get("title", f"{pf['name']}{ci+1}")
            label = pf.get("icon","📄") + " " + pf["name"]

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
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800;900&family=ZCOOL+KuaiLe&family=Ma+Shan+Zheng&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}

body{{
  font-family:'Noto Sans SC',-apple-system,BlinkMacSystemFont,sans-serif;
  background:#0d1117;
  display:flex;flex-direction:column;
  height:100vh;width:100vw;overflow:hidden;
}}

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

.stage{{
  flex:1;display:flex;align-items:center;justify-content:center;
  padding:20px 40px;overflow:hidden;position:relative;
}}
.slide{{display:none;width:100%;height:100%;align-items:center;justify-content:center;animation:slideIn .3s ease;}}
.slide.active{{display:flex;}}
@keyframes slideIn{{from{{opacity:0;transform:scale(.96)}}to{{opacity:1;transform:scale(1)}}}}

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
  font-size:14px;font-weight:700;letter-spacing:1px;margin-bottom:16px;margin-left:auto;margin-right:auto;
}}
.cv-main-title{{
  font-weight:900;line-height:1.08;letter-spacing:2px;margin-bottom:10px;
  text-shadow:0 4px 20px rgba(0,0,0,.4);max-width:88%;margin-left:auto;margin-right:auto;text-align:center;color:var(--text-color,#fff);
}}
.cv-main-title .highlight{{display:inline-block;transform:rotate(-3deg);text-shadow:none;}}
.cv-sub-title{{font-weight:600;margin-bottom:16px;letter-spacing:1px;max-width:82%;margin-left:auto;margin-right:auto;text-align:center;color:var(--text-color,#fff);opacity:0.8;}}
.cv-tag-row{{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:14px;max-width:88%;margin-left:auto;margin-right:auto;}}
.cv-tag{{padding:6px 18px;border-radius:16px;font-size:15px;font-weight:700;letter-spacing:.5px;}}
.cv-emoji-deco{{position:absolute;opacity:.10;z-index:1;object-fit:contain;}}
.cv-bottom-bar{{
  position:absolute;bottom:0;left:0;right:0;height:36px;
  background:rgba(0,0,0,.35);backdrop-filter:blur(4px);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 28px;font-size:13px;color:rgba(255,255,255,.5);z-index:4;
}}

/* 平台适配 */
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

/* 浅色背景适配 */
.cover-card[style*="#fff"] .cv-bottom-bar,
.cover-card[style*="#fbbf24"] .cv-bottom-bar,
.cover-card[style*="#e0f2fe"] .cv-bottom-bar,
.cover-card[style*="#f0fdf4"] .cv-bottom-bar,
.cover-card[style*="#fefce8"] .cv-bottom-bar,
.cover-card[style*="#fff7ed"] .cv-bottom-bar,
.cover-card[style*="#fdf2f8"] .cv-bottom-bar,
.cover-card[style*="#ecfeff"] .cv-bottom-bar,
.cover-card[style*="#fff0f5"] .cv-bottom-bar,
.cover-card[style*="#fef3c7"] .cv-bottom-bar{{
  background:rgba(0,0,0,.12);color:rgba(0,0,0,.4);
}}

/* ===== 差异化字体排版 ===== */
{THEME_FONT_CSS}

/* 萌宠可爱风用手写字体 */
.theme-cute .cv-main-title {{ font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; }}
.theme-fresh .cv-main-title {{ font-family: 'Ma Shan Zheng', 'Noto Sans SC', sans-serif; font-weight: 400; }}
.theme-anime .cv-main-title {{ font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; }}
.theme-doodle .cv-main-title {{ font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; }}

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

<div class="topbar">
  <span class="topbar-title">视频封面预览</span>
  <span class="topbar-page"><span id="curPage">1</span> / {total}</span>
</div>

<div class="stage">
{slide_html}
</div>

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
    all_themes = ["auto","bold","cyber","anime","funny","luxury","fresh","gaming","food","cinema","cute","paper","variety","doodle",
                  "tech","hot","cool","warm","dark","gradient","animal"]
    p = argparse.ArgumentParser(
        description="视频封面生成器 v3.2 - 13大B站爆款风格 × 差异化字体排版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\n示例:\n"
               "  python3 generate_covers.py --title 'Docker一装，运维轻松10倍' --theme cyber\n"
               "  python3 generate_covers.py --title '给爷来个Key' --platform all --theme bold\n"
               "  python3 generate_covers.py --title '猫猫编程日记' --theme cute --platform all\n"
               "  python3 generate_covers.py --title '5款AI工具安利' --theme paper --platform all\n"
               "  python3 generate_covers.py --title '这反应绝了' --theme variety --platform all\n"
               "  python3 generate_covers.py --input ppt.html --output covers.html --platform all\n"
               "  python3 generate_covers.py --config covers.json\n\n"
               "B站爆款风格: bold/cyber/anime/funny/luxury/fresh/gaming/food/cinema/cute/paper/variety/doodle")
    p.add_argument("--input","-i")
    p.add_argument("--output","-o",default="video-covers.html")
    p.add_argument("--config","-c")
    p.add_argument("--platform","-p",default="bilibili",choices=["bilibili","xiaohongshu","wechat","mobile","all"])
    p.add_argument("--theme",default="auto",choices=all_themes)
    p.add_argument("--scheme",help="指定具体配色ID (如 bold_3, cyber_1, cute_2)")
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
        if a.scheme: cover["scheme"] = a.scheme
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
