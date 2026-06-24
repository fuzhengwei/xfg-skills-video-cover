#!/usr/bin/env python3
"""
爆款标题生成器 v1.0
自动为视频内容生成多风格爆款标题

用法：
  python3 title_generator.py --title "原始标题" --tags "Redis,缓存" [--count 5] [--style all]

风格：
  shock: 震惊体 | benefit: 利益体 | curiosity: 悬念体 | number: 数字体
  contrast: 对比体 | pain: 痛点体 | exclusive: 独家体 | challenge: 挑战体
"""
import argparse, json, random, re, sys, os

# ========== 爆款标题模板库 ==========
TEMPLATES = {
    "shock": [
        "震惊！{topic}竟然{result}",
        "万万没想到！{topic}可以{result}",
        "离谱！{topic}居然能{result}",
        "绝了！{topic}原来要这样{action}",
        "{topic}的真相，90%的人都不知道！",
        "太炸了！{topic}竟然{result}！",
    ],
    "benefit": [
        "学会{topic}，从此{benefit}",
        "掌握{topic}，{benefit}不是梦",
        "{topic}完整教程，{benefit}一学就会",
        "一篇文章搞懂{topic}，{benefit}",
        "从零到一学{topic}，{benefit}！",
        "{topic}实战指南，{benefit}！",
    ],
    "curiosity": [
        "{topic}的{count}个秘密，第{pick}个绝了",
        "为什么{topic}能{result}？答案出乎意料",
        "{topic}背后不为人知的{count}个细节",
        "深入{topic}，发现了惊人的{thing}",
        "{topic}到底怎么{action}？看完你就懂了",
        "揭秘{topic}，{count}个你必须知道的事",
    ],
    "number": [
        "{count}分钟搞懂{topic}",
        "{count}个{topic}技巧，{benefit}",
        "只需{count}步，搞定{topic}",
        "{topic}必知的{count}件事",
        "{count}天从入门到精通{topic}",
        "{topic}最强{count}连！",
    ],
    "contrast": [
        "{topic_a} vs {topic_b}，差距竟然这么大",
        "用{topic_a}之前 vs 之后，天壤之别",
        "{topic_a}和{topic_b}，我选了{pick}",
        "放弃{topic_a}改用{topic_b}，结果…",
        "{topic_a} vs {topic_b}，谁是最终赢家？",
        "对比{count}种{topic}方案，最优解是…",
    ],
    "pain": [
        "还在{pain_action}？试试这个方法",
        "{pain_action}太痛苦？{topic}一键搞定",
        "别再{pain_action}了！{topic}才是正确姿势",
        "受够了{pain_action}？{topic}让你解放双手",
        "告别{pain_action}，{topic}让一切变简单",
        "{pain_action}的坑我都踩过了，看这篇就够了",
    ],
    "exclusive": [
        "全网首发！{topic}完整方案",
        "独家！{topic}最全攻略",
        "第一次公开！{topic}核心方法论",
        "内部资料！{topic}实战手册",
        "终于有人把{topic}讲清楚了",
        "收藏！{topic}最全指南",
    ],
    "challenge": [
        "用{topic}挑战{challenge_goal}，结果…",
        "{topic}能{challenge_goal}吗？试了一下",
        "挑战用{topic}完成{challenge_goal}",
        "一天学会{topic}，能做出什么？",
        "新手用{topic}，{challenge_goal}竟然…",
        "零基础{topic}挑战，{count}天搞定",
    ],
}

KEYWORD_MAP = {
    "Redis": ("手动查数据库", "缓存提速10倍"),
    "MySQL": ("SQL写到手软", "查询性能翻倍"),
    "Docker": ("环境配一天", "一键部署全搞定"),
    "Spring": ("配置文件写不完", "自动装配省大事"),
    "AI": ("手动做重复工作", "效率提升100倍"),
    "编程": ("加班改Bug", "优雅写出高质量代码"),
    "面试": ("背八股文背到吐", "轻松拿下Offer"),
    "架构": ("系统越做越乱", "清晰架构一目了然"),
    "Python": ("重复劳动太多", "自动化解放双手"),
    "Java": ("代码又臭又长", "优雅设计模式搞定"),
    "Agent": ("手动操作效率低", "AI自动完成"),
    "缓存": ("数据库扛不住", "性能飞跃提升"),
    "部署": ("手动上线出错", "自动化一键搞定"),
    "算法": ("LeetCode刷不完", "套路搞定面试"),
    "源码": ("看不懂框架", "核心原理一通百通"),
    "微服务": ("单体拆不动", "清晰拆分方案"),
    "设计模式": ("代码一团乱麻", "优雅重构"),
    "OpenClaw": ("重复操作太多", "效率飙升"),
    "Git": ("版本管理混乱", "代码历史清晰明了"),
    "Linux": ("命令记不住", "一行搞定系统管理"),
    "Nginx": ("配置看不懂", "高性能部署一学就会"),
    "K8s": ("容器管理头疼", "编排调度自动化"),
    "React": ("页面写半天", "组件化开发飞快"),
    "Vue": ("前端太复杂", "渐进式框架上手快"),
    "数据库": ("查询慢如龟", "SQL优化飞速"),
    "前端": ("样式调一天", "像素级还原"),
    "后端": ("接口联调崩溃", "RESTful优雅设计"),
}

