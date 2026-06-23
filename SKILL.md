---
name: xfg-skills-video-cover
description: >
  B站/小红书/微信视频号/YouTube 视频封面生成器。根据 PPT 内容、课程大纲或文本描述，
  自动生成大字体突出、俏皮、抓眼球的爆款视频封面 HTML 页面。
  内置多平台尺寸（B站16:9、小红书3:4、视频号9:16）、20+套爆款配色、
  卡通素材库（Twemoji SVG + 开源插画），一键生成多页封面供截图使用。
  触发词：制作视频封面、生成B站封面、视频封面设计、做封面、
  cover design、bilibili cover、视频缩略图、PPT封面、
  课程封面、章节封面、封面生成、小红书封面、视频号封面。
  适用场景：(1) 从 PPT/HTML 提取章节生成封面
  (2) 根据文本描述直接生成封面
  (3) 批量生成系列课程封面
  (4) 多平台尺寸封面一键生成
  (5) 自定义封面模板与配色方案。
license: Apache-2.0
metadata:
  author: xfg-studio
  version: "2.0.0"
  category: creative
  homepage: https://github.com/xfg-skills/xfg-skills-video-cover
allowed-tools: Read Write Edit Bash(python3:*) Bash(node:*) Bash(curl:*)
---

# 视频封面生成器 v2.0

根据 PPT 内容或文本描述，生成大字体突出、俏皮、抓眼球的 B站/小红书/微信视频号 风格爆款视频封面。

## 功能概述

- 从 PPT/HTML 文件中提取章节信息，自动生成每个章节的视频封面
- 支持纯文本描述直接生成封面
- 每个封面包含：超大主标题、副标题、标签栏、装饰元素、底部金句
- **多平台尺寸**：B站（16:9 / 1200×675）、小红书（3:4 / 900×1200）、微信视频号（9:16 / 1080×1920）
- **20+套爆款配色方案**：按主题分类（科技/热情/清爽/温暖/暗黑/渐变），自动匹配或手动选择
- **卡通素材库**：内置 Twemoji SVG（3000+表情）+ 开源插画 URL，按主题智能匹配装饰
- 输出为独立 HTML 文件，多页排列，可在浏览器中逐页截图

## 使用方法

### 方式一：从 PPT/HTML 文件生成

```bash
python3 scripts/generate_covers.py --input <ppt.html> --output <covers.html> --platform bilibili
```

参数说明：
- `--input`：PPT/HTML 文件路径（必需）
- `--output`：输出文件路径（默认：`./video-covers.html`）
- `--platform`：平台尺寸，可选 `bilibili`（默认）/ `xiaohongshu` / `wechat` / `all`
- `--theme`：配色主题，可选 `auto`（默认）/ `tech` / `hot` / `cool` / `warm` / `dark` / `gradient`，详见 `references/color-schemes.md`
- `--extract`：提取模式，可选 `chapters`（按章节，默认）/ `slides`（按页）

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
  --theme tech
