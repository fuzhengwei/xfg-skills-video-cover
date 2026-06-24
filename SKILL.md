---
name: xfg-skills-video-cover
description: >
  B站/小红书/微信视频号/手机竖版 视频封面生成器。根据 PPT 内容、课程大纲或文本描述，
  自动生成大字体突出、俏皮、抓眼球的爆款视频封面 HTML 页面。
  内置55种风格（4大分类）、231套配色方案、差异化字体排版、4平台尺寸、
  iconfont卡通素材库(232个SVG)、真人出镜照片处理、爆款标题生成器。
  触发词：制作视频封面、生成B站封面、视频封面设计、做封面、
  cover design、bilibili cover、视频缩略图、PPT封面、
  课程封面、章节封面、封面生成、小红书封面、视频号封面、选主题、选风格。
  适用场景：(1) 从 PPT/HTML 提取章节生成封面
  (2) 根据文本描述直接生成封面
  (3) 批量生成系列课程封面
  (4) 多平台尺寸封面一键生成
  (5) 交互式主题选择预览
  (6) 真人出镜照片设计处理
  (7) 爆款标题自动生成
license: Apache-2.0
metadata:
  author: xfg-studio
  version: "8.0.0"
  category: creative
  homepage: https://github.com/xfg-skills/xfg-skills-video-cover
allowed-tools: Read Write Edit Bash(python3:*) Bash(node:*) Bash(curl:*) Bash(open:*)
---

# 视频封面生成器 v8.0

根据 PPT 内容或文本描述，生成大字体突出、俏皮、抓眼球的 B站/小红书/微信视频号 风格爆款视频封面。

## ✨ v8.0 新特性

- **55种风格 × 231套配色**：4大分类全覆盖
  - 🚀 科技知识(10)：bold/cyber/minimal/magazine/pixel/glass/aurora/blueprint/typewriter/starfield
  - 🎉 生活娱乐(8)：funny/food/gaming/variety/cute/clay/carnival/popart
  - 💥 视觉冲击(18)：paper/dopamine/doodle/luxury/vaporwave/acid/memphis/comic/neon/graffiti/brutalist/holographic/gradientmesh/screenshot/portrait/product/contrast/zoom
  - 🍃 文艺清新(19)：fresh/anime/cinema/journal/guochao/sticker/retro/collage/ink/stamp/newspaper/polaroid/risograph/film/ribbon/pastel/terrarium/kraft/washi
- **真人出镜照片处理**：`--photo-url` 参数，55种风格各自不同的照片CSS处理（边框/圆角/滤镜/位置）
- **爆款标题生成器**：8种风格×6模板=48个模板，自动生成优化标题
- **iconfont API 集成**：`--auto-icons` 自动从 iconfont.cn 搜索下载图标
- **大卡通角色(Mascot)**：每个封面自动匹配 iconfont 卡通角色
- **iconfont 卡通素材库**：232 个本地 SVG 图标，5 大分类
- **4平台输出**：B站/小红书/微信视频号/手机竖版

## 55种风格分类

### 🚀 科技知识（10种）
| 代码 | 风格 | 适合 |
|------|------|------|
| `bold` | 📢 大字醒目 | 知识/教程/干货 |
| `cyber` | 🌃 赛博朋克 | AI/编程/科技 |
| `minimal` | ⚪ 极简风 | 商务/专业/科普 |
| `magazine` | 📰 杂志风 | 深度/商业/访谈 |
| `pixel` | 👾 像素风 | 复古/游戏/极客 |
| `glass` | 🔹 玻璃拟态 | 高级感/质感/通透 |
| `aurora` | 🌌 极光弥散 | 梦幻/光影/星空 |
| `blueprint` | 📐 蓝图风 | 工程/技术/制图 |
| `typewriter` | ⌨ 打字机风 | 文字/手稿/复古 |
| `starfield` | 🌌 星空宇宙 | 宇宙/银河/深空 |

