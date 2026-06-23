---
name: xfg-skills-video-cover
description: >
  B站/YouTube 视频封面生成器。根据 PPT 内容、课程大纲或文本描述，
  自动生成大字体突出、俏皮、抓眼球的视频封面 HTML 页面。
  触发词：制作视频封面、生成B站封面、视频封面设计、做封面、
  cover design、bilibili cover、视频缩略图、PPT封面、
  课程封面、章节封面、封面生成。
  适用场景：(1) 从 PPT/HTML 提取章节生成封面
  (2) 根据文本描述直接生成封面
  (3) 批量生成系列课程封面
  (4) 自定义封面模板与配色方案。
license: Apache-2.0
metadata:
  author: xfg-studio
  version: "1.0.0"
  category: creative
  homepage: https://github.com/xfg-skills/xfg-skills-video-cover
allowed-tools: Read Write Edit Bash(python3:*) Bash(node:*)
---

# 视频封面生成器

根据 PPT 内容或文本描述，生成大字体突出、俏皮、抓眼球的 B站/YouTube 风格视频封面 HTML 页面。

## 功能概述

- 从 PPT/HTML 文件中提取章节信息，自动生成每个章节的 B站风格封面
- 支持纯文本描述直接生成封面
- 每个封面包含：超大主标题、副标题、标签栏、印章、装饰元素、底部金句
- 输出为独立 HTML 文件，可在浏览器中直接预览

## 使用方法

### 方式一：从 PPT/HTML 文件生成

```bash
python3 scripts/generate_covers.py --input <ppt.html> --output <covers.html>
```

参数说明：
- `--input`：PPT/HTML 文件路径（必需）
- `--output`：输出文件路径（默认：`./video-covers.html`）
- `--style`：封面风格，可选 `bilibili`（默认）/ `youtube` / `minimal`
- `--extract`：提取模式，可选 `chapters`（按章节，默认）/ `slides`（按页）

### 方式二：从文本描述生成

```bash
python3 scripts/generate_covers.py --output covers.html \
  --title "AI Shell 连接云服务器" \
  --subtitle "自然语言操控服务器" \
  --tags "AI Shell,自然语言,零配置" \
  --chapter 1 \
  --badge "新手友好" \
  --quote "告别命令行恐惧症"
```

### 方式三：批量生成（JSON 配置）

```bash
python3 scripts/generate_covers.py --config covers.json --output covers.html
```

JSON 配置格式：
```json
{
  "style": "bilibili",
  "covers": [
    {
      "title": "告别手敲SSH",
      "highlight_words": ["手敲SSH", "自然语言"],
      "subtitle": "AI Shell 连接云服务器",
      "tags": ["AI Shell", "自然语言", "零配置"],
      "chapter": 1,
      "badge": "新手友好",
      "quote": "告别命令行恐惧症",
      "bg_color": "#1a1a2e",
      "accent_color": "#e74c3c"
    }
  ]
}
```

## 封面设计规范

### 视觉要素

1. **主标题**：82px 超大字体，关键词高亮 + 微旋转（-3deg），俏皮感
2. **副标题**：28px，补充说明
3. **标签栏**：4 个彩色标签，与主题色协调
4. **印章**：右上角圆形印章，标注章节编号和类型（实战/进阶/上线/完结）
5. **背景装饰**：大半透明圆形渐变 + emoji 装饰 + 箭头指引
6. **底部金句**：一句抓眼球的短文案
7. **Badge**：左上角分类标签

### 配色方案

内置 9 套主题配色，详见 `references/color-schemes.md`。

选择逻辑：
- 第 1 节：深蓝+红橙（科技+活力）
- 第 2 节：深海蓝+青色（容器+清爽）
- 第 3 节：深紫+品红（数据库+热情）
- 第 4 节：深红+金黄（性能+警示）
- 第 5 节：深绿+亮绿（开发+生机）
- 第 6 节：靛蓝+紫（部署+神秘）
- 第 7 节：深棕+橙红（压测+火焰）
- 第 8 节：深蓝+天蓝（AI+未来）
- 第 9 节：深玫红+粉（对话+温暖）

也支持自定义颜色：`--bg-color "#1a1a2e" --accent-color "#e74c3c"`

### 字体规范

- 主标题：`Noto Sans SC` 900 weight，82px
- 副标题：`Noto Sans SC` 600 weight，28px
- 标签：`Noto Sans SC` 700 weight，15px
- 底部栏：`Noto Sans SC` 400 weight，13px

## 可用脚本

- **`scripts/generate_covers.py`** — 主生成脚本，支持 PPT 提取、单页生成、批量生成
- **`scripts/extract_chapters.py`** — 从 HTML/PPT 文件提取章节信息（被 generate_covers.py 内部调用）

## 可用资源

- **`references/color-schemes.md`** — 9 套主题配色方案详细定义
- **`references/design-spec.md`** — 封面设计规范（尺寸、字体、间距、动效）
- **`assets/cover-template.html`** — 单页封面 HTML 模板（含完整 CSS）
- **`assets/full-page-template.html`** — 完整演示文稿模板（含导航、缩略图、键盘交互）

## 工作流程

### 从 PPT 生成封面的完整流程

1. **读取 PPT 文件**：使用 `read` 工具读取 HTML/PPT 文件内容
2. **提取章节信息**：运行 `python3 scripts/generate_covers.py --input <ppt.html> --extract-only`，获取章节列表
3. **确认封面方案**：与用户确认每个封面的标题、配色、标签
4. **生成封面 HTML**：运行 `python3 scripts/generate_covers.py --input <ppt.html> --output <covers.html>`
5. **预览效果**：用浏览器打开生成的 HTML 文件

### 自定义封面生成流程

1. **准备内容**：确定每个封面的标题、副标题、标签、配色
2. **编写 JSON 配置**：按上述 JSON 格式编写配置文件
3. **运行生成**：`python3 scripts/generate_covers.py --config covers.json --output covers.html`
4. **预览与调整**：浏览器预览，如需调整修改配置后重新生成

## Gotchas

- PPT 提取依赖正则匹配，不同 PPT 结构可能需要调整 `extract_chapters.py` 中的正则
- 封面使用 Google Fonts（Noto Sans SC），首次加载需联网；离线场景需替换为本地字体
- 主标题使用 `transform: rotate(-3deg)` 制造俏皮感，过多高亮词会显得杂乱，建议每页不超过 2 个
- 底部金句控制在 15 字以内，超过会换行影响美观
- 印章文字最多 2 行，每行 3-4 个字
- 输出 HTML 文件包含完整 CSS/JS，无需外部依赖，可直接双击打开
- 生成 9 页以上封面时，文件体积会超过 80KB，注意 `write` 工具的写入限制
- 如遇写入截断，使用 `exec` 追加方式（`cat >> file`）补全剩余内容

## 错误处理

- **PPT 文件无法解析**：检查 HTML 结构，确认包含章节标识（如"第X节"或"Chapter"）
- **字体加载失败**：替换为系统字体 `PingFang SC` / `Microsoft YaHei`
- **颜色不协调**：参考 `references/color-schemes.md` 中的预设配色，避免自行搭配
- **脚本运行报错**：检查 Python 3 环境，确认无缺少依赖