```

### 方式三：批量生成（JSON 配置）

```bash
python3 scripts/generate_covers.py --config covers.json --output covers.html
```

JSON 配置格式：
```json
{
  "platform": "all",
  "theme": "auto",
  "covers": [
    {
      "title": "告别手敲SSH",
      "highlight_words": ["手敲SSH", "自然语言"],
      "subtitle": "AI Shell 连接云服务器",
      "tags": ["AI Shell", "自然语言", "零配置"],
      "badge": "新手友好",
      "quote": "告别命令行恐惧症",
      "theme": "tech"
    }
  ]
}
```

## 多平台尺寸

| 平台 | 比例 | 尺寸 | 说明 |
|------|------|------|------|
| bilibili | 16:9 | 1200×675 | B站视频封面标准尺寸 |
| xiaohongshu | 3:4 | 900×1200 | 小红书笔记封面 |
| wechat | 9:16 | 1080×1920 | 微信视频号封面 |

使用 `--platform all` 时，生成的 HTML 文件包含3页（每个平台一页），可在浏览器中逐页截图。

## 配色主题

内置 20+ 套爆款配色，按主题分类，详见 `references/color-schemes.md`。

| 主题 | 风格 | 适用场景 |
|------|------|---------|
| tech | 科技感（深蓝/青/紫） | 编程、AI、云技术 |
| hot | 热情活力（红/橙/黄） | 教程、入门、实战 |
| cool | 清爽冷色（蓝/绿/青） | Docker、运维、工具 |
| warm | 温暖柔和（粉/紫/玫红） | 设计、生活、对话 |
| dark | 暗黑酷炫（黑/深灰/金） | 安全、高级、硬核 |
| gradient | 渐变潮流（多色渐变） | 时尚、创意、爆款 |

选择逻辑：`--theme auto` 时根据标题关键词智能匹配主题。

## 卡通素材库

### Twemoji SVG（内置）

使用 Twitter 开源 Twemoji（CC-BY 4.0 协议，可免费商用）作为主要装饰素材。

CDN 格式：`https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/svg/{codepoint}.svg`

内置常用 emoji 编码映射，详见 `references/emoji-library.md`。

按主题智能匹配装饰 emoji：
- 科技主题：🚀 ⚡ 💻 🌐 🔧 📡
- Docker/容器：🐳 📦 🔵 🔧
- 数据库：🗄️ 🔐 💾 📊
- AI/大模型：🤖 🧠 ✨ 💡
- 部署/上线：🚀 🌐 🎉 ✅
- 压测/性能：🔥 ⚡ 📊 💪
- 对话/客服：💬 🤗 📱 💬

### 开源插画素材（在线）

以下素材库可免费商用，生成时按需从 URL 加载：

| 素材库 | 地址 | 协议 | 说明 |
|--------|------|------|------|
| unDraw | https://undraw.co/ | MIT | 扁平风插画，可自定义颜色 |
| ManyPixels | https://www.manypixels.co/gallery | MIT | 矢量插画 |
| Storyset | https://storyset.com/ | Free | 动画插画 |
| Open Peeps | https://openpeeps.com/ | CC0 | 手绘人物库 |

## 可用脚本

- **`scripts/generate_covers.py`** — 主生成脚本，支持 PPT 提取、单页生成、批量生成、多平台输出
- **`scripts/extract_chapters.py`** — 从 HTML/PPT 文件提取章节信息

## 可用资源

- **`references/color-schemes.md`** — 20+套爆款配色方案详细定义
- **`references/design-spec.md`** — 封面设计规范（尺寸、字体、间距、多平台适配）
- **`references/emoji-library.md`** — Twemoji emoji 编码映射表 + 主题匹配规则
- **`assets/cover-template.html`** — 单页封面 HTML 模板（含完整 CSS，多平台适配）
- **`assets/full-page-template.html`** — 完整演示文稿模板（含导航、缩略图、键盘交互）

## 工作流程

### 从文本描述生成封面（最常用）

1. **确定内容**：主标题、副标题、标签、高亮词、底部金句
2. **选择平台**：`--platform bilibili`（单页）/ `--platform all`（3页多平台）
3. **选择主题**：`--theme auto`（智能匹配）/ `--theme tech`（指定主题）
4. **运行生成**：`python3 scripts/generate_covers.py --title "..." --platform all --output covers.html`
5. **浏览器预览**：打开 HTML 文件，逐页截图保存

### 从 PPT 生成封面的完整流程

1. **读取 PPT 文件**：使用 `read` 工具读取 HTML/PPT 文件内容
2. **提取章节信息**：运行 `python3 scripts/generate_covers.py --input <ppt.html> --extract-only`
3. **确认封面方案**：与用户确认每个封面的标题、配色、标签
4. **生成封面 HTML**：运行 `python3 scripts/generate_covers.py --input <ppt.html> --output <covers.html>`
5. **预览效果**：用浏览器打开生成的 HTML 文件

### 自定义封面生成流程

1. **准备内容**：确定每个封面的标题、副标题、标签、配色
2. **编写 JSON 配置**：按上述 JSON 格式编写配置文件
3. **运行生成**：`python3 scripts/generate_covers.py --config covers.json --output covers.html`
4. **预览与调整**：浏览器预览，如需调整修改配置后重新生成

## 封面设计规范

### 视觉要素

1. **主标题**：大字体突出（B站72-82px / 小红书56-64px / 视频号48-56px），关键词高亮+微旋转，俏皮感
2. **副标题**：补充说明，字号约为主标题的1/3
3. **标签栏**：3-4个彩色标签，与主题色协调
4. **装饰元素**：大半透明圆形渐变 + Twemoji SVG 装饰 + 箭头指引
5. **底部金句**：一句抓眼球的短文案（≤15字）
6. **Badge**：分类标签（左上角）

### 多平台字体规范

| 平台 | 主标题 | 副标题 | 标签 |
|------|--------|--------|------|
| bilibili (16:9) | 82px / 900 | 28px / 600 | 15px / 700 |
| xiaohongshu (3:4) | 64px / 900 | 24px / 600 | 14px / 700 |
| wechat (9:16) | 56px / 900 | 22px / 600 | 13px / 700 |

## Gotchas

- PPT 提取依赖正则匹配，不同 PPT 结构可能需要调整 `extract_chapters.py` 中的正则
- 封面使用 Google Fonts（Noto Sans SC），首次加载需联网；离线场景需替换为本地字体
- 主标题使用 `transform: rotate(-3deg)` 制造俏皮感，过多高亮词会显得杂乱，建议每页不超过 2 个
- 底部金句控制在 15 字以内，超过会换行影响美观
- 输出 HTML 文件包含完整 CSS/JS，无需外部依赖，可直接双击打开
- 生成 9 页以上封面时，文件体积会超过 80KB，注意 `write` 工具的写入限制
- 如遇写入截断，使用 `exec` 追加方式（`cat >> file`）补全剩余内容
- Twemoji SVG 通过 CDN 加载，首次打开需联网；离线场景 emoji 装饰不显示但不影响布局
- `--platform all` 生成3页不同尺寸的封面，文件体积约为单页的3倍

## 错误处理

- **PPT 文件无法解析**：检查 HTML 结构，确认包含章节标识（如"第X节"或"Chapter"）
- **字体加载失败**：替换为系统字体 `PingFang SC` / `Microsoft YaHei`
- **颜色不协调**：参考 `references/color-schemes.md` 中的预设配色，避免自行搭配
- **脚本运行报错**：检查 Python 3 环境，确认无缺少依赖
- **Twemoji 加载失败**：检查网络连接，或替换为本地 emoji 字符
