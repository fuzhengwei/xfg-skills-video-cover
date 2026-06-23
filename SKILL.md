---
name: xfg-skills-video-cover
description: >
  B站/小红书/微信视频号/手机竖版 视频封面生成器。根据 PPT 内容、课程大纲或文本描述，
  自动生成大字体突出、俏皮、抓眼球的爆款视频封面 HTML 页面。
  内置13大B站爆款风格（大字醒目/赛博朋克/二次元/搞笑整活/黑金奢华/清新治愈/游戏电竞/美食暖调/影视悬疑/萌宠可爱/撕纸拼贴/综艺弹幕/手绘涂鸦）、
  50+套配色方案、差异化字体排版、4平台尺寸、Twemoji卡通素材库。
  触发词：制作视频封面、生成B站封面、视频封面设计、做封面、
  cover design、bilibili cover、视频缩略图、PPT封面、
  课程封面、章节封面、封面生成、小红书封面、视频号封面、选主题、选风格。
  适用场景：(1) 从 PPT/HTML 提取章节生成封面
  (2) 根据文本描述直接生成封面
  (3) 批量生成系列课程封面
  (4) 多平台尺寸封面一键生成
  (5) 交互式主题选择预览
license: Apache-2.0
metadata:
  author: xfg-studio
  version: "3.1.0"
  category: creative
  homepage: https://github.com/xfg-skills/xfg-skills-video-cover
allowed-tools: Read Write Edit Bash(python3:*) Bash(node:*) Bash(curl:*) Bash(open:*)
---

# 视频封面生成器 v3.1

根据 PPT 内容或文本描述，生成大字体突出、俏皮、抓眼球的 B站/小红书/微信视频号 风格爆款视频封面。

## ✨ v3.1 新特性

- **13大B站爆款风格**：每种风格有完全不同的字体排版、高亮方式、装饰元素
- **差异化字体排版**：不再是统一模板，每种风格的视觉表现完全不同
- **交互式主题选择器**：生成预览页，用户一眼看到所有风格效果再选
- **40+套配色方案**：每种风格4-5套配色
- **4平台输出**：B站/小红书/微信视频号/手机竖版
- **3种字体**：Noto Sans SC + ZCOOL KuaiLe + Ma Shan Zheng

## 13大B站爆款风格

这是本技能的核心。每种风格不是简单换色，而是完全不同的视觉设计语言：

| 代码 | 风格名 | 字体处理 | 高亮方式 | 适合场景 |
|------|--------|----------|----------|----------|
| `bold` | 📢 大字醒目 | 900粗体左对齐 | 荧光笔黄底黑字 | 知识区/教程/干货 |
| `cyber` | 🌃 赛博朋克 | 霓虹发光+扫描线 | 多层text-shadow光晕 | AI/编程/科技 |
| `anime` | 🌸 二次元动漫 | ZCOOL圆润体 | 白色描边+倾斜 | ACG/番剧/虚拟主播 |
| `funny` | 😂 搞笑整活 | 大小混排 | 旋转+波浪下划线 | 搞笑/整活/吐槽 |
| `luxury` | 👑 黑金奢华 | 衬线感+宽字距 | 上下双金线框 | 评测/开箱/高端 |
| `fresh` | 🍃 清新治愈 | 马善政手写体 | 波浪下划线 | Vlog/生活/旅行 |
| `gaming` | 🎮 游戏电竞 | 斜切skewX | 双色发光描边 | 游戏/电竞/通关 |
| `food` | 🍜 美食暖调 | 圆润800 | 圆角气泡背景 | 美食/探店/烹饪 |
| `cinema` | 🎬 影视悬疑 | 700+宽字距 | 底部粗线 | 电影解说/悬疑 |
| `cute` | 🐱 萌宠可爱 | ZCOOL手写体 | 气泡背景+旋转 | 宠物/萌系/卡通 |
| `paper` | ✂️ 撕纸拼贴 | 900+阴影 | clip-path不规则裁切 | 评测/攻略/安利 |
| `variety` | 💬 综艺弹幕 | 900+多层描边 | 花字+HOT标记 | 热点/吐槽/反应 |
| `doodle` | 🖍️ 手绘涂鸦 | ZCOOL手写体 | 虚线边框+波点 | 文创/手帐/趣味 |

## 使用方法

### ⭐ 方式零：交互式主题选择（推荐！）

**当用户说"帮我做封面"但没指定风格时，先生成主题选择器让用户选：**

```bash
python3 scripts/theme_picker.py \
  --title "用户的标题" \
  --subtitle "副标题" \
  --tags "标签1,标签2,标签3" \
  --badge "徽章文字" \
  --highlight "高亮词1,高亮词2" \
  --output /path/to/theme-picker.html
```

生成一个包含13种风格预览的HTML页面，用户在浏览器中点击选择喜欢的风格后，再用对应 `--theme` 参数生成正式封面。

### 方式一：从 PPT/HTML 文件生成

```bash
python3 scripts/generate_covers.py --input <ppt.html> --output <covers.html> --platform all --theme auto
```

### 方式二：从文本描述生成

