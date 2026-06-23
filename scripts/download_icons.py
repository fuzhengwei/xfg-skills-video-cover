#!/usr/bin/env python3
"""
iconfont 图标下载器
从 iconfont.cn 搜索关键词并批量下载 SVG 图标到 skills 目录

用法:
  python3 download_icons.py --query 小狗 --category animal --count 20
  python3 download_icons.py --query 程序员 --category coder --count 15
  python3 download_icons.py --query AI --category tech --count 10
"""

import os
import sys
import json
import re
import time
import argparse
import urllib.request
import urllib.parse

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONFONT_DIR = os.path.join(SKILL_DIR, "assets", "iconfont")
INDEX_FILE = os.path.join(ICONFONT_DIR, "_index.json")

SEARCH_URL = "https://www.iconfont.cn/api/icon/search.json"
DETAIL_URL = "https://www.iconfont.cn/api/icon/getIcon.json"
SVG_URL = "https://www.iconfont.cn/api/icon/getIcon.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": "https://www.iconfont.cn/search/index",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.iconfont.cn",
}


def search_icons(query, page=1, page_size=50):
    """搜索 iconfont 图标"""
    data = urllib.parse.urlencode({
        "q": query,
        "sortType": "update",
        "pageSize": str(page_size),
        "page": str(page),
    }).encode("utf-8")
    
    req = urllib.request.Request(SEARCH_URL, data=data, headers=HEADERS, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("code") == 200:
                return result.get("data", {}).get("icons", [])
            else:
                print(f"  ⚠️ 搜索失败: {result.get('message', 'unknown')}")
                return []
    except Exception as e:
        print(f"  ⚠️ 搜索出错: {e}")
        return []


def download_svg(icon_id, name, save_dir):
    """下载单个 SVG 图标"""
    # 从搜索结果中已有 show_svg 字段，直接用
    # 如果没有，尝试通过 API 获取
    url = f"https://www.iconfont.cn/api/icon/getIcon.json?id={icon_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            svg = result.get("data", {}).get("show_svg", "")
            if not svg:
                return False
    except:
        return False
    
    # 清理文件名
    safe_name = re.sub(r'[\\/:*?"<>|]', '_', name)
    filename = f"{safe_name}_{icon_id}.svg"
    filepath = os.path.join(save_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    
    return filename


def update_index(category, icons):
    """更新 _index.json 索引文件"""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = {}
    
    if category not in index:
        index[category] = []
    
    # 去重：已存在的 id 不重复添加
    existing_ids = {item.get("id") for item in index[category]}
    
    for icon in icons:
        if icon["id"] not in existing_ids:
            index[category].append({
                "name": icon["name"],
                "file": f"iconfont/{category}/{icon['filename']}",
                "keyword": icon["keyword"],
                "id": icon["id"],
            })
    
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    return len(index[category])


def main():
    parser = argparse.ArgumentParser(description="从 iconfont.cn 下载 SVG 图标到 skills 目录")
    parser.add_argument("--query", "-q", required=True, help="搜索关键词，如：小狗、程序员、AI")
    parser.add_argument("--category", "-c", required=True, 
                        help="分类目录名，如：animal/coder/tech/emoji/food 或自定义新分类")
    parser.add_argument("--count", "-n", type=int, default=20, help="下载数量（默认20）")
    parser.add_argument("--list-only", "-l", action="store_true", help="只搜索预览，不下载")
    args = parser.parse_args()
    
    save_dir = os.path.join(ICONFONT_DIR, args.category)
    
    print(f"🔍 搜索 iconfont: \"{args.query}\" ...")
    
    all_icons = []
    page = 1
    while len(all_icons) < args.count:
        icons = search_icons(args.query, page=page, page_size=50)
        if not icons:
            break
        all_icons.extend(icons)
        page += 1
        time.sleep(0.5)  # 礼貌延迟
    
    all_icons = all_icons[:args.count]
    
    if not all_icons:
        print("❌ 未找到图标")
        return
    
    print(f"✅ 找到 {len(all_icons)} 个图标\n")
    
    if args.list_only:
        for i, icon in enumerate(all_icons, 1):
            print(f"  {i:2d}. {icon['name']:12s}  ID:{icon['id']}  "
                  f"尺寸:{icon.get('width','?')}x{icon.get('height','?')}")
        return
    
    # 创建目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 下载 SVG
    print(f"📥 下载到: {save_dir}\n")
    downloaded = []
    for i, icon in enumerate(all_icons, 1):
        # 优先使用搜索结果中的 show_svg
        svg_content = icon.get("show_svg", "")
        if svg_content:
            safe_name = re.sub(r'[\\/:*?"<>|]', '_', icon["name"])
            filename = f"{safe_name}_{icon['id']}.svg"
            filepath = os.path.join(save_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(svg_content)
            
            icon["filename"] = filename
            icon["keyword"] = args.query
            downloaded.append(icon)
            print(f"  [{i:2d}/{len(all_icons)}] ✅ {icon['name']} → {filename}")
        else:
            print(f"  [{i:2d}/{len(all_icons)}] ⚠️ {icon['name']} (无SVG数据，跳过)")
        
        time.sleep(0.1)
    
    # 更新索引
    total = update_index(args.category, downloaded)
    print(f"\n📊 分类 \"{args.category}\" 共 {total} 个图标")
    print(f"📁 索引文件: {INDEX_FILE}")


if __name__ == "__main__":
    main()
