#!/usr/bin/env python3
"""
章节提取器 - 从 PPT/HTML 文件中提取章节信息
"""

import re
import sys
import json
import argparse


def extract_chapters_from_html(content):
    """
    从 HTML 内容中提取章节信息。
    
    支持的章节标识格式：
    - "第X节" / "第 X 节"
    - "Chapter X"
    - class="slide-chapter-cover" 或类似
    - <h1>/<h2> 中的标题文本
    - data-chapter="X"
    
    返回格式：
    [
        {
            "number": 1,
            "title": "AI Shell 连接云服务器",
            "subtitle": "...",
            "description": "...",
            "tags": [...],
            "badge": "...",
            "quote": "..."
        }
    ]
    """
    chapters = []
    
    # 方式1：匹配 "第X节" + 后续标题
    pattern1 = re.compile(
        r'第\s*(\d+)\s*节[^>]*>.*?(?:chapter[-_]?(?:title|main|icon)[^>]*>)?\s*(?:<[^>]*>)*\s*([^<]+)',
        re.DOTALL | re.IGNORECASE
    )
    matches = pattern1.findall(content)
    if matches:
        for num, title in matches:
            title = clean_text(title)
            if title and len(title) > 2:
                chapters.append({
                    "number": int(num),
                    "title": title,
                    "subtitle": "",
                    "description": "",
                    "tags": [],
                    "badge": f"第{num}节",
                    "quote": "",
                })
    
    # 方式2：匹配 chapter-cover 类
    if not chapters:
        pattern2 = re.compile(
            r'class="[^"]*chapter[^"]*cover[^"]*"[^>]*>(.*?)</div>\s*</div>',
            re.DOTALL
        )
        blocks = pattern2.findall(content)
        for i, block in enumerate(blocks):
            title = extract_title_from_block(block)
            if title:
                chapters.append({
                    "number": i + 1,
                    "title": title,
                    "subtitle": "",
                    "description": "",
                    "tags": [],
                    "badge": f"第{i+1}节",
                    "quote": "",
                })
    
    # 方式3：匹配 slide 中的 h1/h2 标题
    if not chapters:
        pattern3 = re.compile(
            r'<(?:h1|h2)[^>]*>(.*?)</(?:h1|h2)>',
            re.DOTALL
        )
        matches = pattern3.findall(content)
        for i, match in enumerate(matches):
            title = clean_text(match)
            if title and len(title) > 2 and not title.startswith('课程'):
                chapters.append({
                    "number": i + 1,
                    "title": title,
                    "subtitle": "",
                    "description": "",
                    "tags": [],
                    "badge": f"第{i+1}节",
                    "quote": "",
                })
    
    # 方式4：匹配 data-chapter 属性
    if not chapters:
        pattern4 = re.compile(r'data-chapter="(\d+)"[^>]*>(.*?)</div>', re.DOTALL)
        matches = pattern4.findall(content)
        for num, block in matches:
            title = extract_title_from_block(block)
            if title:
                chapters.append({
                    "number": int(num),
                    "title": title,
                    "subtitle": "",
                    "description": "",
                    "tags": [],
                    "badge": f"第{num}节",
                    "quote": "",
                })
    
    # 方式5：匹配 "第X节" 文本（简单模式）
    if not chapters:
        pattern5 = re.compile(r'第\s*(\d+)\s*节')
        matches = pattern5.findall(content)
        for num in matches:
            chapters.append({
                "number": int(num),
                "title": f"第{num}节",
                "subtitle": "",
                "description": "",
                "tags": [],
                "badge": f"第{num}节",
                "quote": "",
            })
    
    # 去重
    seen = set()
    unique_chapters = []
    for ch in chapters:
        key = ch["number"]
        if key not in seen:
            seen.add(key)
            unique_chapters.append(ch)
    
    return unique_chapters


def extract_title_from_block(block):
    """从 HTML 块中提取标题"""
    # 尝试匹配各种标题标签
    for tag in ['h1', 'h2', 'h3', 'span', 'div']:
        pattern = re.compile(rf'<{tag}[^>]*>(.*?)</{tag}>', re.DOTALL)
        match = pattern.search(block)
        if match:
            title = clean_text(match.group(1))
            if title and len(title) > 2:
                return title
    return None


def clean_text(text):
    """清理 HTML 标签和多余空白"""
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 移除 HTML 实体
    text = re.sub(r'&[a-z]+;', ' ', text)
    # 压缩空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def main():
    parser = argparse.ArgumentParser(description="从 PPT/HTML 文件提取章节信息")
    parser.add_argument("input", help="输入 HTML 文件路径")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径（默认输出到 stdout）")
    parser.add_argument("--format", "-f", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()
    
    chapters = extract_chapters_from_html(content)
    
    if args.format == "json":
        output = json.dumps(chapters, ensure_ascii=False, indent=2)
    else:
        lines = []
        for ch in chapters:
            lines.append(f"第{ch['number']}节: {ch['title']}")
        output = "\n".join(lines)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 提取了 {len(chapters)} 个章节 → {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
