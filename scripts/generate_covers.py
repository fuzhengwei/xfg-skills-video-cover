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

    # ===== 14. 杂志风（magazine）— 评测/深度/商业/高端 =====
    "magazine_1": {"bg": "#fafafa", "accent1": "#1a1a1a", "accent2": "#dc2626", "name": "黑白红杂志", "theme": "magazine", "text_color": "#1a1a1a"},
    "magazine_2": {"bg": "#0a0a0a", "accent1": "#ffffff", "accent2": "#dc2626", "name": "暗黑杂志", "theme": "magazine"},
    "magazine_3": {"bg": "#f5f5f0", "accent1": "#1e3a5f", "accent2": "#c9a96e", "name": "米色蓝金杂志", "theme": "magazine", "text_color": "#1e3a5f"},
    "magazine_4": {"bg": "#1e3a5f", "accent1": "#ffffff", "accent2": "#c9a96e", "name": "深蓝杂志", "theme": "magazine"},

    # ===== 15. 极简风（minimal）— 知识/科普/商务 =====
    "minimal_1": {"bg": "#ffffff", "accent1": "#000000", "accent2": "#3b82f6", "name": "纯黑白蓝", "theme": "minimal", "text_color": "#000000"},
    "minimal_2": {"bg": "#000000", "accent1": "#ffffff", "accent2": "#6b7280", "name": "暗夜极简", "theme": "minimal"},
    "minimal_3": {"bg": "#f8f8f8", "accent1": "#333333", "accent2": "#10b981", "name": "灰白绿极简", "theme": "minimal", "text_color": "#333333"},
    "minimal_4": {"bg": "#fafaf5", "accent1": "#1a1a1a", "accent2": "#f59e0b", "name": "米黄极简", "theme": "minimal", "text_color": "#1a1a1a"},

    # ===== 16. 多巴胺（dopamine）— 撞色/潮流/快乐 =====
    "dopamine_1": {"bg": "linear-gradient(135deg,#ff6b6b 0%,#feca57 50%,#48dbfb 100%)", "accent1": "#ffffff", "accent2": "#5f27cd", "name": "彩虹多巴胺", "theme": "dopamine", "is_gradient": True},
    "dopamine_2": {"bg": "#ff6b6b", "accent1": "#feca57", "accent2": "#48dbfb", "name": "红黄蓝多巴胺", "theme": "dopamine", "text_color": "#ffffff"},
    "dopamine_3": {"bg": "#a29bfe", "accent1": "#fd79a8", "accent2": "#fdcb6e", "name": "紫粉黄多巴胺", "theme": "dopamine"},
    "dopamine_4": {"bg": "linear-gradient(135deg,#00cec9 0%,#a29bfe 100%)", "accent1": "#ffffff", "accent2": "#e84393", "name": "青紫多巴胺", "theme": "dopamine", "is_gradient": True},

    # ===== 17. 国潮风（guochao）— 国风/传统/文化 =====
    "guochao_1": {"bg": "#8b0000", "accent1": "#ffd700", "accent2": "#ffffff", "name": "中国红金", "theme": "guochao"},
    "guochao_2": {"bg": "#1a1a2e", "accent1": "#e94560", "accent2": "#ffd700", "name": "暗夜国风", "theme": "guochao"},
    "guochao_3": {"bg": "#f5e6d3", "accent1": "#8b0000", "accent2": "#1a1a2e", "name": "宣纸红黑", "theme": "guochao", "text_color": "#1a1a2e"},
    "guochao_4": {"bg": "#0d2818", "accent1": "#d4af37", "accent2": "#e94560", "name": "墨绿国风", "theme": "guochao"},

    # ===== 18. 像素风（pixel）— 复古/游戏/极客 =====
    "pixel_1": {"bg": "#1a1a2e", "accent1": "#00ff41", "accent2": "#ff006e", "name": "像素霓虹", "theme": "pixel"},
    "pixel_2": {"bg": "#0a0a0a", "accent1": "#fbbf24", "accent2": "#3b82f6", "name": "像素金蓝", "theme": "pixel"},
    "pixel_3": {"bg": "#1e3a5f", "accent1": "#fbbf24", "accent2": "#ef4444", "name": "8bit红金蓝", "theme": "pixel"},
    "pixel_4": {"bg": "#2d1b69", "accent1": "#00ffff", "accent2": "#fbbf24", "name": "复古像素", "theme": "pixel"},

    # ===== 19. 手账风（journal）— 笔记/记录/手写 =====
    "journal_1": {"bg": "#fef3c7", "accent1": "#92400e", "accent2": "#dc2626", "name": "牛皮纸手账", "theme": "journal", "text_color": "#451a03"},
    "journal_2": {"bg": "#e0f2fe", "accent1": "#0c4a6e", "accent2": "#0ea5e9", "name": "方格纸手账", "theme": "journal", "text_color": "#0c4a6e"},
    "journal_3": {"bg": "#f0fdf4", "accent1": "#14532d", "accent2": "#16a34a", "name": "绿格手账", "theme": "journal", "text_color": "#14532d"},
    "journal_4": {"bg": "#fdf2f8", "accent1": "#831843", "accent2": "#ec4899", "name": "粉白手账", "theme": "journal", "text_color": "#831843"},
    # ===== 20. vaporwave 蒙汽波风 =====
    "vaporwave_1": {"bg": "linear-gradient(135deg,#ff6ec7,#7873f5)", "accent1": "#00ffff", "accent2": "#ff00ff", "name": "粉紫蒸汽波", "theme": "vaporwave"},
    "vaporwave_2": {"bg": "#1a0a2e", "accent1": "#ff6ec7", "accent2": "#00ffff", "name": "暗夜蒸汽波", "theme": "vaporwave"},
    "vaporwave_3": {"bg": "linear-gradient(180deg,#2d1b4e,#ff6ec7,#feca57)", "accent1": "#00ffff", "accent2": "#ff00ff", "name": "日落蒸汽波", "theme": "vaporwave"},
    "vaporwave_4": {"bg": "#0d0221", "accent1": "#d1009c", "accent2": "#00e5ff", "name": "深紫蒸汽波", "theme": "vaporwave"},
    # ===== 21. acid 酸性设计 =====
    "acid_1": {"bg": "#0a0a0a", "accent1": "#aaff00", "accent2": "#ff00aa", "name": "黑白酸", "theme": "acid"},
    "acid_2": {"bg": "#1a0033", "accent1": "#00ff88", "accent2": "#ff6600", "name": "紫绿酸", "theme": "acid"},
    "acid_3": {"bg": "#0d0d0d", "accent1": "#e6ff00", "accent2": "#ff006e", "name": "荧光酸", "theme": "acid"},
    "acid_4": {"bg": "linear-gradient(135deg,#0a0a0a,#1a0033)", "accent1": "#aaff00", "accent2": "#00e5ff", "name": "液态金属酸", "theme": "acid"},
    # ===== 22. memphis 孟菲斯风 =====
    "memphis_1": {"bg": "#fef3c7", "accent1": "#7c3aed", "accent2": "#ec4899", "name": "黄紫粉孟菲", "theme": "memphis", "text_color": "#1a1a2e"},
    "memphis_2": {"bg": "#e0f2fe", "accent1": "#f97316", "accent2": "#22c55e", "name": "蓝橙绿孟菲", "theme": "memphis", "text_color": "#1a1a2e"},
    "memphis_3": {"bg": "#fdf2f8", "accent1": "#0ea5e9", "accent2": "#fbbf24", "name": "粉蓝黄孟菲", "theme": "memphis", "text_color": "#1a1a2e"},
    "memphis_4": {"bg": "#f0fdf4", "accent1": "#dc2626", "accent2": "#7c3aed", "name": "绿红紫孟菲", "theme": "memphis", "text_color": "#1a1a2e"},
    # ===== 23. clay 黏土风 =====
    "clay_1": {"bg": "linear-gradient(135deg,#ffd6a5,#ff9aa2)", "accent1": "#6c5ce7", "accent2": "#fd79a8", "name": "暖粉黏土", "theme": "clay"},
    "clay_2": {"bg": "linear-gradient(135deg,#a8e6cf,#dcedc1)", "accent1": "#ff8b94", "accent2": "#aaa1c8", "name": "清爽黏土", "theme": "clay"},
    "clay_3": {"bg": "linear-gradient(135deg,#ffb5a7,#fcd5ce)", "accent1": "#a86a8e", "accent2": "#547aa5", "name": "柔和黏土", "theme": "clay"},
    "clay_4": {"bg": "linear-gradient(135deg,#b5eaea,#edf6e9)", "accent1": "#ff686b", "accent2": "#79bd9a", "name": "薄荷黏土", "theme": "clay"},
    # ===== 24. glass 玻璃拟态 =====
    "glass_1": {"bg": "linear-gradient(135deg,rgba(255,255,255,0.2),rgba(255,255,255,0.05))", "accent1": "#60a5fa", "accent2": "#a78bfa", "name": "蓝紫玻璃", "theme": "glass"},
    "glass_2": {"bg": "linear-gradient(135deg,rgba(34,197,94,0.15),rgba(59,130,246,0.1))", "accent1": "#22c55e", "accent2": "#3b82f6", "name": "青绿玻璃", "theme": "glass"},
    "glass_3": {"bg": "linear-gradient(135deg,rgba(236,72,153,0.15),rgba(168,85,247,0.1))", "accent1": "#ec4899", "accent2": "#a855f7", "name": "粉紫玻璃", "theme": "glass"},
    "glass_4": {"bg": "linear-gradient(135deg,rgba(251,191,36,0.15),rgba(239,68,68,0.1))", "accent1": "#fbbf24", "accent2": "#ef4444", "name": "金红玻璃", "theme": "glass"},
    # ===== 25. sticker 贴纸风 =====
    "sticker_1": {"bg": "#ffffff", "accent1": "#ff6b9d", "accent2": "#4ecdc4", "name": "白底彩贴纸", "theme": "sticker", "text_color": "#1a1a2e"},
    "sticker_2": {"bg": "#fef3c7", "accent1": "#f97316", "accent2": "#7c3aed", "name": "黄橙紫贴纸", "theme": "sticker", "text_color": "#1a1a2e"},
    "sticker_3": {"bg": "#e0f2fe", "accent1": "#0ea5e9", "accent2": "#ec4899", "name": "蓝粉贴纸", "theme": "sticker", "text_color": "#1a1a2e"},
    "sticker_4": {"bg": "#f0fdf4", "accent1": "#16a34a", "accent2": "#fbbf24", "name": "绿黄贴纸", "theme": "sticker", "text_color": "#1a1a2e"},
    # ===== 26. comic 漫画风 =====
    "comic_1": {"bg": "#fbbf24", "accent1": "#1a1a1a", "accent2": "#ef4444", "name": "黄金黑红漫画", "theme": "comic", "text_color": "#1a1a1a"},
    "comic_2": {"bg": "#ffffff", "accent1": "#1a1a1a", "accent2": "#2563eb", "name": "白底黑蓝漫画", "theme": "comic", "text_color": "#1a1a1a"},
    "comic_3": {"bg": "#ef4444", "accent1": "#ffffff", "accent2": "#1a1a1a", "name": "红白黑漫画", "theme": "comic"},
    "comic_4": {"bg": "#1a1a2e", "accent1": "#fbbf24", "accent2": "#ef4444", "name": "暗金红漫画", "theme": "comic"},
    # ===== 27. neon 霓虹灯风 =====
    "neon_1": {"bg": "#0a0a0a", "accent1": "#ff006e", "accent2": "#00ffff", "name": "粉青霓虹", "theme": "neon"},
    "neon_2": {"bg": "#0d0221", "accent1": "#ff6ec7", "accent2": "#aaff00", "name": "粉绿霓虹", "theme": "neon"},
    "neon_3": {"bg": "#000000", "accent1": "#fbbf24", "accent2": "#a855f7", "name": "金紫霓虹", "theme": "neon"},
    "neon_4": {"bg": "#0a0a0a", "accent1": "#06b6d4", "accent2": "#f97316", "name": "青橙霓虹", "theme": "neon"},
    # ===== 28. retro 复古风 =====
    "retro_1": {"bg": "linear-gradient(135deg,#d4a373,#e9c46a)", "accent1": "#264653", "accent2": "#e76f51", "name": "暖调复古", "theme": "retro"},
    "retro_2": {"bg": "linear-gradient(135deg,#a98467,#dde5b6)", "accent1": "#3a5a40", "accent2": "#a3b18a", "name": "棕绿复古", "theme": "retro"},
    "retro_3": {"bg": "#2a1810", "accent1": "#d4a373", "accent2": "#e9c46a", "name": "暗调复古", "theme": "retro"},
    "retro_4": {"bg": "linear-gradient(135deg,#cc9966,#ffcc99)", "accent1": "#663300", "accent2": "#996633", "name": "胶片复古", "theme": "retro"},
    # ===== 29. collage 拼贴风 =====
    "collage_1": {"bg": "#f5f5dc", "accent1": "#d2691e", "accent2": "#2e8b57", "name": "米棕绿拼贴", "theme": "collage", "text_color": "#1a1a1a"},
    "collage_2": {"bg": "#faf0e6", "accent1": "#8b4513", "accent2": "#ff6347", "name": "暖调拼贴", "theme": "collage", "text_color": "#1a1a1a"},
    "collage_3": {"bg": "#e8e8e8", "accent1": "#2f4f4f", "accent2": "#dc143c", "name": "灰红黑拼贴", "theme": "collage", "text_color": "#1a1a1a"},
    "collage_4": {"bg": "#fffacd", "accent1": "#4b0082", "accent2": "#ff8c00", "name": "黄紫橙拼贴", "theme": "collage", "text_color": "#1a1a1a"},
    # ===== 30. aurora 弥散光/极光风 =====
    "aurora_1": {"bg": "linear-gradient(135deg,#0f0c29,#302b63,#24243e)", "accent1": "#00ff88", "accent2": "#00d4ff", "name": "深空极光", "theme": "aurora"},
    "aurora_2": {"bg": "linear-gradient(135deg,#1a0033,#336699,#00cccc)", "accent1": "#ff66cc", "accent2": "#66ff99", "name": "紫蓝绿极光", "theme": "aurora"},
    "aurora_3": {"bg": "linear-gradient(180deg,#0d1b2a,#1b3a4b,#2d6a7e)", "accent1": "#7fc8f8", "accent2": "#e8b4d8", "name": "海洋极光", "theme": "aurora"},
    "aurora_4": {"bg": "linear-gradient(135deg,#1a0a2e,#16213e,#0f3460)", "accent1": "#e94560", "accent2": "#00d9ff", "name": "星空极光", "theme": "aurora"},

    # ===== 31. ink 水墨风 =====
    "ink_1": {"bg": "#f5f5ec", "accent1": "#1a1a1a", "accent2": "#8b4513", "name": "宣纸水墨", "theme": "ink", "text_color": "#1a1a1a"},
    "ink_2": {"bg": "#e8e4d8", "accent1": "#2c2c2c", "accent2": "#a0522d", "name": "淡墨枯笔", "theme": "ink", "text_color": "#2c2c2c"},
    "ink_3": {"bg": "#1a1a1a", "accent1": "#f5f5ec", "accent2": "#c41e3a", "name": "浓墨红印", "theme": "ink"},
    "ink_4": {"bg": "#f0ede0", "accent1": "#36454f", "accent2": "#8b0000", "name": "青墨朱砂", "theme": "ink", "text_color": "#36454f"},

    # ===== 32. stamp 印章风 =====
    "stamp_1": {"bg": "#f5e6d3", "accent1": "#8b0000", "accent2": "#1a1a2e", "name": "米黄朱印", "theme": "stamp", "text_color": "#1a1a2e"},
    "stamp_2": {"bg": "#1a1a2e", "accent1": "#dc143c", "accent2": "#ffd700", "name": "暗夜金印", "theme": "stamp"},
    "stamp_3": {"bg": "#fdf6e3", "accent1": "#c0392b", "accent2": "#2c3e50", "name": "白底红章", "theme": "stamp", "text_color": "#2c3e50"},
    "stamp_4": {"bg": "#8b0000", "accent1": "#ffd700", "accent2": "#f5e6d3", "name": "红底金印", "theme": "stamp"},

    # ===== 33. newspaper 报纸风 =====
    "newspaper_1": {"bg": "#f5f5f0", "accent1": "#1a1a1a", "accent2": "#8b0000", "name": "黑白报纸", "theme": "newspaper", "text_color": "#1a1a1a"},
    "newspaper_2": {"bg": "#e8e8e0", "accent1": "#2c2c2c", "accent2": "#c0392b", "name": "泛黄报纸", "theme": "newspaper", "text_color": "#2c2c2c"},
    "newspaper_3": {"bg": "#1a1a1a", "accent1": "#f5f5f0", "accent2": "#c0392b", "name": "暗黑报纸", "theme": "newspaper"},
    "newspaper_4": {"bg": "#faf8f0", "accent1": "#1a1a1a", "accent2": "#1e3a5f", "name": "蓝黑报纸", "theme": "newspaper", "text_color": "#1a1a1a"},

    # ===== 34. polaroid 拍立得 =====
    "polaroid_1": {"bg": "#fafafa", "accent1": "#2c2c2c", "accent2": "#e74c3c", "name": "经典拍立得", "theme": "polaroid", "text_color": "#2c2c2c"},
    "polaroid_2": {"bg": "#fff8e7", "accent1": "#d4a373", "accent2": "#264653", "name": "暖调拍立得", "theme": "polaroid", "text_color": "#264653"},
    "polaroid_3": {"bg": "#f0f0f0", "accent1": "#1a1a1a", "accent2": "#06b6d4", "name": "冷调拍立得", "theme": "polaroid", "text_color": "#1a1a1a"},
    "polaroid_4": {"bg": "#fdf2f8", "accent1": "#831843", "accent2": "#9370db", "name": "粉色拍立得", "theme": "polaroid", "text_color": "#831843"},

    # ===== 35. risograph Riso印刷风 =====
    "risograph_1": {"bg": "#fef3c7", "accent1": "#dc2626", "accent2": "#1e3a5f", "name": "Riso红蓝", "theme": "risograph", "text_color": "#1a1a1a"},
    "risograph_2": {"bg": "#f0fdf4", "accent1": "#16a34a", "accent2": "#9333ea", "name": "Riso绿紫", "theme": "risograph", "text_color": "#1a1a1a"},
    "risograph_3": {"bg": "#fdf2f8", "accent1": "#ec4899", "accent2": "#0ea5e9", "name": "Riso粉蓝", "theme": "risograph", "text_color": "#1a1a1a"},
    "risograph_4": {"bg": "#1a1a1a", "accent1": "#fbbf24", "accent2": "#06b6d4", "name": "Riso夜版", "theme": "risograph"},

    # ===== 36. film 电影胶片风 =====
    "film_1": {"bg": "#0a0a0a", "accent1": "#fbbf24", "accent2": "#dc2626", "name": "胶片金红", "theme": "film"},
    "film_2": {"bg": "#1c1410", "accent1": "#d4a373", "accent2": "#fefae0", "name": "暖色胶片", "theme": "film"},
    "film_3": {"bg": "#0a1008", "accent1": "#22c55e", "accent2": "#fbbf24", "name": "复古胶片", "theme": "film"},
    "film_4": {"bg": "#0d0d0d", "accent1": "#c0c0c0", "accent2": "#dc2626", "name": "黑白胶片", "theme": "film"},

    # ===== 37. graffiti 涂鸦街头风 =====
    "graffiti_1": {"bg": "#1a1a1a", "accent1": "#aaff00", "accent2": "#ff00aa", "name": "街头喷漆", "theme": "graffiti"},
    "graffiti_2": {"bg": "#0d0d0d", "accent1": "#ff6600", "accent2": "#00ffff", "name": "地铁涂鸦", "theme": "graffiti"},
    "graffiti_3": {"bg": "#2d1b3d", "accent1": "#ffeb3b", "accent2": "#e91e63", "name": "夜墙涂鸦", "theme": "graffiti"},
    "graffiti_4": {"bg": "#1a0a0a", "accent1": "#ff3366", "accent2": "#33ff33", "name": "野生涂鸦", "theme": "graffiti"},

    # ===== 38. ribbon 缎带横幅风 =====
    "ribbon_1": {"bg": "#fdf6e3", "accent1": "#8b0000", "accent2": "#d4af37", "name": "红金缎带", "theme": "ribbon", "text_color": "#1a1a1a"},
    "ribbon_2": {"bg": "#1e3a5f", "accent1": "#ffd700", "accent2": "#ffffff", "name": "蓝金缎带", "theme": "ribbon"},
    "ribbon_3": {"bg": "#fef3c7", "accent1": "#92400e", "accent2": "#dc2626", "name": "米棕缎带", "theme": "ribbon", "text_color": "#1a1a1a"},
    "ribbon_4": {"bg": "#2d0a1a", "accent1": "#f9a8d4", "accent2": "#ec4899", "name": "玫瑰缎带", "theme": "ribbon"},

    # ===== 39. gradient-mesh 网格渐变风 =====
    "gradientmesh_1": {"bg": "linear-gradient(135deg,#ff9a9e 0%,#fecfef 50%,#a18cd1 100%)", "accent1": "#ffffff", "accent2": "#6a3093", "name": "粉紫网格渐变", "theme": "gradientmesh", "is_gradient": True},
    "gradientmesh_2": {"bg": "linear-gradient(135deg,#a8edea 0%,#fed6e3 50%,#84fab0 100%)", "accent1": "#ffffff", "accent2": "#0d9488", "name": "青绿网格渐变", "theme": "gradientmesh", "is_gradient": True},
    "gradientmesh_3": {"bg": "linear-gradient(135deg,#fbc2eb 0%,#a6c1ee 50%,#c2e9fb 100%)", "accent1": "#ffffff", "accent2": "#4f46e5", "name": "蓝粉网格渐变", "theme": "gradientmesh", "is_gradient": True},
    "gradientmesh_4": {"bg": "linear-gradient(135deg,#fdcbf1 0%,#e6dee9 50%,#a8edea 100%)", "accent1": "#ffffff", "accent2": "#7c3aed", "name": "柔彩网格渐变", "theme": "gradientmesh", "is_gradient": True},

    # ===== 40. brutalist 粗野主义风 =====
    "brutalist_1": {"bg": "#ffffff", "accent1": "#000000", "accent2": "#ff3300", "name": "白底粗野", "theme": "brutalist", "text_color": "#000000"},
    "brutalist_2": {"bg": "#000000", "accent1": "#ffffff", "accent2": "#ff3300", "name": "黑底粗野", "theme": "brutalist"},
    "brutalist_3": {"bg": "#c0c0c0", "accent1": "#1a1a1a", "accent2": "#ff0000", "name": "混凝土粗野", "theme": "brutalist", "text_color": "#1a1a1a"},
    "brutalist_4": {"bg": "#f5f5dc", "accent1": "#1a1a1a", "accent2": "#ff6600", "name": "米色粗野", "theme": "brutalist", "text_color": "#1a1a1a"},

    # ===== 41. pastel 莫兰迪柔色风 =====
    "pastel_1": {"bg": "#e8e0d5", "accent1": "#a8a29e", "accent2": "#d6ccc2", "name": "莫兰迪灰棕", "theme": "pastel", "text_color": "#44403c"},
    "pastel_2": {"bg": "#d4e4e7", "accent1": "#7a9e9f", "accent2": "#c8b6a6", "name": "莫兰迪蓝灰", "theme": "pastel", "text_color": "#3a4a4a"},
    "pastel_3": {"bg": "#f0e6e6", "accent1": "#b0a0a0", "accent2": "#a0b0a0", "name": "莫兰迪粉绿", "theme": "pastel", "text_color": "#5a4a4a"},
    "pastel_4": {"bg": "#e0dccd", "accent1": "#8b7d6b", "accent2": "#c4b7a6", "name": "莫兰迪暖灰", "theme": "pastel", "text_color": "#4a4030"},

    # ===== 42. popart 波普艺术风 =====
    "popart_1": {"bg": "#ffd700", "accent1": "#ff1493", "accent2": "#00bfff", "name": "黄粉蓝波普", "theme": "popart", "text_color": "#1a1a1a"},
    "popart_2": {"bg": "#ff1493", "accent1": "#ffd700", "accent2": "#000000", "name": "粉黄黑波普", "theme": "popart"},
    "popart_3": {"bg": "#00bfff", "accent1": "#ff1493", "accent2": "#ffd700", "name": "蓝粉黄波普", "theme": "popart"},
    "popart_4": {"bg": "#1a1a1a", "accent1": "#ff6600", "accent2": "#00ff99", "name": "暗夜波普", "theme": "popart"},

    # ===== 43. terrarium 玻璃生态风 =====
    "terrarium_1": {"bg": "linear-gradient(135deg,#d1fae5,#a7f3d0)", "accent1": "#065f46", "accent2": "#84cc16", "name": "翠绿生态", "theme": "terrarium", "is_gradient": True, "text_color": "#064e3b"},
    "terrarium_2": {"bg": "linear-gradient(135deg,#ccfbf1,#99f6e4)", "accent1": "#0f766e", "accent2": "#22d3ee", "name": "薄荷生态", "theme": "terrarium", "is_gradient": True, "text_color": "#134e4a"},
    "terrarium_3": {"bg": "linear-gradient(135deg,#ecfccb,#d9f99d)", "accent1": "#3f6212", "accent2": "#65a30d", "name": "嫩绿生态", "theme": "terrarium", "is_gradient": True, "text_color": "#1a2e05"},
    "terrarium_4": {"bg": "linear-gradient(135deg,#f0fdf4,#dcfce7)", "accent1": "#166534", "accent2": "#16a34a", "name": "森林生态", "theme": "terrarium", "is_gradient": True, "text_color": "#14532d"},

    # ===== 44. holographic 全息彩虹风 =====
    "holographic_1": {"bg": "linear-gradient(135deg,#ff006e,#fb5607,#ffbe0b,#8338ec,#3a86ff)", "accent1": "#ffffff", "accent2": "#ff006e", "name": "全息彩虹", "theme": "holographic", "is_gradient": True},
    "holographic_2": {"bg": "linear-gradient(135deg,#06ffa5,#00d9ff,#8338ec,#ff006e)", "accent1": "#ffffff", "accent2": "#06ffa5", "name": "镭射全息", "theme": "holographic", "is_gradient": True},
    "holographic_3": {"bg": "linear-gradient(135deg,#e0aaff,#c77dff,#9d4edd,#5a189a)", "accent1": "#ffffff", "accent2": "#e0aaff", "name": "紫光全息", "theme": "holographic", "is_gradient": True},
    "holographic_4": {"bg": "linear-gradient(135deg,#ffd60a,#00f5d4,#9b5de5,#f15bb5)", "accent1": "#ffffff", "accent2": "#ffd60a", "name": "幻彩全息", "theme": "holographic", "is_gradient": True},

    # ===== 45. kraft 牛皮纸风 =====
    "kraft_1": {"bg": "#d4a574", "accent1": "#3c2415", "accent2": "#8b0000", "name": "经典牛皮纸", "theme": "kraft", "text_color": "#3c2415"},
    "kraft_2": {"bg": "#c4a07a", "accent1": "#2c1810", "accent2": "#654321", "name": "深色牛皮纸", "theme": "kraft", "text_color": "#2c1810"},
    "kraft_3": {"bg": "#e0c094", "accent1": "#4a2c1a", "accent2": "#c0392b", "name": "浅色牛皮纸", "theme": "kraft", "text_color": "#4a2c1a"},
    "kraft_4": {"bg": "#b8956a", "accent1": "#1a1a1a", "accent2": "#cd853f", "name": "复古牛皮纸", "theme": "kraft", "text_color": "#1a1a1a"},

    # ===== 46. blueprint 蓝图风 =====
    "blueprint_1": {"bg": "#0d3b66", "accent1": "#ffffff", "accent2": "#faf0ca", "name": "经典蓝图", "theme": "blueprint"},
    "blueprint_2": {"bg": "#1e3a5f", "accent1": "#ffffff", "accent2": "#ffd700", "name": "工程蓝图", "theme": "blueprint"},
    "blueprint_3": {"bg": "#0a4d8c", "accent1": "#ffffff", "accent2": "#ff6b35", "name": "技术蓝图", "theme": "blueprint"},
    "blueprint_4": {"bg": "#1a3050", "accent1": "#80d8ff", "accent2": "#ffeb3b", "name": "暗蓝蓝图", "theme": "blueprint"},

    # ===== 47. starfield 星空宇宙风 =====
    "starfield_1": {"bg": "#000814", "accent1": "#ffd60a", "accent2": "#00d9ff", "name": "深空星海", "theme": "starfield"},
    "starfield_2": {"bg": "#0a0e27", "accent1": "#7209b7", "accent2": "#4cc9f0", "name": "银河紫蓝", "theme": "starfield"},
    "starfield_3": {"bg": "#0d0221", "accent1": "#ff006e", "accent2": "#3a86ff", "name": "星云粉蓝", "theme": "starfield"},
    "starfield_4": {"bg": "#001233", "accent1": "#ff7b00", "accent2": "#00f5d4", "name": "橙绿星空", "theme": "starfield"},

    # ===== 48. washi 和纸胶带风 =====
    "washi_1": {"bg": "#fef3c7", "accent1": "#dc2626", "accent2": "#1e3a5f", "name": "和风红蓝", "theme": "washi", "text_color": "#1a1a1a"},
    "washi_2": {"bg": "#fdf2f8", "accent1": "#ec4899", "accent2": "#16a34a", "name": "和风粉绿", "theme": "washi", "text_color": "#1a1a1a"},
    "washi_3": {"bg": "#f0fdf4", "accent1": "#0ea5e9", "accent2": "#f59e0b", "name": "和风蓝黄", "theme": "washi", "text_color": "#1a1a1a"},
    "washi_4": {"bg": "#e0f2fe", "accent1": "#7c3aed", "accent2": "#dc2626", "name": "和风紫红", "theme": "washi", "text_color": "#1a1a1a"},

    # ===== 49. typewriter 打字机风 =====
    "typewriter_1": {"bg": "#faf8f0", "accent1": "#1a1a1a", "accent2": "#8b0000", "name": "纸张打字机", "theme": "typewriter", "text_color": "#1a1a1a"},
    "typewriter_2": {"bg": "#f5f0e0", "accent1": "#2c2c2c", "accent2": "#1e3a5f", "name": "泛黄打字机", "theme": "typewriter", "text_color": "#2c2c2c"},
    "typewriter_3": {"bg": "#1a1a1a", "accent1": "#f5f0e0", "accent2": "#fbbf24", "name": "暗夜打字机", "theme": "typewriter"},
    "typewriter_4": {"bg": "#e8e4d8", "accent1": "#36454f", "accent2": "#8b4513", "name": "手稿打字机", "theme": "typewriter", "text_color": "#36454f"},

    # ===== 50. carnival 嘉年华风 =====
    "carnival_1": {"bg": "#1a0033", "accent1": "#ffd700", "accent2": "#ff006e", "name": "马戏团紫金", "theme": "carnival"},
    "carnival_2": {"bg": "#8b0000", "accent1": "#ffd700", "accent2": "#ffffff", "name": "红白金嘉年华", "theme": "carnival"},
    "carnival_3": {"bg": "#2d0a3d", "accent1": "#ff6600", "accent2": "#ffeb3b", "name": "橙黄嘉年华", "theme": "carnival"},
    "carnival_4": {"bg": "#0d0d0d", "accent1": "#ff1493", "accent2": "#00bfff", "name": "霓虹嘉年华", "theme": "carnival"},

    # ===== 51. screenshot 真实截图风 — 教程/源码/PPT =====
    "screenshot_1": {"bg": "#ffffff", "accent1": "#dc2626", "accent2": "#fbbf24", "name": "红条白底", "theme": "screenshot", "text_color": "#1a1a1a"},
    "screenshot_2": {"bg": "#f5f5f5", "accent1": "#0f172a", "accent2": "#dc2626", "name": "暗色代码", "theme": "screenshot", "text_color": "#1a1a1a"},
    "screenshot_3": {"bg": "#fef3c7", "accent1": "#dc2626", "accent2": "#1a1a1a", "name": "黄底红字", "theme": "screenshot", "text_color": "#1a1a1a"},
    "screenshot_4": {"bg": "#1e293b", "accent1": "#fbbf24", "accent2": "#22d3ee", "name": "深色终端", "theme": "screenshot"},

    # ===== 52. portrait 真人出镜风 — 经验/职业/分享 =====
    "portrait_1": {"bg": "#1e40af", "accent1": "#fbbf24", "accent2": "#ffffff", "name": "蓝底黄字", "theme": "portrait"},
    "portrait_2": {"bg": "#0f172a", "accent1": "#22d3ee", "accent2": "#fbbf24", "name": "深夜分享", "theme": "portrait"},
    "portrait_3": {"bg": "#fbbf24", "accent1": "#dc2626", "accent2": "#1a1a1a", "name": "黄色高亮", "theme": "portrait", "text_color": "#1a1a1a"},
    "portrait_4": {"bg": "#dc2626", "accent1": "#ffffff", "accent2": "#fbbf24", "name": "红底白字", "theme": "portrait"},

    # ===== 53. product 实物产品风 — 测评/开箱/工具 =====
    "product_1": {"bg": "#f8fafc", "accent1": "#0ea5e9", "accent2": "#f97316", "name": "浅灰开箱", "theme": "product", "text_color": "#0c4a6e"},
    "product_2": {"bg": "#0a0a0a", "accent1": "#fbbf24", "accent2": "#22d3ee", "name": "黑底金蓝", "theme": "product"},
    "product_3": {"bg": "#fef3c7", "accent1": "#7c3aed", "accent2": "#ec4899", "name": "黄紫撞色", "theme": "product", "text_color": "#1a1a1a"},
    "product_4": {"bg": "#1a1a2e", "accent1": "#06b6d4", "accent2": "#fbbf24", "name": "深蓝高亮", "theme": "product"},

    # ===== 54. contrast 对比冲击风 — 对比/vs/盘点 =====
    "contrast_1": {"bg": "#ffffff", "accent1": "#dc2626", "accent2": "#0ea5e9", "name": "红蓝对决", "theme": "contrast", "text_color": "#1a1a1a"},
    "contrast_2": {"bg": "#0a0a0a", "accent1": "#fbbf24", "accent2": "#ffffff", "name": "黑金对比", "theme": "contrast"},
    "contrast_3": {"bg": "#fef3c7", "accent1": "#16a34a", "accent2": "#dc2626", "name": "黄绿红", "theme": "contrast", "text_color": "#1a1a1a"},
    "contrast_4": {"bg": "#f3e8ff", "accent1": "#7c3aed", "accent2": "#f97316", "name": "紫橙对比", "theme": "contrast", "text_color": "#1a1a1a"},

    # ===== 55. zoom 局部放大风 — 细节/重点/特写 =====
    "zoom_1": {"bg": "#fef2f2", "accent1": "#dc2626", "accent2": "#1a1a1a", "name": "红圈放大", "theme": "zoom", "text_color": "#1a1a1a"},
    "zoom_2": {"bg": "#0f172a", "accent1": "#fbbf24", "accent2": "#dc2626", "name": "暗色放大", "theme": "zoom"},
    "zoom_3": {"bg": "#fffbeb", "accent1": "#f59e0b", "accent2": "#dc2626", "name": "黄底红圈", "theme": "zoom", "text_color": "#1a1a1a"},
    "zoom_4": {"bg": "#ecfdf5", "accent1": "#059669", "accent2": "#7c3aed", "name": "绿紫放大", "theme": "zoom", "text_color": "#064e3b"},

    "glitch_1": {"bg": '#0a0a0a', "accent1": '#00ff41', "accent2": '#ff0040', "name": '绿红故障', "theme": 'glitch'},
    "glitch_2": {"bg": '#1a0a2e', "accent1": '#00ffff', "accent2": '#ff00ff', "name": '青紫故障', "theme": 'glitch'},
    "glitch_3": {"bg": '#0d0d0d', "accent1": '#ff6600', "accent2": '#00ccff', "name": '橙蓝故障', "theme": 'glitch'},
    "glitch_4": {"bg": '#000814', "accent1": '#fbbf24', "accent2": '#ef4444', "name": '金红故障', "theme": 'glitch'},
    "synthwave_1": {"bg": 'linear-gradient(180deg,#2d1b69,#ff6ec7,#feca57)', "accent1": '#00ffff', "accent2": '#ff00ff', "name": '落日合成波', "is_gradient": True, "theme": 'synthwave'},
    "synthwave_2": {"bg": '#1a0a2e', "accent1": '#ff6ec7', "accent2": '#feca57', "name": '暗紫合成波', "theme": 'synthwave'},
    "synthwave_3": {"bg": '#0d0221', "accent1": '#ff71ce', "accent2": '#01cdfe', "name": '粉青合成波', "theme": 'synthwave'},
    "synthwave_4": {"bg": '#2b1055', "accent1": '#d53a9d', "accent2": '#7209b7', "name": '深紫合成波', "theme": 'synthwave'},
    "matrix_1": {"bg": '#000000', "accent1": '#00ff41', "accent2": '#008f11', "name": '经典矩阵', "theme": 'matrix'},
    "matrix_2": {"bg": '#0a0a0a', "accent1": '#00ff41', "accent2": '#39ff14', "name": '亮绿矩阵', "theme": 'matrix'},
    "matrix_3": {"bg": '#000d00', "accent1": '#00ff41', "accent2": '#fbbf24', "name": '绿金矩阵', "theme": 'matrix'},
    "matrix_4": {"bg": '#0d1117', "accent1": '#58a6ff', "accent2": '#00ff41', "name": '蓝绿矩阵', "theme": 'matrix'},
    "quantum_1": {"bg": '#0a0a1a', "accent1": '#7c3aed', "accent2": '#06b6d4', "name": '紫蓝量子', "theme": 'quantum'},
    "quantum_2": {"bg": '#0d0221', "accent1": '#a855f7', "accent2": '#22d3ee', "name": '亮紫量子', "theme": 'quantum'},
    "quantum_3": {"bg": '#000814', "accent1": '#3b82f6', "accent2": '#8b5cf6', "name": '蓝紫量子', "theme": 'quantum'},
    "quantum_4": {"bg": '#1a0a2e', "accent1": '#c084fc', "accent2": '#67e8f9', "name": '柔紫量子', "theme": 'quantum'},
    "ocean_1": {"bg": '#0a1628', "accent1": '#00b4d8', "accent2": '#0077b6', "name": '深海蓝', "theme": 'ocean'},
    "ocean_2": {"bg": '#001220', "accent1": '#48cae4', "accent2": '#023e8a', "name": '深蓝海洋', "theme": 'ocean'},
    "ocean_3": {"bg": '#0d2137', "accent1": '#00b4d8', "accent2": '#90e0ef', "name": '蓝青海洋', "theme": 'ocean'},
    "ocean_4": {"bg": '#0a192f', "accent1": '#64ffda', "accent2": '#0077b6', "name": '蓝绿海洋', "theme": 'ocean'},
    "ice_1": {"bg": '#0a1628', "accent1": '#7dd3fc', "accent2": '#bae6fd', "name": '冰蓝', "theme": 'ice'},
    "ice_2": {"bg": '#0d1b2a', "accent1": '#38bdf8', "accent2": '#e0f2fe', "name": '亮蓝冰', "theme": 'ice'},
    "ice_3": {"bg": '#1e293b', "accent1": '#7dd3fc', "accent2": '#0ea5e9', "name": '蓝灰冰', "theme": 'ice'},
    "ice_4": {"bg": '#0c1929', "accent1": '#a5f3fc', "accent2": '#0284c7', "name": '青蓝冰', "theme": 'ice'},
    "glassmorph_1": {"bg": 'linear-gradient(135deg,#667eea 0%,#764ba2 100%)', "accent1": '#ffffff', "accent2": 'rgba(255,255,255,0.5)', "name": '紫蓝毛玻璃', "is_gradient": True, "theme": 'glassmorph'},
    "glassmorph_2": {"bg": 'linear-gradient(135deg,#0ea5e9 0%,#6366f1 100%)', "accent1": '#ffffff', "accent2": 'rgba(255,255,255,0.5)', "name": '蓝紫毛玻璃', "is_gradient": True, "theme": 'glassmorph'},
    "glassmorph_3": {"bg": 'linear-gradient(135deg,#f97316 0%,#ec4899 100%)', "accent1": '#ffffff', "accent2": 'rgba(255,255,255,0.5)', "name": '橙粉毛玻璃', "is_gradient": True, "theme": 'glassmorph'},
    "glassmorph_4": {"bg": 'linear-gradient(135deg,#10b981 0%,#3b82f6 100%)', "accent1": '#ffffff', "accent2": 'rgba(255,255,255,0.5)', "name": '绿蓝毛玻璃', "is_gradient": True, "theme": 'glassmorph'},
    "retrofuturism_1": {"bg": '#1a0a2e', "accent1": '#ff6ec7', "accent2": '#00ffff', "name": '粉青复古未来', "theme": 'retrofuturism'},
    "retrofuturism_2": {"bg": '#0d0221', "accent1": '#feca57', "accent2": '#ff6ec7', "name": '金粉复古未来', "theme": 'retrofuturism'},
    "retrofuturism_3": {"bg": '#2d1b69', "accent1": '#00ffff', "accent2": '#ff00ff', "name": '青紫复古未来', "theme": 'retrofuturism'},
    "retrofuturism_4": {"bg": '#0a0a1a', "accent1": '#ff6600', "accent2": '#00bfff', "name": '橙蓝复古未来', "theme": 'retrofuturism'},
    "galaxy_1": {"bg": 'linear-gradient(135deg,#0f0c29,#302b63,#24243e)', "accent1": '#a855f7', "accent2": '#06b6d4', "name": '紫蓝银河', "is_gradient": True, "theme": 'galaxy'},
    "galaxy_2": {"bg": 'linear-gradient(135deg,#1a0033,#0d1b2a,#000814)', "accent1": '#f472b6', "accent2": '#818cf8', "name": '粉紫银河', "is_gradient": True, "theme": 'galaxy'},
    "galaxy_3": {"bg": '#000814', "accent1": '#fbbf24', "accent2": '#a855f7', "name": '金紫银河', "theme": 'galaxy'},
    "galaxy_4": {"bg": '#0a0014', "accent1": '#22d3ee', "accent2": '#e879f9', "name": '青粉银河', "theme": 'galaxy'},
    "candy_1": {"bg": '#fdf2f8', "accent1": '#ec4899', "accent2": '#f472b6', "name": '粉红糖果', "text_color": '#831843', "theme": 'candy'},
    "candy_2": {"bg": '#fef3c7', "accent1": '#f59e0b', "accent2": '#ec4899', "name": '黄粉糖果', "text_color": '#92400e', "theme": 'candy'},
    "candy_3": {"bg": '#f0fdf4', "accent1": '#22c55e', "accent2": '#ec4899', "name": '绿粉糖果', "text_color": '#14532d', "theme": 'candy'},
    "candy_4": {"bg": '#e0f2fe', "accent1": '#0ea5e9', "accent2": '#f472b6', "name": '蓝粉糖果', "text_color": '#0c4a6e', "theme": 'candy'},
    "steampunk_1": {"bg": '#2a1810', "accent1": '#d4a373', "accent2": '#cd853f', "name": '铜棕蒸汽', "theme": 'steampunk'},
    "steampunk_2": {"bg": '#1a0f0a', "accent1": '#b8860b', "accent2": '#daa520', "name": '金棕蒸汽', "theme": 'steampunk'},
    "steampunk_3": {"bg": '#3c2415', "accent1": '#f4a460', "accent2": '#8b4513', "name": '暖棕蒸汽', "theme": 'steampunk'},
    "steampunk_4": {"bg": '#0d0a08', "accent1": '#cd853f', "accent2": '#d2691e', "name": '深棕蒸汽', "theme": 'steampunk'},
    "noir_1": {"bg": '#0a0a0a', "accent1": '#ffffff', "accent2": '#888888', "name": '经典黑白', "theme": 'noir'},
    "noir_2": {"bg": '#111111', "accent1": '#e5e5e5', "accent2": '#dc2626', "name": '黑白红', "theme": 'noir'},
    "noir_3": {"bg": '#0d0d0d', "accent1": '#fbbf24', "accent2": '#666666', "name": '黑金noir', "theme": 'noir'},
    "noir_4": {"bg": '#1a1a1a', "accent1": '#cccccc', "accent2": '#444444', "name": '灰调noir', "theme": 'noir'},
    "gothic_1": {"bg": '#0a0000', "accent1": '#8b0000', "accent2": '#4a0020', "name": '暗红哥特', "theme": 'gothic'},
    "gothic_2": {"bg": '#0d0d1a', "accent1": '#7c3aed', "accent2": '#1e1b4b', "name": '紫黑哥特', "theme": 'gothic'},
    "gothic_3": {"bg": '#0a0a0a', "accent1": '#dc2626', "accent2": '#1a1a2e', "name": '红黑哥特', "theme": 'gothic'},
    "gothic_4": {"bg": '#1a0011', "accent1": '#ec4899', "accent2": '#4a0028', "name": '粉紫哥特', "theme": 'gothic'},
    "baroque_1": {"bg": '#1a0a00', "accent1": '#d4af37', "accent2": '#8b0000', "name": '金红巴洛克', "theme": 'baroque'},
    "baroque_2": {"bg": '#0d0a1a', "accent1": '#c9a96e', "accent2": '#4a0080', "name": '金紫巴洛克', "theme": 'baroque'},
    "baroque_3": {"bg": '#2a1810', "accent1": '#ffd700', "accent2": '#1a1a2e', "name": '金棕巴洛克', "theme": 'baroque'},
    "baroque_4": {"bg": '#0a0000', "accent1": '#d4af37', "accent2": '#2d0a0a', "name": '深红金巴洛克', "theme": 'baroque'},
    "tribal_1": {"bg": '#1a0f00', "accent1": '#d4a373', "accent2": '#8b4513', "name": '棕土部落', "theme": 'tribal'},
    "tribal_2": {"bg": '#0a0a00', "accent1": '#fbbf24', "accent2": '#dc2626', "name": '金红部落', "theme": 'tribal'},
    "tribal_3": {"bg": '#2a1810', "accent1": '#16a34a', "accent2": '#d4a373', "name": '绿棕部落', "theme": 'tribal'},
    "tribal_4": {"bg": '#0d0800', "accent1": '#f97316', "accent2": '#7c3aed', "name": '橙紫部落', "theme": 'tribal'},
    "artdeco_1": {"bg": '#0a0a1a', "accent1": '#d4af37', "accent2": '#1a1a3a', "name": '金蓝装饰', "theme": 'artdeco'},
    "artdeco_2": {"bg": '#1a0a00', "accent1": '#ffd700', "accent2": '#2a1810', "name": '金棕装饰', "theme": 'artdeco'},
    "artdeco_3": {"bg": '#0d0d1a', "accent1": '#c9a96e', "accent2": '#1e1b4b', "name": '金紫装饰', "theme": 'artdeco'},
    "artdeco_4": {"bg": '#0a0a0a', "accent1": '#d4af37', "accent2": '#333333', "name": '金灰装饰', "theme": 'artdeco'},
    "fire_1": {"bg": '#1a0000', "accent1": '#ff4500', "accent2": '#ffd700', "name": '红金烈焰', "theme": 'fire'},
    "fire_2": {"bg": '#0a0000', "accent1": '#ff6600', "accent2": '#ff0000', "name": '橙红烈焰', "theme": 'fire'},
    "fire_3": {"bg": '#1a0500', "accent1": '#ff4500', "accent2": '#ff8c00', "name": '深橙烈焰', "theme": 'fire'},
    "fire_4": {"bg": '#0d0000', "accent1": '#dc2626', "accent2": '#fbbf24', "name": '红金暗焰', "theme": 'fire'},
    "streetwear_1": {"bg": '#0a0a0a', "accent1": '#ff0000', "accent2": '#ffffff', "name": '红黑街头', "theme": 'streetwear'},
    "streetwear_2": {"bg": '#111111', "accent1": '#fbbf24', "accent2": '#000000', "name": '金黑街头', "theme": 'streetwear'},
    "streetwear_3": {"bg": '#0d0d0d', "accent1": '#00ff00', "accent2": '#ffffff', "name": '绿黑街头', "theme": 'streetwear'},
    "streetwear_4": {"bg": '#1a1a1a', "accent1": '#ff6600', "accent2": '#000000', "name": '橙黑街头', "theme": 'streetwear'},
    "psychadelic_1": {"bg": 'linear-gradient(135deg,#ff006e,#fb5607,#ffbe0b,#8338ec,#3a86ff)', "accent1": '#ffffff', "accent2": '#ff006e', "name": '彩虹迷幻', "is_gradient": True, "theme": 'psychadelic'},
    "psychadelic_2": {"bg": '#0a0a0a', "accent1": '#ff00ff', "accent2": '#00ffff', "name": '霓虹迷幻', "theme": 'psychadelic'},
    "psychadelic_3": {"bg": 'linear-gradient(135deg,#ff006e,#8338ec,#3a86ff,#06ffa5)', "accent1": '#ffffff', "accent2": '#ffbe0b', "name": '四色迷幻', "is_gradient": True, "theme": 'psychadelic'},
    "psychadelic_4": {"bg": '#1a0033', "accent1": '#ff6600', "accent2": '#00ff88', "name": '橙绿迷幻', "theme": 'psychadelic'},
    "mosaic_1": {"bg": '#1a1a2e', "accent1": '#e94560', "accent2": '#0f3460', "name": '红蓝马赛克', "theme": 'mosaic'},
    "mosaic_2": {"bg": '#0a0a1a', "accent1": '#fbbf24', "accent2": '#7c3aed', "name": '金紫马赛克', "theme": 'mosaic'},
    "mosaic_3": {"bg": '#1a0a2e', "accent1": '#22c55e', "accent2": '#ec4899', "name": '绿粉马赛克', "theme": 'mosaic'},
    "mosaic_4": {"bg": '#0d1117', "accent1": '#58a6ff', "accent2": '#f97316', "name": '蓝橙马赛克', "theme": 'mosaic'},
    "newspaper2_1": {"bg": '#f5f5f0', "accent1": '#dc2626', "accent2": '#1a1a1a', "name": '红黑头条', "text_color": '#1a1a1a', "theme": 'newspaper2'},
    "newspaper2_2": {"bg": '#ffffff', "accent1": '#dc2626', "accent2": '#1e3a5f', "name": '红蓝头条', "text_color": '#1a1a1a', "theme": 'newspaper2'},
    "newspaper2_3": {"bg": '#fef3c7', "accent1": '#dc2626', "accent2": '#92400e', "name": '黄红头条', "text_color": '#1a1a1a', "theme": 'newspaper2'},
    "newspaper2_4": {"bg": '#1a1a1a', "accent1": '#dc2626', "accent2": '#ffffff', "name": '暗黑头条', "theme": 'newspaper2'},
    "techwear_1": {"bg": '#0a0a0a', "accent1": '#fbbf24', "accent2": '#000000', "name": '黑金机能', "theme": 'techwear'},
    "techwear_2": {"bg": '#111111', "accent1": '#22c55e', "accent2": '#000000', "name": '黑绿机能', "theme": 'techwear'},
    "techwear_3": {"bg": '#0d0d0d', "accent1": '#ef4444', "accent2": '#000000', "name": '黑红机能', "theme": 'techwear'},
    "techwear_4": {"bg": '#0a0a0a', "accent1": '#06b6d4', "accent2": '#000000', "name": '黑青机能', "theme": 'techwear'},
    "cyberpunk2_1": {"bg": '#1a0a00', "accent1": '#ff6600', "accent2": '#ffd700', "name": '橙金废土', "theme": 'cyberpunk2'},
    "cyberpunk2_2": {"bg": '#0a0a00', "accent1": '#fbbf24', "accent2": '#dc2626', "name": '金红废土', "theme": 'cyberpunk2'},
    "cyberpunk2_3": {"bg": '#1a1000', "accent1": '#ff8c00', "accent2": '#8b4513', "name": '深棕废土', "theme": 'cyberpunk2'},
    "cyberpunk2_4": {"bg": '#0d0800', "accent1": '#ff4500', "accent2": '#2d1b00', "name": '暗橙废土', "theme": 'cyberpunk2'},
    "neoncity_1": {"bg": '#0a0a1a', "accent1": '#ff006e', "accent2": '#00ffff', "name": '粉青霓虹城', "theme": 'neoncity'},
    "neoncity_2": {"bg": '#0d0221', "accent1": '#ff6ec7', "accent2": '#feca57', "name": '粉金霓虹城', "theme": 'neoncity'},
    "neoncity_3": {"bg": '#000814', "accent1": '#00ff88', "accent2": '#ff006e', "name": '绿粉霓虹城', "theme": 'neoncity'},
    "neoncity_4": {"bg": '#1a0a2e', "accent1": '#ff6600', "accent2": '#00bfff', "name": '橙蓝霓虹城', "theme": 'neoncity'},
    "medieval_1": {"bg": '#1a0f00', "accent1": '#d4af37', "accent2": '#8b0000', "name": '金红中世纪', "theme": 'medieval'},
    "medieval_2": {"bg": '#0d0a00', "accent1": '#c0c0c0', "accent2": '#4a0020', "name": '银暗中世纪', "theme": 'medieval'},
    "medieval_3": {"bg": '#2a1810', "accent1": '#ffd700', "accent2": '#1a1a2e', "name": '金棕中世纪', "theme": 'medieval'},
    "medieval_4": {"bg": '#0a0a1a', "accent1": '#b8860b', "accent2": '#4a0028', "name": '暗金中世纪', "theme": 'medieval'},
    "watercolor_1": {"bg": 'linear-gradient(135deg,#a8edea 0%,#fed6e3 50%,#d4fc79 100%)', "accent1": '#667eea', "accent2": '#f093fb', "name": '彩虹水彩', "is_gradient": True, "theme": 'watercolor'},
    "watercolor_2": {"bg": 'linear-gradient(135deg,#ffecd2 0%,#fcb69f 100%)', "accent1": '#667eea', "accent2": '#764ba2', "name": '暖粉水彩', "is_gradient": True, "theme": 'watercolor'},
    "watercolor_3": {"bg": 'linear-gradient(135deg,#a1c4fd 0%,#c2e9fb 100%)', "accent1": '#667eea', "accent2": '#f093fb', "name": '蓝清水彩', "is_gradient": True, "theme": 'watercolor'},
    "watercolor_4": {"bg": 'linear-gradient(135deg,#d4fc79 0%,#96e6a1 100%)', "accent1": '#667eea', "accent2": '#764ba2', "name": '绿意水彩', "is_gradient": True, "theme": 'watercolor'},
    "zen_1": {"bg": '#f5f0e8', "accent1": '#5c4033', "accent2": '#8b7355', "name": '枯棕禅意', "text_color": '#3c2f2f', "theme": 'zen'},
    "zen_2": {"bg": '#e8e0d0', "accent1": '#4a6741', "accent2": '#8b7355', "name": '绿棕禅意', "text_color": '#2d3a2d', "theme": 'zen'},
    "zen_3": {"bg": '#f0ebe3', "accent1": '#2c3e50', "accent2": '#95a5a6', "name": '灰蓝禅意', "text_color": '#2c3e50', "theme": 'zen'},
    "zen_4": {"bg": '#eae4d9', "accent1": '#8b4513', "accent2": '#d2b48c', "name": '暖棕禅意', "text_color": '#3c2415', "theme": 'zen'},
    "scandinavian_1": {"bg": '#f5f0eb', "accent1": '#2c3e50', "accent2": '#e74c3c', "name": '灰白红北欧', "text_color": '#2c3e50', "theme": 'scandinavian'},
    "scandinavian_2": {"bg": '#e8e0d5', "accent1": '#5d4e37', "accent2": '#8b7355', "name": '棕木北欧', "text_color": '#3c2f2f', "theme": 'scandinavian'},
    "scandinavian_3": {"bg": '#f0ebe3', "accent1": '#1a5276', "accent2": '#2e86c1', "name": '蓝白北欧', "text_color": '#1a3c5e', "theme": 'scandinavian'},
    "scandinavian_4": {"bg": '#eae4d9', "accent1": '#4a6741', "accent2": '#7dcea0', "name": '绿白北欧', "text_color": '#2d3a2d', "theme": 'scandinavian'},
    "boho_1": {"bg": '#f5e6d3', "accent1": '#c0392b', "accent2": '#d4a373', "name": '暖棕波西', "text_color": '#5c3a21', "theme": 'boho'},
    "boho_2": {"bg": '#e8d5b7', "accent1": '#8b4513', "accent2": '#cd853f', "name": '棕金波西', "text_color": '#3c2415', "theme": 'boho'},
    "boho_3": {"bg": '#f0e0c0', "accent1": '#16a34a', "accent2": '#d4a373', "name": '绿棕波西', "text_color": '#2d4a2d', "theme": 'boho'},
    "boho_4": {"bg": '#e0d0b0', "accent1": '#7c3aed', "accent2": '#d4a373', "name": '紫棕波西', "text_color": '#3c2415', "theme": 'boho'},
    "rain_1": {"bg": '#2c3e50', "accent1": '#3498db', "accent2": '#95a5a6', "name": '蓝灰雨天', "theme": 'rain'},
    "rain_2": {"bg": '#1a2a3a', "accent1": '#5dade2', "accent2": '#aab7b8', "name": '深蓝雨天', "theme": 'rain'},
    "rain_3": {"bg": '#34495e', "accent1": '#85c1e9', "accent2": '#d5dbdb', "name": '浅蓝雨天', "theme": 'rain'},
    "rain_4": {"bg": '#1c2833', "accent1": '#7fb3d8', "accent2": '#566573', "name": '暗灰雨天', "theme": 'rain'},
    "sunset_1": {"bg": 'linear-gradient(180deg,#ff6b35 0%,#f7931e 30%,#c0392b 70%,#4a0028 100%)', "accent1": '#ffd700', "accent2": '#ffffff', "name": '橙红日落', "is_gradient": True, "theme": 'sunset'},
    "sunset_2": {"bg": 'linear-gradient(180deg,#ff9a56 0%,#e74c3c 50%,#8b0000 100%)', "accent1": '#ffd700', "accent2": '#fff', "name": '暖红日落', "is_gradient": True, "theme": 'sunset'},
    "sunset_3": {"bg": 'linear-gradient(180deg,#feca57 0%,#ff6b6b 50%,#5f27cd 100%)', "accent1": '#ffffff', "accent2": '#ffd700', "name": '紫橙日落', "is_gradient": True, "theme": 'sunset'},
    "sunset_4": {"bg": '#2d0a1a', "accent1": '#ff6b35', "accent2": '#feca57', "name": '暗调日落', "theme": 'sunset'},
    "forest_1": {"bg": '#0a1a0a', "accent1": '#22c55e', "accent2": '#15803d', "name": '深绿森林', "theme": 'forest'},
    "forest_2": {"bg": '#0d2818', "accent1": '#4ade80', "accent2": '#166534', "name": '亮绿森林', "theme": 'forest'},
    "forest_3": {"bg": '#1a2e1a', "accent1": '#86efac', "accent2": '#14532d', "name": '浅绿森林', "theme": 'forest'},
    "forest_4": {"bg": '#0a1a0f', "accent1": '#10b981', "accent2": '#065f46', "name": '翠绿森林', "theme": 'forest'},
    "desert_1": {"bg": '#f5e6d3', "accent1": '#d4a373', "accent2": '#c0392b', "name": '暖棕沙漠', "text_color": '#5c3a21', "theme": 'desert'},
    "desert_2": {"bg": '#e8d5b7', "accent1": '#e76f51', "accent2": '#f4a261', "name": '橙棕沙漠', "text_color": '#3c2415', "theme": 'desert'},
    "desert_3": {"bg": '#f0e0c0', "accent1": '#d4a373', "accent2": '#8b4513', "name": '金沙沙漠', "text_color": '#3c2415', "theme": 'desert'},
    "desert_4": {"bg": '#e0c8a0', "accent1": '#c0392b', "accent2": '#daa520', "name": '红金沙漠', "text_color": '#3c2415', "theme": 'desert'},
    "vintage_1": {"bg": '#f5e6d3', "accent1": '#8b4513', "accent2": '#d4a373', "name": '暖棕复古', "text_color": '#3c2415', "theme": 'vintage'},
    "vintage_2": {"bg": '#e8d5b7', "accent1": '#b8860b', "accent2": '#cd853f', "name": '金棕复古', "text_color": '#3c2415', "theme": 'vintage'},
    "vintage_3": {"bg": '#d4c5a9', "accent1": '#556b2f', "accent2": '#8b7355', "name": '绿棕复古', "text_color": '#2d3a2d', "theme": 'vintage'},
    "vintage_4": {"bg": '#e0d0b0', "accent1": '#a0522d', "accent2": '#daa520', "name": '红棕复古', "text_color": '#3c2415', "theme": 'vintage'},
    "cherry_1": {"bg": '#fdf2f8', "accent1": '#ec4899', "accent2": '#f9a8d4', "name": '粉嫩樱花', "text_color": '#831843', "theme": 'cherry'},
    "cherry_2": {"bg": '#fce7f3', "accent1": '#db2777', "accent2": '#f472b6', "name": '深粉樱花', "text_color": '#831843', "theme": 'cherry'},
    "cherry_3": {"bg": '#fff1f2', "accent1": '#e11d48', "accent2": '#fda4af', "name": '红粉樱花', "text_color": '#881337', "theme": 'cherry'},
    "cherry_4": {"bg": '#f5f0ff', "accent1": '#a855f7', "accent2": '#e879f9', "name": '紫粉樱花', "text_color": '#581c87', "theme": 'cherry'},
    "woodcut_1": {"bg": '#f5f0e0', "accent1": '#1a1a1a', "accent2": '#8b4513', "name": '黑白木刻', "text_color": '#1a1a1a', "theme": 'woodcut'},
    "woodcut_2": {"bg": '#e8e0c8', "accent1": '#2c2c2c', "accent2": '#a0522d', "name": '棕黑木刻', "text_color": '#2c2c2c', "theme": 'woodcut'},
    "woodcut_3": {"bg": '#1a1a1a', "accent1": '#f5f0e0', "accent2": '#c0392b', "name": '反转木刻', "theme": 'woodcut'},
    "woodcut_4": {"bg": '#f0e8d0', "accent1": '#333333', "accent2": '#8b0000', "name": '深色木刻', "text_color": '#333333', "theme": 'woodcut'},
    "plaid_1": {"bg": '#1e3a5f', "accent1": '#dc2626', "accent2": '#fbbf24', "name": '红蓝格纹', "theme": 'plaid'},
    "plaid_2": {"bg": '#2d4a2d', "accent1": '#daa520', "accent2": '#8b0000', "name": '绿金格纹', "theme": 'plaid'},
    "plaid_3": {"bg": '#3c1515', "accent1": '#fbbf24', "accent2": '#1e3a5f', "name": '红金格纹', "theme": 'plaid'},
    "plaid_4": {"bg": '#1a1a2e', "accent1": '#e94560', "accent2": '#ffd700', "name": '紫红格纹', "theme": 'plaid'},
    "origami_1": {"bg": '#f5f0e8', "accent1": '#e74c3c', "accent2": '#3498db', "name": '红蓝折纸', "text_color": '#2c3e50', "theme": 'origami'},
    "origami_2": {"bg": '#e8e0d0', "accent1": '#2ecc71', "accent2": '#f39c12', "name": '绿黄折纸', "text_color": '#2c3e50', "theme": 'origami'},
    "origami_3": {"bg": '#f0ebe3', "accent1": '#9b59b6', "accent2": '#1abc9c', "name": '紫绿折纸', "text_color": '#2c3e50', "theme": 'origami'},
    "origami_4": {"bg": '#eae4d9', "accent1": '#e67e22', "accent2": '#2980b9', "name": '橙蓝折纸', "text_color": '#2c3e50', "theme": 'origami'},
    "paperplane_1": {"bg": '#87ceeb', "accent1": '#ffffff', "accent2": '#2563eb', "name": '蓝天纸飞机', "text_color": '#1e3a5f', "theme": 'paperplane'},
    "paperplane_2": {"bg": '#e0f2fe', "accent1": '#0ea5e9', "accent2": '#ffffff', "name": '浅蓝纸飞机', "text_color": '#0c4a6e', "theme": 'paperplane'},
    "paperplane_3": {"bg": '#f0f9ff', "accent1": '#3b82f6', "accent2": '#93c5fd', "name": '亮蓝纸飞机', "text_color": '#1e40af', "theme": 'paperplane'},
    "paperplane_4": {"bg": '#0ea5e9', "accent1": '#ffffff', "accent2": '#fbbf24', "name": '蓝白纸飞机', "theme": 'paperplane'},
    "lofi_1": {"bg": '#2d1b4e', "accent1": '#e9a0ff', "accent2": '#feca57', "name": '紫金lofi', "theme": 'lofi'},
    "lofi_2": {"bg": '#1a1a2e', "accent1": '#ff9a9e', "accent2": '#fad0c4', "name": '粉暖lofi', "theme": 'lofi'},
    "lofi_3": {"bg": '#2d2d44', "accent1": '#a0c4ff', "accent2": '#bdb2ff', "name": '蓝紫lofi', "theme": 'lofi'},
    "lofi_4": {"bg": '#1e1e30', "accent1": '#caffbf', "accent2": '#fdffb6', "name": '绿黄lofi', "theme": 'lofi'},

    "wave_1": {"bg": "#0a1628", "accent1": "#38bdf8", "accent2": "#0ea5e9", "name": "蓝波", "theme": "wave"},
    "wave_2": {"bg": "#0d2137", "accent1": "#67e8f9", "accent2": "#0284c7", "name": "青波", "theme": "wave"},
    "wave_3": {"bg": "#1a2a3a", "accent1": "#7dd3fc", "accent2": "#0369a1", "name": "深蓝波", "theme": "wave"},
    "wave_4": {"bg": "#0a192f", "accent1": "#22d3ee", "accent2": "#0ea5e9", "name": "亮蓝波", "theme": "wave"},
    "fairy_1": {"bg": "linear-gradient(135deg,#a78bfa 0%,#f0abfc 50%,#fde68a 100%)", "accent1": "#ffffff", "accent2": "#7c3aed", "name": "紫粉童话", "is_gradient": True, "theme": "fairy"},
    "fairy_2": {"bg": "#f5f0ff", "accent1": "#8b5cf6", "accent2": "#ec4899", "name": "粉紫童话", "text_color": "#581c87", "theme": "fairy"},
    "fairy_3": {"bg": "#fdf2f8", "accent1": "#a855f7", "accent2": "#f472b6", "name": "亮粉童话", "text_color": "#831843", "theme": "fairy"},
    "fairy_4": {"bg": "linear-gradient(135deg,#c084fc 0%,#f9a8d4 100%)", "accent1": "#ffffff", "accent2": "#7c3aed", "name": "渐变童话", "is_gradient": True, "theme": "fairy"},
    "military_1": {"bg": "#1a1a0a", "accent1": "#4a5d23", "accent2": "#8b7355", "name": "军绿", "theme": "military"},
    "military_2": {"bg": "#0d0d00", "accent1": "#6b8e23", "accent2": "#556b2f", "name": "深绿军事", "theme": "military"},
    "military_3": {"bg": "#2a2a10", "accent1": "#bdb76b", "accent2": "#556b2f", "name": "黄绿军事", "theme": "military"},
    "military_4": {"bg": "#0a0a00", "accent1": "#808000", "accent2": "#2f4f2f", "name": "暗绿军事", "theme": "military"},
    "cloud_1": {"bg": "#e0f2fe", "accent1": "#0ea5e9", "accent2": "#38bdf8", "name": "蓝白云", "text_color": "#0c4a6e", "theme": "cloud"},
    "cloud_2": {"bg": "#f0f9ff", "accent1": "#0284c7", "accent2": "#7dd3fc", "name": "浅蓝云", "text_color": "#075985", "theme": "cloud"},
    "cloud_3": {"bg": "#f8fafc", "accent1": "#3b82f6", "accent2": "#93c5fd", "name": "灰白云", "text_color": "#1e3a5f", "theme": "cloud"},
    "cloud_4": {"bg": "#e0e7ff", "accent1": "#6366f1", "accent2": "#a5b4fc", "name": "紫蓝云", "text_color": "#3730a3", "theme": "cloud"},
    "earth_1": {"bg": "#0a1a0a", "accent1": "#22c55e", "accent2": "#0ea5e9", "name": "绿蓝地球", "theme": "earth"},
    "earth_2": {"bg": "#0d1b2a", "accent1": "#10b981", "accent2": "#3b82f6", "name": "蓝绿地球", "theme": "earth"},
    "earth_3": {"bg": "#1a2e1a", "accent1": "#4ade80", "accent2": "#38bdf8", "name": "亮绿地球", "theme": "earth"},
    "earth_4": {"bg": "#0a1628", "accent1": "#22d3ee", "accent2": "#22c55e", "name": "青绿地球", "theme": "earth"},
}