STYLE_KW = {
    "shock": ["揭秘", "真相", "震惊", "绝了", "离谱", "炸了"],
    "benefit": ["学会", "掌握", "搞定", "教程", "指南", "入门"],
    "curiosity": ["秘密", "背后", "为什么", "真相", "不为人知"],
    "number": ["分钟", "步", "个", "天", "连", "种"],
    "contrast": ["vs", "对比", "比较", "区别", "选择"],
    "pain": ["还在", "太痛苦", "别再", "受够", "告别"],
    "exclusive": ["首发", "独家", "公开", "内部", "最全"],
    "challenge": ["挑战", "试了", "能吗", "竟然", "零基础"],
}


def extract_topic(title, tags=None):
    if tags:
        for tag in tags[:3]:
            if 2 <= len(tag) <= 8:
                return tag
    clean = re.sub(r'^[【\[（(]|[\]\)）]$', '', title)
    clean = re.sub(r'^(学会|掌握|搞懂|了解|理解|从零|零基础|入门)', '', clean)
    return clean[:8] if len(clean) >= 4 else title[:8]


def optimize_title(title, max_len=30):
    title = re.sub(r'！{2,}', '！', title)
    title = re.sub(r'!{2,}', '!', title)
    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) > max_len:
        title = title[:max_len - 1] + '…'
    return title


def generate_titles(title, tags=None, count=3, style="all"):
    topic = extract_topic(title, tags)
    pain, benefit = KEYWORD_MAP.get(topic, ("手动操作太累", "效率大幅提升"))
    variables = {
        "topic": topic, "result": benefit, "benefit": benefit,
        "action": "这样用", "count": str(random.choice([3, 5, 7, 10])),
        "pick": str(random.choice([2, 3])), "thing": "真相",
        "topic_a": topic, "topic_b": "传统方案",
        "pain_action": pain, "challenge_goal": "极限挑战",
    }
    if tags and len(tags) >= 2:
        variables["topic_b"] = tags[1]
        variables["challenge_goal"] = tags[-1]

    styles = list(TEMPLATES.keys()) if style == "all" else [style]
    results = []
    for s in styles:
        tpls = TEMPLATES.get(s, [])
        selected = random.sample(tpls, min(count, len(tpls)))
        for tpl in selected:
            try:
                gen = tpl.format(**variables)
            except (KeyError, IndexError):
                gen = tpl.replace("{topic}", topic)
            gen = optimize_title(gen)
            score = 60
            if 20 <= len(gen) <= 28:
                score += 15
            if re.search(r'\d', gen):
                score += 10
            if gen.count('！') == 1 or gen.count('!') == 1:
                score += 5
            if s in ("shock", "curiosity", "contrast"):
                score += 5
            results.append({"style": s, "title": gen, "template": tpl, "score": min(score, 100)})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def suggest_style(title, tags=None):
    text = (title + " " + " ".join(tags or [])).lower()
    best, best_score = "benefit", 0
    for style, kws in STYLE_KW.items():
        score = sum(1 for kw in kws if kw in text)
        if score > best_score:
            best_score, best = score, style
    return best


def generate_cover_titles(title, tags=None, count_per_style=2):
    titles = generate_titles(title, tags, count=count_per_style, style="all")
    topic = extract_topic(title, tags)
    hl = [topic] if topic else []
    for t in titles[:3]:
        for n in re.findall(r'\d+', t["title"]):
            hl.append(n)
    return {
        "original": title,
        "suggested_style": suggest_style(title, tags),
        "titles": titles[:20],
        "highlight_words": hl[:3],
    }


def main():
    p = argparse.ArgumentParser(description="爆款标题生成器")
    p.add_argument("--title", "-t", required=True)
    p.add_argument("--tags", "-g", default="")
    p.add_argument("--count", "-n", type=int, default=3)
    p.add_argument("--style", "-s", default="all",
                   choices=["shock","benefit","curiosity","number","contrast","pain","exclusive","challenge","all"])
    p.add_argument("--json", "-j", action="store_true")
    a = p.parse_args()
    tags = [t.strip() for t in a.tags.split(",") if t.strip()] if a.tags else None
    results = generate_titles(a.title, tags, a.count, a.style)
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"\n🎯 原始标题: {a.title}")
        if tags:
            print(f"🏷️  标签: {', '.join(tags)}")
        print(f"💡 推荐风格: {suggest_style(a.title, tags)}")
        print(f"\n{'='*50}")
        cur = None
        names = {"shock":"😱 震惊体","benefit":"💰 利益体","curiosity":"🤔 悬念体",
                 "number":"🔢 数字体","contrast":"⚔️ 对比体","pain":"😣 痛点体",
                 "exclusive":"🔥 独家体","challenge":"🎮 挑战体"}
        for r in results:
            if r["style"] != cur:
                cur = r["style"]
                print(f"\n{names.get(cur, cur)}:")
            print(f"  [{r['score']}分] {r['title']}")
        print()

if __name__ == "__main__":
    main()