```bash
python3 scripts/generate_covers.py --output covers.html \
  --title "给爷来个Key！自建中转站让AI自己找Key吃" \
  --subtitle "AI IDE / CLI × Skills = 全自动密钥供给" \
  --tags "自建中转站,AI IDE,Skills,自动找Key" \
  --badge "硬核教程·自给自足" \
  --quote "从此不再手动复制粘贴Key" \
  --highlight "给爷来个Key,自己找Key吃" \
  --platform all \
  --theme cyber
```

### 方式三：批量生成（JSON 配置）

```bash
python3 scripts/generate_covers.py --config covers.json --output covers.html
```

## AI 使用流程（重要！）

当用户要求生成视频封面时，按以下流程操作：

### Step 1: 确认内容

从用户输入或 PPT 中提取：标题、副标题、标签、高亮词、底部金句

### Step 2: 展示风格选择

**如果用户没有指定风格**，先运行主题选择器：

```bash
python3 scripts/theme_picker.py --title "标题" --output /tmp/theme-picker.html
```

然后用 `open` 命令打开，并告诉用户：

> 已为你生成风格选择预览页，共13种B站爆款风格：
> 1. 📢 大字醒目 - 适合知识区教程
> 2. 🌃 赛博朋克 - 适合AI/科技
> 3. 🌸 二次元动漫 - 适合ACG
> 4. 😂 搞笑整活 - 适合沙雕整活
> 5. 👑 黑金奢华 - 适合评测开箱
> 6. 🍃 清新治愈 - 适合Vlog生活
> 7. 🎮 游戏电竞 - 适合游戏
> 8. 🍜 美食暖调 - 适合美食
> 9. 🎬 影视悬疑 - 适合影视解说
> 10. 🐱 萌宠可爱 - 适合宠物萌系
> 11. ✂️ 撕纸拼贴 - 适合评测安利
> 12. 💬 综艺弹幕 - 适合热点吐槽
> 13. 🖍️ 手绘涂鸦 - 适合文创手帐
>
> 浏览器里预览效果，告诉我你选哪个，或者直接说"用赛博朋克风"就行。

### Step 3: 生成正式封面

用户选定后，用对应 `--theme` 参数生成：

```bash
python3 scripts/generate_covers.py --title "标题" --theme cyber --platform all --output covers.html
```

### Step 4: 打开预览

```bash
open covers.html
```

## 多平台尺寸

| 平台 | 比例 | 尺寸 | 说明 |
|------|------|------|------|
| bilibili | 16:9 | 1200×675 | B站视频封面标准尺寸 |
| xiaohongshu | 3:4 | 900×1200 | 小红书笔记封面 |
| wechat | 9:16 | 1080×1920 | 微信视频号封面 |
| mobile | 9:19.5 | 1284×2778 | 手机竖版（iPhone Pro Max 原生分辨率） |

使用 `--platform all` 时，4个平台各生成一页，底部缩略图标注平台名，键盘←→翻页。

## 配色方案

每种风格有4-5套配色，共40+套。详见 `references/color-schemes.md`。

- `--theme auto`：根据标题关键词智能匹配风格
- `--theme cyber`：指定赛博朋克风格
- `--scheme cyber_2`：指定具体配色ID（查看 color-schemes.md 获取完整列表）

## 可用脚本

| 脚本 | 说明 |
|------|------|
| `scripts/generate_covers.py` | 主生成脚本，支持PPT提取/单页/批量/多平台 |
| `scripts/theme_picker.py` | **主题选择器**，生成13种风格预览对比页 |
| `scripts/extract_chapters.py` | 从 HTML/PPT 提取章节信息 |

## 可用资源

- `references/color-schemes.md` — 50+套配色方案（13大风格分类）
- `references/design-spec.md` — 封面设计规范
- `references/emoji-library.md` — Twemoji emoji 编码映射 + 主题匹配
- `assets/cover-template.html` — 单页封面模板
- `assets/full-page-template.html` — 完整演示文稿模板

## 关键参数

```bash
python3 generate_covers.py [选项]

必选（之一）:
  --title "标题"           直接生成单页
  --input ppt.html         从PPT提取
  --config covers.json     批量生成

常用:
  --theme auto             风格主题（bold/cyber/anime/funny/luxury/fresh/gaming/food/cinema/cute/paper/variety/doodle）
  --platform bilibili      平台（bilibili/xiaohongshu/wechat/mobile/all）
  --output covers.html     输出路径

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

- PPT 提取依赖正则匹配，不同 PPT 结构可能需要调整 `extract_chapters.py`
- 使用 Google Fonts（Noto Sans SC + ZCOOL KuaiLe + Ma Shan Zheng），首次加载需联网
- 主标题高亮词建议不超过2个，过多会显得杂乱
- 底部金句控制在15字以内
- `--platform all` 生成4页，文件较大但可一次截图所有平台
- Twemoji SVG 通过 CDN 加载，离线场景 emoji 装饰不显示但不影响布局
- 主题选择器 `theme_picker.py` 也可传入自定义标题/标签，预览效果更贴近实际

## 错误处理

- **PPT 无法解析**：检查 HTML 结构，确认包含章节标识
- **字体加载失败**：替换为系统字体 PingFang SC / Microsoft YaHei
- **脚本运行报错**：检查 Python 3 环境
- **Twemoji 加载失败**：检查网络，或替换为本地 emoji 字符