# ===== 风格结构分类 =====
THEME_CATEGORIES = {
    "科技知识": {
        "icon": "🚀",
        "desc": "适合编程、AI、技术教程、知识科普、工程",
        "themes": ["bold", "cyber", "minimal", "magazine", "pixel", "glass", "aurora", "blueprint", "typewriter", "starfield", "glitch", "synthwave", "matrix", "quantum", "ocean", "ice", "glassmorph", "retrofuturism", "galaxy", "cloud"],
    },
    "生活娱乐": {
        "icon": "🎉",
        "desc": "适合搞笑、美食、游戏、综艺、宠物、儿童",
        "themes": ["funny", "food", "gaming", "variety", "cute", "clay", "carnival", "popart", "candy"],
    },
    "视觉冲击": {
        "icon": "💥",
        "desc": "适合热点、评测、开箱、撕纸拼贴、潮流、街头",
        "themes": ["paper", "dopamine", "doodle", "luxury", "vaporwave", "acid", "memphis", "comic", "neon", "graffiti", "brutalist", "holographic", "gradientmesh", "screenshot", "portrait", "product", "contrast", "zoom", "steampunk", "noir", "gothic", "baroque", "tribal", "artdeco", "fire", "streetwear", "psychadelic", "mosaic", "newspaper2", "techwear", "cyberpunk2", "neoncity", "medieval", "military"],
    },
    "文艺清新": {
        "icon": "🍃",
        "desc": "适合Vlog、旅行、动漫、手账、国风、复古、自然",
        "themes": ["fresh", "anime", "cinema", "journal", "guochao", "sticker", "retro", "collage", "ink", "stamp", "newspaper", "polaroid", "risograph", "film", "ribbon", "pastel", "terrarium", "kraft", "washi", "watercolor", "zen", "scandinavian", "boho", "rain", "sunset", "forest", "desert", "vintage", "cherry", "woodcut", "plaid", "origami", "paperplane", "lofi", "wave", "fairy", "earth"],
    },
}

