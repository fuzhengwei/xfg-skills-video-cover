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

    "python_1": {"bg": "#151911", "accent1": "#00ff00", "accent2": "#95b9FF", "name": "Python蛇暗夜", "theme": "python"},
    "python_2": {"bg": "#f0f0f0", "accent1": "#15007f", "accent2": "#5b7F1d", "name": "Python蛇清新", "theme": "python", "text_color": "#1a1a1a"},
    "python_3": {"bg": "linear-gradient(135deg,#959580 0%,#95b9ff 100%)", "accent1": "#ffffff", "accent2": "#095bff", "name": "Python蛇渐变", "theme": "python", "is_gradient": True},
    "python_4": {"bg": "#0095b9", "accent1": "#d195ff", "accent2": "#095b9d", "name": "Python蛇撞色", "theme": "python", "text_color": "#ffffff"},
    "java_1": {"bg": "#05061a", "accent1": "#00ff00", "accent2": "#05c6FF", "name": "Java咖啡暗夜", "theme": "java"},
    "java_2": {"bg": "#f0f0f0", "accent1": "#05007f", "accent2": "#5c7F63", "name": "Java咖啡清新", "theme": "java", "text_color": "#1a1a1a"},
    "java_3": {"bg": "linear-gradient(135deg,#050580 0%,#05c6ff 100%)", "accent1": "#ffffff", "accent2": "#005cff", "name": "Java咖啡渐变", "theme": "java", "is_gradient": True},
    "java_4": {"bg": "#0005c6", "accent1": "#3a05ff", "accent2": "#005c63", "name": "Java咖啡撞色", "theme": "java", "text_color": "#ffffff"},
    "golang_1": {"bg": "#1e0013", "accent1": "#00ff00", "accent2": "#5ea0FF", "name": "Go地鼠暗夜", "theme": "golang"},
    "golang_2": {"bg": "#f0f0f0", "accent1": "#5e007f", "accent2": "#ea7F01", "name": "Go地鼠清新", "theme": "golang", "text_color": "#1a1a1a"},
    "golang_3": {"bg": "linear-gradient(135deg,#5e5e80 0%,#5ea0ff 100%)", "accent1": "#ffffff", "accent2": "#05eaff", "name": "Go地鼠渐变", "theme": "golang", "is_gradient": True},
    "golang_4": {"bg": "#005ea0", "accent1": "#135eff", "accent2": "#05ea01", "name": "Go地鼠撞色", "theme": "golang", "text_color": "#ffffff"},
    "rust_1": {"bg": "#000611", "accent1": "#00ff00", "accent2": "#a0c6FF", "name": "Rust螃蟹暗夜", "theme": "rust"},
    "rust_2": {"bg": "#f0f0f0", "accent1": "#20007f", "accent2": "#0c7F69", "name": "Rust螃蟹清新", "theme": "rust", "text_color": "#1a1a1a"},
    "rust_3": {"bg": "linear-gradient(135deg,#a0a080 0%,#a0c6ff 100%)", "accent1": "#ffffff", "accent2": "#0a0cff", "name": "Rust螃蟹渐变", "theme": "rust", "is_gradient": True},
    "rust_4": {"bg": "#00a0c6", "accent1": "#91a0ff", "accent2": "#0a0c69", "name": "Rust螃蟹撞色", "theme": "rust", "text_color": "#ffffff"},
    "typescript_1": {"bg": "#091c0b", "accent1": "#00ff00", "accent2": "#c91cFF", "name": "TS蓝标暗夜", "theme": "typescript"},
    "typescript_2": {"bg": "#f0f0f0", "accent1": "#49007f", "accent2": "#917F42", "name": "TS蓝标清新", "theme": "typescript", "text_color": "#1a1a1a"},
    "typescript_3": {"bg": "linear-gradient(135deg,#c9c980 0%,#c91cff 100%)", "accent1": "#ffffff", "accent2": "#0c91ff", "name": "TS蓝标渐变", "theme": "typescript", "is_gradient": True},
    "typescript_4": {"bg": "#00c91c", "accent1": "#2bc9ff", "accent2": "#0c91c2", "name": "TS蓝标撞色", "theme": "typescript", "text_color": "#ffffff"},
    "react_1": {"bg": "#000702", "accent1": "#00ff00", "accent2": "#8027FF", "name": "React原子暗夜", "theme": "react"},
    "react_2": {"bg": "#f0f0f0", "accent1": "#00007f", "accent2": "#027F7e", "name": "React原子清新", "theme": "react", "text_color": "#1a1a1a"},
    "react_3": {"bg": "linear-gradient(135deg,#808080 0%,#8027ff 100%)", "accent1": "#ffffff", "accent2": "#0802ff", "name": "React原子渐变", "theme": "react", "is_gradient": True},
    "react_4": {"bg": "#008027", "accent1": "#e280ff", "accent2": "#08027e", "name": "React原子撞色", "theme": "react", "text_color": "#ffffff"},
    "vue_1": {"bg": "#11100c", "accent1": "#00ff00", "accent2": "#7190FF", "name": "Vue绿叶暗夜", "theme": "vue"},
    "vue_2": {"bg": "#f0f0f0", "accent1": "#71007f", "accent2": "#197F04", "name": "Vue绿叶清新", "theme": "vue", "text_color": "#1a1a1a"},
    "vue_3": {"bg": "linear-gradient(135deg,#717180 0%,#7190ff 100%)", "accent1": "#ffffff", "accent2": "#0719ff", "name": "Vue绿叶渐变", "theme": "vue", "is_gradient": True},
    "vue_4": {"bg": "#007190", "accent1": "#4c71ff", "accent2": "#071904", "name": "Vue绿叶撞色", "theme": "vue", "text_color": "#ffffff"},
    "angular_1": {"bg": "#08181d", "accent1": "#00ff00", "accent2": "#48f8FF", "name": "Angular盾暗夜", "theme": "angular"},
    "angular_2": {"bg": "#f0f0f0", "accent1": "#48007f", "accent2": "#8f7F0d", "name": "Angular盾清新", "theme": "angular", "text_color": "#1a1a1a"},
    "angular_3": {"bg": "linear-gradient(135deg,#484880 0%,#48f8ff 100%)", "accent1": "#ffffff", "accent2": "#048fff", "name": "Angular盾渐变", "theme": "angular", "is_gradient": True},
    "angular_4": {"bg": "#0048f8", "accent1": "#dd48ff", "accent2": "#048f8d", "name": "Angular盾撞色", "theme": "angular", "text_color": "#ffffff"},
    "svelte_1": {"bg": "#180019", "accent1": "#00ff00", "accent2": "#3820FF", "name": "Svelte橙暗夜", "theme": "svelte"},
    "svelte_2": {"bg": "#f0f0f0", "accent1": "#38007f", "accent2": "#827F01", "name": "Svelte橙清新", "theme": "svelte", "text_color": "#1a1a1a"},
    "svelte_3": {"bg": "linear-gradient(135deg,#383880 0%,#3820ff 100%)", "accent1": "#ffffff", "accent2": "#0382ff", "name": "Svelte橙渐变", "theme": "svelte", "is_gradient": True},
    "svelte_4": {"bg": "#003820", "accent1": "#1938ff", "accent2": "#038201", "name": "Svelte橙撞色", "theme": "svelte", "text_color": "#ffffff"},
    "nodejs_1": {"bg": "#00091a", "accent1": "#00ff00", "accent2": "#a0a9FF", "name": "Node六边形暗夜", "theme": "nodejs"},
    "nodejs_2": {"bg": "#f0f0f0", "accent1": "#20007f", "accent2": "#0a7F17", "name": "Node六边形清新", "theme": "nodejs", "text_color": "#1a1a1a"},
    "nodejs_3": {"bg": "linear-gradient(135deg,#a0a080 0%,#a0a9ff 100%)", "accent1": "#ffffff", "accent2": "#0a0aff", "name": "Node六边形渐变", "theme": "nodejs", "is_gradient": True},
    "nodejs_4": {"bg": "#00a0a9", "accent1": "#7aa0ff", "accent2": "#0a0a97", "name": "Node六边形撞色", "theme": "nodejs", "text_color": "#ffffff"},
    "mysql_1": {"bg": "#1d0a1c", "accent1": "#00ff00", "accent2": "#dd4aFF", "name": "MySQL海豚暗夜", "theme": "mysql"},
    "mysql_2": {"bg": "#f0f0f0", "accent1": "#5d007f", "accent2": "#d47F2f", "name": "MySQL海豚清新", "theme": "mysql", "text_color": "#1a1a1a"},
    "mysql_3": {"bg": "linear-gradient(135deg,#dddd80 0%,#dd4aff 100%)", "accent1": "#ffffff", "accent2": "#0dd4ff", "name": "MySQL海豚渐变", "theme": "mysql", "is_gradient": True},
    "mysql_4": {"bg": "#00dd4a", "accent1": "#fcddff", "accent2": "#0dd4af", "name": "MySQL海豚撞色", "theme": "mysql", "text_color": "#ffffff"},
    "postgres_1": {"bg": "#1a1206", "accent1": "#00ff00", "accent2": "#ba12FF", "name": "Postgres象暗夜", "theme": "postgres"},
    "postgres_2": {"bg": "#f0f0f0", "accent1": "#3a007f", "accent2": "#a17F20", "name": "Postgres象清新", "theme": "postgres", "text_color": "#1a1a1a"},
    "postgres_3": {"bg": "linear-gradient(135deg,#baba80 0%,#ba12ff 100%)", "accent1": "#ffffff", "accent2": "#0ba1ff", "name": "Postgres象渐变", "theme": "postgres", "is_gradient": True},
    "postgres_4": {"bg": "#00ba12", "accent1": "#06baff", "accent2": "#0ba120", "name": "Postgres象撞色", "theme": "postgres", "text_color": "#ffffff"},
    "redis_1": {"bg": "#150317", "accent1": "#00ff00", "accent2": "#75e3FF", "name": "Redis立方暗夜", "theme": "redis"},
    "redis_2": {"bg": "#f0f0f0", "accent1": "#75007f", "accent2": "#5e7F3d", "name": "Redis立方清新", "theme": "redis", "text_color": "#1a1a1a"},
    "redis_3": {"bg": "linear-gradient(135deg,#757580 0%,#75e3ff 100%)", "accent1": "#ffffff", "accent2": "#075eff", "name": "Redis立方渐变", "theme": "redis", "is_gradient": True},
    "redis_4": {"bg": "#0075e3", "accent1": "#d775ff", "accent2": "#075e3d", "name": "Redis立方撞色", "theme": "redis", "text_color": "#ffffff"},
    "mongo_1": {"bg": "#120d1e", "accent1": "#00ff00", "accent2": "#b2cdFF", "name": "MongoDB叶暗夜", "theme": "mongo"},
    "mongo_2": {"bg": "#f0f0f0", "accent1": "#32007f", "accent2": "#2c7F53", "name": "MongoDB叶清新", "theme": "mongo", "text_color": "#1a1a1a"},
    "mongo_3": {"bg": "linear-gradient(135deg,#b2b280 0%,#b2cdff 100%)", "accent1": "#ffffff", "accent2": "#0b2cff", "name": "MongoDB叶渐变", "theme": "mongo", "is_gradient": True},
    "mongo_4": {"bg": "#00b2cd", "accent1": "#3eb2ff", "accent2": "#0b2cd3", "name": "MongoDB叶撞色", "theme": "mongo", "text_color": "#ffffff"},
    "sqlite_1": {"bg": "#1b1f0a", "accent1": "#00ff00", "accent2": "#7b9fFF", "name": "SQLite羽毛暗夜", "theme": "sqlite"},
    "sqlite_2": {"bg": "#f0f0f0", "accent1": "#7b007f", "accent2": "#b97F7a", "name": "SQLite羽毛清新", "theme": "sqlite", "text_color": "#1a1a1a"},
    "sqlite_3": {"bg": "linear-gradient(135deg,#7b7b80 0%,#7b9fff 100%)", "accent1": "#ffffff", "accent2": "#07b9ff", "name": "SQLite羽毛渐变", "theme": "sqlite", "is_gradient": True},
    "sqlite_4": {"bg": "#007b9f", "accent1": "#aa7bff", "accent2": "#07b9fa", "name": "SQLite羽毛撞色", "theme": "sqlite", "text_color": "#ffffff"},
    "elastic_1": {"bg": "#15050c", "accent1": "#00ff00", "accent2": "#15c5FF", "name": "ES搜索暗夜", "theme": "elastic"},
    "elastic_2": {"bg": "#f0f0f0", "accent1": "#15007f", "accent2": "#5c7F5a", "name": "ES搜索清新", "theme": "elastic", "text_color": "#1a1a1a"},
    "elastic_3": {"bg": "linear-gradient(135deg,#151580 0%,#15c5ff 100%)", "accent1": "#ffffff", "accent2": "#015cff", "name": "ES搜索渐变", "theme": "elastic", "is_gradient": True},
    "elastic_4": {"bg": "#0015c5", "accent1": "#ac15ff", "accent2": "#015c5a", "name": "ES搜索撞色", "theme": "elastic", "text_color": "#ffffff"},
    "docker_1": {"bg": "#1b1209", "accent1": "#00ff00", "accent2": "#fbd2FF", "name": "Docker鲸鱼暗夜", "theme": "docker"},
    "docker_2": {"bg": "#f0f0f0", "accent1": "#7b007f", "accent2": "#bd7F20", "name": "Docker鲸鱼清新", "theme": "docker", "text_color": "#1a1a1a"},
    "docker_3": {"bg": "linear-gradient(135deg,#fbfb80 0%,#fbd2ff 100%)", "accent1": "#ffffff", "accent2": "#0fbdff", "name": "Docker鲸鱼渐变", "theme": "docker", "is_gradient": True},
    "docker_4": {"bg": "#00fbd2", "accent1": "#09fbff", "accent2": "#0fbd20", "name": "Docker鲸鱼撞色", "theme": "docker", "text_color": "#ffffff"},
    "k8s_1": {"bg": "#120701", "accent1": "#00ff00", "accent2": "#3267FF", "name": "K8s舵轮暗夜", "theme": "k8s"},
    "k8s_2": {"bg": "#f0f0f0", "accent1": "#32007f", "accent2": "#267F74", "name": "K8s舵轮清新", "theme": "k8s", "text_color": "#1a1a1a"},
    "k8s_3": {"bg": "linear-gradient(135deg,#323280 0%,#3267ff 100%)", "accent1": "#ffffff", "accent2": "#0326ff", "name": "K8s舵轮渐变", "theme": "k8s", "is_gradient": True},
    "k8s_4": {"bg": "#003267", "accent1": "#4132ff", "accent2": "#032674", "name": "K8s舵轮撞色", "theme": "k8s", "text_color": "#ffffff"},
    "terraform_1": {"bg": "#1a1d16", "accent1": "#00ff00", "accent2": "#fa1dFF", "name": "Terraform暗夜", "theme": "terraform"},
    "terraform_2": {"bg": "#f0f0f0", "accent1": "#7a007f", "accent2": "#a17F51", "name": "Terraform清新", "theme": "terraform", "text_color": "#1a1a1a"},
    "terraform_3": {"bg": "linear-gradient(135deg,#fafa80 0%,#fa1dff 100%)", "accent1": "#ffffff", "accent2": "#0fa1ff", "name": "Terraform渐变", "theme": "terraform", "is_gradient": True},
    "terraform_4": {"bg": "#00fa1d", "accent1": "#16faff", "accent2": "#0fa1d1", "name": "Terraform撞色", "theme": "terraform", "text_color": "#ffffff"},
    "jenkins_1": {"bg": "#140a06", "accent1": "#00ff00", "accent2": "#f4aaFF", "name": "Jenkins暗夜", "theme": "jenkins"},
    "jenkins_2": {"bg": "#f0f0f0", "accent1": "#74007f", "accent2": "#4a7F22", "name": "Jenkins清新", "theme": "jenkins", "text_color": "#1a1a1a"},
    "jenkins_3": {"bg": "linear-gradient(135deg,#f4f480 0%,#f4aaff 100%)", "accent1": "#ffffff", "accent2": "#0f4aff", "name": "Jenkins渐变", "theme": "jenkins", "is_gradient": True},
    "jenkins_4": {"bg": "#00f4aa", "accent1": "#26f4ff", "accent2": "#0f4aa2", "name": "Jenkins撞色", "theme": "jenkins", "text_color": "#ffffff"},
    "github_1": {"bg": "#041418", "accent1": "#00ff00", "accent2": "#4494FF", "name": "GitHub猫暗夜", "theme": "github"},
    "github_2": {"bg": "#f0f0f0", "accent1": "#44007f", "accent2": "#497F4b", "name": "GitHub猫清新", "theme": "github", "text_color": "#1a1a1a"},
    "github_3": {"bg": "linear-gradient(135deg,#444480 0%,#4494ff 100%)", "accent1": "#ffffff", "accent2": "#0449ff", "name": "GitHub猫渐变", "theme": "github", "is_gradient": True},
    "github_4": {"bg": "#004494", "accent1": "#b844ff", "accent2": "#04494b", "name": "GitHub猫撞色", "theme": "github", "text_color": "#ffffff"},
    "gitlab_1": {"bg": "#110208", "accent1": "#00ff00", "accent2": "#91a2FF", "name": "GitLab狐暗夜", "theme": "gitlab"},
    "gitlab_2": {"bg": "#f0f0f0", "accent1": "#11007f", "accent2": "#1a7F2e", "name": "GitLab狐清新", "theme": "gitlab", "text_color": "#1a1a1a"},
    "gitlab_3": {"bg": "linear-gradient(135deg,#919180 0%,#91a2ff 100%)", "accent1": "#ffffff", "accent2": "#091aff", "name": "GitLab狐渐变", "theme": "gitlab", "is_gradient": True},
    "gitlab_4": {"bg": "#0091a2", "accent1": "#e891ff", "accent2": "#091a2e", "name": "GitLab狐撞色", "theme": "gitlab", "text_color": "#ffffff"},
    "prometheus_1": {"bg": "#180b07", "accent1": "#00ff00", "accent2": "#388bFF", "name": "Prometheus暗夜", "theme": "prometheus"},
    "prometheus_2": {"bg": "#f0f0f0", "accent1": "#38007f", "accent2": "#887F3c", "name": "Prometheus清新", "theme": "prometheus", "text_color": "#1a1a1a"},
    "prometheus_3": {"bg": "linear-gradient(135deg,#383880 0%,#388bff 100%)", "accent1": "#ffffff", "accent2": "#0388ff", "name": "Prometheus渐变", "theme": "prometheus", "is_gradient": True},
    "prometheus_4": {"bg": "#00388b", "accent1": "#c738ff", "accent2": "#0388bc", "name": "Prometheus撞色", "theme": "prometheus", "text_color": "#ffffff"},
    "grafana_1": {"bg": "#190e06", "accent1": "#00ff00", "accent2": "#b92eFF", "name": "Grafana暗夜", "theme": "grafana"},
    "grafana_2": {"bg": "#f0f0f0", "accent1": "#39007f", "accent2": "#927F68", "name": "Grafana清新", "theme": "grafana", "text_color": "#1a1a1a"},
    "grafana_3": {"bg": "linear-gradient(135deg,#b9b980 0%,#b92eff 100%)", "accent1": "#ffffff", "accent2": "#0b92ff", "name": "Grafana渐变", "theme": "grafana", "is_gradient": True},
    "grafana_4": {"bg": "#00b92e", "accent1": "#86b9ff", "accent2": "#0b92e8", "name": "Grafana撞色", "theme": "grafana", "text_color": "#ffffff"},
    "tensorflow_1": {"bg": "#061402", "accent1": "#00ff00", "accent2": "#0654FF", "name": "TF流暗夜", "theme": "tensorflow"},
    "tensorflow_2": {"bg": "#f0f0f0", "accent1": "#06007f", "accent2": "#657F40", "name": "TF流清新", "theme": "tensorflow", "text_color": "#1a1a1a"},
    "tensorflow_3": {"bg": "linear-gradient(135deg,#060680 0%,#0654ff 100%)", "accent1": "#ffffff", "accent2": "#0065ff", "name": "TF流渐变", "theme": "tensorflow", "is_gradient": True},
    "tensorflow_4": {"bg": "#000654", "accent1": "#0206ff", "accent2": "#006540", "name": "TF流撞色", "theme": "tensorflow", "text_color": "#ffffff"},
    "pytorch_1": {"bg": "#11051c", "accent1": "#00ff00", "accent2": "#71e5FF", "name": "PyTorch火暗夜", "theme": "pytorch"},
    "pytorch_2": {"bg": "#f0f0f0", "accent1": "#71007f", "accent2": "#1e7F5b", "name": "PyTorch火清新", "theme": "pytorch", "text_color": "#1a1a1a"},
    "pytorch_3": {"bg": "linear-gradient(135deg,#717180 0%,#71e5ff 100%)", "accent1": "#ffffff", "accent2": "#071eff", "name": "PyTorch火渐变", "theme": "pytorch", "is_gradient": True},
    "pytorch_4": {"bg": "#0071e5", "accent1": "#bc71ff", "accent2": "#071e5b", "name": "PyTorch火撞色", "theme": "pytorch", "text_color": "#ffffff"},
    "huggingface_1": {"bg": "#0f1d02", "accent1": "#00ff00", "accent2": "#afddFF", "name": "HF抱脸暗夜", "theme": "huggingface"},
    "huggingface_2": {"bg": "#f0f0f0", "accent1": "#2f007f", "accent2": "#fd7F5c", "name": "HF抱脸清新", "theme": "huggingface", "text_color": "#1a1a1a"},
    "huggingface_3": {"bg": "linear-gradient(135deg,#afaf80 0%,#afddff 100%)", "accent1": "#ffffff", "accent2": "#0afdff", "name": "HF抱脸渐变", "theme": "huggingface", "is_gradient": True},
    "huggingface_4": {"bg": "#00afdd", "accent1": "#c2afff", "accent2": "#0afddc", "name": "HF抱脸撞色", "theme": "huggingface", "text_color": "#ffffff"},
    "openai_1": {"bg": "#0b1200", "accent1": "#00ff00", "accent2": "#cb72FF", "name": "OpenAI暗夜", "theme": "openai"},
    "openai_2": {"bg": "#f0f0f0", "accent1": "#4b007f", "accent2": "#b77F22", "name": "OpenAI清新", "theme": "openai", "text_color": "#1a1a1a"},
    "openai_3": {"bg": "linear-gradient(135deg,#cbcb80 0%,#cb72ff 100%)", "accent1": "#ffffff", "accent2": "#0cb7ff", "name": "OpenAI渐变", "theme": "openai", "is_gradient": True},
    "openai_4": {"bg": "#00cb72", "accent1": "#20cbff", "accent2": "#0cb722", "name": "OpenAI撞色", "theme": "openai", "text_color": "#ffffff"},
    "langchain_1": {"bg": "#0d0f18", "accent1": "#00ff00", "accent2": "#cd8fFF", "name": "LangChain暗夜", "theme": "langchain"},
    "langchain_2": {"bg": "#f0f0f0", "accent1": "#4d007f", "accent2": "#d87F75", "name": "LangChain清新", "theme": "langchain", "text_color": "#1a1a1a"},
    "langchain_3": {"bg": "linear-gradient(135deg,#cdcd80 0%,#cd8fff 100%)", "accent1": "#ffffff", "accent2": "#0cd8ff", "name": "LangChain渐变", "theme": "langchain", "is_gradient": True},
    "langchain_4": {"bg": "#00cd8f", "accent1": "#58cdff", "accent2": "#0cd8f5", "name": "LangChain撞色", "theme": "langchain", "text_color": "#ffffff"},
    "ollama_1": {"bg": "#120211", "accent1": "#00ff00", "accent2": "#92e2FF", "name": "Ollama羊暗夜", "theme": "ollama"},
    "ollama_2": {"bg": "#f0f0f0", "accent1": "#12007f", "accent2": "#2e7F23", "name": "Ollama羊清新", "theme": "ollama", "text_color": "#1a1a1a"},
    "ollama_3": {"bg": "linear-gradient(135deg,#929280 0%,#92e2ff 100%)", "accent1": "#ffffff", "accent2": "#092eff", "name": "Ollama羊渐变", "theme": "ollama", "is_gradient": True},
    "ollama_4": {"bg": "#0092e2", "accent1": "#3192ff", "accent2": "#092e23", "name": "Ollama羊撞色", "theme": "ollama", "text_color": "#ffffff"},
    "stable_1": {"bg": "#180d0f", "accent1": "#00ff00", "accent2": "#58adFF", "name": "SD扩散暗夜", "theme": "stable"},
    "stable_2": {"bg": "#f0f0f0", "accent1": "#58007f", "accent2": "#8a7F58", "name": "SD扩散清新", "theme": "stable", "text_color": "#1a1a1a"},
    "stable_3": {"bg": "linear-gradient(135deg,#585880 0%,#58adff 100%)", "accent1": "#ffffff", "accent2": "#058aff", "name": "SD扩散渐变", "theme": "stable", "is_gradient": True},
    "stable_4": {"bg": "#0058ad", "accent1": "#8f58ff", "accent2": "#058ad8", "name": "SD扩散撞色", "theme": "stable", "text_color": "#ffffff"},
    "agent_1": {"bg": "#051713", "accent1": "#00ff00", "accent2": "#c5f7FF", "name": "AI Agent暗夜", "theme": "agent"},
    "agent_2": {"bg": "#f0f0f0", "accent1": "#45007f", "accent2": "#5f7F7d", "name": "AI Agent清新", "theme": "agent", "text_color": "#1a1a1a"},
    "agent_3": {"bg": "linear-gradient(135deg,#c5c580 0%,#c5f7ff 100%)", "accent1": "#ffffff", "accent2": "#0c5fff", "name": "AI Agent渐变", "theme": "agent", "is_gradient": True},
    "agent_4": {"bg": "#00c5f7", "accent1": "#d3c5ff", "accent2": "#0c5f7d", "name": "AI Agent撞色", "theme": "agent", "text_color": "#ffffff"},
    "rag_1": {"bg": "#0d1412", "accent1": "#00ff00", "accent2": "#6d34FF", "name": "RAG检索暗夜", "theme": "rag"},
    "rag_2": {"bg": "#f0f0f0", "accent1": "#6d007f", "accent2": "#d37F47", "name": "RAG检索清新", "theme": "rag", "text_color": "#1a1a1a"},
    "rag_3": {"bg": "linear-gradient(135deg,#6d6d80 0%,#6d34ff 100%)", "accent1": "#ffffff", "accent2": "#06d3ff", "name": "RAG检索渐变", "theme": "rag", "is_gradient": True},
    "rag_4": {"bg": "#006d34", "accent1": "#726dff", "accent2": "#06d347", "name": "RAG检索撞色", "theme": "rag", "text_color": "#ffffff"},
    "webpack_1": {"bg": "#191c03", "accent1": "#00ff00", "accent2": "#79fcFF", "name": "Webpack暗夜", "theme": "webpack"},
    "webpack_2": {"bg": "#f0f0f0", "accent1": "#79007f", "accent2": "#9f7F46", "name": "Webpack清新", "theme": "webpack", "text_color": "#1a1a1a"},
    "webpack_3": {"bg": "linear-gradient(135deg,#797980 0%,#79fcff 100%)", "accent1": "#ffffff", "accent2": "#079fff", "name": "Webpack渐变", "theme": "webpack", "is_gradient": True},
    "webpack_4": {"bg": "#0079fc", "accent1": "#6379ff", "accent2": "#079fc6", "name": "Webpack撞色", "theme": "webpack", "text_color": "#ffffff"},
    "vite_1": {"bg": "#0e1619", "accent1": "#00ff00", "accent2": "#eed6FF", "name": "Vite闪电暗夜", "theme": "vite"},
    "vite_2": {"bg": "#f0f0f0", "accent1": "#6e007f", "accent2": "#ed7F67", "name": "Vite闪电清新", "theme": "vite", "text_color": "#1a1a1a"},
    "vite_3": {"bg": "linear-gradient(135deg,#eeee80 0%,#eed6ff 100%)", "accent1": "#ffffff", "accent2": "#0eedff", "name": "Vite闪电渐变", "theme": "vite", "is_gradient": True},
    "vite_4": {"bg": "#00eed6", "accent1": "#79eeff", "accent2": "#0eed67", "name": "Vite闪电撞色", "theme": "vite", "text_color": "#ffffff"},
    "tailwind_1": {"bg": "#1a1513", "accent1": "#00ff00", "accent2": "#daf5FF", "name": "Tailwind暗夜", "theme": "tailwind"},
    "tailwind_2": {"bg": "#f0f0f0", "accent1": "#5a007f", "accent2": "#af7F59", "name": "Tailwind清新", "theme": "tailwind", "text_color": "#1a1a1a"},
    "tailwind_3": {"bg": "linear-gradient(135deg,#dada80 0%,#daf5ff 100%)", "accent1": "#ffffff", "accent2": "#0dafff", "name": "Tailwind渐变", "theme": "tailwind", "is_gradient": True},
    "tailwind_4": {"bg": "#00daf5", "accent1": "#93daff", "accent2": "#0daf59", "name": "Tailwind撞色", "theme": "tailwind", "text_color": "#ffffff"},
    "figma_1": {"bg": "#0c0a18", "accent1": "#00ff00", "accent2": "#ecaaFF", "name": "Figma暗夜", "theme": "figma"},
    "figma_2": {"bg": "#f0f0f0", "accent1": "#6c007f", "accent2": "#ca7F21", "name": "Figma清新", "theme": "figma", "text_color": "#1a1a1a"},
    "figma_3": {"bg": "linear-gradient(135deg,#ecec80 0%,#ecaaff 100%)", "accent1": "#ffffff", "accent2": "#0ecaff", "name": "Figma渐变", "theme": "figma", "is_gradient": True},
    "figma_4": {"bg": "#00ecaa", "accent1": "#18ecff", "accent2": "#0ecaa1", "name": "Figma撞色", "theme": "figma", "text_color": "#ffffff"},
    "graphql_1": {"bg": "#0d0d14", "accent1": "#00ff00", "accent2": "#cdadFF", "name": "GraphQL暗夜", "theme": "graphql"},
    "graphql_2": {"bg": "#f0f0f0", "accent1": "#4d007f", "accent2": "#da7F55", "name": "GraphQL清新", "theme": "graphql", "text_color": "#1a1a1a"},
    "graphql_3": {"bg": "linear-gradient(135deg,#cdcd80 0%,#cdadff 100%)", "accent1": "#ffffff", "accent2": "#0cdaff", "name": "GraphQL渐变", "theme": "graphql", "is_gradient": True},
    "graphql_4": {"bg": "#00cdad", "accent1": "#54cdff", "accent2": "#0cdad5", "name": "GraphQL撞色", "theme": "graphql", "text_color": "#ffffff"},
    "grpc_1": {"bg": "#021b07", "accent1": "#00ff00", "accent2": "#62dbFF", "name": "gRPC暗夜", "theme": "grpc"},
    "grpc_2": {"bg": "#f0f0f0", "accent1": "#62007f", "accent2": "#2d7F3c", "name": "gRPC清新", "theme": "grpc", "text_color": "#1a1a1a"},
    "grpc_3": {"bg": "linear-gradient(135deg,#626280 0%,#62dbff 100%)", "accent1": "#ffffff", "accent2": "#062dff", "name": "gRPC渐变", "theme": "grpc", "is_gradient": True},
    "grpc_4": {"bg": "#0062db", "accent1": "#c762ff", "accent2": "#062dbc", "name": "gRPC撞色", "theme": "grpc", "text_color": "#ffffff"},
    "kafka_1": {"bg": "#0f1913", "accent1": "#00ff00", "accent2": "#efb9FF", "name": "Kafka暗夜", "theme": "kafka"},
    "kafka_2": {"bg": "#f0f0f0", "accent1": "#6f007f", "accent2": "#fb7F19", "name": "Kafka清新", "theme": "kafka", "text_color": "#1a1a1a"},
    "kafka_3": {"bg": "linear-gradient(135deg,#efef80 0%,#efb9ff 100%)", "accent1": "#ffffff", "accent2": "#0efbff", "name": "Kafka渐变", "theme": "kafka", "is_gradient": True},
    "kafka_4": {"bg": "#00efb9", "accent1": "#93efff", "accent2": "#0efb99", "name": "Kafka撞色", "theme": "kafka", "text_color": "#ffffff"},
    "rabbit_1": {"bg": "#0b0e05", "accent1": "#00ff00", "accent2": "#eb4eFF", "name": "兔子暗夜", "theme": "rabbit"},
    "rabbit_2": {"bg": "#f0f0f0", "accent1": "#6b007f", "accent2": "#b47F6c", "name": "兔子清新", "theme": "rabbit", "text_color": "#1a1a1a"},
    "rabbit_3": {"bg": "linear-gradient(135deg,#ebeb80 0%,#eb4eff 100%)", "accent1": "#ffffff", "accent2": "#0eb4ff", "name": "兔子渐变", "theme": "rabbit", "is_gradient": True},
    "rabbit_4": {"bg": "#00eb4e", "accent1": "#c5ebff", "accent2": "#0eb4ec", "name": "兔子撞色", "theme": "rabbit", "text_color": "#ffffff"},
    "nginx_1": {"bg": "#190812", "accent1": "#00ff00", "accent2": "#b908FF", "name": "Nginx暗夜", "theme": "nginx"},
    "nginx_2": {"bg": "#f0f0f0", "accent1": "#39007f", "accent2": "#907F0b", "name": "Nginx清新", "theme": "nginx", "text_color": "#1a1a1a"},
    "nginx_3": {"bg": "linear-gradient(135deg,#b9b980 0%,#b908ff 100%)", "accent1": "#ffffff", "accent2": "#0b90ff", "name": "Nginx渐变", "theme": "nginx", "is_gradient": True},
    "nginx_4": {"bg": "#00b908", "accent1": "#b2b9ff", "accent2": "#0b908b", "name": "Nginx撞色", "theme": "nginx", "text_color": "#ffffff"},
    "spring_1": {"bg": "#1f0310", "accent1": "#00ff00", "accent2": "#5fa3FF", "name": "春暗夜", "theme": "spring"},
    "spring_2": {"bg": "#f0f0f0", "accent1": "#5f007f", "accent2": "#fa7F31", "name": "春清新", "theme": "spring", "text_color": "#1a1a1a"},
    "spring_3": {"bg": "linear-gradient(135deg,#5f5f80 0%,#5fa3ff 100%)", "accent1": "#ffffff", "accent2": "#05faff", "name": "春渐变", "theme": "spring", "is_gradient": True},
    "spring_4": {"bg": "#005fa3", "accent1": "#105fff", "accent2": "#05fa31", "name": "春撞色", "theme": "spring", "text_color": "#ffffff"},
    "ddd_1": {"bg": "#110f07", "accent1": "#00ff00", "accent2": "#318fFF", "name": "DDD分层暗夜", "theme": "ddd"},
    "ddd_2": {"bg": "#f0f0f0", "accent1": "#31007f", "accent2": "#187F74", "name": "DDD分层清新", "theme": "ddd", "text_color": "#1a1a1a"},
    "ddd_3": {"bg": "linear-gradient(135deg,#313180 0%,#318fff 100%)", "accent1": "#ffffff", "accent2": "#0318ff", "name": "DDD分层渐变", "theme": "ddd", "is_gradient": True},
    "ddd_4": {"bg": "#00318f", "accent1": "#4731ff", "accent2": "#0318f4", "name": "DDD分层撞色", "theme": "ddd", "text_color": "#ffffff"},
    "microsvc_1": {"bg": "#011405", "accent1": "#00ff00", "accent2": "#e194FF", "name": "微服务暗夜", "theme": "microsvc"},
    "microsvc_2": {"bg": "#f0f0f0", "accent1": "#61007f", "accent2": "#197F48", "name": "微服务清新", "theme": "microsvc", "text_color": "#1a1a1a"},
    "microsvc_3": {"bg": "linear-gradient(135deg,#e1e180 0%,#e194ff 100%)", "accent1": "#ffffff", "accent2": "#0e19ff", "name": "微服务渐变", "theme": "microsvc", "is_gradient": True},
    "microsvc_4": {"bg": "#00e194", "accent1": "#85e1ff", "accent2": "#0e1948", "name": "微服务撞色", "theme": "microsvc", "text_color": "#ffffff"},
    "serverless_1": {"bg": "#040203", "accent1": "#00ff00", "accent2": "#0482FF", "name": "无服务暗夜", "theme": "serverless"},
    "serverless_2": {"bg": "#f0f0f0", "accent1": "#04007f", "accent2": "#487F28", "name": "无服务清新", "theme": "serverless", "text_color": "#1a1a1a"},
    "serverless_3": {"bg": "linear-gradient(135deg,#040480 0%,#0482ff 100%)", "accent1": "#ffffff", "accent2": "#0048ff", "name": "无服务渐变", "theme": "serverless", "is_gradient": True},
    "serverless_4": {"bg": "#000482", "accent1": "#8304ff", "accent2": "#004828", "name": "无服务撞色", "theme": "serverless", "text_color": "#ffffff"},
    "security_1": {"bg": "#080d0e", "accent1": "#00ff00", "accent2": "#e82dFF", "name": "安全盾暗夜", "theme": "security"},
    "security_2": {"bg": "#f0f0f0", "accent1": "#68007f", "accent2": "#827F56", "name": "安全盾清新", "theme": "security", "text_color": "#1a1a1a"},
    "security_3": {"bg": "linear-gradient(135deg,#e8e880 0%,#e82dff 100%)", "accent1": "#ffffff", "accent2": "#0e82ff", "name": "安全盾渐变", "theme": "security", "is_gradient": True},
    "security_4": {"bg": "#00e82d", "accent1": "#6ee8ff", "accent2": "#0e82d6", "name": "安全盾撞色", "theme": "security", "text_color": "#ffffff"},
    "blockchain_1": {"bg": "#140c0b", "accent1": "#00ff00", "accent2": "#f46cFF", "name": "区块链暗夜", "theme": "blockchain"},
    "blockchain_2": {"bg": "#f0f0f0", "accent1": "#74007f", "accent2": "#467F48", "name": "区块链清新", "theme": "blockchain", "text_color": "#1a1a1a"},
    "blockchain_3": {"bg": "linear-gradient(135deg,#f4f480 0%,#f46cff 100%)", "accent1": "#ffffff", "accent2": "#0f46ff", "name": "区块链渐变", "theme": "blockchain", "is_gradient": True},
    "blockchain_4": {"bg": "#00f46c", "accent1": "#8bf4ff", "accent2": "#0f46c8", "name": "区块链撞色", "theme": "blockchain", "text_color": "#ffffff"},
    "web3_1": {"bg": "#080916", "accent1": "#00ff00", "accent2": "#c869FF", "name": "Web3暗夜", "theme": "web3"},
    "web3_2": {"bg": "#f0f0f0", "accent1": "#48007f", "accent2": "#867F1f", "name": "Web3清新", "theme": "web3", "text_color": "#1a1a1a"},
    "web3_3": {"bg": "linear-gradient(135deg,#c8c880 0%,#c869ff 100%)", "accent1": "#ffffff", "accent2": "#0c86ff", "name": "Web3渐变", "theme": "web3", "is_gradient": True},
    "web3_4": {"bg": "#00c869", "accent1": "#f6c8ff", "accent2": "#0c869f", "name": "Web3撞色", "theme": "web3", "text_color": "#ffffff"},
    "linux_1": {"bg": "#0f021a", "accent1": "#00ff00", "accent2": "#8f22FF", "name": "Linux企鹅暗夜", "theme": "linux"},
    "linux_2": {"bg": "#f0f0f0", "accent1": "#0f007f", "accent2": "#f27F21", "name": "Linux企鹅清新", "theme": "linux", "text_color": "#1a1a1a"},
    "linux_3": {"bg": "linear-gradient(135deg,#8f8f80 0%,#8f22ff 100%)", "accent1": "#ffffff", "accent2": "#08f2ff", "name": "Linux企鹅渐变", "theme": "linux", "is_gradient": True},
    "linux_4": {"bg": "#008f22", "accent1": "#1a8fff", "accent2": "#08f221", "name": "Linux企鹅撞色", "theme": "linux", "text_color": "#ffffff"},
    "terminal_1": {"bg": "#150102", "accent1": "#00ff00", "accent2": "#5501FF", "name": "终端暗夜", "theme": "terminal"},
    "terminal_2": {"bg": "#f0f0f0", "accent1": "#55007f", "accent2": "#507F1c", "name": "终端清新", "theme": "terminal", "text_color": "#1a1a1a"},
    "terminal_3": {"bg": "linear-gradient(135deg,#555580 0%,#5501ff 100%)", "accent1": "#ffffff", "accent2": "#0550ff", "name": "终端渐变", "theme": "terminal", "is_gradient": True},
    "terminal_4": {"bg": "#005501", "accent1": "#c255ff", "accent2": "#05501c", "name": "终端撞色", "theme": "terminal", "text_color": "#ffffff"},
    "vim_1": {"bg": "#1b0a17", "accent1": "#00ff00", "accent2": "#3b2aFF", "name": "Vim暗夜", "theme": "vim"},
    "vim_2": {"bg": "#f0f0f0", "accent1": "#3b007f", "accent2": "#b27F27", "name": "Vim清新", "theme": "vim", "text_color": "#1a1a1a"},
    "vim_3": {"bg": "linear-gradient(135deg,#3b3b80 0%,#3b2aff 100%)", "accent1": "#ffffff", "accent2": "#03b2ff", "name": "Vim渐变", "theme": "vim", "is_gradient": True},
    "vim_4": {"bg": "#003b2a", "accent1": "#773bff", "accent2": "#03b2a7", "name": "Vim撞色", "theme": "vim", "text_color": "#ffffff"},
    "vscode_1": {"bg": "#12040e", "accent1": "#00ff00", "accent2": "#32c4FF", "name": "VSCode暗夜", "theme": "vscode"},
    "vscode_2": {"bg": "#f0f0f0", "accent1": "#32007f", "accent2": "#2c7F42", "name": "VSCode清新", "theme": "vscode", "text_color": "#1a1a1a"},
    "vscode_3": {"bg": "linear-gradient(135deg,#323280 0%,#32c4ff 100%)", "accent1": "#ffffff", "accent2": "#032cff", "name": "VSCode渐变", "theme": "vscode", "is_gradient": True},
    "vscode_4": {"bg": "#0032c4", "accent1": "#2e32ff", "accent2": "#032c42", "name": "VSCode撞色", "theme": "vscode", "text_color": "#ffffff"},
    "ssh_1": {"bg": "#0c1e13", "accent1": "#00ff00", "accent2": "#6cfeFF", "name": "SSH密钥暗夜", "theme": "ssh"},
    "ssh_2": {"bg": "#f0f0f0", "accent1": "#6c007f", "accent2": "#cf7F6b", "name": "SSH密钥清新", "theme": "ssh", "text_color": "#1a1a1a"},
    "ssh_3": {"bg": "linear-gradient(135deg,#6c6c80 0%,#6cfeff 100%)", "accent1": "#ffffff", "accent2": "#06cfff", "name": "SSH密钥渐变", "theme": "ssh", "is_gradient": True},
    "ssh_4": {"bg": "#006cfe", "accent1": "#b36cff", "accent2": "#06cfeb", "name": "SSH密钥撞色", "theme": "ssh", "text_color": "#ffffff"},
    "cron_1": {"bg": "#080303", "accent1": "#00ff00", "accent2": "#4843FF", "name": "定时任务暗夜", "theme": "cron"},
    "cron_2": {"bg": "#f0f0f0", "accent1": "#48007f", "accent2": "#847F3e", "name": "定时任务清新", "theme": "cron", "text_color": "#1a1a1a"},
    "cron_3": {"bg": "linear-gradient(135deg,#484880 0%,#4843ff 100%)", "accent1": "#ffffff", "accent2": "#0484ff", "name": "定时任务渐变", "theme": "cron", "is_gradient": True},
    "cron_4": {"bg": "#004843", "accent1": "#e348ff", "accent2": "#04843e", "name": "定时任务撞色", "theme": "cron", "text_color": "#ffffff"},
    "regex_1": {"bg": "#1a1c18", "accent1": "#00ff00", "accent2": "#3a5cFF", "name": "正则暗夜", "theme": "regex"},
    "regex_2": {"bg": "#f0f0f0", "accent1": "#3a007f", "accent2": "#a57F4d", "name": "正则清新", "theme": "regex", "text_color": "#1a1a1a"},
    "regex_3": {"bg": "linear-gradient(135deg,#3a3a80 0%,#3a5cff 100%)", "accent1": "#ffffff", "accent2": "#03a5ff", "name": "正则渐变", "theme": "regex", "is_gradient": True},
    "regex_4": {"bg": "#003a5c", "accent1": "#d83aff", "accent2": "#03a5cd", "name": "正则撞色", "theme": "regex", "text_color": "#ffffff"},
    "restapi_1": {"bg": "#171715", "accent1": "#00ff00", "accent2": "#57d7FF", "name": "REST API暗夜", "theme": "restapi"},
    "restapi_2": {"bg": "#f0f0f0", "accent1": "#57007f", "accent2": "#7d7F7f", "name": "REST API清新", "theme": "restapi", "text_color": "#1a1a1a"},
    "restapi_3": {"bg": "linear-gradient(135deg,#575780 0%,#57d7ff 100%)", "accent1": "#ffffff", "accent2": "#057dff", "name": "REST API渐变", "theme": "restapi", "is_gradient": True},
    "restapi_4": {"bg": "#0057d7", "accent1": "#f557ff", "accent2": "#057d7f", "name": "REST API撞色", "theme": "restapi", "text_color": "#ffffff"},
    "json2_1": {"bg": "#030610", "accent1": "#00ff00", "accent2": "#c346FF", "name": "JSON暗夜", "theme": "json2"},
    "json2_2": {"bg": "#f0f0f0", "accent1": "#43007f", "accent2": "#347F61", "name": "JSON清新", "theme": "json2", "text_color": "#1a1a1a"},
    "json2_3": {"bg": "linear-gradient(135deg,#c3c380 0%,#c346ff 100%)", "accent1": "#ffffff", "accent2": "#0c34ff", "name": "JSON渐变", "theme": "json2", "is_gradient": True},
    "json2_4": {"bg": "#00c346", "accent1": "#10c3ff", "accent2": "#0c3461", "name": "JSON撞色", "theme": "json2", "text_color": "#ffffff"},
    "yaml_1": {"bg": "#0b1412", "accent1": "#00ff00", "accent2": "#eb54FF", "name": "YAML暗夜", "theme": "yaml"},
    "yaml_2": {"bg": "#f0f0f0", "accent1": "#6b007f", "accent2": "#b57F4b", "name": "YAML清新", "theme": "yaml", "text_color": "#1a1a1a"},
    "yaml_3": {"bg": "linear-gradient(135deg,#ebeb80 0%,#eb54ff 100%)", "accent1": "#ffffff", "accent2": "#0eb5ff", "name": "YAML渐变", "theme": "yaml", "is_gradient": True},
    "yaml_4": {"bg": "#00eb54", "accent1": "#b2ebff", "accent2": "#0eb54b", "name": "YAML撞色", "theme": "yaml", "text_color": "#ffffff"},
    "cicd_1": {"bg": "#0a030f", "accent1": "#00ff00", "accent2": "#aa63FF", "name": "CI/CD暗夜", "theme": "cicd"},
    "cicd_2": {"bg": "#f0f0f0", "accent1": "#2a007f", "accent2": "#a67F3a", "name": "CI/CD清新", "theme": "cicd", "text_color": "#1a1a1a"},
    "cicd_3": {"bg": "linear-gradient(135deg,#aaaa80 0%,#aa63ff 100%)", "accent1": "#ffffff", "accent2": "#0aa6ff", "name": "CI/CD渐变", "theme": "cicd", "is_gradient": True},
    "cicd_4": {"bg": "#00aa63", "accent1": "#afaaff", "accent2": "#0aa63a", "name": "CI/CD撞色", "theme": "cicd", "text_color": "#ffffff"},
    "dataviz_1": {"bg": "#011d18", "accent1": "#00ff00", "accent2": "#411dFF", "name": "数据可视化暗夜", "theme": "dataviz"},
    "dataviz_2": {"bg": "#f0f0f0", "accent1": "#41007f", "accent2": "#117F57", "name": "数据可视化清新", "theme": "dataviz", "text_color": "#1a1a1a"},
    "dataviz_3": {"bg": "linear-gradient(135deg,#414180 0%,#411dff 100%)", "accent1": "#ffffff", "accent2": "#0411ff", "name": "数据可视化渐变", "theme": "dataviz", "is_gradient": True},
    "dataviz_4": {"bg": "#00411d", "accent1": "#7841ff", "accent2": "#0411d7", "name": "数据可视化撞色", "theme": "dataviz", "text_color": "#ffffff"},
    "algo_1": {"bg": "#0e1b19", "accent1": "#00ff00", "accent2": "#2e9bFF", "name": "算法暗夜", "theme": "algo"},
    "algo_2": {"bg": "#f0f0f0", "accent1": "#2e007f", "accent2": "#e97F3b", "name": "算法清新", "theme": "algo", "text_color": "#1a1a1a"},
    "algo_3": {"bg": "linear-gradient(135deg,#2e2e80 0%,#2e9bff 100%)", "accent1": "#ffffff", "accent2": "#02e9ff", "name": "算法渐变", "theme": "algo", "is_gradient": True},
    "algo_4": {"bg": "#002e9b", "accent1": "#b92eff", "accent2": "#02e9bb", "name": "算法撞色", "theme": "algo", "text_color": "#ffffff"},
    "binary_1": {"bg": "#1a0510", "accent1": "#00ff00", "accent2": "#fa45FF", "name": "二进制暗夜", "theme": "binary"},
    "binary_2": {"bg": "#f0f0f0", "accent1": "#7a007f", "accent2": "#a47F55", "name": "二进制清新", "theme": "binary", "text_color": "#1a1a1a"},
    "binary_3": {"bg": "linear-gradient(135deg,#fafa80 0%,#fa45ff 100%)", "accent1": "#ffffff", "accent2": "#0fa4ff", "name": "二进制渐变", "theme": "binary", "is_gradient": True},
    "binary_4": {"bg": "#00fa45", "accent1": "#50faff", "accent2": "#0fa455", "name": "二进制撞色", "theme": "binary", "text_color": "#ffffff"},
    "neural_1": {"bg": "#01090f", "accent1": "#00ff00", "accent2": "#a109FF", "name": "神经网络暗夜", "theme": "neural"},
    "neural_2": {"bg": "#f0f0f0", "accent1": "#21007f", "accent2": "#107F16", "name": "神经网络清新", "theme": "neural", "text_color": "#1a1a1a"},
    "neural_3": {"bg": "linear-gradient(135deg,#a1a180 0%,#a109ff 100%)", "accent1": "#ffffff", "accent2": "#0a10ff", "name": "神经网络渐变", "theme": "neural", "is_gradient": True},
    "neural_4": {"bg": "#00a109", "accent1": "#6fa1ff", "accent2": "#0a1096", "name": "神经网络撞色", "theme": "neural", "text_color": "#ffffff"},
    "quantum2_1": {"bg": "#0f171d", "accent1": "#00ff00", "accent2": "#efd7FF", "name": "量子计算暗夜", "theme": "quantum2"},
    "quantum2_2": {"bg": "#f0f0f0", "accent1": "#6f007f", "accent2": "#fd7F71", "name": "量子计算清新", "theme": "quantum2", "text_color": "#1a1a1a"},
    "quantum2_3": {"bg": "linear-gradient(135deg,#efef80 0%,#efd7ff 100%)", "accent1": "#ffffff", "accent2": "#0efdff", "name": "量子计算渐变", "theme": "quantum2", "is_gradient": True},
    "quantum2_4": {"bg": "#00efd7", "accent1": "#1defff", "accent2": "#0efd71", "name": "量子计算撞色", "theme": "quantum2", "text_color": "#ffffff"},
    "edge_1": {"bg": "#001e1f", "accent1": "#00ff00", "accent2": "#607eFF", "name": "边缘计算暗夜", "theme": "edge"},
    "edge_2": {"bg": "#f0f0f0", "accent1": "#60007f", "accent2": "#077F63", "name": "边缘计算清新", "theme": "edge", "text_color": "#1a1a1a"},
    "edge_3": {"bg": "linear-gradient(135deg,#606080 0%,#607eff 100%)", "accent1": "#ffffff", "accent2": "#0607ff", "name": "边缘计算渐变", "theme": "edge", "is_gradient": True},
    "edge_4": {"bg": "#00607e", "accent1": "#3f60ff", "accent2": "#0607e3", "name": "边缘计算撞色", "theme": "edge", "text_color": "#ffffff"},
    "mesh2_1": {"bg": "#1e0812", "accent1": "#00ff00", "accent2": "#de08FF", "name": "服务网格暗夜", "theme": "mesh2"},
    "mesh2_2": {"bg": "#f0f0f0", "accent1": "#5e007f", "accent2": "#e07F0f", "name": "服务网格清新", "theme": "mesh2", "text_color": "#1a1a1a"},
    "mesh2_3": {"bg": "linear-gradient(135deg,#dede80 0%,#de08ff 100%)", "accent1": "#ffffff", "accent2": "#0de0ff", "name": "服务网格渐变", "theme": "mesh2", "is_gradient": True},
    "mesh2_4": {"bg": "#00de08", "accent1": "#f2deff", "accent2": "#0de08f", "name": "服务网格撞色", "theme": "mesh2", "text_color": "#ffffff"},
    "observ_1": {"bg": "#17190b", "accent1": "#00ff00", "accent2": "#9739FF", "name": "可观测暗夜", "theme": "observ"},
    "observ_2": {"bg": "#f0f0f0", "accent1": "#17007f", "accent2": "#737F1e", "name": "可观测清新", "theme": "observ", "text_color": "#1a1a1a"},
    "observ_3": {"bg": "linear-gradient(135deg,#979780 0%,#9739ff 100%)", "accent1": "#ffffff", "accent2": "#0973ff", "name": "可观测渐变", "theme": "observ", "is_gradient": True},
    "observ_4": {"bg": "#009739", "accent1": "#eb97ff", "accent2": "#09739e", "name": "可观测撞色", "theme": "observ", "text_color": "#ffffff"},
    "chaos_1": {"bg": "#061f12", "accent1": "#00ff00", "accent2": "#263fFF", "name": "混沌工程暗夜", "theme": "chaos"},
    "chaos_2": {"bg": "#f0f0f0", "accent1": "#26007f", "accent2": "#637F77", "name": "混沌工程清新", "theme": "chaos", "text_color": "#1a1a1a"},
    "chaos_3": {"bg": "linear-gradient(135deg,#262680 0%,#263fff 100%)", "accent1": "#ffffff", "accent2": "#0263ff", "name": "混沌工程渐变", "theme": "chaos", "is_gradient": True},
    "chaos_4": {"bg": "#00263f", "accent1": "#7226ff", "accent2": "#0263f7", "name": "混沌工程撞色", "theme": "chaos", "text_color": "#ffffff"},
    "gitops_1": {"bg": "#09151b", "accent1": "#00ff00", "accent2": "#49b5FF", "name": "GitOps暗夜", "theme": "gitops"},
    "gitops_2": {"bg": "#f0f0f0", "accent1": "#49007f", "accent2": "#9b7F57", "name": "GitOps清新", "theme": "gitops", "text_color": "#1a1a1a"},
    "gitops_3": {"bg": "linear-gradient(135deg,#494980 0%,#49b5ff 100%)", "accent1": "#ffffff", "accent2": "#049bff", "name": "GitOps渐变", "theme": "gitops", "is_gradient": True},
    "gitops_4": {"bg": "#0049b5", "accent1": "#7b49ff", "accent2": "#049b57", "name": "GitOps撞色", "theme": "gitops", "text_color": "#ffffff"},
    "saas_1": {"bg": "#1e1d14", "accent1": "#00ff00", "accent2": "#3ebdFF", "name": "SaaS暗夜", "theme": "saas"},
    "saas_2": {"bg": "#f0f0f0", "accent1": "#3e007f", "accent2": "#eb7F5f", "name": "SaaS清新", "theme": "saas", "text_color": "#1a1a1a"},
    "saas_3": {"bg": "linear-gradient(135deg,#3e3e80 0%,#3ebdff 100%)", "accent1": "#ffffff", "accent2": "#03ebff", "name": "SaaS渐变", "theme": "saas", "is_gradient": True},
    "saas_4": {"bg": "#003ebd", "accent1": "#f43eff", "accent2": "#03ebdf", "name": "SaaS撞色", "theme": "saas", "text_color": "#ffffff"},
    "paas_1": {"bg": "#071809", "accent1": "#00ff00", "accent2": "#07f8FF", "name": "PaaS暗夜", "theme": "paas"},
    "paas_2": {"bg": "#f0f0f0", "accent1": "#07007f", "accent2": "#7f7F0e", "name": "PaaS清新", "theme": "paas", "text_color": "#1a1a1a"},
    "paas_3": {"bg": "linear-gradient(135deg,#070780 0%,#07f8ff 100%)", "accent1": "#ffffff", "accent2": "#007fff", "name": "PaaS渐变", "theme": "paas", "is_gradient": True},
    "paas_4": {"bg": "#0007f8", "accent1": "#e907ff", "accent2": "#007f8e", "name": "PaaS撞色", "theme": "paas", "text_color": "#ffffff"},
    "lowcode_1": {"bg": "#1b040a", "accent1": "#00ff00", "accent2": "#1b24FF", "name": "低代码暗夜", "theme": "lowcode"},
    "lowcode_2": {"bg": "#f0f0f0", "accent1": "#1b007f", "accent2": "#b27F46", "name": "低代码清新", "theme": "lowcode", "text_color": "#1a1a1a"},
    "lowcode_3": {"bg": "linear-gradient(135deg,#1b1b80 0%,#1b24ff 100%)", "accent1": "#ffffff", "accent2": "#01b2ff", "name": "低代码渐变", "theme": "lowcode", "is_gradient": True},
    "lowcode_4": {"bg": "#001b24", "accent1": "#6a1bff", "accent2": "#01b246", "name": "低代码撞色", "theme": "lowcode", "text_color": "#ffffff"},
    "vibe_1": {"bg": "#150510", "accent1": "#00ff00", "accent2": "#9545FF", "name": "Vibe Coding暗夜", "theme": "vibe"},
    "vibe_2": {"bg": "#f0f0f0", "accent1": "#15007f", "accent2": "#547F53", "name": "Vibe Coding清新", "theme": "vibe", "text_color": "#1a1a1a"},
    "vibe_3": {"bg": "linear-gradient(135deg,#959580 0%,#9545ff 100%)", "accent1": "#ffffff", "accent2": "#0954ff", "name": "Vibe Coding渐变", "theme": "vibe", "is_gradient": True},
    "vibe_4": {"bg": "#009545", "accent1": "#3095ff", "accent2": "#095453", "name": "Vibe Coding撞色", "theme": "vibe", "text_color": "#ffffff"},
    "prompt_1": {"bg": "#171002", "accent1": "#00ff00", "accent2": "#1750FF", "name": "提示词暗夜", "theme": "prompt"},
    "prompt_2": {"bg": "#f0f0f0", "accent1": "#17007f", "accent2": "#757F0e", "name": "提示词清新", "theme": "prompt", "text_color": "#1a1a1a"},
    "prompt_3": {"bg": "linear-gradient(135deg,#171780 0%,#1750ff 100%)", "accent1": "#ffffff", "accent2": "#0175ff", "name": "提示词渐变", "theme": "prompt", "is_gradient": True},
    "prompt_4": {"bg": "#001750", "accent1": "#e217ff", "accent2": "#01750e", "name": "提示词撞色", "theme": "prompt", "text_color": "#ffffff"},
    "copilot_1": {"bg": "#190f10", "accent1": "#00ff00", "accent2": "#79efFF", "name": "Copilot暗夜", "theme": "copilot"},
    "copilot_2": {"bg": "#f0f0f0", "accent1": "#79007f", "accent2": "#9e7F79", "name": "Copilot清新", "theme": "copilot", "text_color": "#1a1a1a"},
    "copilot_3": {"bg": "linear-gradient(135deg,#797980 0%,#79efff 100%)", "accent1": "#ffffff", "accent2": "#079eff", "name": "Copilot渐变", "theme": "copilot", "is_gradient": True},
    "copilot_4": {"bg": "#0079ef", "accent1": "#9079ff", "accent2": "#079ef9", "name": "Copilot撞色", "theme": "copilot", "text_color": "#ffffff"},
    "embedding_1": {"bg": "#0c011d", "accent1": "#00ff00", "accent2": "#8c41FF", "name": "向量嵌入暗夜", "theme": "embedding"},
    "embedding_2": {"bg": "#f0f0f0", "accent1": "#0c007f", "accent2": "#c47F17", "name": "向量嵌入清新", "theme": "embedding", "text_color": "#1a1a1a"},
    "embedding_3": {"bg": "linear-gradient(135deg,#8c8c80 0%,#8c41ff 100%)", "accent1": "#ffffff", "accent2": "#08c4ff", "name": "向量嵌入渐变", "theme": "embedding", "is_gradient": True},
    "embedding_4": {"bg": "#008c41", "accent1": "#7d8cff", "accent2": "#08c417", "name": "向量嵌入撞色", "theme": "embedding", "text_color": "#ffffff"},
    "cubism_1": {"bg": "#1f0904", "accent1": "#00ff00", "accent2": "#dfe9FF", "name": "立体派暗夜", "theme": "cubism"},
    "cubism_2": {"bg": "#f0f0f0", "accent1": "#5f007f", "accent2": "#fe7F18", "name": "立体派清新", "theme": "cubism", "text_color": "#1a1a1a"},
    "cubism_3": {"bg": "linear-gradient(135deg,#dfdf80 0%,#dfe9ff 100%)", "accent1": "#ffffff", "accent2": "#0dfeff", "name": "立体派渐变", "theme": "cubism", "is_gradient": True},
    "cubism_4": {"bg": "#00dfe9", "accent1": "#84dfff", "accent2": "#0dfe98", "name": "立体派撞色", "theme": "cubism", "text_color": "#ffffff"},
    "surreal_1": {"bg": "#02030b", "accent1": "#00ff00", "accent2": "#2203FF", "name": "超现实暗夜", "theme": "surreal"},
    "surreal_2": {"bg": "#f0f0f0", "accent1": "#22007f", "accent2": "#207F3e", "name": "超现实清新", "theme": "surreal", "text_color": "#1a1a1a"},
    "surreal_3": {"bg": "linear-gradient(135deg,#222280 0%,#2203ff 100%)", "accent1": "#ffffff", "accent2": "#0220ff", "name": "超现实渐变", "theme": "surreal", "is_gradient": True},
    "surreal_4": {"bg": "#002203", "accent1": "#eb22ff", "accent2": "#02203e", "name": "超现实撞色", "theme": "surreal", "text_color": "#ffffff"},
    "impression_1": {"bg": "#0c0d10", "accent1": "#00ff00", "accent2": "#8c2dFF", "name": "印象派暗夜", "theme": "impression"},
    "impression_2": {"bg": "#f0f0f0", "accent1": "#0c007f", "accent2": "#c27F57", "name": "印象派清新", "theme": "impression", "text_color": "#1a1a1a"},
    "impression_3": {"bg": "linear-gradient(135deg,#8c8c80 0%,#8c2dff 100%)", "accent1": "#ffffff", "accent2": "#08c2ff", "name": "印象派渐变", "theme": "impression", "is_gradient": True},
    "impression_4": {"bg": "#008c2d", "accent1": "#708cff", "accent2": "#08c2d7", "name": "印象派撞色", "theme": "impression", "text_color": "#ffffff"},
    "expression_1": {"bg": "#1c0315", "accent1": "#00ff00", "accent2": "#1ca3FF", "name": "表现派暗夜", "theme": "expression"},
    "expression_2": {"bg": "#f0f0f0", "accent1": "#1c007f", "accent2": "#ca7F3b", "name": "表现派清新", "theme": "expression", "text_color": "#1a1a1a"},
    "expression_3": {"bg": "linear-gradient(135deg,#1c1c80 0%,#1ca3ff 100%)", "accent1": "#ffffff", "accent2": "#01caff", "name": "表现派渐变", "theme": "expression", "is_gradient": True},
    "expression_4": {"bg": "#001ca3", "accent1": "#b51cff", "accent2": "#01ca3b", "name": "表现派撞色", "theme": "expression", "text_color": "#ffffff"},
    "fauvism_1": {"bg": "#1a0614", "accent1": "#00ff00", "accent2": "#fa06FF", "name": "野兽派暗夜", "theme": "fauvism"},
    "fauvism_2": {"bg": "#f0f0f0", "accent1": "#7a007f", "accent2": "#a07F6f", "name": "野兽派清新", "theme": "fauvism", "text_color": "#1a1a1a"},
    "fauvism_3": {"bg": "linear-gradient(135deg,#fafa80 0%,#fa06ff 100%)", "accent1": "#ffffff", "accent2": "#0fa0ff", "name": "野兽派渐变", "theme": "fauvism", "is_gradient": True},
    "fauvism_4": {"bg": "#00fa06", "accent1": "#f4faff", "accent2": "#0fa06f", "name": "野兽派撞色", "theme": "fauvism", "text_color": "#ffffff"},
    "dada_1": {"bg": "#030411", "accent1": "#00ff00", "accent2": "#4364FF", "name": "达达主义暗夜", "theme": "dada"},
    "dada_2": {"bg": "#f0f0f0", "accent1": "#43007f", "accent2": "#367F47", "name": "达达主义清新", "theme": "dada", "text_color": "#1a1a1a"},
    "dada_3": {"bg": "linear-gradient(135deg,#434380 0%,#4364ff 100%)", "accent1": "#ffffff", "accent2": "#0436ff", "name": "达达主义渐变", "theme": "dada", "is_gradient": True},
    "dada_4": {"bg": "#004364", "accent1": "#7143ff", "accent2": "#043647", "name": "达达主义撞色", "theme": "dada", "text_color": "#ffffff"},
    "construct_1": {"bg": "#081816", "accent1": "#00ff00", "accent2": "#08b8FF", "name": "构成主义暗夜", "theme": "construct"},
    "construct_2": {"bg": "#f0f0f0", "accent1": "#08007f", "accent2": "#8b7F07", "name": "构成主义清新", "theme": "construct", "text_color": "#1a1a1a"},
    "construct_3": {"bg": "linear-gradient(135deg,#080880 0%,#08b8ff 100%)", "accent1": "#ffffff", "accent2": "#008bff", "name": "构成主义渐变", "theme": "construct", "is_gradient": True},
    "construct_4": {"bg": "#0008b8", "accent1": "#7608ff", "accent2": "#008b87", "name": "构成主义撞色", "theme": "construct", "text_color": "#ffffff"},
    "destijl_1": {"bg": "#100b12", "accent1": "#00ff00", "accent2": "#906bFF", "name": "风格派暗夜", "theme": "destijl"},
    "destijl_2": {"bg": "#f0f0f0", "accent1": "#10007f", "accent2": "#067F3b", "name": "风格派清新", "theme": "destijl", "text_color": "#1a1a1a"},
    "destijl_3": {"bg": "linear-gradient(135deg,#909080 0%,#906bff 100%)", "accent1": "#ffffff", "accent2": "#0906ff", "name": "风格派渐变", "theme": "destijl", "is_gradient": True},
    "destijl_4": {"bg": "#00906b", "accent1": "#b290ff", "accent2": "#0906bb", "name": "风格派撞色", "theme": "destijl", "text_color": "#ffffff"},
    "bauhaus_1": {"bg": "#100c12", "accent1": "#00ff00", "accent2": "#904cFF", "name": "包豪斯暗夜", "theme": "bauhaus"},
    "bauhaus_2": {"bg": "#f0f0f0", "accent1": "#10007f", "accent2": "#047F49", "name": "包豪斯清新", "theme": "bauhaus", "text_color": "#1a1a1a"},
    "bauhaus_3": {"bg": "linear-gradient(135deg,#909080 0%,#904cff 100%)", "accent1": "#ffffff", "accent2": "#0904ff", "name": "包豪斯渐变", "theme": "bauhaus", "is_gradient": True},
    "bauhaus_4": {"bg": "#00904c", "accent1": "#9290ff", "accent2": "#0904c9", "name": "包豪斯撞色", "theme": "bauhaus", "text_color": "#ffffff"},
    "artnouveau_1": {"bg": "#0a120d", "accent1": "#00ff00", "accent2": "#0ab2FF", "name": "新艺术暗夜", "theme": "artnouveau"},
    "artnouveau_2": {"bg": "#f0f0f0", "accent1": "#0a007f", "accent2": "#ab7F2e", "name": "新艺术清新", "theme": "artnouveau", "text_color": "#1a1a1a"},
    "artnouveau_3": {"bg": "linear-gradient(135deg,#0a0a80 0%,#0ab2ff 100%)", "accent1": "#ffffff", "accent2": "#00abff", "name": "新艺术渐变", "theme": "artnouveau", "is_gradient": True},
    "artnouveau_4": {"bg": "#000ab2", "accent1": "#ed0aff", "accent2": "#00ab2e", "name": "新艺术撞色", "theme": "artnouveau", "text_color": "#ffffff"},
    "macro_1": {"bg": "#1c151b", "accent1": "#00ff00", "accent2": "#3c15FF", "name": "微距暗夜", "theme": "macro"},
    "macro_2": {"bg": "#f0f0f0", "accent1": "#3c007f", "accent2": "#c17F59", "name": "微距清新", "theme": "macro", "text_color": "#1a1a1a"},
    "macro_3": {"bg": "linear-gradient(135deg,#3c3c80 0%,#3c15ff 100%)", "accent1": "#ffffff", "accent2": "#03c1ff", "name": "微距渐变", "theme": "macro", "is_gradient": True},
    "macro_4": {"bg": "#003c15", "accent1": "#9b3cff", "accent2": "#03c159", "name": "微距撞色", "theme": "macro", "text_color": "#ffffff"},
    "longexp_1": {"bg": "#161815", "accent1": "#00ff00", "accent2": "#b6b8FF", "name": "长曝光暗夜", "theme": "longexp"},
    "longexp_2": {"bg": "#f0f0f0", "accent1": "#36007f", "accent2": "#6b7F0b", "name": "长曝光清新", "theme": "longexp", "text_color": "#1a1a1a"},
    "longexp_3": {"bg": "linear-gradient(135deg,#b6b680 0%,#b6b8ff 100%)", "accent1": "#ffffff", "accent2": "#0b6bff", "name": "长曝光渐变", "theme": "longexp", "is_gradient": True},
    "longexp_4": {"bg": "#00b6b8", "accent1": "#b5b6ff", "accent2": "#0b6b8b", "name": "长曝光撞色", "theme": "longexp", "text_color": "#ffffff"},
    "tiltshift_1": {"bg": "#020315", "accent1": "#00ff00", "accent2": "#4263FF", "name": "移轴暗夜", "theme": "tiltshift"},
    "tiltshift_2": {"bg": "#f0f0f0", "accent1": "#42007f", "accent2": "#267F33", "name": "移轴清新", "theme": "tiltshift", "text_color": "#1a1a1a"},
    "tiltshift_3": {"bg": "linear-gradient(135deg,#424280 0%,#4263ff 100%)", "accent1": "#ffffff", "accent2": "#0426ff", "name": "移轴渐变", "theme": "tiltshift", "is_gradient": True},
    "tiltshift_4": {"bg": "#004263", "accent1": "#3542ff", "accent2": "#042633", "name": "移轴撞色", "theme": "tiltshift", "text_color": "#ffffff"},
    "doubleexp_1": {"bg": "#1d0b14", "accent1": "#00ff00", "accent2": "#ddcbFF", "name": "双重曝光暗夜", "theme": "doubleexp"},
    "doubleexp_2": {"bg": "#f0f0f0", "accent1": "#5d007f", "accent2": "#dc7F39", "name": "双重曝光清新", "theme": "doubleexp", "text_color": "#1a1a1a"},
    "doubleexp_3": {"bg": "linear-gradient(135deg,#dddd80 0%,#ddcbff 100%)", "accent1": "#ffffff", "accent2": "#0ddcff", "name": "双重曝光渐变", "theme": "doubleexp", "is_gradient": True},
    "doubleexp_4": {"bg": "#00ddcb", "accent1": "#94ddff", "accent2": "#0ddcb9", "name": "双重曝光撞色", "theme": "doubleexp", "text_color": "#ffffff"},
    "infrared_1": {"bg": "#0c0d02", "accent1": "#00ff00", "accent2": "#cc0dFF", "name": "红外暗夜", "theme": "infrared"},
    "infrared_2": {"bg": "#f0f0f0", "accent1": "#4c007f", "accent2": "#c07F5e", "name": "红外清新", "theme": "infrared", "text_color": "#1a1a1a"},
    "infrared_3": {"bg": "linear-gradient(135deg,#cccc80 0%,#cc0dff 100%)", "accent1": "#ffffff", "accent2": "#0cc0ff", "name": "红外渐变", "theme": "infrared", "is_gradient": True},
    "infrared_4": {"bg": "#00cc0d", "accent1": "#e2ccff", "accent2": "#0cc0de", "name": "红外撞色", "theme": "infrared", "text_color": "#ffffff"},
    "cyberfilm_1": {"bg": "#1b0404", "accent1": "#00ff00", "accent2": "#7b84FF", "name": "赛博电影暗夜", "theme": "cyberfilm"},
    "cyberfilm_2": {"bg": "#f0f0f0", "accent1": "#7b007f", "accent2": "#b87F4c", "name": "赛博电影清新", "theme": "cyberfilm", "text_color": "#1a1a1a"},
    "cyberfilm_3": {"bg": "linear-gradient(135deg,#7b7b80 0%,#7b84ff 100%)", "accent1": "#ffffff", "accent2": "#07b8ff", "name": "赛博电影渐变", "theme": "cyberfilm", "is_gradient": True},
    "cyberfilm_4": {"bg": "#007b84", "accent1": "#c47bff", "accent2": "#07b84c", "name": "赛博电影撞色", "theme": "cyberfilm", "text_color": "#ffffff"},
    "wuxia_1": {"bg": "#0d0903", "accent1": "#00ff00", "accent2": "#2d49FF", "name": "武侠暗夜", "theme": "wuxia"},
    "wuxia_2": {"bg": "#f0f0f0", "accent1": "#2d007f", "accent2": "#d47F1a", "name": "武侠清新", "theme": "wuxia", "text_color": "#1a1a1a"},
    "wuxia_3": {"bg": "linear-gradient(135deg,#2d2d80 0%,#2d49ff 100%)", "accent1": "#ffffff", "accent2": "#02d4ff", "name": "武侠渐变", "theme": "wuxia", "is_gradient": True},
    "wuxia_4": {"bg": "#002d49", "accent1": "#a32dff", "accent2": "#02d49a", "name": "武侠撞色", "theme": "wuxia", "text_color": "#ffffff"},
    "scifi_1": {"bg": "#1d030f", "accent1": "#00ff00", "accent2": "#9d03FF", "name": "科幻暗夜", "theme": "scifi"},
    "scifi_2": {"bg": "#f0f0f0", "accent1": "#1d007f", "accent2": "#d07F32", "name": "科幻清新", "theme": "scifi", "text_color": "#1a1a1a"},
    "scifi_3": {"bg": "linear-gradient(135deg,#9d9d80 0%,#9d03ff 100%)", "accent1": "#ffffff", "accent2": "#09d0ff", "name": "科幻渐变", "theme": "scifi", "is_gradient": True},
    "scifi_4": {"bg": "#009d03", "accent1": "#2f9dff", "accent2": "#09d032", "name": "科幻撞色", "theme": "scifi", "text_color": "#ffffff"},
    "horror_1": {"bg": "#091c0b", "accent1": "#00ff00", "accent2": "#693cFF", "name": "恐怖暗夜", "theme": "horror"},
    "horror_2": {"bg": "#f0f0f0", "accent1": "#69007f", "accent2": "#937F46", "name": "恐怖清新", "theme": "horror", "text_color": "#1a1a1a"},
    "horror_3": {"bg": "linear-gradient(135deg,#696980 0%,#693cff 100%)", "accent1": "#ffffff", "accent2": "#0693ff", "name": "恐怖渐变", "theme": "horror", "is_gradient": True},
    "horror_4": {"bg": "#00693c", "accent1": "#6b69ff", "accent2": "#0693c6", "name": "恐怖撞色", "theme": "horror", "text_color": "#ffffff"},
    "western_1": {"bg": "#15121d", "accent1": "#00ff00", "accent2": "#75d2FF", "name": "西部暗夜", "theme": "western"},
    "western_2": {"bg": "#f0f0f0", "accent1": "#75007f", "accent2": "#5d7F29", "name": "西部清新", "theme": "western", "text_color": "#1a1a1a"},
    "western_3": {"bg": "linear-gradient(135deg,#757580 0%,#75d2ff 100%)", "accent1": "#ffffff", "accent2": "#075dff", "name": "西部渐变", "theme": "western", "is_gradient": True},
    "western_4": {"bg": "#0075d2", "accent1": "#9d75ff", "accent2": "#075d29", "name": "西部撞色", "theme": "western", "text_color": "#ffffff"},
    "spy_1": {"bg": "#140219", "accent1": "#00ff00", "accent2": "#9462FF", "name": "谍战暗夜", "theme": "spy"},
    "spy_2": {"bg": "#f0f0f0", "accent1": "#14007f", "accent2": "#467F23", "name": "谍战清新", "theme": "spy", "text_color": "#1a1a1a"},
    "spy_3": {"bg": "linear-gradient(135deg,#949480 0%,#9462ff 100%)", "accent1": "#ffffff", "accent2": "#0946ff", "name": "谍战渐变", "theme": "spy", "is_gradient": True},
    "spy_4": {"bg": "#009462", "accent1": "#3994ff", "accent2": "#094623", "name": "谍战撞色", "theme": "spy", "text_color": "#ffffff"},
    "rock_1": {"bg": "#0a090d", "accent1": "#00ff00", "accent2": "#2a69FF", "name": "摇滚暗夜", "theme": "rock"},
    "rock_2": {"bg": "#f0f0f0", "accent1": "#2a007f", "accent2": "#a67F10", "name": "摇滚清新", "theme": "rock", "text_color": "#1a1a1a"},
    "rock_3": {"bg": "linear-gradient(135deg,#2a2a80 0%,#2a69ff 100%)", "accent1": "#ffffff", "accent2": "#02a6ff", "name": "摇滚渐变", "theme": "rock", "is_gradient": True},
    "rock_4": {"bg": "#002a69", "accent1": "#0d2aff", "accent2": "#02a690", "name": "摇滚撞色", "theme": "rock", "text_color": "#ffffff"},
    "hiphop_1": {"bg": "#091f07", "accent1": "#00ff00", "accent2": "#891fFF", "name": "嘻哈暗夜", "theme": "hiphop"},
    "hiphop_2": {"bg": "#f0f0f0", "accent1": "#09007f", "accent2": "#917F78", "name": "嘻哈清新", "theme": "hiphop", "text_color": "#1a1a1a"},
    "hiphop_3": {"bg": "linear-gradient(135deg,#898980 0%,#891fff 100%)", "accent1": "#ffffff", "accent2": "#0891ff", "name": "嘻哈渐变", "theme": "hiphop", "is_gradient": True},
    "hiphop_4": {"bg": "#00891f", "accent1": "#8789ff", "accent2": "#0891f8", "name": "嘻哈撞色", "theme": "hiphop", "text_color": "#ffffff"},
    "jazz_1": {"bg": "#161408", "accent1": "#00ff00", "accent2": "#96d4FF", "name": "爵士暗夜", "theme": "jazz"},
    "jazz_2": {"bg": "#f0f0f0", "accent1": "#16007f", "accent2": "#6d7F44", "name": "爵士清新", "theme": "jazz", "text_color": "#1a1a1a"},
    "jazz_3": {"bg": "linear-gradient(135deg,#969680 0%,#96d4ff 100%)", "accent1": "#ffffff", "accent2": "#096dff", "name": "爵士渐变", "theme": "jazz", "is_gradient": True},
    "jazz_4": {"bg": "#0096d4", "accent1": "#4896ff", "accent2": "#096d44", "name": "爵士撞色", "theme": "jazz", "text_color": "#ffffff"},
    "edm_1": {"bg": "#131310", "accent1": "#00ff00", "accent2": "#93b3FF", "name": "电音暗夜", "theme": "edm"},
    "edm_2": {"bg": "#f0f0f0", "accent1": "#13007f", "accent2": "#3b7F3f", "name": "电音清新", "theme": "edm", "text_color": "#1a1a1a"},
    "edm_3": {"bg": "linear-gradient(135deg,#939380 0%,#93b3ff 100%)", "accent1": "#ffffff", "accent2": "#093bff", "name": "电音渐变", "theme": "edm", "is_gradient": True},
    "edm_4": {"bg": "#0093b3", "accent1": "#f093ff", "accent2": "#093b3f", "name": "电音撞色", "theme": "edm", "text_color": "#ffffff"},
    "punk_1": {"bg": "#0b041e", "accent1": "#00ff00", "accent2": "#8b44FF", "name": "朋克暗夜", "theme": "punk"},
    "punk_2": {"bg": "#f0f0f0", "accent1": "#0b007f", "accent2": "#b47F43", "name": "朋克清新", "theme": "punk", "text_color": "#1a1a1a"},
    "punk_3": {"bg": "linear-gradient(135deg,#8b8b80 0%,#8b44ff 100%)", "accent1": "#ffffff", "accent2": "#08b4ff", "name": "朋克渐变", "theme": "punk", "is_gradient": True},
    "punk_4": {"bg": "#008b44", "accent1": "#3e8bff", "accent2": "#08b443", "name": "朋克撞色", "theme": "punk", "text_color": "#ffffff"},
    "metal_1": {"bg": "#0e000e", "accent1": "#00ff00", "accent2": "#8ee0FF", "name": "金属暗夜", "theme": "metal"},
    "metal_2": {"bg": "#f0f0f0", "accent1": "#0e007f", "accent2": "#ee7F08", "name": "金属清新", "theme": "metal", "text_color": "#1a1a1a"},
    "metal_3": {"bg": "linear-gradient(135deg,#8e8e80 0%,#8ee0ff 100%)", "accent1": "#ffffff", "accent2": "#08eeff", "name": "金属渐变", "theme": "metal", "is_gradient": True},
    "metal_4": {"bg": "#008ee0", "accent1": "#8e8eff", "accent2": "#08ee08", "name": "金属撞色", "theme": "metal", "text_color": "#ffffff"},
    "blues_1": {"bg": "#011114", "accent1": "#00ff00", "accent2": "#0171FF", "name": "蓝调暗夜", "theme": "blues"},
    "blues_2": {"bg": "#f0f0f0", "accent1": "#01007f", "accent2": "#177F11", "name": "蓝调清新", "theme": "blues", "text_color": "#1a1a1a"},
    "blues_3": {"bg": "linear-gradient(135deg,#010180 0%,#0171ff 100%)", "accent1": "#ffffff", "accent2": "#0017ff", "name": "蓝调渐变", "theme": "blues", "is_gradient": True},
    "blues_4": {"bg": "#000171", "accent1": "#1401ff", "accent2": "#001711", "name": "蓝调撞色", "theme": "blues", "text_color": "#ffffff"},
    "reggae_1": {"bg": "#1c0215", "accent1": "#00ff00", "accent2": "#dc82FF", "name": "雷鬼暗夜", "theme": "reggae"},
    "reggae_2": {"bg": "#f0f0f0", "accent1": "#5c007f", "accent2": "#c87F2b", "name": "雷鬼清新", "theme": "reggae", "text_color": "#1a1a1a"},
    "reggae_3": {"bg": "linear-gradient(135deg,#dcdc80 0%,#dc82ff 100%)", "accent1": "#ffffff", "accent2": "#0dc8ff", "name": "雷鬼渐变", "theme": "reggae", "is_gradient": True},
    "reggae_4": {"bg": "#00dc82", "accent1": "#b5dcff", "accent2": "#0dc82b", "name": "雷鬼撞色", "theme": "reggae", "text_color": "#ffffff"},
    "deco_1": {"bg": "#081501", "accent1": "#00ff00", "accent2": "#c815FF", "name": "装饰艺术暗夜", "theme": "deco"},
    "deco_2": {"bg": "#f0f0f0", "accent1": "#48007f", "accent2": "#817F58", "name": "装饰艺术清新", "theme": "deco", "text_color": "#1a1a1a"},
    "deco_3": {"bg": "linear-gradient(135deg,#c8c880 0%,#c815ff 100%)", "accent1": "#ffffff", "accent2": "#0c81ff", "name": "装饰艺术渐变", "theme": "deco", "is_gradient": True},
    "deco_4": {"bg": "#00c815", "accent1": "#81c8ff", "accent2": "#0c8158", "name": "装饰艺术撞色", "theme": "deco", "text_color": "#ffffff"},
    "brutal2_1": {"bg": "#1d0710", "accent1": "#00ff00", "accent2": "#1d07FF", "name": "粗野建筑暗夜", "theme": "brutal2"},
    "brutal2_2": {"bg": "#f0f0f0", "accent1": "#1d007f", "accent2": "#d07F71", "name": "粗野建筑清新", "theme": "brutal2", "text_color": "#1a1a1a"},
    "brutal2_3": {"bg": "linear-gradient(135deg,#1d1d80 0%,#1d07ff 100%)", "accent1": "#ffffff", "accent2": "#01d0ff", "name": "粗野建筑渐变", "theme": "brutal2", "is_gradient": True},
    "brutal2_4": {"bg": "#001d07", "accent1": "#101dff", "accent2": "#01d071", "name": "粗野建筑撞色", "theme": "brutal2", "text_color": "#ffffff"},
    "gothic2_1": {"bg": "#020506", "accent1": "#00ff00", "accent2": "#4265FF", "name": "哥特建筑暗夜", "theme": "gothic2"},
    "gothic2_2": {"bg": "#f0f0f0", "accent1": "#42007f", "accent2": "#267F5c", "name": "哥特建筑清新", "theme": "gothic2", "text_color": "#1a1a1a"},
    "gothic2_3": {"bg": "linear-gradient(135deg,#424280 0%,#4265ff 100%)", "accent1": "#ffffff", "accent2": "#0426ff", "name": "哥特建筑渐变", "theme": "gothic2", "is_gradient": True},
    "gothic2_4": {"bg": "#004265", "accent1": "#c642ff", "accent2": "#04265c", "name": "哥特建筑撞色", "theme": "gothic2", "text_color": "#ffffff"},
    "modernist_1": {"bg": "#1c1d11", "accent1": "#00ff00", "accent2": "#5c5dFF", "name": "现代主义暗夜", "theme": "modernist"},
    "modernist_2": {"bg": "#f0f0f0", "accent1": "#5c007f", "accent2": "#c57F51", "name": "现代主义清新", "theme": "modernist", "text_color": "#1a1a1a"},
    "modernist_3": {"bg": "linear-gradient(135deg,#5c5c80 0%,#5c5dff 100%)", "accent1": "#ffffff", "accent2": "#05c5ff", "name": "现代主义渐变", "theme": "modernist", "is_gradient": True},
    "modernist_4": {"bg": "#005c5d", "accent1": "#115cff", "accent2": "#05c5d1", "name": "现代主义撞色", "theme": "modernist", "text_color": "#ffffff"},
    "parametric_1": {"bg": "#121e1a", "accent1": "#00ff00", "accent2": "#f2beFF", "name": "参数化暗夜", "theme": "parametric"},
    "parametric_2": {"bg": "#f0f0f0", "accent1": "#72007f", "accent2": "#2b7F6b", "name": "参数化清新", "theme": "parametric", "text_color": "#1a1a1a"},
    "parametric_3": {"bg": "linear-gradient(135deg,#f2f280 0%,#f2beff 100%)", "accent1": "#ffffff", "accent2": "#0f2bff", "name": "参数化渐变", "theme": "parametric", "is_gradient": True},
    "parametric_4": {"bg": "#00f2be", "accent1": "#baf2ff", "accent2": "#0f2beb", "name": "参数化撞色", "theme": "parametric", "text_color": "#ffffff"},
    "glam_1": {"bg": "#0e1408", "accent1": "#00ff00", "accent2": "#6e54FF", "name": "华丽暗夜", "theme": "glam"},
    "glam_2": {"bg": "#f0f0f0", "accent1": "#6e007f", "accent2": "#e57F4e", "name": "华丽清新", "theme": "glam", "text_color": "#1a1a1a"},
    "glam_3": {"bg": "linear-gradient(135deg,#6e6e80 0%,#6e54ff 100%)", "accent1": "#ffffff", "accent2": "#06e5ff", "name": "华丽渐变", "theme": "glam", "is_gradient": True},
    "glam_4": {"bg": "#006e54", "accent1": "#e86eff", "accent2": "#06e54e", "name": "华丽撞色", "theme": "glam", "text_color": "#ffffff"},
    "grunge_1": {"bg": "#110a1a", "accent1": "#00ff00", "accent2": "#f16aFF", "name": "垃圾风暗夜", "theme": "grunge"},
    "grunge_2": {"bg": "#f0f0f0", "accent1": "#71007f", "accent2": "#167F2b", "name": "垃圾风清新", "theme": "grunge", "text_color": "#1a1a1a"},
    "grunge_3": {"bg": "linear-gradient(135deg,#f1f180 0%,#f16aff 100%)", "accent1": "#ffffff", "accent2": "#0f16ff", "name": "垃圾风渐变", "theme": "grunge", "is_gradient": True},
    "grunge_4": {"bg": "#00f16a", "accent1": "#baf1ff", "accent2": "#0f16ab", "name": "垃圾风撞色", "theme": "grunge", "text_color": "#ffffff"},
    "preppy_1": {"bg": "#161b1f", "accent1": "#00ff00", "accent2": "#36bbFF", "name": "学院风暗夜", "theme": "preppy"},
    "preppy_2": {"bg": "#f0f0f0", "accent1": "#36007f", "accent2": "#6b7F3d", "name": "学院风清新", "theme": "preppy", "text_color": "#1a1a1a"},
    "preppy_3": {"bg": "linear-gradient(135deg,#363680 0%,#36bbff 100%)", "accent1": "#ffffff", "accent2": "#036bff", "name": "学院风渐变", "theme": "preppy", "is_gradient": True},
    "preppy_4": {"bg": "#0036bb", "accent1": "#df36ff", "accent2": "#036bbd", "name": "学院风撞色", "theme": "preppy", "text_color": "#ffffff"},
    "maximal_1": {"bg": "#130a00", "accent1": "#00ff00", "accent2": "#d3aaFF", "name": "极繁主义暗夜", "theme": "maximal"},
    "maximal_2": {"bg": "#f0f0f0", "accent1": "#53007f", "accent2": "#3a7F24", "name": "极繁主义清新", "theme": "maximal", "text_color": "#1a1a1a"},
    "maximal_3": {"bg": "linear-gradient(135deg,#d3d380 0%,#d3aaff 100%)", "accent1": "#ffffff", "accent2": "#0d3aff", "name": "极繁主义渐变", "theme": "maximal", "is_gradient": True},
    "maximal_4": {"bg": "#00d3aa", "accent1": "#40d3ff", "accent2": "#0d3aa4", "name": "极繁主义撞色", "theme": "maximal", "text_color": "#ffffff"},
    "skate_1": {"bg": "#130706", "accent1": "#00ff00", "accent2": "#13a7FF", "name": "滑板暗夜", "theme": "skate"},
    "skate_2": {"bg": "#f0f0f0", "accent1": "#13007f", "accent2": "#3a7F74", "name": "滑板清新", "theme": "skate", "text_color": "#1a1a1a"},
    "skate_3": {"bg": "linear-gradient(135deg,#131380 0%,#13a7ff 100%)", "accent1": "#ffffff", "accent2": "#013aff", "name": "滑板渐变", "theme": "skate", "is_gradient": True},
    "skate_4": {"bg": "#0013a7", "accent1": "#4613ff", "accent2": "#013a74", "name": "滑板撞色", "theme": "skate", "text_color": "#ffffff"},
    "surf_1": {"bg": "#1d1c0a", "accent1": "#00ff00", "accent2": "#fd7cFF", "name": "冲浪暗夜", "theme": "surf"},
    "surf_2": {"bg": "#f0f0f0", "accent1": "#7d007f", "accent2": "#d77F40", "name": "冲浪清新", "theme": "surf", "text_color": "#1a1a1a"},
    "surf_3": {"bg": "linear-gradient(135deg,#fdfd80 0%,#fd7cff 100%)", "accent1": "#ffffff", "accent2": "#0fd7ff", "name": "冲浪渐变", "theme": "surf", "is_gradient": True},
    "surf_4": {"bg": "#00fd7c", "accent1": "#0afdff", "accent2": "#0fd7c0", "name": "冲浪撞色", "theme": "surf", "text_color": "#ffffff"},
    "bike_1": {"bg": "#050718", "accent1": "#00ff00", "accent2": "#85e7FF", "name": "骑行暗夜", "theme": "bike"},
    "bike_2": {"bg": "#f0f0f0", "accent1": "#05007f", "accent2": "#5e7F73", "name": "骑行清新", "theme": "bike", "text_color": "#1a1a1a"},
    "bike_3": {"bg": "linear-gradient(135deg,#858580 0%,#85e7ff 100%)", "accent1": "#ffffff", "accent2": "#085eff", "name": "骑行渐变", "theme": "bike", "is_gradient": True},
    "bike_4": {"bg": "#0085e7", "accent1": "#3885ff", "accent2": "#085e73", "name": "骑行撞色", "theme": "bike", "text_color": "#ffffff"},
    "tattoo_1": {"bg": "#020003", "accent1": "#00ff00", "accent2": "#42a0FF", "name": "纹身暗夜", "theme": "tattoo"},
    "tattoo_2": {"bg": "#f0f0f0", "accent1": "#42007f", "accent2": "#2a7F0a", "name": "纹身清新", "theme": "tattoo", "text_color": "#1a1a1a"},
    "tattoo_3": {"bg": "linear-gradient(135deg,#424280 0%,#42a0ff 100%)", "accent1": "#ffffff", "accent2": "#042aff", "name": "纹身渐变", "theme": "tattoo", "is_gradient": True},
    "tattoo_4": {"bg": "#0042a0", "accent1": "#a342ff", "accent2": "#042a0a", "name": "纹身撞色", "theme": "tattoo", "text_color": "#ffffff"},
    "fifties_1": {"bg": "#1b0a06", "accent1": "#00ff00", "accent2": "#7b0aFF", "name": "50年代暗夜", "theme": "fifties"},
    "fifties_2": {"bg": "#f0f0f0", "accent1": "#7b007f", "accent2": "#b07F20", "name": "50年代清新", "theme": "fifties", "text_color": "#1a1a1a"},
    "fifties_3": {"bg": "linear-gradient(135deg,#7b7b80 0%,#7b0aff 100%)", "accent1": "#ffffff", "accent2": "#07b0ff", "name": "50年代渐变", "theme": "fifties", "is_gradient": True},
    "fifties_4": {"bg": "#007b0a", "accent1": "#067bff", "accent2": "#07b0a0", "name": "50年代撞色", "theme": "fifties", "text_color": "#ffffff"},
    "sixties_1": {"bg": "#131d01", "accent1": "#00ff00", "accent2": "#f3fdFF", "name": "60年代暗夜", "theme": "sixties"},
    "sixties_2": {"bg": "#f0f0f0", "accent1": "#73007f", "accent2": "#3f7F5e", "name": "60年代清新", "theme": "sixties", "text_color": "#1a1a1a"},
    "sixties_3": {"bg": "linear-gradient(135deg,#f3f380 0%,#f3fdff 100%)", "accent1": "#ffffff", "accent2": "#0f3fff", "name": "60年代渐变", "theme": "sixties", "is_gradient": True},
    "sixties_4": {"bg": "#00f3fd", "accent1": "#e1f3ff", "accent2": "#0f3fde", "name": "60年代撞色", "theme": "sixties", "text_color": "#ffffff"},
    "seventies_1": {"bg": "#160f01", "accent1": "#00ff00", "accent2": "#966fFF", "name": "70年代暗夜", "theme": "seventies"},
    "seventies_2": {"bg": "#f0f0f0", "accent1": "#16007f", "accent2": "#667F70", "name": "70年代清新", "theme": "seventies", "text_color": "#1a1a1a"},
    "seventies_3": {"bg": "linear-gradient(135deg,#969680 0%,#966fff 100%)", "accent1": "#ffffff", "accent2": "#0966ff", "name": "70年代渐变", "theme": "seventies", "is_gradient": True},
    "seventies_4": {"bg": "#00966f", "accent1": "#0196ff", "accent2": "#0966f0", "name": "70年代撞色", "theme": "seventies", "text_color": "#ffffff"},
    "eighties_1": {"bg": "#191e1d", "accent1": "#00ff00", "accent2": "#d93eFF", "name": "80年代暗夜", "theme": "eighties"},
    "eighties_2": {"bg": "#f0f0f0", "accent1": "#59007f", "accent2": "#937F65", "name": "80年代清新", "theme": "eighties", "text_color": "#1a1a1a"},
    "eighties_3": {"bg": "linear-gradient(135deg,#d9d980 0%,#d93eff 100%)", "accent1": "#ffffff", "accent2": "#0d93ff", "name": "80年代渐变", "theme": "eighties", "is_gradient": True},
    "eighties_4": {"bg": "#00d93e", "accent1": "#5dd9ff", "accent2": "#0d93e5", "name": "80年代撞色", "theme": "eighties", "text_color": "#ffffff"},
    "nineties_1": {"bg": "#051f1c", "accent1": "#00ff00", "accent2": "#453fFF", "name": "90年代暗夜", "theme": "nineties"},
    "nineties_2": {"bg": "#f0f0f0", "accent1": "#45007f", "accent2": "#537F73", "name": "90年代清新", "theme": "nineties", "text_color": "#1a1a1a"},
    "nineties_3": {"bg": "linear-gradient(135deg,#454580 0%,#453fff 100%)", "accent1": "#ffffff", "accent2": "#0453ff", "name": "90年代渐变", "theme": "nineties", "is_gradient": True},
    "nineties_4": {"bg": "#00453f", "accent1": "#3c45ff", "accent2": "#0453f3", "name": "90年代撞色", "theme": "nineties", "text_color": "#ffffff"},
    "y2k2_1": {"bg": "#000e0f", "accent1": "#00ff00", "accent2": "#e0aeFF", "name": "Y2K千禧暗夜", "theme": "y2k2"},
    "y2k2_2": {"bg": "#f0f0f0", "accent1": "#60007f", "accent2": "#0a7F60", "name": "Y2K千禧清新", "theme": "y2k2", "text_color": "#1a1a1a"},
    "y2k2_3": {"bg": "linear-gradient(135deg,#e0e080 0%,#e0aeff 100%)", "accent1": "#ffffff", "accent2": "#0e0aff", "name": "Y2K千禧渐变", "theme": "y2k2", "is_gradient": True},
    "y2k2_4": {"bg": "#00e0ae", "accent1": "#0fe0ff", "accent2": "#0e0ae0", "name": "Y2K千禧撞色", "theme": "y2k2", "text_color": "#ffffff"},
    "solarpunk_1": {"bg": "#140b0f", "accent1": "#00ff00", "accent2": "#d48bFF", "name": "太阳朋克暗夜", "theme": "solarpunk"},
    "solarpunk_2": {"bg": "#f0f0f0", "accent1": "#54007f", "accent2": "#487F3c", "name": "太阳朋克清新", "theme": "solarpunk", "text_color": "#1a1a1a"},
    "solarpunk_3": {"bg": "linear-gradient(135deg,#d4d480 0%,#d48bff 100%)", "accent1": "#ffffff", "accent2": "#0d48ff", "name": "太阳朋克渐变", "theme": "solarpunk", "is_gradient": True},
    "solarpunk_4": {"bg": "#00d48b", "accent1": "#cfd4ff", "accent2": "#0d48bc", "name": "太阳朋克撞色", "theme": "solarpunk", "text_color": "#ffffff"},
    "biopunk_1": {"bg": "#0a0a02", "accent1": "#00ff00", "accent2": "#8a2aFF", "name": "生物朋克暗夜", "theme": "biopunk"},
    "biopunk_2": {"bg": "#f0f0f0", "accent1": "#0a007f", "accent2": "#a27F2e", "name": "生物朋克清新", "theme": "biopunk", "text_color": "#1a1a1a"},
    "biopunk_3": {"bg": "linear-gradient(135deg,#8a8a80 0%,#8a2aff 100%)", "accent1": "#ffffff", "accent2": "#08a2ff", "name": "生物朋克渐变", "theme": "biopunk", "is_gradient": True},
    "biopunk_4": {"bg": "#008a2a", "accent1": "#e28aff", "accent2": "#08a2ae", "name": "生物朋克撞色", "theme": "biopunk", "text_color": "#ffffff"},
    "nanopunk_1": {"bg": "#11001e", "accent1": "#00ff00", "accent2": "#51c0FF", "name": "纳米朋克暗夜", "theme": "nanopunk"},
    "nanopunk_2": {"bg": "#f0f0f0", "accent1": "#51007f", "accent2": "#1c7F01", "name": "纳米朋克清新", "theme": "nanopunk", "text_color": "#1a1a1a"},
    "nanopunk_3": {"bg": "linear-gradient(135deg,#515180 0%,#51c0ff 100%)", "accent1": "#ffffff", "accent2": "#051cff", "name": "纳米朋克渐变", "theme": "nanopunk", "is_gradient": True},
    "nanopunk_4": {"bg": "#0051c0", "accent1": "#1e51ff", "accent2": "#051c01", "name": "纳米朋克撞色", "theme": "nanopunk", "text_color": "#ffffff"},
    "posthuman_1": {"bg": "#151c14", "accent1": "#00ff00", "accent2": "#b53cFF", "name": "后人类暗夜", "theme": "posthuman"},
    "posthuman_2": {"bg": "#f0f0f0", "accent1": "#35007f", "accent2": "#537F43", "name": "后人类清新", "theme": "posthuman", "text_color": "#1a1a1a"},
    "posthuman_3": {"bg": "linear-gradient(135deg,#b5b580 0%,#b53cff 100%)", "accent1": "#ffffff", "accent2": "#0b53ff", "name": "后人类渐变", "theme": "posthuman", "is_gradient": True},
    "posthuman_4": {"bg": "#00b53c", "accent1": "#34b5ff", "accent2": "#0b53c3", "name": "后人类撞色", "theme": "posthuman", "text_color": "#ffffff"},
    "glitch2_1": {"bg": "#010e09", "accent1": "#00ff00", "accent2": "#a18eFF", "name": "故障艺术暗夜", "theme": "glitch2"},
    "glitch2_2": {"bg": "#f0f0f0", "accent1": "#21007f", "accent2": "#187F68", "name": "故障艺术清新", "theme": "glitch2", "text_color": "#1a1a1a"},
    "glitch2_3": {"bg": "linear-gradient(135deg,#a1a180 0%,#a18eff 100%)", "accent1": "#ffffff", "accent2": "#0a18ff", "name": "故障艺术渐变", "theme": "glitch2", "is_gradient": True},
    "glitch2_4": {"bg": "#00a18e", "accent1": "#89a1ff", "accent2": "#0a18e8", "name": "故障艺术撞色", "theme": "glitch2", "text_color": "#ffffff"},
    "datamosh_1": {"bg": "#041413", "accent1": "#00ff00", "accent2": "#4474FF", "name": "数据压缩暗夜", "theme": "datamosh"},
    "datamosh_2": {"bg": "#f0f0f0", "accent1": "#44007f", "accent2": "#477F45", "name": "数据压缩清新", "theme": "datamosh", "text_color": "#1a1a1a"},
    "datamosh_3": {"bg": "linear-gradient(135deg,#444480 0%,#4474ff 100%)", "accent1": "#ffffff", "accent2": "#0447ff", "name": "数据压缩渐变", "theme": "datamosh", "is_gradient": True},
    "datamosh_4": {"bg": "#004474", "accent1": "#5344ff", "accent2": "#044745", "name": "数据压缩撞色", "theme": "datamosh", "text_color": "#ffffff"},
    "ascii_1": {"bg": "#111d01", "accent1": "#00ff00", "accent2": "#713dFF", "name": "ASCII艺术暗夜", "theme": "ascii"},
    "ascii_2": {"bg": "#f0f0f0", "accent1": "#71007f", "accent2": "#137F54", "name": "ASCII艺术清新", "theme": "ascii", "text_color": "#1a1a1a"},
    "ascii_3": {"bg": "linear-gradient(135deg,#717180 0%,#713dff 100%)", "accent1": "#ffffff", "accent2": "#0713ff", "name": "ASCII艺术渐变", "theme": "ascii", "is_gradient": True},
    "ascii_4": {"bg": "#00713d", "accent1": "#4171ff", "accent2": "#0713d4", "name": "ASCII艺术撞色", "theme": "ascii", "text_color": "#ffffff"},
    "generative_1": {"bg": "#151b00", "accent1": "#00ff00", "accent2": "#55dbFF", "name": "生成艺术暗夜", "theme": "generative"},
    "generative_2": {"bg": "#f0f0f0", "accent1": "#55007f", "accent2": "#5d7F3a", "name": "生成艺术清新", "theme": "generative", "text_color": "#1a1a1a"},
    "generative_3": {"bg": "linear-gradient(135deg,#555580 0%,#55dbff 100%)", "accent1": "#ffffff", "accent2": "#055dff", "name": "生成艺术渐变", "theme": "generative", "is_gradient": True},
    "generative_4": {"bg": "#0055db", "accent1": "#a055ff", "accent2": "#055dba", "name": "生成艺术撞色", "theme": "generative", "text_color": "#ffffff"},
    "fractal_1": {"bg": "#060212", "accent1": "#00ff00", "accent2": "#6602FF", "name": "分形暗夜", "theme": "fractal"},
    "fractal_2": {"bg": "#f0f0f0", "accent1": "#66007f", "accent2": "#607F29", "name": "分形清新", "theme": "fractal", "text_color": "#1a1a1a"},
    "fractal_3": {"bg": "linear-gradient(135deg,#666680 0%,#6602ff 100%)", "accent1": "#ffffff", "accent2": "#0660ff", "name": "分形渐变", "theme": "fractal", "is_gradient": True},
    "fractal_4": {"bg": "#006602", "accent1": "#9266ff", "accent2": "#066029", "name": "分形撞色", "theme": "fractal", "text_color": "#ffffff"},
    "voronoi_1": {"bg": "#011f0e", "accent1": "#00ff00", "accent2": "#417fFF", "name": "沃罗诺伊暗夜", "theme": "voronoi"},
    "voronoi_2": {"bg": "#f0f0f0", "accent1": "#41007f", "accent2": "#177F70", "name": "沃罗诺伊清新", "theme": "voronoi", "text_color": "#1a1a1a"},
    "voronoi_3": {"bg": "linear-gradient(135deg,#414180 0%,#417fff 100%)", "accent1": "#ffffff", "accent2": "#0417ff", "name": "沃罗诺伊渐变", "theme": "voronoi", "is_gradient": True},
    "voronoi_4": {"bg": "#00417f", "accent1": "#0e41ff", "accent2": "#0417f0", "name": "沃罗诺伊撞色", "theme": "voronoi", "text_color": "#ffffff"},
    "particles_1": {"bg": "#131f15", "accent1": "#00ff00", "accent2": "#539fFF", "name": "粒子暗夜", "theme": "particles"},
    "particles_2": {"bg": "#f0f0f0", "accent1": "#53007f", "accent2": "#397F7d", "name": "粒子清新", "theme": "particles", "text_color": "#1a1a1a"},
    "particles_3": {"bg": "linear-gradient(135deg,#535380 0%,#539fff 100%)", "accent1": "#ffffff", "accent2": "#0539ff", "name": "粒子渐变", "theme": "particles", "is_gradient": True},
    "particles_4": {"bg": "#00539f", "accent1": "#d553ff", "accent2": "#0539fd", "name": "粒子撞色", "theme": "particles", "text_color": "#ffffff"},
    "fluid_1": {"bg": "#181319", "accent1": "#00ff00", "accent2": "#f8d3FF", "name": "流体暗夜", "theme": "fluid"},
    "fluid_2": {"bg": "#f0f0f0", "accent1": "#78007f", "accent2": "#8d7F35", "name": "流体清新", "theme": "fluid", "text_color": "#1a1a1a"},
    "fluid_3": {"bg": "linear-gradient(135deg,#f8f880 0%,#f8d3ff 100%)", "accent1": "#ffffff", "accent2": "#0f8dff", "name": "流体渐变", "theme": "fluid", "is_gradient": True},
    "fluid_4": {"bg": "#00f8d3", "accent1": "#59f8ff", "accent2": "#0f8d35", "name": "流体撞色", "theme": "fluid", "text_color": "#ffffff"},
    "abstract_1": {"bg": "#1e081b", "accent1": "#00ff00", "accent2": "#dec8FF", "name": "抽象暗夜", "theme": "abstract"},
    "abstract_2": {"bg": "#f0f0f0", "accent1": "#5e007f", "accent2": "#ec7F0d", "name": "抽象清新", "theme": "abstract", "text_color": "#1a1a1a"},
    "abstract_3": {"bg": "linear-gradient(135deg,#dede80 0%,#dec8ff 100%)", "accent1": "#ffffff", "accent2": "#0decff", "name": "抽象渐变", "theme": "abstract", "is_gradient": True},
    "abstract_4": {"bg": "#00dec8", "accent1": "#dbdeff", "accent2": "#0dec8d", "name": "抽象撞色", "theme": "abstract", "text_color": "#ffffff"},
    "geometric_1": {"bg": "#1f170c", "accent1": "#00ff00", "accent2": "#ffd7FF", "name": "几何暗夜", "theme": "geometric"},
    "geometric_2": {"bg": "#f0f0f0", "accent1": "#7f007f", "accent2": "#fd7F78", "name": "几何清新", "theme": "geometric", "text_color": "#1a1a1a"},
    "geometric_3": {"bg": "linear-gradient(135deg,#ffff80 0%,#ffd7ff 100%)", "accent1": "#ffffff", "accent2": "#0ffdff", "name": "几何渐变", "theme": "geometric", "is_gradient": True},
    "geometric_4": {"bg": "#00ffd7", "accent1": "#8cffff", "accent2": "#0ffd78", "name": "几何撞色", "theme": "geometric", "text_color": "#ffffff"},
    "opart_1": {"bg": "#1f0619", "accent1": "#00ff00", "accent2": "#7f86FF", "name": "视错觉暗夜", "theme": "opart"},
    "opart_2": {"bg": "#f0f0f0", "accent1": "#7f007f", "accent2": "#f87F6b", "name": "视错觉清新", "theme": "opart", "text_color": "#1a1a1a"},
    "opart_3": {"bg": "linear-gradient(135deg,#7f7f80 0%,#7f86ff 100%)", "accent1": "#ffffff", "accent2": "#07f8ff", "name": "视错觉渐变", "theme": "opart", "is_gradient": True},
    "opart_4": {"bg": "#007f86", "accent1": "#b97fff", "accent2": "#07f86b", "name": "视错觉撞色", "theme": "opart", "text_color": "#ffffff"},
    "kinetic_1": {"bg": "#1b110d", "accent1": "#00ff00", "accent2": "#3b91FF", "name": "动态艺术暗夜", "theme": "kinetic"},
    "kinetic_2": {"bg": "#f0f0f0", "accent1": "#3b007f", "accent2": "#b97F18", "name": "动态艺术清新", "theme": "kinetic", "text_color": "#1a1a1a"},
    "kinetic_3": {"bg": "linear-gradient(135deg,#3b3b80 0%,#3b91ff 100%)", "accent1": "#ffffff", "accent2": "#03b9ff", "name": "动态艺术渐变", "theme": "kinetic", "is_gradient": True},
    "kinetic_4": {"bg": "#003b91", "accent1": "#8d3bff", "accent2": "#03b918", "name": "动态艺术撞色", "theme": "kinetic", "text_color": "#ffffff"},
    "colorfield_1": {"bg": "#180b19", "accent1": "#00ff00", "accent2": "#588bFF", "name": "色域暗夜", "theme": "colorfield"},
    "colorfield_2": {"bg": "#f0f0f0", "accent1": "#58007f", "accent2": "#887F3f", "name": "色域清新", "theme": "colorfield", "text_color": "#1a1a1a"},
    "colorfield_3": {"bg": "linear-gradient(135deg,#585880 0%,#588bff 100%)", "accent1": "#ffffff", "accent2": "#0588ff", "name": "色域渐变", "theme": "colorfield", "is_gradient": True},
    "colorfield_4": {"bg": "#00588b", "accent1": "#f958ff", "accent2": "#0588bf", "name": "色域撞色", "theme": "colorfield", "text_color": "#ffffff"},
    "monochrome_1": {"bg": "#03010f", "accent1": "#00ff00", "accent2": "#e321FF", "name": "单色暗夜", "theme": "monochrome"},
    "monochrome_2": {"bg": "#f0f0f0", "accent1": "#63007f", "accent2": "#327F1a", "name": "单色清新", "theme": "monochrome", "text_color": "#1a1a1a"},
    "monochrome_3": {"bg": "linear-gradient(135deg,#e3e380 0%,#e321ff 100%)", "accent1": "#ffffff", "accent2": "#0e32ff", "name": "单色渐变", "theme": "monochrome", "is_gradient": True},
    "monochrome_4": {"bg": "#00e321", "accent1": "#afe3ff", "accent2": "#0e321a", "name": "单色撞色", "theme": "monochrome", "text_color": "#ffffff"},
    "duotone_1": {"bg": "#160518", "accent1": "#00ff00", "accent2": "#76e5FF", "name": "双色调暗夜", "theme": "duotone"},
    "duotone_2": {"bg": "#f0f0f0", "accent1": "#76007f", "accent2": "#6e7F5d", "name": "双色调清新", "theme": "duotone", "text_color": "#1a1a1a"},
    "duotone_3": {"bg": "linear-gradient(135deg,#767680 0%,#76e5ff 100%)", "accent1": "#ffffff", "accent2": "#076eff", "name": "双色调渐变", "theme": "duotone", "is_gradient": True},
    "duotone_4": {"bg": "#0076e5", "accent1": "#d876ff", "accent2": "#076e5d", "name": "双色调撞色", "theme": "duotone", "text_color": "#ffffff"},
    "pattern_1": {"bg": "#01020c", "accent1": "#00ff00", "accent2": "#0162FF", "name": "图案暗夜", "theme": "pattern"},
    "pattern_2": {"bg": "#f0f0f0", "accent1": "#01007f", "accent2": "#167F20", "name": "图案清新", "theme": "pattern", "text_color": "#1a1a1a"},
    "pattern_3": {"bg": "linear-gradient(135deg,#010180 0%,#0162ff 100%)", "accent1": "#ffffff", "accent2": "#0016ff", "name": "图案渐变", "theme": "pattern", "is_gradient": True},
    "pattern_4": {"bg": "#000162", "accent1": "#0c01ff", "accent2": "#001620", "name": "图案撞色", "theme": "pattern", "text_color": "#ffffff"},
    "ornate_1": {"bg": "#061b07", "accent1": "#00ff00", "accent2": "#c6fbFF", "name": "华丽装饰暗夜", "theme": "ornate"},
    "ornate_2": {"bg": "#f0f0f0", "accent1": "#46007f", "accent2": "#6f7F3e", "name": "华丽装饰清新", "theme": "ornate", "text_color": "#1a1a1a"},
    "ornate_3": {"bg": "linear-gradient(135deg,#c6c680 0%,#c6fbff 100%)", "accent1": "#ffffff", "accent2": "#0c6fff", "name": "华丽装饰渐变", "theme": "ornate", "is_gradient": True},
    "ornate_4": {"bg": "#00c6fb", "accent1": "#e7c6ff", "accent2": "#0c6fbe", "name": "华丽装饰撞色", "theme": "ornate", "text_color": "#ffffff"},
    "rococo_1": {"bg": "#09170b", "accent1": "#00ff00", "accent2": "#a9d7FF", "name": "洛可可暗夜", "theme": "rococo"},
    "rococo_2": {"bg": "#f0f0f0", "accent1": "#29007f", "accent2": "#9d7F72", "name": "洛可可清新", "theme": "rococo", "text_color": "#1a1a1a"},
    "rococo_3": {"bg": "linear-gradient(135deg,#a9a980 0%,#a9d7ff 100%)", "accent1": "#ffffff", "accent2": "#0a9dff", "name": "洛可可渐变", "theme": "rococo", "is_gradient": True},
    "rococo_4": {"bg": "#00a9d7", "accent1": "#2ba9ff", "accent2": "#0a9d72", "name": "洛可可撞色", "theme": "rococo", "text_color": "#ffffff"},
    "chrome_1": {"bg": "#021612", "accent1": "#00ff00", "accent2": "#4216FF", "name": "镀铬暗夜", "theme": "chrome"},
    "chrome_2": {"bg": "#f0f0f0", "accent1": "#42007f", "accent2": "#217F6d", "name": "镀铬清新", "theme": "chrome", "text_color": "#1a1a1a"},
    "chrome_3": {"bg": "linear-gradient(135deg,#424280 0%,#4216ff 100%)", "accent1": "#ffffff", "accent2": "#0421ff", "name": "镀铬渐变", "theme": "chrome", "is_gradient": True},
    "chrome_4": {"bg": "#004216", "accent1": "#d242ff", "accent2": "#04216d", "name": "镀铬撞色", "theme": "chrome", "text_color": "#ffffff"},
    "gold_1": {"bg": "#090f14", "accent1": "#00ff00", "accent2": "#894fFF", "name": "黄金暗夜", "theme": "gold"},
    "gold_2": {"bg": "#f0f0f0", "accent1": "#09007f", "accent2": "#947F77", "name": "黄金清新", "theme": "gold", "text_color": "#1a1a1a"},
    "gold_3": {"bg": "linear-gradient(135deg,#898980 0%,#894fff 100%)", "accent1": "#ffffff", "accent2": "#0894ff", "name": "黄金渐变", "theme": "gold", "is_gradient": True},
    "gold_4": {"bg": "#00894f", "accent1": "#7489ff", "accent2": "#0894f7", "name": "黄金撞色", "theme": "gold", "text_color": "#ffffff"},
    "silver_1": {"bg": "#170911", "accent1": "#00ff00", "accent2": "#5789FF", "name": "白银暗夜", "theme": "silver"},
    "silver_2": {"bg": "#f0f0f0", "accent1": "#57007f", "accent2": "#787F11", "name": "白银清新", "theme": "silver", "text_color": "#1a1a1a"},
    "silver_3": {"bg": "linear-gradient(135deg,#575780 0%,#5789ff 100%)", "accent1": "#ffffff", "accent2": "#0578ff", "name": "白银渐变", "theme": "silver", "is_gradient": True},
    "silver_4": {"bg": "#005789", "accent1": "#1157ff", "accent2": "#057891", "name": "白银撞色", "theme": "silver", "text_color": "#ffffff"},
    "iridescent_1": {"bg": "#1f1d03", "accent1": "#00ff00", "accent2": "#9fbdFF", "name": "虹彩暗夜", "theme": "iridescent"},
    "iridescent_2": {"bg": "#f0f0f0", "accent1": "#1f007f", "accent2": "#fb7F5a", "name": "虹彩清新", "theme": "iridescent", "text_color": "#1a1a1a"},
    "iridescent_3": {"bg": "linear-gradient(135deg,#9f9f80 0%,#9fbdff 100%)", "accent1": "#ffffff", "accent2": "#09fbff", "name": "虹彩渐变", "theme": "iridescent", "is_gradient": True},
    "iridescent_4": {"bg": "#009fbd", "accent1": "#a39fff", "accent2": "#09fbda", "name": "虹彩撞色", "theme": "iridescent", "text_color": "#ffffff"},
    "pearlescent_1": {"bg": "#130f11", "accent1": "#00ff00", "accent2": "#f36fFF", "name": "珍珠暗夜", "theme": "pearlescent"},
    "pearlescent_2": {"bg": "#f0f0f0", "accent1": "#73007f", "accent2": "#367F7b", "name": "珍珠清新", "theme": "pearlescent", "text_color": "#1a1a1a"},
    "pearlescent_3": {"bg": "linear-gradient(135deg,#f3f380 0%,#f36fff 100%)", "accent1": "#ffffff", "accent2": "#0f36ff", "name": "珍珠渐变", "theme": "pearlescent", "is_gradient": True},
    "pearlescent_4": {"bg": "#00f36f", "accent1": "#b1f3ff", "accent2": "#0f36fb", "name": "珍珠撞色", "theme": "pearlescent", "text_color": "#ffffff"},
    "matte_1": {"bg": "#101312", "accent1": "#00ff00", "accent2": "#9033FF", "name": "哑光暗夜", "theme": "matte"},
    "matte_2": {"bg": "#f0f0f0", "accent1": "#10007f", "accent2": "#037F3b", "name": "哑光清新", "theme": "matte", "text_color": "#1a1a1a"},
    "matte_3": {"bg": "linear-gradient(135deg,#909080 0%,#9033ff 100%)", "accent1": "#ffffff", "accent2": "#0903ff", "name": "哑光渐变", "theme": "matte", "is_gradient": True},
    "matte_4": {"bg": "#009033", "accent1": "#b290ff", "accent2": "#09033b", "name": "哑光撞色", "theme": "matte", "text_color": "#ffffff"},
    "glossy_1": {"bg": "#1f1816", "accent1": "#00ff00", "accent2": "#9f18FF", "name": "光泽暗夜", "theme": "glossy"},
    "glossy_2": {"bg": "#f0f0f0", "accent1": "#1f007f", "accent2": "#f17F0d", "name": "光泽清新", "theme": "glossy", "text_color": "#1a1a1a"},
    "glossy_3": {"bg": "linear-gradient(135deg,#9f9f80 0%,#9f18ff 100%)", "accent1": "#ffffff", "accent2": "#09f1ff", "name": "光泽渐变", "theme": "glossy", "is_gradient": True},
    "glossy_4": {"bg": "#009f18", "accent1": "#d69fff", "accent2": "#09f18d", "name": "光泽撞色", "theme": "glossy", "text_color": "#ffffff"},
    "mirror_1": {"bg": "#080e0f", "accent1": "#00ff00", "accent2": "#68ceFF", "name": "镜面暗夜", "theme": "mirror"},
    "mirror_2": {"bg": "#f0f0f0", "accent1": "#68007f", "accent2": "#8c7F6a", "name": "镜面清新", "theme": "mirror", "text_color": "#1a1a1a"},
    "mirror_3": {"bg": "linear-gradient(135deg,#686880 0%,#68ceff 100%)", "accent1": "#ffffff", "accent2": "#068cff", "name": "镜面渐变", "theme": "mirror", "is_gradient": True},
    "mirror_4": {"bg": "#0068ce", "accent1": "#af68ff", "accent2": "#068cea", "name": "镜面撞色", "theme": "mirror", "text_color": "#ffffff"},
    "shadow_1": {"bg": "#1e1809", "accent1": "#00ff00", "accent2": "#7e58FF", "name": "阴影暗夜", "theme": "shadow"},
    "shadow_2": {"bg": "#f0f0f0", "accent1": "#7e007f", "accent2": "#e57F02", "name": "阴影清新", "theme": "shadow", "text_color": "#1a1a1a"},
    "shadow_3": {"bg": "linear-gradient(135deg,#7e7e80 0%,#7e58ff 100%)", "accent1": "#ffffff", "accent2": "#07e5ff", "name": "阴影渐变", "theme": "shadow", "is_gradient": True},
    "shadow_4": {"bg": "#007e58", "accent1": "#297eff", "accent2": "#07e582", "name": "阴影撞色", "theme": "shadow", "text_color": "#ffffff"},
    "laser_1": {"bg": "#020413", "accent1": "#00ff00", "accent2": "#e264FF", "name": "激光暗夜", "theme": "laser"},
    "laser_2": {"bg": "#f0f0f0", "accent1": "#62007f", "accent2": "#267F45", "name": "激光清新", "theme": "laser", "text_color": "#1a1a1a"},
    "laser_3": {"bg": "linear-gradient(135deg,#e2e280 0%,#e264ff 100%)", "accent1": "#ffffff", "accent2": "#0e26ff", "name": "激光渐变", "theme": "laser", "is_gradient": True},
    "laser_4": {"bg": "#00e264", "accent1": "#53e2ff", "accent2": "#0e2645", "name": "激光撞色", "theme": "laser", "text_color": "#ffffff"},
    "prism_1": {"bg": "#18060b", "accent1": "#00ff00", "accent2": "#3866FF", "name": "棱镜暗夜", "theme": "prism"},
    "prism_2": {"bg": "#f0f0f0", "accent1": "#38007f", "accent2": "#867F6a", "name": "棱镜清新", "theme": "prism", "text_color": "#1a1a1a"},
    "prism_3": {"bg": "linear-gradient(135deg,#383880 0%,#3866ff 100%)", "accent1": "#ffffff", "accent2": "#0386ff", "name": "棱镜渐变", "theme": "prism", "is_gradient": True},
    "prism_4": {"bg": "#003866", "accent1": "#ab38ff", "accent2": "#03866a", "name": "棱镜撞色", "theme": "prism", "text_color": "#ffffff"},
    "crystal_1": {"bg": "#0c1c07", "accent1": "#00ff00", "accent2": "#8cdcFF", "name": "水晶暗夜", "theme": "crystal"},
    "crystal_2": {"bg": "#f0f0f0", "accent1": "#0c007f", "accent2": "#cd7F4a", "name": "水晶清新", "theme": "crystal", "text_color": "#1a1a1a"},
    "crystal_3": {"bg": "linear-gradient(135deg,#8c8c80 0%,#8cdcff 100%)", "accent1": "#ffffff", "accent2": "#08cdff", "name": "水晶渐变", "theme": "crystal", "is_gradient": True},
    "crystal_4": {"bg": "#008cdc", "accent1": "#a78cff", "accent2": "#08cdca", "name": "水晶撞色", "theme": "crystal", "text_color": "#ffffff"},
    "diamond_1": {"bg": "#041008", "accent1": "#00ff00", "accent2": "#c490FF", "name": "钻石暗夜", "theme": "diamond"},
    "diamond_2": {"bg": "#f0f0f0", "accent1": "#44007f", "accent2": "#497F0c", "name": "钻石清新", "theme": "diamond", "text_color": "#1a1a1a"},
    "diamond_3": {"bg": "linear-gradient(135deg,#c4c480 0%,#c490ff 100%)", "accent1": "#ffffff", "accent2": "#0c49ff", "name": "钻石渐变", "theme": "diamond", "is_gradient": True},
    "diamond_4": {"bg": "#00c490", "accent1": "#c8c4ff", "accent2": "#0c490c", "name": "钻石撞色", "theme": "diamond", "text_color": "#ffffff"},
    "lightning_1": {"bg": "#130a17", "accent1": "#00ff00", "accent2": "#d30aFF", "name": "闪电暗夜", "theme": "lightning"},
    "lightning_2": {"bg": "#f0f0f0", "accent1": "#53007f", "accent2": "#307F2f", "name": "闪电清新", "theme": "lightning", "text_color": "#1a1a1a"},
    "lightning_3": {"bg": "linear-gradient(135deg,#d3d380 0%,#d30aff 100%)", "accent1": "#ffffff", "accent2": "#0d30ff", "name": "闪电渐变", "theme": "lightning", "is_gradient": True},
    "lightning_4": {"bg": "#00d30a", "accent1": "#f7d3ff", "accent2": "#0d30af", "name": "闪电撞色", "theme": "lightning", "text_color": "#ffffff"},
    "storm_1": {"bg": "#090313", "accent1": "#00ff00", "accent2": "#e9a3FF", "name": "暴风暗夜", "theme": "storm"},
    "storm_2": {"bg": "#f0f0f0", "accent1": "#69007f", "accent2": "#9a7F35", "name": "暴风清新", "theme": "storm", "text_color": "#1a1a1a"},
    "storm_3": {"bg": "linear-gradient(135deg,#e9e980 0%,#e9a3ff 100%)", "accent1": "#ffffff", "accent2": "#0e9aff", "name": "暴风渐变", "theme": "storm", "is_gradient": True},
    "storm_4": {"bg": "#00e9a3", "accent1": "#53e9ff", "accent2": "#0e9a35", "name": "暴风撞色", "theme": "storm", "text_color": "#ffffff"},
    "volcano_1": {"bg": "#021c11", "accent1": "#00ff00", "accent2": "#829cFF", "name": "火山暗夜", "theme": "volcano"},
    "volcano_2": {"bg": "#f0f0f0", "accent1": "#02007f", "accent2": "#297F43", "name": "火山清新", "theme": "volcano", "text_color": "#1a1a1a"},
    "volcano_3": {"bg": "linear-gradient(135deg,#828280 0%,#829cff 100%)", "accent1": "#ffffff", "accent2": "#0829ff", "name": "火山渐变", "theme": "volcano", "is_gradient": True},
    "volcano_4": {"bg": "#00829c", "accent1": "#3182ff", "accent2": "#0829c3", "name": "火山撞色", "theme": "volcano", "text_color": "#ffffff"},
    "tsunami_1": {"bg": "#180d0d", "accent1": "#00ff00", "accent2": "#b8cdFF", "name": "海啸暗夜", "theme": "tsunami"},
    "tsunami_2": {"bg": "#f0f0f0", "accent1": "#38007f", "accent2": "#8c7F50", "name": "海啸清新", "theme": "tsunami", "text_color": "#1a1a1a"},
    "tsunami_3": {"bg": "linear-gradient(135deg,#b8b880 0%,#b8cdff 100%)", "accent1": "#ffffff", "accent2": "#0b8cff", "name": "海啸渐变", "theme": "tsunami", "is_gradient": True},
    "tsunami_4": {"bg": "#00b8cd", "accent1": "#0db8ff", "accent2": "#0b8cd0", "name": "海啸撞色", "theme": "tsunami", "text_color": "#ffffff"},
    "ukiyoe_1": {"bg": "#1f0b00", "accent1": "#00ff00", "accent2": "#5fcbFF", "name": "浮世绘暗夜", "theme": "ukiyoe"},
    "ukiyoe_2": {"bg": "#f0f0f0", "accent1": "#5f007f", "accent2": "#fc7F34", "name": "浮世绘清新", "theme": "ukiyoe", "text_color": "#1a1a1a"},
    "ukiyoe_3": {"bg": "linear-gradient(135deg,#5f5f80 0%,#5fcbff 100%)", "accent1": "#ffffff", "accent2": "#05fcff", "name": "浮世绘渐变", "theme": "ukiyoe", "is_gradient": True},
    "ukiyoe_4": {"bg": "#005fcb", "accent1": "#405fff", "accent2": "#05fcb4", "name": "浮世绘撞色", "theme": "ukiyoe", "text_color": "#ffffff"},
    "sumi_e_1": {"bg": "#151100", "accent1": "#00ff00", "accent2": "#7571FF", "name": "水墨画暗夜", "theme": "sumi_e"},
    "sumi_e_2": {"bg": "#f0f0f0", "accent1": "#75007f", "accent2": "#577F16", "name": "水墨画清新", "theme": "sumi_e", "text_color": "#1a1a1a"},
    "sumi_e_3": {"bg": "linear-gradient(135deg,#757580 0%,#7571ff 100%)", "accent1": "#ffffff", "accent2": "#0757ff", "name": "水墨画渐变", "theme": "sumi_e", "is_gradient": True},
    "sumi_e_4": {"bg": "#007571", "accent1": "#6075ff", "accent2": "#075716", "name": "水墨画撞色", "theme": "sumi_e", "text_color": "#ffffff"},
    "mingqing_1": {"bg": "#1e041e", "accent1": "#00ff00", "accent2": "#9e64FF", "name": "明清风暗夜", "theme": "mingqing"},
    "mingqing_2": {"bg": "#f0f0f0", "accent1": "#1e007f", "accent2": "#e67F45", "name": "明清风清新", "theme": "mingqing", "text_color": "#1a1a1a"},
    "mingqing_3": {"bg": "linear-gradient(135deg,#9e9e80 0%,#9e64ff 100%)", "accent1": "#ffffff", "accent2": "#09e6ff", "name": "明清风渐变", "theme": "mingqing", "is_gradient": True},
    "mingqing_4": {"bg": "#009e64", "accent1": "#5e9eff", "accent2": "#09e645", "name": "明清风撞色", "theme": "mingqing", "text_color": "#ffffff"},
    "dunhuang_1": {"bg": "#0d1805", "accent1": "#00ff00", "accent2": "#0d98FF", "name": "敦煌暗夜", "theme": "dunhuang"},
    "dunhuang_2": {"bg": "#f0f0f0", "accent1": "#0d007f", "accent2": "#d97F0e", "name": "敦煌清新", "theme": "dunhuang", "text_color": "#1a1a1a"},
    "dunhuang_3": {"bg": "linear-gradient(135deg,#0d0d80 0%,#0d98ff 100%)", "accent1": "#ffffff", "accent2": "#00d9ff", "name": "敦煌渐变", "theme": "dunhuang", "is_gradient": True},
    "dunhuang_4": {"bg": "#000d98", "accent1": "#e50dff", "accent2": "#00d98e", "name": "敦煌撞色", "theme": "dunhuang", "text_color": "#ffffff"},
    "shuimo_1": {"bg": "#110d1f", "accent1": "#00ff00", "accent2": "#71adFF", "name": "写意暗夜", "theme": "shuimo"},
    "shuimo_2": {"bg": "#f0f0f0", "accent1": "#71007f", "accent2": "#1a7F59", "name": "写意清新", "theme": "shuimo", "text_color": "#1a1a1a"},
    "shuimo_3": {"bg": "linear-gradient(135deg,#717180 0%,#71adff 100%)", "accent1": "#ffffff", "accent2": "#071aff", "name": "写意渐变", "theme": "shuimo", "is_gradient": True},
    "shuimo_4": {"bg": "#0071ad", "accent1": "#9f71ff", "accent2": "#071ad9", "name": "写意撞色", "theme": "shuimo", "text_color": "#ffffff"},
    "gongbi_1": {"bg": "#000503", "accent1": "#00ff00", "accent2": "#4065FF", "name": "工笔暗夜", "theme": "gongbi"},
    "gongbi_2": {"bg": "#f0f0f0", "accent1": "#40007f", "accent2": "#067F58", "name": "工笔清新", "theme": "gongbi", "text_color": "#1a1a1a"},
    "gongbi_3": {"bg": "linear-gradient(135deg,#404080 0%,#4065ff 100%)", "accent1": "#ffffff", "accent2": "#0406ff", "name": "工笔渐变", "theme": "gongbi", "is_gradient": True},
    "gongbi_4": {"bg": "#004065", "accent1": "#8340ff", "accent2": "#040658", "name": "工笔撞色", "theme": "gongbi", "text_color": "#ffffff"},
    "persian_1": {"bg": "#100302", "accent1": "#00ff00", "accent2": "#b023FF", "name": "波斯暗夜", "theme": "persian"},
    "persian_2": {"bg": "#f0f0f0", "accent1": "#30007f", "accent2": "#027F3e", "name": "波斯清新", "theme": "persian", "text_color": "#1a1a1a"},
    "persian_3": {"bg": "linear-gradient(135deg,#b0b080 0%,#b023ff 100%)", "accent1": "#ffffff", "accent2": "#0b02ff", "name": "波斯渐变", "theme": "persian", "is_gradient": True},
    "persian_4": {"bg": "#00b023", "accent1": "#e2b0ff", "accent2": "#0b023e", "name": "波斯撞色", "theme": "persian", "text_color": "#ffffff"},
    "arabesque_1": {"bg": "#1e1110", "accent1": "#00ff00", "accent2": "#3e71FF", "name": "阿拉伯暗夜", "theme": "arabesque"},
    "arabesque_2": {"bg": "#f0f0f0", "accent1": "#3e007f", "accent2": "#e77F17", "name": "阿拉伯清新", "theme": "arabesque", "text_color": "#1a1a1a"},
    "arabesque_3": {"bg": "linear-gradient(135deg,#3e3e80 0%,#3e71ff 100%)", "accent1": "#ffffff", "accent2": "#03e7ff", "name": "阿拉伯渐变", "theme": "arabesque", "is_gradient": True},
    "arabesque_4": {"bg": "#003e71", "accent1": "#703eff", "accent2": "#03e717", "name": "阿拉伯撞色", "theme": "arabesque", "text_color": "#ffffff"},
    "moroccan_1": {"bg": "#10111c", "accent1": "#00ff00", "accent2": "#d0b1FF", "name": "摩洛哥暗夜", "theme": "moroccan"},
    "moroccan_2": {"bg": "#f0f0f0", "accent1": "#50007f", "accent2": "#0b7F13", "name": "摩洛哥清新", "theme": "moroccan", "text_color": "#1a1a1a"},
    "moroccan_3": {"bg": "linear-gradient(135deg,#d0d080 0%,#d0b1ff 100%)", "accent1": "#ffffff", "accent2": "#0d0bff", "name": "摩洛哥渐变", "theme": "moroccan", "is_gradient": True},
    "moroccan_4": {"bg": "#00d0b1", "accent1": "#3cd0ff", "accent2": "#0d0b13", "name": "摩洛哥撞色", "theme": "moroccan", "text_color": "#ffffff"},
    "african_1": {"bg": "#041606", "accent1": "#00ff00", "accent2": "#64b6FF", "name": "非洲暗夜", "theme": "african"},
    "african_2": {"bg": "#f0f0f0", "accent1": "#64007f", "accent2": "#4b7F6c", "name": "非洲清新", "theme": "african", "text_color": "#1a1a1a"},
    "african_3": {"bg": "linear-gradient(135deg,#646480 0%,#64b6ff 100%)", "accent1": "#ffffff", "accent2": "#064bff", "name": "非洲渐变", "theme": "african", "is_gradient": True},
    "african_4": {"bg": "#0064b6", "accent1": "#c664ff", "accent2": "#064b6c", "name": "非洲撞色", "theme": "african", "text_color": "#ffffff"},
    "aztec_1": {"bg": "#1f070f", "accent1": "#00ff00", "accent2": "#7fe7FF", "name": "阿兹特克暗夜", "theme": "aztec"},
    "aztec_2": {"bg": "#f0f0f0", "accent1": "#7f007f", "accent2": "#fe7F7a", "name": "阿兹特克清新", "theme": "aztec", "text_color": "#1a1a1a"},
    "aztec_3": {"bg": "linear-gradient(135deg,#7f7f80 0%,#7fe7ff 100%)", "accent1": "#ffffff", "accent2": "#07feff", "name": "阿兹特克渐变", "theme": "aztec", "is_gradient": True},
    "aztec_4": {"bg": "#007fe7", "accent1": "#af7fff", "accent2": "#07fe7a", "name": "阿兹特克撞色", "theme": "aztec", "text_color": "#ffffff"},
    "maya_1": {"bg": "#071618", "accent1": "#00ff00", "accent2": "#8776FF", "name": "玛雅暗夜", "theme": "maya"},
    "maya_2": {"bg": "#f0f0f0", "accent1": "#07007f", "accent2": "#777F67", "name": "玛雅清新", "theme": "maya", "text_color": "#1a1a1a"},
    "maya_3": {"bg": "linear-gradient(135deg,#878780 0%,#8776ff 100%)", "accent1": "#ffffff", "accent2": "#0877ff", "name": "玛雅渐变", "theme": "maya", "is_gradient": True},
    "maya_4": {"bg": "#008776", "accent1": "#7887ff", "accent2": "#087767", "name": "玛雅撞色", "theme": "maya", "text_color": "#ffffff"},
    "inca_1": {"bg": "#030e1e", "accent1": "#00ff00", "accent2": "#23ceFF", "name": "印加暗夜", "theme": "inca"},
    "inca_2": {"bg": "#f0f0f0", "accent1": "#23007f", "accent2": "#3c7F67", "name": "印加清新", "theme": "inca", "text_color": "#1a1a1a"},
    "inca_3": {"bg": "linear-gradient(135deg,#232380 0%,#23ceff 100%)", "accent1": "#ffffff", "accent2": "#023cff", "name": "印加渐变", "theme": "inca", "is_gradient": True},
    "inca_4": {"bg": "#0023ce", "accent1": "#7e23ff", "accent2": "#023ce7", "name": "印加撞色", "theme": "inca", "text_color": "#ffffff"},
    "viking_1": {"bg": "#1f080b", "accent1": "#00ff00", "accent2": "#9fe8FF", "name": "维京暗夜", "theme": "viking"},
    "viking_2": {"bg": "#f0f0f0", "accent1": "#1f007f", "accent2": "#fe7F0e", "name": "维京清新", "theme": "viking", "text_color": "#1a1a1a"},
    "viking_3": {"bg": "linear-gradient(135deg,#9f9f80 0%,#9fe8ff 100%)", "accent1": "#ffffff", "accent2": "#09feff", "name": "维京渐变", "theme": "viking", "is_gradient": True},
    "viking_4": {"bg": "#009fe8", "accent1": "#eb9fff", "accent2": "#09fe8e", "name": "维京撞色", "theme": "viking", "text_color": "#ffffff"},
    "celtic_1": {"bg": "#1c0312", "accent1": "#00ff00", "accent2": "#7c23FF", "name": "凯尔特暗夜", "theme": "celtic"},
    "celtic_2": {"bg": "#f0f0f0", "accent1": "#7c007f", "accent2": "#c27F31", "name": "凯尔特清新", "theme": "celtic", "text_color": "#1a1a1a"},
    "celtic_3": {"bg": "linear-gradient(135deg,#7c7c80 0%,#7c23ff 100%)", "accent1": "#ffffff", "accent2": "#07c2ff", "name": "凯尔特渐变", "theme": "celtic", "is_gradient": True},
    "celtic_4": {"bg": "#007c23", "accent1": "#127cff", "accent2": "#07c231", "name": "凯尔特撞色", "theme": "celtic", "text_color": "#ffffff"},
    "egyptian_1": {"bg": "#110318", "accent1": "#00ff00", "accent2": "#f1a3FF", "name": "埃及暗夜", "theme": "egyptian"},
    "egyptian_2": {"bg": "#f0f0f0", "accent1": "#71007f", "accent2": "#1a7F39", "name": "埃及清新", "theme": "egyptian", "text_color": "#1a1a1a"},
    "egyptian_3": {"bg": "linear-gradient(135deg,#f1f180 0%,#f1a3ff 100%)", "accent1": "#ffffff", "accent2": "#0f1aff", "name": "埃及渐变", "theme": "egyptian", "is_gradient": True},
    "egyptian_4": {"bg": "#00f1a3", "accent1": "#98f1ff", "accent2": "#0f1a39", "name": "埃及撞色", "theme": "egyptian", "text_color": "#ffffff"},
    "greek_1": {"bg": "#011914", "accent1": "#00ff00", "accent2": "#01d9FF", "name": "希腊暗夜", "theme": "greek"},
    "greek_2": {"bg": "#f0f0f0", "accent1": "#01007f", "accent2": "#1d7F1b", "name": "希腊清新", "theme": "greek", "text_color": "#1a1a1a"},
    "greek_3": {"bg": "linear-gradient(135deg,#010180 0%,#01d9ff 100%)", "accent1": "#ffffff", "accent2": "#001dff", "name": "希腊渐变", "theme": "greek", "is_gradient": True},
    "greek_4": {"bg": "#0001d9", "accent1": "#b401ff", "accent2": "#001d9b", "name": "希腊撞色", "theme": "greek", "text_color": "#ffffff"},
    "roman_1": {"bg": "#061912", "accent1": "#00ff00", "accent2": "#66d9FF", "name": "罗马暗夜", "theme": "roman"},
    "roman_2": {"bg": "#f0f0f0", "accent1": "#66007f", "accent2": "#6d7F11", "name": "罗马清新", "theme": "roman", "text_color": "#1a1a1a"},
    "roman_3": {"bg": "linear-gradient(135deg,#666680 0%,#66d9ff 100%)", "accent1": "#ffffff", "accent2": "#066dff", "name": "罗马渐变", "theme": "roman", "is_gradient": True},
    "roman_4": {"bg": "#0066d9", "accent1": "#1266ff", "accent2": "#066d91", "name": "罗马撞色", "theme": "roman", "text_color": "#ffffff"},
    "byzantine_1": {"bg": "#10190e", "accent1": "#00ff00", "accent2": "#3019FF", "name": "拜占庭暗夜", "theme": "byzantine"},
    "byzantine_2": {"bg": "#f0f0f0", "accent1": "#30007f", "accent2": "#017F10", "name": "拜占庭清新", "theme": "byzantine", "text_color": "#1a1a1a"},
    "byzantine_3": {"bg": "linear-gradient(135deg,#303080 0%,#3019ff 100%)", "accent1": "#ffffff", "accent2": "#0301ff", "name": "拜占庭渐变", "theme": "byzantine", "is_gradient": True},
    "byzantine_4": {"bg": "#003019", "accent1": "#0e30ff", "accent2": "#030190", "name": "拜占庭撞色", "theme": "byzantine", "text_color": "#ffffff"},
    "russian_1": {"bg": "#1b0306", "accent1": "#00ff00", "accent2": "#7b23FF", "name": "俄罗斯暗夜", "theme": "russian"},
    "russian_2": {"bg": "#f0f0f0", "accent1": "#7b007f", "accent2": "#b27F3c", "name": "俄罗斯清新", "theme": "russian", "text_color": "#1a1a1a"},
    "russian_3": {"bg": "linear-gradient(135deg,#7b7b80 0%,#7b23ff 100%)", "accent1": "#ffffff", "accent2": "#07b2ff", "name": "俄罗斯渐变", "theme": "russian", "is_gradient": True},
    "russian_4": {"bg": "#007b23", "accent1": "#c67bff", "accent2": "#07b23c", "name": "俄罗斯撞色", "theme": "russian", "text_color": "#ffffff"},
    "tokyo_1": {"bg": "#0c1103", "accent1": "#00ff00", "accent2": "#8cb1FF", "name": "东京暗夜", "theme": "tokyo"},
    "tokyo_2": {"bg": "#f0f0f0", "accent1": "#0c007f", "accent2": "#cb7F12", "name": "东京清新", "theme": "tokyo", "text_color": "#1a1a1a"},
    "tokyo_3": {"bg": "linear-gradient(135deg,#8c8c80 0%,#8cb1ff 100%)", "accent1": "#ffffff", "accent2": "#08cbff", "name": "东京渐变", "theme": "tokyo", "is_gradient": True},
    "tokyo_4": {"bg": "#008cb1", "accent1": "#238cff", "accent2": "#08cb12", "name": "东京撞色", "theme": "tokyo", "text_color": "#ffffff"},
    "kyoto_1": {"bg": "#1d1e01", "accent1": "#00ff00", "accent2": "#3ddeFF", "name": "京都暗夜", "theme": "kyoto"},
    "kyoto_2": {"bg": "#f0f0f0", "accent1": "#3d007f", "accent2": "#dd7F66", "name": "京都清新", "theme": "kyoto", "text_color": "#1a1a1a"},
    "kyoto_3": {"bg": "linear-gradient(135deg,#3d3d80 0%,#3ddeff 100%)", "accent1": "#ffffff", "accent2": "#03ddff", "name": "京都渐变", "theme": "kyoto", "is_gradient": True},
    "kyoto_4": {"bg": "#003dde", "accent1": "#613dff", "accent2": "#03dde6", "name": "京都撞色", "theme": "kyoto", "text_color": "#ffffff"},
    "paris_1": {"bg": "#191d13", "accent1": "#00ff00", "accent2": "#b99dFF", "name": "巴黎暗夜", "theme": "paris"},
    "paris_2": {"bg": "#f0f0f0", "accent1": "#39007f", "accent2": "#997F5d", "name": "巴黎清新", "theme": "paris", "text_color": "#1a1a1a"},
    "paris_3": {"bg": "linear-gradient(135deg,#b9b980 0%,#b99dff 100%)", "accent1": "#ffffff", "accent2": "#0b99ff", "name": "巴黎渐变", "theme": "paris", "is_gradient": True},
    "paris_4": {"bg": "#00b99d", "accent1": "#d3b9ff", "accent2": "#0b99dd", "name": "巴黎撞色", "theme": "paris", "text_color": "#ffffff"},
    "london_1": {"bg": "#1b0812", "accent1": "#00ff00", "accent2": "#dbe8FF", "name": "伦敦暗夜", "theme": "london"},
    "london_2": {"bg": "#f0f0f0", "accent1": "#5b007f", "accent2": "#be7F0f", "name": "伦敦清新", "theme": "london", "text_color": "#1a1a1a"},
    "london_3": {"bg": "linear-gradient(135deg,#dbdb80 0%,#dbe8ff 100%)", "accent1": "#ffffff", "accent2": "#0dbeff", "name": "伦敦渐变", "theme": "london", "is_gradient": True},
    "london_4": {"bg": "#00dbe8", "accent1": "#f2dbff", "accent2": "#0dbe8f", "name": "伦敦撞色", "theme": "london", "text_color": "#ffffff"},
    "nyc_1": {"bg": "#01140a", "accent1": "#00ff00", "accent2": "#c1d4FF", "name": "纽约暗夜", "theme": "nyc"},
    "nyc_2": {"bg": "#f0f0f0", "accent1": "#41007f", "accent2": "#1d7F48", "name": "纽约清新", "theme": "nyc", "text_color": "#1a1a1a"},
    "nyc_3": {"bg": "linear-gradient(135deg,#c1c180 0%,#c1d4ff 100%)", "accent1": "#ffffff", "accent2": "#0c1dff", "name": "纽约渐变", "theme": "nyc", "is_gradient": True},
    "nyc_4": {"bg": "#00c1d4", "accent1": "#8ac1ff", "accent2": "#0c1d48", "name": "纽约撞色", "theme": "nyc", "text_color": "#ffffff"},
    "shanghai_1": {"bg": "#0f1300", "accent1": "#00ff00", "accent2": "#0f53FF", "name": "上海暗夜", "theme": "shanghai"},
    "shanghai_2": {"bg": "#f0f0f0", "accent1": "#0f007f", "accent2": "#f57F3a", "name": "上海清新", "theme": "shanghai", "text_color": "#1a1a1a"},
    "shanghai_3": {"bg": "linear-gradient(135deg,#0f0f80 0%,#0f53ff 100%)", "accent1": "#ffffff", "accent2": "#00f5ff", "name": "上海渐变", "theme": "shanghai", "is_gradient": True},
    "shanghai_4": {"bg": "#000f53", "accent1": "#a00fff", "accent2": "#00f53a", "name": "上海撞色", "theme": "shanghai", "text_color": "#ffffff"},
    "chengdu_1": {"bg": "#1c0e1b", "accent1": "#00ff00", "accent2": "#dc2eFF", "name": "成都暗夜", "theme": "chengdu"},
    "chengdu_2": {"bg": "#f0f0f0", "accent1": "#5c007f", "accent2": "#c27F6b", "name": "成都清新", "theme": "chengdu", "text_color": "#1a1a1a"},
    "chengdu_3": {"bg": "linear-gradient(135deg,#dcdc80 0%,#dc2eff 100%)", "accent1": "#ffffff", "accent2": "#0dc2ff", "name": "成都渐变", "theme": "chengdu", "is_gradient": True},
    "chengdu_4": {"bg": "#00dc2e", "accent1": "#bbdcff", "accent2": "#0dc2eb", "name": "成都撞色", "theme": "chengdu", "text_color": "#ffffff"},
    "yunnan_1": {"bg": "#031a04", "accent1": "#00ff00", "accent2": "#a35aFF", "name": "云南暗夜", "theme": "yunnan"},
    "yunnan_2": {"bg": "#f0f0f0", "accent1": "#23007f", "accent2": "#357F2c", "name": "云南清新", "theme": "yunnan", "text_color": "#1a1a1a"},
    "yunnan_3": {"bg": "linear-gradient(135deg,#a3a380 0%,#a35aff 100%)", "accent1": "#ffffff", "accent2": "#0a35ff", "name": "云南渐变", "theme": "yunnan", "is_gradient": True},
    "yunnan_4": {"bg": "#00a35a", "accent1": "#c4a3ff", "accent2": "#0a35ac", "name": "云南撞色", "theme": "yunnan", "text_color": "#ffffff"},
    "tibet_1": {"bg": "#020016", "accent1": "#00ff00", "accent2": "#8240FF", "name": "西藏暗夜", "theme": "tibet"},
    "tibet_2": {"bg": "#f0f0f0", "accent1": "#02007f", "accent2": "#247F03", "name": "西藏清新", "theme": "tibet", "text_color": "#1a1a1a"},
    "tibet_3": {"bg": "linear-gradient(135deg,#828280 0%,#8240ff 100%)", "accent1": "#ffffff", "accent2": "#0824ff", "name": "西藏渐变", "theme": "tibet", "is_gradient": True},
    "tibet_4": {"bg": "#008240", "accent1": "#3682ff", "accent2": "#082403", "name": "西藏撞色", "theme": "tibet", "text_color": "#ffffff"},
    "mongolia_1": {"bg": "#0c0c09", "accent1": "#00ff00", "accent2": "#acacFF", "name": "蒙古暗夜", "theme": "mongolia"},
    "mongolia_2": {"bg": "#f0f0f0", "accent1": "#2c007f", "accent2": "#ca7F46", "name": "蒙古清新", "theme": "mongolia", "text_color": "#1a1a1a"},
    "mongolia_3": {"bg": "linear-gradient(135deg,#acac80 0%,#acacff 100%)", "accent1": "#ffffff", "accent2": "#0acaff", "name": "蒙古渐变", "theme": "mongolia", "is_gradient": True},
    "mongolia_4": {"bg": "#00acac", "accent1": "#69acff", "accent2": "#0acac6", "name": "蒙古撞色", "theme": "mongolia", "text_color": "#ffffff"},
    "bamboo_1": {"bg": "#081e09", "accent1": "#00ff00", "accent2": "#489eFF", "name": "竹暗夜", "theme": "bamboo"},
    "bamboo_2": {"bg": "#f0f0f0", "accent1": "#48007f", "accent2": "#897F68", "name": "竹清新", "theme": "bamboo", "text_color": "#1a1a1a"},
    "bamboo_3": {"bg": "linear-gradient(135deg,#484880 0%,#489eff 100%)", "accent1": "#ffffff", "accent2": "#0489ff", "name": "竹渐变", "theme": "bamboo", "is_gradient": True},
    "bamboo_4": {"bg": "#00489e", "accent1": "#8948ff", "accent2": "#0489e8", "name": "竹撞色", "theme": "bamboo", "text_color": "#ffffff"},
    "lotus_1": {"bg": "#060111", "accent1": "#00ff00", "accent2": "#2681FF", "name": "莲花暗夜", "theme": "lotus"},
    "lotus_2": {"bg": "#f0f0f0", "accent1": "#26007f", "accent2": "#687F11", "name": "莲花清新", "theme": "lotus", "text_color": "#1a1a1a"},
    "lotus_3": {"bg": "linear-gradient(135deg,#262680 0%,#2681ff 100%)", "accent1": "#ffffff", "accent2": "#0268ff", "name": "莲花渐变", "theme": "lotus", "is_gradient": True},
    "lotus_4": {"bg": "#002681", "accent1": "#1126ff", "accent2": "#026811", "name": "莲花撞色", "theme": "lotus", "text_color": "#ffffff"},
    "plum_1": {"bg": "#1d0d19", "accent1": "#00ff00", "accent2": "#7dcdFF", "name": "梅花暗夜", "theme": "plum"},
    "plum_2": {"bg": "#f0f0f0", "accent1": "#7d007f", "accent2": "#dc7F53", "name": "梅花清新", "theme": "plum", "text_color": "#1a1a1a"},
    "plum_3": {"bg": "linear-gradient(135deg,#7d7d80 0%,#7dcdff 100%)", "accent1": "#ffffff", "accent2": "#07dcff", "name": "梅花渐变", "theme": "plum", "is_gradient": True},
    "plum_4": {"bg": "#007dcd", "accent1": "#397dff", "accent2": "#07dcd3", "name": "梅花撞色", "theme": "plum", "text_color": "#ffffff"},
    "orchid_1": {"bg": "#0c1706", "accent1": "#00ff00", "accent2": "#2c77FF", "name": "兰花暗夜", "theme": "orchid"},
    "orchid_2": {"bg": "#f0f0f0", "accent1": "#2c007f", "accent2": "#c77F78", "name": "兰花清新", "theme": "orchid", "text_color": "#1a1a1a"},
    "orchid_3": {"bg": "linear-gradient(135deg,#2c2c80 0%,#2c77ff 100%)", "accent1": "#ffffff", "accent2": "#02c7ff", "name": "兰花渐变", "theme": "orchid", "is_gradient": True},
    "orchid_4": {"bg": "#002c77", "accent1": "#862cff", "accent2": "#02c778", "name": "兰花撞色", "theme": "orchid", "text_color": "#ffffff"},
    "pine_1": {"bg": "#1f0d08", "accent1": "#00ff00", "accent2": "#7f6dFF", "name": "松暗夜", "theme": "pine"},
    "pine_2": {"bg": "#f0f0f0", "accent1": "#7f007f", "accent2": "#f67F5e", "name": "松清新", "theme": "pine", "text_color": "#1a1a1a"},
    "pine_3": {"bg": "linear-gradient(135deg,#7f7f80 0%,#7f6dff 100%)", "accent1": "#ffffff", "accent2": "#07f6ff", "name": "松渐变", "theme": "pine", "is_gradient": True},
    "pine_4": {"bg": "#007f6d", "accent1": "#e87fff", "accent2": "#07f6de", "name": "松撞色", "theme": "pine", "text_color": "#ffffff"},
    "maple_1": {"bg": "#17190d", "accent1": "#00ff00", "accent2": "#97d9FF", "name": "枫暗夜", "theme": "maple"},
    "maple_2": {"bg": "#f0f0f0", "accent1": "#17007f", "accent2": "#7d7F12", "name": "枫清新", "theme": "maple", "text_color": "#1a1a1a"},
    "maple_3": {"bg": "linear-gradient(135deg,#979780 0%,#97d9ff 100%)", "accent1": "#ffffff", "accent2": "#097dff", "name": "枫渐变", "theme": "maple", "is_gradient": True},
    "maple_4": {"bg": "#0097d9", "accent1": "#2d97ff", "accent2": "#097d92", "name": "枫撞色", "theme": "maple", "text_color": "#ffffff"},
    "willow_1": {"bg": "#070617", "accent1": "#00ff00", "accent2": "#c726FF", "name": "柳暗夜", "theme": "willow"},
    "willow_2": {"bg": "#f0f0f0", "accent1": "#47007f", "accent2": "#727F63", "name": "柳清新", "theme": "willow", "text_color": "#1a1a1a"},
    "willow_3": {"bg": "linear-gradient(135deg,#c7c780 0%,#c726ff 100%)", "accent1": "#ffffff", "accent2": "#0c72ff", "name": "柳渐变", "theme": "willow", "is_gradient": True},
    "willow_4": {"bg": "#00c726", "accent1": "#37c7ff", "accent2": "#0c7263", "name": "柳撞色", "theme": "willow", "text_color": "#ffffff"},
    "ginkgo_1": {"bg": "#050f1f", "accent1": "#00ff00", "accent2": "#058fFF", "name": "银杏暗夜", "theme": "ginkgo"},
    "ginkgo_2": {"bg": "#f0f0f0", "accent1": "#05007f", "accent2": "#587F77", "name": "银杏清新", "theme": "ginkgo", "text_color": "#1a1a1a"},
    "ginkgo_3": {"bg": "linear-gradient(135deg,#050580 0%,#058fff 100%)", "accent1": "#ffffff", "accent2": "#0058ff", "name": "银杏渐变", "theme": "ginkgo", "is_gradient": True},
    "ginkgo_4": {"bg": "#00058f", "accent1": "#7f05ff", "accent2": "#0058f7", "name": "银杏撞色", "theme": "ginkgo", "text_color": "#ffffff"},
    "cactus_1": {"bg": "#05161d", "accent1": "#00ff00", "accent2": "#e556FF", "name": "仙人掌暗夜", "theme": "cactus"},
    "cactus_2": {"bg": "#f0f0f0", "accent1": "#65007f", "accent2": "#557F69", "name": "仙人掌清新", "theme": "cactus", "text_color": "#1a1a1a"},
    "cactus_3": {"bg": "linear-gradient(135deg,#e5e580 0%,#e556ff 100%)", "accent1": "#ffffff", "accent2": "#0e55ff", "name": "仙人掌渐变", "theme": "cactus", "is_gradient": True},
    "cactus_4": {"bg": "#00e556", "accent1": "#9de5ff", "accent2": "#0e5569", "name": "仙人掌撞色", "theme": "cactus", "text_color": "#ffffff"},
    "bonsai_1": {"bg": "#05090c", "accent1": "#00ff00", "accent2": "#a5e9FF", "name": "盆景暗夜", "theme": "bonsai"},
    "bonsai_2": {"bg": "#f0f0f0", "accent1": "#25007f", "accent2": "#5e7F1a", "name": "盆景清新", "theme": "bonsai", "text_color": "#1a1a1a"},
    "bonsai_3": {"bg": "linear-gradient(135deg,#a5a580 0%,#a5e9ff 100%)", "accent1": "#ffffff", "accent2": "#0a5eff", "name": "盆景渐变", "theme": "bonsai", "is_gradient": True},
    "bonsai_4": {"bg": "#00a5e9", "accent1": "#aca5ff", "accent2": "#0a5e9a", "name": "盆景撞色", "theme": "bonsai", "text_color": "#ffffff"},
    "moss_1": {"bg": "#1f0316", "accent1": "#00ff00", "accent2": "#ff03FF", "name": "苔藓暗夜", "theme": "moss"},
    "moss_2": {"bg": "#f0f0f0", "accent1": "#7f007f", "accent2": "#f07F33", "name": "苔藓清新", "theme": "moss", "text_color": "#1a1a1a"},
    "moss_3": {"bg": "linear-gradient(135deg,#ffff80 0%,#ff03ff 100%)", "accent1": "#ffffff", "accent2": "#0ff0ff", "name": "苔藓渐变", "theme": "moss", "is_gradient": True},
    "moss_4": {"bg": "#00ff03", "accent1": "#36ffff", "accent2": "#0ff033", "name": "苔藓撞色", "theme": "moss", "text_color": "#ffffff"},
    "dandelion_1": {"bg": "#020703", "accent1": "#00ff00", "accent2": "#c2a7FF", "name": "蒲公英暗夜", "theme": "dandelion"},
    "dandelion_2": {"bg": "#f0f0f0", "accent1": "#42007f", "accent2": "#2a7F76", "name": "蒲公英清新", "theme": "dandelion", "text_color": "#1a1a1a"},
    "dandelion_3": {"bg": "linear-gradient(135deg,#c2c280 0%,#c2a7ff 100%)", "accent1": "#ffffff", "accent2": "#0c2aff", "name": "蒲公英渐变", "theme": "dandelion", "is_gradient": True},
    "dandelion_4": {"bg": "#00c2a7", "accent1": "#63c2ff", "accent2": "#0c2a76", "name": "蒲公英撞色", "theme": "dandelion", "text_color": "#ffffff"},
    "lavender_1": {"bg": "#020a17", "accent1": "#00ff00", "accent2": "#024aFF", "name": "薰衣草暗夜", "theme": "lavender"},
    "lavender_2": {"bg": "#f0f0f0", "accent1": "#02007f", "accent2": "#247F27", "name": "薰衣草清新", "theme": "lavender", "text_color": "#1a1a1a"},
    "lavender_3": {"bg": "linear-gradient(135deg,#020280 0%,#024aff 100%)", "accent1": "#ffffff", "accent2": "#0024ff", "name": "薰衣草渐变", "theme": "lavender", "is_gradient": True},
    "lavender_4": {"bg": "#00024a", "accent1": "#7702ff", "accent2": "#0024a7", "name": "薰衣草撞色", "theme": "lavender", "text_color": "#ffffff"},
    "sunflower_1": {"bg": "#1d0d0c", "accent1": "#00ff00", "accent2": "#ddcdFF", "name": "向日葵暗夜", "theme": "sunflower"},
    "sunflower_2": {"bg": "#f0f0f0", "accent1": "#5d007f", "accent2": "#dc7F5e", "name": "向日葵清新", "theme": "sunflower", "text_color": "#1a1a1a"},
    "sunflower_3": {"bg": "linear-gradient(135deg,#dddd80 0%,#ddcdff 100%)", "accent1": "#ffffff", "accent2": "#0ddcff", "name": "向日葵渐变", "theme": "sunflower", "is_gradient": True},
    "sunflower_4": {"bg": "#00ddcd", "accent1": "#ecddff", "accent2": "#0ddcde", "name": "向日葵撞色", "theme": "sunflower", "text_color": "#ffffff"},
    "rose_1": {"bg": "#161900", "accent1": "#00ff00", "accent2": "#d659FF", "name": "玫瑰暗夜", "theme": "rose"},
    "rose_2": {"bg": "#f0f0f0", "accent1": "#56007f", "accent2": "#657F16", "name": "玫瑰清新", "theme": "rose", "text_color": "#1a1a1a"},
    "rose_3": {"bg": "linear-gradient(135deg,#d6d680 0%,#d659ff 100%)", "accent1": "#ffffff", "accent2": "#0d65ff", "name": "玫瑰渐变", "theme": "rose", "is_gradient": True},
    "rose_4": {"bg": "#00d659", "accent1": "#60d6ff", "accent2": "#0d6596", "name": "玫瑰撞色", "theme": "rose", "text_color": "#ffffff"},
    "tulip_1": {"bg": "#1b1909", "accent1": "#00ff00", "accent2": "#db59FF", "name": "郁金香暗夜", "theme": "tulip"},
    "tulip_2": {"bg": "#f0f0f0", "accent1": "#5b007f", "accent2": "#b57F1a", "name": "郁金香清新", "theme": "tulip", "text_color": "#1a1a1a"},
    "tulip_3": {"bg": "linear-gradient(135deg,#dbdb80 0%,#db59ff 100%)", "accent1": "#ffffff", "accent2": "#0db5ff", "name": "郁金香渐变", "theme": "tulip", "is_gradient": True},
    "tulip_4": {"bg": "#00db59", "accent1": "#a9dbff", "accent2": "#0db59a", "name": "郁金香撞色", "theme": "tulip", "text_color": "#ffffff"},
    "summer_1": {"bg": "#1d0e0f", "accent1": "#00ff00", "accent2": "#3d2eFF", "name": "夏暗夜", "theme": "summer"},
    "summer_2": {"bg": "#f0f0f0", "accent1": "#3d007f", "accent2": "#d27F60", "name": "夏清新", "theme": "summer", "text_color": "#1a1a1a"},
    "summer_3": {"bg": "linear-gradient(135deg,#3d3d80 0%,#3d2eff 100%)", "accent1": "#ffffff", "accent2": "#03d2ff", "name": "夏渐变", "theme": "summer", "is_gradient": True},
    "summer_4": {"bg": "#003d2e", "accent1": "#0f3dff", "accent2": "#03d2e0", "name": "夏撞色", "theme": "summer", "text_color": "#ffffff"},
    "autumn_1": {"bg": "#0e0a0f", "accent1": "#00ff00", "accent2": "#8e0aFF", "name": "秋暗夜", "theme": "autumn"},
    "autumn_2": {"bg": "#f0f0f0", "accent1": "#0e007f", "accent2": "#e07F20", "name": "秋清新", "theme": "autumn", "text_color": "#1a1a1a"},
    "autumn_3": {"bg": "linear-gradient(135deg,#8e8e80 0%,#8e0aff 100%)", "accent1": "#ffffff", "accent2": "#08e0ff", "name": "秋渐变", "theme": "autumn", "is_gradient": True},
    "autumn_4": {"bg": "#008e0a", "accent1": "#0f8eff", "accent2": "#08e0a0", "name": "秋撞色", "theme": "autumn", "text_color": "#ffffff"},
    "winter_1": {"bg": "#0c1e02", "accent1": "#00ff00", "accent2": "#ec9eFF", "name": "冬暗夜", "theme": "winter"},
    "winter_2": {"bg": "#f0f0f0", "accent1": "#6c007f", "accent2": "#c97F6e", "name": "冬清新", "theme": "winter", "text_color": "#1a1a1a"},
    "winter_3": {"bg": "linear-gradient(135deg,#ecec80 0%,#ec9eff 100%)", "accent1": "#ffffff", "accent2": "#0ec9ff", "name": "冬渐变", "theme": "winter", "is_gradient": True},
    "winter_4": {"bg": "#00ec9e", "accent1": "#e2ecff", "accent2": "#0ec9ee", "name": "冬撞色", "theme": "winter", "text_color": "#ffffff"},
    "snow2_1": {"bg": "#071106", "accent1": "#00ff00", "accent2": "#c7f1FF", "name": "雪暗夜", "theme": "snow2"},
    "snow2_2": {"bg": "#f0f0f0", "accent1": "#47007f", "accent2": "#7f7F16", "name": "雪清新", "theme": "snow2", "text_color": "#1a1a1a"},
    "snow2_3": {"bg": "linear-gradient(135deg,#c7c780 0%,#c7f1ff 100%)", "accent1": "#ffffff", "accent2": "#0c7fff", "name": "雪渐变", "theme": "snow2", "is_gradient": True},
    "snow2_4": {"bg": "#00c7f1", "accent1": "#66c7ff", "accent2": "#0c7f16", "name": "雪撞色", "theme": "snow2", "text_color": "#ffffff"},
    "fog_1": {"bg": "#090001", "accent1": "#00ff00", "accent2": "#c9c0FF", "name": "雾暗夜", "theme": "fog"},
    "fog_2": {"bg": "#f0f0f0", "accent1": "#49007f", "accent2": "#9c7F04", "name": "雾清新", "theme": "fog", "text_color": "#1a1a1a"},
    "fog_3": {"bg": "linear-gradient(135deg,#c9c980 0%,#c9c0ff 100%)", "accent1": "#ffffff", "accent2": "#0c9cff", "name": "雾渐变", "theme": "fog", "is_gradient": True},
    "fog_4": {"bg": "#00c9c0", "accent1": "#41c9ff", "accent2": "#0c9c04", "name": "雾撞色", "theme": "fog", "text_color": "#ffffff"},
    "drizzle_1": {"bg": "#13010c", "accent1": "#00ff00", "accent2": "#1341FF", "name": "细雨暗夜", "theme": "drizzle"},
    "drizzle_2": {"bg": "#f0f0f0", "accent1": "#13007f", "accent2": "#347F14", "name": "细雨清新", "theme": "drizzle", "text_color": "#1a1a1a"},
    "drizzle_3": {"bg": "linear-gradient(135deg,#131380 0%,#1341ff 100%)", "accent1": "#ffffff", "accent2": "#0134ff", "name": "细雨渐变", "theme": "drizzle", "is_gradient": True},
    "drizzle_4": {"bg": "#001341", "accent1": "#4c13ff", "accent2": "#013414", "name": "细雨撞色", "theme": "drizzle", "text_color": "#ffffff"},
    "dawn_1": {"bg": "#160e1d", "accent1": "#00ff00", "accent2": "#36eeFF", "name": "黎明暗夜", "theme": "dawn"},
    "dawn_2": {"bg": "#f0f0f0", "accent1": "#36007f", "accent2": "#6e7F6d", "name": "黎明清新", "theme": "dawn", "text_color": "#1a1a1a"},
    "dawn_3": {"bg": "linear-gradient(135deg,#363680 0%,#36eeff 100%)", "accent1": "#ffffff", "accent2": "#036eff", "name": "黎明渐变", "theme": "dawn", "is_gradient": True},
    "dawn_4": {"bg": "#0036ee", "accent1": "#dd36ff", "accent2": "#036eed", "name": "黎明撞色", "theme": "dawn", "text_color": "#ffffff"},
    "dusk_1": {"bg": "#1c0313", "accent1": "#00ff00", "accent2": "#9cc3FF", "name": "黄昏暗夜", "theme": "dusk"},
    "dusk_2": {"bg": "#f0f0f0", "accent1": "#1c007f", "accent2": "#cc7F3d", "name": "黄昏清新", "theme": "dusk", "text_color": "#1a1a1a"},
    "dusk_3": {"bg": "linear-gradient(135deg,#9c9c80 0%,#9cc3ff 100%)", "accent1": "#ffffff", "accent2": "#09ccff", "name": "黄昏渐变", "theme": "dusk", "is_gradient": True},
    "dusk_4": {"bg": "#009cc3", "accent1": "#d39cff", "accent2": "#09cc3d", "name": "黄昏撞色", "theme": "dusk", "text_color": "#ffffff"},
    "moonlight_1": {"bg": "#03131e", "accent1": "#00ff00", "accent2": "#8393FF", "name": "月光暗夜", "theme": "moonlight"},
    "moonlight_2": {"bg": "#f0f0f0", "accent1": "#03007f", "accent2": "#397F31", "name": "月光清新", "theme": "moonlight", "text_color": "#1a1a1a"},
    "moonlight_3": {"bg": "linear-gradient(135deg,#838380 0%,#8393ff 100%)", "accent1": "#ffffff", "accent2": "#0839ff", "name": "月光渐变", "theme": "moonlight", "is_gradient": True},
    "moonlight_4": {"bg": "#008393", "accent1": "#1e83ff", "accent2": "#083931", "name": "月光撞色", "theme": "moonlight", "text_color": "#ffffff"},
    "starlight_1": {"bg": "#110218", "accent1": "#00ff00", "accent2": "#9122FF", "name": "星光暗夜", "theme": "starlight"},
    "starlight_2": {"bg": "#f0f0f0", "accent1": "#11007f", "accent2": "#127F21", "name": "星光清新", "theme": "starlight", "text_color": "#1a1a1a"},
    "starlight_3": {"bg": "linear-gradient(135deg,#919180 0%,#9122ff 100%)", "accent1": "#ffffff", "accent2": "#0912ff", "name": "星光渐变", "theme": "starlight", "is_gradient": True},
    "starlight_4": {"bg": "#009122", "accent1": "#1891ff", "accent2": "#091221", "name": "星光撞色", "theme": "starlight", "text_color": "#ffffff"},
    "mountain_1": {"bg": "#080b10", "accent1": "#00ff00", "accent2": "#680bFF", "name": "山暗夜", "theme": "mountain"},
    "mountain_2": {"bg": "#f0f0f0", "accent1": "#68007f", "accent2": "#807F3b", "name": "山清新", "theme": "mountain", "text_color": "#1a1a1a"},
    "mountain_3": {"bg": "linear-gradient(135deg,#686880 0%,#680bff 100%)", "accent1": "#ffffff", "accent2": "#0680ff", "name": "山渐变", "theme": "mountain", "is_gradient": True},
    "mountain_4": {"bg": "#00680b", "accent1": "#b068ff", "accent2": "#0680bb", "name": "山撞色", "theme": "mountain", "text_color": "#ffffff"},
    "valley_1": {"bg": "#19021b", "accent1": "#00ff00", "accent2": "#f922FF", "name": "山谷暗夜", "theme": "valley"},
    "valley_2": {"bg": "#f0f0f0", "accent1": "#79007f", "accent2": "#927F2f", "name": "山谷清新", "theme": "valley", "text_color": "#1a1a1a"},
    "valley_3": {"bg": "linear-gradient(135deg,#f9f980 0%,#f922ff 100%)", "accent1": "#ffffff", "accent2": "#0f92ff", "name": "山谷渐变", "theme": "valley", "is_gradient": True},
    "valley_4": {"bg": "#00f922", "accent1": "#fbf9ff", "accent2": "#0f922f", "name": "山谷撞色", "theme": "valley", "text_color": "#ffffff"},
    "island_1": {"bg": "#1a1811", "accent1": "#00ff00", "accent2": "#7a78FF", "name": "岛屿暗夜", "theme": "island"},
    "island_2": {"bg": "#f0f0f0", "accent1": "#7a007f", "accent2": "#a77F01", "name": "岛屿清新", "theme": "island", "text_color": "#1a1a1a"},
    "island_3": {"bg": "linear-gradient(135deg,#7a7a80 0%,#7a78ff 100%)", "accent1": "#ffffff", "accent2": "#07a7ff", "name": "岛屿渐变", "theme": "island", "is_gradient": True},
    "island_4": {"bg": "#007a78", "accent1": "#117aff", "accent2": "#07a781", "name": "岛屿撞色", "theme": "island", "text_color": "#ffffff"},
    "harbor_1": {"bg": "#111f10", "accent1": "#00ff00", "accent2": "#d1ffFF", "name": "港口暗夜", "theme": "harbor"},
    "harbor_2": {"bg": "#f0f0f0", "accent1": "#51007f", "accent2": "#1f7F79", "name": "港口清新", "theme": "harbor", "text_color": "#1a1a1a"},
    "harbor_3": {"bg": "linear-gradient(135deg,#d1d180 0%,#d1ffff 100%)", "accent1": "#ffffff", "accent2": "#0d1fff", "name": "港口渐变", "theme": "harbor", "is_gradient": True},
    "harbor_4": {"bg": "#00d1ff", "accent1": "#90d1ff", "accent2": "#0d1ff9", "name": "港口撞色", "theme": "harbor", "text_color": "#ffffff"},
    "lighthouse_1": {"bg": "#1e0012", "accent1": "#00ff00", "accent2": "#1ec0FF", "name": "灯塔暗夜", "theme": "lighthouse"},
    "lighthouse_2": {"bg": "#f0f0f0", "accent1": "#1e007f", "accent2": "#ec7F0b", "name": "灯塔清新", "theme": "lighthouse", "text_color": "#1a1a1a"},
    "lighthouse_3": {"bg": "linear-gradient(135deg,#1e1e80 0%,#1ec0ff 100%)", "accent1": "#ffffff", "accent2": "#01ecff", "name": "灯塔渐变", "theme": "lighthouse", "is_gradient": True},
    "lighthouse_4": {"bg": "#001ec0", "accent1": "#b21eff", "accent2": "#01ec0b", "name": "灯塔撞色", "theme": "lighthouse", "text_color": "#ffffff"},
    "bridge_1": {"bg": "#091613", "accent1": "#00ff00", "accent2": "#2936FF", "name": "桥暗夜", "theme": "bridge"},
    "bridge_2": {"bg": "#f0f0f0", "accent1": "#29007f", "accent2": "#937F67", "name": "桥清新", "theme": "bridge", "text_color": "#1a1a1a"},
    "bridge_3": {"bg": "linear-gradient(135deg,#292980 0%,#2936ff 100%)", "accent1": "#ffffff", "accent2": "#0293ff", "name": "桥渐变", "theme": "bridge", "is_gradient": True},
    "bridge_4": {"bg": "#002936", "accent1": "#7329ff", "accent2": "#029367", "name": "桥撞色", "theme": "bridge", "text_color": "#ffffff"},
    "windmill_1": {"bg": "#191018", "accent1": "#00ff00", "accent2": "#f9b0FF", "name": "风车暗夜", "theme": "windmill"},
    "windmill_2": {"bg": "#f0f0f0", "accent1": "#79007f", "accent2": "#9b7F09", "name": "风车清新", "theme": "windmill", "text_color": "#1a1a1a"},
    "windmill_3": {"bg": "linear-gradient(135deg,#f9f980 0%,#f9b0ff 100%)", "accent1": "#ffffff", "accent2": "#0f9bff", "name": "风车渐变", "theme": "windmill", "is_gradient": True},
    "windmill_4": {"bg": "#00f9b0", "accent1": "#98f9ff", "accent2": "#0f9b09", "name": "风车撞色", "theme": "windmill", "text_color": "#ffffff"},
    "cabin_1": {"bg": "#1f0c19", "accent1": "#00ff00", "accent2": "#df6cFF", "name": "小屋暗夜", "theme": "cabin"},
    "cabin_2": {"bg": "#f0f0f0", "accent1": "#5f007f", "accent2": "#f67F49", "name": "小屋清新", "theme": "cabin", "text_color": "#1a1a1a"},
    "cabin_3": {"bg": "linear-gradient(135deg,#dfdf80 0%,#df6cff 100%)", "accent1": "#ffffff", "accent2": "#0df6ff", "name": "小屋渐变", "theme": "cabin", "is_gradient": True},
    "cabin_4": {"bg": "#00df6c", "accent1": "#99dfff", "accent2": "#0df6c9", "name": "小屋撞色", "theme": "cabin", "text_color": "#ffffff"},
    "temple_1": {"bg": "#1e151c", "accent1": "#00ff00", "accent2": "#fe55FF", "name": "寺庙暗夜", "theme": "temple"},
    "temple_2": {"bg": "#f0f0f0", "accent1": "#7e007f", "accent2": "#e57F57", "name": "寺庙清新", "theme": "temple", "text_color": "#1a1a1a"},
    "temple_3": {"bg": "linear-gradient(135deg,#fefe80 0%,#fe55ff 100%)", "accent1": "#ffffff", "accent2": "#0fe5ff", "name": "寺庙渐变", "theme": "temple", "is_gradient": True},
    "temple_4": {"bg": "#00fe55", "accent1": "#7cfeff", "accent2": "#0fe557", "name": "寺庙撞色", "theme": "temple", "text_color": "#ffffff"},
    "castle_1": {"bg": "#01091b", "accent1": "#00ff00", "accent2": "#21c9FF", "name": "城堡暗夜", "theme": "castle"},
    "castle_2": {"bg": "#f0f0f0", "accent1": "#21007f", "accent2": "#1c7F15", "name": "城堡清新", "theme": "castle", "text_color": "#1a1a1a"},
    "castle_3": {"bg": "linear-gradient(135deg,#212180 0%,#21c9ff 100%)", "accent1": "#ffffff", "accent2": "#021cff", "name": "城堡渐变", "theme": "castle", "is_gradient": True},
    "castle_4": {"bg": "#0021c9", "accent1": "#5b21ff", "accent2": "#021c95", "name": "城堡撞色", "theme": "castle", "text_color": "#ffffff"},
    "poetry_1": {"bg": "#120513", "accent1": "#00ff00", "accent2": "#f265FF", "name": "诗歌暗夜", "theme": "poetry"},
    "poetry_2": {"bg": "#f0f0f0", "accent1": "#72007f", "accent2": "#267F59", "name": "诗歌清新", "theme": "poetry", "text_color": "#1a1a1a"},
    "poetry_3": {"bg": "linear-gradient(135deg,#f2f280 0%,#f265ff 100%)", "accent1": "#ffffff", "accent2": "#0f26ff", "name": "诗歌渐变", "theme": "poetry", "is_gradient": True},
    "poetry_4": {"bg": "#00f265", "accent1": "#93f2ff", "accent2": "#0f2659", "name": "诗歌撞色", "theme": "poetry", "text_color": "#ffffff"},
    "novel_1": {"bg": "#0d0215", "accent1": "#00ff00", "accent2": "#4de2FF", "name": "小说暗夜", "theme": "novel"},
    "novel_2": {"bg": "#f0f0f0", "accent1": "#4d007f", "accent2": "#de7F27", "name": "小说清新", "theme": "novel", "text_color": "#1a1a1a"},
    "novel_3": {"bg": "linear-gradient(135deg,#4d4d80 0%,#4de2ff 100%)", "accent1": "#ffffff", "accent2": "#04deff", "name": "小说渐变", "theme": "novel", "is_gradient": True},
    "novel_4": {"bg": "#004de2", "accent1": "#754dff", "accent2": "#04de27", "name": "小说撞色", "theme": "novel", "text_color": "#ffffff"},
    "fairytale_1": {"bg": "#17120a", "accent1": "#00ff00", "accent2": "#7772FF", "name": "童话暗夜", "theme": "fairytale"},
    "fairytale_2": {"bg": "#f0f0f0", "accent1": "#77007f", "accent2": "#777F26", "name": "童话清新", "theme": "fairytale", "text_color": "#1a1a1a"},
    "fairytale_3": {"bg": "linear-gradient(135deg,#777780 0%,#7772ff 100%)", "accent1": "#ffffff", "accent2": "#0777ff", "name": "童话渐变", "theme": "fairytale", "is_gradient": True},
    "fairytale_4": {"bg": "#007772", "accent1": "#6a77ff", "accent2": "#077726", "name": "童话撞色", "theme": "fairytale", "text_color": "#ffffff"},
    "myth_1": {"bg": "#1d0214", "accent1": "#00ff00", "accent2": "#1d62FF", "name": "神话暗夜", "theme": "myth"},
    "myth_2": {"bg": "#f0f0f0", "accent1": "#1d007f", "accent2": "#d67F2b", "name": "神话清新", "theme": "myth", "text_color": "#1a1a1a"},
    "myth_3": {"bg": "linear-gradient(135deg,#1d1d80 0%,#1d62ff 100%)", "accent1": "#ffffff", "accent2": "#01d6ff", "name": "神话渐变", "theme": "myth", "is_gradient": True},
    "myth_4": {"bg": "#001d62", "accent1": "#b41dff", "accent2": "#01d62b", "name": "神话撞色", "theme": "myth", "text_color": "#ffffff"},
    "haiku_1": {"bg": "#1c1b08", "accent1": "#00ff00", "accent2": "#7c1bFF", "name": "俳句暗夜", "theme": "haiku"},
    "haiku_2": {"bg": "#f0f0f0", "accent1": "#7c007f", "accent2": "#c17F30", "name": "俳句清新", "theme": "haiku", "text_color": "#1a1a1a"},
    "haiku_3": {"bg": "linear-gradient(135deg,#7c7c80 0%,#7c1bff 100%)", "accent1": "#ffffff", "accent2": "#07c1ff", "name": "俳句渐变", "theme": "haiku", "is_gradient": True},
    "haiku_4": {"bg": "#007c1b", "accent1": "#087cff", "accent2": "#07c1b0", "name": "俳句撞色", "theme": "haiku", "text_color": "#ffffff"},
    "ceramic_1": {"bg": "#120211", "accent1": "#00ff00", "accent2": "#1282FF", "name": "陶瓷暗夜", "theme": "ceramic"},
    "ceramic_2": {"bg": "#f0f0f0", "accent1": "#12007f", "accent2": "#287F29", "name": "陶瓷清新", "theme": "ceramic", "text_color": "#1a1a1a"},
    "ceramic_3": {"bg": "linear-gradient(135deg,#121280 0%,#1282ff 100%)", "accent1": "#ffffff", "accent2": "#0128ff", "name": "陶瓷渐变", "theme": "ceramic", "is_gradient": True},
    "ceramic_4": {"bg": "#001282", "accent1": "#9112ff", "accent2": "#012829", "name": "陶瓷撞色", "theme": "ceramic", "text_color": "#ffffff"},
    "pottery_1": {"bg": "#151a0a", "accent1": "#00ff00", "accent2": "#f55aFF", "name": "陶器暗夜", "theme": "pottery"},
    "pottery_2": {"bg": "#f0f0f0", "accent1": "#75007f", "accent2": "#557F2c", "name": "陶器清新", "theme": "pottery", "text_color": "#1a1a1a"},
    "pottery_3": {"bg": "linear-gradient(135deg,#f5f580 0%,#f55aff 100%)", "accent1": "#ffffff", "accent2": "#0f55ff", "name": "陶器渐变", "theme": "pottery", "is_gradient": True},
    "pottery_4": {"bg": "#00f55a", "accent1": "#caf5ff", "accent2": "#0f55ac", "name": "陶器撞色", "theme": "pottery", "text_color": "#ffffff"},
    "porcelain_1": {"bg": "#071f01", "accent1": "#00ff00", "accent2": "#e7dfFF", "name": "瓷器暗夜", "theme": "porcelain"},
    "porcelain_2": {"bg": "#f0f0f0", "accent1": "#67007f", "accent2": "#7d7F78", "name": "瓷器清新", "theme": "porcelain", "text_color": "#1a1a1a"},
    "porcelain_3": {"bg": "linear-gradient(135deg,#e7e780 0%,#e7dfff 100%)", "accent1": "#ffffff", "accent2": "#0e7dff", "name": "瓷器渐变", "theme": "porcelain", "is_gradient": True},
    "porcelain_4": {"bg": "#00e7df", "accent1": "#81e7ff", "accent2": "#0e7df8", "name": "瓷器撞色", "theme": "porcelain", "text_color": "#ffffff"},
    "lacquer_1": {"bg": "#191c0b", "accent1": "#00ff00", "accent2": "#79bcFF", "name": "漆器暗夜", "theme": "lacquer"},
    "lacquer_2": {"bg": "#f0f0f0", "accent1": "#79007f", "accent2": "#9b7F42", "name": "漆器清新", "theme": "lacquer", "text_color": "#1a1a1a"},
    "lacquer_3": {"bg": "linear-gradient(135deg,#797980 0%,#79bcff 100%)", "accent1": "#ffffff", "accent2": "#079bff", "name": "漆器渐变", "theme": "lacquer", "is_gradient": True},
    "lacquer_4": {"bg": "#0079bc", "accent1": "#2b79ff", "accent2": "#079bc2", "name": "漆器撞色", "theme": "lacquer", "text_color": "#ffffff"},
    "weaving_1": {"bg": "#1c1b05", "accent1": "#00ff00", "accent2": "#3cdbFF", "name": "编织暗夜", "theme": "weaving"},
    "weaving_2": {"bg": "#f0f0f0", "accent1": "#3c007f", "accent2": "#cd7F3e", "name": "编织清新", "theme": "weaving", "text_color": "#1a1a1a"},
    "weaving_3": {"bg": "linear-gradient(135deg,#3c3c80 0%,#3cdbff 100%)", "accent1": "#ffffff", "accent2": "#03cdff", "name": "编织渐变", "theme": "weaving", "is_gradient": True},
    "weaving_4": {"bg": "#003cdb", "accent1": "#e53cff", "accent2": "#03cdbe", "name": "编织撞色", "theme": "weaving", "text_color": "#ffffff"},
    "dyeing_1": {"bg": "#110706", "accent1": "#00ff00", "accent2": "#1107FF", "name": "扎染暗夜", "theme": "dyeing"},
    "dyeing_2": {"bg": "#f0f0f0", "accent1": "#11007f", "accent2": "#107F7e", "name": "扎染清新", "theme": "dyeing", "text_color": "#1a1a1a"},
    "dyeing_3": {"bg": "linear-gradient(135deg,#111180 0%,#1107ff 100%)", "accent1": "#ffffff", "accent2": "#0110ff", "name": "扎染渐变", "theme": "dyeing", "is_gradient": True},
    "dyeing_4": {"bg": "#001107", "accent1": "#e611ff", "accent2": "#01107e", "name": "扎染撞色", "theme": "dyeing", "text_color": "#ffffff"},
    "calligraphy_1": {"bg": "#0c150f", "accent1": "#00ff00", "accent2": "#2c55FF", "name": "书法暗夜", "theme": "calligraphy"},
    "calligraphy_2": {"bg": "#f0f0f0", "accent1": "#2c007f", "accent2": "#c57F5e", "name": "书法清新", "theme": "calligraphy", "text_color": "#1a1a1a"},
    "calligraphy_3": {"bg": "linear-gradient(135deg,#2c2c80 0%,#2c55ff 100%)", "accent1": "#ffffff", "accent2": "#02c5ff", "name": "书法渐变", "theme": "calligraphy", "is_gradient": True},
    "calligraphy_4": {"bg": "#002c55", "accent1": "#ef2cff", "accent2": "#02c55e", "name": "书法撞色", "theme": "calligraphy", "text_color": "#ffffff"},
    "seal2_1": {"bg": "#040b08", "accent1": "#00ff00", "accent2": "#e40bFF", "name": "篆刻暗夜", "theme": "seal2"},
    "seal2_2": {"bg": "#f0f0f0", "accent1": "#64007f", "accent2": "#407F36", "name": "篆刻清新", "theme": "seal2", "text_color": "#1a1a1a"},
    "seal2_3": {"bg": "linear-gradient(135deg,#e4e480 0%,#e40bff 100%)", "accent1": "#ffffff", "accent2": "#0e40ff", "name": "篆刻渐变", "theme": "seal2", "is_gradient": True},
    "seal2_4": {"bg": "#00e40b", "accent1": "#68e4ff", "accent2": "#0e40b6", "name": "篆刻撞色", "theme": "seal2", "text_color": "#ffffff"},
    "wood_1": {"bg": "#18081f", "accent1": "#00ff00", "accent2": "#78a8FF", "name": "木纹暗夜", "theme": "wood"},
    "wood_2": {"bg": "#f0f0f0", "accent1": "#78007f", "accent2": "#8a7F03", "name": "木纹清新", "theme": "wood", "text_color": "#1a1a1a"},
    "wood_3": {"bg": "linear-gradient(135deg,#787880 0%,#78a8ff 100%)", "accent1": "#ffffff", "accent2": "#078aff", "name": "木纹渐变", "theme": "wood", "is_gradient": True},
    "wood_4": {"bg": "#0078a8", "accent1": "#3f78ff", "accent2": "#078a83", "name": "木纹撞色", "theme": "wood", "text_color": "#ffffff"},
    "stone_1": {"bg": "#1b010d", "accent1": "#00ff00", "accent2": "#dbe1FF", "name": "石头暗夜", "theme": "stone"},
    "stone_2": {"bg": "#f0f0f0", "accent1": "#5b007f", "accent2": "#be7F1c", "name": "石头清新", "theme": "stone", "text_color": "#1a1a1a"},
    "stone_3": {"bg": "linear-gradient(135deg,#dbdb80 0%,#dbe1ff 100%)", "accent1": "#ffffff", "accent2": "#0dbeff", "name": "石头渐变", "theme": "stone", "is_gradient": True},
    "stone_4": {"bg": "#00dbe1", "accent1": "#cddbff", "accent2": "#0dbe1c", "name": "石头撞色", "theme": "stone", "text_color": "#ffffff"},
    "marble_1": {"bg": "#01131b", "accent1": "#00ff00", "accent2": "#0193FF", "name": "大理石暗夜", "theme": "marble"},
    "marble_2": {"bg": "#f0f0f0", "accent1": "#01007f", "accent2": "#197F39", "name": "大理石清新", "theme": "marble", "text_color": "#1a1a1a"},
    "marble_3": {"bg": "linear-gradient(135deg,#010180 0%,#0193ff 100%)", "accent1": "#ffffff", "accent2": "#0019ff", "name": "大理石渐变", "theme": "marble", "is_gradient": True},
    "marble_4": {"bg": "#000193", "accent1": "#9b01ff", "accent2": "#001939", "name": "大理石撞色", "theme": "marble", "text_color": "#ffffff"},
    "linen_1": {"bg": "#1c060e", "accent1": "#00ff00", "accent2": "#5c86FF", "name": "亚麻暗夜", "theme": "linen"},
    "linen_2": {"bg": "#f0f0f0", "accent1": "#5c007f", "accent2": "#c87F64", "name": "亚麻清新", "theme": "linen", "text_color": "#1a1a1a"},
    "linen_3": {"bg": "linear-gradient(135deg,#5c5c80 0%,#5c86ff 100%)", "accent1": "#ffffff", "accent2": "#05c8ff", "name": "亚麻渐变", "theme": "linen", "is_gradient": True},
    "linen_4": {"bg": "#005c86", "accent1": "#4e5cff", "accent2": "#05c864", "name": "亚麻撞色", "theme": "linen", "text_color": "#ffffff"},
    "silk_1": {"bg": "#151f0e", "accent1": "#00ff00", "accent2": "#b5ffFF", "name": "丝绸暗夜", "theme": "silk"},
    "silk_2": {"bg": "#f0f0f0", "accent1": "#35007f", "accent2": "#5f7F7c", "name": "丝绸清新", "theme": "silk", "text_color": "#1a1a1a"},
    "silk_3": {"bg": "linear-gradient(135deg,#b5b580 0%,#b5ffff 100%)", "accent1": "#ffffff", "accent2": "#0b5fff", "name": "丝绸渐变", "theme": "silk", "is_gradient": True},
    "silk_4": {"bg": "#00b5ff", "accent1": "#ceb5ff", "accent2": "#0b5ffc", "name": "丝绸撞色", "theme": "silk", "text_color": "#ffffff"},
    "leather_1": {"bg": "#13070a", "accent1": "#00ff00", "accent2": "#b367FF", "name": "皮革暗夜", "theme": "leather"},
    "leather_2": {"bg": "#f0f0f0", "accent1": "#33007f", "accent2": "#367F70", "name": "皮革清新", "theme": "leather", "text_color": "#1a1a1a"},
    "leather_3": {"bg": "linear-gradient(135deg,#b3b380 0%,#b367ff 100%)", "accent1": "#ffffff", "accent2": "#0b36ff", "name": "皮革渐变", "theme": "leather", "is_gradient": True},
    "leather_4": {"bg": "#00b367", "accent1": "#0ab3ff", "accent2": "#0b3670", "name": "皮革撞色", "theme": "leather", "text_color": "#ffffff"},
    "wabi_1": {"bg": "#1e1e13", "accent1": "#00ff00", "accent2": "#1ebeFF", "name": "侘寂暗夜", "theme": "wabi"},
    "wabi_2": {"bg": "#f0f0f0", "accent1": "#1e007f", "accent2": "#eb7F6b", "name": "侘寂清新", "theme": "wabi", "text_color": "#1a1a1a"},
    "wabi_3": {"bg": "linear-gradient(135deg,#1e1e80 0%,#1ebeff 100%)", "accent1": "#ffffff", "accent2": "#01ebff", "name": "侘寂渐变", "theme": "wabi", "is_gradient": True},
    "wabi_4": {"bg": "#001ebe", "accent1": "#b31eff", "accent2": "#01ebeb", "name": "侘寂撞色", "theme": "wabi", "text_color": "#ffffff"},
    "ikigai_1": {"bg": "#0f0d11", "accent1": "#00ff00", "accent2": "#6fedFF", "name": "生意义暗夜", "theme": "ikigai"},
    "ikigai_2": {"bg": "#f0f0f0", "accent1": "#6f007f", "accent2": "#fe7F55", "name": "生意义清新", "theme": "ikigai", "text_color": "#1a1a1a"},
    "ikigai_3": {"bg": "linear-gradient(135deg,#6f6f80 0%,#6fedff 100%)", "accent1": "#ffffff", "accent2": "#06feff", "name": "生意义渐变", "theme": "ikigai", "is_gradient": True},
    "ikigai_4": {"bg": "#006fed", "accent1": "#516fff", "accent2": "#06fed5", "name": "生意义撞色", "theme": "ikigai", "text_color": "#ffffff"},
    "hygge_1": {"bg": "#161000", "accent1": "#00ff00", "accent2": "#5610FF", "name": "舒适暗夜", "theme": "hygge"},
    "hygge_2": {"bg": "#f0f0f0", "accent1": "#56007f", "accent2": "#617F04", "name": "舒适清新", "theme": "hygge", "text_color": "#1a1a1a"},
    "hygge_3": {"bg": "linear-gradient(135deg,#565680 0%,#5610ff 100%)", "accent1": "#ffffff", "accent2": "#0561ff", "name": "舒适渐变", "theme": "hygge", "is_gradient": True},
    "hygge_4": {"bg": "#005610", "accent1": "#4056ff", "accent2": "#056104", "name": "舒适撞色", "theme": "hygge", "text_color": "#ffffff"},
    "feathers_1": {"bg": "#0a170e", "accent1": "#00ff00", "accent2": "#6ad7FF", "name": "羽毛暗夜", "theme": "feathers"},
    "feathers_2": {"bg": "#f0f0f0", "accent1": "#6a007f", "accent2": "#ad7F70", "name": "羽毛清新", "theme": "feathers", "text_color": "#1a1a1a"},
    "feathers_3": {"bg": "linear-gradient(135deg,#6a6a80 0%,#6ad7ff 100%)", "accent1": "#ffffff", "accent2": "#06adff", "name": "羽毛渐变", "theme": "feathers", "is_gradient": True},
    "feathers_4": {"bg": "#006ad7", "accent1": "#0e6aff", "accent2": "#06ad70", "name": "羽毛撞色", "theme": "feathers", "text_color": "#ffffff"},
    "scales_1": {"bg": "#140b0e", "accent1": "#00ff00", "accent2": "#146bFF", "name": "鳞片暗夜", "theme": "scales"},
    "scales_2": {"bg": "#f0f0f0", "accent1": "#14007f", "accent2": "#467F36", "name": "鳞片清新", "theme": "scales", "text_color": "#1a1a1a"},
    "scales_3": {"bg": "linear-gradient(135deg,#141480 0%,#146bff 100%)", "accent1": "#ffffff", "accent2": "#0146ff", "name": "鳞片渐变", "theme": "scales", "is_gradient": True},
    "scales_4": {"bg": "#00146b", "accent1": "#6e14ff", "accent2": "#0146b6", "name": "鳞片撞色", "theme": "scales", "text_color": "#ffffff"},
    "shell_1": {"bg": "#15121b", "accent1": "#00ff00", "accent2": "#5552FF", "name": "贝壳暗夜", "theme": "shell"},
    "shell_2": {"bg": "#f0f0f0", "accent1": "#55007f", "accent2": "#557F23", "name": "贝壳清新", "theme": "shell", "text_color": "#1a1a1a"},
    "shell_3": {"bg": "linear-gradient(135deg,#555580 0%,#5552ff 100%)", "accent1": "#ffffff", "accent2": "#0555ff", "name": "贝壳渐变", "theme": "shell", "is_gradient": True},
    "shell_4": {"bg": "#005552", "accent1": "#3b55ff", "accent2": "#055523", "name": "贝壳撞色", "theme": "shell", "text_color": "#ffffff"},
    "coral_1": {"bg": "#1f1a05", "accent1": "#00ff00", "accent2": "#1f7aFF", "name": "珊瑚暗夜", "theme": "coral"},
    "coral_2": {"bg": "#f0f0f0", "accent1": "#1f007f", "accent2": "#f77F26", "name": "珊瑚清新", "theme": "coral", "text_color": "#1a1a1a"},
    "coral_3": {"bg": "linear-gradient(135deg,#1f1f80 0%,#1f7aff 100%)", "accent1": "#ffffff", "accent2": "#01f7ff", "name": "珊瑚渐变", "theme": "coral", "is_gradient": True},
    "coral_4": {"bg": "#001f7a", "accent1": "#651fff", "accent2": "#01f7a6", "name": "珊瑚撞色", "theme": "coral", "text_color": "#ffffff"},
    "basketball_1": {"bg": "#091414", "accent1": "#00ff00", "accent2": "#c9b4FF", "name": "篮球暗夜", "theme": "basketball"},
    "basketball_2": {"bg": "#f0f0f0", "accent1": "#49007f", "accent2": "#9b7F47", "name": "篮球清新", "theme": "basketball", "text_color": "#1a1a1a"},
    "basketball_3": {"bg": "linear-gradient(135deg,#c9c980 0%,#c9b4ff 100%)", "accent1": "#ffffff", "accent2": "#0c9bff", "name": "篮球渐变", "theme": "basketball", "is_gradient": True},
    "basketball_4": {"bg": "#00c9b4", "accent1": "#74c9ff", "accent2": "#0c9b47", "name": "篮球撞色", "theme": "basketball", "text_color": "#ffffff"},
    "football_1": {"bg": "#000212", "accent1": "#00ff00", "accent2": "#20c2FF", "name": "足球暗夜", "theme": "football"},
    "football_2": {"bg": "#f0f0f0", "accent1": "#20007f", "accent2": "#0c7F2d", "name": "足球清新", "theme": "football", "text_color": "#1a1a1a"},
    "football_3": {"bg": "linear-gradient(135deg,#202080 0%,#20c2ff 100%)", "accent1": "#ffffff", "accent2": "#020cff", "name": "足球渐变", "theme": "football", "is_gradient": True},
    "football_4": {"bg": "#0020c2", "accent1": "#d220ff", "accent2": "#020c2d", "name": "足球撞色", "theme": "football", "text_color": "#ffffff"},
    "tennis_1": {"bg": "#081e06", "accent1": "#00ff00", "accent2": "#e81eFF", "name": "网球暗夜", "theme": "tennis"},
    "tennis_2": {"bg": "#f0f0f0", "accent1": "#68007f", "accent2": "#817F66", "name": "网球清新", "theme": "tennis", "text_color": "#1a1a1a"},
    "tennis_3": {"bg": "linear-gradient(135deg,#e8e880 0%,#e81eff 100%)", "accent1": "#ffffff", "accent2": "#0e81ff", "name": "网球渐变", "theme": "tennis", "is_gradient": True},
    "tennis_4": {"bg": "#00e81e", "accent1": "#66e8ff", "accent2": "#0e81e6", "name": "网球撞色", "theme": "tennis", "text_color": "#ffffff"},
    "baseball_1": {"bg": "#070200", "accent1": "#00ff00", "accent2": "#0702FF", "name": "棒球暗夜", "theme": "baseball"},
    "baseball_2": {"bg": "#f0f0f0", "accent1": "#07007f", "accent2": "#707F2e", "name": "棒球清新", "theme": "baseball", "text_color": "#1a1a1a"},
    "baseball_3": {"bg": "linear-gradient(135deg,#070780 0%,#0702ff 100%)", "accent1": "#ffffff", "accent2": "#0070ff", "name": "棒球渐变", "theme": "baseball", "is_gradient": True},
    "baseball_4": {"bg": "#000702", "accent1": "#e007ff", "accent2": "#00702e", "name": "棒球撞色", "theme": "baseball", "text_color": "#ffffff"},
    "swimming_1": {"bg": "#0b0019", "accent1": "#00ff00", "accent2": "#4b00FF", "name": "游泳暗夜", "theme": "swimming"},
    "swimming_2": {"bg": "#f0f0f0", "accent1": "#4b007f", "accent2": "#b07F05", "name": "游泳清新", "theme": "swimming", "text_color": "#1a1a1a"},
    "swimming_3": {"bg": "linear-gradient(135deg,#4b4b80 0%,#4b00ff 100%)", "accent1": "#ffffff", "accent2": "#04b0ff", "name": "游泳渐变", "theme": "swimming", "is_gradient": True},
    "swimming_4": {"bg": "#004b00", "accent1": "#594bff", "accent2": "#04b005", "name": "游泳撞色", "theme": "swimming", "text_color": "#ffffff"},
    "running_1": {"bg": "#000e0f", "accent1": "#00ff00", "accent2": "#204eFF", "name": "跑步暗夜", "theme": "running"},
    "running_2": {"bg": "#f0f0f0", "accent1": "#20007f", "accent2": "#047F6c", "name": "跑步清新", "theme": "running", "text_color": "#1a1a1a"},
    "running_3": {"bg": "linear-gradient(135deg,#202080 0%,#204eff 100%)", "accent1": "#ffffff", "accent2": "#0204ff", "name": "跑步渐变", "theme": "running", "is_gradient": True},
    "running_4": {"bg": "#00204e", "accent1": "#cf20ff", "accent2": "#0204ec", "name": "跑步撞色", "theme": "running", "text_color": "#ffffff"},
    "cycling_1": {"bg": "#0e1407", "accent1": "#00ff00", "accent2": "#8e14FF", "name": "自行车暗夜", "theme": "cycling"},
    "cycling_2": {"bg": "#f0f0f0", "accent1": "#0e007f", "accent2": "#e17F40", "name": "自行车清新", "theme": "cycling", "text_color": "#1a1a1a"},
    "cycling_3": {"bg": "linear-gradient(135deg,#8e8e80 0%,#8e14ff 100%)", "accent1": "#ffffff", "accent2": "#08e1ff", "name": "自行车渐变", "theme": "cycling", "is_gradient": True},
    "cycling_4": {"bg": "#008e14", "accent1": "#078eff", "accent2": "#08e140", "name": "自行车撞色", "theme": "cycling", "text_color": "#ffffff"},
    "yoga_1": {"bg": "#040a11", "accent1": "#00ff00", "accent2": "#246aFF", "name": "瑜伽暗夜", "theme": "yoga"},
    "yoga_2": {"bg": "#f0f0f0", "accent1": "#24007f", "accent2": "#467F27", "name": "瑜伽清新", "theme": "yoga", "text_color": "#1a1a1a"},
    "yoga_3": {"bg": "linear-gradient(135deg,#242480 0%,#246aff 100%)", "accent1": "#ffffff", "accent2": "#0246ff", "name": "瑜伽渐变", "theme": "yoga", "is_gradient": True},
    "yoga_4": {"bg": "#00246a", "accent1": "#7124ff", "accent2": "#0246a7", "name": "瑜伽撞色", "theme": "yoga", "text_color": "#ffffff"},
    "climbing_1": {"bg": "#1e0002", "accent1": "#00ff00", "accent2": "#1e40FF", "name": "攀岩暗夜", "theme": "climbing"},
    "climbing_2": {"bg": "#f0f0f0", "accent1": "#1e007f", "accent2": "#e47F0c", "name": "攀岩清新", "theme": "climbing", "text_color": "#1a1a1a"},
    "climbing_3": {"bg": "linear-gradient(135deg,#1e1e80 0%,#1e40ff 100%)", "accent1": "#ffffff", "accent2": "#01e4ff", "name": "攀岩渐变", "theme": "climbing", "is_gradient": True},
    "climbing_4": {"bg": "#001e40", "accent1": "#c21eff", "accent2": "#01e40c", "name": "攀岩撞色", "theme": "climbing", "text_color": "#ffffff"},
    "skiing_1": {"bg": "#0c070f", "accent1": "#00ff00", "accent2": "#6c67FF", "name": "滑雪暗夜", "theme": "skiing"},
    "skiing_2": {"bg": "#f0f0f0", "accent1": "#6c007f", "accent2": "#c67F7c", "name": "滑雪清新", "theme": "skiing", "text_color": "#1a1a1a"},
    "skiing_3": {"bg": "linear-gradient(135deg,#6c6c80 0%,#6c67ff 100%)", "accent1": "#ffffff", "accent2": "#06c6ff", "name": "滑雪渐变", "theme": "skiing", "is_gradient": True},
    "skiing_4": {"bg": "#006c67", "accent1": "#cf6cff", "accent2": "#06c67c", "name": "滑雪撞色", "theme": "skiing", "text_color": "#ffffff"},
    "boxing_1": {"bg": "#041e19", "accent1": "#00ff00", "accent2": "#c4beFF", "name": "拳击暗夜", "theme": "boxing"},
    "boxing_2": {"bg": "#f0f0f0", "accent1": "#44007f", "accent2": "#4b7F63", "name": "拳击清新", "theme": "boxing", "text_color": "#1a1a1a"},
    "boxing_3": {"bg": "linear-gradient(135deg,#c4c480 0%,#c4beff 100%)", "accent1": "#ffffff", "accent2": "#0c4bff", "name": "拳击渐变", "theme": "boxing", "is_gradient": True},
    "boxing_4": {"bg": "#00c4be", "accent1": "#39c4ff", "accent2": "#0c4be3", "name": "拳击撞色", "theme": "boxing", "text_color": "#ffffff"},
    "golf_1": {"bg": "#071b04", "accent1": "#00ff00", "accent2": "#07fbFF", "name": "高尔夫暗夜", "theme": "golf"},
    "golf_2": {"bg": "#f0f0f0", "accent1": "#07007f", "accent2": "#7f7F36", "name": "高尔夫清新", "theme": "golf", "text_color": "#1a1a1a"},
    "golf_3": {"bg": "linear-gradient(135deg,#070780 0%,#07fbff 100%)", "accent1": "#ffffff", "accent2": "#007fff", "name": "高尔夫渐变", "theme": "golf", "is_gradient": True},
    "golf_4": {"bg": "#0007fb", "accent1": "#6407ff", "accent2": "#007fb6", "name": "高尔夫撞色", "theme": "golf", "text_color": "#ffffff"},
    "bbq_1": {"bg": "#010a1c", "accent1": "#00ff00", "accent2": "#c1eaFF", "name": "烧烤暗夜", "theme": "bbq"},
    "bbq_2": {"bg": "#f0f0f0", "accent1": "#41007f", "accent2": "#1e7F2b", "name": "烧烤清新", "theme": "bbq", "text_color": "#1a1a1a"},
    "bbq_3": {"bg": "linear-gradient(135deg,#c1c180 0%,#c1eaff 100%)", "accent1": "#ffffff", "accent2": "#0c1eff", "name": "烧烤渐变", "theme": "bbq", "is_gradient": True},
    "bbq_4": {"bg": "#00c1ea", "accent1": "#bcc1ff", "accent2": "#0c1eab", "name": "烧烤撞色", "theme": "bbq", "text_color": "#ffffff"},
    "sushi2_1": {"bg": "#181607", "accent1": "#00ff00", "accent2": "#b836FF", "name": "寿司暗夜", "theme": "sushi2"},
    "sushi2_2": {"bg": "#f0f0f0", "accent1": "#38007f", "accent2": "#837F68", "name": "寿司清新", "theme": "sushi2", "text_color": "#1a1a1a"},
    "sushi2_3": {"bg": "linear-gradient(135deg,#b8b880 0%,#b836ff 100%)", "accent1": "#ffffff", "accent2": "#0b83ff", "name": "寿司渐变", "theme": "sushi2", "is_gradient": True},
    "sushi2_4": {"bg": "#00b836", "accent1": "#87b8ff", "accent2": "#0b8368", "name": "寿司撞色", "theme": "sushi2", "text_color": "#ffffff"},
    "ramen_1": {"bg": "#0d151c", "accent1": "#00ff00", "accent2": "#0db5FF", "name": "拉面暗夜", "theme": "ramen"},
    "ramen_2": {"bg": "#f0f0f0", "accent1": "#0d007f", "accent2": "#db7F51", "name": "拉面清新", "theme": "ramen", "text_color": "#1a1a1a"},
    "ramen_3": {"bg": "linear-gradient(135deg,#0d0d80 0%,#0db5ff 100%)", "accent1": "#ffffff", "accent2": "#00dbff", "name": "拉面渐变", "theme": "ramen", "is_gradient": True},
    "ramen_4": {"bg": "#000db5", "accent1": "#1c0dff", "accent2": "#00db51", "name": "拉面撞色", "theme": "ramen", "text_color": "#ffffff"},
    "dessert_1": {"bg": "#0a110b", "accent1": "#00ff00", "accent2": "#2a91FF", "name": "甜点暗夜", "theme": "dessert"},
    "dessert_2": {"bg": "#f0f0f0", "accent1": "#2a007f", "accent2": "#a97F1e", "name": "甜点清新", "theme": "dessert", "text_color": "#1a1a1a"},
    "dessert_3": {"bg": "linear-gradient(135deg,#2a2a80 0%,#2a91ff 100%)", "accent1": "#ffffff", "accent2": "#02a9ff", "name": "甜点渐变", "theme": "dessert", "is_gradient": True},
    "dessert_4": {"bg": "#002a91", "accent1": "#eb2aff", "accent2": "#02a91e", "name": "甜点撞色", "theme": "dessert", "text_color": "#ffffff"},
    "coffee2_1": {"bg": "#19180e", "accent1": "#00ff00", "accent2": "#d9f8FF", "name": "咖啡暗夜", "theme": "coffee2"},
    "coffee2_2": {"bg": "#f0f0f0", "accent1": "#59007f", "accent2": "#9f7F06", "name": "咖啡清新", "theme": "coffee2", "text_color": "#1a1a1a"},
    "coffee2_3": {"bg": "linear-gradient(135deg,#d9d980 0%,#d9f8ff 100%)", "accent1": "#ffffff", "accent2": "#0d9fff", "name": "咖啡渐变", "theme": "coffee2", "is_gradient": True},
    "coffee2_4": {"bg": "#00d9f8", "accent1": "#6ed9ff", "accent2": "#0d9f86", "name": "咖啡撞色", "theme": "coffee2", "text_color": "#ffffff"},
    "tea_1": {"bg": "#151705", "accent1": "#00ff00", "accent2": "#d577FF", "name": "茶暗夜", "theme": "tea"},
    "tea_2": {"bg": "#f0f0f0", "accent1": "#55007f", "accent2": "#577F7a", "name": "茶清新", "theme": "tea", "text_color": "#1a1a1a"},
    "tea_3": {"bg": "linear-gradient(135deg,#d5d580 0%,#d577ff 100%)", "accent1": "#ffffff", "accent2": "#0d57ff", "name": "茶渐变", "theme": "tea", "is_gradient": True},
    "tea_4": {"bg": "#00d577", "accent1": "#a5d5ff", "accent2": "#0d577a", "name": "茶撞色", "theme": "tea", "text_color": "#ffffff"},
    "cocktail_1": {"bg": "#170718", "accent1": "#00ff00", "accent2": "#b7a7FF", "name": "鸡尾酒暗夜", "theme": "cocktail"},
    "cocktail_2": {"bg": "#f0f0f0", "accent1": "#37007f", "accent2": "#7a7F71", "name": "鸡尾酒清新", "theme": "cocktail", "text_color": "#1a1a1a"},
    "cocktail_3": {"bg": "linear-gradient(135deg,#b7b780 0%,#b7a7ff 100%)", "accent1": "#ffffff", "accent2": "#0b7aff", "name": "鸡尾酒渐变", "theme": "cocktail", "is_gradient": True},
    "cocktail_4": {"bg": "#00b7a7", "accent1": "#18b7ff", "accent2": "#0b7a71", "name": "鸡尾酒撞色", "theme": "cocktail", "text_color": "#ffffff"},
    "wine_1": {"bg": "#1d1a10", "accent1": "#00ff00", "accent2": "#fd7aFF", "name": "红酒暗夜", "theme": "wine"},
    "wine_2": {"bg": "#f0f0f0", "accent1": "#7d007f", "accent2": "#d77F2b", "name": "红酒清新", "theme": "wine", "text_color": "#1a1a1a"},
    "wine_3": {"bg": "linear-gradient(135deg,#fdfd80 0%,#fd7aff 100%)", "accent1": "#ffffff", "accent2": "#0fd7ff", "name": "红酒渐变", "theme": "wine", "is_gradient": True},
    "wine_4": {"bg": "#00fd7a", "accent1": "#b0fdff", "accent2": "#0fd7ab", "name": "红酒撞色", "theme": "wine", "text_color": "#ffffff"},
    "beer_1": {"bg": "#101c19", "accent1": "#00ff00", "accent2": "#105cFF", "name": "啤酒暗夜", "theme": "beer"},
    "beer_2": {"bg": "#f0f0f0", "accent1": "#10007f", "accent2": "#057F49", "name": "啤酒清新", "theme": "beer", "text_color": "#1a1a1a"},
    "beer_3": {"bg": "linear-gradient(135deg,#101080 0%,#105cff 100%)", "accent1": "#ffffff", "accent2": "#0105ff", "name": "啤酒渐变", "theme": "beer", "is_gradient": True},
    "beer_4": {"bg": "#00105c", "accent1": "#9910ff", "accent2": "#0105c9", "name": "啤酒撞色", "theme": "beer", "text_color": "#ffffff"},
    "milktea_1": {"bg": "#100e15", "accent1": "#00ff00", "accent2": "#f0aeFF", "name": "奶茶暗夜", "theme": "milktea"},
    "milktea_2": {"bg": "#f0f0f0", "accent1": "#70007f", "accent2": "#0a7F6d", "name": "奶茶清新", "theme": "milktea", "text_color": "#1a1a1a"},
    "milktea_3": {"bg": "linear-gradient(135deg,#f0f080 0%,#f0aeff 100%)", "accent1": "#ffffff", "accent2": "#0f0aff", "name": "奶茶渐变", "theme": "milktea", "is_gradient": True},
    "milktea_4": {"bg": "#00f0ae", "accent1": "#d5f0ff", "accent2": "#0f0aed", "name": "奶茶撞色", "theme": "milktea", "text_color": "#ffffff"},
    "juice_1": {"bg": "#020716", "accent1": "#00ff00", "accent2": "#a267FF", "name": "果汁暗夜", "theme": "juice"},
    "juice_2": {"bg": "#f0f0f0", "accent1": "#22007f", "accent2": "#267F75", "name": "果汁清新", "theme": "juice", "text_color": "#1a1a1a"},
    "juice_3": {"bg": "linear-gradient(135deg,#a2a280 0%,#a267ff 100%)", "accent1": "#ffffff", "accent2": "#0a26ff", "name": "果汁渐变", "theme": "juice", "is_gradient": True},
    "juice_4": {"bg": "#00a267", "accent1": "#56a2ff", "accent2": "#0a2675", "name": "果汁撞色", "theme": "juice", "text_color": "#ffffff"},
    "christmas_1": {"bg": "#0b0606", "accent1": "#00ff00", "accent2": "#8be6FF", "name": "圣诞暗夜", "theme": "christmas"},
    "christmas_2": {"bg": "#f0f0f0", "accent1": "#0b007f", "accent2": "#be7F64", "name": "圣诞清新", "theme": "christmas", "text_color": "#1a1a1a"},
    "christmas_3": {"bg": "linear-gradient(135deg,#8b8b80 0%,#8be6ff 100%)", "accent1": "#ffffff", "accent2": "#08beff", "name": "圣诞渐变", "theme": "christmas", "is_gradient": True},
    "christmas_4": {"bg": "#008be6", "accent1": "#468bff", "accent2": "#08be64", "name": "圣诞撞色", "theme": "christmas", "text_color": "#ffffff"},
    "halloween_1": {"bg": "#041416", "accent1": "#00ff00", "accent2": "#a4f4FF", "name": "万圣暗夜", "theme": "halloween"},
    "halloween_2": {"bg": "#f0f0f0", "accent1": "#24007f", "accent2": "#4f7F43", "name": "万圣清新", "theme": "halloween", "text_color": "#1a1a1a"},
    "halloween_3": {"bg": "linear-gradient(135deg,#a4a480 0%,#a4f4ff 100%)", "accent1": "#ffffff", "accent2": "#0a4fff", "name": "万圣渐变", "theme": "halloween", "is_gradient": True},
    "halloween_4": {"bg": "#00a4f4", "accent1": "#36a4ff", "accent2": "#0a4f43", "name": "万圣撞色", "theme": "halloween", "text_color": "#ffffff"},
    "newyear_1": {"bg": "#1b0808", "accent1": "#00ff00", "accent2": "#7ba8FF", "name": "新年暗夜", "theme": "newyear"},
    "newyear_2": {"bg": "#f0f0f0", "accent1": "#7b007f", "accent2": "#ba7F04", "name": "新年清新", "theme": "newyear", "text_color": "#1a1a1a"},
    "newyear_3": {"bg": "linear-gradient(135deg,#7b7b80 0%,#7ba8ff 100%)", "accent1": "#ffffff", "accent2": "#07baff", "name": "新年渐变", "theme": "newyear", "is_gradient": True},
    "newyear_4": {"bg": "#007ba8", "accent1": "#487bff", "accent2": "#07ba84", "name": "新年撞色", "theme": "newyear", "text_color": "#ffffff"},
    "midautumn_1": {"bg": "#0b1510", "accent1": "#00ff00", "accent2": "#4bb5FF", "name": "中秋暗夜", "theme": "midautumn"},
    "midautumn_2": {"bg": "#f0f0f0", "accent1": "#4b007f", "accent2": "#bb7F5b", "name": "中秋清新", "theme": "midautumn", "text_color": "#1a1a1a"},
    "midautumn_3": {"bg": "linear-gradient(135deg,#4b4b80 0%,#4bb5ff 100%)", "accent1": "#ffffff", "accent2": "#04bbff", "name": "中秋渐变", "theme": "midautumn", "is_gradient": True},
    "midautumn_4": {"bg": "#004bb5", "accent1": "#b04bff", "accent2": "#04bb5b", "name": "中秋撞色", "theme": "midautumn", "text_color": "#ffffff"},
    "springfestival_1": {"bg": "#021b11", "accent1": "#00ff00", "accent2": "#223bFF", "name": "春节暗夜", "theme": "springfestival"},
    "springfestival_2": {"bg": "#f0f0f0", "accent1": "#22007f", "accent2": "#237F39", "name": "春节清新", "theme": "springfestival", "text_color": "#1a1a1a"},
    "springfestival_3": {"bg": "linear-gradient(135deg,#222280 0%,#223bff 100%)", "accent1": "#ffffff", "accent2": "#0223ff", "name": "春节渐变", "theme": "springfestival", "is_gradient": True},
    "springfestival_4": {"bg": "#00223b", "accent1": "#9122ff", "accent2": "#0223b9", "name": "春节撞色", "theme": "springfestival", "text_color": "#ffffff"},
    "valentine_1": {"bg": "#07140e", "accent1": "#00ff00", "accent2": "#a754FF", "name": "情人暗夜", "theme": "valentine"},
    "valentine_2": {"bg": "#f0f0f0", "accent1": "#27007f", "accent2": "#757F4a", "name": "情人清新", "theme": "valentine", "text_color": "#1a1a1a"},
    "valentine_3": {"bg": "linear-gradient(135deg,#a7a780 0%,#a754ff 100%)", "accent1": "#ffffff", "accent2": "#0a75ff", "name": "情人渐变", "theme": "valentine", "is_gradient": True},
    "valentine_4": {"bg": "#00a754", "accent1": "#aea7ff", "accent2": "#0a754a", "name": "情人撞色", "theme": "valentine", "text_color": "#ffffff"},
    "rpg_1": {"bg": "#190314", "accent1": "#00ff00", "accent2": "#f9e3FF", "name": "RPG暗夜", "theme": "rpg"},
    "rpg_2": {"bg": "#f0f0f0", "accent1": "#79007f", "accent2": "#9e7F3d", "name": "RPG清新", "theme": "rpg", "text_color": "#1a1a1a"},
    "rpg_3": {"bg": "linear-gradient(135deg,#f9f980 0%,#f9e3ff 100%)", "accent1": "#ffffff", "accent2": "#0f9eff", "name": "RPG渐变", "theme": "rpg", "is_gradient": True},
    "rpg_4": {"bg": "#00f9e3", "accent1": "#d4f9ff", "accent2": "#0f9e3d", "name": "RPG撞色", "theme": "rpg", "text_color": "#ffffff"},
    "fps_1": {"bg": "#110012", "accent1": "#00ff00", "accent2": "#d120FF", "name": "FPS暗夜", "theme": "fps"},
    "fps_2": {"bg": "#f0f0f0", "accent1": "#51007f", "accent2": "#127F03", "name": "FPS清新", "theme": "fps", "text_color": "#1a1a1a"},
    "fps_3": {"bg": "linear-gradient(135deg,#d1d180 0%,#d120ff 100%)", "accent1": "#ffffff", "accent2": "#0d12ff", "name": "FPS渐变", "theme": "fps", "is_gradient": True},
    "fps_4": {"bg": "#00d120", "accent1": "#32d1ff", "accent2": "#0d1203", "name": "FPS撞色", "theme": "fps", "text_color": "#ffffff"},
    "moba_1": {"bg": "#1a1904", "accent1": "#00ff00", "accent2": "#baf9FF", "name": "MOBA暗夜", "theme": "moba"},
    "moba_2": {"bg": "#f0f0f0", "accent1": "#3a007f", "accent2": "#af7F18", "name": "MOBA清新", "theme": "moba", "text_color": "#1a1a1a"},
    "moba_3": {"bg": "linear-gradient(135deg,#baba80 0%,#baf9ff 100%)", "accent1": "#ffffff", "accent2": "#0bafff", "name": "MOBA渐变", "theme": "moba", "is_gradient": True},
    "moba_4": {"bg": "#00baf9", "accent1": "#84baff", "accent2": "#0baf98", "name": "MOBA撞色", "theme": "moba", "text_color": "#ffffff"},
    "racing_1": {"bg": "#0d020e", "accent1": "#00ff00", "accent2": "#2d62FF", "name": "赛车暗夜", "theme": "racing"},
    "racing_2": {"bg": "#f0f0f0", "accent1": "#2d007f", "accent2": "#d67F22", "name": "赛车清新", "theme": "racing", "text_color": "#1a1a1a"},
    "racing_3": {"bg": "linear-gradient(135deg,#2d2d80 0%,#2d62ff 100%)", "accent1": "#ffffff", "accent2": "#02d6ff", "name": "赛车渐变", "theme": "racing", "is_gradient": True},
    "racing_4": {"bg": "#002d62", "accent1": "#2e2dff", "accent2": "#02d622", "name": "赛车撞色", "theme": "racing", "text_color": "#ffffff"},
    "puzzle_1": {"bg": "#15121a", "accent1": "#00ff00", "accent2": "#9512FF", "name": "解谜暗夜", "theme": "puzzle"},
    "puzzle_2": {"bg": "#f0f0f0", "accent1": "#15007f", "accent2": "#517F2d", "name": "解谜清新", "theme": "puzzle", "text_color": "#1a1a1a"},
    "puzzle_3": {"bg": "linear-gradient(135deg,#959580 0%,#9512ff 100%)", "accent1": "#ffffff", "accent2": "#0951ff", "name": "解谜渐变", "theme": "puzzle", "is_gradient": True},
    "puzzle_4": {"bg": "#009512", "accent1": "#da95ff", "accent2": "#09512d", "name": "解谜撞色", "theme": "puzzle", "text_color": "#ffffff"},
    "sandbox_1": {"bg": "#040105", "accent1": "#00ff00", "accent2": "#4421FF", "name": "沙盒暗夜", "theme": "sandbox"},
    "sandbox_2": {"bg": "#f0f0f0", "accent1": "#44007f", "accent2": "#427F1e", "name": "沙盒清新", "theme": "sandbox", "text_color": "#1a1a1a"},
    "sandbox_3": {"bg": "linear-gradient(135deg,#444480 0%,#4421ff 100%)", "accent1": "#ffffff", "accent2": "#0442ff", "name": "沙盒渐变", "theme": "sandbox", "is_gradient": True},
    "sandbox_4": {"bg": "#004421", "accent1": "#e544ff", "accent2": "#04421e", "name": "沙盒撞色", "theme": "sandbox", "text_color": "#ffffff"},
    "cozy_1": {"bg": "#170411", "accent1": "#00ff00", "accent2": "#d784FF", "name": "休闲暗夜", "theme": "cozy"},
    "cozy_2": {"bg": "#f0f0f0", "accent1": "#57007f", "accent2": "#787F4f", "name": "休闲清新", "theme": "cozy", "text_color": "#1a1a1a"},
    "cozy_3": {"bg": "linear-gradient(135deg,#d7d780 0%,#d784ff 100%)", "accent1": "#ffffff", "accent2": "#0d78ff", "name": "休闲渐变", "theme": "cozy", "is_gradient": True},
    "cozy_4": {"bg": "#00d784", "accent1": "#f1d7ff", "accent2": "#0d784f", "name": "休闲撞色", "theme": "cozy", "text_color": "#ffffff"},
    "classical_1": {"bg": "#020a07", "accent1": "#00ff00", "accent2": "#228aFF", "name": "古典暗夜", "theme": "classical"},
    "classical_2": {"bg": "#f0f0f0", "accent1": "#22007f", "accent2": "#287F22", "name": "古典清新", "theme": "classical", "text_color": "#1a1a1a"},
    "classical_3": {"bg": "linear-gradient(135deg,#222280 0%,#228aff 100%)", "accent1": "#ffffff", "accent2": "#0228ff", "name": "古典渐变", "theme": "classical", "is_gradient": True},
    "classical_4": {"bg": "#00228a", "accent1": "#2722ff", "accent2": "#0228a2", "name": "古典撞色", "theme": "classical", "text_color": "#ffffff"},
    "country_1": {"bg": "#15010b", "accent1": "#00ff00", "accent2": "#75a1FF", "name": "乡村暗夜", "theme": "country"},
    "country_2": {"bg": "#f0f0f0", "accent1": "#75007f", "accent2": "#5a7F1e", "name": "乡村清新", "theme": "country", "text_color": "#1a1a1a"},
    "country_3": {"bg": "linear-gradient(135deg,#757580 0%,#75a1ff 100%)", "accent1": "#ffffff", "accent2": "#075aff", "name": "乡村渐变", "theme": "country", "is_gradient": True},
    "country_4": {"bg": "#0075a1", "accent1": "#eb75ff", "accent2": "#075a1e", "name": "乡村撞色", "theme": "country", "text_color": "#ffffff"},
    "folk_1": {"bg": "#17140b", "accent1": "#00ff00", "accent2": "#1714FF", "name": "民谣暗夜", "theme": "folk"},
    "folk_2": {"bg": "#f0f0f0", "accent1": "#17007f", "accent2": "#717F42", "name": "民谣清新", "theme": "folk", "text_color": "#1a1a1a"},
    "folk_3": {"bg": "linear-gradient(135deg,#171780 0%,#1714ff 100%)", "accent1": "#ffffff", "accent2": "#0171ff", "name": "民谣渐变", "theme": "folk", "is_gradient": True},
    "folk_4": {"bg": "#001714", "accent1": "#2b17ff", "accent2": "#017142", "name": "民谣撞色", "theme": "folk", "text_color": "#ffffff"},
    "funk_1": {"bg": "#09031f", "accent1": "#00ff00", "accent2": "#0983FF", "name": "放克暗夜", "theme": "funk"},
    "funk_2": {"bg": "#f0f0f0", "accent1": "#09007f", "accent2": "#987F35", "name": "放克清新", "theme": "funk", "text_color": "#1a1a1a"},
    "funk_3": {"bg": "linear-gradient(135deg,#090980 0%,#0983ff 100%)", "accent1": "#ffffff", "accent2": "#0098ff", "name": "放克渐变", "theme": "funk", "is_gradient": True},
    "funk_4": {"bg": "#000983", "accent1": "#5f09ff", "accent2": "#009835", "name": "放克撞色", "theme": "funk", "text_color": "#ffffff"},
    "disco_1": {"bg": "#100b03", "accent1": "#00ff00", "accent2": "#508bFF", "name": "迪斯科暗夜", "theme": "disco"},
    "disco_2": {"bg": "#f0f0f0", "accent1": "#50007f", "accent2": "#087F3e", "name": "迪斯科清新", "theme": "disco", "text_color": "#1a1a1a"},
    "disco_3": {"bg": "linear-gradient(135deg,#505080 0%,#508bff 100%)", "accent1": "#ffffff", "accent2": "#0508ff", "name": "迪斯科渐变", "theme": "disco", "is_gradient": True},
    "disco_4": {"bg": "#00508b", "accent1": "#e350ff", "accent2": "#0508be", "name": "迪斯科撞色", "theme": "disco", "text_color": "#ffffff"},
    "techno_1": {"bg": "#08110c", "accent1": "#00ff00", "accent2": "#8851FF", "name": "Techno暗夜", "theme": "techno"},
    "techno_2": {"bg": "#f0f0f0", "accent1": "#08007f", "accent2": "#857F16", "name": "Techno清新", "theme": "techno", "text_color": "#1a1a1a"},
    "techno_3": {"bg": "linear-gradient(135deg,#888880 0%,#8851ff 100%)", "accent1": "#ffffff", "accent2": "#0885ff", "name": "Techno渐变", "theme": "techno", "is_gradient": True},
    "techno_4": {"bg": "#008851", "accent1": "#6c88ff", "accent2": "#088516", "name": "Techno撞色", "theme": "techno", "text_color": "#ffffff"},
    "house_1": {"bg": "#0a051e", "accent1": "#00ff00", "accent2": "#aa85FF", "name": "House暗夜", "theme": "house"},
    "house_2": {"bg": "#f0f0f0", "accent1": "#2a007f", "accent2": "#a87F5b", "name": "House清新", "theme": "house", "text_color": "#1a1a1a"},
    "house_3": {"bg": "linear-gradient(135deg,#aaaa80 0%,#aa85ff 100%)", "accent1": "#ffffff", "accent2": "#0aa8ff", "name": "House渐变", "theme": "house", "is_gradient": True},
    "house_4": {"bg": "#00aa85", "accent1": "#beaaff", "accent2": "#0aa85b", "name": "House撞色", "theme": "house", "text_color": "#ffffff"},
    "anime2_1": {"bg": "#191d03", "accent1": "#00ff00", "accent2": "#59fdFF", "name": "动漫暗夜", "theme": "anime2"},
    "anime2_2": {"bg": "#f0f0f0", "accent1": "#59007f", "accent2": "#9f7F56", "name": "动漫清新", "theme": "anime2", "text_color": "#1a1a1a"},
    "anime2_3": {"bg": "linear-gradient(135deg,#595980 0%,#59fdff 100%)", "accent1": "#ffffff", "accent2": "#059fff", "name": "动漫渐变", "theme": "anime2", "is_gradient": True},
    "anime2_4": {"bg": "#0059fd", "accent1": "#6359ff", "accent2": "#059fd6", "name": "动漫撞色", "theme": "anime2", "text_color": "#ffffff"},
    "drama_1": {"bg": "#1a0a17", "accent1": "#00ff00", "accent2": "#9aaaFF", "name": "剧情暗夜", "theme": "drama"},
    "drama_2": {"bg": "#f0f0f0", "accent1": "#1a007f", "accent2": "#aa7F2d", "name": "剧情清新", "theme": "drama", "text_color": "#1a1a1a"},
    "drama_3": {"bg": "linear-gradient(135deg,#9a9a80 0%,#9aaaff 100%)", "accent1": "#ffffff", "accent2": "#09aaff", "name": "剧情渐变", "theme": "drama", "is_gradient": True},
    "drama_4": {"bg": "#009aaa", "accent1": "#d79aff", "accent2": "#09aaad", "name": "剧情撞色", "theme": "drama", "text_color": "#ffffff"},
    "comedy_1": {"bg": "#091806", "accent1": "#00ff00", "accent2": "#89f8FF", "name": "喜剧暗夜", "theme": "comedy"},
    "comedy_2": {"bg": "#f0f0f0", "accent1": "#09007f", "accent2": "#9f7F02", "name": "喜剧清新", "theme": "comedy", "text_color": "#1a1a1a"},
    "comedy_3": {"bg": "linear-gradient(135deg,#898980 0%,#89f8ff 100%)", "accent1": "#ffffff", "accent2": "#089fff", "name": "喜剧渐变", "theme": "comedy", "is_gradient": True},
    "comedy_4": {"bg": "#0089f8", "accent1": "#2689ff", "accent2": "#089f82", "name": "喜剧撞色", "theme": "comedy", "text_color": "#ffffff"},
    "romance_1": {"bg": "#12110b", "accent1": "#00ff00", "accent2": "#7211FF", "name": "爱情暗夜", "theme": "romance"},
    "romance_2": {"bg": "#f0f0f0", "accent1": "#72007f", "accent2": "#217F10", "name": "爱情清新", "theme": "romance", "text_color": "#1a1a1a"},
    "romance_3": {"bg": "linear-gradient(135deg,#727280 0%,#7211ff 100%)", "accent1": "#ffffff", "accent2": "#0721ff", "name": "爱情渐变", "theme": "romance", "is_gradient": True},
    "romance_4": {"bg": "#007211", "accent1": "#0b72ff", "accent2": "#072110", "name": "爱情撞色", "theme": "romance", "text_color": "#ffffff"},
    "action_1": {"bg": "#140f16", "accent1": "#00ff00", "accent2": "#d48fFF", "name": "动作暗夜", "theme": "action"},
    "action_2": {"bg": "#f0f0f0", "accent1": "#54007f", "accent2": "#487F7d", "name": "动作清新", "theme": "action", "text_color": "#1a1a1a"},
    "action_3": {"bg": "linear-gradient(135deg,#d4d480 0%,#d48fff 100%)", "accent1": "#ffffff", "accent2": "#0d48ff", "name": "动作渐变", "theme": "action", "is_gradient": True},
    "action_4": {"bg": "#00d48f", "accent1": "#d6d4ff", "accent2": "#0d48fd", "name": "动作撞色", "theme": "action", "text_color": "#ffffff"},
    "fantasy_1": {"bg": "#030d1e", "accent1": "#00ff00", "accent2": "#830dFF", "name": "奇幻暗夜", "theme": "fantasy"},
    "fantasy_2": {"bg": "#f0f0f0", "accent1": "#03007f", "accent2": "#307F5b", "name": "奇幻清新", "theme": "fantasy", "text_color": "#1a1a1a"},
    "fantasy_3": {"bg": "linear-gradient(135deg,#838380 0%,#830dff 100%)", "accent1": "#ffffff", "accent2": "#0830ff", "name": "奇幻渐变", "theme": "fantasy", "is_gradient": True},
    "fantasy_4": {"bg": "#00830d", "accent1": "#be83ff", "accent2": "#0830db", "name": "奇幻撞色", "theme": "fantasy", "text_color": "#ffffff"},
    "mystery_1": {"bg": "#08190f", "accent1": "#00ff00", "accent2": "#e8b9FF", "name": "悬疑暗夜", "theme": "mystery"},
    "mystery_2": {"bg": "#f0f0f0", "accent1": "#68007f", "accent2": "#8b7F1c", "name": "悬疑清新", "theme": "mystery", "text_color": "#1a1a1a"},
    "mystery_3": {"bg": "linear-gradient(135deg,#e8e880 0%,#e8b9ff 100%)", "accent1": "#ffffff", "accent2": "#0e8bff", "name": "悬疑渐变", "theme": "mystery", "is_gradient": True},
    "mystery_4": {"bg": "#00e8b9", "accent1": "#cfe8ff", "accent2": "#0e8b9c", "name": "悬疑撞色", "theme": "mystery", "text_color": "#ffffff"},
    "party_1": {"bg": "#1a0d18", "accent1": "#00ff00", "accent2": "#9aedFF", "name": "派对暗夜", "theme": "party"},
    "party_2": {"bg": "#f0f0f0", "accent1": "#1a007f", "accent2": "#ae7F53", "name": "派对清新", "theme": "party", "text_color": "#1a1a1a"},
    "party_3": {"bg": "linear-gradient(135deg,#9a9a80 0%,#9aedff 100%)", "accent1": "#ffffff", "accent2": "#09aeff", "name": "派对渐变", "theme": "party", "is_gradient": True},
    "party_4": {"bg": "#009aed", "accent1": "#389aff", "accent2": "#09aed3", "name": "派对撞色", "theme": "party", "text_color": "#ffffff"},
    "picnic_1": {"bg": "#0a0d1e", "accent1": "#00ff00", "accent2": "#6a2dFF", "name": "野餐暗夜", "theme": "picnic"},
    "picnic_2": {"bg": "#f0f0f0", "accent1": "#6a007f", "accent2": "#a27F5b", "name": "野餐清新", "theme": "picnic", "text_color": "#1a1a1a"},
    "picnic_3": {"bg": "linear-gradient(135deg,#6a6a80 0%,#6a2dff 100%)", "accent1": "#ffffff", "accent2": "#06a2ff", "name": "野餐渐变", "theme": "picnic", "is_gradient": True},
    "picnic_4": {"bg": "#006a2d", "accent1": "#be6aff", "accent2": "#06a2db", "name": "野餐撞色", "theme": "picnic", "text_color": "#ffffff"},
    "camping_1": {"bg": "#061605", "accent1": "#00ff00", "accent2": "#2656FF", "name": "露营暗夜", "theme": "camping"},
    "camping_2": {"bg": "#f0f0f0", "accent1": "#26007f", "accent2": "#657F66", "name": "露营清新", "theme": "camping", "text_color": "#1a1a1a"},
    "camping_3": {"bg": "linear-gradient(135deg,#262680 0%,#2656ff 100%)", "accent1": "#ffffff", "accent2": "#0265ff", "name": "露营渐变", "theme": "camping", "is_gradient": True},
    "camping_4": {"bg": "#002656", "accent1": "#6526ff", "accent2": "#026566", "name": "露营撞色", "theme": "camping", "text_color": "#ffffff"},
    "roadtrip_1": {"bg": "#0a0204", "accent1": "#00ff00", "accent2": "#4a02FF", "name": "公路暗夜", "theme": "roadtrip"},
    "roadtrip_2": {"bg": "#f0f0f0", "accent1": "#4a007f", "accent2": "#a07F22", "name": "公路清新", "theme": "roadtrip", "text_color": "#1a1a1a"},
    "roadtrip_3": {"bg": "linear-gradient(135deg,#4a4a80 0%,#4a02ff 100%)", "accent1": "#ffffff", "accent2": "#04a0ff", "name": "公路渐变", "theme": "roadtrip", "is_gradient": True},
    "roadtrip_4": {"bg": "#004a02", "accent1": "#244aff", "accent2": "#04a022", "name": "公路撞色", "theme": "roadtrip", "text_color": "#ffffff"},
    "concert_1": {"bg": "#1c1712", "accent1": "#00ff00", "accent2": "#5c37FF", "name": "演唱会暗夜", "theme": "concert"},
    "concert_2": {"bg": "#f0f0f0", "accent1": "#5c007f", "accent2": "#c37F7d", "name": "演唱会清新", "theme": "concert", "text_color": "#1a1a1a"},
    "concert_3": {"bg": "linear-gradient(135deg,#5c5c80 0%,#5c37ff 100%)", "accent1": "#ffffff", "accent2": "#05c3ff", "name": "演唱会渐变", "theme": "concert", "is_gradient": True},
    "concert_4": {"bg": "#005c37", "accent1": "#d25cff", "accent2": "#05c37d", "name": "演唱会撞色", "theme": "concert", "text_color": "#ffffff"},
    "karaoke_1": {"bg": "#0d1501", "accent1": "#00ff00", "accent2": "#ed15FF", "name": "K歌暗夜", "theme": "karaoke"},
    "karaoke_2": {"bg": "#f0f0f0", "accent1": "#6d007f", "accent2": "#d17F5a", "name": "K歌清新", "theme": "karaoke", "text_color": "#1a1a1a"},
    "karaoke_3": {"bg": "linear-gradient(135deg,#eded80 0%,#ed15ff 100%)", "accent1": "#ffffff", "accent2": "#0ed1ff", "name": "K歌渐变", "theme": "karaoke", "is_gradient": True},
    "karaoke_4": {"bg": "#00ed15", "accent1": "#a1edff", "accent2": "#0ed15a", "name": "K歌撞色", "theme": "karaoke", "text_color": "#ffffff"},
    "slow_1": {"bg": "#061a13", "accent1": "#00ff00", "accent2": "#e67aFF", "name": "慢生活暗夜", "theme": "slow"},
    "slow_2": {"bg": "#f0f0f0", "accent1": "#66007f", "accent2": "#677F29", "name": "慢生活清新", "theme": "slow", "text_color": "#1a1a1a"},
    "slow_3": {"bg": "linear-gradient(135deg,#e6e680 0%,#e67aff 100%)", "accent1": "#ffffff", "accent2": "#0e67ff", "name": "慢生活渐变", "theme": "slow", "is_gradient": True},
    "slow_4": {"bg": "#00e67a", "accent1": "#93e6ff", "accent2": "#0e67a9", "name": "慢生活撞色", "theme": "slow", "text_color": "#ffffff"},
    "eco_1": {"bg": "#1f141b", "accent1": "#00ff00", "accent2": "#bfb4FF", "name": "环保暗夜", "theme": "eco"},
    "eco_2": {"bg": "#f0f0f0", "accent1": "#3f007f", "accent2": "#fb7F4d", "name": "环保清新", "theme": "eco", "text_color": "#1a1a1a"},
    "eco_3": {"bg": "linear-gradient(135deg,#bfbf80 0%,#bfb4ff 100%)", "accent1": "#ffffff", "accent2": "#0bfbff", "name": "环保渐变", "theme": "eco", "is_gradient": True},
    "eco_4": {"bg": "#00bfb4", "accent1": "#dbbfff", "accent2": "#0bfb4d", "name": "环保撞色", "theme": "eco", "text_color": "#ffffff"},
    "diy_1": {"bg": "#0b1702", "accent1": "#00ff00", "accent2": "#0b57FF", "name": "DIY暗夜", "theme": "diy"},
    "diy_2": {"bg": "#f0f0f0", "accent1": "#0b007f", "accent2": "#b57F76", "name": "DIY清新", "theme": "diy", "text_color": "#1a1a1a"},
    "diy_3": {"bg": "linear-gradient(135deg,#0b0b80 0%,#0b57ff 100%)", "accent1": "#ffffff", "accent2": "#00b5ff", "name": "DIY渐变", "theme": "diy", "is_gradient": True},
    "diy_4": {"bg": "#000b57", "accent1": "#620bff", "accent2": "#00b576", "name": "DIY撞色", "theme": "diy", "text_color": "#ffffff"},
    "reading_1": {"bg": "#0b0517", "accent1": "#00ff00", "accent2": "#6b25FF", "name": "阅读暗夜", "theme": "reading"},
    "reading_2": {"bg": "#f0f0f0", "accent1": "#6b007f", "accent2": "#b27F5d", "name": "阅读清新", "theme": "reading", "text_color": "#1a1a1a"},
    "reading_3": {"bg": "linear-gradient(135deg,#6b6b80 0%,#6b25ff 100%)", "accent1": "#ffffff", "accent2": "#06b2ff", "name": "阅读渐变", "theme": "reading", "is_gradient": True},
    "reading_4": {"bg": "#006b25", "accent1": "#d76bff", "accent2": "#06b25d", "name": "阅读撞色", "theme": "reading", "text_color": "#ffffff"},
    "painting_1": {"bg": "#1c1c0d", "accent1": "#00ff00", "accent2": "#bc7cFF", "name": "绘画暗夜", "theme": "painting"},
    "painting_2": {"bg": "#f0f0f0", "accent1": "#3c007f", "accent2": "#c77F44", "name": "绘画清新", "theme": "painting", "text_color": "#1a1a1a"},
    "painting_3": {"bg": "linear-gradient(135deg,#bcbc80 0%,#bc7cff 100%)", "accent1": "#ffffff", "accent2": "#0bc7ff", "name": "绘画渐变", "theme": "painting", "is_gradient": True},
    "painting_4": {"bg": "#00bc7c", "accent1": "#4dbcff", "accent2": "#0bc7c4", "name": "绘画撞色", "theme": "painting", "text_color": "#ffffff"},
    "photo2_1": {"bg": "#110c17", "accent1": "#00ff00", "accent2": "#b1acFF", "name": "摄影暗夜", "theme": "photo2"},
    "photo2_2": {"bg": "#f0f0f0", "accent1": "#31007f", "accent2": "#1a7F49", "name": "摄影清新", "theme": "photo2", "text_color": "#1a1a1a"},
    "photo2_3": {"bg": "linear-gradient(135deg,#b1b180 0%,#b1acff 100%)", "accent1": "#ffffff", "accent2": "#0b1aff", "name": "摄影渐变", "theme": "photo2", "is_gradient": True},
    "photo2_4": {"bg": "#00b1ac", "accent1": "#97b1ff", "accent2": "#0b1ac9", "name": "摄影撞色", "theme": "photo2", "text_color": "#ffffff"},
    "gardening_1": {"bg": "#191e1c", "accent1": "#00ff00", "accent2": "#795eFF", "name": "园艺暗夜", "theme": "gardening"},
    "gardening_2": {"bg": "#f0f0f0", "accent1": "#79007f", "accent2": "#957F67", "name": "园艺清新", "theme": "gardening", "text_color": "#1a1a1a"},
    "gardening_3": {"bg": "linear-gradient(135deg,#797980 0%,#795eff 100%)", "accent1": "#ffffff", "accent2": "#0795ff", "name": "园艺渐变", "theme": "gardening", "is_gradient": True},
    "gardening_4": {"bg": "#00795e", "accent1": "#7c79ff", "accent2": "#0795e7", "name": "园艺撞色", "theme": "gardening", "text_color": "#ffffff"},
    "cooking_1": {"bg": "#010710", "accent1": "#00ff00", "accent2": "#41e7FF", "name": "烹饪暗夜", "theme": "cooking"},
    "cooking_2": {"bg": "#f0f0f0", "accent1": "#41007f", "accent2": "#1e7F7b", "name": "烹饪清新", "theme": "cooking", "text_color": "#1a1a1a"},
    "cooking_3": {"bg": "linear-gradient(135deg,#414180 0%,#41e7ff 100%)", "accent1": "#ffffff", "accent2": "#041eff", "name": "烹饪渐变", "theme": "cooking", "is_gradient": True},
    "cooking_4": {"bg": "#0041e7", "accent1": "#b041ff", "accent2": "#041e7b", "name": "烹饪撞色", "theme": "cooking", "text_color": "#ffffff"},
    "baking_1": {"bg": "#011a0f", "accent1": "#00ff00", "accent2": "#e1daFF", "name": "烘焙暗夜", "theme": "baking"},
    "baking_2": {"bg": "#f0f0f0", "accent1": "#61007f", "accent2": "#1d7F2e", "name": "烘焙清新", "theme": "baking", "text_color": "#1a1a1a"},
    "baking_3": {"bg": "linear-gradient(135deg,#e1e180 0%,#e1daff 100%)", "accent1": "#ffffff", "accent2": "#0e1dff", "name": "烘焙渐变", "theme": "baking", "is_gradient": True},
    "baking_4": {"bg": "#00e1da", "accent1": "#efe1ff", "accent2": "#0e1dae", "name": "烘焙撞色", "theme": "baking", "text_color": "#ffffff"},
    "cat_1": {"bg": "#081b07", "accent1": "#00ff00", "accent2": "#48bbFF", "name": "猫暗夜", "theme": "cat"},
    "cat_2": {"bg": "#f0f0f0", "accent1": "#48007f", "accent2": "#8b7F30", "name": "猫清新", "theme": "cat", "text_color": "#1a1a1a"},
    "cat_3": {"bg": "linear-gradient(135deg,#484880 0%,#48bbff 100%)", "accent1": "#ffffff", "accent2": "#048bff", "name": "猫渐变", "theme": "cat", "is_gradient": True},
    "cat_4": {"bg": "#0048bb", "accent1": "#0748ff", "accent2": "#048bb0", "name": "猫撞色", "theme": "cat", "text_color": "#ffffff"},
    "dog_1": {"bg": "#070404", "accent1": "#00ff00", "accent2": "#e764FF", "name": "狗暗夜", "theme": "dog"},
    "dog_2": {"bg": "#f0f0f0", "accent1": "#67007f", "accent2": "#767F44", "name": "狗清新", "theme": "dog", "text_color": "#1a1a1a"},
    "dog_3": {"bg": "linear-gradient(135deg,#e7e780 0%,#e764ff 100%)", "accent1": "#ffffff", "accent2": "#0e76ff", "name": "狗渐变", "theme": "dog", "is_gradient": True},
    "dog_4": {"bg": "#00e764", "accent1": "#44e7ff", "accent2": "#0e7644", "name": "狗撞色", "theme": "dog", "text_color": "#ffffff"},
    "hamster_1": {"bg": "#1d180d", "accent1": "#00ff00", "accent2": "#9d18FF", "name": "仓鼠暗夜", "theme": "hamster"},
    "hamster_2": {"bg": "#f0f0f0", "accent1": "#1d007f", "accent2": "#d17F06", "name": "仓鼠清新", "theme": "hamster", "text_color": "#1a1a1a"},
    "hamster_3": {"bg": "linear-gradient(135deg,#9d9d80 0%,#9d18ff 100%)", "accent1": "#ffffff", "accent2": "#09d1ff", "name": "仓鼠渐变", "theme": "hamster", "is_gradient": True},
    "hamster_4": {"bg": "#009d18", "accent1": "#6d9dff", "accent2": "#09d186", "name": "仓鼠撞色", "theme": "hamster", "text_color": "#ffffff"},
    "parrot_1": {"bg": "#090a14", "accent1": "#00ff00", "accent2": "#e9aaFF", "name": "鹦鹉暗夜", "theme": "parrot"},
    "parrot_2": {"bg": "#f0f0f0", "accent1": "#69007f", "accent2": "#9a7F2d", "name": "鹦鹉清新", "theme": "parrot", "text_color": "#1a1a1a"},
    "parrot_3": {"bg": "linear-gradient(135deg,#e9e980 0%,#e9aaff 100%)", "accent1": "#ffffff", "accent2": "#0e9aff", "name": "鹦鹉渐变", "theme": "parrot", "is_gradient": True},
    "parrot_4": {"bg": "#00e9aa", "accent1": "#d4e9ff", "accent2": "#0e9aad", "name": "鹦鹉撞色", "theme": "parrot", "text_color": "#ffffff"},
    "fish_1": {"bg": "#06151a", "accent1": "#00ff00", "accent2": "#c635FF", "name": "鱼暗夜", "theme": "fish"},
    "fish_2": {"bg": "#f0f0f0", "accent1": "#46007f", "accent2": "#637F5b", "name": "鱼清新", "theme": "fish", "text_color": "#1a1a1a"},
    "fish_3": {"bg": "linear-gradient(135deg,#c6c680 0%,#c635ff 100%)", "accent1": "#ffffff", "accent2": "#0c63ff", "name": "鱼渐变", "theme": "fish", "is_gradient": True},
    "fish_4": {"bg": "#00c635", "accent1": "#bac6ff", "accent2": "#0c635b", "name": "鱼撞色", "theme": "fish", "text_color": "#ffffff"},
    "hiking_1": {"bg": "#0a0b1c", "accent1": "#00ff00", "accent2": "#0aabFF", "name": "徒步暗夜", "theme": "hiking"},
    "hiking_2": {"bg": "#f0f0f0", "accent1": "#0a007f", "accent2": "#aa7F37", "name": "徒步清新", "theme": "hiking", "text_color": "#1a1a1a"},
    "hiking_3": {"bg": "linear-gradient(135deg,#0a0a80 0%,#0aabff 100%)", "accent1": "#ffffff", "accent2": "#00aaff", "name": "徒步渐变", "theme": "hiking", "is_gradient": True},
    "hiking_4": {"bg": "#000aab", "accent1": "#7c0aff", "accent2": "#00aab7", "name": "徒步撞色", "theme": "hiking", "text_color": "#ffffff"},
    "fishing_1": {"bg": "#160319", "accent1": "#00ff00", "accent2": "#d6e3FF", "name": "钓鱼暗夜", "theme": "fishing"},
    "fishing_2": {"bg": "#f0f0f0", "accent1": "#56007f", "accent2": "#6e7F33", "name": "钓鱼清新", "theme": "fishing", "text_color": "#1a1a1a"},
    "fishing_3": {"bg": "linear-gradient(135deg,#d6d680 0%,#d6e3ff 100%)", "accent1": "#ffffff", "accent2": "#0d6eff", "name": "钓鱼渐变", "theme": "fishing", "is_gradient": True},
    "fishing_4": {"bg": "#00d6e3", "accent1": "#39d6ff", "accent2": "#0d6e33", "name": "钓鱼撞色", "theme": "fishing", "text_color": "#ffffff"},
    "kayaking_1": {"bg": "#020811", "accent1": "#00ff00", "accent2": "#c288FF", "name": "皮划艇暗夜", "theme": "kayaking"},
    "kayaking_2": {"bg": "#f0f0f0", "accent1": "#42007f", "accent2": "#287F0b", "name": "皮划艇清新", "theme": "kayaking", "text_color": "#1a1a1a"},
    "kayaking_3": {"bg": "linear-gradient(135deg,#c2c280 0%,#c288ff 100%)", "accent1": "#ffffff", "accent2": "#0c28ff", "name": "皮划艇渐变", "theme": "kayaking", "is_gradient": True},
    "kayaking_4": {"bg": "#00c288", "accent1": "#b1c2ff", "accent2": "#0c288b", "name": "皮划艇撞色", "theme": "kayaking", "text_color": "#ffffff"},
    "stargazing_1": {"bg": "#061900", "accent1": "#00ff00", "accent2": "#8659FF", "name": "观星暗夜", "theme": "stargazing"},
    "stargazing_2": {"bg": "#f0f0f0", "accent1": "#06007f", "accent2": "#657F1c", "name": "观星清新", "theme": "stargazing", "text_color": "#1a1a1a"},
    "stargazing_3": {"bg": "linear-gradient(135deg,#868680 0%,#8659ff 100%)", "accent1": "#ffffff", "accent2": "#0865ff", "name": "观星渐变", "theme": "stargazing", "is_gradient": True},
    "stargazing_4": {"bg": "#008659", "accent1": "#c086ff", "accent2": "#08659c", "name": "观星撞色", "theme": "stargazing", "text_color": "#ffffff"},}

# ===== 风格结构分类 =====
THEME_CATEGORIES = {
    "科技知识": {
        "icon": "🚀",
        "desc": "适合编程、AI、技术教程、知识科普、工程",
        "themes": ["bold", "cyber", "minimal", "magazine", "pixel", "glass", "aurora", "blueprint", "typewriter", "starfield", "glitch", "synthwave", "matrix", "quantum", "ocean", "ice", "glassmorph", "retrofuturism", "galaxy", "cloud", "python", "java", "golang", "rust", "typescript", "react", "vue", "angular", "svelte", "nodejs", "mysql", "postgres", "redis", "mongo", "sqlite", "elastic", "docker", "k8s", "terraform", "jenkins", "github", "gitlab", "prometheus", "grafana", "tensorflow", "pytorch", "huggingface", "openai", "langchain", "ollama", "stable", "agent", "rag", "webpack", "vite", "tailwind", "figma", "graphql", "grpc", "kafka", "rabbit", "nginx", "spring", "ddd", "microsvc", "serverless", "security", "blockchain", "web3", "linux", "terminal", "vim", "vscode", "ssh", "cron", "regex", "restapi", "json2", "yaml", "cicd", "dataviz", "algo", "binary", "neural", "quantum2", "edge", "mesh2", "observ", "chaos", "gitops", "saas", "paas", "lowcode", "vibe", "prompt", "copilot", "embedding"],
    },
    "生活娱乐": {
        "icon": "🎉",
        "desc": "适合搞笑、美食、游戏、综艺、宠物、儿童",
        "themes": ["funny", "food", "gaming", "variety", "cute", "clay", "carnival", "popart", "candy", "basketball", "football", "tennis", "baseball", "swimming", "running", "cycling", "yoga", "climbing", "skiing", "boxing", "golf", "bbq", "sushi2", "ramen", "dessert", "coffee2", "tea", "cocktail", "wine", "beer", "milktea", "juice", "christmas", "halloween", "newyear", "midautumn", "springfestival", "valentine", "rpg", "fps", "moba", "racing", "puzzle", "sandbox", "cozy", "classical", "country", "folk", "funk", "disco", "techno", "house", "anime2", "drama", "comedy", "romance", "action", "fantasy", "mystery", "party", "picnic", "camping", "roadtrip", "concert", "karaoke", "slow", "eco", "diy", "reading", "painting", "photo2", "gardening", "cooking", "baking", "cat", "dog", "rabbit", "hamster", "parrot", "fish", "hiking", "fishing", "kayaking", "stargazing"],
    },
    "视觉冲击": {
        "icon": "💥",
        "desc": "适合热点、评测、开箱、撕纸拼贴、潮流、街头",
        "themes": ["paper", "dopamine", "doodle", "luxury", "vaporwave", "acid", "memphis", "comic", "neon", "graffiti", "brutalist", "holographic", "gradientmesh", "screenshot", "portrait", "product", "contrast", "zoom", "steampunk", "noir", "gothic", "baroque", "tribal", "artdeco", "fire", "streetwear", "psychadelic", "mosaic", "newspaper2", "techwear", "cyberpunk2", "neoncity", "medieval", "military", "cubism", "surreal", "impression", "expression", "fauvism", "dada", "construct", "destijl", "bauhaus", "artnouveau", "macro", "longexp", "tiltshift", "doubleexp", "infrared", "cyberfilm", "wuxia", "scifi", "horror", "western", "spy", "rock", "hiphop", "jazz", "edm", "punk", "metal", "blues", "reggae", "deco", "brutal2", "gothic2", "modernist", "parametric", "glam", "grunge", "preppy", "maximal", "skate", "surf", "bike", "tattoo", "fifties", "sixties", "seventies", "eighties", "nineties", "y2k2", "solarpunk", "biopunk", "nanopunk", "posthuman", "glitch2", "datamosh", "ascii", "generative", "fractal", "voronoi", "particles", "fluid", "abstract", "geometric", "opart", "kinetic", "colorfield", "monochrome", "duotone", "pattern", "ornate", "rococo", "chrome", "gold", "silver", "iridescent", "pearlescent", "matte", "glossy", "mirror", "shadow", "laser", "prism", "crystal", "diamond", "lightning", "storm", "volcano", "tsunami"],
    },
    "文艺清新": {
        "icon": "🍃",
        "desc": "适合Vlog、旅行、动漫、手账、国风、复古、自然",
        "themes": ["fresh", "anime", "cinema", "journal", "guochao", "sticker", "retro", "collage", "ink", "stamp", "newspaper", "polaroid", "risograph", "film", "ribbon", "pastel", "terrarium", "kraft", "washi", "watercolor", "zen", "scandinavian", "boho", "rain", "sunset", "forest", "desert", "vintage", "cherry", "woodcut", "plaid", "origami", "paperplane", "lofi", "wave", "fairy", "earth", "ukiyoe", "sumi_e", "mingqing", "dunhuang", "shuimo", "gongbi", "persian", "arabesque", "moroccan", "african", "aztec", "maya", "inca", "viking", "celtic", "egyptian", "greek", "roman", "byzantine", "russian", "tokyo", "kyoto", "paris", "london", "nyc", "shanghai", "chengdu", "yunnan", "tibet", "mongolia", "bamboo", "lotus", "plum", "orchid", "pine", "maple", "willow", "ginkgo", "cactus", "bonsai", "moss", "dandelion", "lavender", "sunflower", "rose", "tulip", "spring", "summer", "autumn", "winter", "snow2", "fog", "drizzle", "dawn", "dusk", "moonlight", "starlight", "mountain", "valley", "island", "harbor", "lighthouse", "bridge", "windmill", "cabin", "temple", "castle", "poetry", "novel", "fairytale", "myth", "haiku", "ceramic", "pottery", "porcelain", "lacquer", "weaving", "dyeing", "calligraphy", "seal2", "wood", "stone", "marble", "linen", "silk", "leather", "wabi", "ikigai", "hygge", "feathers", "scales", "shell", "coral"],
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


    "python": ["Python", "Django", "Flask"],
    "java": ["Java", "JVM", "Spring", "Maven"],
    "golang": ["Go", "Golang", "goroutine"],
    "rust": ["Rust", "Cargo"],
    "typescript": ["TypeScript", "TS"],
    "react": ["React", "JSX", "hook"],
    "vue": ["Vue", "Vuex"],
    "angular": ["Angular", "RxJS"],
    "svelte": ["Svelte", "编译"],
    "nodejs": ["Node", "npm", "Express"],
    "mysql": ["MySQL", "SQL", "数据库"],
    "postgres": ["PostgreSQL", "pg"],
    "redis": ["Redis", "缓存"],
    "mongo": ["MongoDB", "NoSQL"],
    "sqlite": ["SQLite", "轻量"],
    "elastic": ["Elasticsearch", "ES"],
    "docker": ["Docker", "容器"],
    "k8s": ["K8s", "Kubernetes"],
    "terraform": ["Terraform", "IaC"],
    "jenkins": ["Jenkins", "CI", "CD"],
    "github": ["GitHub", "Git"],
    "gitlab": ["GitLab"],
    "prometheus": ["Prometheus", "监控"],
    "grafana": ["Grafana", "可视化"],
    "tensorflow": ["TensorFlow", "TF"],
    "pytorch": ["PyTorch", "张量"],
    "huggingface": ["HuggingFace", "Transformers"],
    "openai": ["OpenAI", "GPT"],
    "langchain": ["LangChain", "LLM"],
    "ollama": ["Ollama", "LLM"],
    "stable": ["Stable", "Diffusion"],
    "agent": ["Agent", "智能体"],
    "rag": ["RAG", "检索增强"],
    "webpack": ["Webpack", "打包"],
    "vite": ["Vite", "ESM"],
    "tailwind": ["Tailwind", "CSS"],
    "figma": ["Figma", "设计"],
    "graphql": ["GraphQL", "查询"],
    "grpc": ["gRPC", "protobuf"],
    "kafka": ["Kafka", "消息队列"],
    "rabbit": ["兔", "rabbit"],
    "nginx": ["Nginx", "代理"],
    "spring": ["春", "spring"],
    "ddd": ["DDD", "领域驱动", "分层"],
    "microsvc": ["微服务", "microservice"],
    "serverless": ["Serverless", "Lambda"],
    "security": ["安全", "加密", "渗透"],
    "blockchain": ["区块链", "blockchain"],
    "web3": ["Web3", "DApp"],
    "linux": ["Linux", "Shell"],
    "terminal": ["终端", "Terminal", "CLI"],
    "vim": ["Vim", "Neovim"],
    "vscode": ["VSCode", "IDE"],
    "ssh": ["SSH", "远程"],
    "cron": ["cron", "定时"],
    "regex": ["正则", "regex"],
    "restapi": ["REST", "API", "接口"],
    "json2": ["JSON", "序列化"],
    "yaml": ["YAML", "配置"],
    "cicd": ["CI", "CD", "流水线"],
    "dataviz": ["可视化", "图表"],
    "algo": ["算法", "排序", "搜索"],
    "binary": ["二进制", "binary"],
    "neural": ["神经网络", "neural"],
    "quantum2": ["量子", "qubit"],
    "edge": ["边缘", "edge"],
    "mesh2": ["mesh", "Istio"],
    "observ": ["可观测", "监控"],
    "chaos": ["混沌", "chaos"],
    "gitops": ["GitOps", "ArgoCD"],
    "saas": ["SaaS", "订阅"],
    "paas": ["PaaS", "平台"],
    "lowcode": ["低代码", "lowcode"],
    "vibe": ["Vibe", "Coding"],
    "prompt": ["提示词", "prompt"],
    "copilot": ["Copilot", "AI助手"],
    "embedding": ["embedding", "向量"],
    "cubism": ["立体", "cubism"],
    "surreal": ["超现实", "surreal"],
    "impression": ["印象", "impression"],
    "expression": ["表现", "expression"],
    "fauvism": ["野兽", "fauvism"],
    "dada": ["达达", "dada"],
    "construct": ["构成", "construct"],
    "destijl": ["风格派", "DeStijl"],
    "bauhaus": ["包豪斯", "bauhaus"],
    "artnouveau": ["新艺术", "ArtNouveau"],
    "macro": ["微距", "macro"],
    "longexp": ["长曝光", "慢门"],
    "tiltshift": ["移轴", "tilt"],
    "doubleexp": ["双重曝光"],
    "infrared": ["红外", "infrared"],
    "cyberfilm": ["赛博", "电影"],
    "wuxia": ["武侠", "江湖"],
    "scifi": ["科幻", "sci-fi"],
    "horror": ["恐怖", "horror"],
    "western": ["西部", "western"],
    "spy": ["谍战", "间谍"],
    "rock": ["摇滚", "rock"],
    "hiphop": ["嘻哈", "hiphop"],
    "jazz": ["爵士", "jazz"],
    "edm": ["电音", "EDM"],
    "punk": ["朋克", "punk"],
    "metal": ["金属", "metal"],
    "blues": ["蓝调", "blues"],
    "reggae": ["雷鬼", "reggae"],
    "deco": ["装饰", "ArtDeco"],
    "brutal2": ["粗野", "混凝土"],
    "gothic2": ["哥特", "尖拱"],
    "modernist": ["现代", "modernist"],
    "parametric": ["参数", "parametric"],
    "glam": ["华丽", "glam"],
    "grunge": ["grunge", "垃圾"],
    "preppy": ["学院", "preppy"],
    "maximal": ["极繁", "maximal"],
    "skate": ["滑板", "skate"],
    "surf": ["冲浪", "surf"],
    "bike": ["骑行", "bike"],
    "tattoo": ["纹身", "tattoo"],
    "fifties": ["50年代", "复古"],
    "sixties": ["60年代", "嬉皮"],
    "seventies": ["70年代", "迪斯科"],
    "eighties": ["80年代", "霓虹"],
    "nineties": ["90年代", "街机"],
    "y2k2": ["Y2K", "千禧"],
    "solarpunk": ["太阳", "solar"],
    "biopunk": ["生物", "bio"],
    "nanopunk": ["纳米", "nano"],
    "posthuman": ["后人类", "义体"],
    "glitch2": ["故障", "glitch"],
    "datamosh": ["datamosh"],
    "ascii": ["ASCII", "字符"],
    "generative": ["生成", "generative"],
    "fractal": ["分形", "fractal"],
    "voronoi": ["voronoi"],
    "particles": ["粒子", "particle"],
    "fluid": ["流体", "fluid"],
    "abstract": ["抽象", "abstract"],
    "geometric": ["几何", "geometric"],
    "opart": ["视错觉", "OpArt"],
    "kinetic": ["动态", "kinetic"],
    "colorfield": ["色域", "color"],
    "monochrome": ["单色", "monochrome"],
    "duotone": ["双色调", "duotone"],
    "pattern": ["图案", "pattern"],
    "ornate": ["华丽", "ornate"],
    "rococo": ["洛可可", "rococo"],
    "chrome": ["镀铬", "chrome"],
    "gold": ["黄金", "gold"],
    "silver": ["白银", "silver"],
    "iridescent": ["虹彩", "iridescent"],
    "pearlescent": ["珍珠", "pearl"],
    "matte": ["哑光", "matte"],
    "glossy": ["光泽", "glossy"],
    "mirror": ["镜面", "mirror"],
    "shadow": ["阴影", "shadow"],
    "laser": ["激光", "laser"],
    "prism": ["棱镜", "prism"],
    "crystal": ["水晶", "crystal"],
    "diamond": ["钻石", "diamond"],
    "lightning": ["闪电", "lightning"],
    "storm": ["暴风", "storm"],
    "volcano": ["火山", "volcano"],
    "tsunami": ["海啸", "tsunami"],
    "ukiyoe": ["浮世绘", "ukiyoe"],
    "sumi_e": ["水墨", "sumi-e"],
    "mingqing": ["明清", "古典"],
    "dunhuang": ["敦煌", "壁画"],
    "shuimo": ["写意", "国画"],
    "gongbi": ["工笔", "精细"],
    "persian": ["波斯", "伊斯兰"],
    "arabesque": ["阿拉伯", "arabesque"],
    "moroccan": ["摩洛哥"],
    "african": ["非洲", "部落"],
    "aztec": ["阿兹特克"],
    "maya": ["玛雅"],
    "inca": ["印加"],
    "viking": ["维京", "北欧"],
    "celtic": ["凯尔特"],
    "egyptian": ["埃及", "法老"],
    "greek": ["希腊", "雅典"],
    "roman": ["罗马", "帝国"],
    "byzantine": ["拜占庭"],
    "russian": ["俄罗斯"],
    "tokyo": ["东京", "日本"],
    "kyoto": ["京都", "古都"],
    "paris": ["巴黎", "法国"],
    "london": ["伦敦", "英国"],
    "nyc": ["纽约", "美国"],
    "shanghai": ["上海", "外滩"],
    "chengdu": ["成都", "四川"],
    "yunnan": ["云南"],
    "tibet": ["西藏", "高原"],
    "mongolia": ["蒙古", "草原"],
    "bamboo": ["竹", "bamboo"],
    "lotus": ["莲", "lotus"],
    "plum": ["梅", "plum"],
    "orchid": ["兰", "orchid"],
    "pine": ["松", "pine"],
    "maple": ["枫", "maple"],
    "willow": ["柳", "willow"],
    "ginkgo": ["银杏"],
    "cactus": ["仙人掌"],
    "bonsai": ["盆景", "bonsai"],
    "moss": ["苔藓", "moss"],
    "dandelion": ["蒲公英"],
    "lavender": ["薰衣草"],
    "sunflower": ["向日葵"],
    "rose": ["玫瑰", "rose"],
    "tulip": ["郁金香"],
    "summer": ["夏", "summer"],
    "autumn": ["秋", "autumn"],
    "winter": ["冬", "winter"],
    "snow2": ["雪", "snow"],
    "fog": ["雾", "fog"],
    "drizzle": ["细雨", "drizzle"],
    "dawn": ["黎明", "dawn"],
    "dusk": ["黄昏", "dusk"],
    "moonlight": ["月光", "moon"],
    "starlight": ["星光", "star"],
    "mountain": ["山", "mountain"],
    "valley": ["山谷", "valley"],
    "island": ["岛屿", "island"],
    "harbor": ["港口", "harbor"],
    "lighthouse": ["灯塔"],
    "bridge": ["桥", "bridge"],
    "windmill": ["风车"],
    "cabin": ["小屋", "cabin"],
    "temple": ["寺庙", "temple"],
    "castle": ["城堡", "castle"],
    "poetry": ["诗", "poetry"],
    "novel": ["小说", "novel"],
    "fairytale": ["童话", "fairytale"],
    "myth": ["神话", "myth"],
    "haiku": ["俳句", "haiku"],
    "ceramic": ["陶瓷", "ceramic"],
    "pottery": ["陶器", "pottery"],
    "porcelain": ["瓷器", "porcelain"],
    "lacquer": ["漆器", "lacquer"],
    "weaving": ["编织", "weaving"],
    "dyeing": ["扎染", "dyeing"],
    "calligraphy": ["书法", "calligraphy"],
    "seal2": ["篆刻", "seal"],
    "wood": ["木纹", "wood"],
    "stone": ["石头", "stone"],
    "marble": ["大理石", "marble"],
    "linen": ["亚麻", "linen"],
    "silk": ["丝绸", "silk"],
    "leather": ["皮革", "leather"],
    "wabi": ["侘寂", "wabi"],
    "ikigai": ["ikigai"],
    "hygge": ["hygge", "舒适"],
    "feathers": ["羽毛", "feather"],
    "scales": ["鳞片", "scale"],
    "shell": ["贝壳", "shell"],
    "coral": ["珊瑚", "coral"],
    "basketball": ["篮球", "basketball"],
    "football": ["足球", "football"],
    "tennis": ["网球", "tennis"],
    "baseball": ["棒球", "baseball"],
    "swimming": ["游泳", "swimming"],
    "running": ["跑步", "running"],
    "cycling": ["自行车", "cycling"],
    "yoga": ["瑜伽", "yoga"],
    "climbing": ["攀岩", "climbing"],
    "skiing": ["滑雪", "skiing"],
    "boxing": ["拳击", "boxing"],
    "golf": ["高尔夫", "golf"],
    "bbq": ["烧烤", "bbq"],
    "sushi2": ["寿司", "sushi"],
    "ramen": ["拉面", "ramen"],
    "dessert": ["甜点", "dessert"],
    "coffee2": ["咖啡", "coffee"],
    "tea": ["茶", "tea"],
    "cocktail": ["鸡尾酒"],
    "wine": ["红酒", "wine"],
    "beer": ["啤酒", "beer"],
    "milktea": ["奶茶", "milktea"],
    "juice": ["果汁", "juice"],
    "christmas": ["圣诞", "christmas"],
    "halloween": ["万圣", "halloween"],
    "newyear": ["新年", "newyear"],
    "midautumn": ["中秋", "mooncake"],
    "springfestival": ["春节", "spring"],
    "valentine": ["情人", "valentine"],
    "rpg": ["RPG", "角色扮演"],
    "fps": ["FPS", "射击"],
    "moba": ["MOBA", "对战"],
    "racing": ["赛车", "racing"],
    "puzzle": ["解谜", "puzzle"],
    "sandbox": ["沙盒", "sandbox"],
    "cozy": ["休闲", "cozy"],
    "classical": ["古典", "classical"],
    "country": ["乡村", "country"],
    "folk": ["民谣", "folk"],
    "funk": ["放克", "funk"],
    "disco": ["迪斯科", "disco"],
    "techno": ["techno", "电子"],
    "house": ["house", "舞曲"],
    "anime2": ["动漫", "anime"],
    "drama": ["剧情", "drama"],
    "comedy": ["喜剧", "comedy"],
    "romance": ["爱情", "romance"],
    "action": ["动作", "action"],
    "fantasy": ["奇幻", "fantasy"],
    "mystery": ["悬疑", "mystery"],
    "party": ["派对", "party"],
    "picnic": ["野餐", "picnic"],
    "camping": ["露营", "camping"],
    "roadtrip": ["公路", "roadtrip"],
    "concert": ["演唱会", "concert"],
    "karaoke": ["K歌", "karaoke"],
    "slow": ["慢生活", "slow"],
    "eco": ["环保", "eco"],
    "diy": ["DIY", "手工"],
    "reading": ["阅读", "reading"],
    "painting": ["绘画", "painting"],
    "photo2": ["摄影", "photo"],
    "gardening": ["园艺", "garden"],
    "cooking": ["烹饪", "cooking"],
    "baking": ["烘焙", "baking"],
    "cat": ["猫", "cat", "猫咪"],
    "dog": ["狗", "dog", "狗狗"],
    "hamster": ["仓鼠", "hamster"],
    "parrot": ["鹦鹉", "parrot"],
    "fish": ["鱼", "fish"],
    "hiking": ["徒步", "hiking"],
    "fishing": ["钓鱼", "fishing"],
    "kayaking": ["皮划艇", "kayak"],
    "stargazing": ["观星", "star"],}

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


    "bridge": [("🌉","🌉")],
    "bamboo": [("🎋","🎋")],
    "nginx": [("🌐","🌐")],
    "gaming": [("✨","✨")],
    "seventies": [("🪩","🪩")],
    "dyeing": [("🌀","🌀")],
    "glitch2": [("📺","📺")],
    "bike": [("🚴","🚴")],
    "monochrome": [("⚫","⚫")],
    "baking": [("🥖","🥖")],
    "security": [("🔐","🔐")],
    "reggae": [("🇯🇲","🇯🇲")],
    "huggingface": [("🤗","🤗")],
    "gongbi": [("✏️","✏️")],
    "hygge": [("🕯️","🕯️")],
    "postgres": [("🐘","🐘")],
    "arabesque": [("🔯","🔯")],
    "stable": [("🎨","🎨")],
    "harbor": [("⛵","⛵")],
    "cyberpunk2": [("✨","✨")],
    "snow2": [("❄️","❄️")],
    "concert": [("🎤","🎤")],
    "mesh2": [("🕸️","🕸️")],
    "nineties": [("🎮","🎮")],
    "sushi2": [("🍣","🍣")],
    "eighties": [("📺","📺")],
    "json2": [("{}","{}")],
    "yoga": [("🧘","🧘")],
    "prompt": [("💬","💬")],
    "figma": [("🎨","🎨")],
    "military": [("✨","✨")],
    "plum": [("🌸","🌸")],
    "candy": [("✨","✨")],
    "pearlescent": [("🫧","🫧")],
    "blues": [("🎸","🎸")],
    "prometheus": [("🔥","🔥")],
    "christmas": [("🎄","🎄")],
    "embedding": [("📐","📐")],
    "carnival": [("✨","✨")],
    "basketball": [("🏀","🏀")],
    "rpg": [("⚔️","⚔️")],
    "party": [("🎉","🎉")],
    "steampunk": [("✨","✨")],
    "washi": [("✨","✨")],
    "spy": [("🕵️","🕵️")],
    "quantum2": [("⚛️","⚛️")],
    "golf": [("⛳","⛳")],
    "pattern": [("🔮","🔮")],
    "myth": [("🐉","🐉")],
    "gold": [("🥇","🥇")],
    "product": [("✨","✨")],
    "artnouveau": [("🌸","🌸")],
    "blockchain": [("⛓️","⛓️")],
    "opart": [("👁️","👁️")],
    "novel": [("📖","📖")],
    "microsvc": [("🔬","🔬")],
    "paper": [("✨","✨")],
    "summer": [("☀️","☀️")],
    "fauvism": [("🦁","🦁")],
    "drizzle": [("🌦️","🌦️")],
    "mysql": [("🐬","🐬")],
    "sunset": [("✨","✨")],
    "mosaic": [("✨","✨")],
    "coral": [("🪸","🪸")],
    "marble": [("⬜","⬜")],
    "roman": [("🏛️","🏛️")],
    "viking": [("🛡️","🛡️")],
    "kayaking": [("🛶","🛶")],
    "binary": [("01","01")],
    "cat": [("🐱","🐱")],
    "mongo": [("🍃","🍃")],
    "scifi": [("🚀","🚀")],
    "deco": [("🏙️","🏙️")],
    "polaroid": [("✨","✨")],
    "maple": [("🍁","🍁")],
    "jazz": [("🎷","🎷")],
    "blueprint": [("✨","✨")],
    "tattoo": [("🐉","🐉")],
    "generative": [("🌸","🌸")],
    "rococo": [("💝","💝")],
    "infrared": [("🔴","🔴")],
    "boho": [("✨","✨")],
    "journal": [("✨","✨")],
    "medieval": [("✨","✨")],
    "voronoi": [("🔷","🔷")],
    "swimming": [("🏊","🏊")],
    "risograph": [("✨","✨")],
    "abstract": [("🔸","🔸")],
    "persian": [("🕌","🕌")],
    "fresh": [("✨","✨")],
    "vite": [("⚡","⚡")],
    "retro": [("✨","✨")],
    "tailwind": [("💨","💨")],
    "volcano": [("🌋","🌋")],
    "aztec": [("🦅","🦅")],
    "grunge": [("🗑️","🗑️")],
    "moonlight": [("🌙","🌙")],
    "western": [("🤠","🤠")],
    "byzantine": [("☦️","☦️")],
    "lofi": [("✨","✨")],
    "svelte": [("🔥","🔥")],
    "funk": [("🕺","🕺")],
    "rabbit": [("🐰","🐰")],
    "graffiti": [("✨","✨")],
    "popart": [("✨","✨")],
    "vim": [("📝","📝")],
    "fractal": [("❄️","❄️")],
    "gothic2": [("⛪","⛪")],
    "ramen": [("🍜","🍜")],
    "tokyo": [("🗼","🗼")],
    "bauhaus": [("📐","📐")],
    "rose": [("🌹","🌹")],
    "mountain": [("⛰️","⛰️")],
    "web3": [("🌐","🌐")],
    "vscode": [("💙","💙")],
    "karaoke": [("🎵","🎵")],
    "silver": [("🥈","🥈")],
    "egyptian": [("𓂀","𓂀")],
    "newyear": [("🎉","🎉")],
    "minimal": [("✨","✨")],
    "biopunk": [("🧬","🧬")],
    "java": [("☕","☕")],
    "copilot": [("✈️","✈️")],
    "luxury": [("✨","✨")],
    "grafana": [("📊","📊")],
    "yunnan": [("🌺","🌺")],
    "ornate": [("🎊","🎊")],
    "mystery": [("🔍","🔍")],
    "chaos": [("🌪️","🌪️")],
    "picnic": [("🧺","🧺")],
    "jenkins": [("🔧","🔧")],
    "crystal": [("💎","💎")],
    "classical": [("🎼","🎼")],
    "warm": [("✨","✨")],
    "food": [("✨","✨")],
    "surf": [("🏄","🏄")],
    "cycling": [("🚴","🚴")],
    "ceramic": [("🏺","🏺")],
    "stargazing": [("🔭","🔭")],
    "agent": [("🤖","🤖")],
    "saas": [("☁️","☁️")],
    "scales": [("🐉","🐉")],
    "cyberfilm": [("🎬","🎬")],
    "russian": [("套娃","套娃")],
    "modernist": [("🏛️","🏛️")],
    "running": [("🏃","🏃")],
    "stone": [("🪨","🪨")],
    "weaving": [("🧶","🧶")],
    "lightning": [("⚡","⚡")],
    "sunflower": [("🌻","🌻")],
    "romance": [("💕","💕")],
    "tennis": [("🎾","🎾")],
    "expression": [("😨","😨")],
    "contrast": [("✨","✨")],
    "hiking": [("🥾","🥾")],
    "shanghai": [("🏙️","🏙️")],
    "datamosh": [("🗜️","🗜️")],
    "mingqing": [("🏛️","🏛️")],
    "observ": [("👁️","👁️")],
    "diamond": [("💍","💍")],
    "edge": [("📡","📡")],
    "dada": [("🎲","🎲")],
    "fishing": [("🎣","🎣")],
    "boxing": [("🥊","🥊")],
    "ginkgo": [("🍂","🍂")],
    "portrait": [("✨","✨")],
    "midautumn": [("🥮","🥮")],
    "fish": [("🐟","🐟")],
    "streetwear": [("✨","✨")],
    "cloud": [("✨","✨")],
    "iridescent": [("🌈","🌈")],
    "action": [("💥","💥")],
    "cicd": [("🔄","🔄")],
    "vintage": [("✨","✨")],
    "holographic": [("✨","✨")],
    "ice": [("✨","✨")],
    "gradientmesh": [("✨","✨")],
    "glass": [("✨","✨")],
    "willow": [("🌿","🌿")],
    "posthuman": [("🦿","🦿")],
    "clay": [("✨","✨")],
    "wood": [("🪵","🪵")],
    "cocktail": [("🍸","🍸")],
    "hiphop": [("🎤","🎤")],
    "tech": [("✨","✨")],
    "matte": [("⬛","⬛")],
    "film": [("✨","✨")],
    "starlight": [("✨","✨")],
    "fantasy": [("🐉","🐉")],
    "golang": [("🐹","🐹")],
    "tsunami": [("🌊","🌊")],
    "desert": [("✨","✨")],
    "metal": [("🤘","🤘")],
    "folk": [("🪕","🪕")],
    "restapi": [("🔗","🔗")],
    "gitlab": [("🦊","🦊")],
    "sqlite": [("🪶","🪶")],
    "rock": [("🤘","🤘")],
    "lotus": [("🪷","🪷")],
    "painting": [("🎨","🎨")],
    "starfield": [("✨","✨")],
    "react": [("⚛️","⚛️")],
    "sticker": [("✨","✨")],
    "terraform": [("🌍","🌍")],
    "bbq": [("🔥","🔥")],
    "ssh": [("🔑","🔑")],
    "maya": [("🗿","🗿")],
    "stamp": [("✨","✨")],
    "london": [("🎡","🎡")],
    "rain": [("✨","✨")],
    "sandbox": [("🏜️","🏜️")],
    "neon": [("✨","✨")],
    "eco": [("🌱","🌱")],
    "cool": [("✨","✨")],
    "lavender": [("💜","💜")],
    "winter": [("❄️","❄️")],
    "anime": [("✨","✨")],
    "ddd": [("🏛️","🏛️")],
    "lacquer": [("🪵","🪵")],
    "techwear": [("✨","✨")],
    "chrome": [("🪙","🪙")],
    "geometric": [("🔺","🔺")],
    "zoom": [("✨","✨")],
    "preppy": [("🎓","🎓")],
    "dawn": [("🌅","🌅")],
    "vibe": [("🎵","🎵")],
    "acid": [("✨","✨")],
    "tensorflow": [("🌊","🌊")],
    "lowcode": [("🧩","🧩")],
    "macro": [("🔬","🔬")],
    "gardening": [("🌱","🌱")],
    "fire": [("✨","✨")],
    "bonsai": [("🪴","🪴")],
    "parametric": [("〰️","〰️")],
    "destijl": [("⬜","⬜")],
    "hamster": [("🐹","🐹")],
    "woodcut": [("✨","✨")],
    "anime2": [("🌸","🌸")],
    "pixel": [("✨","✨")],
    "halloween": [("🎃","🎃")],
    "psychadelic": [("✨","✨")],
    "wine": [("🍷","🍷")],
    "cooking": [("👨‍🍳","👨‍🍳")],
    "milktea": [("🧋","🧋")],
    "laser": [("🔴","🔴")],
    "fairytale": [("🧚","🧚")],
    "origami": [("✨","✨")],
    "house": [("🏠","🏠")],
    "climbing": [("🧗","🧗")],
    "grpc": [("🔌","🔌")],
    "vaporwave": [("✨","✨")],
    "magazine": [("✨","✨")],
    "dataviz": [("📈","📈")],
    "sixties": [("☮️","☮️")],
    "football": [("⚽","⚽")],
    "shadow": [("🌑","🌑")],
    "feathers": [("🪶","🪶")],
    "slow": [("🐌","🐌")],
    "mongolia": [("🐎","🐎")],
    "baroque": [("✨","✨")],
    "mirror": [("🪞","🪞")],
    "pine": [("🌲","🌲")],
    "tiltshift": [("🎰","🎰")],
    "racing": [("🏎️","🏎️")],
    "dunhuang": [("飞天","飞天")],
    "cozy": [("🛋️","🛋️")],
    "guochao": [("✨","✨")],
    "horror": [("💀","💀")],
    "rust": [("🦀","🦀")],
    "paas": [("🏗️","🏗️")],
    "noir": [("✨","✨")],
    "tulip": [("🌷","🌷")],
    "greek": [("🏛️","🏛️")],
    "coffee2": [("☕","☕")],
    "poetry": [("📜","📜")],
    "puzzle": [("🧩","🧩")],
    "gitops": [("🔄","🔄")],
    "camping": [("⛺","⛺")],
    "orchid": [("🌷","🌷")],
    "beer": [("🍺","🍺")],
    "yaml": [("📋","📋")],
    "edm": [("🎧","🎧")],
    "cinema": [("✨","✨")],
    "paperplane": [("✨","✨")],
    "k8s": [("⚓","⚓")],
    "cubism": [("🔺","🔺")],
    "artdeco": [("✨","✨")],
    "hot": [("✨","✨")],
    "spring": [("🌸","🌸")],
    "chengdu": [("🐼","🐼")],
    "typescript": [("🔷","🔷")],
    "cactus": [("🌵","🌵")],
    "memphis": [("✨","✨")],
    "neural": [("🧠","🧠")],
    "screenshot": [("✨","✨")],
    "zen": [("✨","✨")],
    "cherry": [("✨","✨")],
    "kafka": [("📨","📨")],
    "fluid": [("🌊","🌊")],
    "tribal": [("✨","✨")],
    "valley": [("🏞️","🏞️")],
    "cute": [("✨","✨")],
    "tibet": [("🏔️","🏔️")],
    "comic": [("✨","✨")],
    "fairy": [("✨","✨")],
    "cyber": [("✨","✨")],
    "nodejs": [("⬡","⬡")],
    "sumi_e": [("🎨","🎨")],
    "prism": [("🔺","🔺")],
    "openai": [("🧠","🧠")],
    "graphql": [("◈","◈")],
    "glitch": [("✨","✨")],
    "glassmorph": [("✨","✨")],
    "kinetic": [("🌀","🌀")],
    "seal2": [("🔲","🔲")],
    "dandelion": [("🌼","🌼")],
    "temple": [("🛕","🛕")],
    "langchain": [("🔗","🔗")],
    "dopamine": [("✨","✨")],
    "dessert": [("🍰","🍰")],
    "terminal": [("⌨️","⌨️")],
    "paris": [("🗼","🗼")],
    "python": [("🐍","🐍")],
    "leather": [("👜","👜")],
    "aurora": [("✨","✨")],
    "shell": [("🐚","🐚")],
    "watercolor": [("✨","✨")],
    "galaxy": [("✨","✨")],
    "storm": [("🌪️","🌪️")],
    "moroccan": [("🏛️","🏛️")],
    "angular": [("🛡️","🛡️")],
    "wabi": [("🍂","🍂")],
    "gothic": [("✨","✨")],
    "pytorch": [("🔥","🔥")],
    "fps": [("🎯","🎯")],
    "diy": [("🔨","🔨")],
    "duotone": [("🔵","🔵")],
    "skate": [("🛹","🛹")],
    "photo2": [("📷","📷")],
    "drama": [("🎭","🎭")],
    "animal": [("✨","✨")],
    "typewriter": [("✨","✨")],
    "castle": [("🏰","🏰")],
    "porcelain": [("🍵","🍵")],
    "moba": [("🏰","🏰")],
    "bold": [("✨","✨")],
    "colorfield": [("🟦","🟦")],
    "variety": [("✨","✨")],
    "y2k2": [("💿","💿")],
    "gradient": [("✨","✨")],
    "springfestival": [("🧧","🧧")],
    "wave": [("✨","✨")],
    "forest": [("✨","✨")],
    "cron": [("⏰","⏰")],
    "juice": [("🧃","🧃")],
    "dog": [("🐶","🐶")],
    "webpack": [("📦","📦")],
    "solarpunk": [("☀️","☀️")],
    "longexp": [("⏳","⏳")],
    "dusk": [("🌆","🌆")],
    "ollama": [("🦙","🦙")],
    "pastel": [("✨","✨")],
    "algo": [("🧮","🧮")],
    "african": [("🪘","🪘")],
    "calligraphy": [("✒️","✒️")],
    "newspaper": [("✨","✨")],
    "doubleexp": [("👻","👻")],
    "techno": [("⚙️","⚙️")],
    "funny": [("✨","✨")],
    "inca": [("⛰️","⛰️")],
    "autumn": [("🍂","🍂")],
    "terrarium": [("✨","✨")],
    "tea": [("🍵","🍵")],
    "punk": [("🦷","🦷")],
    "ink": [("✨","✨")],
    "serverless": [("☁️","☁️")],
    "elastic": [("🔍","🔍")],
    "particles": [("✨","✨")],
    "disco": [("🪩","🪩")],
    "baseball": [("⚾","⚾")],
    "fifties": [("📻","📻")],
    "haiku": [("🌸","🌸")],
    "parrot": [("🦜","🦜")],
    "plaid": [("✨","✨")],
    "kyoto": [("⛩️","⛩️")],
    "neoncity": [("✨","✨")],
    "reading": [("📚","📚")],
    "celtic": [("☘️","☘️")],
    "island": [("🏝️","🏝️")],
    "quantum": [("✨","✨")],
    "newspaper2": [("✨","✨")],
    "vue": [("🌿","🌿")],
    "lighthouse": [("🗼","🗼")],
    "glossy": [("💎","💎")],
    "brutal2": [("🏢","🏢")],
    "github": [("🐙","🐙")],
    "wuxia": [("⚔️","⚔️")],
    "kraft": [("✨","✨")],
    "maximal": [("🎊","🎊")],
    "comedy": [("😂","😂")],
    "earth": [("✨","✨")],
    "matrix": [("✨","✨")],
    "linen": [("🧵","🧵")],
    "valentine": [("💝","💝")],
    "construct": [("⬛","⬛")],
    "country": [("🤠","🤠")],
    "linux": [("🐧","🐧")],
    "rag": [("📚","📚")],
    "shuimo": [("🖌️","🖌️")],
    "dark": [("✨","✨")],
    "glam": [("✨","✨")],
    "retrofuturism": [("✨","✨")],
    "silk": [("🧣","🧣")],
    "ikigai": [("☀️","☀️")],
    "ukiyoe": [("🌊","🌊")],
    "collage": [("✨","✨")],
    "impression": [("🎨","🎨")],
    "ascii": [("█","█")],
    "redis": [("🟥","🟥")],
    "ocean": [("✨","✨")],
    "cabin": [("🏡","🏡")],
    "surreal": [("🌀","🌀")],
    "brutalist": [("✨","✨")],
    "roadtrip": [("🚗","🚗")],
    "nyc": [("🗽","🗽")],
    "ribbon": [("✨","✨")],
    "doodle": [("✨","✨")],
    "pottery": [("🪔","🪔")],
    "fog": [("🌫️","🌫️")],
    "docker": [("🐳","🐳")],
    "scandinavian": [("✨","✨")],
    "moss": [("🟢","🟢")],
    "synthwave": [("✨","✨")],
    "regex": [("🔎","🔎")],
    "windmill": [("🌬️","🌬️")],
    "skiing": [("⛷️","⛷️")],
    "nanopunk": [("🔬","🔬")],}

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


    "bridge": "coder",
    "bamboo": "tech",
    "nginx": "tech",
    "gaming": "animal",
    "seventies": "coder",
    "dyeing": "tech",
    "glitch2": "animal",
    "bike": "coder",
    "monochrome": "coder",
    "baking": "coder",
    "security": "coder",
    "reggae": "coder",
    "huggingface": "emoji",
    "gongbi": "coder",
    "hygge": "tech",
    "postgres": "tech",
    "arabesque": "emoji",
    "stable": "food",
    "harbor": "emoji",
    "cyberpunk2": "animal",
    "snow2": "food",
    "concert": "animal",
    "mesh2": "food",
    "nineties": "coder",
    "sushi2": "food",
    "eighties": "food",
    "json2": "food",
    "yoga": "animal",
    "prompt": "food",
    "figma": "animal",
    "military": "animal",
    "plum": "animal",
    "candy": "emoji",
    "pearlescent": "food",
    "blues": "animal",
    "prometheus": "coder",
    "christmas": "animal",
    "embedding": "emoji",
    "carnival": "coder",
    "basketball": "food",
    "rpg": "coder",
    "party": "animal",
    "steampunk": "animal",
    "washi": "emoji",
    "spy": "tech",
    "quantum2": "tech",
    "golf": "coder",
    "pattern": "tech",
    "myth": "tech",
    "gold": "tech",
    "product": "tech",
    "artnouveau": "tech",
    "blockchain": "food",
    "opart": "tech",
    "novel": "emoji",
    "microsvc": "food",
    "paper": "coder",
    "summer": "animal",
    "fauvism": "coder",
    "drizzle": "animal",
    "mysql": "animal",
    "sunset": "emoji",
    "mosaic": "animal",
    "coral": "emoji",
    "marble": "coder",
    "roman": "emoji",
    "viking": "food",
    "kayaking": "animal",
    "binary": "tech",
    "cat": "emoji",
    "mongo": "food",
    "scifi": "animal",
    "deco": "emoji",
    "polaroid": "animal",
    "maple": "coder",
    "jazz": "emoji",
    "blueprint": "tech",
    "tattoo": "animal",
    "generative": "animal",
    "rococo": "food",
    "infrared": "emoji",
    "boho": "emoji",
    "journal": "tech",
    "medieval": "food",
    "voronoi": "tech",
    "swimming": "animal",
    "risograph": "emoji",
    "abstract": "food",
    "persian": "tech",
    "fresh": "coder",
    "vite": "emoji",
    "retro": "tech",
    "tailwind": "food",
    "volcano": "coder",
    "aztec": "tech",
    "grunge": "animal",
    "moonlight": "coder",
    "western": "emoji",
    "byzantine": "animal",
    "lofi": "coder",
    "svelte": "food",
    "funk": "animal",
    "rabbit": "tech",
    "graffiti": "tech",
    "popart": "tech",
    "vim": "animal",
    "fractal": "coder",
    "gothic2": "emoji",
    "ramen": "coder",
    "tokyo": "food",
    "bauhaus": "emoji",
    "rose": "animal",
    "mountain": "coder",
    "web3": "food",
    "vscode": "coder",
    "karaoke": "coder",
    "silver": "food",
    "egyptian": "food",
    "newyear": "animal",
    "minimal": "emoji",
    "biopunk": "emoji",
    "java": "animal",
    "copilot": "food",
    "luxury": "coder",
    "grafana": "animal",
    "yunnan": "food",
    "ornate": "food",
    "mystery": "food",
    "chaos": "animal",
    "picnic": "animal",
    "jenkins": "emoji",
    "crystal": "food",
    "classical": "emoji",
    "warm": "emoji",
    "food": "food",
    "surf": "emoji",
    "cycling": "tech",
    "ceramic": "food",
    "stargazing": "tech",
    "agent": "coder",
    "saas": "animal",
    "scales": "tech",
    "cyberfilm": "animal",
    "russian": "emoji",
    "modernist": "emoji",
    "running": "tech",
    "stone": "animal",
    "weaving": "food",
    "lightning": "coder",
    "sunflower": "animal",
    "romance": "emoji",
    "tennis": "tech",
    "expression": "emoji",
    "contrast": "tech",
    "hiking": "emoji",
    "shanghai": "animal",
    "datamosh": "food",
    "mingqing": "coder",
    "observ": "animal",
    "diamond": "animal",
    "edge": "food",
    "dada": "tech",
    "fishing": "emoji",
    "boxing": "tech",
    "ginkgo": "tech",
    "portrait": "tech",
    "midautumn": "emoji",
    "fish": "food",
    "streetwear": "food",
    "cloud": "food",
    "iridescent": "animal",
    "action": "coder",
    "cicd": "coder",
    "vintage": "animal",
    "holographic": "coder",
    "ice": "animal",
    "gradientmesh": "tech",
    "glass": "emoji",
    "willow": "animal",
    "posthuman": "coder",
    "clay": "emoji",
    "wood": "food",
    "cocktail": "tech",
    "hiphop": "coder",
    "tech": "coder",
    "matte": "tech",
    "film": "emoji",
    "starlight": "tech",
    "fantasy": "emoji",
    "golang": "food",
    "tsunami": "tech",
    "desert": "food",
    "metal": "tech",
    "folk": "animal",
    "restapi": "emoji",
    "gitlab": "emoji",
    "sqlite": "food",
    "rock": "coder",
    "lotus": "coder",
    "painting": "tech",
    "starfield": "animal",
    "react": "emoji",
    "sticker": "coder",
    "terraform": "emoji",
    "bbq": "coder",
    "ssh": "food",
    "maya": "tech",
    "stamp": "emoji",
    "london": "animal",
    "rain": "tech",
    "sandbox": "tech",
    "neon": "tech",
    "eco": "food",
    "cool": "food",
    "lavender": "emoji",
    "winter": "tech",
    "anime": "emoji",
    "ddd": "animal",
    "lacquer": "emoji",
    "techwear": "coder",
    "chrome": "tech",
    "geometric": "coder",
    "zoom": "coder",
    "preppy": "emoji",
    "dawn": "animal",
    "vibe": "food",
    "acid": "emoji",
    "tensorflow": "emoji",
    "lowcode": "emoji",
    "macro": "animal",
    "gardening": "emoji",
    "fire": "animal",
    "bonsai": "tech",
    "parametric": "food",
    "destijl": "emoji",
    "hamster": "emoji",
    "woodcut": "coder",
    "anime2": "animal",
    "pixel": "coder",
    "halloween": "tech",
    "psychadelic": "emoji",
    "wine": "food",
    "cooking": "animal",
    "milktea": "food",
    "laser": "coder",
    "fairytale": "animal",
    "origami": "animal",
    "house": "emoji",
    "climbing": "food",
    "grpc": "emoji",
    "vaporwave": "emoji",
    "magazine": "animal",
    "dataviz": "emoji",
    "sixties": "coder",
    "football": "food",
    "shadow": "food",
    "feathers": "animal",
    "slow": "emoji",
    "mongolia": "animal",
    "baroque": "food",
    "mirror": "food",
    "pine": "emoji",
    "tiltshift": "coder",
    "racing": "food",
    "dunhuang": "tech",
    "cozy": "tech",
    "guochao": "tech",
    "horror": "emoji",
    "rust": "tech",
    "paas": "food",
    "noir": "emoji",
    "tulip": "food",
    "greek": "animal",
    "coffee2": "animal",
    "poetry": "coder",
    "puzzle": "food",
    "gitops": "food",
    "camping": "food",
    "orchid": "emoji",
    "beer": "tech",
    "yaml": "tech",
    "edm": "coder",
    "cinema": "emoji",
    "paperplane": "animal",
    "k8s": "food",
    "cubism": "emoji",
    "artdeco": "tech",
    "hot": "coder",
    "spring": "food",
    "chengdu": "food",
    "typescript": "coder",
    "cactus": "food",
    "memphis": "food",
    "neural": "coder",
    "screenshot": "coder",
    "zen": "tech",
    "cherry": "emoji",
    "kafka": "animal",
    "fluid": "food",
    "tribal": "tech",
    "valley": "tech",
    "cute": "tech",
    "tibet": "food",
    "comic": "tech",
    "fairy": "coder",
    "cyber": "emoji",
    "nodejs": "animal",
    "sumi_e": "food",
    "prism": "coder",
    "openai": "food",
    "graphql": "tech",
    "glitch": "animal",
    "glassmorph": "tech",
    "kinetic": "tech",
    "seal2": "food",
    "dandelion": "food",
    "temple": "tech",
    "langchain": "tech",
    "dopamine": "coder",
    "dessert": "coder",
    "terminal": "tech",
    "paris": "animal",
    "python": "tech",
    "leather": "emoji",
    "aurora": "animal",
    "shell": "food",
    "watercolor": "coder",
    "galaxy": "emoji",
    "storm": "animal",
    "moroccan": "animal",
    "angular": "tech",
    "wabi": "animal",
    "gothic": "tech",
    "pytorch": "emoji",
    "fps": "coder",
    "diy": "coder",
    "duotone": "food",
    "skate": "animal",
    "photo2": "food",
    "drama": "animal",
    "animal": "animal",
    "typewriter": "tech",
    "castle": "food",
    "porcelain": "tech",
    "moba": "emoji",
    "bold": "animal",
    "colorfield": "coder",
    "variety": "coder",
    "y2k2": "tech",
    "gradient": "food",
    "springfestival": "food",
    "wave": "emoji",
    "forest": "animal",
    "cron": "food",
    "juice": "animal",
    "dog": "animal",
    "webpack": "animal",
    "solarpunk": "animal",
    "longexp": "animal",
    "dusk": "coder",
    "ollama": "emoji",
    "pastel": "emoji",
    "algo": "tech",
    "african": "animal",
    "calligraphy": "food",
    "newspaper": "animal",
    "doubleexp": "tech",
    "techno": "coder",
    "funny": "tech",
    "inca": "coder",
    "autumn": "food",
    "terrarium": "food",
    "tea": "food",
    "punk": "coder",
    "ink": "tech",
    "serverless": "animal",
    "elastic": "emoji",
    "particles": "food",
    "disco": "emoji",
    "baseball": "coder",
    "fifties": "coder",
    "haiku": "emoji",
    "parrot": "emoji",
    "plaid": "coder",
    "kyoto": "animal",
    "neoncity": "food",
    "reading": "animal",
    "celtic": "coder",
    "island": "food",
    "quantum": "animal",
    "newspaper2": "animal",
    "vue": "coder",
    "lighthouse": "animal",
    "glossy": "coder",
    "brutal2": "tech",
    "github": "animal",
    "wuxia": "emoji",
    "kraft": "coder",
    "maximal": "food",
    "comedy": "animal",
    "earth": "coder",
    "matrix": "coder",
    "linen": "emoji",
    "valentine": "coder",
    "construct": "coder",
    "country": "coder",
    "linux": "animal",
    "rag": "tech",
    "shuimo": "animal",
    "dark": "animal",
    "glam": "emoji",
    "retrofuturism": "coder",
    "silk": "emoji",
    "ikigai": "food",
    "ukiyoe": "animal",
    "collage": "animal",
    "impression": "food",
    "ascii": "coder",
    "redis": "emoji",
    "ocean": "food",
    "cabin": "animal",
    "surreal": "emoji",
    "brutalist": "tech",
    "roadtrip": "emoji",
    "nyc": "coder",
    "ribbon": "tech",
    "doodle": "food",
    "pottery": "animal",
    "fog": "emoji",
    "docker": "emoji",
    "scandinavian": "animal",
    "moss": "food",
    "synthwave": "emoji",
    "regex": "food",
    "windmill": "emoji",
    "skiing": "emoji",
    "nanopunk": "emoji",}

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
    # v10新增330种风格
    for theme in ["python", "java", "golang", "rust", "typescript", "react", "vue", "angular", "svelte", "nodejs", "mysql", "postgres", "redis", "mongo", "sqlite", "elastic", "docker", "k8s", "terraform", "jenkins", "github", "gitlab", "prometheus", "grafana", "tensorflow", "pytorch", "huggingface", "openai", "langchain", "ollama", "stable", "agent", "rag", "webpack", "vite", "tailwind", "figma", "graphql", "grpc", "kafka", "rabbit", "nginx", "spring", "ddd", "microsvc", "serverless", "security", "blockchain", "web3", "linux", "terminal", "vim", "vscode", "ssh", "cron", "regex", "restapi", "json2", "yaml", "cicd", "dataviz", "algo", "binary", "neural", "quantum2", "edge", "mesh2", "observ", "chaos", "gitops", "saas", "paas", "lowcode", "vibe", "prompt", "copilot", "embedding", "cubism", "surreal", "impression", "expression", "fauvism", "dada", "construct", "destijl", "bauhaus", "artnouveau", "macro", "longexp", "tiltshift", "doubleexp", "infrared", "cyberfilm", "wuxia", "scifi", "horror", "western", "spy", "rock", "hiphop", "jazz", "edm", "punk", "metal", "blues", "reggae", "deco", "brutal2", "gothic2", "modernist", "parametric", "glam", "grunge", "preppy", "maximal", "skate", "surf", "bike", "tattoo", "fifties", "sixties", "seventies", "eighties", "nineties", "y2k2", "solarpunk", "biopunk", "nanopunk", "posthuman", "glitch2", "datamosh", "ascii", "generative", "fractal", "voronoi", "particles", "fluid", "abstract", "geometric", "opart", "kinetic", "colorfield", "monochrome", "duotone", "pattern", "ornate", "rococo", "chrome", "gold", "silver", "iridescent", "pearlescent", "matte", "glossy", "mirror", "shadow", "laser", "prism", "crystal", "diamond", "lightning", "storm", "volcano", "tsunami", "ukiyoe", "sumi_e", "mingqing", "dunhuang", "shuimo", "gongbi", "persian", "arabesque", "moroccan", "african", "aztec", "maya", "inca", "viking", "celtic", "egyptian", "greek", "roman", "byzantine", "russian", "tokyo", "kyoto", "paris", "london", "nyc", "shanghai", "chengdu", "yunnan", "tibet", "mongolia", "bamboo", "lotus", "plum", "orchid", "pine", "maple", "willow", "ginkgo", "cactus", "bonsai", "moss", "dandelion", "lavender", "sunflower", "rose", "tulip", "summer", "autumn", "winter", "snow2", "fog", "drizzle", "dawn", "dusk", "moonlight", "starlight", "mountain", "valley", "island", "harbor", "lighthouse", "bridge", "windmill", "cabin", "temple", "castle", "poetry", "novel", "fairytale", "myth", "haiku", "ceramic", "pottery", "porcelain", "lacquer", "weaving", "dyeing", "calligraphy", "seal2", "wood", "stone", "marble", "linen", "silk", "leather", "wabi", "ikigai", "hygge", "feathers", "scales", "shell", "coral", "basketball", "football", "tennis", "baseball", "swimming", "running", "cycling", "yoga", "climbing", "skiing", "boxing", "golf", "bbq", "sushi2", "ramen", "dessert", "coffee2", "tea", "cocktail", "wine", "beer", "milktea", "juice", "christmas", "halloween", "newyear", "midautumn", "springfestival", "valentine", "rpg", "fps", "moba", "racing", "puzzle", "sandbox", "cozy", "classical", "country", "folk", "funk", "disco", "techno", "house", "anime2", "drama", "comedy", "romance", "action", "fantasy", "mystery", "party", "picnic", "camping", "roadtrip", "concert", "karaoke", "slow", "eco", "diy", "reading", "painting", "photo2", "gardening", "cooking", "baking", "cat", "dog", "hamster", "parrot", "fish", "hiking", "fishing", "kayaking", "stargazing"]:
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


# ========== 文艺清新类 全面差异化重设计 ==========

# ===== fresh 清新治愈 — 整图加柔和渐变 + 透明叶片叠加 =====
.theme-fresh::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(255,255,255,0.3) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(74,222,128,0.15) 0%, transparent 50%);
}
.theme-fresh .cv-bg-decoration::before {
  content:''; position:absolute; top:-20px; right:-20px; width:200px; height:200px; pointer-events:none;
  background:radial-gradient(circle, rgba(134,239,172,0.4) 0%, transparent 70%); border-radius:50%;
}
.theme-fresh .cv-bg-decoration::after {
  content:''; position:absolute; bottom:0; left:0; right:0; height:60%;
  background:linear-gradient(to top, rgba(74,222,128,0.08) 0%, transparent 100%);
}
.theme-fresh .cv-content { background:linear-gradient(180deg, transparent 0%, rgba(255,255,255,0.05) 100%); }

# ===== anime 二次元 — 巨大渐变放射圆 + 半透明装饰带 =====
.theme-anime::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:radial-gradient(circle at 70% 30%, var(--accent2) 0%, transparent 35%);
  opacity:0.4;
}
.theme-anime .cv-bg-decoration::before {
  content:'★'; position:absolute; top:10%; left:8%; font-size:80px; color:var(--accent2);
  opacity:0.2; text-shadow:0 0 20px var(--accent2);
  animation: animeStar 4s ease-in-out infinite;
}
@keyframes animeStar { 0%,100%{transform:scale(1) rotate(0);} 50%{transform:scale(1.2) rotate(20deg);} }
.theme-anime .cv-bg-decoration::after {
  content:'✦'; position:absolute; bottom:15%; right:10%; font-size:60px; color:var(--accent1);
  opacity:0.3;
}
.theme-anime .cv-content::before {
  content:''; position:absolute; top:0; left:0; right:0; height:6px;
  background:linear-gradient(90deg, var(--accent1) 0%, var(--accent2) 50%, var(--accent1) 100%);
}

# ===== cinema 影视悬疑 — 顶部胶片孔 + 底部黑边 + 大模糊 =====
.theme-cinema .cv-bg-decoration::before {
  content:''; position:absolute; top:0; left:0; right:0; height:20px;
  background:repeating-linear-gradient(90deg, #000 0px, #000 30px, #1a1a1a 30px, #1a1a1a 40px);
  border-bottom:2px solid #000;
}
.theme-cinema .cv-bg-decoration::after {
  content:''; position:absolute; bottom:0; left:0; right:0; height:20px;
  background:repeating-linear-gradient(90deg, #000 0px, #000 30px, #1a1a1a 30px, #1a1a1a 40px);
  border-top:2px solid #000;
}
.theme-cinema::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:radial-gradient(ellipse at center, transparent 30%, rgba(0,0,0,0.6) 100%);
}
.theme-cinema .cv-content { padding-top:60px !important; padding-bottom:60px !important; }

# ===== journal 手账 — 胶带斜贴 + 虚线缝纫线 + 圆点矩阵 =====
.theme-journal::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background-image:radial-gradient(circle, rgba(0,0,0,0.06) 1.5px, transparent 1.5px);
  background-size:24px 24px;
}
.theme-journal .cv-bg-decoration::before {
  content:''; position:absolute; top:8px; right:20px; width:80px; height:24px;
  background:rgba(251,191,36,0.5); transform:rotate(-8deg);
  box-shadow:0 2px 6px rgba(0,0,0,0.1);
}
.theme-journal .cv-bg-decoration::after {
  content:''; position:absolute; bottom:8px; left:20px; width:80px; height:24px;
  background:rgba(236,72,153,0.5); transform:rotate(5deg);
  box-shadow:0 2px 6px rgba(0,0,0,0.1);
}
.theme-journal .cv-content::before {
  content:''; position:absolute; top:50%; left:0; right:0; height:0;
  border-top:2px dashed rgba(0,0,0,0.15);
}

# ===== guochao 国潮 — 红色印章 + 祥云 + 山水画 =====
.theme-guochao::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(circle at 15% 85%, rgba(220,38,38,0.15) 0%, transparent 30%),
    radial-gradient(circle at 85% 15%, rgba(220,38,38,0.1) 0%, transparent 30%);
}
.theme-guochao .cv-bg-decoration::after {
  content:'印'; position:absolute; top:15px; right:15px; width:60px; height:60px;
  background:#dc2626; color:#fef3c7; font-size:32px; font-weight:900;
  display:flex; align-items:center; justify-content:center;
  border:3px solid #fef3c7; border-radius:6px;
  transform:rotate(-8deg); box-shadow:0 2px 8px rgba(0,0,0,0.3);
  font-family:'Ma Shan Zheng', 'Noto Serif SC', serif;
}
.theme-guochao .cv-content::before {
  content:'祥云'; position:absolute; top:50%; left:20px; transform:translateY(-50%);
  font-size:24px; opacity:0.2; color:#dc2626; font-family:serif;
}
.theme-guochao .cv-content::after {
  content:'山'; position:absolute; bottom:80px; right:30px; font-size:60px;
  opacity:0.15; color:#1e3a5f; font-family:'Ma Shan Zheng', serif;
}

# ===== sticker 贴纸 — 倾斜白边贴纸 + 阴影叠加 =====
.theme-sticker::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:repeating-linear-gradient(45deg, transparent 0px, transparent 20px, rgba(0,0,0,0.02) 20px, rgba(0,0,0,0.02) 22px);
}
.theme-sticker .cv-bg-decoration::before {
  content:''; position:absolute; top:30%; left:5%; width:40px; height:40px;
  background:var(--accent1); border:3px solid #fff; border-radius:50%;
  box-shadow:3px 3px 0 rgba(0,0,0,0.2); transform:rotate(-15deg);
}
.theme-sticker .cv-bg-decoration::after {
  content:''; position:absolute; bottom:25%; right:8%; width:50px; height:50px;
  background:var(--accent2); border:3px solid #fff; transform:rotate(20deg);
  box-shadow:3px 3px 0 rgba(0,0,0,0.2);
}
.theme-sticker .cv-mascot { transform:rotate(-8deg) !important; }

# ===== retro 复古胶片 — 整体米黄 + 颗粒 + 暗角 =====
.theme-retro::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.4) 100%),
    repeating-linear-gradient(0deg, transparent 0px, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 3px);
  mix-blend-mode:multiply;
}
.theme-retro .cv-bg-decoration::before {
  content:''; position:absolute; inset:12px; border:2px solid rgba(0,0,0,0.2); border-radius:4px;
  pointer-events:none;
}
.theme-retro .cv-content { filter:sepia(0.15) contrast(1.05); }

# ===== collage 拼贴 — 多张倾斜的色块纸张叠放 =====
.theme-collage::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    linear-gradient(135deg, transparent 40%, rgba(251,191,36,0.15) 40%, rgba(251,191,36,0.15) 45%, transparent 45%),
    linear-gradient(225deg, transparent 60%, rgba(236,72,153,0.15) 60%, rgba(236,72,153,0.15) 65%, transparent 65%);
}
.theme-collage .cv-bg-decoration::before {
  content:''; position:absolute; top:20px; right:30px; width:90px; height:120px;
  background:var(--accent1); transform:rotate(8deg); box-shadow:3px 3px 8px rgba(0,0,0,0.2);
  border:2px solid #fff;
}
.theme-collage .cv-bg-decoration::after {
  content:''; position:absolute; bottom:30px; left:20px; width:80px; height:100px;
  background:var(--accent2); transform:rotate(-6deg); box-shadow:3px 3px 8px rgba(0,0,0,0.2);
  border:2px solid #fff;
}
.theme-collage .cv-mascot { transform:rotate(4deg) !important; }

# ===== ink 水墨 — 黑色墨迹晕染 + 留白 =====
.theme-ink::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 10% 20%, rgba(0,0,0,0.4) 0%, transparent 25%),
    radial-gradient(ellipse at 90% 80%, rgba(0,0,0,0.3) 0%, transparent 20%),
    radial-gradient(circle at 50% 50%, transparent 30%, rgba(255,255,255,0.1) 100%);
}
.theme-ink .cv-bg-decoration::before {
  content:'墨'; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  font-size:200px; color:rgba(0,0,0,0.06); font-family:'Ma Shan Zheng', serif;
}
.theme-ink .cv-content::after {
  content:'山高水长'; position:absolute; bottom:30px; right:40px;
  font-family:'Ma Shan Zheng', 'Noto Serif SC', serif; font-size:18px;
  color:rgba(0,0,0,0.4); letter-spacing:8px; writing-mode:vertical-rl;
}
.theme-ink .cv-main-title { font-family:'Ma Shan Zheng', 'Noto Serif SC', serif !important; font-weight:400 !important; }

# ===== stamp 印章 — 整图压红印 + 暗纹 + 边框 =====
.theme-stamp::before {
  content:''; position:absolute; inset:8px; border:3px solid #dc2626; pointer-events:none;
  box-shadow:inset 0 0 0 1px #dc2626;
}
.theme-stamp .cv-bg-decoration::before {
  content:'篆'; position:absolute; top:20%; right:10%; font-size:160px; color:rgba(220,38,38,0.15);
  font-family:'Ma Shan Zheng', serif; font-weight:900; transform:rotate(-5deg);
}
.theme-stamp .cv-bg-decoration::after {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:repeating-linear-gradient(45deg, transparent 0, transparent 12px, rgba(220,38,38,0.04) 12px, rgba(220,38,38,0.04) 13px);
}
.theme-stamp .cv-content { border:2px dashed rgba(220,38,38,0.3); }

# ===== newspaper 报纸 — 整图报纸纹理 + 报纸栏分割线 =====
.theme-newspaper::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:repeating-linear-gradient(90deg, transparent 0px, transparent 80px, rgba(0,0,0,0.08) 80px, rgba(0,0,0,0.08) 81px);
}
.theme-newspaper .cv-bg-decoration::before {
  content:'今日头条'; position:absolute; top:30px; left:30px; right:30px;
  font-family:'Noto Serif SC', serif; font-size:14px; font-weight:900; letter-spacing:8px;
  text-align:center; color:var(--accent1); border-bottom:3px double var(--accent1); padding-bottom:8px;
}
.theme-newspaper .cv-bg-decoration::after {
  content:''; position:absolute; bottom:60px; left:30px; right:30px; height:2px;
  background:var(--accent1);
}
.theme-newspaper .cv-content { background:repeating-linear-gradient(0deg, transparent 0px, transparent 30px, rgba(0,0,0,0.04) 30px, rgba(0,0,0,0.04) 31px); }

# ===== polaroid 拍立得 — 大白边 + 日期戳 + 倾斜 =====
.theme-polaroid::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:#f5f5f0;
}
.theme-polaroid .cv-bg-decoration::before {
  content:''; position:absolute; top:20px; right:20px; width:50%; height:75%;
  background:#fff; box-shadow:0 8px 24px rgba(0,0,0,0.3); transform:rotate(2deg);
  padding:12px 12px 50px;
}
.theme-polaroid .cv-bg-decoration::after {
  content:'2024 📷'; position:absolute; bottom:35px; right:40px;
  font-family:'Courier New', monospace; font-size:14px; color:#666; font-weight:700;
  z-index:2;
}
.theme-polaroid .cv-content { padding-left:10px !important; }

# ===== risograph Riso印刷 — 错位双色 + 颗粒 =====
.theme-risograph::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    linear-gradient(180deg, var(--accent1) 0%, transparent 40%),
    linear-gradient(0deg, var(--accent2) 0%, transparent 40%);
  opacity:0.2;
  mix-blend-mode:multiply;
}
.theme-risograph .cv-bg-decoration::before {
  content:''; position:absolute; inset:0; pointer-events:none;
  background-image:radial-gradient(circle, rgba(0,0,0,0.3) 0.5px, transparent 0.5px);
  background-size:3px 3px;
  mix-blend-mode:multiply;
}
.theme-risograph .cv-main-title { text-shadow:2px 0 0 var(--accent1), -2px 0 0 var(--accent2); }

# ===== film 胶片 — 顶部底部胶片孔 + 帧感 =====
.theme-film::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 50% 0%, rgba(255,255,255,0.2) 0%, transparent 30%),
    radial-gradient(ellipse at 50% 100%, rgba(255,255,255,0.2) 0%, transparent 30%);
}
.theme-film .cv-bg-decoration::before {
  content:''; position:absolute; top:0; left:0; right:0; height:18px;
  background:repeating-linear-gradient(90deg, #1a1a1a 0px, #1a1a1a 18px, transparent 18px, transparent 36px);
}
.theme-film .cv-bg-decoration::after {
  content:''; position:absolute; bottom:0; left:0; right:0; height:18px;
  background:repeating-linear-gradient(90deg, #1a1a1a 0px, #1a1a1a 18px, transparent 18px, transparent 36px);
}
.theme-film .cv-content { padding-top:30px !important; padding-bottom:30px !important; }
.theme-film .cv-bottom-bar { background:#1a1a1a !important; }

# ===== ribbon 缎带 — 大对角缎带 + 蝴蝶结 =====
.theme-ribbon::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:linear-gradient(135deg, var(--accent1) 0%, var(--accent2) 100%);
  opacity:0.15;
}
.theme-ribbon .cv-bg-decoration::before {
  content:''; position:absolute; top:0; left:20%; right:20%; height:60px;
  background:linear-gradient(to bottom, transparent 0%, var(--accent1) 50%, transparent 100%);
  transform:rotate(-3deg); transform-origin:left center;
  box-shadow:0 4px 12px rgba(0,0,0,0.2);
}
.theme-ribbon .cv-bg-decoration::after {
  content:'🎀'; position:absolute; top:15px; right:30px; font-size:50px;
  filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
}

# ===== pastel 莫兰迪 — 整体低饱和柔光 + 圆角柔化 =====
.theme-pastel::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:radial-gradient(circle at 30% 40%, rgba(255,255,255,0.5) 0%, transparent 50%),
             radial-gradient(circle at 70% 60%, rgba(255,255,255,0.3) 0%, transparent 50%);
  filter:blur(20px);
}
.theme-pastel .cv-bg-decoration::before {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:rgba(255,255,255,0.15);
  mix-blend-mode:soft-light;
}
.theme-pastel .cv-bg-circle { opacity:0.1 !important; }
.theme-pastel .cover-card, .theme-pastel .theme-preview { border-radius:20px !important; }

# ===== kraft 牛皮纸 — 纸质纹理 + 麻绳边框 + 印章 =====
.theme-kraft::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background-image:
    linear-gradient(45deg, transparent 48%, rgba(139,90,43,0.05) 48%, rgba(139,90,43,0.05) 52%, transparent 52%),
    linear-gradient(-45deg, transparent 48%, rgba(139,90,43,0.05) 48%, rgba(139,90,43,0.05) 52%, transparent 52%);
  background-size:8px 8px;
}
.theme-kraft .cv-bg-decoration::before {
  content:''; position:absolute; inset:8px; border:2px dashed rgba(139,90,43,0.4);
  border-radius:4px; pointer-events:none;
}
.theme-kraft .cv-bg-decoration::after {
  content:'✦ HANDMADE ✦'; position:absolute; top:10px; left:50%; transform:translateX(-50%);
  font-family:'Courier New', monospace; font-size:12px; color:rgba(139,90,43,0.6);
  letter-spacing:4px; font-weight:700;
}

# ===== washi 和纸胶带 — 多条斜贴胶带 + 樱花点缀 =====
.theme-washi::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background-image:radial-gradient(circle, rgba(236,72,153,0.1) 1px, transparent 1px);
  background-size:20px 20px;
}
.theme-washi .cv-bg-decoration::before {
  content:''; position:absolute; top:15%; left:-5%; width:110%; height:20px;
  background:repeating-linear-gradient(90deg, #ec4899 0px, #ec4899 20px, #fff 20px, #fff 25px);
  transform:rotate(-5deg); opacity:0.7;
}
.theme-washi .cv-bg-decoration::after {
  content:''; position:absolute; bottom:20%; left:-5%; width:110%; height:20px;
  background:repeating-linear-gradient(90deg, #10b981 0px, #10b981 20px, #fff 20px, #fff 25px);
  transform:rotate(3deg); opacity:0.7;
}

# ===== terrarium 玻璃生态 — 圆形玻璃罩 + 植物剪影 =====
.theme-terrarium::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:radial-gradient(ellipse at center, rgba(255,255,255,0.3) 0%, transparent 60%);
}
.theme-terrarium .cv-bg-decoration::before {
  content:''; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  width:240px; height:240px; border-radius:50%;
  background:radial-gradient(circle at 30% 30%, rgba(255,255,255,0.6) 0%, transparent 40%),
             radial-gradient(circle at 50% 100%, rgba(34,197,94,0.4) 0%, transparent 50%);
  border:3px solid rgba(255,255,255,0.4);
  box-shadow:inset 0 0 30px rgba(34,197,94,0.2);
}

# ===== watercolor 水彩晕染 — 多色水彩斑点 + 边缘晕开 =====
.theme-watercolor::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(circle at 20% 20%, rgba(236,72,153,0.4) 0%, transparent 25%),
    radial-gradient(circle at 80% 30%, rgba(59,130,246,0.4) 0%, transparent 25%),
    radial-gradient(circle at 30% 80%, rgba(251,191,36,0.4) 0%, transparent 25%),
    radial-gradient(circle at 70% 70%, rgba(34,197,94,0.4) 0%, transparent 25%);
  filter:blur(30px);
  opacity:0.7;
}
.theme-watercolor .cv-bg-decoration::before {
  content:''; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  width:280px; height:280px; border-radius:50%;
  background:radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
}
.theme-watercolor .cv-main-title { text-shadow:1px 1px 0 rgba(255,255,255,0.5); }

# ===== zen 禅意侘寂 — 圆形禅意圆 + 灰调 + 大量留白 =====
.theme-zen::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:radial-gradient(circle at 50% 50%, transparent 35%, rgba(0,0,0,0.05) 100%);
}
.theme-zen .cv-bg-decoration::before {
  content:''; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  width:300px; height:300px; border-radius:50%;
  border:2px solid currentColor; opacity:0.15;
}
.theme-zen .cv-bg-decoration::after {
  content:'禅'; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  font-size:200px; opacity:0.08; color:currentColor; font-family:'Ma Shan Zheng', serif;
}
.theme-zen .cv-main-title { font-family:'Ma Shan Zheng', 'Noto Serif SC', serif !important; font-weight:300 !important; }

# ===== scandinavian 北欧极简 — 大白底 + 极简线条 + 几何元素 =====
.theme-scandinavian::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:linear-gradient(180deg, transparent 60%, rgba(0,0,0,0.03) 100%);
}
.theme-scandinavian .cv-bg-decoration::before {
  content:''; position:absolute; top:20px; right:20px; width:80px; height:80px;
  background:linear-gradient(135deg, var(--accent1) 0%, transparent 70%);
  border-radius:50% 0 50% 0;
}
.theme-scandinavian .cv-bg-decoration::after {
  content:''; position:absolute; bottom:20px; left:20px; width:60px; height:60px;
  border:3px solid var(--accent2); border-radius:50%;
  opacity:0.3;
}
.theme-scandinavian .cv-content { padding-left:60px !important; }

# ===== boho 波西米亚 — 多彩流苏 + 曼陀罗 + 几何 =====
.theme-boho::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(circle at 25% 25%, rgba(251,191,36,0.2) 0%, transparent 15%),
    radial-gradient(circle at 75% 75%, rgba(236,72,153,0.2) 0%, transparent 15%),
    radial-gradient(circle at 75% 25%, rgba(34,197,94,0.2) 0%, transparent 15%),
    radial-gradient(circle at 25% 75%, rgba(59,130,246,0.2) 0%, transparent 15%);
}
.theme-boho .cv-bg-decoration::before {
  content:'✦ ☽ ✦ ☾ ✦'; position:absolute; top:30%; left:0; right:0; text-align:center;
  font-size:24px; opacity:0.2; letter-spacing:30px; color:var(--accent1);
}
.theme-boho .cv-bg-decoration::after {
  content:''; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  width:200px; height:200px; border:2px solid var(--accent2); border-radius:50%;
  opacity:0.3; box-shadow:0 0 0 8px transparent, 0 0 0 10px var(--accent2);
}

# ===== forest 森林秘境 — 树叶剪影 + 顶部树梢 =====
.theme-forest::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    linear-gradient(180deg, rgba(34,197,94,0.1) 0%, transparent 30%, transparent 70%, rgba(34,197,94,0.2) 100%);
}
.theme-forest .cv-bg-decoration::before {
  content:'🌲🌲🌲'; position:absolute; top:0; left:0; right:0;
  text-align:center; font-size:30px; letter-spacing:5px;
  opacity:0.4; filter:brightness(0.7);
}
.theme-forest .cv-bg-decoration::after {
  content:''; position:absolute; bottom:0; left:0; right:0; height:40%;
  background:
    linear-gradient(180deg, transparent 0%, rgba(20,83,45,0.4) 100%);
}

# ===== desert 沙漠暖阳 — 沙丘剪影 + 太阳圆盘 =====
.theme-desert::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:linear-gradient(180deg, var(--accent2) 0%, var(--accent1) 100%);
  opacity:0.2;
}
.theme-desert .cv-bg-decoration::before {
  content:'☀'; position:absolute; top:15%; right:15%; font-size:120px;
  color:var(--accent1); opacity:0.4;
  filter:drop-shadow(0 0 30px var(--accent1));
}
.theme-desert .cv-bg-decoration::after {
  content:''; position:absolute; bottom:0; left:0; right:0; height:50%;
  background:linear-gradient(180deg, transparent 0%, var(--accent1) 100%);
  clip-path:polygon(0 60%, 20% 50%, 40% 65%, 60% 45%, 80% 60%, 100% 50%, 100% 100%, 0 100%);
}

# ===== vintage 复古怀旧 — 米黄底 + 暗角 + 颗粒 =====
.theme-vintage::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.3) 100%),
    repeating-linear-gradient(0deg, transparent 0px, transparent 1px, rgba(0,0,0,0.04) 1px, rgba(0,0,0,0.04) 2px);
}
.theme-vintage .cv-content { filter:sepia(0.3) contrast(1.1) brightness(0.95); }

# ===== cherry 樱花粉嫩 — 飘落樱花瓣 =====
.theme-cherry::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:radial-gradient(circle at 30% 30%, rgba(252,165,165,0.4) 0%, transparent 40%),
             radial-gradient(circle at 70% 70%, rgba(251,113,133,0.3) 0%, transparent 40%);
}
.theme-cherry .cv-bg-decoration::before {
  content:'🌸'; position:absolute; top:8%; left:8%; font-size:60px; opacity:0.5;
}
.theme-cherry .cv-bg-decoration::after {
  content:'🌸'; position:absolute; top:60%; right:12%; font-size:50px; opacity:0.4;
  transform:rotate(30deg);
}

# ===== woodcut 版画木刻 — 黑白对比 + 木刻线条 =====
.theme-woodcut::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    repeating-linear-gradient(90deg, transparent 0px, transparent 4px, rgba(0,0,0,0.08) 4px, rgba(0,0,0,0.08) 5px),
    repeating-linear-gradient(0deg, transparent 0px, transparent 4px, rgba(0,0,0,0.08) 4px, rgba(0,0,0,0.08) 5px);
}
.theme-woodcut .cv-bg-decoration::before {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:radial-gradient(ellipse at center, transparent 30%, rgba(0,0,0,0.4) 100%);
}
.theme-woodcut .cv-main-title { font-family:'Noto Serif SC', serif; text-shadow:1px 1px 0 #000; }

# ===== plaid 格纹学院 — 完整格纹底 =====
.theme-plaid::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    repeating-linear-gradient(0deg, transparent 0px, transparent 30px, var(--accent1) 30px, var(--accent1) 32px),
    repeating-linear-gradient(90deg, transparent 0px, transparent 30px, var(--accent2) 30px, var(--accent2) 32px);
  opacity:0.3;
}
.theme-plaid .cv-bg-decoration::before {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:repeating-linear-gradient(45deg, transparent 0, transparent 20px, var(--accent1) 20px, var(--accent1) 22px);
  opacity:0.1;
}

# ===== origami 折纸手工 — 几何折纸元素 =====
.theme-origami::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:linear-gradient(135deg, rgba(255,255,255,0.3) 0%, transparent 50%, rgba(0,0,0,0.05) 100%);
}
.theme-origami .cv-bg-decoration::before {
  content:''; position:absolute; top:20px; right:20px;
  width:0; height:0;
  border-left:30px solid transparent; border-right:30px solid transparent;
  border-bottom:52px solid var(--accent1);
  filter:drop-shadow(3px 3px 5px rgba(0,0,0,0.2));
}
.theme-origami .cv-bg-decoration::after {
  content:''; position:absolute; bottom:20px; left:30px;
  width:0; height:0;
  border-left:25px solid transparent; border-right:25px solid transparent;
  border-bottom:43px solid var(--accent2);
  filter:drop-shadow(3px 3px 5px rgba(0,0,0,0.2));
  transform:rotate(45deg);
}

# ===== paperplane 纸飞机 — 飞行轨迹 =====
.theme-paperplane::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:linear-gradient(135deg, transparent 60%, rgba(0,0,0,0.05) 100%);
}
.theme-paperplane .cv-bg-decoration::before {
  content:'✈️'; position:absolute; top:30%; right:20%; font-size:80px; opacity:0.3;
  transform:rotate(-45deg);
}
.theme-paperplane .cv-bg-decoration::after {
  content:''; position:absolute; top:30%; right:20%;
  width:200px; height:2px; background:linear-gradient(to right, transparent 0%, var(--accent1) 100%);
  transform:rotate(-45deg); transform-origin:right center;
  opacity:0.4;
}

# ===== lofi Lo-Fi慵懒 — 噪点 + 暖黄滤镜 =====
.theme-lofi::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background-image:radial-gradient(circle, rgba(0,0,0,0.15) 0.5px, transparent 0.5px);
  background-size:2px 2px; mix-blend-mode:overlay;
}
.theme-lofi .cv-bg-decoration::before {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(180deg, rgba(251,191,36,0.1) 0%, rgba(236,72,153,0.1) 100%);
}
.theme-lofi .cv-content { filter:sepia(0.1) saturate(0.9); }

# ===== wave 海浪波纹 — 多层波浪 =====
.theme-wave::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    linear-gradient(180deg, transparent 0%, var(--accent1) 100%);
  opacity:0.2;
}
.theme-wave .cv-bg-decoration::before {
  content:''; position:absolute; bottom:0; left:-10%; right:-10%; height:60%;
  background:
    radial-gradient(ellipse at 50% 100%, var(--accent2) 0%, transparent 70%);
  border-radius:50% 50% 0 0;
}
.theme-wave .cv-bg-decoration::after {
  content:''; position:absolute; bottom:0; left:-10%; right:-10%; height:40%;
  background:radial-gradient(ellipse at 50% 100%, var(--accent1) 0%, transparent 70%);
  border-radius:50% 50% 0 0;
}

# ===== fairy 童话梦幻 — 闪光星星 + 飘浮云朵 =====
.theme-fairy::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(circle at 30% 20%, rgba(255,255,255,0.8) 0%, transparent 8%),
    radial-gradient(circle at 70% 40%, rgba(255,255,255,0.6) 0%, transparent 6%),
    radial-gradient(circle at 20% 70%, rgba(255,255,255,0.7) 0%, transparent 7%),
    radial-gradient(circle at 80% 80%, rgba(255,255,255,0.5) 0%, transparent 5%);
}
.theme-fairy .cv-bg-decoration::before {
  content:'✨ 🧚 ✨'; position:absolute; top:25%; left:0; right:0; text-align:center;
  font-size:30px; letter-spacing:20px; opacity:0.5;
}
.theme-fairy .cv-bg-decoration::after {
  content:'☁️'; position:absolute; top:10%; right:15%; font-size:50px; opacity:0.4;
}

# ===== earth 地球生态 — 蓝色星球 + 经纬线 =====
.theme-earth::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(circle at 70% 50%, var(--accent1) 0%, var(--accent2) 50%, transparent 70%);
  opacity:0.3;
}
.theme-earth .cv-bg-decoration::before {
  content:''; position:absolute; top:50%; right:15%; transform:translateY(-50%);
  width:180px; height:180px; border-radius:50%;
  background:radial-gradient(circle at 30% 30%, #4ade80 0%, #16a34a 30%, #0ea5e9 60%, #1e3a5f 100%);
  box-shadow:0 0 40px rgba(59,130,246,0.4), inset -20px -20px 40px rgba(0,0,0,0.3);
}
.theme-earth .cv-bg-decoration::after {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:
    repeating-linear-gradient(0deg, transparent 0px, transparent 30px, rgba(255,255,255,0.05) 30px, rgba(255,255,255,0.05) 31px),
    repeating-linear-gradient(90deg, transparent 0px, transparent 30px, rgba(255,255,255,0.05) 30px, rgba(255,255,255,0.05) 31px);
}

# ===== rain 雨天氛围 — 雨滴元素 + 灰调 =====
.theme-rain::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.3) 100%);
}
.theme-rain .cv-bg-decoration::before {
  content:'💧💧💧'; position:absolute; top:0; left:0; right:0;
  text-align:center; font-size:20px; letter-spacing:8px; opacity:0.3;
}
.theme-rain .cv-content { filter:brightness(0.95); }

# ===== sunset 日落黄昏 — 落日 + 晚霞渐变 =====
.theme-sunset::before {
  content:''; position:absolute; inset:0; pointer-events:none; z-index:0;
  background:linear-gradient(180deg, var(--accent1) 0%, var(--accent2) 50%, var(--accent1) 100%);
  opacity:0.3;
}
.theme-sunset .cv-bg-decoration::before {
  content:'🌅'; position:absolute; top:30%; left:50%; transform:translateX(-50%);
  font-size:100px; opacity:0.5;
  filter:drop-shadow(0 0 30px var(--accent1));
}

# ===== cardstock 笔记本 — 笔记本横线 + 边距红竖线 =====
# (待添加)

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



/* ===== 深色主题差异化CSS v2 ===== */

/* ===== abstract (triangles) ===== */
.theme-abstract .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-abstract .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== action (zigzag) ===== */
.theme-action .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-action .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== african (triangles) ===== */
.theme-african .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-african .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== agent (circuit) ===== */
.theme-agent .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-agent .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== algo (circuit) ===== */
.theme-algo .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-algo .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== angular (circuit) ===== */
.theme-angular .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-angular .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== anime2 (aura) ===== */
.theme-anime2 .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-anime2 .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== arabesque (curves) ===== */
.theme-arabesque .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-arabesque .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== artnouveau (curves) ===== */
.theme-artnouveau .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-artnouveau .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== ascii (barcode) ===== */
.theme-ascii .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 0,var(--accent1) 3px,transparent 3px,transparent 8px,var(--accent1) 8px,var(--accent1) 10px,transparent 10px,transparent 15px);opacity:.05;mix-blend-mode:screen;} .theme-ascii .cv-bg-decoration::after {content:"";position:absolute;top:30%;right:8%;width:60px;height:60px;border:2px solid var(--accent2);opacity:.15;transform:rotate(45deg);}
/* ===== autumn (leaves) ===== */
.theme-autumn .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-autumn .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== aztec (steps) ===== */
.theme-aztec .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-aztec .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== baking (dots) ===== */
.theme-baking .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-baking .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== bamboo (beams) ===== */
.theme-bamboo .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-bamboo .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== baseball (stripes) ===== */
.theme-baseball .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-baseball .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== basketball (stripes) ===== */
.theme-basketball .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-basketball .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== bauhaus (triangles) ===== */
.theme-bauhaus .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-bauhaus .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== bbq (radial) ===== */
.theme-bbq .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-bbq .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== beer (bokeh) ===== */
.theme-beer .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-beer .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== bike (stripes) ===== */
.theme-bike .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-bike .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== binary (barcode) ===== */
.theme-binary .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 0,var(--accent1) 3px,transparent 3px,transparent 8px,var(--accent1) 8px,var(--accent1) 10px,transparent 10px,transparent 15px);opacity:.05;mix-blend-mode:screen;} .theme-binary .cv-bg-decoration::after {content:"";position:absolute;top:30%;right:8%;width:60px;height:60px;border:2px solid var(--accent2);opacity:.15;transform:rotate(45deg);}
/* ===== biopunk (circuit) ===== */
.theme-biopunk .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-biopunk .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== blockchain (hexagon) ===== */
.theme-blockchain .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(-60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(0deg,var(--accent1) 1px,transparent 1px,transparent 35px);opacity:.06;mix-blend-mode:screen;} .theme-blockchain .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:5%;width:80px;height:92px;background:var(--accent2);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);opacity:.12;}
/* ===== blues (waves) ===== */
.theme-blues .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-blues .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== bonsai (steps) ===== */
.theme-bonsai .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-bonsai .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== boxing (zigzag) ===== */
.theme-boxing .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-boxing .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== bridge (curves) ===== */
.theme-bridge .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-bridge .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== brutal2 (bricks) ===== */
.theme-brutal2 .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-brutal2 .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== byzantine (aura) ===== */
.theme-byzantine .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-byzantine .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== cabin (bricks) ===== */
.theme-cabin .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-cabin .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== cactus (dots) ===== */
.theme-cactus .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-cactus .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== calligraphy (curves) ===== */
.theme-calligraphy .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-calligraphy .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== camping (stars) ===== */
.theme-camping .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(1px 1px at 20% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 60% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 50%,var(--accent1),transparent),radial-gradient(1px 1px at 80% 10%,var(--accent2),transparent),radial-gradient(1px 1px at 90% 60%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 33% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 15% 65%,var(--accent1),transparent);opacity:.25;} .theme-camping .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.12;filter:blur(20px);border-radius:50%;}
/* ===== castle (bricks) ===== */
.theme-castle .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-castle .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== cat (dots) ===== */
.theme-cat .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-cat .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== celtic (weave) ===== */
.theme-celtic .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-celtic .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== ceramic (weave) ===== */
.theme-ceramic .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-ceramic .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== chaos (zigzag) ===== */
.theme-chaos .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-chaos .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== chengdu (aura) ===== */
.theme-chengdu .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-chengdu .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== christmas (snow) ===== */
.theme-christmas .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(2px 2px at 10% 20%,var(--accent1),transparent),radial-gradient(1px 1px at 30% 50%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 70% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 85% 40%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 20% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 60% 10%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 90% 85%,var(--accent2),transparent);opacity:.2;} .theme-christmas .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;left:-10%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.12;filter:blur(30px);border-radius:50%;}
/* ===== chrome (beams) ===== */
.theme-chrome .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-chrome .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== cicd (steps) ===== */
.theme-cicd .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-cicd .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== classical (curves) ===== */
.theme-classical .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-classical .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== climbing (steps) ===== */
.theme-climbing .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-climbing .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== cocktail (bokeh) ===== */
.theme-cocktail .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-cocktail .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== coffee2 (steam) ===== */
.theme-coffee2 .cv-bg-decoration::before {content:"";position:absolute;bottom:10%;left:10%;width:3px;height:200px;background:linear-gradient(to top,transparent,var(--accent1),transparent);opacity:.15;filter:blur(8px);border-radius:50%;} .theme-coffee2 .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:15%;width:3px;height:180px;background:linear-gradient(to top,transparent,var(--accent2),transparent);opacity:.12;filter:blur(10px);border-radius:50%;transform:skewX(-10deg);}
/* ===== colorfield (blocks) ===== */
.theme-colorfield .cv-bg-decoration::before {content:"";position:absolute;top:0;left:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent1),transparent);opacity:.08;} .theme-colorfield .cv-bg-decoration::after {content:"";position:absolute;top:0;right:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent2),transparent);opacity:.08;}
/* ===== comedy (zigzag) ===== */
.theme-comedy .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-comedy .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== concert (beams) ===== */
.theme-concert .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-concert .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== construct (steps) ===== */
.theme-construct .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-construct .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== cooking (steam) ===== */
.theme-cooking .cv-bg-decoration::before {content:"";position:absolute;bottom:10%;left:10%;width:3px;height:200px;background:linear-gradient(to top,transparent,var(--accent1),transparent);opacity:.15;filter:blur(8px);border-radius:50%;} .theme-cooking .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:15%;width:3px;height:180px;background:linear-gradient(to top,transparent,var(--accent2),transparent);opacity:.12;filter:blur(10px);border-radius:50%;transform:skewX(-10deg);}
/* ===== copilot (circuit) ===== */
.theme-copilot .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-copilot .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== country (leaves) ===== */
.theme-country .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-country .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== cozy (aura) ===== */
.theme-cozy .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-cozy .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== cron (steps) ===== */
.theme-cron .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-cron .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== crystal (triangles) ===== */
.theme-crystal .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-crystal .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== cubism (triangles) ===== */
.theme-cubism .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-cubism .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== cyberfilm (noise) ===== */
.theme-cyberfilm .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 1px,transparent 1px);background-size:15px 15px,20px 20px;background-position:0 0,7px 7px;opacity:.06;mix-blend-mode:screen;} .theme-cyberfilm .cv-bg-decoration::after {content:"";position:absolute;top:20%;left:-10%;width:200px;height:60%;background:linear-gradient(45deg,transparent,var(--accent2),transparent);opacity:.08;filter:blur(40px);transform:rotate(-15deg);}
/* ===== cycling (stripes) ===== */
.theme-cycling .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-cycling .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== dada (chaos) ===== */
.theme-dada .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(17deg,transparent 0,transparent 25px,var(--accent1) 25px,var(--accent1) 26px),repeating-linear-gradient(-23deg,transparent 0,transparent 35px,var(--accent2) 35px,var(--accent2) 36px);opacity:.05;mix-blend-mode:screen;} .theme-dada .cv-bg-decoration::after {content:"";position:absolute;top:25%;right:8%;width:100px;height:100px;border:3px solid var(--accent2);opacity:.1;clip-path:polygon(50% 0%,100% 50%,50% 100%,0% 50%,50% 25%,75% 50%,50% 75%,25% 50%);}
/* ===== dandelion (dots) ===== */
.theme-dandelion .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-dandelion .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== datamosh (noise) ===== */
.theme-datamosh .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 1px,transparent 1px);background-size:15px 15px,20px 20px;background-position:0 0,7px 7px;opacity:.06;mix-blend-mode:screen;} .theme-datamosh .cv-bg-decoration::after {content:"";position:absolute;top:20%;left:-10%;width:200px;height:60%;background:linear-gradient(45deg,transparent,var(--accent2),transparent);opacity:.08;filter:blur(40px);transform:rotate(-15deg);}
/* ===== dataviz (barcode) ===== */
.theme-dataviz .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 0,var(--accent1) 3px,transparent 3px,transparent 8px,var(--accent1) 8px,var(--accent1) 10px,transparent 10px,transparent 15px);opacity:.05;mix-blend-mode:screen;} .theme-dataviz .cv-bg-decoration::after {content:"";position:absolute;top:30%;right:8%;width:60px;height:60px;border:2px solid var(--accent2);opacity:.15;transform:rotate(45deg);}
/* ===== dawn (aura) ===== */
.theme-dawn .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-dawn .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== ddd (bricks) ===== */
.theme-ddd .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-ddd .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== deco (steps) ===== */
.theme-deco .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-deco .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== dessert (bokeh) ===== */
.theme-dessert .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-dessert .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== destijl (blocks) ===== */
.theme-destijl .cv-bg-decoration::before {content:"";position:absolute;top:0;left:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent1),transparent);opacity:.08;} .theme-destijl .cv-bg-decoration::after {content:"";position:absolute;top:0;right:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent2),transparent);opacity:.08;}
/* ===== diamond (triangles) ===== */
.theme-diamond .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-diamond .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== disco (dots) ===== */
.theme-disco .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-disco .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== diy (bricks) ===== */
.theme-diy .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-diy .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== docker (waves) ===== */
.theme-docker .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-docker .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== dog (dots) ===== */
.theme-dog .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-dog .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== doubleexp (bokeh) ===== */
.theme-doubleexp .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-doubleexp .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== drama (curves) ===== */
.theme-drama .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-drama .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== drizzle (rain) ===== */
.theme-drizzle .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-drizzle .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== dunhuang (aura) ===== */
.theme-dunhuang .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-dunhuang .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== duotone (blocks) ===== */
.theme-duotone .cv-bg-decoration::before {content:"";position:absolute;top:0;left:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent1),transparent);opacity:.08;} .theme-duotone .cv-bg-decoration::after {content:"";position:absolute;top:0;right:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent2),transparent);opacity:.08;}
/* ===== dusk (aura) ===== */
.theme-dusk .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-dusk .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== dyeing (weave) ===== */
.theme-dyeing .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-dyeing .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== eco (leaves) ===== */
.theme-eco .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-eco .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== edge (beams) ===== */
.theme-edge .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-edge .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== edm (beams) ===== */
.theme-edm .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-edm .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== egyptian (steps) ===== */
.theme-egyptian .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-egyptian .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== eighties (grid) ===== */
.theme-eighties .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-eighties .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== elastic (grid) ===== */
.theme-elastic .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-elastic .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== embedding (dots) ===== */
.theme-embedding .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-embedding .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== expression (zigzag) ===== */
.theme-expression .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-expression .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== fairytale (aura) ===== */
.theme-fairytale .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-fairytale .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== fantasy (aura) ===== */
.theme-fantasy .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-fantasy .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== fauvism (blocks) ===== */
.theme-fauvism .cv-bg-decoration::before {content:"";position:absolute;top:0;left:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent1),transparent);opacity:.08;} .theme-fauvism .cv-bg-decoration::after {content:"";position:absolute;top:0;right:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent2),transparent);opacity:.08;}
/* ===== feathers (curves) ===== */
.theme-feathers .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-feathers .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== fifties (dots) ===== */
.theme-fifties .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-fifties .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== figma (geometric) ===== */
.theme-figma .cv-bg-decoration::before {content:"";position:absolute;top:10%;right:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.1;transform:rotate(45deg);} .theme-figma .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;left:8%;width:70px;height:70px;border:2px solid var(--accent2);opacity:.12;border-radius:50%;}
/* ===== fish (waves) ===== */
.theme-fish .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-fish .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== fishing (waves) ===== */
.theme-fishing .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-fishing .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== fluid (waves) ===== */
.theme-fluid .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-fluid .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== fog (fog) ===== */
.theme-fog .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 30% 40%,var(--accent1) 0%,transparent 40%),radial-gradient(ellipse at 70% 60%,var(--accent2) 0%,transparent 40%);opacity:.1;filter:blur(40px);} .theme-fog .cv-bg-decoration::after {content:"";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:300px;height:1px;background:var(--accent1);opacity:.2;filter:blur(3px);box-shadow:0 30px 0 var(--accent2),0 -30px 0 var(--accent1);}
/* ===== folk (leaves) ===== */
.theme-folk .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-folk .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== football (stripes) ===== */
.theme-football .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-football .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== fps (zigzag) ===== */
.theme-fps .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-fps .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== fractal (fractal) ===== */
.theme-fractal .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 50% 50%,var(--accent1) 0deg,transparent 60deg,var(--accent2) 120deg,transparent 180deg,var(--accent1) 240deg,transparent 300deg);opacity:.06;filter:blur(2px);} .theme-fractal .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:5%;transform:translateY(-50%);width:120px;height:120px;border:2px solid var(--accent1);opacity:.1;box-shadow:inset 0 0 0 22px var(--accent2),inset 0 0 0 42px var(--accent1);border-radius:50%;}
/* ===== funk (stripes) ===== */
.theme-funk .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-funk .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== gardening (leaves) ===== */
.theme-gardening .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-gardening .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== generative (fractal) ===== */
.theme-generative .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 50% 50%,var(--accent1) 0deg,transparent 60deg,var(--accent2) 120deg,transparent 180deg,var(--accent1) 240deg,transparent 300deg);opacity:.06;filter:blur(2px);} .theme-generative .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:5%;transform:translateY(-50%);width:120px;height:120px;border:2px solid var(--accent1);opacity:.1;box-shadow:inset 0 0 0 22px var(--accent2),inset 0 0 0 42px var(--accent1);border-radius:50%;}
/* ===== geometric (triangles) ===== */
.theme-geometric .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-geometric .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== ginkgo (leaves) ===== */
.theme-ginkgo .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-ginkgo .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== github (grid) ===== */
.theme-github .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-github .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== gitlab (grid) ===== */
.theme-gitlab .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-gitlab .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== gitops (steps) ===== */
.theme-gitops .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-gitops .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== glam (bokeh) ===== */
.theme-glam .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-glam .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== glitch2 (zigzag) ===== */
.theme-glitch2 .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-glitch2 .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== glossy (bokeh) ===== */
.theme-glossy .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-glossy .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== golang (circuit) ===== */
.theme-golang .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-golang .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== gold (radial) ===== */
.theme-gold .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-gold .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== golf (dots) ===== */
.theme-golf .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-golf .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== gongbi (leaves) ===== */
.theme-gongbi .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-gongbi .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== gothic2 (triangles) ===== */
.theme-gothic2 .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-gothic2 .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== grafana (rings) ===== */
.theme-grafana .cv-bg-decoration::before {content:"";position:absolute;top:50%;right:-15%;transform:translateY(-50%);width:300px;height:300px;border:2px solid var(--accent1);border-radius:50%;opacity:.1;box-shadow:0 0 0 42px var(--accent1),0 0 0 82px var(--accent2);} .theme-grafana .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-15%;transform:translateY(-50%);width:100px;height:100px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);border-radius:50%;opacity:.2;filter:blur(10px);}
/* ===== graphql (circuit) ===== */
.theme-graphql .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-graphql .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== greek (curves) ===== */
.theme-greek .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-greek .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== grpc (circuit) ===== */
.theme-grpc .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-grpc .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== grunge (noise) ===== */
.theme-grunge .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 1px,transparent 1px);background-size:15px 15px,20px 20px;background-position:0 0,7px 7px;opacity:.06;mix-blend-mode:screen;} .theme-grunge .cv-bg-decoration::after {content:"";position:absolute;top:20%;left:-10%;width:200px;height:60%;background:linear-gradient(45deg,transparent,var(--accent2),transparent);opacity:.08;filter:blur(40px);transform:rotate(-15deg);}
/* ===== haiku (curves) ===== */
.theme-haiku .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-haiku .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== halloween (zigzag) ===== */
.theme-halloween .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-halloween .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== hamster (dots) ===== */
.theme-hamster .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-hamster .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== harbor (waves) ===== */
.theme-harbor .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-harbor .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== hiking (steps) ===== */
.theme-hiking .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-hiking .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== hiphop (stripes) ===== */
.theme-hiphop .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-hiphop .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== horror (fog) ===== */
.theme-horror .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 30% 40%,var(--accent1) 0%,transparent 40%),radial-gradient(ellipse at 70% 60%,var(--accent2) 0%,transparent 40%);opacity:.1;filter:blur(40px);} .theme-horror .cv-bg-decoration::after {content:"";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:300px;height:1px;background:var(--accent1);opacity:.2;filter:blur(3px);box-shadow:0 30px 0 var(--accent2),0 -30px 0 var(--accent1);}
/* ===== house (beams) ===== */
.theme-house .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-house .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== huggingface (dots) ===== */
.theme-huggingface .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-huggingface .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== hygge (aura) ===== */
.theme-hygge .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-hygge .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== ikigai (bokeh) ===== */
.theme-ikigai .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-ikigai .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== impression (bokeh) ===== */
.theme-impression .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-impression .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== inca (steps) ===== */
.theme-inca .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-inca .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== infrared (radial) ===== */
.theme-infrared .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-infrared .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== iridescent (aura) ===== */
.theme-iridescent .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-iridescent .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== island (waves) ===== */
.theme-island .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-island .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== java (circuit) ===== */
.theme-java .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-java .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== jazz (curves) ===== */
.theme-jazz .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-jazz .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== jenkins (steps) ===== */
.theme-jenkins .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-jenkins .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== json2 (bricks) ===== */
.theme-json2 .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-json2 .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== juice (bokeh) ===== */
.theme-juice .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-juice .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== k8s (hexagon) ===== */
.theme-k8s .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(-60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(0deg,var(--accent1) 1px,transparent 1px,transparent 35px);opacity:.06;mix-blend-mode:screen;} .theme-k8s .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:5%;width:80px;height:92px;background:var(--accent2);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);opacity:.12;}
/* ===== kafka (beams) ===== */
.theme-kafka .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-kafka .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== karaoke (beams) ===== */
.theme-karaoke .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-karaoke .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== kayaking (waves) ===== */
.theme-kayaking .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-kayaking .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== kinetic (steps) ===== */
.theme-kinetic .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-kinetic .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== kyoto (curves) ===== */
.theme-kyoto .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-kyoto .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== lacquer (weave) ===== */
.theme-lacquer .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-lacquer .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== langchain (circuit) ===== */
.theme-langchain .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-langchain .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== laser (beams) ===== */
.theme-laser .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-laser .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== lavender (bokeh) ===== */
.theme-lavender .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-lavender .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== leather (weave) ===== */
.theme-leather .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-leather .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== lighthouse (beams) ===== */
.theme-lighthouse .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-lighthouse .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== lightning (zigzag) ===== */
.theme-lightning .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-lightning .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== linen (weave) ===== */
.theme-linen .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-linen .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== linux (terminal) ===== */
.theme-linux .cv-bg-decoration::before {content:">_";position:absolute;top:8%;left:3%;font-family:monospace;font-size:14px;color:var(--accent1);opacity:.3;letter-spacing:2px;} .theme-linux .cv-bg-decoration::after {content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0,transparent 3px,var(--accent1) 3px,var(--accent1) 4px);opacity:.03;mix-blend-mode:screen;}
/* ===== london (fog) ===== */
.theme-london .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 30% 40%,var(--accent1) 0%,transparent 40%),radial-gradient(ellipse at 70% 60%,var(--accent2) 0%,transparent 40%);opacity:.1;filter:blur(40px);} .theme-london .cv-bg-decoration::after {content:"";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:300px;height:1px;background:var(--accent1);opacity:.2;filter:blur(3px);box-shadow:0 30px 0 var(--accent2),0 -30px 0 var(--accent1);}
/* ===== longexp (beams) ===== */
.theme-longexp .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-longexp .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== lotus (leaves) ===== */
.theme-lotus .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-lotus .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== lowcode (bricks) ===== */
.theme-lowcode .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-lowcode .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== macro (bokeh) ===== */
.theme-macro .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-macro .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== maple (leaves) ===== */
.theme-maple .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-maple .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== marble (aura) ===== */
.theme-marble .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-marble .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== matte (bricks) ===== */
.theme-matte .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-matte .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== maximal (blocks) ===== */
.theme-maximal .cv-bg-decoration::before {content:"";position:absolute;top:0;left:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent1),transparent);opacity:.08;} .theme-maximal .cv-bg-decoration::after {content:"";position:absolute;top:0;right:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent2),transparent);opacity:.08;}
/* ===== maya (steps) ===== */
.theme-maya .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-maya .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== mesh2 (grid) ===== */
.theme-mesh2 .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-mesh2 .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== metal (triangles) ===== */
.theme-metal .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-metal .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== microsvc (hexagon) ===== */
.theme-microsvc .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(-60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(0deg,var(--accent1) 1px,transparent 1px,transparent 35px);opacity:.06;mix-blend-mode:screen;} .theme-microsvc .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:5%;width:80px;height:92px;background:var(--accent2);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);opacity:.12;}
/* ===== midautumn (aura) ===== */
.theme-midautumn .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-midautumn .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== milktea (dots) ===== */
.theme-milktea .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-milktea .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== mingqing (curves) ===== */
.theme-mingqing .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-mingqing .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== mirror (beams) ===== */
.theme-mirror .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-mirror .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== moba (grid) ===== */
.theme-moba .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-moba .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== modernist (grid) ===== */
.theme-modernist .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-modernist .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== mongo (grid) ===== */
.theme-mongo .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-mongo .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== mongolia (curves) ===== */
.theme-mongolia .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-mongolia .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== monochrome (blocks) ===== */
.theme-monochrome .cv-bg-decoration::before {content:"";position:absolute;top:0;left:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent1),transparent);opacity:.08;} .theme-monochrome .cv-bg-decoration::after {content:"";position:absolute;top:0;right:0;width:50%;height:100%;background:linear-gradient(180deg,var(--accent2),transparent);opacity:.08;}
/* ===== moonlight (stars) ===== */
.theme-moonlight .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(1px 1px at 20% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 60% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 50%,var(--accent1),transparent),radial-gradient(1px 1px at 80% 10%,var(--accent2),transparent),radial-gradient(1px 1px at 90% 60%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 33% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 15% 65%,var(--accent1),transparent);opacity:.25;} .theme-moonlight .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.12;filter:blur(20px);border-radius:50%;}
/* ===== moroccan (triangles) ===== */
.theme-moroccan .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-moroccan .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== moss (bokeh) ===== */
.theme-moss .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-moss .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== mountain (triangles) ===== */
.theme-mountain .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-mountain .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== mysql (grid) ===== */
.theme-mysql .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-mysql .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== mystery (fog) ===== */
.theme-mystery .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 30% 40%,var(--accent1) 0%,transparent 40%),radial-gradient(ellipse at 70% 60%,var(--accent2) 0%,transparent 40%);opacity:.1;filter:blur(40px);} .theme-mystery .cv-bg-decoration::after {content:"";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:300px;height:1px;background:var(--accent1);opacity:.2;filter:blur(3px);box-shadow:0 30px 0 var(--accent2),0 -30px 0 var(--accent1);}
/* ===== myth (stars) ===== */
.theme-myth .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(1px 1px at 20% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 60% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 50%,var(--accent1),transparent),radial-gradient(1px 1px at 80% 10%,var(--accent2),transparent),radial-gradient(1px 1px at 90% 60%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 33% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 15% 65%,var(--accent1),transparent);opacity:.25;} .theme-myth .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.12;filter:blur(20px);border-radius:50%;}
/* ===== nanopunk (hexagon) ===== */
.theme-nanopunk .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(-60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(0deg,var(--accent1) 1px,transparent 1px,transparent 35px);opacity:.06;mix-blend-mode:screen;} .theme-nanopunk .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:5%;width:80px;height:92px;background:var(--accent2);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);opacity:.12;}
/* ===== neural (dots) ===== */
.theme-neural .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-neural .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== newyear (radial) ===== */
.theme-newyear .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-newyear .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== nginx (hexagon) ===== */
.theme-nginx .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(-60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(0deg,var(--accent1) 1px,transparent 1px,transparent 35px);opacity:.06;mix-blend-mode:screen;} .theme-nginx .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:5%;width:80px;height:92px;background:var(--accent2);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);opacity:.12;}
/* ===== nineties (noise) ===== */
.theme-nineties .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 1px,transparent 1px);background-size:15px 15px,20px 20px;background-position:0 0,7px 7px;opacity:.06;mix-blend-mode:screen;} .theme-nineties .cv-bg-decoration::after {content:"";position:absolute;top:20%;left:-10%;width:200px;height:60%;background:linear-gradient(45deg,transparent,var(--accent2),transparent);opacity:.08;filter:blur(40px);transform:rotate(-15deg);}
/* ===== nodejs (circuit) ===== */
.theme-nodejs .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-nodejs .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== novel (bricks) ===== */
.theme-novel .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-novel .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== nyc (grid) ===== */
.theme-nyc .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-nyc .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== observ (rings) ===== */
.theme-observ .cv-bg-decoration::before {content:"";position:absolute;top:50%;right:-15%;transform:translateY(-50%);width:300px;height:300px;border:2px solid var(--accent1);border-radius:50%;opacity:.1;box-shadow:0 0 0 42px var(--accent1),0 0 0 82px var(--accent2);} .theme-observ .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-15%;transform:translateY(-50%);width:100px;height:100px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);border-radius:50%;opacity:.2;filter:blur(10px);}
/* ===== ollama (dots) ===== */
.theme-ollama .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-ollama .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== opart (stripes) ===== */
.theme-opart .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-opart .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== openai (radial) ===== */
.theme-openai .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-openai .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== orchid (curves) ===== */
.theme-orchid .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-orchid .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== ornate (curves) ===== */
.theme-ornate .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-ornate .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== paas (clouds) ===== */
.theme-paas .cv-bg-decoration::before {content:"";position:absolute;top:-10%;left:-5%;width:300px;height:150px;background:radial-gradient(ellipse,var(--accent1) 0%,transparent 60%);opacity:.1;filter:blur(30px);border-radius:50%;} .theme-paas .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;right:-5%;width:350px;height:180px;background:radial-gradient(ellipse,var(--accent2) 0%,transparent 60%);opacity:.12;filter:blur(35px);border-radius:50%;}
/* ===== painting (bokeh) ===== */
.theme-painting .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-painting .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== parametric (curves) ===== */
.theme-parametric .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-parametric .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== paris (curves) ===== */
.theme-paris .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-paris .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== parrot (leaves) ===== */
.theme-parrot .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-parrot .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== particles (dots) ===== */
.theme-particles .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-particles .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== party (radial) ===== */
.theme-party .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-party .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== pattern (weave) ===== */
.theme-pattern .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-pattern .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== pearlescent (aura) ===== */
.theme-pearlescent .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-pearlescent .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== persian (weave) ===== */
.theme-persian .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-persian .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== photo2 (bokeh) ===== */
.theme-photo2 .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-photo2 .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== picnic (leaves) ===== */
.theme-picnic .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-picnic .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== pine (triangles) ===== */
.theme-pine .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-pine .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== plum (dots) ===== */
.theme-plum .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-plum .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== poetry (curves) ===== */
.theme-poetry .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-poetry .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== porcelain (aura) ===== */
.theme-porcelain .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-porcelain .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== postgres (grid) ===== */
.theme-postgres .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-postgres .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== posthuman (circuit) ===== */
.theme-posthuman .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-posthuman .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== pottery (weave) ===== */
.theme-pottery .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-pottery .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== preppy (stripes) ===== */
.theme-preppy .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-preppy .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== prism (triangles) ===== */
.theme-prism .cv-bg-decoration::before {content:"";position:absolute;top:0;right:0;width:0;height:0;border-style:solid;border-width:0 200px 200px 0;border-color:transparent var(--accent1) transparent transparent;opacity:.08;} .theme-prism .cv-bg-decoration::after {content:"";position:absolute;bottom:0;left:0;width:0;height:0;border-style:solid;border-width:150px 0 0 150px;border-color:transparent transparent transparent var(--accent2);opacity:.1;}
/* ===== prometheus (rings) ===== */
.theme-prometheus .cv-bg-decoration::before {content:"";position:absolute;top:50%;right:-15%;transform:translateY(-50%);width:300px;height:300px;border:2px solid var(--accent1);border-radius:50%;opacity:.1;box-shadow:0 0 0 42px var(--accent1),0 0 0 82px var(--accent2);} .theme-prometheus .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-15%;transform:translateY(-50%);width:100px;height:100px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);border-radius:50%;opacity:.2;filter:blur(10px);}
/* ===== prompt (terminal) ===== */
.theme-prompt .cv-bg-decoration::before {content:">_";position:absolute;top:8%;left:3%;font-family:monospace;font-size:14px;color:var(--accent1);opacity:.3;letter-spacing:2px;} .theme-prompt .cv-bg-decoration::after {content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0,transparent 3px,var(--accent1) 3px,var(--accent1) 4px);opacity:.03;mix-blend-mode:screen;}
/* ===== punk (zigzag) ===== */
.theme-punk .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-punk .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== puzzle (origami) ===== */
.theme-puzzle .cv-bg-decoration::before {content:"";position:absolute;top:15%;right:10%;width:100px;height:100px;background:var(--accent1);clip-path:polygon(50% 0%,100% 50%,50% 100%,0% 50%);opacity:.1;filter:blur(1px);} .theme-puzzle .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;left:5%;width:80px;height:80px;background:var(--accent2);clip-path:polygon(50% 0%,100% 50%,50% 100%,0% 50%);opacity:.12;transform:rotate(30deg);}
/* ===== python (circuit) ===== */
.theme-python .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-python .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== pytorch (neural) ===== */
.theme-pytorch .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 3px,transparent 4px),radial-gradient(circle at 50% 50%,var(--accent2) 3px,transparent 4px),radial-gradient(circle at 80% 70%,var(--accent1) 3px,transparent 4px),radial-gradient(circle at 30% 70%,var(--accent2) 2px,transparent 3px),radial-gradient(circle at 70% 20%,var(--accent1) 2px,transparent 3px);opacity:.15;} .theme-pytorch .cv-bg-decoration::after {content:"";position:absolute;top:30%;left:15%;width:70%;height:40%;background:linear-gradient(20deg,transparent 48%,var(--accent1) 48%,var(--accent1) 50%,transparent 50%),linear-gradient(-30deg,transparent 48%,var(--accent2) 48%,var(--accent2) 50%,transparent 50%);opacity:.06;}
/* ===== quantum2 (rings) ===== */
.theme-quantum2 .cv-bg-decoration::before {content:"";position:absolute;top:50%;right:-15%;transform:translateY(-50%);width:300px;height:300px;border:2px solid var(--accent1);border-radius:50%;opacity:.1;box-shadow:0 0 0 42px var(--accent1),0 0 0 82px var(--accent2);} .theme-quantum2 .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-15%;transform:translateY(-50%);width:100px;height:100px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);border-radius:50%;opacity:.2;filter:blur(10px);}
/* ===== rabbit (dots) ===== */
.theme-rabbit .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-rabbit .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== racing (stripes) ===== */
.theme-racing .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-racing .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== rag (circuit) ===== */
.theme-rag .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-rag .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== ramen (waves) ===== */
.theme-ramen .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-ramen .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== react (circuit) ===== */
.theme-react .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-react .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== reading (bricks) ===== */
.theme-reading .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-reading .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== redis (beams) ===== */
.theme-redis .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-redis .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== regex (barcode) ===== */
.theme-regex .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 0,var(--accent1) 3px,transparent 3px,transparent 8px,var(--accent1) 8px,var(--accent1) 10px,transparent 10px,transparent 15px);opacity:.05;mix-blend-mode:screen;} .theme-regex .cv-bg-decoration::after {content:"";position:absolute;top:30%;right:8%;width:60px;height:60px;border:2px solid var(--accent2);opacity:.15;transform:rotate(45deg);}
/* ===== reggae (stripes) ===== */
.theme-reggae .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-reggae .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== restapi (circuit) ===== */
.theme-restapi .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-restapi .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== roadtrip (stripes) ===== */
.theme-roadtrip .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-roadtrip .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== rock (zigzag) ===== */
.theme-rock .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-rock .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== rococo (curves) ===== */
.theme-rococo .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-rococo .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== roman (steps) ===== */
.theme-roman .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-roman .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== romance (bokeh) ===== */
.theme-romance .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-romance .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== rose (curves) ===== */
.theme-rose .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-rose .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== rpg (steps) ===== */
.theme-rpg .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-rpg .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== running (stripes) ===== */
.theme-running .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-running .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== russian (aura) ===== */
.theme-russian .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-russian .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== rust (circuit) ===== */
.theme-rust .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-rust .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== saas (clouds) ===== */
.theme-saas .cv-bg-decoration::before {content:"";position:absolute;top:-10%;left:-5%;width:300px;height:150px;background:radial-gradient(ellipse,var(--accent1) 0%,transparent 60%);opacity:.1;filter:blur(30px);border-radius:50%;} .theme-saas .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;right:-5%;width:350px;height:180px;background:radial-gradient(ellipse,var(--accent2) 0%,transparent 60%);opacity:.12;filter:blur(35px);border-radius:50%;}
/* ===== sandbox (bricks) ===== */
.theme-sandbox .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-sandbox .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== scales (weave) ===== */
.theme-scales .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-scales .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== scifi (stars) ===== */
.theme-scifi .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(1px 1px at 20% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 60% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 50%,var(--accent1),transparent),radial-gradient(1px 1px at 80% 10%,var(--accent2),transparent),radial-gradient(1px 1px at 90% 60%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 33% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 15% 65%,var(--accent1),transparent);opacity:.25;} .theme-scifi .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.12;filter:blur(20px);border-radius:50%;}
/* ===== seal2 (steps) ===== */
.theme-seal2 .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-seal2 .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== security (shield) ===== */
.theme-security .cv-bg-decoration::before {content:"";position:absolute;top:15%;right:8%;width:100px;height:120px;background:var(--accent1);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);opacity:.08;filter:blur(2px);} .theme-security .cv-bg-decoration::after {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 60px,var(--accent2) 60px,var(--accent2) 61px);opacity:.04;mix-blend-mode:screen;}
/* ===== serverless (dots) ===== */
.theme-serverless .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 2px,transparent 2px);background-size:25px 25px;opacity:.1;} .theme-serverless .cv-bg-decoration::after {content:"";position:absolute;top:15%;right:10%;width:120px;height:120px;border:3px dashed var(--accent2);border-radius:50%;opacity:.15;}
/* ===== seventies (stripes) ===== */
.theme-seventies .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-seventies .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== shadow (fog) ===== */
.theme-shadow .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 30% 40%,var(--accent1) 0%,transparent 40%),radial-gradient(ellipse at 70% 60%,var(--accent2) 0%,transparent 40%);opacity:.1;filter:blur(40px);} .theme-shadow .cv-bg-decoration::after {content:"";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:300px;height:1px;background:var(--accent1);opacity:.2;filter:blur(3px);box-shadow:0 30px 0 var(--accent2),0 -30px 0 var(--accent1);}
/* ===== shanghai (beams) ===== */
.theme-shanghai .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-shanghai .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== shuimo (curves) ===== */
.theme-shuimo .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-shuimo .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== silk (curves) ===== */
.theme-silk .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-silk .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== silver (beams) ===== */
.theme-silver .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-silver .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== sixties (curves) ===== */
.theme-sixties .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-sixties .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== skate (zigzag) ===== */
.theme-skate .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-skate .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== skiing (snow) ===== */
.theme-skiing .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(2px 2px at 10% 20%,var(--accent1),transparent),radial-gradient(1px 1px at 30% 50%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 70% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 85% 40%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 20% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 60% 10%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 90% 85%,var(--accent2),transparent);opacity:.2;} .theme-skiing .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;left:-10%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.12;filter:blur(30px);border-radius:50%;}
/* ===== slow (aura) ===== */
.theme-slow .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-slow .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== snow2 (snow) ===== */
.theme-snow2 .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(2px 2px at 10% 20%,var(--accent1),transparent),radial-gradient(1px 1px at 30% 50%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 70% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 85% 40%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 20% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 60% 10%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 90% 85%,var(--accent2),transparent);opacity:.2;} .theme-snow2 .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;left:-10%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.12;filter:blur(30px);border-radius:50%;}
/* ===== solarpunk (leaves) ===== */
.theme-solarpunk .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-solarpunk .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== spring (leaves) ===== */
.theme-spring .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-spring .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== springfestival (radial) ===== */
.theme-springfestival .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-springfestival .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== spy (noise) ===== */
.theme-spy .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 1px,transparent 1px);background-size:15px 15px,20px 20px;background-position:0 0,7px 7px;opacity:.06;mix-blend-mode:screen;} .theme-spy .cv-bg-decoration::after {content:"";position:absolute;top:20%;left:-10%;width:200px;height:60%;background:linear-gradient(45deg,transparent,var(--accent2),transparent);opacity:.08;filter:blur(40px);transform:rotate(-15deg);}
/* ===== sqlite (grid) ===== */
.theme-sqlite .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-sqlite .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== ssh (terminal) ===== */
.theme-ssh .cv-bg-decoration::before {content:">_";position:absolute;top:8%;left:3%;font-family:monospace;font-size:14px;color:var(--accent1);opacity:.3;letter-spacing:2px;} .theme-ssh .cv-bg-decoration::after {content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0,transparent 3px,var(--accent1) 3px,var(--accent1) 4px);opacity:.03;mix-blend-mode:screen;}
/* ===== stable (grid) ===== */
.theme-stable .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-stable .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== stargazing (stars) ===== */
.theme-stargazing .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(1px 1px at 20% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 60% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 50%,var(--accent1),transparent),radial-gradient(1px 1px at 80% 10%,var(--accent2),transparent),radial-gradient(1px 1px at 90% 60%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 33% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 15% 65%,var(--accent1),transparent);opacity:.25;} .theme-stargazing .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.12;filter:blur(20px);border-radius:50%;}
/* ===== starlight (stars) ===== */
.theme-starlight .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(1px 1px at 20% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 60% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 50%,var(--accent1),transparent),radial-gradient(1px 1px at 80% 10%,var(--accent2),transparent),radial-gradient(1px 1px at 90% 60%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 33% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 15% 65%,var(--accent1),transparent);opacity:.25;} .theme-starlight .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.12;filter:blur(20px);border-radius:50%;}
/* ===== stone (bricks) ===== */
.theme-stone .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-stone .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== storm (noise) ===== */
.theme-storm .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 1px,transparent 1px);background-size:15px 15px,20px 20px;background-position:0 0,7px 7px;opacity:.06;mix-blend-mode:screen;} .theme-storm .cv-bg-decoration::after {content:"";position:absolute;top:20%;left:-10%;width:200px;height:60%;background:linear-gradient(45deg,transparent,var(--accent2),transparent);opacity:.08;filter:blur(40px);transform:rotate(-15deg);}
/* ===== sumi_e (curves) ===== */
.theme-sumi_e .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-sumi_e .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== summer (radial) ===== */
.theme-summer .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-summer .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== sunflower (radial) ===== */
.theme-sunflower .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-sunflower .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== surf (waves) ===== */
.theme-surf .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-surf .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== surreal (aura) ===== */
.theme-surreal .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-surreal .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== sushi2 (waves) ===== */
.theme-sushi2 .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-sushi2 .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== svelte (circuit) ===== */
.theme-svelte .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-svelte .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== swimming (waves) ===== */
.theme-swimming .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-swimming .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== tailwind (waves) ===== */
.theme-tailwind .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-tailwind .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== tattoo (curves) ===== */
.theme-tattoo .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-tattoo .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== tea (steam) ===== */
.theme-tea .cv-bg-decoration::before {content:"";position:absolute;bottom:10%;left:10%;width:3px;height:200px;background:linear-gradient(to top,transparent,var(--accent1),transparent);opacity:.15;filter:blur(8px);border-radius:50%;} .theme-tea .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:15%;width:3px;height:180px;background:linear-gradient(to top,transparent,var(--accent2),transparent);opacity:.12;filter:blur(10px);border-radius:50%;transform:skewX(-10deg);}
/* ===== techno (beams) ===== */
.theme-techno .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-techno .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== temple (steps) ===== */
.theme-temple .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-temple .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== tennis (curves) ===== */
.theme-tennis .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-tennis .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== tensorflow (neural) ===== */
.theme-tensorflow .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 3px,transparent 4px),radial-gradient(circle at 50% 50%,var(--accent2) 3px,transparent 4px),radial-gradient(circle at 80% 70%,var(--accent1) 3px,transparent 4px),radial-gradient(circle at 30% 70%,var(--accent2) 2px,transparent 3px),radial-gradient(circle at 70% 20%,var(--accent1) 2px,transparent 3px);opacity:.15;} .theme-tensorflow .cv-bg-decoration::after {content:"";position:absolute;top:30%;left:15%;width:70%;height:40%;background:linear-gradient(20deg,transparent 48%,var(--accent1) 48%,var(--accent1) 50%,transparent 50%),linear-gradient(-30deg,transparent 48%,var(--accent2) 48%,var(--accent2) 50%,transparent 50%);opacity:.06;}
/* ===== terminal (terminal) ===== */
.theme-terminal .cv-bg-decoration::before {content:">_";position:absolute;top:8%;left:3%;font-family:monospace;font-size:14px;color:var(--accent1);opacity:.3;letter-spacing:2px;} .theme-terminal .cv-bg-decoration::after {content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0,transparent 3px,var(--accent1) 3px,var(--accent1) 4px);opacity:.03;mix-blend-mode:screen;}
/* ===== terraform (grid) ===== */
.theme-terraform .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-terraform .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== tibet (aura) ===== */
.theme-tibet .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-tibet .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== tiltshift (stripes) ===== */
.theme-tiltshift .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-tiltshift .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== tokyo (beams) ===== */
.theme-tokyo .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-tokyo .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== tsunami (waves) ===== */
.theme-tsunami .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-tsunami .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== tulip (leaves) ===== */
.theme-tulip .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-tulip .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}
/* ===== typescript (circuit) ===== */
.theme-typescript .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-typescript .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== ukiyoe (waves) ===== */
.theme-ukiyoe .cv-bg-decoration::before {content:"";position:absolute;bottom:0;left:0;right:0;height:40%;background:repeating-linear-gradient(90deg,transparent 0,var(--accent1) 2px,transparent 4px,transparent 40px);-webkit-mask:linear-gradient(to top,black,transparent);mask:linear-gradient(to top,black,transparent);opacity:.12;} .theme-ukiyoe .cv-bg-decoration::after {content:"";position:absolute;top:-10%;right:-10%;width:250px;height:250px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.18;filter:blur(30px);border-radius:50%;}
/* ===== valentine (bokeh) ===== */
.theme-valentine .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-valentine .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== valley (curves) ===== */
.theme-valley .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-valley .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== vibe (radial) ===== */
.theme-vibe .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-vibe .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== viking (zigzag) ===== */
.theme-viking .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,transparent 0,transparent 20px,var(--accent1) 20px,var(--accent1) 22px,transparent 22px,transparent 42px,var(--accent2) 42px,var(--accent2) 44px);opacity:.06;mix-blend-mode:screen;} .theme-viking .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:-5%;width:150px;height:200px;background:var(--accent2);clip-path:polygon(40% 0%,60% 30%,30% 50%,55% 100%,35% 60%,65% 40%);opacity:.1;filter:blur(1px);}
/* ===== vim (terminal) ===== */
.theme-vim .cv-bg-decoration::before {content:">_";position:absolute;top:8%;left:3%;font-family:monospace;font-size:14px;color:var(--accent1);opacity:.3;letter-spacing:2px;} .theme-vim .cv-bg-decoration::after {content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0,transparent 3px,var(--accent1) 3px,var(--accent1) 4px);opacity:.03;mix-blend-mode:screen;}
/* ===== vite (beams) ===== */
.theme-vite .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-vite .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== volcano (radial) ===== */
.theme-volcano .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:conic-gradient(from 0deg at 70% 50%,transparent 0deg,var(--accent1) 5deg,transparent 10deg,transparent 30deg,var(--accent2) 35deg,transparent 40deg,transparent 60deg,var(--accent1) 65deg,transparent 70deg,transparent 90deg,var(--accent2) 95deg,transparent 100deg);opacity:.08;mix-blend-mode:screen;} .theme-volcano .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:0;transform:translateY(-50%);width:150px;height:150px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.2;filter:blur(15px);border-radius:50%;}
/* ===== voronoi (hexagon) ===== */
.theme-voronoi .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(-60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(0deg,var(--accent1) 1px,transparent 1px,transparent 35px);opacity:.06;mix-blend-mode:screen;} .theme-voronoi .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:5%;width:80px;height:92px;background:var(--accent2);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);opacity:.12;}
/* ===== vscode (grid) ===== */
.theme-vscode .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px);background-size:40px 40px;opacity:.08;mix-blend-mode:screen;} .theme-vscode .cv-bg-decoration::after {content:"";position:absolute;top:10%;right:-5%;width:200px;height:200px;border:2px solid var(--accent2);border-radius:50%;opacity:.12;filter:blur(1px);}
/* ===== vue (circuit) ===== */
.theme-vue .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:linear-gradient(var(--accent1) 1px,transparent 1px),linear-gradient(90deg,var(--accent1) 1px,transparent 1px),radial-gradient(var(--accent2) 2px,transparent 2px);background-size:50px 50px,50px 50px,50px 50px;opacity:.07;mix-blend-mode:screen;} .theme-vue .cv-bg-decoration::after {content:"";position:absolute;bottom:15%;right:10%;width:100px;height:100px;border:2px solid var(--accent2);border-radius:8px;opacity:.15;box-shadow:inset 0 0 20px var(--accent2);}
/* ===== wabi (aura) ===== */
.theme-wabi .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-wabi .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== weaving (weave) ===== */
.theme-weaving .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,var(--accent1) 0,var(--accent1) 2px,transparent 2px,transparent 12px),repeating-linear-gradient(90deg,var(--accent2) 0,var(--accent2) 2px,transparent 2px,transparent 12px);opacity:.05;mix-blend-mode:screen;} .theme-weaving .cv-bg-decoration::after {content:"";position:absolute;top:20%;right:5%;width:140px;height:140px;border:2px solid var(--accent1);border-radius:50%;opacity:.12;}
/* ===== web3 (hexagon) ===== */
.theme-web3 .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(-60deg,var(--accent1) 1px,transparent 1px,transparent 35px),repeating-linear-gradient(0deg,var(--accent1) 1px,transparent 1px,transparent 35px);opacity:.06;mix-blend-mode:screen;} .theme-web3 .cv-bg-decoration::after {content:"";position:absolute;bottom:10%;right:5%;width:80px;height:92px;background:var(--accent2);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);opacity:.12;}
/* ===== webpack (bricks) ===== */
.theme-webpack .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-webpack .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== western (stripes) ===== */
.theme-western .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(135deg,transparent 0,transparent 30px,var(--accent1) 30px,var(--accent1) 31px);opacity:.06;} .theme-western .cv-bg-decoration::after {content:"";position:absolute;bottom:-10%;left:-5%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 70%);opacity:.15;filter:blur(20px);}
/* ===== willow (curves) ===== */
.theme-willow .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-willow .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== windmill (steps) ===== */
.theme-windmill .cv-bg-decoration::before {content:"";position:absolute;bottom:0;right:0;width:250px;height:250px;background:linear-gradient(135deg,transparent 40%,var(--accent1) 40%,var(--accent1) 50%,transparent 50%),linear-gradient(135deg,transparent 60%,var(--accent2) 60%,var(--accent2) 70%,transparent 70%);opacity:.1;clip-path:polygon(100% 0%,100% 100%,0% 100%);} .theme-windmill .cv-bg-decoration::after {content:"";position:absolute;top:10%;left:5%;width:100px;height:100px;border:2px solid var(--accent1);opacity:.12;border-radius:4px;}
/* ===== wine (bokeh) ===== */
.theme-wine .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,var(--accent1) 0%,transparent 8%),radial-gradient(circle at 70% 60%,var(--accent2) 0%,transparent 6%),radial-gradient(circle at 40% 80%,var(--accent1) 0%,transparent 5%),radial-gradient(circle at 85% 20%,var(--accent2) 0%,transparent 7%);opacity:.12;filter:blur(10px);} .theme-wine .cv-bg-decoration::after {content:"";position:absolute;top:50%;right:-10%;transform:translateY(-50%);width:200px;height:200px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.15;filter:blur(30px);border-radius:50%;}
/* ===== winter (snow) ===== */
.theme-winter .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:radial-gradient(2px 2px at 10% 20%,var(--accent1),transparent),radial-gradient(1px 1px at 30% 50%,var(--accent2),transparent),radial-gradient(2px 2px at 50% 30%,var(--accent1),transparent),radial-gradient(1px 1px at 70% 70%,var(--accent2),transparent),radial-gradient(2px 2px at 85% 40%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 20% 80%,var(--accent2),transparent),radial-gradient(1px 1px at 60% 10%,var(--accent1),transparent),radial-gradient(1.5px 1.5px at 90% 85%,var(--accent2),transparent);opacity:.2;} .theme-winter .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;left:-10%;width:300px;height:300px;background:radial-gradient(circle,var(--accent2) 0%,transparent 60%);opacity:.12;filter:blur(30px);border-radius:50%;}
/* ===== wuxia (curves) ===== */
.theme-wuxia .cv-bg-decoration::before {content:"";position:absolute;top:-30%;right:-20%;width:500px;height:500px;border:2px solid var(--accent1);border-radius:50%;opacity:.08;clip-path:polygon(50% 0%,100% 0%,100% 50%,50% 50%);} .theme-wuxia .cv-bg-decoration::after {content:"";position:absolute;bottom:-30%;left:-20%;width:400px;height:400px;border:2px solid var(--accent2);border-radius:50%;opacity:.1;clip-path:polygon(0% 50%,50% 50%,50% 100%,0% 100%);}
/* ===== y2k2 (beams) ===== */
.theme-y2k2 .cv-bg-decoration::before {content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0,transparent 80px,var(--accent1) 80px,var(--accent1) 81px,transparent 81px,transparent 120px);opacity:.07;mix-blend-mode:screen;} .theme-y2k2 .cv-bg-decoration::after {content:"";position:absolute;top:0;right:20%;width:2px;height:100%;background:linear-gradient(to bottom,transparent,var(--accent2),transparent);opacity:.4;filter:blur(2px);box-shadow:0 0 20px var(--accent2);}
/* ===== yaml (bricks) ===== */
.theme-yaml .cv-bg-decoration::before {content:"";position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 29px,var(--accent1) 29px,var(--accent1) 30px),repeating-linear-gradient(90deg,transparent 0,transparent 59px,var(--accent1) 59px,var(--accent1) 60px);opacity:.06;mix-blend-mode:screen;} .theme-yaml .cv-bg-decoration::after {content:"";position:absolute;bottom:-5%;right:-5%;width:180px;height:180px;border:3px solid var(--accent2);opacity:.1;transform:rotate(15deg);}
/* ===== yoga (aura) ===== */
.theme-yoga .cv-bg-decoration::before {content:"";position:absolute;top:-20%;left:-10%;width:400px;height:400px;background:radial-gradient(circle,var(--accent1) 0%,transparent 50%);opacity:.12;filter:blur(40px);border-radius:50%;} .theme-yoga .cv-bg-decoration::after {content:"";position:absolute;bottom:-20%;right:-10%;width:350px;height:350px;background:radial-gradient(circle,var(--accent2) 0%,transparent 50%);opacity:.15;filter:blur(50px);border-radius:50%;}
/* ===== yunnan (leaves) ===== */
.theme-yunnan .cv-bg-decoration::before {content:"";position:absolute;top:10%;left:-5%;width:180px;height:180px;background:var(--accent1);clip-path:ellipse(50% 20% at 50% 50%);opacity:.08;transform:rotate(-30deg);filter:blur(2px);} .theme-yunnan .cv-bg-decoration::after {content:"";position:absolute;bottom:5%;right:-5%;width:220px;height:220px;background:var(--accent2);clip-path:ellipse(50% 25% at 50% 50%);opacity:.1;transform:rotate(45deg);filter:blur(3px);}

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
