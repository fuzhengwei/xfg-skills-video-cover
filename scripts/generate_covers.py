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
}

# ===== 风格结构分类 =====
THEME_CATEGORIES = {
    "科技知识": {
        "icon": "🚀",
        "desc": "适合编程、AI、技术教程、知识科普",
        "themes": ["bold", "cyber", "minimal", "magazine", "pixel", "glass", "aurora"],
    },
    "生活娱乐": {
        "icon": "🎉",
        "desc": "适合搞笑、美食、游戏、综艺、宠物",
        "themes": ["funny", "food", "gaming", "variety", "cute", "clay"],
    },
    "视觉冲击": {
        "icon": "💥",
        "desc": "适合热点、评测、开箱、撕纸拼贴、潮流",
        "themes": ["paper", "dopamine", "doodle", "luxury", "vaporwave", "acid", "memphis", "comic", "neon"],
    },
    "文艺清新": {
        "icon": "🍃",
        "desc": "适合Vlog、旅行、动漫、手账、国风、复古",
        "themes": ["fresh", "anime", "cinema", "journal", "guochao", "sticker", "retro", "collage"],
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
    "aurora": [("1f30c","🌌"),("2728","✨"),("1f4ab","💫"),("1f31f","🌟"),("1f300","🌀"),("1f315","🌕")],
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
    # 先匹配新11种风格（更具体）
    for theme in ["vaporwave","acid","memphis","clay","glass","sticker","comic","neon","retro","collage","aurora"]:
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