THEME_KEYWORDS = {
    "bold": ["干货","教程","知识","必看","入门","指南","科普","总结","万字","硬核","速成","避坑"],
    "cyber": ["AI","赛博","未来","霓虹","代码","编程","程序","服务器","Shell","API","CLI","Key","密钥","模型","Ollama","qwen","GPT","IDE","云","大模型","Agent"],
    "anime": ["二次元","动漫","番剧","虚拟","萌","动画","日漫","cosplay"],
    "funny": ["搞笑","整活","沙雕","表情包","吐槽","鬼畜","名场面","爆笑","离谱","抽象"],
    "luxury": ["评测","高端","旗舰","Pro","Max","豪华","奢华","开箱","体验","深度","测评"],
    "fresh": ["Vlog","生活","旅行","日常","治愈","清新","慢生活","记录"],
    "gaming": ["游戏","电竞","对战","吃鸡","王者","原神","Steam","FPS","MOBA","通关","攻略"],
    "food": ["美食","探店","烹饪","吃","做饭","料理","烘焙","食谱","吃货","外卖"],
    "cinema": ["电影","影视","悬疑","恐怖","解说","剧情","惊悚","科幻","影评","拆解"],
    "cute": ["可爱","宠物","猫","狗","熊猫","狐狸","卡通","萌宠","治愈系","手帐","动物"],
    "paper": ["安利","推荐","攻略","评测","对比","排行","盘点","合集","总结","撕","拼贴"],
    "variety": ["热点","吃瓜","反转","震惊","弹幕","名场面","反应","绝了","崩溃"],
    "doodle": ["手帐","手绘","涂鸦","文创","日记","笔记","创意","DIY","手作","画"],
    "magazine": ["商业","财经","深度","报道","访谈","专题","周刊","趋势","分析","白皮书","行业"],
    "minimal": ["极简","简约","设计","美学","留白","高级感","性冷感","黑白","商务","专业"],
    "dopamine": ["多巴胺","撞色","潮流","快乐","元气","夏日","色彩","穿搭","活力","开心"],
    "guochao": ["国潮","国风","传统","文化","汉服","古风","中国","非遗","东方","水墨"],
    "pixel": ["像素","复古","8bit","游戏","街机","红白机","怀旧","极客","像素画","像素风"],
    "journal": ["手账","手帐","笔记","日记","记录","计划","打卡","日程","规划","手写"],
    "tech": ["AI","Shell","API","代码","编程","程序","服务器","云","IDE","CLI","Key","密钥","模型","Ollama","qwen","GPT"],
    "hot": ["教程","入门","实战","安装","部署","上线","新手","快速"],
    "cool": ["Docker","容器","MySQL","Redis","数据库","缓存","Portainer","Nginx"],
    "warm": ["对话","客服","设计","生活","沟通","SSE","流式"],
    "dark": ["安全","黑客","高级","硬核","渗透","密码"],
    "gradient": ["时尚","创意","爆款","热门","推荐"],
    "animal": ["萌","可爱","治愈","动物","宠物","猫","狗","熊猫","狐狸","卡通"],
    "vaporwave": ["蒸汽波","vaporwave","复古","迷幻","故障","80s","90s","怀旧","录像带"],
    "acid": ["酸性","acid","液态","金属","荧光","扭曲","实验","前卫","赛博","y2k"],
    "memphis": ["孟菲斯","memphis","几何","波点","折线","色块","活泼","拼接","撞色"],
    "clay": ["黏土","clay","3D","立体","圆润","柔软","手工","童趣","可爱","捏"],
    "glass": ["玻璃","glass","拟态","模糊","半透明","毛玻璃","高级感","质感","通透"],
    "sticker": ["贴纸","sticker","手绘","可爱","拼贴","白边","卡通","贴画","装饰"],
    "comic": ["漫画","comic","描边","气泡","网点","美漫","日漫","热血","格斗"],
    "neon": ["霓虹","neon","灯管","发光","荧光","暗夜","招牌","夜店","赛博"],
    "retro": ["复古","retro","怀旧","胶片","做旧","80年代","90年代","复古风","老照片"],
    "collage": ["拼贴","collage","剪报","胶带","混合","材质","手做","文艺","剪贴"],
    "aurora": ["极光","弥散光","光晕","梦幻","渐变","模糊","光影","星空","深空","弥散"],
    "ink": ["水墨","书法","国画","写意","山水","笔墨","丹青","留白","枯笔","东方"],
    "stamp": ["印章","篆刻","朱印","盖章","钢印","印记","印鉴","章法","钤印","落款"],
    "newspaper": ["报纸","新闻","报道","头条","刊号","日报","周报","头版","专栏","社论"],
    "polaroid": ["拍立得","宝丽来","即时成像","白边","相框","照片","冲洗","胶卷","回忆","旅行照"],
    "risograph": ["riso","孔版印刷","丝网印","双色印刷","复古印刷","颗粒","独立出版","zine","版画","手工印刷"],
    "film": ["胶片","电影","帧","胶卷","放映","片场","镜头","35mm","8mm","胶片相机"],
    "graffiti": ["涂鸦","街头","喷漆","墙绘","野生","地铁涂鸦","滑板","嘻哈","街头文化","反叛"],
    "ribbon": ["缎带","丝带","横幅","奖项","颁奖","礼盒","优雅","典礼","表彰","花环"],
    "gradientmesh": ["网格渐变","柔和渐变","梦幻渐变","多色渐变","平滑过渡","mesh","流体渐变","云朵渐变","柔和色彩","梦幻背景"],
    "brutalist": ["粗野主义","野兽派","原始","混凝土","粗犷","极简粗野","建筑感","结构","块面","野性"],
    "pastel": ["莫兰迪","柔色","低饱和","高级灰","柔和","温和","内敛","雅致","灰调","燕麦色"],
    "popart": ["波普","波普艺术","安迪沃霍尔","利希滕斯坦","撞色波普","大众艺术","消费主义","明星","撞色","网点"],
    "terrarium": ["生态缸","植物","玻璃缸","微景观","多肉","苔藓","绿植","自然","森林","花园"],
    "holographic": ["全息","镭射","彩虹","幻彩","偏光","炫彩","激光","hips","珠光","变色龙"],
    "kraft": ["牛皮纸","纸袋","手工纸","包装纸","原色纸","复古纸","粗糙","手工","质朴","原生态"],
    "blueprint": ["蓝图","工程图","制图","建筑图","技术图","设计图","施工图","图纸","测绘","规划"],
    "starfield": ["星空","宇宙","银河","深空","星海","星云","天文","行星","太阳系","星座"],
    "washi": ["和纸","胶带","纸胶带","和风","日式","手帐胶带","拼贴胶带","装饰胶带","纸胶带","日本纸"],
    "typewriter": ["打字机","机械","复古打字","手稿","文稿","手写","旧体","文字稿","打印","字稿"],
    "carnival": ["嘉年华","马戏团","狂欢","庆典","游乐园","派对","热闹","庆祝","节日","表演"],
    "screenshot": ["截图","实操","演示","实战","案例","看代码","读源码","源码","跑一遍","现场"],
    "portrait": ["经验","职业","分享","我","个人","出镜","老码农","转行","面试","程序员","开发","工作"],
    "product": ["开箱","测评","评测","产品","体验","工具","神器","效率","APP","硬件","键盘","MacBook","iPad"],
    "contrast": ["对比","vs","区别","选择","哪个好","比较","较量","盘点","TOP","排行榜"],
    "zoom": ["细节","重点","局部","放大","特写","深入","看这个","注意","记住","这几点"],

    "glitch": ["故障","glitch","错误","bug","崩溃","异常","干扰","信号","失真","花屏"],
    "synthwave": ["synthwave","合成波","retrowave","80年代","霓虹","落日","棕榈","网格","复古未来"],
    "matrix": ["matrix","矩阵","代码雨","黑客","绿色","终端","命令行","01","二进制"],
    "quantum": ["量子","quantum","纠缠","叠加","计算","物理","粒子","波函数"],
    "ocean": ["海洋","ocean","深海","蓝色","水下","珊瑚","鱼群","波浪"],
    "ice": ["冰","ice","冰晶","寒冷","蓝色","透明","霜","雪","冻"],
    "glassmorph": ["毛玻璃","frosted","模糊","透明","质感","高级","UI","设计"],
    "retrofuturism": ["复古未来","retrofuturism","未来主义","飞车","太空","原子","60年代","科幻"],
    "galaxy": ["银河","galaxy","星系","宇宙","太空","行星","黑洞","星云"],
    "candy": ["糖果","candy","甜蜜","粉色","可爱","棒棒糖","蛋糕","奶茶"],
    "steampunk": ["蒸汽朋克","steampunk","齿轮","机械","铜","维多利亚","蒸汽","发条"],
    "noir": ["黑色","noir","侦探","犯罪","暗影","黑白","悬疑","电影","硬汉"],
    "gothic": ["哥特","gothic","暗黑","黑暗","中世纪","城堡","尖塔","玫瑰","十字架"],
    "baroque": ["巴洛克","baroque","华丽","繁复","金饰","宫廷","古典","欧洲","皇室"],
    "tribal": ["部落","tribal","图腾","原始","非洲","面具","纹样","狩猎","自然"],
    "artdeco": ["装饰艺术","art deco","几何","对称","金色","20年代","纽约","帝国大厦"],
    "fire": ["火","fire","烈焰","燃烧","热","爆炸","能量","火山"],
    "streetwear": ["街头","street","潮牌","滑板","嘻哈","涂鸦","限量","sneaker"],
    "psychadelic": ["迷幻","psychedelic","万花筒","彩虹","旋涡","荧光","60年代","嬉皮"],
    "mosaic": ["马赛克","mosaic","像素","拼图","方块","瓷砖","拼接","几何"],
    "newspaper2": ["头版","头条","breaking","新闻","紧急","突发","报道","号外"],
    "techwear": ["机能","techwear","工装","战术","户外","防水","反光","黑色","装备"],
    "cyberpunk2": ["废土","wasteland","末日","废墟","残破","荒芜","辐射","核爆"],
    "neoncity": ["霓虹","neon","城市","city","夜景","灯光","繁华","都市"],
    "medieval": ["中世纪","medieval","骑士","城堡","剑","盾","王国","龙"],
    "watercolor": ["水彩","watercolor","晕染","透明","渐变","画笔","颜料","湿画","流动"],
    "zen": ["禅","zen","侘寂","wabi-sabi","枯山水","茶道","空寂","留白","自然"],
    "scandinavian": ["北欧","scandinavian","极简","木质","自然","温暖","hygge","斯堪的纳维亚"],
    "boho": ["波西米亚","boho","bohemian","自由","流苏","民族","旅行","嬉皮","花卉"],
    "rain": ["雨","rain","雨天","水滴","窗户","灰蒙","潮湿","忧郁","安静"],
    "sunset": ["日落","sunset","黄昏","晚霞","橙色","紫色","天空","暮色"],
    "forest": ["森林","forest","树木","绿色","自然","深林","苔藓","蘑菇"],
    "desert": ["沙漠","desert","沙丘","骆驼","仙人掌","干燥","暖色","黄沙"],
    "vintage": ["vintage","复古","怀旧","老照片","旧时光","80后","90后","经典"],
    "cherry": ["樱花","cherry","粉色","春天","浪漫","花瓣","少女","粉色系"],
    "woodcut": ["版画","woodcut","木刻","黑白","线条","雕刻","印刷","木版"],
    "plaid": ["格纹","plaid","学院","英伦","苏格兰","校服","preppy","经典"],
    "origami": ["折纸","origami","纸艺","手工","折叠","千纸鹤","纸飞机","立体"],
    "paperplane": ["纸飞机","paper plane","飞翔","蓝天","梦想","童年","白纸","天空"],
    "lofi": ["lofi","lo-fi","慵懒","放松","音乐","咖啡","深夜","学习","白噪音"],
    "wave": ["波浪","wave","涟漪","水纹","流动","海浪","波纹","起伏"],
    "fairy": ["童话","fairy","梦幻","魔法","精灵","公主","城堡","魔法棒"],
    "military": ["军事","military","军队","战术","作战","迷彩","军用","硬核","武器"],
    "cloud": ["云","cloud","云端","轻盈","飘浮","天空","棉花","柔软"],
    "earth": ["地球","earth","生态","环保","绿色","可持续","碳中和","自然","蓝色星球"],

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
    "magazine": [("1f4f0","📰"),("1f4d0","📐"),("1f3a8","🎨"),("1f451","👑"),("1f4ca","📊")],
    "minimal": [("26aa","⚪"),("26ab","⚫"),("25fc","◼️"),("25fb","◻️"),("1f539","🔹")],
    "dopamine": [("1f308","🌈"),("1f389","🎉"),("1f31f","🌟"),("2728","✨"),("1f4ab","💫"),("1f3c6","🏆")],
    "guochao": [("1f380","🎴"),("1f534","🔴"),("1f4e0","🎏"),("1f3a8","🎨"),("1f31e","🌕")],
    "pixel": [("1f3ae","🎮"),("1f47e","👾"),("1f3a8","🎨"),("1f4a5","💥"),("26a1","⚡")],
    "journal": [("1f4d3","📓"),("1f4dd","📝"),("270f","✏️"),("1f4cc","📌"),("1f4c4","📄"),("1f3a8","🎨")],
    "tech": [("1f680","🚀"),("26a1","⚡"),("1f4bb","💻"),("1f310","🌐"),("1f527","🔧"),("1f4e1","📡")],
    "hot": [("1f525","🔥"),("2b50","⭐"),("1f4a5","💥"),("1f3af","🎯"),("1f389","🎉")],
    "cool": [("1f433","🐳"),("1f4e6","📦"),("1f5c3","🗄️"),("1f510","🔐"),("1f4be","💾")],
    "warm": [("1f49b","💛"),("1f4ac","💬"),("1f917","🤗"),("1f4f1","📱"),("2728","✨")],
    "dark": [("1f576","🕶️"),("1f512","🔒"),("1f480","💀"),("1f451","👑"),("1f9e0","🧠")],
    "gradient": [("2728","✨"),("1f308","🌈"),("1f4ab","💫"),("1f31f","🌟"),("1f48e","💎")],
    "animal": [("1f431","🐱"),("1f436","🐶"),("1f98a","🦊"),("1f43c","🐼"),("1f428","🐨"),("1f42f","🐯"),("1f981","🦁"),("1f438","🐸"),("1f419","🐙"),("1f989","🦉"),("1f984","🦄"),("1f41d","🐝"),("1f98b","🦋")],
    "vaporwave": [("1f47e","👾"),("1f3a8","🎨"),("1f31f","🌟"),("1f4a5","💥"),("1f300","🌀"),("1f47b","👻"),("1f3b5","🎵")],
    "acid": [("1f4a5","💥"),("1f300","🌀"),("1f4ab","💫"),("1f7e1","🟡"),("1f7e2","🟢"),("1f7e3","🟣"),("1f525","🔥")],
    "memphis": [("1f3a8","🎨"),("2b50","⭐"),("1f4ab","💫"),("1f380","🎀"),("26ab","⚫"),("1f7e0","🟠"),("1f7e1","🟡")],
    "clay": [("1f476","👶"),("1f388","🎈"),("1f370","🍰"),("1f47d","👽"),("1f434","🐴"),("1f431","🐱"),("1f436","🐶")],
    "glass": [("1f539","🔹"),("1f53a","🔺"),("1f300","🌀"),("26aa","⚪"),("1f4ab","💫"),("2728","✨")],
    "sticker": [("1f389","🎉"),("2b50","⭐"),("1f380","🎀"),("1f496","💖"),("1f3a8","🎨"),("1f4ab","💫")],
    "comic": [("1f4ac","💬"),("1f4a5","💥"),("2753","❓"),("2764","❤️"),("1f621","😡"),("1f606","😆"),("1f4f0","📰")],
    "neon": [("1f3a8","🎨"),("26a1","⚡"),("1f50c","🔌"),("1f4a5","💥"),("1f525","🔥"),("1f31f","🌟")],
    "retro": [("1f4f7","📷"),("1f3a8","🎨"),("1f4c4","📄"),("1f451","👑"),("1f3b5","🎵"),("1f4fb","📻")],
    "collage": [("1f4cc","📌"),("2702","✂️"),("1f4dd","📝"),("1f4c4","📄"),("1f3a8","🎨"),("1f4bc","💼")],
    "aurora":    [("1f30c","🌌"),("2728","✨"),("1f4ab","💫"),("1f31f","🌟"),("1f300","🌀"),("1f315","🌕")],
    "ink":       [("1f3a8","🎨"),("1f4dd","📝"),("270f","✏️"),("1f31e","🌕"),("1f340","🍀")],
    "stamp":     [("1f4e0","📠"),("1f3a8","🎨"),("2705","✅"),("1f4d0","📐"),("1f539","🔹")],
    "newspaper": [("1f4f0","📰"),("1f4d0","📐"),("1f4ca","📊"),("1f4dd","📝"),("1f3a8","🎨")],
    "polaroid":  [("1f4f7","📷"),("1f4f8","📸"),("1f3a8","🎨"),("1f381","🎁"),("1f389","🎉")],
    "risograph": [("1f3a8","🎨"),("1f4c4","📄"),("1f4dd","📝"),("2728","✨"),("1f31f","🌟")],
    "film":      [("1f39e","🎞️"),("1f4f7","📷"),("1f3ac","🎬"),("1f4fd","📽️"),("1f3a4","🎤")],
    "graffiti":  [("1f3a8","🎨"),("1f4a5","💥"),("1f525","🔥"),("26a1","⚡"),("1f476","👶")],
    "ribbon":    [("1f380","🎀"),("1f3c6","🏆"),("1f381","🎁"),("1f397","🎗️"),("1f9e1","🧡")],
    "gradientmesh": [("1f308","🌈"),("2728","✨"),("1f4ab","💫"),("1f31f","🌟"),("1f300","🌀")],
    "brutalist": [("2b50","⭐"),("25fc","◼️"),("25fb","◻️"),("1f4a5","💥"),("1f539","🔹")],
    "pastel":    [("1f49b","💛"),("1f49c","💚"),("1f49a","💚"),("1f48e","💎"),("1f3a8","🎨")],
    "popart":    [("1f3a8","🎨"),("1f4a5","💥"),("2b50","⭐"),("1f31f","🌟"),("1f389","🎉"),("1f4ab","💫")],
    "terrarium": [("1f331","🌱"),("1f33f","🌿"),("1f343","🍃"),("1f33c","🌼"),("1f490","💐"),("1f338","🌸")],
    "holographic": [("1f308","🌈"),("2728","✨"),("1f4ab","💫"),("1f31f","🌟"),("1f300","🌀"),("1f48e","💎")],
    "kraft":     [("1f4c4","📄"),("1f4dd","📝"),("1f9f4","🧴"),("1f6cd","🛍"),("1f381","🎁")],
    "blueprint": [("1f4d0","📐"),("1f527","🔧"),("2699","⚙️"),("1f539","🔹"),("1f4bb","💻")],
    "starfield": [("1f30c","🌌"),("2728","✨"),("1f31f","🌟"),("1f4ab","💫"),("1f315","🌕"),("1f300","🌀")],
    "washi":     [("1f380","🎀"),("1f3a8","🎨"),("1f4cc","📌"),("2702","✂️"),("1f4dd","📝")],
    "typewriter": [("2328","⌨"),("1f4dd","📝"),("1f4c4","📄"),("1f4d6","📖"),("270f","✏️")],
    "carnival":  [("1f38a","🎊"),("1f381","🎁"),("1f3aa","🎪"),("1f389","🎉"),("1f380","🎀"),("1f3b2","🎲")],
    "screenshot": [("1f4bb","💻"),("1f4c4","📄"),("1f4ca","📊"),("1f3a8","🎨"),("1f50d","🔍"),("1f4dd","📝")],
    "portrait":   [("1f464","👤"),("1f466","👦"),("1f467","👧"),("1f468","👨"),("1f469","👩"),("1f476","👶")],
    "product":    [("1f4f1","📱"),("1f4bb","💻"),("1f3a8","🎨"),("2b50","⭐"),("1f680","🚀"),("1f389","🎉")],
    "contrast":   [("1f4a5","💥"),("1f19a","🆚"),("1f525","🔥"),("26a1","⚡"),("1f3af","🎯"),("1f4ca","📊")],
    "zoom":       [("1f50d","🔍"),("1f3af","🎯"),("1f4cc","📌"),("1f525","🔥"),("26a1","⚡"),("2b50","⭐")],

    "glitch": [("1f4a5","💥"),("1f4f0","📰"),("26a1","⚡"),("1f527","🔧")],
    "synthwave": [("1f305","🌅"),("1f308","🌈"),("1f4a5","💥"),("1f525","🔥")],
    "matrix": [("1f4bb","💻"),("1f4a1","💡"),("26a1","⚡"),("1f527","🔧")],
    "quantum": [("269b","⚛"),("1f30c","🌌"),("2728","✨"),("1f9ec","🧬")],
    "ocean": [("1f30a","🌊"),("1f41f","🐟"),("1f42c","🐬"),("1f3dd","🏝")],
    "ice": [("2744","❄"),("2603","⛄"),("1f4a7","💧"),("1f328","🌨")],
    "glassmorph": [("1f539","🔹"),("2728","✨"),("1f4ab","💫"),("26aa","⚪")],
    "retrofuturism": [("1f680","🚀"),("1f30c","🌌"),("2728","✨"),("1f47e","👾")],
    "galaxy": [("1f30c","🌌"),("2b50","⭐"),("1f4ab","💫"),("1f31f","🌟")],
    "candy": [("1f36c","🍬"),("1f36d","🍭"),("1f370","🍰"),("1f9c1","🧁")],
    "steampunk": [("2699","⚙"),("1f527","🔧"),("1f4a1","💡"),("26a1","⚡")],
    "noir": [("1f3ac","🎬"),("1f576","🕶"),("1f480","💀"),("1f50d","🔍")],
    "gothic": [("1f987","🦇"),("1f480","💀"),("2620","☠"),("1f56f","🕯")],
    "baroque": [("1f451","👑"),("1f48e","💎"),("2728","✨"),("1f3a9","🎩")],
    "tribal": [("1f5ff","🗿"),("1f3dd","🏝"),("1f3b2","🎲"),("1f525","🔥")],
    "artdeco": [("1f48e","💎"),("2728","✨"),("1f451","👑"),("2b50","⭐")],
    "fire": [("1f525","🔥"),("1f4a5","💥"),("26a1","⚡"),("1f30b","🌋")],
    "streetwear": [("1f6f9","🛹"),("1f45f","👟"),("1f3a8","🎨"),("1f525","🔥")],
    "psychadelic": [("1f300","🌀"),("1f308","🌈"),("2728","✨"),("1f4ab","💫")],
    "mosaic": [("1f9e9","🧩"),("1f4a0","💠"),("25fb","◻"),("25fc","◼")],
    "newspaper2": [("1f4f0","📰"),("1f4ca","📊"),("1f4dd","📝"),("2757","❗")],
    "techwear": [("1f9e5","🧥"),("1f451","👑"),("26a1","⚡"),("1f6e1","🛡")],
    "cyberpunk2": [("1f3da","🏚"),("2622","☢"),("1f480","💀"),("1f525","🔥")],
    "neoncity": [("1f307","🌇"),("1f3d9","🏙"),("2728","✨"),("1f4a1","💡")],
    "medieval": [("2694","⚔"),("1f6e1","🛡"),("1f3f0","🏰"),("1f409","🐉")],
    "watercolor": [("1f3a8","🎨"),("1f58c","🖌"),("2728","✨"),("1f4ab","💫")],
    "zen": [("1fab6","🪴"),("2618","☘"),("1f343","🍃"),("1f371","🍱")],
    "scandinavian": [("1f332","🌲"),("2744","❄"),("2618","☕"),("1f36a","🍪")],
    "boho": [("1f33b","🌻"),("1f33a","🌺"),("1f3dd","🏝"),("2728","✨")],
    "rain": [("1f327","🌧"),("2614","☂"),("1f4a7","💧"),("1f32c","🌬")],
    "sunset": [("1f307","🌇"),("1f305","🌅"),("2728","✨"),("1f31f","🌟")],
    "forest": [("1f332","🌲"),("1f33f","🌿"),("1f344","🍄"),("1f43a","🐺")],
    "desert": [("1f3dc","🏜"),("1f42a","🐫"),("1f335","🌵"),("2600","☀")],
    "vintage": [("1f4fb","📻"),("1f4f7","📷"),("1f3a8","🎨"),("1f451","👑")],
    "cherry": [("1f338","🌸"),("1f49d","💝"),("2728","✨"),("1f33a","🌺")],
    "woodcut": [("1fab5","🪵"),("2702","✂"),("1f4dd","📝"),("1f3a8","🎨")],
    "plaid": [("1f393","🎓"),("1f4da","📚"),("2328","⌨"),("1f3a8","🎨")],
    "origami": [("1faba","🦢"),("2702","✂"),("1f4dd","📝"),("1f3a8","🎨")],
    "paperplane": [("2708","✈"),("2601","☁"),("1f308","🌈"),("2728","✨")],
    "lofi": [("1f3a7","🎧"),("2615","☕"),("1f4d6","📖"),("1f319","🌙")],
    "wave": [("1f30a","🌊"),("1f4a7","💧"),("2728","✨"),("1f300","🌀")],
    "fairy": [("1f9da","🧚"),("2728","✨"),("1f31f","🌟"),("1f4ab","💫")],
    "military": [("1f396","🎖"),("2708","✈"),("1f6e1","🛡"),("1f527","🔧")],
    "cloud": [("2601","☁"),("26a1","⚡"),("1f4bb","💻"),("1f680","🚀")],
    "earth": [("1f30d","🌍"),("1f331","🌱"),("1f33f","🌿"),("2728","✨")],

}