### 🎉 生活娱乐（8种）
| 代码 | 风格 | 适合 |
|------|------|------|
| `funny` | 😂 搞笑整活 | 搞笑/吐槽/整活 |
| `food` | 🍜 美食暖调 | 美食/探店/烹饪 |
| `gaming` | 🎮 游戏电竞 | 游戏/电竞/通关 |
| `variety` | 💬 综艺弹幕 | 热点/吃瓜/反应 |
| `cute` | 🐱 萌宠可爱 | 宠物/萌系/卡通 |
| `clay` | 🧸 黏土风 | 3D/手工/童趣 |
| `carnival` | 🎪 嘉年华 | 派对/庆典/节日 |
| `popart` | 🎨 波普艺术 | 潮流/撞色/大众 |

### 💥 视觉冲击（18种）
| 代码 | 风格 | 适合 |
|------|------|------|
| `paper` | ✂️ 撕纸拼贴 | 评测/攻略/安利 |
| `dopamine` | 🌈 多巴胺撞色 | 潮流/快乐/穿搭 |
| `doodle` | 🖍️ 手绘涂鸦 | 文创/手帐/趣味 |
| `luxury` | 👑 黑金奢华 | 评测/开箱/高端 |
| `vaporwave` | 👾 蒸汽波 | 复古/迷幻/80s |
| `acid` | 🧪 酸性设计 | 实验/前卫/液态 |
| `memphis` | 🔷 孟菲斯 | 几何/活泼/拼接 |
| `comic` | 💥 漫画风 | 热血/格斗/美漫 |
| `neon` | 💡 霓虹灯 | 暗夜/招牌/荧光 |
| `graffiti` | 🎨 涂鸦街头 | 街头/嘻哈/反叛 |
| `brutalist` | 🏗️ 粗野主义 | 原始/粗犷/建筑 |
| `holographic` | 💎 全息彩虹 | 镭射/幻彩/变色 |
| `gradientmesh` | 🌊 网格渐变 | 柔和/梦幻/多色 |
| `screenshot` | 📸 真实截图 | 教程/源码/演示 |
| `portrait` | 👤 真人出镜 | 经验/职业/分享 |
| `product` | 📦 实物产品 | 测评/开箱/工具 |
| `contrast` | ⚔️ 对比冲击 | 对比/vs/盘点 |
| `zoom` | 🔍 局部放大 | 细节/重点/特写 |

### 🍃 文艺清新（19种）
| 代码 | 风格 | 适合 |
|------|------|------|
| `fresh` | 🍃 清新治愈 | Vlog/生活/旅行 |
| `anime` | 🌸 二次元动漫 | ACG/番剧/虚拟 |
| `cinema` | 🎬 影视悬疑 | 电影/解说/悬疑 |
| `journal` | 📓 手账风 | 笔记/记录/手写 |
| `guochao` | 🏮 国潮风 | 国风/传统/文化 |
| `sticker` | 🏷️ 贴纸风 | 手绘/可爱/拼贴 |
| `retro` | 📷 复古风 | 怀旧/胶片/80s |
| `collage` | 📰 拼贴风 | 剪报/混合/文艺 |
| `ink` | 🖌️ 水墨风 | 书法/国画/写意 |
| `stamp` | 🔴 印章风 | 篆刻/朱印/盖章 |
| `newspaper` | 📰 报纸风 | 新闻/报道/头条 |
| `polaroid` | 📸 拍立得 | 即时成像/回忆 |
| `risograph` | 🖨️ Riso印刷 | 孔版/颗粒/zine |
| `film` | 🎞️ 电影胶片 | 胶卷/片场/镜头 |
| `ribbon` | 🎀 缎带横幅 | 颁奖/礼盒/优雅 |
| `pastel` | 🎨 莫兰迪 | 柔色/低饱和/雅致 |
| `terrarium` | 🌿 玻璃生态 | 植物/微景观/自然 |
| `kraft` | 📄 牛皮纸 | 手工/质朴/原生态 |
| `washi` | 🎀 和纸胶带 | 和风/日式/手帐 |