GENERAL_EMOJIS = [("1f680","🚀"),("26a1","⚡"),("1f4bb","💻"),("1f310","🌐"),
                  ("1f525","🔥"),("2b50","⭐"),("2728","✨"),("1f4a1","💡"),
                  ("1f3af","🎯"),("1f389","🎉"),("1f4aa","💪")]

TWEMOJI_CDN = "https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/svg"

# ========== Iconfont 本地卡通素材 ==========
ICONFONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "iconfont")

# 风格 → iconfont 分类映射
THEME_ICONFONT_MAP = {
    "cute":     "animal",
    "animal":   "animal",
    "funny":    "animal",
    "cyber":    "coder",
    "tech":     "tech",
    "bold":     "coder",
    "gaming":   "tech",
    "dark":     "coder",
    "food":     "food",
    "fresh":    "animal",
    "doodle":   "emoji",
    "variety":  "emoji",
    "anime":    "animal",
    "luxury":   "tech",
    "cinema":   "tech",
    "paper":    "coder",
    "hot":      "tech",
    "cool":     "coder",
    "warm":     "animal",
    "gradient": "animal",
    "magazine": "coder",
    "minimal":  "tech",
    "dopamine": "emoji",
    "guochao":  "animal",
    "pixel":    "tech",
    "journal":  "emoji",
    "vaporwave": "tech",
    "acid":      "tech",
    "memphis":   "emoji",
    "clay":      "animal",
    "glass":     "tech",
    "sticker":   "emoji",
    "comic":     "emoji",
    "neon":      "tech",
    "retro":     "animal",
    "collage":   "coder",
    "aurora":    "tech",
    "ink":       "animal",
    "stamp":     "coder",
    "newspaper": "coder",
    "polaroid":  "animal",
    "risograph": "emoji",
    "film":      "tech",
    "graffiti":  "emoji",
    "ribbon":    "emoji",
    "gradientmesh": "emoji",
    "brutalist": "coder",
    "pastel":    "animal",
    "popart":    "emoji",
    "terrarium": "animal",
    "holographic": "tech",
    "kraft":     "food",
    "blueprint": "coder",
    "starfield": "tech",
    "washi":     "emoji",
    "typewriter": "coder",
    "carnival":  "emoji",
    "screenshot": "tech",
    "portrait":   "animal",
    "product":    "tech",
    "contrast":   "emoji",
    "zoom":       "tech",

    "glitch":     "tech",
    "synthwave":     "tech",
    "matrix":     "coder",
    "quantum":     "tech",
    "ocean":     "animal",
    "ice":     "tech",
    "glassmorph":     "tech",
    "retrofuturism":     "tech",
    "galaxy":     "tech",
    "candy":     "food",
    "steampunk":     "tech",
    "noir":     "coder",
    "gothic":     "coder",
    "baroque":     "emoji",
    "tribal":     "animal",
    "artdeco":     "tech",
    "fire":     "tech",
    "streetwear":     "emoji",
    "psychadelic":     "emoji",
    "mosaic":     "emoji",
    "newspaper2":     "coder",
    "techwear":     "tech",
    "cyberpunk2":     "tech",
    "neoncity":     "tech",
    "medieval":     "coder",
    "watercolor":     "emoji",
    "zen":     "animal",
    "scandinavian":     "animal",
    "boho":     "animal",
    "rain":     "animal",
    "sunset":     "animal",
    "forest":     "animal",
    "desert":     "animal",
    "vintage":     "animal",
    "cherry":     "animal",
    "woodcut":     "coder",
    "plaid":     "coder",
    "origami":     "emoji",
    "paperplane":     "emoji",
    "lofi":     "animal",
    "wave":     "animal",
    "fairy":     "animal",
    "military":     "tech",
    "cloud":     "tech",
    "earth":     "animal",

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



def auto_fetch_icons(title, theme, count=3):
    """根据标题关键词自动从 iconfont.cn 搜索并下载图标"""
    import subprocess
    download_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "download_icons.py")
    if not os.path.exists(download_script):
        return []

    # 从标题提取关键词
    keywords = []
    # 去掉标点和常见停用词
    import re
    clean = re.sub(r'[！？。，、；：\u201c\u201d\u2018\u2019【】（）《》\s]+', ' ', title).strip()
    words = clean.split()
    for w in words:
        if len(w) >= 2 and len(w) <= 6:
            keywords.append(w)

    # 添加主题相关关键词
    theme_kw_map = {
        "cyber": ["代码", "编程", "科技"],
        "gaming": ["游戏", "手柄", "电竞"],
        "food": ["美食", "食物", "餐厅"],
        "cute": ["可爱", "动物", "萌"],
        "anime": ["动漫", "二次元"],
        "luxury": ["高端", "奢华"],
        "fresh": ["清新", "自然"],
    }
    keywords.extend(theme_kw_map.get(theme, [])[:1])

    if not keywords:
        return []

    # 检查是否已有足够的本地图标
    category = THEME_ICONFONT_MAP.get(theme, "tech")
    cat_dir = os.path.join(ICONFONT_DIR, category)
    existing = 0
    if os.path.isdir(cat_dir):
        existing = len([f for f in os.listdir(cat_dir) if f.endswith('.svg')])

    if existing >= count:
        return []  # 已有足够图标

    # 调用 download_icons.py 下载
    query = keywords[0]  # 用第一个关键词搜索
    try:
        result = subprocess.run(
            ["python3", download_script, "-q", query, "-c", category, "-n", str(count)],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            # 重新扫描目录
            if os.path.isdir(cat_dir):
                return [os.path.join(cat_dir, f) for f in sorted(os.listdir(cat_dir)) if f.endswith('.svg')][:count]
    except (subprocess.TimeoutExpired, Exception):
        pass  # 静默失败，不影响主流程

    return []


def ensure_iconfont_assets(title, theme, min_count=3):
    """确保有足够的 iconfont 图标，不够则自动下载"""
    # 先检查本地
    local_svgs = get_iconfont_svgs(theme, count=min_count)
    if len(local_svgs) >= min_count:
        return local_svgs

    # 不够，尝试自动补充
    auto_fetch_icons(title, theme, count=min_count)

    # 重新获取
    return get_iconfont_svgs(theme, count=min_count)

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
    # 先匹配5种新加的「真实派」风格（最具体）
    for theme in ["screenshot","portrait","product","contrast","zoom"]:
        kws = THEME_KEYWORDS.get(theme, [])
        if any(kw.lower() in text for kw in kws):
            return theme
    # 再匹配新20种风格（v6）
    for theme in ["ink","stamp","newspaper","polaroid","risograph","film","graffiti","ribbon","gradientmesh","brutalist","pastel","popart","terrarium","holographic","kraft","blueprint","starfield","washi","typewriter","carnival"]:
        kws = THEME_KEYWORDS.get(theme, [])
        if any(kw.lower() in text for kw in kws):
            return theme
    # 再匹配v5的11种风格
    for theme in ["vaporwave","acid","memphis","clay","glass","sticker","comic","neon","retro","collage","aurora"]:
        kws = THEME_KEYWORDS.get(theme, [])
        if any(kw.lower() in text for kw in kws):
            return theme
    # 再匹配v9新增的40种风格
    for theme in ["glitch","synthwave","matrix","quantum","ocean","ice","glassmorph","retrofuturism","galaxy","candy","steampunk","noir","gothic","baroque","tribal","artdeco","fire","streetwear","psychadelic","mosaic","newspaper2","techwear","cyberpunk2","neoncity","medieval","watercolor","zen","scandinavian","boho","rain","sunset","forest","desert","vintage","cherry","woodcut","plaid","origami","paperplane","lofi","wave","fairy","military","cloud","earth"]:
        kws = THEME_KEYWORDS.get(theme, [])
        if any(kw.lower() in text for kw in kws):
            return theme
    # 再匹配原有19种风格
    for theme in ["bold","cyber","anime","funny","luxury","fresh","gaming","food","cinema","cute","paper","variety","doodle","magazine","minimal","dopamine","guochao","pixel","journal"]:
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
        elif theme == "magazine":
            # 杂志风：衬线字体 + 上边框线 + 字间距
            dt = dt.replace(w, f'<span class="hl-magazine" style="color:{c};border-top:3px solid {c};letter-spacing:2px;padding-top:2px;font-family:Noto Serif SC,serif;font-style:italic;">{w}</span>')
        elif theme == "minimal":
            # 极简：加粗 + 颜色对比
            dt = dt.replace(w, f'<span class="hl-minimal" style="color:{c};font-weight:700;">{w}</span>')
        elif theme == "dopamine":
            # 多巴胺：渐变背景 + 白色文字 + 旋转
            rot = -3 if i%2==0 else 3
            dt = dt.replace(w, f'<span class="hl-dopamine" style="background:linear-gradient(135deg,{a1},{a2});color:#fff;padding:2px 12px;border-radius:20px;transform:rotate({rot}deg);display:inline-block;">{w}</span>')
        elif theme == "guochao":
            # 国潮：金色描边 + 印章风
            dt = dt.replace(w, f'<span class="hl-guochao" style="color:{c};-webkit-text-stroke:1px {a2};text-stroke:1px {a2};letter-spacing:4px;border:1px solid {c};padding:2px 8px;">{w}</span>')
        elif theme == "pixel":
            # 像素风：方块背景 + 等宽字体
            dt = dt.replace(w, f'<span class="hl-pixel" style="background:{c};color:var(--bg);padding:0 6px;font-family:monospace;font-weight:900;">{w}</span>')
        elif theme == "journal":
            # 手账风：手写体 + 胶带下划线
            dt = dt.replace(w, f'<span class="hl-journal" style="color:{c};border-bottom:3px solid {c};font-family:ZCOOL KuaiLe,sans-serif;position:relative;display:inline-block;">{w}<span style="position:absolute;bottom:-3px;left:-2px;right:-2px;height:6px;background:{c};opacity:0.2;border-radius:2px;"></span></span>')
        elif theme == "vaporwave":
            # 蒸汽波：渐变文字 + 发光
            dt = dt.replace(w, f'<span class="hl-vaporwave" style="background:linear-gradient(90deg,{a1},{a2});-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 0 8px {a1});">{w}</span>')
        elif theme == "acid":
            # 酸性设计：荧光色 + 扭曲 + 描边
            dt = dt.replace(w, f'<span class="hl-acid" style="color:{c};-webkit-text-stroke:2px {a2};text-stroke:2px {a2};filter:drop-shadow(2px 2px 0 {a2}) drop-shadow(0 0 6px {c});transform:skewX(-3deg);display:inline-block;">{w}</span>')
        elif theme == "memphis":
            # 孟菲斯：色块背景 + 几何感
            dt = dt.replace(w, f'<span class="hl-memphis" style="background:{c};color:#fff;padding:2px 10px;border-radius:0;transform:rotate(-2deg);display:inline-block;box-shadow:3px 3px 0 {a2};">{w}</span>')
        elif theme == "clay":
            # 黏土风：柔和阴影 + 圆角
            dt = dt.replace(w, f'<span class="hl-clay" style="background:{c};color:#fff;padding:3px 12px;border-radius:20px;box-shadow:2px 4px 8px rgba(0,0,0,0.15),inset 1px 1px 2px rgba(255,255,255,0.3);display:inline-block;">{w}</span>')
        elif theme == "glass":
            # 玻璃拟态：半透明背景 + 模糊
            dt = dt.replace(w, f'<span class="hl-glass" style="background:rgba({hex_to_rgb(c)},0.15);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);color:{c};padding:2px 10px;border-radius:8px;border:1px solid rgba({hex_to_rgb(c)},0.3);">{w}</span>')
        elif theme == "sticker":
            # 贴纸风：白边 + 阴影 + 旋转
            rot = -3 if i%2==0 else 3
            dt = dt.replace(w, f'<span class="hl-sticker" style="background:{c};color:#fff;padding:2px 10px;border-radius:6px;border:2px solid #fff;box-shadow:2px 2px 0 rgba(0,0,0,0.2);transform:rotate({rot}deg);display:inline-block;">{w}</span>')
        elif theme == "comic":
            # 漫画风：粗黑描边 + 倾斜
            dt = dt.replace(w, f'<span class="hl-comic" style="color:{c};-webkit-text-stroke:3px #000;text-stroke:3px #000;font-weight:900;transform:rotate(-2deg);display:inline-block;filter:drop-shadow(2px 2px 0 #000);">{w}</span>')
        elif theme == "neon":
            # 霓虹灯：多层发光
            dt = dt.replace(w, f'<span class="hl-neon" style="color:{c};text-shadow:0 0 5px {c},0 0 10px {c},0 0 20px {c},0 0 40px {c};font-weight:900;">{w}</span>')
        elif theme == "retro":
            # 复古：做旧色调 + 下划线
            dt = dt.replace(w, f'<span class="hl-retro" style="color:{c};border-bottom:3px double {c};letter-spacing:2px;opacity:0.9;">{w}</span>')
        elif theme == "collage":
            # 拼贴：剪报感 + 胶带
            rot = 2 if i%2==0 else -2
            dt = dt.replace(w, f'<span class="hl-collage" style="background:rgba({hex_to_rgb(c)},0.12);color:{c};padding:2px 8px;border:1px dashed {c};transform:rotate({rot}deg);display:inline-block;position:relative;">{w}<span style="position:absolute;top:-4px;left:30%;width:20px;height:6px;background:{a2};opacity:0.5;"></span></span>')
        elif theme == "aurora":
            # 极光弥散光：渐变 + 光晕
            dt = dt.replace(w, f'<span class="hl-aurora" style="background:linear-gradient(90deg,{a1},{a2});-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 6px {a1}) drop-shadow(0 0 12px {a2});">{w}</span>')
        elif theme == "ink":
            # 水墨：毛笔体 + 墨晕效果
            dt = dt.replace(w, f'<span class="hl-ink" style="color:{c};font-family:\'Ma Shan Zheng\',\'Noto Serif SC\',serif;text-shadow:2px 2px 8px rgba(0,0,0,0.15);border-bottom:2px solid {c};">{w}</span>')
        elif theme == "stamp":
            # 印章：红色方框 + 篆刻风
            dt = dt.replace(w, f'<span class="hl-stamp" style="color:{c};border:3px solid {c};padding:4px 8px;font-family:\'Noto Serif SC\',serif;letter-spacing:2px;display:inline-block;transform:rotate(-2deg);">{w}</span>')
        elif theme == "newspaper":
            # 报纸：粗体 + 下划线 + 衬线
            dt = dt.replace(w, f'<span class="hl-newspaper" style="color:{c};font-weight:900;border-bottom:3px solid {c};font-family:\'Noto Serif SC\',serif;">{w}</span>')
        elif theme == "polaroid":
            # 拍立得：白边相框 + 手写体
            dt = dt.replace(w, f'<span class="hl-polaroid" style="background:#fff;color:{c};padding:4px 10px;border:4px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.15);font-family:\'ZCOOL KuaiLe\',sans-serif;display:inline-block;">{w}</span>')
        elif theme == "risograph":
            # Riso：双色错位 + 颗粒感
            dt = dt.replace(w, f'<span class="hl-risograph" style="color:{c};text-shadow:2px 2px 0 {a2};font-weight:800;opacity:0.95;">{w}</span>')
        elif theme == "film":
            # 胶片：底部帧线 + 做旧
            dt = dt.replace(w, f'<span class="hl-film" style="color:{c};border-bottom:3px double {c};letter-spacing:3px;font-family:\'Noto Serif SC\',serif;">{w}</span>')
        elif theme == "graffiti":
            # 涂鸦：喷漆效果 + 倾斜
            rot = -5 if i%2==0 else 5
            dt = dt.replace(w, f'<span class="hl-graffiti" style="color:{c};font-weight:900;transform:rotate({rot}deg) scale(1.1);display:inline-block;text-shadow:3px 3px 0 rgba(0,0,0,0.5);-webkit-text-stroke:1px {a2};text-stroke:1px {a2};">{w}</span>')
        elif theme == "ribbon":
            # 缎带：优雅曲线 + 金色描边
            dt = dt.replace(w, f'<span class="hl-ribbon" style="color:{c};font-family:\'Noto Serif SC\',serif;border-bottom:2px solid {a2};letter-spacing:3px;padding:2px 6px;">{w}</span>')
        elif theme == "gradientmesh":
            # 网格渐变：渐变文字 + 柔和光晕
            dt = dt.replace(w, f'<span class="hl-gradientmesh" style="background:linear-gradient(135deg,{a1},{a2});-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 4px rgba(255,255,255,0.3));">{w}</span>')
        elif theme == "brutalist":
            # 粗野：粗黑边框 + 块面
            dt = dt.replace(w, f'<span class="hl-brutalist" style="background:{c};color:var(--bg);padding:2px 8px;border:3px solid #000;font-weight:900;display:inline-block;">{w}</span>')
        elif theme == "pastel":
            # 莫兰迪：柔和下划线 + 低调
            dt = dt.replace(w, f'<span class="hl-pastel" style="color:{c};border-bottom:2px solid {c};opacity:0.85;font-weight:600;">{w}</span>')
        elif theme == "popart":
            # 波普：网点背景 + 撞色
            dt = dt.replace(w, f'<span class="hl-popart" style="color:{c};-webkit-text-stroke:2px #000;text-stroke:2px #000;font-weight:900;transform:scale(1.1);display:inline-block;">{w}</span>')
        elif theme == "terrarium":
            # 生态：叶子装饰 + 绿色
            dt = dt.replace(w, f'<span class="hl-terrarium" style="color:{c};border:2px solid {c};border-radius:20px;padding:2px 12px;background:rgba({hex_to_rgb(c)},0.1);">{w}</span>')
        elif theme == "holographic":
            # 全息：彩虹渐变 + 光晕
            dt = dt.replace(w, f'<span class="hl-holographic" style="background:linear-gradient(90deg,#ff006e,#fb5607,#ffbe0b,#8338ec,#3a86ff);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 4px rgba(255,255,255,0.4));">{w}</span>')
        elif theme == "kraft":
            # 牛皮纸：手写体 + 做旧下划线
            dt = dt.replace(w, f'<span class="hl-kraft" style="color:{c};border-bottom:2px dashed {c};font-family:\'ZCOOL KuaiLe\',sans-serif;">{w}</span>')
        elif theme == "blueprint":
            # 蓝图：等宽字体 + 白色描线
            dt = dt.replace(w, f'<span class="hl-blueprint" style="color:{c};font-family:monospace;border:1px solid {c};padding:1px 6px;letter-spacing:2px;">{w}</span>')
        elif theme == "starfield":
            # 星空：发光 + 星点
            dt = dt.replace(w, f'<span class="hl-starfield" style="color:{c};text-shadow:0 0 8px {c},0 0 16px {c},0 0 24px {a2};font-weight:800;">{w}</span>')
        elif theme == "washi":
            # 和纸胶带：胶带装饰 + 倾斜
            rot = -2 if i%2==0 else 2
            dt = dt.replace(w, f'<span class="hl-washi" style="color:{c};background:rgba({hex_to_rgb(c)},0.1);padding:2px 8px;transform:rotate({rot}deg);display:inline-block;border-left:3px solid {c};">{w}</span>')
        elif theme == "typewriter":
            # 打字机：等宽字体 + 下划线
            dt = dt.replace(w, f'<span class="hl-typewriter" style="color:{c};font-family:\'Courier New\',monospace;border-bottom:2px solid {c};letter-spacing:1px;">{w}</span>')
        elif theme == "carnival":
            # 嘉年华：彩旗感 + 旋转
            rot = -3 if i%2==0 else 3
            dt = dt.replace(w, f'<span class="hl-carnival" style="color:{c};font-weight:900;transform:rotate({rot}deg) scale(1.15);display:inline-block;text-shadow:2px 2px 0 {a2};">{w}</span>')
        elif theme == "screenshot":
            # 真实截图：荧光笔黄底 + 黑色文字 + 醒目描边
            dt = dt.replace(w, f'<span class="hl-screenshot" style="background:{c};color:#000;padding:2px 8px;box-decoration-break:clone;-webkit-box-decoration-break:clone;font-weight:900;box-shadow:inset 0 -2px 0 {a2};">{w}</span>')
        elif theme == "portrait":
            # 真人出镜：人名标签感 + 加粗白字
            dt = dt.replace(w, f'<span class="hl-portrait" style="color:{c};font-weight:900;text-shadow:2px 2px 0 rgba(0,0,0,0.4),-1px -1px 0 rgba(0,0,0,0.4);">{w}</span>')
        elif theme == "product":
            # 实物开箱：徽章感 + 金属描边
            dt = dt.replace(w, f'<span class="hl-product" style="background:linear-gradient(135deg,{c},{a2});color:#fff;padding:2px 12px;border-radius:4px;font-weight:800;display:inline-block;box-shadow:0 2px 8px rgba(0,0,0,0.2);">{w}</span>')
        elif theme == "contrast":
            # 对比：左红右蓝或上下反差
            dt = dt.replace(w, f'<span class="hl-contrast" style="background:{c};color:#fff;padding:2px 10px;font-weight:900;display:inline-block;clip-path:polygon(0 0,100% 0,90% 100%,0 100%);">{w}</span>')
        elif theme == "zoom":
            # 局部放大：红色圆圈 + 放大字体
            sz = 1.3 if i%2==0 else 1.15
            dt = dt.replace(w, f'<span class="hl-zoom" style="color:{c};font-weight:900;font-size:{sz}em;text-shadow:3px 3px 0 {a2},-1px -1px 0 {a2},1px -1px 0 {a2},-1px 1px 0 {a2};display:inline-block;">{w}</span>')
        elif theme == "glitch":
            dt = dt.replace(w, f'<span class="hl-glitch" style="color:{c};">{w}</span>')
        elif theme == "synthwave":
            dt = dt.replace(w, f'<span class="hl-synthwave" style="color:{c};">{w}</span>')
        elif theme == "matrix":
            dt = dt.replace(w, f'<span class="hl-matrix" style="color:{c};">{w}</span>')
        elif theme == "quantum":
            dt = dt.replace(w, f'<span class="hl-quantum" style="color:{c};">{w}</span>')
        elif theme == "ocean":
            dt = dt.replace(w, f'<span class="hl-ocean" style="color:{c};">{w}</span>')
        elif theme == "ice":
            dt = dt.replace(w, f'<span class="hl-ice" style="color:{c};">{w}</span>')
        elif theme == "glassmorph":
            dt = dt.replace(w, f'<span class="hl-glassmorph" style="color:{c};">{w}</span>')
        elif theme == "retrofuturism":
            dt = dt.replace(w, f'<span class="hl-retrofuturism" style="color:{c};">{w}</span>')
        elif theme == "galaxy":
            dt = dt.replace(w, f'<span class="hl-galaxy" style="color:{c};">{w}</span>')
        elif theme == "candy":
            dt = dt.replace(w, f'<span class="hl-candy" style="color:{c};">{w}</span>')
        elif theme == "steampunk":
            dt = dt.replace(w, f'<span class="hl-steampunk" style="color:{c};">{w}</span>')
        elif theme == "noir":
            dt = dt.replace(w, f'<span class="hl-noir" style="color:{c};">{w}</span>')
        elif theme == "gothic":
            dt = dt.replace(w, f'<span class="hl-gothic" style="color:{c};">{w}</span>')
        elif theme == "baroque":
            dt = dt.replace(w, f'<span class="hl-baroque" style="color:{c};">{w}</span>')
        elif theme == "tribal":
            dt = dt.replace(w, f'<span class="hl-tribal" style="color:{c};">{w}</span>')
        elif theme == "artdeco":
            dt = dt.replace(w, f'<span class="hl-artdeco" style="color:{c};">{w}</span>')
        elif theme == "fire":
            dt = dt.replace(w, f'<span class="hl-fire" style="color:{c};">{w}</span>')
        elif theme == "streetwear":
            dt = dt.replace(w, f'<span class="hl-streetwear" style="color:{c};">{w}</span>')
        elif theme == "psychadelic":
            dt = dt.replace(w, f'<span class="hl-psychadelic" style="color:{c};">{w}</span>')
        elif theme == "mosaic":
            dt = dt.replace(w, f'<span class="hl-mosaic" style="color:{c};">{w}</span>')
        elif theme == "newspaper2":
            dt = dt.replace(w, f'<span class="hl-newspaper2" style="color:{c};">{w}</span>')
        elif theme == "techwear":
            dt = dt.replace(w, f'<span class="hl-techwear" style="color:{c};">{w}</span>')
        elif theme == "cyberpunk2":
            dt = dt.replace(w, f'<span class="hl-cyberpunk2" style="color:{c};">{w}</span>')
        elif theme == "neoncity":
            dt = dt.replace(w, f'<span class="hl-neoncity" style="color:{c};">{w}</span>')
        elif theme == "medieval":
            dt = dt.replace(w, f'<span class="hl-medieval" style="color:{c};">{w}</span>')
        elif theme == "watercolor":
            dt = dt.replace(w, f'<span class="hl-watercolor" style="color:{c};">{w}</span>')
        elif theme == "zen":
            dt = dt.replace(w, f'<span class="hl-zen" style="color:{c};">{w}</span>')
        elif theme == "scandinavian":
            dt = dt.replace(w, f'<span class="hl-scandinavian" style="color:{c};">{w}</span>')
        elif theme == "boho":
            dt = dt.replace(w, f'<span class="hl-boho" style="color:{c};">{w}</span>')
        elif theme == "rain":
            dt = dt.replace(w, f'<span class="hl-rain" style="color:{c};">{w}</span>')
        elif theme == "sunset":
            dt = dt.replace(w, f'<span class="hl-sunset" style="color:{c};">{w}</span>')
        elif theme == "forest":
            dt = dt.replace(w, f'<span class="hl-forest" style="color:{c};">{w}</span>')
        elif theme == "desert":
            dt = dt.replace(w, f'<span class="hl-desert" style="color:{c};">{w}</span>')
        elif theme == "vintage":
            dt = dt.replace(w, f'<span class="hl-vintage" style="color:{c};">{w}</span>')
        elif theme == "cherry":
            dt = dt.replace(w, f'<span class="hl-cherry" style="color:{c};">{w}</span>')
        elif theme == "woodcut":
            dt = dt.replace(w, f'<span class="hl-woodcut" style="color:{c};">{w}</span>')
        elif theme == "plaid":
            dt = dt.replace(w, f'<span class="hl-plaid" style="color:{c};">{w}</span>')
        elif theme == "origami":
            dt = dt.replace(w, f'<span class="hl-origami" style="color:{c};">{w}</span>')
        elif theme == "paperplane":
            dt = dt.replace(w, f'<span class="hl-paperplane" style="color:{c};">{w}</span>')
        elif theme == "lofi":
            dt = dt.replace(w, f'<span class="hl-lofi" style="color:{c};">{w}</span>')
        elif theme == "wave":
            dt = dt.replace(w, f'<span class="hl-wave" style="color:{c};">{w}</span>')
        elif theme == "fairy":
            dt = dt.replace(w, f'<span class="hl-fairy" style="color:{c};">{w}</span>')
        elif theme == "military":
            dt = dt.replace(w, f'<span class="hl-military" style="color:{c};">{w}</span>')
        elif theme == "cloud":
            dt = dt.replace(w, f'<span class="hl-cloud" style="color:{c};">{w}</span>')
        elif theme == "earth":
            dt = dt.replace(w, f'<span class="hl-earth" style="color:{c};">{w}</span>')
        else:
            dt = dt.replace(w, f'<span class="highlight" style="color:{c};">{w}</span>')
    return dt


def generate_single_cover(cfg, pf_key="bilibili", index=0, photo_url=None):
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
    auto_icons = cfg.get("auto_icons", False)
    if auto_icons:
        ensure_iconfont_assets(title, theme, min_count=2)
    deco_assets = get_decoration_assets(theme, index)
    (da1_url, da1_name), (da2_url, da2_name) = deco_assets[0], deco_assets[1] if len(deco_assets) > 1 else (deco_assets[0][0], deco_assets[0][0])

    # ===== 真人出镜照片处理 =====
    user_photo = cfg.get("photo_url") or photo_url
    has_photo = bool(user_photo)
    photo_position = cfg.get("photo_position", "right")  # right/left/center
    photo_class = f"cv-photo-{photo_position}" if photo_position in ("right","left","center") else "cv-photo-right"
    has_photo_class = "cv-has-photo" if has_photo else ""
    photo_html = ""
    if has_photo:
        photo_html = f'''    <img class="cv-user-photo {photo_class}" src="{user_photo}" alt="用户照片" onerror="this.style.display='none'" />
'''

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

    return f'''<div class="cover-card cover-{pf_key} theme-{theme} {has_photo_class}" data-platform="{pf['name']}" data-index="{index+1}" style="--bg-color:{bg};--accent1:{a1};--accent2:{a2};--text-color:{text_color};">
  <div class="cv-bg-decoration">
    <div class="cv-bg-circle" style="width:{350+index*20}px;height:{350+index*20}px;background:{a1};top:-{80+index*10}px;left:-{80+index*10}px;"></div>
    <div class="cv-bg-circle" style="width:{260+index*15}px;height:{260+index*15}px;background:{a2};bottom:-60px;right:-60px;"></div>
    <!-- 大卡通角色：半透明背景装饰 -->
    <img class="cv-mascot-bg" src="{mascot_url}" alt="" style="position:absolute;right:{mascot_right}px;bottom:{mascot_bottom}px;width:{mw}px;height:{mh}px;opacity:{mascot_opacity};z-index:0;filter:blur(1px);" onerror="this.style.display='none'">
    <!-- 小装饰图标：左上角 -->
    <img class="cv-emoji-deco cv-emoji-1 cv-iconfont-deco" src="{da1_url}" alt="" style="top:{12+index*3}%;left:4%;width:{es1}px;height:{es1}px;filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.15));" onerror="this.style.display='none'">
    <img class="cv-emoji-deco cv-emoji-2 cv-iconfont-deco" src="{da2_url}" alt="" style="bottom:{10+index*3}%;right:5%;width:{es2}px;height:{es2}px;filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.15));" onerror="this.style.display='none'">
{photo_html}  </div>
  <!-- 大卡通角色：实体（右侧） -->
  <img class="cv-mascot" src="{mascot_url}" alt="" onerror="this.style.display='none'">
  <div class="cv-content">
    <div class="cv-badge" style="background:rgba({hex_to_rgb(a1)},0.2);color:{a1};border:1px solid rgba({hex_to_rgb(a1)},0.4);">{badge_emoji} {badge}</div>
    <div class="cv-main-title" style="font-size:{ts}px;color:{text_color};">{dt}</div>
    <div class="cv-sub-title" style="font-size:{ss}px;color:{text_color};">{subtitle}</div>
    <div class="cv-tag-row">
{th}    </div>
  </div>
  <div class="cv-bottom-bar"><span>{bar_emoji} {quote}</span></div>
</div>'''


# ========== 差异化字体排版CSS ==========
THEME_FONT_CSS = """
/* ===== iconfont 卡通装饰图标增强 ===== */
.cv-iconfont-deco { opacity: 0.85; transition: transform 0.3s ease; z-index: 1; }

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
.cover-card:hover .cv-mascot { /* no animation */ }
/* 竖版封面：卡通角色放底部居中 */
.cover-wechat .cv-mascot,
.cover-mobile .cv-mascot {
  right: auto;
  left: 50%;
  transform: translateX(-50%);
  bottom: 8%;
  width: 28%;
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

/* ===== 14. magazine: 杂志风 ===== */
.theme-magazine .cv-main-title { font-weight: 900; letter-spacing: -1px; line-height: 1.0; font-family: 'Noto Serif SC', 'Playfair Display', serif; text-shadow: none; }
.theme-magazine .cv-main-title .hl-magazine { display: inline-block; }
.theme-magazine .cv-badge { border-radius: 0; border: none; border-top: 3px solid currentColor; border-bottom: 1px solid currentColor; background: transparent; letter-spacing: 4px; font-size: 12px; text-transform: uppercase; }
.theme-magazine .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; letter-spacing: 2px; }
.theme-magazine .cv-content::before {
  content: ''; position: absolute; top: 0; left: 0; bottom: 0; width: 4px;
  background: var(--accent2); z-index: 3;
}
.theme-magazine .cv-sub-title { font-family: 'Noto Serif SC', serif; font-style: italic; }
.theme-magazine .cv-bottom-bar { letter-spacing: 3px; font-size: 11px; text-transform: uppercase; }

/* ===== 15. minimal: 极简风 ===== */
.theme-minimal .cv-main-title { font-weight: 300; letter-spacing: 4px; line-height: 1.25; text-shadow: none; font-family: 'Noto Sans SC', sans-serif; }
.theme-minimal .cv-main-title .hl-minimal { display: inline; font-weight: 700; }
.theme-minimal .cv-badge { border-radius: 0; border: 1px solid currentColor; background: transparent; letter-spacing: 3px; font-size: 11px; }
.theme-minimal .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; font-size: 12px; }
.theme-minimal .cv-content { align-items: center; text-align: center; }
.theme-minimal .cv-bg-circle { display: none; }
.theme-minimal .cv-emoji-deco { display: none; }
.theme-minimal .cv-mascot { opacity: 0.5; }
.theme-minimal .cv-bottom-bar { letter-spacing: 2px; font-size: 11px; }

/* ===== 16. dopamine: 多巴胺撞色风 ===== */
.theme-dopamine .cv-main-title { font-weight: 900; letter-spacing: 1px; line-height: 1.1; text-shadow: 2px 2px 0 rgba(0,0,0,0.15); }
.theme-dopamine .cv-main-title .hl-dopamine { display: inline-block; }
.theme-dopamine .cv-badge { border-radius: 50px; border: 2px solid rgba(255,255,255,0.8); }
.theme-dopamine .cv-tag { border-radius: 50px; border: 2px solid rgba(255,255,255,0.6); }
.theme-dopamine .cv-bg-circle { filter: blur(30px); opacity: 0.3; }
.theme-dopamine .cv-emoji-deco { opacity: 0.25 !important; }
.theme-dopamine .cv-mascot { filter: drop-shadow(4px 4px 0 rgba(0,0,0,0.2)) drop-shadow(0 0 10px rgba(255,255,255,0.3)); }

/* ===== 17. guochao: 国潮风 ===== */
.theme-guochao .cv-main-title { font-weight: 900; letter-spacing: 6px; line-height: 1.15; font-family: 'Noto Serif SC', 'ZCOOL XiaoWei', serif; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
.theme-guochao .cv-main-title .hl-guochao { display: inline-block; }
.theme-guochao .cv-badge { border-radius: 0; border: 2px solid currentColor; background: transparent; letter-spacing: 4px; }
.theme-guochao .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; letter-spacing: 2px; }
.theme-guochao .cv-content::before {
  content: ''; position: absolute; top: 15px; right: 15px; width: 60px; height: 60px;
  border: 2px solid currentColor; border-radius: 50%; opacity: 0.15; z-index: 1;
}
.theme-guochao .cv-content::after {
  content: ''; position: absolute; bottom: 50px; left: 30px; width: 40px; height: 40px;
  border: 1px solid currentColor; transform: rotate(45deg); opacity: 0.1; z-index: 1;
}
.theme-guochao .cv-bottom-bar { letter-spacing: 4px; }

/* ===== 18. pixel: 像素风 ===== */
.theme-pixel .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.1; font-family: 'Press Start 2P', 'Noto Sans SC', monospace; text-shadow: 3px 3px 0 var(--accent2); image-rendering: pixelated; }
.theme-pixel .cv-main-title .hl-pixel { display: inline-block; }
.theme-pixel .cv-badge { border-radius: 0; border: none; background: var(--accent1); color: var(--bg); padding: 4px 8px; font-family: monospace; font-size: 11px; }
.theme-pixel .cv-tag { border-radius: 0; border: none; background: var(--accent2); color: var(--bg); font-family: monospace; }
.theme-pixel .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 4px, rgba(255,255,255,0.03) 4px, rgba(255,255,255,0.03) 8px);
  pointer-events: none;
}
.theme-pixel .cv-content::before {
  content: '▶'; position: absolute; top: 20px; left: 30px; font-size: 16px; color: var(--accent1); font-family: monospace;
}
.theme-pixel .cv-mascot { image-rendering: pixelated; filter: drop-shadow(2px 2px 0 #000); }

/* ===== 19. journal: 手账风 ===== */
.theme-journal .cv-main-title { font-weight: 700; letter-spacing: 1px; line-height: 1.2; font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; text-shadow: none; }
.theme-journal .cv-main-title .hl-journal { display: inline; border-bottom: 2px solid var(--accent2); }
.theme-journal .cv-badge { border-radius: 0; border: 1px solid currentColor; background: transparent; font-family: 'ZCOOL KuaiLe', sans-serif; }
.theme-journal .cv-tag { border-radius: 0; border: 1px dashed currentColor; background: transparent; }
.theme-journal .cv-bg-decoration::after {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 24px, rgba(0,0,0,0.04) 24px, rgba(0,0,0,0.04) 25px);
  pointer-events: none;
}
.theme-journal .cv-content::before {
  content: '📌'; position: absolute; top: 15px; right: 25px; font-size: 20px; opacity: 0.5; z-index: 1;
}
.theme-journal .cv-mascot { filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.15)); opacity: 0.8; transform: rotate(-3deg); }

/* ===== 20. vaporwave: 蒸汽波风 ===== */
.theme-vaporwave .cv-main-title { font-weight: 900; letter-spacing: 4px; line-height: 1.1; font-family: 'Noto Sans SC', sans-serif; text-shadow: 2px 2px 0 rgba(255,0,255,0.3), -2px -2px 0 rgba(0,255,255,0.3); }
.theme-vaporwave .cv-main-title .hl-vaporwave { display: inline-block; }
.theme-vaporwave .cv-badge { border-radius: 0; border: 1px solid rgba(255,255,255,0.3); background: rgba(0,0,0,0.2); letter-spacing: 3px; }
.theme-vaporwave .cv-tag { border-radius: 0; border: 1px solid rgba(255,255,255,0.2); }
.theme-vaporwave .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background:
    repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,0,255,0.03) 2px, rgba(255,0,255,0.03) 3px),
    linear-gradient(180deg, transparent 60%, rgba(255,110,199,0.15) 100%);
  pointer-events: none;
}
.theme-vaporwave .cv-bg-decoration::after {
  content: '▶'; position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
  font-size: 120px; color: rgba(255,255,255,0.04); z-index: 0; pointer-events: none;
}
.theme-vaporwave .cv-content::before {
  content: 'ＡＥＳＴＨＥＴＩＣ'; position: absolute; bottom: 50px; right: 30px;
  font-size: 10px; letter-spacing: 4px; color: var(--accent1); opacity: 0.4; z-index: 1;
}
.theme-vaporwave .cv-mascot { filter: drop-shadow(0 0 10px var(--accent1)) drop-shadow(0 0 20px var(--accent2)); opacity: 0.8; }

/* ===== 21. acid: 酸性设计 ===== */
.theme-acid .cv-main-title { font-weight: 900; letter-spacing: 1px; line-height: 1.1; text-shadow: none; font-family: 'Noto Sans SC', sans-serif; }
.theme-acid .cv-main-title .hl-acid { display: inline-block; }
.theme-acid .cv-badge { border-radius: 0; border: none; background: var(--accent1); color: #000; font-weight: 900; clip-path: polygon(0 0, 100% 0, 95% 100%, 5% 100%); }
.theme-acid .cv-tag { border-radius: 0; border: 1px solid var(--accent1); background: transparent; }
.theme-acid .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(circle at 20% 30%, var(--accent1) 0%, transparent 25%),
    radial-gradient(circle at 80% 70%, var(--accent2) 0%, transparent 25%);
  opacity: 0.08; pointer-events: none;
}
.theme-acid .cv-bg-decoration::after {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(45deg, transparent, transparent 80px, rgba(255,255,255,0.02) 80px, rgba(255,255,255,0.02) 82px);
  pointer-events: none;
}
.theme-acid .cv-mascot { filter: drop-shadow(0 0 8px var(--accent1)) contrast(1.2) saturate(1.3); opacity: 0.85; }

/* ===== 22. memphis: 孟菲斯风 ===== */
.theme-memphis .cv-main-title { font-weight: 900; letter-spacing: 1px; line-height: 1.15; text-shadow: none; }
.theme-memphis .cv-main-title .hl-memphis { display: inline-block; }
.theme-memphis .cv-badge { border-radius: 0; border: 2px solid var(--accent1); background: transparent; }
.theme-memphis .cv-tag { border-radius: 0; border: 2px solid currentColor; background: transparent; }
.theme-memphis .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(circle at 10% 15%, var(--accent1) 6px, transparent 7px),
    radial-gradient(circle at 85% 85%, var(--accent2) 8px, transparent 9px),
    repeating-linear-gradient(45deg, transparent, transparent 30px, rgba(0,0,0,0.03) 30px, rgba(0,0,0,0.03) 32px);
  background-size: 60px 60px, 80px 80px, auto; opacity: 0.3; pointer-events: none;
}
.theme-memphis .cv-bg-decoration::after {
  content: '◢◣'; position: absolute; bottom: 40px; left: 30px;
  font-size: 40px; color: var(--accent1); opacity: 0.15; z-index: 0;
}
.theme-memphis .cv-mascot { filter: drop-shadow(3px 3px 0 rgba(0,0,0,0.2)); opacity: 0.9; }

/* ===== 23. clay: 黏土风 ===== */
.theme-clay .cv-main-title { font-weight: 800; letter-spacing: 1px; line-height: 1.15; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
.theme-clay .cv-main-title .hl-clay { display: inline-block; }
.theme-clay .cv-badge { border-radius: 50px; border: none; background: rgba(255,255,255,0.6); box-shadow: 2px 4px 8px rgba(0,0,0,0.1), inset 1px 1px 2px rgba(255,255,255,0.5); }
.theme-clay .cv-tag { border-radius: 50px; border: none; background: rgba(255,255,255,0.5); box-shadow: 1px 2px 4px rgba(0,0,0,0.08); }
.theme-clay .cv-bg-circle { filter: blur(30px); opacity: 0.2; }
.theme-clay .cv-mascot { filter: drop-shadow(4px 6px 8px rgba(0,0,0,0.15)) brightness(1.05); opacity: 0.95; }

/* ===== 24. glass: 玻璃拟态 ===== */
.theme-glass .cv-main-title { font-weight: 700; letter-spacing: 2px; line-height: 1.2; text-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.theme-glass .cv-main-title .hl-glass { display: inline-block; }
.theme-glass .cv-badge {
  border-radius: 12px; border: 1px solid rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
}
.theme-glass .cv-tag {
  border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.1); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
}
.theme-glass .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(circle at 20% 20%, var(--accent1) 0%, transparent 40%),
    radial-gradient(circle at 80% 80%, var(--accent2) 0%, transparent 40%);
  opacity: 0.15; filter: blur(40px); pointer-events: none;
}
.theme-glass .cv-mascot { filter: drop-shadow(0 0 10px rgba(255,255,255,0.3)); opacity: 0.8; }

/* ===== 25. sticker: 贴纸风 ===== */
.theme-sticker .cv-main-title { font-weight: 800; letter-spacing: 1px; line-height: 1.15; text-shadow: 1px 1px 0 #fff, 2px 2px 0 rgba(0,0,0,0.1); }
.theme-sticker .cv-main-title .hl-sticker { display: inline-block; }
.theme-sticker .cv-badge { border-radius: 8px; border: 2px solid #fff; box-shadow: 2px 2px 0 rgba(0,0,0,0.15); }
.theme-sticker .cv-tag { border-radius: 6px; border: 2px solid #fff; box-shadow: 1px 1px 0 rgba(0,0,0,0.1); }
.theme-sticker .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(circle at 15% 20%, var(--accent1) 3px, transparent 4px),
              radial-gradient(circle at 70% 60%, var(--accent2) 4px, transparent 5px),
              radial-gradient(circle at 40% 85%, var(--accent1) 2px, transparent 3px);
  background-size: 50px 50px, 70px 70px, 40px 40px; opacity: 0.12; pointer-events: none;
}
.theme-sticker .cv-mascot { filter: drop-shadow(3px 3px 0 #fff) drop-shadow(4px 4px 0 rgba(0,0,0,0.1)); opacity: 0.95; }

/* ===== 26. comic: 漫画风 ===== */
.theme-comic .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.1; text-shadow: 3px 3px 0 #000; font-family: 'Noto Sans SC', sans-serif; }
.theme-comic .cv-main-title .hl-comic { display: inline-block; }
.theme-comic .cv-badge { border-radius: 0; border: 3px solid #000; background: #fff; color: #000; font-weight: 900; }
.theme-comic .cv-tag { border-radius: 0; border: 2px solid #000; background: #fff; color: #000; font-weight: 700; }
.theme-comic .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-radial-gradient(circle at 50% 50%, transparent, transparent 3px, rgba(0,0,0,0.04) 3px, rgba(0,0,0,0.04) 5px);
  pointer-events: none;
}
.theme-comic .cv-bg-decoration::after {
  content: 'POW!'; position: absolute; top: 20px; right: 30px;
  font-size: 24px; font-weight: 900; color: var(--accent2);
  -webkit-text-stroke: 2px #000; text-stroke: 2px #000;
  transform: rotate(-15deg); opacity: 0.3; z-index: 0;
}
.theme-comic .cv-content::before {
  content: ''; position: absolute; top: 10px; left: 10px; right: 10px; bottom: 10px;
  border: 3px solid #000; border-radius: 8px; pointer-events: none; z-index: 1;
}
.theme-comic .cv-mascot { filter: drop-shadow(3px 3px 0 #000); opacity: 0.9; }

/* ===== 27. neon: 霓虹灯风 ===== */
.theme-neon .cv-main-title { font-weight: 900; letter-spacing: 2px; line-height: 1.1; font-family: 'Noto Sans SC', sans-serif; }
.theme-neon .cv-main-title .hl-neon { display: inline-block; }
.theme-neon .cv-badge { border-radius: 50px; border: 2px solid var(--accent1); background: transparent; box-shadow: 0 0 10px var(--accent1), inset 0 0 10px rgba(255,0,110,0.1); }
.theme-neon .cv-tag { border-radius: 50px; border: 1px solid var(--accent2); background: transparent; box-shadow: 0 0 8px var(--accent2); }
.theme-neon .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(circle at 50% 50%, transparent 0%, rgba(0,0,0,0.3) 100%);
  pointer-events: none;
}
.theme-neon .cv-content::before {
  content: 'ＮＥＯＮ'; position: absolute; top: 15px; right: 25px;
  font-size: 11px; letter-spacing: 4px; color: var(--accent1); opacity: 0.3;
  text-shadow: 0 0 5px var(--accent1); z-index: 1;
}
.theme-neon .cv-mascot { filter: drop-shadow(0 0 8px var(--accent1)) drop-shadow(0 0 16px var(--accent2)) brightness(1.2); opacity: 0.85; }

/* ===== 28. retro: 复古风 ===== */
.theme-retro .cv-main-title { font-weight: 800; letter-spacing: 2px; line-height: 1.15; font-family: 'Noto Serif SC', serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.15); }
.theme-retro .cv-main-title .hl-retro { display: inline-block; }
.theme-retro .cv-badge { border-radius: 0; border: 2px solid currentColor; background: transparent; letter-spacing: 3px; font-family: 'Noto Serif SC', serif; }
.theme-retro .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; }
.theme-retro .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.02) 3px, rgba(0,0,0,0.02) 4px);
  pointer-events: none;
}
.theme-retro .cv-bg-decoration::after {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(ellipse at center, transparent 0%, rgba(0,0,0,0.1) 100%);
  pointer-events: none;
}
.theme-retro .cv-mascot { filter: sepia(0.3) contrast(0.95) drop-shadow(2px 2px 4px rgba(0,0,0,0.2)); opacity: 0.82; }

/* ===== 29. collage: 拼贴风 ===== */
.theme-collage .cv-main-title { font-weight: 800; letter-spacing: 1px; line-height: 1.2; text-shadow: 1px 1px 0 rgba(0,0,0,0.1); }
.theme-collage .cv-main-title .hl-collage { display: inline-block; }
.theme-collage .cv-badge { border-radius: 0; border: 1px dashed currentColor; background: rgba(255,255,255,0.5); transform: rotate(-1deg); }
.theme-collage .cv-tag { border-radius: 0; border: 1px solid currentColor; background: rgba(255,255,255,0.3); transform: rotate(1deg); }
.theme-collage .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background:
    repeating-linear-gradient(0deg, transparent, transparent 24px, rgba(0,0,0,0.03) 24px, rgba(0,0,0,0.03) 25px);
  pointer-events: none;
}
.theme-collage .cv-bg-decoration::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 15px;
  background: var(--accent2); opacity: 0.15; z-index: 0;
}
.theme-collage .cv-content::before {
  content: '📰'; position: absolute; top: 12px; right: 20px; font-size: 18px; opacity: 0.3; z-index: 1;
}
.theme-collage .cv-mascot { filter: drop-shadow(2px 2px 3px rgba(0,0,0,0.2)); opacity: 0.85; transform: rotate(2deg); }

/* ===== 30. aurora: 弥散光/极光风 ===== */
.theme-aurora .cv-main-title { font-weight: 700; letter-spacing: 3px; line-height: 1.2; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
.theme-aurora .cv-main-title .hl-aurora { display: inline-block; }
.theme-aurora .cv-badge { border-radius: 50px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.1); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
.theme-aurora .cv-tag { border-radius: 50px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.08); backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px); }
.theme-aurora .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(ellipse at 20% 30%, var(--accent1) 0%, transparent 40%),
    radial-gradient(ellipse at 80% 60%, var(--accent2) 0%, transparent 40%),
    radial-gradient(ellipse at 50% 100%, var(--accent1) 0%, transparent 50%);
  opacity: 0.2; filter: blur(30px); pointer-events: none;
}
.theme-aurora .cv-bg-circle { filter: blur(40px); opacity: 0.15; }
.theme-aurora .cv-mascot { filter: drop-shadow(0 0 8px var(--accent1)) drop-shadow(0 0 16px var(--accent2)); opacity: 0.82; }

/* ===== 31. ink: 水墨风 ===== */
.theme-ink .cv-main-title { font-weight: 700; letter-spacing: 6px; line-height: 1.25; font-family: 'Ma Shan Zheng', 'Noto Serif SC', serif; text-shadow: 1px 1px 3px rgba(0,0,0,0.1); }
.theme-ink .cv-main-title .hl-ink { display: inline-block; }
.theme-ink .cv-badge { border-radius: 0; border: 1px solid currentColor; background: transparent; letter-spacing: 4px; font-family: 'Noto Serif SC', serif; }
.theme-ink .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; }
.theme-ink .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(ellipse at 30% 40%, rgba(0,0,0,0.03) 0%, transparent 60%),
              radial-gradient(ellipse at 70% 70%, rgba(0,0,0,0.02) 0%, transparent 50%);
  pointer-events: none;
}
.theme-ink .cv-content::before {
  content: '印'; position: absolute; bottom: 50px; right: 30px;
  font-size: 36px; font-family: 'Noto Serif SC', serif; color: var(--accent2);
  opacity: 0.12; z-index: 1; border: 2px solid var(--accent2); padding: 4px 8px;
}
.theme-ink .cv-mascot { filter: grayscale(0.3) opacity(0.7); opacity: 0.75; }

/* ===== 32. stamp: 印章风 ===== */
.theme-stamp .cv-main-title { font-weight: 900; letter-spacing: 4px; line-height: 1.15; font-family: 'Noto Serif SC', serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
.theme-stamp .cv-main-title .hl-stamp { display: inline-block; }
.theme-stamp .cv-badge { border-radius: 0; border: 3px solid currentColor; background: transparent; letter-spacing: 3px; font-family: 'Noto Serif SC', serif; }
.theme-stamp .cv-tag { border-radius: 0; border: 2px solid currentColor; background: transparent; }
.theme-stamp .cv-content::before {
  content: '鑑'; position: absolute; top: 20px; right: 25px;
  font-size: 32px; font-family: 'Noto Serif SC', serif; color: var(--accent1);
  border: 3px solid var(--accent1); padding: 4px 8px; opacity: 0.25; z-index: 1;
}
.theme-stamp .cv-content::after {
  content: ''; position: absolute; bottom: 50px; left: 30px; width: 50px; height: 50px;
  border: 2px solid var(--accent2); transform: rotate(45deg); opacity: 0.15; z-index: 1;
}
.theme-stamp .cv-mascot { filter: sepia(0.2) opacity(0.8); opacity: 0.8; }

/* ===== 33. newspaper: 报纸风 ===== */
.theme-newspaper .cv-main-title { font-weight: 900; letter-spacing: -0.5px; line-height: 1.05; font-family: 'Noto Serif SC', 'Playfair Display', serif; text-shadow: none; }
.theme-newspaper .cv-main-title .hl-newspaper { display: inline-block; }
.theme-newspaper .cv-badge { border-radius: 0; border: none; border-top: 3px double currentColor; border-bottom: 1px solid currentColor; background: transparent; letter-spacing: 3px; font-size: 11px; text-transform: uppercase; }
.theme-newspaper .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; font-size: 12px; }
.theme-newspaper .cv-content::before {
  content: 'BREAKING'; position: absolute; top: 15px; left: 30px;
  font-size: 10px; font-weight: 900; letter-spacing: 4px; color: var(--accent2);
  opacity: 0.5; z-index: 1;
}
.theme-newspaper .cv-bg-decoration::after {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.02) 3px, rgba(0,0,0,0.02) 4px);
  pointer-events: none;
}
.theme-newspaper .cv-mascot { filter: grayscale(0.5) contrast(0.9) opacity(0.7); opacity: 0.7; }

/* ===== 34. polaroid: 拍立得 ===== */
.theme-polaroid .cv-main-title { font-weight: 600; letter-spacing: 1px; line-height: 1.2; font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
.theme-polaroid .cv-main-title .hl-polaroid { display: inline-block; }
.theme-polaroid .cv-badge { border-radius: 8px; border: 4px solid #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
.theme-polaroid .cv-tag { border-radius: 6px; border: 3px solid #fff; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
.theme-polaroid .cv-content::before {
  content: ''; position: absolute; top: 10px; left: 10px; right: 10px; bottom: 60px;
  border: 4px solid #fff; box-shadow: 0 4px 16px rgba(0,0,0,0.12); z-index: 1; pointer-events: none;
}
.theme-polaroid .cv-bg-circle { filter: blur(20px); opacity: 0.08; }
.theme-polaroid .cv-mascot { filter: sepia(0.15) contrast(0.95) drop-shadow(2px 2px 4px rgba(0,0,0,0.1)); opacity: 0.88; }

/* ===== 35. risograph: Riso印刷风 ===== */
.theme-risograph .cv-main-title { font-weight: 800; letter-spacing: 1px; line-height: 1.15; text-shadow: 2px 2px 0 var(--accent2); }
.theme-risograph .cv-main-title .hl-risograph { display: inline-block; }
.theme-risograph .cv-badge { border-radius: 0; border: 2px solid currentColor; background: transparent; }
.theme-risograph .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; }
.theme-risograph .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.015) 2px, rgba(0,0,0,0.015) 3px);
  pointer-events: none;
}
.theme-risograph .cv-bg-decoration::after {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(circle at 30% 30%, var(--accent1) 0%, transparent 20%),
              radial-gradient(circle at 70% 70%, var(--accent2) 0%, transparent 20%);
  opacity: 0.06; filter: blur(10px); pointer-events: none;
}
.theme-risograph .cv-mascot { filter: contrast(1.15) saturate(0.8) drop-shadow(2px 2px 0 var(--accent2)); opacity: 0.85; }

/* ===== 36. film: 电影胶片风 ===== */
.theme-film .cv-main-title { font-weight: 700; letter-spacing: 3px; line-height: 1.15; font-family: 'Noto Serif SC', serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); }
.theme-film .cv-main-title .hl-film { display: inline-block; }
.theme-film .cv-badge { border-radius: 0; border: 1px solid currentColor; background: rgba(0,0,0,0.3); letter-spacing: 2px; }
.theme-film .cv-tag { border-radius: 0; border: 1px solid currentColor; background: rgba(0,0,0,0.2); }
.theme-film .cv-bg-decoration::before {
  content: ''; position: absolute; top: 0; bottom: 0; left: 0; width: 30px;
  background: repeating-linear-gradient(0deg, transparent, transparent 30px, rgba(255,255,255,0.06) 30px, rgba(255,255,255,0.06) 36px);
  z-index: 0; pointer-events: none;
}
.theme-film .cv-bg-decoration::after {
  content: ''; position: absolute; top: 0; bottom: 0; right: 0; width: 30px;
  background: repeating-linear-gradient(0deg, transparent, transparent 30px, rgba(255,255,255,0.06) 30px, rgba(255,255,255,0.06) 36px);
  z-index: 0; pointer-events: none;
}
.theme-film .cv-content::before {
  content: '● REC'; position: absolute; top: 15px; right: 40px;
  font-size: 11px; color: var(--accent1); opacity: 0.4; letter-spacing: 2px; z-index: 1;
}
.theme-film .cv-mascot { filter: sepia(0.2) contrast(0.95) drop-shadow(2px 2px 4px rgba(0,0,0,0.2)); opacity: 0.82; }

/* ===== 37. graffiti: 涂鸦街头风 ===== */
.theme-graffiti .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.1; text-shadow: 3px 3px 0 rgba(0,0,0,0.5); font-family: 'Noto Sans SC', sans-serif; }
.theme-graffiti .cv-main-title .hl-graffiti { display: inline-block; }
.theme-graffiti .cv-badge { border-radius: 0; border: none; background: var(--accent1); color: #000; font-weight: 900; clip-path: polygon(0 0, 100% 0, 95% 100%, 5% 100%); transform: rotate(-2deg); }
.theme-graffiti .cv-tag { border-radius: 0; border: 2px solid currentColor; background: rgba(0,0,0,0.3); transform: rotate(1deg); }
.theme-graffiti .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(circle at 20% 80%, var(--accent1) 0%, transparent 15%),
              radial-gradient(circle at 80% 20%, var(--accent2) 0%, transparent 15%);
  opacity: 0.1; pointer-events: none;
}
.theme-graffiti .cv-content::before {
  content: 'WILD'; position: absolute; bottom: 50px; left: 30px;
  font-size: 28px; font-weight: 900; color: var(--accent2);
  opacity: 0.2; transform: rotate(-15deg); letter-spacing: 4px; z-index: 0;
}
.theme-graffiti .cv-mascot { filter: drop-shadow(3px 3px 0 rgba(0,0,0,0.4)) saturate(1.3) contrast(1.1); opacity: 0.9; }

/* ===== 38. ribbon: 缎带横幅风 ===== */
.theme-ribbon .cv-main-title { font-weight: 700; letter-spacing: 4px; line-height: 1.2; font-family: 'Noto Serif SC', serif; text-shadow: 1px 1px 3px rgba(0,0,0,0.1); }
.theme-ribbon .cv-main-title .hl-ribbon { display: inline-block; }
.theme-ribbon .cv-badge { border-radius: 0; clip-path: polygon(0 0, 100% 0, 95% 100%, 5% 100%); border: none; background: var(--accent1); color: #fff; letter-spacing: 3px; }
.theme-ribbon .cv-tag { border-radius: 0; clip-path: polygon(5% 0, 100% 0, 95% 100%, 0 100%); border: none; background: rgba(255,255,255,0.15); }
.theme-ribbon .cv-content::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px;
  background: linear-gradient(90deg, transparent, var(--accent1), var(--accent2), var(--accent1), transparent);
  z-index: 3;
}
.theme-ribbon .cv-content::after {
  content: ''; position: absolute; bottom: 36px; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, transparent, var(--accent2), var(--accent1), var(--accent2), transparent);
  z-index: 3;
}
.theme-ribbon .cv-mascot { filter: drop-shadow(0 0 6px rgba(0,0,0,0.1)) brightness(1.05); opacity: 0.88; }

/* ===== 39. gradientmesh: 网格渐变风 ===== */
.theme-gradientmesh .cv-main-title { font-weight: 800; letter-spacing: 2px; line-height: 1.2; text-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.theme-gradientmesh .cv-main-title .hl-gradientmesh { display: inline-block; }
.theme-gradientmesh .cv-badge { border-radius: 50px; border: 1px solid rgba(255,255,255,0.4); background: rgba(255,255,255,0.2); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
.theme-gradientmesh .cv-tag { border-radius: 50px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.15); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
.theme-gradientmesh .cv-bg-circle { filter: blur(40px); opacity: 0.25; }
.theme-gradientmesh .cv-mascot { filter: drop-shadow(0 0 8px rgba(255,255,255,0.3)); opacity: 0.85; }

/* ===== 40. brutalist: 粗野主义风 ===== */
.theme-brutalist .cv-main-title { font-weight: 900; letter-spacing: -1px; line-height: 1.0; text-shadow: none; font-family: 'Noto Sans SC', sans-serif; }
.theme-brutalist .cv-main-title .hl-brutalist { display: inline-block; }
.theme-brutalist .cv-badge { border-radius: 0; border: 3px solid #000; background: transparent; font-weight: 900; letter-spacing: 2px; }
.theme-brutalist .cv-tag { border-radius: 0; border: 3px solid #000; background: transparent; font-weight: 700; }
.theme-brutalist .cv-content::before {
  content: ''; position: absolute; top: 8px; left: 8px; right: 8px; bottom: 44px;
  border: 4px solid #000; pointer-events: none; z-index: 1;
}
.theme-brutalist .cv-bg-circle { display: none; }
.theme-brutalist .cv-emoji-deco { display: none; }
.theme-brutalist .cv-mascot { opacity: 0.5; filter: grayscale(0.3); }

/* ===== 41. pastel: 莫兰迪柔色风 ===== */
.theme-pastel .cv-main-title { font-weight: 500; letter-spacing: 3px; line-height: 1.25; text-shadow: none; }
.theme-pastel .cv-main-title .hl-pastel { display: inline; }
.theme-pastel .cv-badge { border-radius: 20px; border: 1px solid currentColor; background: transparent; font-weight: 400; letter-spacing: 2px; }
.theme-pastel .cv-tag { border-radius: 16px; border: 1px solid currentColor; background: transparent; font-weight: 400; }
.theme-pastel .cv-bg-circle { filter: blur(30px); opacity: 0.12; }
.theme-pastel .cv-content { align-items: center; text-align: center; }
.theme-pastel .cv-mascot { opacity: 0.7; filter: brightness(0.95) saturate(0.7); }

/* ===== 42. popart: 波普艺术风 ===== */
.theme-popart .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.1; text-shadow: 3px 3px 0 #000; }
.theme-popart .cv-main-title .hl-popart { display: inline-block; }
.theme-popart .cv-badge { border-radius: 0; border: 3px solid #000; background: #fff; color: #000; font-weight: 900; }
.theme-popart .cv-tag { border-radius: 0; border: 2px solid #000; background: #fff; color: #000; font-weight: 700; }
.theme-popart .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-radial-gradient(circle at 30% 70%, transparent, transparent 4px, rgba(0,0,0,0.04) 4px, rgba(0,0,0,0.04) 6px);
  pointer-events: none;
}
.theme-popart .cv-bg-decoration::after {
  content: 'POW!'; position: absolute; top: 20px; right: 30px;
  font-size: 28px; font-weight: 900; color: var(--accent2);
  -webkit-text-stroke: 2px #000; text-stroke: 2px #000;
  transform: rotate(-12deg); opacity: 0.25; z-index: 0;
}
.theme-popart .cv-mascot { filter: drop-shadow(3px 3px 0 #000) saturate(1.3) contrast(1.1); opacity: 0.9; }

/* ===== 43. terrarium: 玻璃生态风 ===== */
.theme-terrarium .cv-main-title { font-weight: 600; letter-spacing: 2px; line-height: 1.2; text-shadow: 0 1px 4px rgba(0,0,0,0.1); }
.theme-terrarium .cv-main-title .hl-terrarium { display: inline-block; }
.theme-terrarium .cv-badge { border-radius: 50px; border: 1px solid rgba(255,255,255,0.4); background: rgba(255,255,255,0.2); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
.theme-terrarium .cv-tag { border-radius: 50px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.15); }
.theme-terrarium .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.1) 0%, transparent 30%),
              radial-gradient(circle at 80% 70%, rgba(255,255,255,0.08) 0%, transparent 25%);
  filter: blur(10px); pointer-events: none;
}
.theme-terrarium .cv-bg-circle { filter: blur(25px); opacity: 0.15; }
.theme-terrarium .cv-mascot { filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1)) brightness(1.05) saturate(1.1); opacity: 0.9; }

/* ===== 44. holographic: 全息彩虹风 ===== */
.theme-holographic .cv-main-title { font-weight: 800; letter-spacing: 2px; line-height: 1.15; text-shadow: 0 2px 10px rgba(255,255,255,0.2); }
.theme-holographic .cv-main-title .hl-holographic { display: inline-block; }
.theme-holographic .cv-badge { border-radius: 50px; border: 1px solid rgba(255,255,255,0.5); background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }
.theme-holographic .cv-tag { border-radius: 50px; border: 1px solid rgba(255,255,255,0.4); background: rgba(255,255,255,0.1); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
.theme-holographic .cv-bg-circle { filter: blur(30px); opacity: 0.2; }
.theme-holographic .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: linear-gradient(135deg, rgba(255,0,110,0.08), rgba(131,56,239,0.08), rgba(58,134,255,0.08), rgba(255,190,11,0.08));
  pointer-events: none;
}
.theme-holographic .cv-mascot { filter: drop-shadow(0 0 8px rgba(255,255,255,0.4)) saturate(1.4) hue-rotate(10deg); opacity: 0.88; }

/* ===== 45. kraft: 牛皮纸风 ===== */
.theme-kraft .cv-main-title { font-weight: 700; letter-spacing: 1px; line-height: 1.2; font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; text-shadow: 1px 1px 0 rgba(255,255,255,0.3); }
.theme-kraft .cv-main-title .hl-kraft { display: inline-block; }
.theme-kraft .cv-badge { border-radius: 0; border: 2px solid currentColor; background: transparent; font-family: 'ZCOOL KuaiLe', sans-serif; }
.theme-kraft .cv-tag { border-radius: 0; border: 1px dashed currentColor; background: transparent; }
.theme-kraft .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 40px, rgba(0,0,0,0.015) 40px, rgba(0,0,0,0.015) 41px);
  pointer-events: none;
}
.theme-kraft .cv-bg-decoration::after {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(ellipse at 20% 20%, rgba(255,255,255,0.1) 0%, transparent 40%);
  pointer-events: none;
}
.theme-kraft .cv-mascot { filter: sepia(0.15) contrast(0.95) drop-shadow(2px 2px 4px rgba(0,0,0,0.15)); opacity: 0.85; }

/* ===== 46. blueprint: 蓝图风 ===== */
.theme-blueprint .cv-main-title { font-weight: 500; letter-spacing: 3px; line-height: 1.2; font-family: 'Courier New', monospace; text-shadow: none; }
.theme-blueprint .cv-main-title .hl-blueprint { display: inline-block; }
.theme-blueprint .cv-badge { border-radius: 0; border: 1px solid currentColor; background: transparent; font-family: monospace; letter-spacing: 2px; }
.theme-blueprint .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; font-family: monospace; }
.theme-blueprint .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background:
    repeating-linear-gradient(0deg, transparent, transparent 40px, rgba(255,255,255,0.04) 40px, rgba(255,255,255,0.04) 41px),
    repeating-linear-gradient(90deg, transparent, transparent 40px, rgba(255,255,255,0.04) 40px, rgba(255,255,255,0.04) 41px);
  pointer-events: none;
}
.theme-blueprint .cv-content::before {
  content: 'FIG. 1'; position: absolute; top: 15px; right: 30px;
  font-size: 11px; font-family: monospace; color: var(--accent1); opacity: 0.5; letter-spacing: 2px; z-index: 1;
}
.theme-blueprint .cv-mascot { filter: brightness(1.1) hue-rotate(180deg) opacity(0.7); opacity: 0.7; }

/* ===== 47. starfield: 星空宇宙风 ===== */
.theme-starfield .cv-main-title { font-weight: 700; letter-spacing: 3px; line-height: 1.2; text-shadow: 0 0 15px rgba(255,255,255,0.2); }
.theme-starfield .cv-main-title .hl-starfield { display: inline-block; }
.theme-starfield .cv-badge { border-radius: 50px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.08); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
.theme-starfield .cv-tag { border-radius: 50px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.05); }
.theme-starfield .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: radial-gradient(2px 2px at 10% 20%, rgba(255,255,255,0.8), transparent),
              radial-gradient(1px 1px at 30% 50%, rgba(255,255,255,0.6), transparent),
              radial-gradient(2px 2px at 50% 30%, rgba(255,255,255,0.7), transparent),
              radial-gradient(1px 1px at 70% 60%, rgba(255,255,255,0.5), transparent),
              radial-gradient(2px 2px at 85% 25%, rgba(255,255,255,0.8), transparent),
              radial-gradient(1px 1px at 15% 75%, rgba(255,255,255,0.4), transparent),
              radial-gradient(1px 1px at 60% 85%, rgba(255,255,255,0.6), transparent);
  background-size: 200px 200px; opacity: 0.6; pointer-events: none;
}
.theme-starfield .cv-bg-circle { filter: blur(30px); opacity: 0.12; }
.theme-starfield .cv-mascot { filter: drop-shadow(0 0 8px var(--accent1)) drop-shadow(0 0 16px var(--accent2)) brightness(1.1); opacity: 0.85; }

/* ===== 48. washi: 和纸胶带风 ===== */
.theme-washi .cv-main-title { font-weight: 700; letter-spacing: 2px; line-height: 1.2; font-family: 'ZCOOL KuaiLe', 'Noto Sans SC', sans-serif; text-shadow: 1px 1px 0 rgba(255,255,255,0.4); }
.theme-washi .cv-main-title .hl-washi { display: inline-block; }
.theme-washi .cv-badge { border-radius: 0; border: none; background: rgba(255,255,255,0.5); border-left: 4px solid currentColor; padding: 4px 12px; transform: rotate(-1deg); }
.theme-washi .cv-tag { border-radius: 0; border: none; background: rgba(255,255,255,0.4); border-left: 3px solid currentColor; transform: rotate(1deg); }
.theme-washi .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 24px, rgba(0,0,0,0.02) 24px, rgba(0,0,0,0.02) 25px);
  pointer-events: none;
}
.theme-washi .cv-bg-decoration::after {
  content: ''; position: absolute; top: 0; left: 20%; width: 60px; height: 12px;
  background: var(--accent1); opacity: 0.15; transform: rotate(-3deg); z-index: 0;
}
.theme-washi .cv-mascot { filter: drop-shadow(2px 2px 3px rgba(0,0,0,0.1)); opacity: 0.88; }

/* ===== 49. typewriter: 打字机风 ===== */
.theme-typewriter .cv-main-title { font-weight: 700; letter-spacing: 1px; line-height: 1.3; font-family: 'Courier New', 'Noto Serif SC', monospace; text-shadow: none; }
.theme-typewriter .cv-main-title .hl-typewriter { display: inline-block; }
.theme-typewriter .cv-badge { border-radius: 0; border: 1px solid currentColor; background: transparent; font-family: 'Courier New', monospace; letter-spacing: 2px; }
.theme-typewriter .cv-tag { border-radius: 0; border: 1px solid currentColor; background: transparent; font-family: 'Courier New', monospace; }
.theme-typewriter .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 28px, rgba(0,0,0,0.04) 28px, rgba(0,0,0,0.04) 29px);
  pointer-events: none;
}
.theme-typewriter .cv-content::before {
  content: 'DRAFT'; position: absolute; top: 15px; right: 30px;
  font-size: 11px; font-family: 'Courier New', monospace; color: var(--accent2);
  opacity: 0.3; letter-spacing: 3px; z-index: 1;
}
.theme-typewriter .cv-mascot { filter: grayscale(0.3) sepia(0.1) opacity(0.75); opacity: 0.75; }

/* ===== 50. carnival: 嘉年华风 ===== */
.theme-carnival .cv-main-title { font-weight: 900; letter-spacing: 1px; line-height: 1.1; text-shadow: 2px 2px 0 rgba(0,0,0,0.3); }
.theme-carnival .cv-main-title .hl-carnival { display: inline-block; }
.theme-carnival .cv-badge { border-radius: 50px; border: 2px solid var(--accent1); background: rgba(255,255,255,0.1); box-shadow: 0 0 10px var(--accent1); }
.theme-carnival .cv-tag { border-radius: 50px; border: 2px solid currentColor; background: rgba(0,0,0,0.2); }
.theme-carnival .cv-bg-decoration::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 20px;
  background: repeating-conic-gradient(from 0deg, var(--accent1) 0deg 15deg, var(--accent2) 15deg 30deg, transparent 30deg 45deg);
  background-size: 30px 20px; opacity: 0.15; z-index: 0; pointer-events: none;
}
.theme-carnival .cv-bg-decoration::after {
  content: '🎪'; position: absolute; bottom: 40px; left: 30px;
  font-size: 40px; opacity: 0.12; z-index: 0; pointer-events: none;
}
.theme-carnival .cv-mascot { filter: drop-shadow(0 0 6px var(--accent1)) drop-shadow(0 0 12px var(--accent2)) saturate(1.3); opacity: 0.9; }

/* ===== 51. screenshot: 真实截图风 — 顶部红条 + 大粗字 + 代码/PPT背景 ===== */
.theme-screenshot .cv-bg-decoration::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 12%;
  background: var(--accent1); z-index: 1;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.theme-screenshot .cv-bg-decoration::after {
  content: ''; position: absolute; inset: 12% 0 0 0;
  background-image:
    linear-gradient(rgba(0,0,0,0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.06) 1px, transparent 1px);
  background-size: 32px 32px;
  z-index: 0; pointer-events: none;
}
.theme-screenshot .cv-main-title { font-weight: 900; letter-spacing: -1px; line-height: 1.05; text-shadow: 4px 4px 0 rgba(0,0,0,0.15); position: relative; z-index: 3; }
.theme-screenshot .cv-main-title .hl-screenshot { display: inline-block; }
.theme-screenshot .cv-badge {
  position: absolute; top: 4%; left: 4%; z-index: 5;
  background: #fff; color: var(--accent1);
  border-radius: 0; border: 3px solid var(--accent1);
  font-weight: 900; letter-spacing: 1px; padding: 4px 12px;
  transform: rotate(-2deg); box-shadow: 3px 3px 0 rgba(0,0,0,0.2);
}
.theme-screenshot .cv-tag { border-radius: 0; border: 2px solid currentColor; background: #fff; font-weight: 800; }
.theme-screenshot .cv-mascot { display: none; }  /* 不用插画角色 */
.theme-screenshot .cv-emoji-deco { display: none; }
.theme-screenshot .cv-content { position: relative; z-index: 3; }
.theme-screenshot .cv-content::before {
  content: '截屏自视频 00:42'; position: absolute; bottom: -8%; right: 3%;
  font-family: 'SF Mono', 'Courier New', monospace; font-size: 12px;
  color: rgba(0,0,0,0.4); z-index: 4;
}
.theme-screenshot .cv-content::after {
  content: '▶'; position: absolute; top: -6%; right: 4%;
  font-size: 24px; color: var(--accent1); z-index: 4;
  width: 36px; height: 36px; background: #fff; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

/* ===== 52. portrait: 真人出镜风 — 大头像圈 + 顶部色条 + 粗字 ===== */
.theme-portrait .cv-bg-decoration::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 8%;
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  z-index: 1;
}
.theme-portrait .cv-bg-decoration::after {
  content: '👤'; position: absolute; right: 4%; top: 14%;
  font-size: 180px; opacity: 0.9; z-index: 0; pointer-events: none;
  background: var(--accent1); width: 200px; height: 200px;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3); border: 6px solid #fff;
}
/* 有真照片时隐藏CSS伪元素头像 */
.cv-has-photo.theme-portrait .cv-bg-decoration::after { display: none; }
.theme-portrait .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.08; text-shadow: 3px 3px 0 rgba(0,0,0,0.2); }
.theme-portrait .cv-main-title .hl-portrait { display: inline-block; }
.theme-portrait .cv-badge { border-radius: 50px; background: var(--accent1); color: #000; font-weight: 900; border: 3px solid #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.theme-portrait .cv-tag { border-radius: 50px; background: rgba(255,255,255,0.2); color: #fff; border: 1px solid rgba(255,255,255,0.4); backdrop-filter: blur(6px); }
.theme-portrait .cv-mascot { display: none; }  /* 不用插画，用纯CSS人物圈 */
.theme-portrait .cv-emoji-deco { display: none; }
.theme-portrait .cv-content { position: relative; z-index: 3; max-width: 65%; }
.theme-portrait .cv-content::before {
  content: '@本期嘉宾'; position: absolute; top: -8%; left: 0;
  font-size: 14px; color: var(--accent1); font-weight: 700; letter-spacing: 2px;
  background: rgba(0,0,0,0.6); padding: 2px 10px; border-radius: 4px;
}

/* ===== 53. product: 实物产品风 — 渐变背景 + 产品框 + 问号 ===== */
.theme-product .cv-bg-decoration::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 70% 50%, rgba(255,255,255,0.1) 0%, transparent 60%);
  z-index: 0; pointer-events: none;
}
.theme-product .cv-bg-decoration::after {
  content: '?'; position: absolute; top: 8%; right: 4%;
  font-size: 200px; font-weight: 900; color: var(--accent1); opacity: 0.15;
  z-index: 0; pointer-events: none; line-height: 1;
}
.theme-product .cv-main-title { font-weight: 900; letter-spacing: 1px; line-height: 1.1; text-shadow: 2px 2px 0 rgba(0,0,0,0.3); position: relative; z-index: 3; }
.theme-product .cv-main-title .hl-product { display: inline-block; }
.theme-product .cv-badge { border-radius: 8px; background: var(--accent1); color: #000; font-weight: 900; box-shadow: 0 4px 12px rgba(0,0,0,0.25); }
.theme-product .cv-tag { border-radius: 8px; background: rgba(255,255,255,0.2); color: #fff; font-weight: 700; border: 1px solid rgba(255,255,255,0.3); }
.theme-product .cv-mascot { display: none; }
.theme-product .cv-emoji-deco { display: none; }
.theme-product .cv-content { position: relative; z-index: 3; }
.theme-product .cv-content::before {
  content: '开箱'; position: absolute; top: -10%; left: 0;
  background: var(--accent2); color: #000; font-weight: 900; font-size: 24px;
  padding: 4px 16px; transform: rotate(-3deg);
  box-shadow: 4px 4px 0 rgba(0,0,0,0.3);
}
.theme-product .cv-content::after {
  content: 'REVIEW'; position: absolute; bottom: -8%; right: 3%;
  font-family: 'Courier New', monospace; font-size: 11px;
  color: var(--accent1); letter-spacing: 4px; font-weight: 700;
  border: 1px solid var(--accent1); padding: 2px 8px;
}

/* ===== 54. contrast: 对比冲击风 — 左右/上下分割 + 反差色 ===== */
.theme-contrast .cv-bg-decoration::before {
  content: 'VS'; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  font-size: 120px; font-weight: 900; color: var(--accent2); opacity: 0.2;
  z-index: 1; pointer-events: none; font-family: 'Impact', sans-serif;
  letter-spacing: -8px;
}
.theme-contrast .cv-bg-decoration::after {
  content: ''; position: absolute; top: 0; right: 0; bottom: 0; width: 50%;
  background: linear-gradient(135deg, var(--accent1) 0%, var(--accent2) 100%);
  opacity: 0.15; z-index: 0; pointer-events: none;
  clip-path: polygon(20% 0, 100% 0, 100% 100%, 0 100%);
}
.theme-contrast .cv-main-title { font-weight: 900; letter-spacing: -1px; line-height: 1.05; position: relative; z-index: 3; }
.theme-contrast .cv-main-title .hl-contrast { display: inline-block; }
.theme-contrast .cv-badge { border-radius: 0; background: #000; color: var(--accent1); font-weight: 900; border: 3px solid var(--accent1); letter-spacing: 2px; }
.theme-contrast .cv-tag { border-radius: 0; background: var(--accent1); color: #000; font-weight: 800; border: 2px solid #000; }
.theme-contrast .cv-mascot { display: none; }
.theme-contrast .cv-emoji-deco { display: none; }
.theme-contrast .cv-content { position: relative; z-index: 3; }
.theme-contrast .cv-content::before {
  content: 'A'; position: absolute; top: 4%; left: 4%;
  font-size: 60px; font-weight: 900; color: var(--accent1); font-family: Impact, sans-serif;
  z-index: 4; line-height: 1;
}
.theme-contrast .cv-content::after {
  content: 'B'; position: absolute; top: 4%; right: 4%;
  font-size: 60px; font-weight: 900; color: var(--accent2); font-family: Impact, sans-serif;
  z-index: 4; line-height: 1;
}

/* ===== 55. zoom: 局部放大风 — 红色圆圈 + 放大镜 + 重点标注 ===== */
.theme-zoom .cv-bg-decoration::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background-image:
    linear-gradient(rgba(220,38,38,0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(220,38,38,0.08) 1px, transparent 1px);
  background-size: 24px 24px;
  z-index: 0; pointer-events: none;
}
.theme-zoom .cv-bg-decoration::after {
  content: '🔍'; position: absolute; bottom: 12%; right: 6%;
  font-size: 100px; opacity: 0.25; z-index: 1; pointer-events: none;
  filter: drop-shadow(0 0 8px var(--accent1));
}
.theme-zoom .cv-main-title { font-weight: 900; letter-spacing: 0; line-height: 1.08; text-shadow: 2px 2px 0 rgba(0,0,0,0.2); position: relative; z-index: 3; }
.theme-zoom .cv-main-title .hl-zoom { display: inline-block; }
.theme-zoom .cv-badge { border-radius: 50px; background: var(--accent1); color: #fff; font-weight: 900; border: 3px solid #fff; box-shadow: 0 4px 16px rgba(220,38,38,0.4); }
.theme-zoom .cv-tag { border-radius: 50px; background: var(--accent2); color: #fff; font-weight: 800; border: 2px solid #fff; }
.theme-zoom .cv-mascot { display: none; }
.theme-zoom .cv-emoji-deco { display: none; }
.theme-zoom .cv-content { position: relative; z-index: 3; }
.theme-zoom .cv-content::before {
  content: '⭕ 看这里'; position: absolute; top: -6%; left: 0;
  font-size: 14px; color: var(--accent1); font-weight: 900; letter-spacing: 1px;
  z-index: 4;
}
.theme-zoom .cv-content::after {
  content: '↑ 重点'; position: absolute; bottom: 8%; right: 4%;
  font-size: 14px; color: var(--accent1); font-weight: 900; z-index: 4;
  background: #fff; padding: 2px 8px; border-radius: 4px;
  border: 2px solid var(--accent1);
}

/* ===== 真人出镜照片 v4 — B站风格：照片清晰可见+文字描边 ===== */

/* 照片：全屏背景，保持清晰 */
.cv-user-photo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
  pointer-events: none;
}

/* 照片位置参数（全屏模式下不生效） */
.cv-photo-right, .cv-photo-left, .cv-photo-center {
  inset: 0; width: 100%; height: 100%;
}

/* 有照片时：仅底部轻微暗角，保持人物清晰可见 */
.cv-has-photo::before {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  z-index: 1 !important;
  background: linear-gradient(0deg, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.15) 40%, rgba(0,0,0,0.05) 100%) !important;
  pointer-events: none !important;
}

/* 有照片时：文字加粗描边，保证在任何背景上可读 */
.cv-has-photo .cv-main-title {
  text-shadow: 
    3px 3px 0 rgba(0,0,0,0.8),
    -2px -2px 0 rgba(0,0,0,0.8),
    2px -2px 0 rgba(0,0,0,0.8),
    -2px 2px 0 rgba(0,0,0,0.8),
    0 0 20px rgba(0,0,0,0.6) !important;
  -webkit-text-stroke: 1px rgba(0,0,0,0.3) !important;
}

.cv-has-photo .cv-sub-title {
  text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 12px rgba(0,0,0,0.5) !important;
}

.cv-has-photo .cv-tag {
  background: rgba(0,0,0,0.5) !important;
  backdrop-filter: blur(4px) !important;
  border: 1px solid rgba(255,255,255,0.2) !important;
}

.cv-has-photo .cv-badge {
  background: rgba(0,0,0,0.5) !important;
  backdrop-filter: blur(4px) !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
}

/* 有照片时内容区提升层级 */
.cv-has-photo .cv-content { position: relative; z-index: 5 !important; }
.cv-has-photo .cv-bg-decoration { z-index: 0 !important; }

/* 有照片时隐藏mascot和emoji装饰 */
.cv-has-photo .cv-mascot { display: none !important; }
.cv-has-photo .cv-mascot-bg { display: none !important; }
.cv-has-photo .cv-emoji-deco { display: none !important; }

/* 有照片时隐藏CSS伪元素装饰 */
.cv-has-photo .cv-bg-decoration::before { display: none !important; }
.cv-has-photo .cv-bg-decoration::after { display: none !important; }

/* 底部栏 */
.cv-has-photo .cv-bottom-bar {
  background: rgba(0,0,0,0.6) !important;
  backdrop-filter: blur(8px) !important;
}

/* ===== 故障风（glitch） ===== */
.theme-glitch .cv-main-title { font-weight:900;letter-spacing:2px;line-height:1.05;text-shadow:3px 0 #ff0040,-3px 0 #00ff41,0 0 10px rgba(0,255,65,0.3); }
.theme-glitch .cv-main-title .hl-glitch { display: inline-block; }
.theme-glitch .cv-badge { border-radius:0;border:2px solid currentColor;background:transparent;clip-path:polygon(0 0,100% 0,95% 100%,5% 100%); }
.theme-glitch .cv-mascot { filter:drop-shadow(2px 0 #ff0040) drop-shadow(-2px 0 #00ff41);opacity:0.85; }

/* ===== 合成波（synthwave） ===== */
.theme-synthwave .cv-main-title { font-weight:900;letter-spacing:3px;line-height:1.1;text-shadow:0 0 20px rgba(255,110,199,0.5); }
.theme-synthwave .cv-main-title .hl-synthwave { display: inline-block; }
.theme-synthwave .cv-badge { border-radius:0;border:2px solid var(--accent1);background:rgba(0,0,0,0.3);letter-spacing:2px; }
.theme-synthwave .cv-mascot { filter:drop-shadow(0 0 10px var(--accent1)) drop-shadow(0 0 20px var(--accent2));opacity:0.85; }

/* ===== 矩阵代码（matrix） ===== */
.theme-matrix .cv-main-title { font-weight:900;letter-spacing:2px;line-height:1.08;font-family:'Courier New',monospace;text-shadow:0 0 15px rgba(0,255,65,0.4); }
.theme-matrix .cv-main-title .hl-matrix { display: inline-block; }
.theme-matrix .cv-badge { border-radius:0;border:1px solid var(--accent1);background:transparent;font-family:monospace;letter-spacing:2px; }
.theme-matrix .cv-mascot { filter:brightness(1.2) hue-rotate(80deg);opacity:0.75; }

/* ===== 量子科技（quantum） ===== */
.theme-quantum .cv-main-title { font-weight:700;letter-spacing:3px;line-height:1.2;text-shadow:0 0 15px rgba(124,58,237,0.4); }
.theme-quantum .cv-main-title .hl-quantum { display: inline-block; }
.theme-quantum .cv-badge { border-radius:50px;border:1px solid var(--accent1);background:rgba(124,58,237,0.1);backdrop-filter:blur(6px); }
.theme-quantum .cv-mascot { filter:drop-shadow(0 0 8px var(--accent1));opacity:0.85; }

/* ===== 深海蓝调（ocean） ===== */
.theme-ocean .cv-main-title { font-weight:700;letter-spacing:2px;line-height:1.15;text-shadow:0 2px 10px rgba(0,180,216,0.3); }
.theme-ocean .cv-main-title .hl-ocean { display: inline-block; }
.theme-ocean .cv-badge { border-radius:50px;border:1px solid var(--accent1);background:rgba(0,180,216,0.1);backdrop-filter:blur(6px); }
.theme-ocean .cv-mascot { filter:drop-shadow(0 0 8px var(--accent1));opacity:0.85; }

/* ===== 冰晶透蓝（ice） ===== */
.theme-ice .cv-main-title { font-weight:600;letter-spacing:3px;line-height:1.2;text-shadow:0 0 15px rgba(125,211,252,0.3); }
.theme-ice .cv-main-title .hl-ice { display: inline-block; }
.theme-ice .cv-badge { border-radius:12px;border:1px solid rgba(125,211,252,0.4);background:rgba(125,211,252,0.1);backdrop-filter:blur(6px); }
.theme-ice .cv-mascot { filter:drop-shadow(0 0 8px rgba(125,211,252,0.3)) brightness(1.1);opacity:0.85; }

/* ===== 毛玻璃质感（glassmorph） ===== */
.theme-glassmorph .cv-main-title { font-weight:700;letter-spacing:2px;line-height:1.2;text-shadow:0 2px 10px rgba(0,0,0,0.2); }
.theme-glassmorph .cv-main-title .hl-glassmorph { display: inline-block; }
.theme-glassmorph .cv-badge { border-radius:12px;border:1px solid rgba(255,255,255,0.3);background:rgba(255,255,255,0.15);backdrop-filter:blur(10px); }
.theme-glassmorph .cv-mascot { filter:drop-shadow(0 0 8px rgba(255,255,255,0.3));opacity:0.85; }

/* ===== 复古未来（retrofuturism） ===== */
.theme-retrofuturism .cv-main-title { font-weight:900;letter-spacing:3px;line-height:1.1;text-shadow:2px 2px 0 rgba(0,0,0,0.3),0 0 15px rgba(255,110,199,0.3); }
.theme-retrofuturism .cv-main-title .hl-retrofuturism { display: inline-block; }
.theme-retrofuturism .cv-badge { border-radius:0;border:2px solid var(--accent1);background:rgba(0,0,0,0.3);letter-spacing:2px; }
.theme-retrofuturism .cv-mascot { filter:drop-shadow(0 0 8px var(--accent1)) saturate(1.3);opacity:0.85; }

/* ===== 银河星系（galaxy） ===== */
.theme-galaxy .cv-main-title { font-weight:700;letter-spacing:3px;line-height:1.2;text-shadow:0 0 20px rgba(168,85,247,0.4); }
.theme-galaxy .cv-main-title .hl-galaxy { display: inline-block; }
.theme-galaxy .cv-badge { border-radius:50px;border:1px solid rgba(255,255,255,0.3);background:rgba(255,255,255,0.08);backdrop-filter:blur(6px); }
.theme-galaxy .cv-mascot { filter:drop-shadow(0 0 10px var(--accent1)) brightness(1.1);opacity:0.85; }

/* ===== 糖果甜蜜（candy） ===== */
.theme-candy .cv-main-title { font-weight:800;letter-spacing:1px;line-height:1.15;font-family:'ZCOOL KuaiLe',sans-serif; }
.theme-candy .cv-main-title .hl-candy { display: inline-block; }
.theme-candy .cv-badge { border-radius:50px;border:2px solid var(--accent1);background:rgba(255,255,255,0.5); }
.theme-candy .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.1));opacity:0.95; }

/* ===== 蒸汽朋克（steampunk） ===== */
.theme-steampunk .cv-main-title { font-weight:800;letter-spacing:2px;line-height:1.1;font-family:'Noto Serif SC',serif; }
.theme-steampunk .cv-main-title .hl-steampunk { display: inline-block; }
.theme-steampunk .cv-badge { border-radius:0;border:2px solid var(--accent1);background:transparent;letter-spacing:2px; }
.theme-steampunk .cv-mascot { filter:sepia(0.4) contrast(1.1);opacity:0.85; }

/* ===== 黑色电影（noir） ===== */
.theme-noir .cv-main-title { font-weight:700;letter-spacing:4px;line-height:1.15;font-family:'Noto Serif SC',serif; }
.theme-noir .cv-main-title .hl-noir { display: inline-block; }
.theme-noir .cv-badge { border-radius:0;border:1px solid currentColor;background:transparent;letter-spacing:3px;font-size:11px; }
.theme-noir .cv-mascot { filter:grayscale(0.8) contrast(1.2);opacity:0.7; }

/* ===== 哥特暗黑（gothic） ===== */
.theme-gothic .cv-main-title { font-weight:900;letter-spacing:3px;line-height:1.1;font-family:'Noto Serif SC',serif; }
.theme-gothic .cv-main-title .hl-gothic { display: inline-block; }
.theme-gothic .cv-badge { border-radius:0;border:2px solid currentColor;background:transparent;letter-spacing:3px; }
.theme-gothic .cv-mascot { filter:brightness(0.8) contrast(1.2);opacity:0.8; }

/* ===== 巴洛克华丽（baroque） ===== */
.theme-baroque .cv-main-title { font-weight:700;letter-spacing:4px;line-height:1.15;font-family:'Noto Serif SC',serif; }
.theme-baroque .cv-main-title .hl-baroque { display: inline-block; }
.theme-baroque .cv-badge { border-radius:0;border:2px solid var(--accent1);background:transparent;letter-spacing:3px; }
.theme-baroque .cv-mascot { filter:sepia(0.2) drop-shadow(0 0 6px rgba(212,175,55,0.3));opacity:0.85; }

/* ===== 部落图腾（tribal） ===== */
.theme-tribal .cv-main-title { font-weight:900;letter-spacing:1px;line-height:1.1; }
.theme-tribal .cv-main-title .hl-tribal { display: inline-block; }
.theme-tribal .cv-badge { border-radius:0;border:2px solid currentColor;background:transparent; }
.theme-tribal .cv-mascot { filter:sepia(0.3) contrast(1.1);opacity:0.9; }

/* ===== 装饰艺术（artdeco） ===== */
.theme-artdeco .cv-main-title { font-weight:700;letter-spacing:4px;line-height:1.15; }
.theme-artdeco .cv-main-title .hl-artdeco { display: inline-block; }
.theme-artdeco .cv-badge { border-radius:0;border:1px solid var(--accent1);background:transparent;letter-spacing:3px;clip-path:polygon(5% 0,100% 0,95% 100%,0 100%); }
.theme-artdeco .cv-mascot { filter:drop-shadow(0 0 6px rgba(212,175,55,0.3));opacity:0.85; }

/* ===== 烈焰燃烧（fire） ===== */
.theme-fire .cv-main-title { font-weight:900;letter-spacing:1px;line-height:1.05;text-shadow:2px 2px 0 rgba(0,0,0,0.5),0 0 20px rgba(255,69,0,0.3); }
.theme-fire .cv-main-title .hl-fire { display: inline-block; }
.theme-fire .cv-badge { border-radius:0;border:2px solid var(--accent1);background:rgba(255,69,0,0.15); }
.theme-fire .cv-mascot { filter:drop-shadow(0 0 10px rgba(255,69,0,0.5)) brightness(1.1);opacity:0.85; }

/* ===== 街头潮牌（streetwear） ===== */
.theme-streetwear .cv-main-title { font-weight:900;letter-spacing:0;line-height:1.05;text-shadow:3px 3px 0 rgba(0,0,0,0.5); }
.theme-streetwear .cv-main-title .hl-streetwear { display: inline-block; }
.theme-streetwear .cv-badge { border-radius:0;border:3px solid currentColor;background:transparent;font-weight:900;letter-spacing:2px; }
.theme-streetwear .cv-mascot { filter:drop-shadow(3px 3px 0 rgba(0,0,0,0.5));opacity:0.9; }

/* ===== 迷幻色彩（psychadelic） ===== */
.theme-psychadelic .cv-main-title { font-weight:900;letter-spacing:1px;line-height:1.1;text-shadow:3px 3px 0 rgba(0,0,0,0.3); }
.theme-psychadelic .cv-main-title .hl-psychadelic { display: inline-block; }
.theme-psychadelic .cv-badge { border-radius:50px;border:2px solid var(--accent1);background:rgba(0,0,0,0.3); }
.theme-psychadelic .cv-mascot { filter:saturate(1.5) hue-rotate(10deg);opacity:0.9; }

/* ===== 马赛克拼图（mosaic） ===== */
.theme-mosaic .cv-main-title { font-weight:900;letter-spacing:1px;line-height:1.1; }
.theme-mosaic .cv-main-title .hl-mosaic { display: inline-block; }
.theme-mosaic .cv-badge { border-radius:0;border:2px solid currentColor;background:transparent; }
.theme-mosaic .cv-mascot { filter:contrast(1.1);opacity:0.85; }

/* ===== 头版头条（newspaper2） ===== */
.theme-newspaper2 .cv-main-title { font-weight:900;letter-spacing:-0.5px;line-height:1.0;font-family:'Noto Serif SC',serif; }
.theme-newspaper2 .cv-main-title .hl-newspaper2 { display: inline-block; }
.theme-newspaper2 .cv-badge { border-radius:0;border:3px solid var(--accent1);background:var(--accent1);color:#fff;font-weight:900;letter-spacing:2px; }
.theme-newspaper2 .cv-mascot { display:none; }

/* ===== 机能工装（techwear） ===== */
.theme-techwear .cv-main-title { font-weight:900;letter-spacing:2px;line-height:1.05;text-transform:uppercase; }
.theme-techwear .cv-main-title .hl-techwear { display: inline-block; }
.theme-techwear .cv-badge { border-radius:0;border:2px solid var(--accent1);background:transparent;font-weight:900;letter-spacing:3px;font-size:11px;clip-path:polygon(0 0,100% 0,95% 100%,5% 100%); }
.theme-techwear .cv-mascot { filter:brightness(0.9) contrast(1.2);opacity:0.85; }

/* ===== 赛博废土（cyberpunk2） ===== */
.theme-cyberpunk2 .cv-main-title { font-weight:900;letter-spacing:1px;line-height:1.05;text-shadow:3px 3px 0 rgba(0,0,0,0.5); }
.theme-cyberpunk2 .cv-main-title .hl-cyberpunk2 { display: inline-block; }
.theme-cyberpunk2 .cv-badge { border-radius:0;border:2px solid var(--accent1);background:rgba(0,0,0,0.4); }
.theme-cyberpunk2 .cv-mascot { filter:sepia(0.3) contrast(1.2) brightness(0.9);opacity:0.85; }

/* ===== 霓虹都市（neoncity） ===== */
.theme-neoncity .cv-main-title { font-weight:900;letter-spacing:2px;line-height:1.1;text-shadow:0 0 15px rgba(255,0,110,0.4); }
.theme-neoncity .cv-main-title .hl-neoncity { display: inline-block; }
.theme-neoncity .cv-badge { border-radius:50px;border:2px solid var(--accent1);background:transparent;box-shadow:0 0 8px var(--accent1); }
.theme-neoncity .cv-mascot { filter:drop-shadow(0 0 8px var(--accent1)) drop-shadow(0 0 16px var(--accent2));opacity:0.85; }

/* ===== 中世纪（medieval） ===== */
.theme-medieval .cv-main-title { font-weight:900;letter-spacing:2px;line-height:1.1;font-family:'Noto Serif SC',serif; }
.theme-medieval .cv-main-title .hl-medieval { display: inline-block; }
.theme-medieval .cv-badge { border-radius:0;border:3px solid var(--accent1);background:transparent;letter-spacing:3px; }
.theme-medieval .cv-mascot { filter:sepia(0.3) contrast(1.1);opacity:0.85; }

/* ===== 水彩晕染（watercolor） ===== */
.theme-watercolor .cv-main-title { font-weight:600;letter-spacing:2px;line-height:1.2; }
.theme-watercolor .cv-main-title .hl-watercolor { display: inline-block; }
.theme-watercolor .cv-badge { border-radius:20px;border:1px solid var(--accent1);background:rgba(255,255,255,0.3);backdrop-filter:blur(4px); }
.theme-watercolor .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.1));opacity:0.85; }

/* ===== 禅意侘寂（zen） ===== */
.theme-zen .cv-main-title { font-weight:400;letter-spacing:6px;line-height:1.3;font-family:'Noto Serif SC',serif; }
.theme-zen .cv-main-title .hl-zen { display: inline-block; }
.theme-zen .cv-badge { border-radius:0;border:1px solid currentColor;background:transparent;letter-spacing:3px;font-weight:400; }
.theme-zen .cv-mascot { filter:grayscale(0.3) opacity(0.7);opacity:0.7; }

/* ===== 北欧极简（scandinavian） ===== */
.theme-scandinavian .cv-main-title { font-weight:300;letter-spacing:4px;line-height:1.3; }
.theme-scandinavian .cv-main-title .hl-scandinavian { display: inline-block; }
.theme-scandinavian .cv-badge { border-radius:0;border:1px solid currentColor;background:transparent;letter-spacing:2px;font-weight:400;font-size:11px; }
.theme-scandinavian .cv-mascot { filter:brightness(0.95) saturate(0.8);opacity:0.75; }

/* ===== 波西米亚（boho） ===== */
.theme-boho .cv-main-title { font-weight:600;letter-spacing:2px;line-height:1.2; }
.theme-boho .cv-main-title .hl-boho { display: inline-block; }
.theme-boho .cv-badge { border-radius:20px;border:2px solid currentColor;background:transparent;letter-spacing:1px; }
.theme-boho .cv-mascot { filter:sepia(0.2) saturate(1.2);opacity:0.85; }

/* ===== 雨天氛围（rain） ===== */
.theme-rain .cv-main-title { font-weight:600;letter-spacing:3px;line-height:1.2; }
.theme-rain .cv-main-title .hl-rain { display: inline-block; }
.theme-rain .cv-badge { border-radius:20px;border:1px solid rgba(255,255,255,0.3);background:rgba(255,255,255,0.1);backdrop-filter:blur(4px); }
.theme-rain .cv-mascot { filter:brightness(0.9) contrast(1.05);opacity:0.8; }

/* ===== 日落黄昏（sunset） ===== */
.theme-sunset .cv-main-title { font-weight:800;letter-spacing:2px;line-height:1.1; }
.theme-sunset .cv-main-title .hl-sunset { display: inline-block; }
.theme-sunset .cv-badge { border-radius:50px;border:2px solid rgba(255,255,255,0.4);background:rgba(0,0,0,0.2); }
.theme-sunset .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.3));opacity:0.85; }

/* ===== 森林秘境（forest） ===== */
.theme-forest .cv-main-title { font-weight:700;letter-spacing:2px;line-height:1.15; }
.theme-forest .cv-main-title .hl-forest { display: inline-block; }
.theme-forest .cv-badge { border-radius:20px;border:1px solid var(--accent1);background:rgba(34,197,94,0.1); }
.theme-forest .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.2)) brightness(1.05);opacity:0.9; }

/* ===== 沙漠暖阳（desert） ===== */
.theme-desert .cv-main-title { font-weight:700;letter-spacing:2px;line-height:1.15; }
.theme-desert .cv-main-title .hl-desert { display: inline-block; }
.theme-desert .cv-badge { border-radius:0;border:2px solid currentColor;background:transparent; }
.theme-desert .cv-mascot { filter:sepia(0.2) brightness(1.05);opacity:0.85; }

/* ===== 复古怀旧（vintage） ===== */
.theme-vintage .cv-main-title { font-weight:700;letter-spacing:2px;line-height:1.15;font-family:'Noto Serif SC',serif; }
.theme-vintage .cv-main-title .hl-vintage { display: inline-block; }
.theme-vintage .cv-badge { border-radius:0;border:2px solid currentColor;background:transparent;letter-spacing:2px; }
.theme-vintage .cv-mascot { filter:sepia(0.4) contrast(0.9) brightness(0.95);opacity:0.8; }

/* ===== 樱花粉嫩（cherry） ===== */
.theme-cherry .cv-main-title { font-weight:700;letter-spacing:2px;line-height:1.2;font-family:'ZCOOL KuaiLe',sans-serif; }
.theme-cherry .cv-main-title .hl-cherry { display: inline-block; }
.theme-cherry .cv-badge { border-radius:50px;border:2px solid var(--accent1);background:rgba(255,255,255,0.5); }
.theme-cherry .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.08));opacity:0.9; }

/* ===== 版画木刻（woodcut） ===== */
.theme-woodcut .cv-main-title { font-weight:900;letter-spacing:1px;line-height:1.1;font-family:'Noto Serif SC',serif; }
.theme-woodcut .cv-main-title .hl-woodcut { display: inline-block; }
.theme-woodcut .cv-badge { border-radius:0;border:2px solid currentColor;background:transparent; }
.theme-woodcut .cv-mascot { filter:grayscale(0.5) contrast(1.3);opacity:0.8; }

/* ===== 格纹学院（plaid） ===== */
.theme-plaid .cv-main-title { font-weight:700;letter-spacing:2px;line-height:1.15;font-family:'Noto Serif SC',serif; }
.theme-plaid .cv-main-title .hl-plaid { display: inline-block; }
.theme-plaid .cv-badge { border-radius:0;border:2px solid currentColor;background:transparent;letter-spacing:2px; }
.theme-plaid .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.2));opacity:0.85; }

/* ===== 折纸手工（origami） ===== */
.theme-origami .cv-main-title { font-weight:600;letter-spacing:2px;line-height:1.2; }
.theme-origami .cv-main-title .hl-origami { display: inline-block; }
.theme-origami .cv-badge { border-radius:8px;border:2px solid currentColor;background:transparent; }
.theme-origami .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.1));opacity:0.9; }

/* ===== 纸飞机（paperplane） ===== */
.theme-paperplane .cv-main-title { font-weight:600;letter-spacing:3px;line-height:1.2; }
.theme-paperplane .cv-main-title .hl-paperplane { display: inline-block; }
.theme-paperplane .cv-badge { border-radius:20px;border:2px solid currentColor;background:rgba(255,255,255,0.3); }
.theme-paperplane .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.1));opacity:0.9; }

/* ===== Lo-Fi慵懒（lofi） ===== */
.theme-lofi .cv-main-title { font-weight:500;letter-spacing:2px;line-height:1.25; }
.theme-lofi .cv-main-title .hl-lofi { display: inline-block; }
.theme-lofi .cv-badge { border-radius:20px;border:1px solid rgba(255,255,255,0.3);background:rgba(255,255,255,0.1);backdrop-filter:blur(6px); }
.theme-lofi .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.2));opacity:0.85; }

/* ===== 海浪波纹（wave） ===== */
.theme-wave .cv-main-title { font-weight:600;letter-spacing:3px;line-height:1.2; }
.theme-wave .cv-main-title .hl-wave { display: inline-block; }
.theme-wave .cv-badge { border-radius:20px;border:1px solid var(--accent1);background:rgba(14,165,233,0.1); }
.theme-wave .cv-mascot { filter:drop-shadow(0 0 6px var(--accent1));opacity:0.85; }

/* ===== 童话梦幻（fairy） ===== */
.theme-fairy .cv-main-title { font-weight:700;letter-spacing:2px;line-height:1.2;font-family:'ZCOOL KuaiLe',sans-serif; }
.theme-fairy .cv-main-title .hl-fairy { display: inline-block; }
.theme-fairy .cv-badge { border-radius:50px;border:2px solid var(--accent1);background:rgba(255,255,255,0.5); }
.theme-fairy .cv-mascot { filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.1));opacity:0.9; }

/* ===== 军事硬核（military） ===== */
.theme-military .cv-main-title { font-weight:900;letter-spacing:2px;line-height:1.05;text-transform:uppercase; }
.theme-military .cv-main-title .hl-military { display: inline-block; }
.theme-military .cv-badge { border-radius:0;border:2px solid var(--accent1);background:transparent;font-weight:900;letter-spacing:2px; }
.theme-military .cv-mascot { filter:brightness(0.9) contrast(1.2);opacity:0.85; }

/* ===== 云端轻盈（cloud） ===== */
.theme-cloud .cv-main-title { font-weight:300;letter-spacing:4px;line-height:1.3; }
.theme-cloud .cv-main-title .hl-cloud { display: inline-block; }
.theme-cloud .cv-badge { border-radius:20px;border:1px solid var(--accent1);background:rgba(255,255,255,0.5);backdrop-filter:blur(6px); }
.theme-cloud .cv-mascot { filter:drop-shadow(2px 2px 6px rgba(0,0,0,0.08));opacity:0.8; }

/* ===== 地球生态（earth） ===== */
.theme-earth .cv-main-title { font-weight:600;letter-spacing:3px;line-height:1.2; }
.theme-earth .cv-main-title .hl-earth { display: inline-block; }
.theme-earth .cv-badge { border-radius:50px;border:1px solid var(--accent1);background:rgba(34,197,94,0.1); }
.theme-earth .cv-mascot { filter:drop-shadow(0 0 6px var(--accent1));opacity:0.85; }

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
    all_themes = ["auto",
        "bold","cyber","anime","funny","luxury","fresh","gaming","food","cinema","cute",
        "paper","variety","doodle","magazine","minimal","dopamine","guochao","pixel","journal",
        "vaporwave","acid","memphis","clay","glass","sticker","comic","neon","retro","collage","aurora",
        "ink","stamp","newspaper","polaroid","risograph","film","graffiti","ribbon","gradientmesh","brutalist",
        "pastel","popart","terrarium","holographic","kraft","blueprint","starfield","washi","typewriter","carnival",
        "screenshot","portrait","product","contrast","zoom",
        "glitch","synthwave","matrix","quantum","ocean","ice","glassmorph","retrofuturism","galaxy","candy","steampunk","noir","gothic","baroque","tribal","artdeco","fire","streetwear","psychadelic","mosaic","newspaper2","techwear","cyberpunk2","neoncity","medieval","watercolor","zen","scandinavian","boho","rain","sunset","forest","desert","vintage","cherry","woodcut","plaid","origami","paperplane","lofi",
        "tech","hot","cool","warm","dark","gradient","animal"]
    p = argparse.ArgumentParser(
        description="视频封面生成器 v9.0 - 100种风格 × 411套配色 × 真人出镜 × 爆款标题",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\n示例:\n"
               "  python3 generate_covers.py --title 'Docker一装，运维轻松10倍' --theme cyber\n"
               "  python3 generate_covers.py --title '给爷来个Key' --platform all --theme bold\n"
               "  python3 generate_covers.py --title '猫猫编程日记' --theme cute --platform all\n"
               "  python3 generate_covers.py --title '5款AI工具安利' --theme paper --platform all\n"
               "  python3 generate_covers.py --title '这反应绝了' --theme variety --platform all\n"
               "  python3 generate_covers.py --input ppt.html --output covers.html --platform all\n"
               "  python3 generate_covers.py --config covers.json\n\n"
               "55种风格: bold/cyber/anime/funny/luxury/fresh/gaming/food/cinema/cute/paper/variety/doodle\n"
               "  + magazine/minimal/dopamine/guochao/pixel/journal/vaporwave/acid/memphis/clay\n"
               "  + glass/sticker/comic/neon/retro/collage/aurora/ink/stamp/newspaper/polaroid\n"
               "  + risograph/film/graffiti/ribbon/gradientmesh/brutalist/pastel/popart/terrarium\n"
               "  + holographic/kraft/blueprint/starfield/washi/typewriter/carnival\n"
               "  + screenshot/portrait/product/contrast/zoom (真实派)")
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
    p.add_argument("--photo-url", help="真人出镜照片URL或本地路径")
    p.add_argument("--auto-icons", action="store_true", help="根据标题自动从 iconfont.cn 下载图标")
    p.add_argument("--photo-position", default="right", choices=["right","left","center"], help="照片位置")
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
                 "tags":tg,"badge":a.badge or "","quote":a.quote or "","theme":a.theme,
                 "photo_url":a.photo_url,"photo_position":a.photo_position,
                 "auto_icons":a.auto_icons}
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