## 真人出镜照片处理

当用户需要真人出镜时，通过 `--photo-url` 传入照片URL或本地路径。

### 工作流
1. 用户提供视频主题/标题
2. 确认是否需要真人出镜（要→用户提供照片URL；不要→走纯图标路线）
3. 生成带照片的封面预览
4. 不同风格自动对照片做不同CSS处理

### 5种照片处理预设
| 预设 | 边框 | 圆角 | 滤镜 | 适合 |
|------|------|------|------|------|
| 硬核揭秘 | 直角+红描边3px | 0 | 无 | bold/screenshot/brutalist |
| 科技工具 | 细线+投影 | 12px | contrast(1.1) | cyber/glass/neon |
| 情绪冲击 | 双层描边 | 8px | 无 | funny/variety/contrast |
| 游戏猎奇 | 厚边框4px | 16px | 无 | gaming/carnival/comic |
| 知识干货 | 干净无边框 | 20px | 无 | minimal/magazine/fresh |

### 用法
```bash
# 真人出镜 + 赛博朋克风格
python3 scripts/generate_covers.py \
  --title "AI编程实战" \
  --theme cyber \
  --photo-url "https://example.com/photo.jpg" \
  --photo-position right \
  --platform bilibili

# 真人出镜 + 真人出镜风格（portrait专用）
python3 scripts/generate_covers.py \
  --title "转行程序员的经验分享" \
  --theme portrait \
  --photo-url "/path/to/photo.jpg" \
  --photo-position right \
  --platform all
```

照片位置：`--photo-position right|left|center`（默认 right）

## 爆款标题生成器

内置 `title_generator.py`，8种标题风格自动优化。

### 8种标题风格
| 风格 | 示例 | 适合 |
|------|------|------|
| 😱 震惊体 | "震惊！Redis竟然这么快" | 热点/揭秘 |
| 💰 利益体 | "学会Docker，从此部署不愁" | 教程/技能 |
| 🤔 悬念体 | "Redis的3个秘密，第2个绝了" | 深度/探索 |
| 🔢 数字体 | "5分钟搞懂Redis缓存" | 干货/盘点 |
| ⚔️ 对比体 | "Redis vs Memcached，差距竟然这么大" | 评测/对比 |
| 😣 痛点体 | "还在手动查数据库？试试这个方法" | 解决方案 |
| 🔥 独家体 | "全网首发！Redis完整方案" | 新品/首发 |
| 🎮 挑战体 | "零基础Redis挑战，3天搞定" | 教学/实验 |

### 用法
```bash
# 命令行调用
python3 scripts/title_generator.py --title "Redis缓存" --tags "Redis,数据库,缓存"

# JSON输出
python3 scripts/title_generator.py --title "Docker部署" --json

# 指定风格
python3 scripts/title_generator.py --title "AI编程" --style shock
```

### AI流程集成
当用户给出标题时，先调用标题生成器生成优化方案，再让用户选择。

## 使用方法

### ⭐ 方式零：交互式主题选择（推荐！）

```bash
python3 scripts/theme_picker.py \
  --title "用户的标题" \
  --subtitle "副标题" \
  --tags "标签1,标签2,标签3" \
  --badge "徽章文字" \
  --highlight "高亮词1,高亮词2" \
  --output /path/to/theme-picker.html
```

生成55种风格预览的HTML页面，用户点击选择喜欢的风格。

### 方式一：从 PPT/HTML 文件生成

```bash
python3 scripts/generate_covers.py --input <ppt.html> --output <covers.html> --platform all --theme auto
```

### 方式二：从文本描述生成

```bash
python3 scripts/generate_covers.py --output covers.html \
  --title "Docker一装，运维轻松10倍" \
  --subtitle "容器化部署完整指南" \
  --tags "Docker,容器,运维" \
  --badge "硬核教程" \
  --quote "从此不再手动配环境" \
  --highlight "Docker,10倍" \
  --platform all \
  --theme cyber
```

### 方式三：真人出镜

```bash
python3 scripts/generate_covers.py --output covers.html \
  --title "转行程序员的经验分享" \
  --theme portrait \
  --photo-url "https://example.com/photo.jpg" \
  --photo-position right \
  --platform all
```

### 方式四：自动图标

```bash
python3 scripts/generate_covers.py --output covers.html \
  --title "AI Agent开发实战" \
  --theme cyber \
  --auto-icons \
  --platform all
```

## AI 使用流程（重要！）

### Step 1: 信息收集与标题优化

1. **信息收集**：如果用户只给了标题，主动询问内容介绍
2. **标题优化**：调用 `title_generator.py` 生成 3-5 个优化标题供选择
3. **真人确认**：询问是否需要真人出镜（要→请用户提供照片URL）

### Step 2: 一次性生成全部风格封面

```bash
python3 scripts/theme_picker.py \
  --title "最终标题" \
  --subtitle "副标题" \
  --tags "标签1,标签2" \
  --badge "徽章" \
  --highlight "高亮词1,高亮词2" \
  --output /path/to/theme-picker.html
```

### Step 3: 收集反馈，生成最终版

用户选定风格后，如有调整需求，用 `generate_covers.py` 针对性生成。

## 多平台尺寸

| 平台 | 代码 | 比例 | 尺寸 | 标题字号 |
|------|------|------|------|----------|
| B站 | bilibili | 16:9 | 1200×675 | 82px |
| 小红书 | xiaohongshu | 3:4 | 900×1200 | 64px |
| 视频号 | wechat | 9:16 | 1080×1920 | 56px |
| 手机竖版 | mobile | ~9:14.5 | 440×710 | 52px |

## 可用脚本

| 脚本 | 说明 |
|------|------|
| `scripts/generate_covers.py` | 主生成脚本，支持PPT提取/单页/批量/多平台/真人照片/自动图标 |
| `scripts/theme_picker.py` | 主题选择器，生成55种风格预览对比页 |
| `scripts/title_generator.py` | 爆款标题生成器，8种风格×6模板 |
| `scripts/download_icons.py` | iconfont图标下载器，从iconfont.cn搜索下载SVG |
| `scripts/extract_chapters.py` | 从HTML/PPT提取章节信息 |

## 关键参数

```bash
python3 generate_covers.py [选项]

必选（之一）:
  --title "标题"           直接生成单页
  --input ppt.html         从PPT提取
  --config covers.json     批量生成

常用:
  --theme auto             风格主题（55种可选，见上方分类表）
  --platform bilibili      平台（bilibili/xiaohongshu/wechat/mobile/all）
  --output covers.html     输出路径

真人出镜:
  --photo-url "URL"        照片URL或本地路径
  --photo-position right   照片位置（right/left/center）

自动图标:
  --auto-icons             根据标题自动从iconfont.cn下载图标

可选:
  --subtitle "副标题"
  --tags "标签1,标签2"
  --badge "徽章"
  --quote "底部金句"
  --highlight "高亮词1,高亮词2"
  --scheme cyber_2          指定具体配色ID
  --bg-color "#hex"         自定义背景色
  --accent-color "#hex"     自定义主色调
```

## Gotchas

- PPT 提取依赖正则匹配，不同 PPT 结构可能需要调整
- 使用 Google Fonts（Noto Sans SC + ZCOOL KuaiLe + Ma Shan Zheng），首次加载需联网
- 主标题高亮词建议不超过2个
- 底部金句控制在15字以内
- `--platform all` 生成4页，文件较大
- Twemoji SVG 通过 CDN 加载，离线场景 emoji 装饰不显示但不影响布局
- 真人出镜照片建议横版16:9或3:4比例，分辨率≥800px
- `--auto-icons` 需要网络连接访问 iconfont.cn API
- 55种风格中，screenshot/portrait/product/contrast/zoom 5种「真实派」风格默认隐藏 mascot 和 emoji 装饰
