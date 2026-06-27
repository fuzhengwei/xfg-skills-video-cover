#!/usr/bin/env python3
"""
主题选择器 v2.0 - 点击主题卡片直接跳转4平台详细预览
单文件输出，所有风格+所有平台全打包
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_covers import (
    PLATFORMS, COLOR_SCHEMES, THEME_EMOJIS, THEME_KEYWORDS,
    detect_theme, get_scheme_by_theme, get_emojis,
    apply_highlights, hex_to_rgb, TWEMOJI_CDN,
    THEME_FONT_CSS, generate_single_cover,
    get_decoration_assets,
)

THEME_INFO = {
    # ===== 科技知识类 =====
    "bold":    {"name": "大字醒目", "desc": "知识区/教程/干货", "icon": "📢", "best": "编程教程、知识科普、硬核干货", "category": "科技知识"},
    "cyber":   {"name": "赛博朋克", "desc": "数码/科技/AI", "icon": "🌃", "best": "AI、编程、科技、服务器", "category": "科技知识"},
    "minimal": {"name": "极简主义", "desc": "设计/商务/美学", "icon": "⬜", "best": "知识科普、商务、设计美学", "category": "科技知识"},
    "magazine":{"name": "杂志风", "desc": "商业/深度/报道", "icon": "📰", "best": "商业财经、深度报道、行业分析", "category": "科技知识"},
    "pixel":   {"name": "像素复古", "desc": "复古/游戏/极客", "icon": "👾", "best": "复古游戏、极客、街机怀旧", "category": "科技知识"},
    # ===== 生活娱乐类 =====
    "funny":   {"name": "搞笑整活", "desc": "搞笑/整活/表情包", "icon": "😂", "best": "搞笑、沙雕、吐槽、鬼畜", "category": "生活娱乐"},
    "food":    {"name": "美食暖调", "desc": "美食/探店/烹饪", "icon": "🍜", "best": "美食、探店、烹饪教程", "category": "生活娱乐"},
    "gaming":  {"name": "游戏电竞", "desc": "游戏/电竞/直播", "icon": "🎮", "best": "游戏、电竞、通关攻略", "category": "生活娱乐"},
    "variety": {"name": "综艺弹幕", "desc": "热点/吐槽/反应", "icon": "💬", "best": "热点、吃瓜、名场面、反应", "category": "生活娱乐"},
    "cute":    {"name": "萌宠可爱", "desc": "宠物/萌系/卡通", "icon": "🐱", "best": "宠物、萌系、卡通、手帐", "category": "生活娱乐"},
    # ===== 视觉冲击类 =====
    "paper":   {"name": "撕纸拼贴", "desc": "评测/攻略/安利", "icon": "✂️", "best": "安利推荐、攻略对比、排行盘点", "category": "视觉冲击"},
    "dopamine":{"name": "多巴胺撞色", "desc": "潮流/撞色/快乐", "icon": "🌈", "best": "潮流穿搭、夏日、元气活力", "category": "视觉冲击"},
    "doodle":  {"name": "手绘涂鸦", "desc": "文创/手绘/创意", "icon": "🖍️", "best": "文创、手绘、创意DIY", "category": "视觉冲击"},
    "luxury":  {"name": "黑金奢华", "desc": "评测/高端/开箱", "icon": "👑", "best": "数码评测、开箱、高端体验", "category": "视觉冲击"},
    # ===== 文艺清新类 =====
    "fresh":   {"name": "清新治愈", "desc": "Vlog/生活/旅行", "icon": "🍃", "best": "Vlog、旅行、生活记录", "category": "文艺清新"},
    "anime":   {"name": "二次元动漫", "desc": "ACG/番剧/虚拟主播", "icon": "🌸", "best": "动漫、番剧、虚拟主播", "category": "文艺清新"},
    "cinema":  {"name": "影视悬疑", "desc": "影视/悬疑/解说", "icon": "🎬", "best": "电影解说、悬疑、剧情", "category": "文艺清新"},
    "journal": {"name": "手账风", "desc": "笔记/记录/手写", "icon": "📓", "best": "手账、笔记、日记、打卡", "category": "文艺清新"},
    "guochao": {"name": "国潮风", "desc": "国风/传统/文化", "icon": "🏮", "best": "国风、汉服、传统文化、非遗", "category": "文艺清新"},
    # ===== 新增11种风格 =====
    "vaporwave": {"name": "蒸汽波", "desc": "复古/迷幻/80s", "icon": "👾", "best": "复古、迷幻、音乐、80s怀旧", "category": "视觉冲击"},
    "acid":      {"name": "酸性设计", "desc": "液态/荧光/前卫", "icon": "💥", "best": "前卫艺术、音乐、潮流、实验", "category": "视觉冲击"},
    "memphis":   {"name": "孟菲斯", "desc": "几何/波点/撞色", "icon": "🎨", "best": "活泼、卡通、教育、年轻化", "category": "视觉冲击"},
    "comic":     {"name": "漫画风", "desc": "描边/气泡/热血", "icon": "💬", "best": "漫画解说、热血、战斗、搞笑", "category": "视觉冲击"},
    "neon":      {"name": "霓虹灯", "desc": "暗夜/发光/荧光", "icon": "⚡", "best": "夜店、音乐、赛博、暗夜", "category": "视觉冲击"},
    "clay":      {"name": "黏土风", "desc": "3D/圆润/童趣", "icon": "👶", "best": "儿童、萌系、教程、可爱", "category": "生活娱乐"},
    "glass":     {"name": "玻璃拟态", "desc": "模糊/半透/质感", "icon": "🔹", "best": "科技、产品、高端、设计", "category": "科技知识"},
    "aurora":    {"name": "弥散光", "desc": "极光/光晕/梦幻", "icon": "🌌", "best": "梦幻、星空、科幻、宇宙", "category": "科技知识"},
    "sticker":   {"name": "贴纸风", "desc": "白边/手绘/可爱", "icon": "🎀", "best": "手绘、可爱、装饰、日记", "category": "文艺清新"},
    "retro":     {"name": "复古风", "desc": "胶片/做旧/怀旧", "icon": "📷", "best": "怀旧、老歌、胶片、回忆", "category": "文艺清新"},
    "collage":   {"name": "拼贴风", "desc": "剪报/胶带/混合", "icon": "📌", "best": "文艺、剪报、手做、混搭", "category": "文艺清新"},
    # ===== 新增20种风格 v6 =====
    "ink":         {"name": "水墨风", "desc": "国画/书法/写意", "icon": "🎨", "best": "书法、国画、东方美学、文化", "category": "文艺清新"},
    "stamp":       {"name": "印章风", "desc": "篆刻/朱印/传统", "icon": "📠", "best": "传统文化、篆刻、收藏、鉴定", "category": "文艺清新"},
    "newspaper":   {"name": "报纸风", "desc": "新闻/头条/社论", "icon": "📰", "best": "新闻、报道、评论、时事", "category": "文艺清新"},
    "polaroid":    {"name": "拍立得", "desc": "白边/相框/回忆", "icon": "📷", "best": "旅行、回忆、日常、Vlog", "category": "文艺清新"},
    "risograph":   {"name": "Riso印刷", "desc": "双色/颗粒/独立出版", "icon": "📄", "best": "独立出版、设计、艺术、Zine", "category": "文艺清新"},
    "film":        {"name": "胶片风", "desc": "胶卷/帧/放映", "icon": "🎞️", "best": "电影、摄影、胶片相机、怀旧", "category": "文艺清新"},
    "ribbon":      {"name": "缎带风", "desc": "丝带/横幅/颁奖", "icon": "🎀", "best": "颁奖、典礼、表彰、节日", "category": "文艺清新"},
    "pastel":      {"name": "莫兰迪", "desc": "低饱和/高级灰/柔和", "icon": "💛", "best": "家居、穿搭、高级感、内敛", "category": "文艺清新"},
    "kraft":       {"name": "牛皮纸", "desc": "纸袋/手工/质朴", "icon": "📄", "best": "手工、包装、质朴、原生态", "category": "文艺清新"},
    "washi":       {"name": "和纸胶带", "desc": "日式/纸胶带/装饰", "icon": "🎀", "best": "手帐、日式、拼贴、装饰", "category": "文艺清新"},
    "graffiti":    {"name": "涂鸦街头", "desc": "喷漆/街头/野生", "icon": "💥", "best": "街头文化、嘻哈、滑板、反叛", "category": "视觉冲击"},
    "gradientmesh": {"name": "网格渐变", "desc": "柔和/多色/梦幻", "icon": "🌈", "best": "梦幻、柔和、品牌、壁纸", "category": "视觉冲击"},
    "brutalist":   {"name": "粗野主义", "desc": "原始/混凝土/粗犷", "icon": "◼️", "best": "建筑、结构、极简粗野、设计", "category": "视觉冲击"},
    "popart":      {"name": "波普艺术", "desc": "撞色/网点/大众艺术", "icon": "🎨", "best": "波普、明星、消费、撞色", "category": "生活娱乐"},
    "holographic": {"name": "全息彩虹", "desc": "镭射/幻彩/偏光", "icon": "✨", "best": "潮流、镭射、炫彩、未来", "category": "视觉冲击"},
    "carnival":    {"name": "嘉年华", "desc": "马戏团/彩旗/狂欢", "icon": "🎪", "best": "庆典、派对、节日、游乐园", "category": "生活娱乐"},
    "blueprint":   {"name": "蓝图风", "desc": "工程图/制图/蓝底白线", "icon": "📐", "best": "建筑、工程、技术制图、设计", "category": "科技知识"},
    "starfield":   {"name": "星空宇宙", "desc": "深空/银河/星海", "icon": "🌌", "best": "天文、科幻、宇宙、探索", "category": "科技知识"},
    "typewriter":  {"name": "打字机", "desc": "等宽/手稿/复古", "icon": "⌨", "best": "手稿、文稿、复古、文字", "category": "科技知识"},
    "terrarium":   {"name": "玻璃生态", "desc": "植物/微景观/通透", "icon": "🌱", "best": "植物、自然、微景观、生态", "category": "文艺清新"},
    # ===== v7 新增5种「真实派」风格 — 点击率最高 =====
    "screenshot": {"name": "真实截图", "desc": "PPT/代码/演示", "icon": "💻", "best": "教程、源码、实操、案例", "category": "视觉冲击"},
    "portrait":   {"name": "真人出镜", "desc": "经验/职业/分享", "icon": "👤", "best": "经验、职业、面试、转型分享", "category": "视觉冲击"},
    "product":    {"name": "实物产品", "desc": "测评/开箱/工具", "icon": "📱", "best": "开箱、测评、工具、硬件", "category": "视觉冲击"},
    "contrast":   {"name": "对比冲击", "desc": "对比/vs/盘点", "icon": "🆚", "best": "对比、区别、选择、TOP排行", "category": "视觉冲击"},
    "zoom":       {"name": "局部放大", "desc": "细节/重点/特写", "icon": "🔍", "best": "细节、重点、特写、深入", "category": "视觉冲击"},

    "glitch": {"name": "故障风", "icon": "📺", "category": "科技知识"},
    "synthwave": {"name": "合成波", "icon": "🌅", "category": "科技知识"},
    "matrix": {"name": "矩阵代码", "icon": "🔢", "category": "科技知识"},
    "quantum": {"name": "量子科技", "icon": "⚛️", "category": "科技知识"},
    "ocean": {"name": "深海蓝调", "icon": "🌊", "category": "科技知识"},
    "ice": {"name": "冰晶透蓝", "icon": "❄", "category": "科技知识"},
    "glassmorph": {"name": "毛玻璃质感", "icon": "🪟", "category": "科技知识"},
    "retrofuturism": {"name": "复古未来", "icon": "🚀", "category": "科技知识"},
    "galaxy": {"name": "银河星系", "icon": "🌌", "category": "科技知识"},
    "candy": {"name": "糖果甜蜜", "icon": "🍬", "category": "生活娱乐"},
    "steampunk": {"name": "蒸汽朋克", "icon": "⚙️", "category": "视觉冲击"},
    "noir": {"name": "黑色电影", "icon": "🎬", "category": "视觉冲击"},
    "gothic": {"name": "哥特暗黑", "icon": "🦇", "category": "视觉冲击"},
    "baroque": {"name": "巴洛克华丽", "icon": "👑", "category": "视觉冲击"},
    "tribal": {"name": "部落图腾", "icon": "🗿", "category": "视觉冲击"},
    "artdeco": {"name": "装饰艺术", "icon": "💎", "category": "视觉冲击"},
    "fire": {"name": "烈焰燃烧", "icon": "🔥", "category": "视觉冲击"},
    "streetwear": {"name": "街头潮牌", "icon": "🛹", "category": "视觉冲击"},
    "psychadelic": {"name": "迷幻色彩", "icon": "🌀", "category": "视觉冲击"},
    "mosaic": {"name": "马赛克拼图", "icon": "🧩", "category": "视觉冲击"},
    "newspaper2": {"name": "头版头条", "icon": "📰", "category": "视觉冲击"},
    "techwear": {"name": "机能工装", "icon": "🦺", "category": "视觉冲击"},
    "cyberpunk2": {"name": "赛博废土", "icon": "🏚", "category": "视觉冲击"},
    "neoncity": {"name": "霓虹都市", "icon": "🌃", "category": "视觉冲击"},
    "medieval": {"name": "中世纪", "icon": "⚔", "category": "视觉冲击"},
    "watercolor": {"name": "水彩晕染", "icon": "🎨", "category": "文艺清新"},
    "zen": {"name": "禅意侘寂", "icon": "🪨", "category": "文艺清新"},
    "scandinavian": {"name": "北欧极简", "icon": "🌲", "category": "文艺清新"},
    "boho": {"name": "波西米亚", "icon": "🌻", "category": "文艺清新"},
    "rain": {"name": "雨天氛围", "icon": "🌧", "category": "文艺清新"},
    "sunset": {"name": "日落黄昏", "icon": "🌇", "category": "文艺清新"},
    "forest": {"name": "森林秘境", "icon": "🌲", "category": "文艺清新"},
    "desert": {"name": "沙漠暖阳", "icon": "🏜", "category": "文艺清新"},
    "vintage": {"name": "复古怀旧", "icon": "📻", "category": "文艺清新"},
    "cherry": {"name": "樱花粉嫩", "icon": "🌸", "category": "文艺清新"},
    "woodcut": {"name": "版画木刻", "icon": "🪵", "category": "文艺清新"},
    "plaid": {"name": "格纹学院", "icon": "🏫", "category": "文艺清新"},
    "origami": {"name": "折纸手工", "icon": "🦢", "category": "文艺清新"},
    "paperplane": {"name": "纸飞机", "icon": "✈", "category": "文艺清新"},
    "lofi": {"name": "Lo-Fi慵懒", "icon": "🎧", "category": "文艺清新"},
    "wave": {"name": "海浪波纹", "icon": "🌊", "category": "文艺清新"},
    "fairy": {"name": "童话梦幻", "icon": "🧚", "category": "文艺清新"},
    "military": {"name": "军事硬核", "icon": "🎖", "category": "视觉冲击"},
    "cloud": {"name": "云端轻盈", "icon": "☁️", "category": "科技知识"},
    "earth": {"name": "地球生态", "icon": "🌍", "category": "文艺清新"},

    "tech": {"name":"tech","desc":"AI","icon":"✨","best":"AI、Shell、API","category":"视觉冲击"},
    "hot": {"name":"hot","desc":"教程","icon":"✨","best":"教程、入门、实战","category":"视觉冲击"},
    "cool": {"name":"cool","desc":"Docker","icon":"✨","best":"Docker、容器、MySQL","category":"视觉冲击"},
    "warm": {"name":"warm","desc":"对话","icon":"✨","best":"对话、客服、设计","category":"视觉冲击"},
    "dark": {"name":"dark","desc":"安全","icon":"✨","best":"安全、黑客、高级","category":"视觉冲击"},
    "gradient": {"name":"gradient","desc":"时尚","icon":"✨","best":"时尚、创意、爆款","category":"视觉冲击"},
    "animal": {"name":"animal","desc":"萌","icon":"✨","best":"萌、可爱、治愈","category":"视觉冲击"},
    "python": {"name":"python","desc":"Python","icon":"🐍","best":"Python、Django、Flask","category":"科技知识"},
    "java": {"name":"java","desc":"Java","icon":"☕","best":"Java、JVM、Spring","category":"科技知识"},
    "golang": {"name":"golang","desc":"Go","icon":"🐹","best":"Go、Golang、goroutine","category":"科技知识"},
    "rust": {"name":"rust","desc":"Rust","icon":"🦀","best":"Rust、Cargo","category":"科技知识"},
    "typescript": {"name":"typescript","desc":"TypeScript","icon":"🔷","best":"TypeScript、TS","category":"科技知识"},
    "react": {"name":"react","desc":"React","icon":"⚛️","best":"React、JSX、hook","category":"科技知识"},
    "vue": {"name":"vue","desc":"Vue","icon":"🌿","best":"Vue、Vuex","category":"科技知识"},
    "angular": {"name":"angular","desc":"Angular","icon":"🛡️","best":"Angular、RxJS","category":"科技知识"},
    "svelte": {"name":"svelte","desc":"Svelte","icon":"🔥","best":"Svelte、编译","category":"科技知识"},
    "nodejs": {"name":"nodejs","desc":"Node","icon":"⬡","best":"Node、npm、Express","category":"科技知识"},
    "mysql": {"name":"mysql","desc":"MySQL","icon":"🐬","best":"MySQL、SQL、数据库","category":"科技知识"},
    "postgres": {"name":"postgres","desc":"PostgreSQL","icon":"🐘","best":"PostgreSQL、pg","category":"科技知识"},
    "redis": {"name":"redis","desc":"Redis","icon":"🟥","best":"Redis、缓存","category":"科技知识"},
    "mongo": {"name":"mongo","desc":"MongoDB","icon":"🍃","best":"MongoDB、NoSQL","category":"科技知识"},
    "sqlite": {"name":"sqlite","desc":"SQLite","icon":"🪶","best":"SQLite、轻量","category":"科技知识"},
    "elastic": {"name":"elastic","desc":"Elasticsearch","icon":"🔍","best":"Elasticsearch、ES","category":"科技知识"},
    "docker": {"name":"docker","desc":"Docker","icon":"🐳","best":"Docker、容器","category":"科技知识"},
    "k8s": {"name":"k8s","desc":"K8s","icon":"⚓","best":"K8s、Kubernetes","category":"科技知识"},
    "terraform": {"name":"terraform","desc":"Terraform","icon":"🌍","best":"Terraform、IaC","category":"科技知识"},
    "jenkins": {"name":"jenkins","desc":"Jenkins","icon":"🔧","best":"Jenkins、CI、CD","category":"科技知识"},
    "github": {"name":"github","desc":"GitHub","icon":"🐙","best":"GitHub、Git","category":"科技知识"},
    "gitlab": {"name":"gitlab","desc":"GitLab","icon":"🦊","best":"GitLab","category":"科技知识"},
    "prometheus": {"name":"prometheus","desc":"Prometheus","icon":"🔥","best":"Prometheus、监控","category":"科技知识"},
    "grafana": {"name":"grafana","desc":"Grafana","icon":"📊","best":"Grafana、可视化","category":"科技知识"},
    "tensorflow": {"name":"tensorflow","desc":"TensorFlow","icon":"🌊","best":"TensorFlow、TF","category":"科技知识"},
    "pytorch": {"name":"pytorch","desc":"PyTorch","icon":"🔥","best":"PyTorch、张量","category":"科技知识"},
    "huggingface": {"name":"huggingface","desc":"HuggingFace","icon":"🤗","best":"HuggingFace、Transformers","category":"科技知识"},
    "openai": {"name":"openai","desc":"OpenAI","icon":"🧠","best":"OpenAI、GPT","category":"科技知识"},
    "langchain": {"name":"langchain","desc":"LangChain","icon":"🔗","best":"LangChain、LLM","category":"科技知识"},
    "ollama": {"name":"ollama","desc":"Ollama","icon":"🦙","best":"Ollama、LLM","category":"科技知识"},
    "stable": {"name":"stable","desc":"Stable","icon":"🎨","best":"Stable、Diffusion","category":"科技知识"},
    "agent": {"name":"agent","desc":"Agent","icon":"🤖","best":"Agent、智能体","category":"科技知识"},
    "rag": {"name":"rag","desc":"RAG","icon":"📚","best":"RAG、检索增强","category":"科技知识"},
    "webpack": {"name":"webpack","desc":"Webpack","icon":"📦","best":"Webpack、打包","category":"科技知识"},
    "vite": {"name":"vite","desc":"Vite","icon":"⚡","best":"Vite、ESM","category":"科技知识"},
    "tailwind": {"name":"tailwind","desc":"Tailwind","icon":"💨","best":"Tailwind、CSS","category":"科技知识"},
    "figma": {"name":"figma","desc":"Figma","icon":"🎨","best":"Figma、设计","category":"科技知识"},
    "graphql": {"name":"graphql","desc":"GraphQL","icon":"◈","best":"GraphQL、查询","category":"科技知识"},
    "grpc": {"name":"grpc","desc":"gRPC","icon":"🔌","best":"gRPC、protobuf","category":"科技知识"},
    "kafka": {"name":"kafka","desc":"Kafka","icon":"📨","best":"Kafka、消息队列","category":"科技知识"},
    "rabbit": {"name":"rabbit","desc":"兔","icon":"🐰","best":"兔、rabbit","category":"生活娱乐"},
    "nginx": {"name":"nginx","desc":"Nginx","icon":"🌐","best":"Nginx、代理","category":"科技知识"},
    "spring": {"name":"spring","desc":"春","icon":"🌸","best":"春、spring","category":"文艺清新"},
    "ddd": {"name":"ddd","desc":"DDD","icon":"🏛️","best":"DDD、领域驱动、分层","category":"科技知识"},
    "microsvc": {"name":"microsvc","desc":"微服务","icon":"🔬","best":"微服务、microservice","category":"科技知识"},
    "serverless": {"name":"serverless","desc":"Serverless","icon":"☁️","best":"Serverless、Lambda","category":"科技知识"},
    "security": {"name":"security","desc":"安全","icon":"🔐","best":"安全、加密、渗透","category":"科技知识"},
    "blockchain": {"name":"blockchain","desc":"区块链","icon":"⛓️","best":"区块链、blockchain","category":"科技知识"},
    "web3": {"name":"web3","desc":"Web3","icon":"🌐","best":"Web3、DApp","category":"科技知识"},
    "linux": {"name":"linux","desc":"Linux","icon":"🐧","best":"Linux、Shell","category":"科技知识"},
    "terminal": {"name":"terminal","desc":"终端","icon":"⌨️","best":"终端、Terminal、CLI","category":"科技知识"},
    "vim": {"name":"vim","desc":"Vim","icon":"📝","best":"Vim、Neovim","category":"科技知识"},
    "vscode": {"name":"vscode","desc":"VSCode","icon":"💙","best":"VSCode、IDE","category":"科技知识"},
    "ssh": {"name":"ssh","desc":"SSH","icon":"🔑","best":"SSH、远程","category":"科技知识"},
    "cron": {"name":"cron","desc":"cron","icon":"⏰","best":"cron、定时","category":"科技知识"},
    "regex": {"name":"regex","desc":"正则","icon":"🔎","best":"正则、regex","category":"科技知识"},
    "restapi": {"name":"restapi","desc":"REST","icon":"🔗","best":"REST、API、接口","category":"科技知识"},
    "json2": {"name":"json2","desc":"JSON","icon":"{}","best":"JSON、序列化","category":"科技知识"},
    "yaml": {"name":"yaml","desc":"YAML","icon":"📋","best":"YAML、配置","category":"科技知识"},
    "cicd": {"name":"cicd","desc":"CI","icon":"🔄","best":"CI、CD、流水线","category":"科技知识"},
    "dataviz": {"name":"dataviz","desc":"可视化","icon":"📈","best":"可视化、图表","category":"科技知识"},
    "algo": {"name":"algo","desc":"算法","icon":"🧮","best":"算法、排序、搜索","category":"科技知识"},
    "binary": {"name":"binary","desc":"二进制","icon":"01","best":"二进制、binary","category":"科技知识"},
    "neural": {"name":"neural","desc":"神经网络","icon":"🧠","best":"神经网络、neural","category":"科技知识"},
    "quantum2": {"name":"quantum2","desc":"量子","icon":"⚛️","best":"量子、qubit","category":"科技知识"},
    "edge": {"name":"edge","desc":"边缘","icon":"📡","best":"边缘、edge","category":"科技知识"},
    "mesh2": {"name":"mesh2","desc":"mesh","icon":"🕸️","best":"mesh、Istio","category":"科技知识"},
    "observ": {"name":"observ","desc":"可观测","icon":"👁️","best":"可观测、监控","category":"科技知识"},
    "chaos": {"name":"chaos","desc":"混沌","icon":"🌪️","best":"混沌、chaos","category":"科技知识"},
    "gitops": {"name":"gitops","desc":"GitOps","icon":"🔄","best":"GitOps、ArgoCD","category":"科技知识"},
    "saas": {"name":"saas","desc":"SaaS","icon":"☁️","best":"SaaS、订阅","category":"科技知识"},
    "paas": {"name":"paas","desc":"PaaS","icon":"🏗️","best":"PaaS、平台","category":"科技知识"},
    "lowcode": {"name":"lowcode","desc":"低代码","icon":"🧩","best":"低代码、lowcode","category":"科技知识"},
    "vibe": {"name":"vibe","desc":"Vibe","icon":"🎵","best":"Vibe、Coding","category":"科技知识"},
    "prompt": {"name":"prompt","desc":"提示词","icon":"💬","best":"提示词、prompt","category":"科技知识"},
    "copilot": {"name":"copilot","desc":"Copilot","icon":"✈️","best":"Copilot、AI助手","category":"科技知识"},
    "embedding": {"name":"embedding","desc":"embedding","icon":"📐","best":"embedding、向量","category":"科技知识"},
    "cubism": {"name":"cubism","desc":"立体","icon":"🔺","best":"立体、cubism","category":"视觉冲击"},
    "surreal": {"name":"surreal","desc":"超现实","icon":"🌀","best":"超现实、surreal","category":"视觉冲击"},
    "impression": {"name":"impression","desc":"印象","icon":"🎨","best":"印象、impression","category":"视觉冲击"},
    "expression": {"name":"expression","desc":"表现","icon":"😨","best":"表现、expression","category":"视觉冲击"},
    "fauvism": {"name":"fauvism","desc":"野兽","icon":"🦁","best":"野兽、fauvism","category":"视觉冲击"},
    "dada": {"name":"dada","desc":"达达","icon":"🎲","best":"达达、dada","category":"视觉冲击"},
    "construct": {"name":"construct","desc":"构成","icon":"⬛","best":"构成、construct","category":"视觉冲击"},
    "destijl": {"name":"destijl","desc":"风格派","icon":"⬜","best":"风格派、DeStijl","category":"视觉冲击"},
    "bauhaus": {"name":"bauhaus","desc":"包豪斯","icon":"📐","best":"包豪斯、bauhaus","category":"视觉冲击"},
    "artnouveau": {"name":"artnouveau","desc":"新艺术","icon":"🌸","best":"新艺术、ArtNouveau","category":"视觉冲击"},
    "macro": {"name":"macro","desc":"微距","icon":"🔬","best":"微距、macro","category":"视觉冲击"},
    "longexp": {"name":"longexp","desc":"长曝光","icon":"⏳","best":"长曝光、慢门","category":"视觉冲击"},
    "tiltshift": {"name":"tiltshift","desc":"移轴","icon":"🎰","best":"移轴、tilt","category":"视觉冲击"},
    "doubleexp": {"name":"doubleexp","desc":"双重曝光","icon":"👻","best":"双重曝光","category":"视觉冲击"},
    "infrared": {"name":"infrared","desc":"红外","icon":"🔴","best":"红外、infrared","category":"视觉冲击"},
    "cyberfilm": {"name":"cyberfilm","desc":"赛博","icon":"🎬","best":"赛博、电影","category":"视觉冲击"},
    "wuxia": {"name":"wuxia","desc":"武侠","icon":"⚔️","best":"武侠、江湖","category":"视觉冲击"},
    "scifi": {"name":"scifi","desc":"科幻","icon":"🚀","best":"科幻、sci-fi","category":"视觉冲击"},
    "horror": {"name":"horror","desc":"恐怖","icon":"💀","best":"恐怖、horror","category":"视觉冲击"},
    "western": {"name":"western","desc":"西部","icon":"🤠","best":"西部、western","category":"视觉冲击"},
    "spy": {"name":"spy","desc":"谍战","icon":"🕵️","best":"谍战、间谍","category":"视觉冲击"},
    "rock": {"name":"rock","desc":"摇滚","icon":"🤘","best":"摇滚、rock","category":"视觉冲击"},
    "hiphop": {"name":"hiphop","desc":"嘻哈","icon":"🎤","best":"嘻哈、hiphop","category":"视觉冲击"},
    "jazz": {"name":"jazz","desc":"爵士","icon":"🎷","best":"爵士、jazz","category":"视觉冲击"},
    "edm": {"name":"edm","desc":"电音","icon":"🎧","best":"电音、EDM","category":"视觉冲击"},
    "punk": {"name":"punk","desc":"朋克","icon":"🦷","best":"朋克、punk","category":"视觉冲击"},
    "metal": {"name":"metal","desc":"金属","icon":"🤘","best":"金属、metal","category":"视觉冲击"},
    "blues": {"name":"blues","desc":"蓝调","icon":"🎸","best":"蓝调、blues","category":"视觉冲击"},
    "reggae": {"name":"reggae","desc":"雷鬼","icon":"🇯🇲","best":"雷鬼、reggae","category":"视觉冲击"},
    "deco": {"name":"deco","desc":"装饰","icon":"🏙️","best":"装饰、ArtDeco","category":"视觉冲击"},
    "brutal2": {"name":"brutal2","desc":"粗野","icon":"🏢","best":"粗野、混凝土","category":"视觉冲击"},
    "gothic2": {"name":"gothic2","desc":"哥特","icon":"⛪","best":"哥特、尖拱","category":"视觉冲击"},
    "modernist": {"name":"modernist","desc":"现代","icon":"🏛️","best":"现代、modernist","category":"视觉冲击"},
    "parametric": {"name":"parametric","desc":"参数","icon":"〰️","best":"参数、parametric","category":"视觉冲击"},
    "glam": {"name":"glam","desc":"华丽","icon":"✨","best":"华丽、glam","category":"视觉冲击"},
    "grunge": {"name":"grunge","desc":"grunge","icon":"🗑️","best":"grunge、垃圾","category":"视觉冲击"},
    "preppy": {"name":"preppy","desc":"学院","icon":"🎓","best":"学院、preppy","category":"视觉冲击"},
    "maximal": {"name":"maximal","desc":"极繁","icon":"🎊","best":"极繁、maximal","category":"视觉冲击"},
    "skate": {"name":"skate","desc":"滑板","icon":"🛹","best":"滑板、skate","category":"视觉冲击"},
    "surf": {"name":"surf","desc":"冲浪","icon":"🏄","best":"冲浪、surf","category":"视觉冲击"},
    "bike": {"name":"bike","desc":"骑行","icon":"🚴","best":"骑行、bike","category":"视觉冲击"},
    "tattoo": {"name":"tattoo","desc":"纹身","icon":"🐉","best":"纹身、tattoo","category":"视觉冲击"},
    "fifties": {"name":"fifties","desc":"50年代","icon":"📻","best":"50年代、复古","category":"视觉冲击"},
    "sixties": {"name":"sixties","desc":"60年代","icon":"☮️","best":"60年代、嬉皮","category":"视觉冲击"},
    "seventies": {"name":"seventies","desc":"70年代","icon":"🪩","best":"70年代、迪斯科","category":"视觉冲击"},
    "eighties": {"name":"eighties","desc":"80年代","icon":"📺","best":"80年代、霓虹","category":"视觉冲击"},
    "nineties": {"name":"nineties","desc":"90年代","icon":"🎮","best":"90年代、街机","category":"视觉冲击"},
    "y2k2": {"name":"y2k2","desc":"Y2K","icon":"💿","best":"Y2K、千禧","category":"视觉冲击"},
    "solarpunk": {"name":"solarpunk","desc":"太阳","icon":"☀️","best":"太阳、solar","category":"视觉冲击"},
    "biopunk": {"name":"biopunk","desc":"生物","icon":"🧬","best":"生物、bio","category":"视觉冲击"},
    "nanopunk": {"name":"nanopunk","desc":"纳米","icon":"🔬","best":"纳米、nano","category":"视觉冲击"},
    "posthuman": {"name":"posthuman","desc":"后人类","icon":"🦿","best":"后人类、义体","category":"视觉冲击"},
    "glitch2": {"name":"glitch2","desc":"故障","icon":"📺","best":"故障、glitch","category":"视觉冲击"},
    "datamosh": {"name":"datamosh","desc":"datamosh","icon":"🗜️","best":"datamosh","category":"视觉冲击"},
    "ascii": {"name":"ascii","desc":"ASCII","icon":"█","best":"ASCII、字符","category":"视觉冲击"},
    "generative": {"name":"generative","desc":"生成","icon":"🌸","best":"生成、generative","category":"视觉冲击"},
    "fractal": {"name":"fractal","desc":"分形","icon":"❄️","best":"分形、fractal","category":"视觉冲击"},
    "voronoi": {"name":"voronoi","desc":"voronoi","icon":"🔷","best":"voronoi","category":"视觉冲击"},
    "particles": {"name":"particles","desc":"粒子","icon":"✨","best":"粒子、particle","category":"视觉冲击"},
    "fluid": {"name":"fluid","desc":"流体","icon":"🌊","best":"流体、fluid","category":"视觉冲击"},
    "abstract": {"name":"abstract","desc":"抽象","icon":"🔸","best":"抽象、abstract","category":"视觉冲击"},
    "geometric": {"name":"geometric","desc":"几何","icon":"🔺","best":"几何、geometric","category":"视觉冲击"},
    "opart": {"name":"opart","desc":"视错觉","icon":"👁️","best":"视错觉、OpArt","category":"视觉冲击"},
    "kinetic": {"name":"kinetic","desc":"动态","icon":"🌀","best":"动态、kinetic","category":"视觉冲击"},
    "colorfield": {"name":"colorfield","desc":"色域","icon":"🟦","best":"色域、color","category":"视觉冲击"},
    "monochrome": {"name":"monochrome","desc":"单色","icon":"⚫","best":"单色、monochrome","category":"视觉冲击"},
    "duotone": {"name":"duotone","desc":"双色调","icon":"🔵","best":"双色调、duotone","category":"视觉冲击"},
    "pattern": {"name":"pattern","desc":"图案","icon":"🔮","best":"图案、pattern","category":"视觉冲击"},
    "ornate": {"name":"ornate","desc":"华丽","icon":"🎊","best":"华丽、ornate","category":"视觉冲击"},
    "rococo": {"name":"rococo","desc":"洛可可","icon":"💝","best":"洛可可、rococo","category":"视觉冲击"},
    "chrome": {"name":"chrome","desc":"镀铬","icon":"🪙","best":"镀铬、chrome","category":"视觉冲击"},
    "gold": {"name":"gold","desc":"黄金","icon":"🥇","best":"黄金、gold","category":"视觉冲击"},
    "silver": {"name":"silver","desc":"白银","icon":"🥈","best":"白银、silver","category":"视觉冲击"},
    "iridescent": {"name":"iridescent","desc":"虹彩","icon":"🌈","best":"虹彩、iridescent","category":"视觉冲击"},
    "pearlescent": {"name":"pearlescent","desc":"珍珠","icon":"🫧","best":"珍珠、pearl","category":"视觉冲击"},
    "matte": {"name":"matte","desc":"哑光","icon":"⬛","best":"哑光、matte","category":"视觉冲击"},
    "glossy": {"name":"glossy","desc":"光泽","icon":"💎","best":"光泽、glossy","category":"视觉冲击"},
    "mirror": {"name":"mirror","desc":"镜面","icon":"🪞","best":"镜面、mirror","category":"视觉冲击"},
    "shadow": {"name":"shadow","desc":"阴影","icon":"🌑","best":"阴影、shadow","category":"视觉冲击"},
    "laser": {"name":"laser","desc":"激光","icon":"🔴","best":"激光、laser","category":"视觉冲击"},
    "prism": {"name":"prism","desc":"棱镜","icon":"🔺","best":"棱镜、prism","category":"视觉冲击"},
    "crystal": {"name":"crystal","desc":"水晶","icon":"💎","best":"水晶、crystal","category":"视觉冲击"},
    "diamond": {"name":"diamond","desc":"钻石","icon":"💍","best":"钻石、diamond","category":"视觉冲击"},
    "lightning": {"name":"lightning","desc":"闪电","icon":"⚡","best":"闪电、lightning","category":"视觉冲击"},
    "storm": {"name":"storm","desc":"暴风","icon":"🌪️","best":"暴风、storm","category":"视觉冲击"},
    "volcano": {"name":"volcano","desc":"火山","icon":"🌋","best":"火山、volcano","category":"视觉冲击"},
    "tsunami": {"name":"tsunami","desc":"海啸","icon":"🌊","best":"海啸、tsunami","category":"视觉冲击"},
    "ukiyoe": {"name":"ukiyoe","desc":"浮世绘","icon":"🌊","best":"浮世绘、ukiyoe","category":"文艺清新"},
    "sumi_e": {"name":"sumi_e","desc":"水墨","icon":"🎨","best":"水墨、sumi-e","category":"文艺清新"},
    "mingqing": {"name":"mingqing","desc":"明清","icon":"🏛️","best":"明清、古典","category":"文艺清新"},
    "dunhuang": {"name":"dunhuang","desc":"敦煌","icon":"飞天","best":"敦煌、壁画","category":"文艺清新"},
    "shuimo": {"name":"shuimo","desc":"写意","icon":"🖌️","best":"写意、国画","category":"文艺清新"},
    "gongbi": {"name":"gongbi","desc":"工笔","icon":"✏️","best":"工笔、精细","category":"文艺清新"},
    "persian": {"name":"persian","desc":"波斯","icon":"🕌","best":"波斯、伊斯兰","category":"文艺清新"},
    "arabesque": {"name":"arabesque","desc":"阿拉伯","icon":"🔯","best":"阿拉伯、arabesque","category":"文艺清新"},
    "moroccan": {"name":"moroccan","desc":"摩洛哥","icon":"🏛️","best":"摩洛哥","category":"文艺清新"},
    "african": {"name":"african","desc":"非洲","icon":"🪘","best":"非洲、部落","category":"文艺清新"},
    "aztec": {"name":"aztec","desc":"阿兹特克","icon":"🦅","best":"阿兹特克","category":"文艺清新"},
    "maya": {"name":"maya","desc":"玛雅","icon":"🗿","best":"玛雅","category":"文艺清新"},
    "inca": {"name":"inca","desc":"印加","icon":"⛰️","best":"印加","category":"文艺清新"},
    "viking": {"name":"viking","desc":"维京","icon":"🛡️","best":"维京、北欧","category":"文艺清新"},
    "celtic": {"name":"celtic","desc":"凯尔特","icon":"☘️","best":"凯尔特","category":"文艺清新"},
    "egyptian": {"name":"egyptian","desc":"埃及","icon":"𓂀","best":"埃及、法老","category":"文艺清新"},
    "greek": {"name":"greek","desc":"希腊","icon":"🏛️","best":"希腊、雅典","category":"文艺清新"},
    "roman": {"name":"roman","desc":"罗马","icon":"🏛️","best":"罗马、帝国","category":"文艺清新"},
    "byzantine": {"name":"byzantine","desc":"拜占庭","icon":"☦️","best":"拜占庭","category":"文艺清新"},
    "russian": {"name":"russian","desc":"俄罗斯","icon":"套娃","best":"俄罗斯","category":"文艺清新"},
    "tokyo": {"name":"tokyo","desc":"东京","icon":"🗼","best":"东京、日本","category":"文艺清新"},
    "kyoto": {"name":"kyoto","desc":"京都","icon":"⛩️","best":"京都、古都","category":"文艺清新"},
    "paris": {"name":"paris","desc":"巴黎","icon":"🗼","best":"巴黎、法国","category":"文艺清新"},
    "london": {"name":"london","desc":"伦敦","icon":"🎡","best":"伦敦、英国","category":"文艺清新"},
    "nyc": {"name":"nyc","desc":"纽约","icon":"🗽","best":"纽约、美国","category":"文艺清新"},
    "shanghai": {"name":"shanghai","desc":"上海","icon":"🏙️","best":"上海、外滩","category":"文艺清新"},
    "chengdu": {"name":"chengdu","desc":"成都","icon":"🐼","best":"成都、四川","category":"文艺清新"},
    "yunnan": {"name":"yunnan","desc":"云南","icon":"🌺","best":"云南","category":"文艺清新"},
    "tibet": {"name":"tibet","desc":"西藏","icon":"🏔️","best":"西藏、高原","category":"文艺清新"},
    "mongolia": {"name":"mongolia","desc":"蒙古","icon":"🐎","best":"蒙古、草原","category":"文艺清新"},
    "bamboo": {"name":"bamboo","desc":"竹","icon":"🎋","best":"竹、bamboo","category":"文艺清新"},
    "lotus": {"name":"lotus","desc":"莲","icon":"🪷","best":"莲、lotus","category":"文艺清新"},
    "plum": {"name":"plum","desc":"梅","icon":"🌸","best":"梅、plum","category":"文艺清新"},
    "orchid": {"name":"orchid","desc":"兰","icon":"🌷","best":"兰、orchid","category":"文艺清新"},
    "pine": {"name":"pine","desc":"松","icon":"🌲","best":"松、pine","category":"文艺清新"},
    "maple": {"name":"maple","desc":"枫","icon":"🍁","best":"枫、maple","category":"文艺清新"},
    "willow": {"name":"willow","desc":"柳","icon":"🌿","best":"柳、willow","category":"文艺清新"},
    "ginkgo": {"name":"ginkgo","desc":"银杏","icon":"🍂","best":"银杏","category":"文艺清新"},
    "cactus": {"name":"cactus","desc":"仙人掌","icon":"🌵","best":"仙人掌","category":"文艺清新"},
    "bonsai": {"name":"bonsai","desc":"盆景","icon":"🪴","best":"盆景、bonsai","category":"文艺清新"},
    "moss": {"name":"moss","desc":"苔藓","icon":"🟢","best":"苔藓、moss","category":"文艺清新"},
    "dandelion": {"name":"dandelion","desc":"蒲公英","icon":"🌼","best":"蒲公英","category":"文艺清新"},
    "lavender": {"name":"lavender","desc":"薰衣草","icon":"💜","best":"薰衣草","category":"文艺清新"},
    "sunflower": {"name":"sunflower","desc":"向日葵","icon":"🌻","best":"向日葵","category":"文艺清新"},
    "rose": {"name":"rose","desc":"玫瑰","icon":"🌹","best":"玫瑰、rose","category":"文艺清新"},
    "tulip": {"name":"tulip","desc":"郁金香","icon":"🌷","best":"郁金香","category":"文艺清新"},
    "summer": {"name":"summer","desc":"夏","icon":"☀️","best":"夏、summer","category":"文艺清新"},
    "autumn": {"name":"autumn","desc":"秋","icon":"🍂","best":"秋、autumn","category":"文艺清新"},
    "winter": {"name":"winter","desc":"冬","icon":"❄️","best":"冬、winter","category":"文艺清新"},
    "snow2": {"name":"snow2","desc":"雪","icon":"❄️","best":"雪、snow","category":"文艺清新"},
    "fog": {"name":"fog","desc":"雾","icon":"🌫️","best":"雾、fog","category":"文艺清新"},
    "drizzle": {"name":"drizzle","desc":"细雨","icon":"🌦️","best":"细雨、drizzle","category":"文艺清新"},
    "dawn": {"name":"dawn","desc":"黎明","icon":"🌅","best":"黎明、dawn","category":"文艺清新"},
    "dusk": {"name":"dusk","desc":"黄昏","icon":"🌆","best":"黄昏、dusk","category":"文艺清新"},
    "moonlight": {"name":"moonlight","desc":"月光","icon":"🌙","best":"月光、moon","category":"文艺清新"},
    "starlight": {"name":"starlight","desc":"星光","icon":"✨","best":"星光、star","category":"文艺清新"},
    "mountain": {"name":"mountain","desc":"山","icon":"⛰️","best":"山、mountain","category":"文艺清新"},
    "valley": {"name":"valley","desc":"山谷","icon":"🏞️","best":"山谷、valley","category":"文艺清新"},
    "island": {"name":"island","desc":"岛屿","icon":"🏝️","best":"岛屿、island","category":"文艺清新"},
    "harbor": {"name":"harbor","desc":"港口","icon":"⛵","best":"港口、harbor","category":"文艺清新"},
    "lighthouse": {"name":"lighthouse","desc":"灯塔","icon":"🗼","best":"灯塔","category":"文艺清新"},
    "bridge": {"name":"bridge","desc":"桥","icon":"🌉","best":"桥、bridge","category":"文艺清新"},
    "windmill": {"name":"windmill","desc":"风车","icon":"🌬️","best":"风车","category":"文艺清新"},
    "cabin": {"name":"cabin","desc":"小屋","icon":"🏡","best":"小屋、cabin","category":"文艺清新"},
    "temple": {"name":"temple","desc":"寺庙","icon":"🛕","best":"寺庙、temple","category":"文艺清新"},
    "castle": {"name":"castle","desc":"城堡","icon":"🏰","best":"城堡、castle","category":"文艺清新"},
    "poetry": {"name":"poetry","desc":"诗","icon":"📜","best":"诗、poetry","category":"文艺清新"},
    "novel": {"name":"novel","desc":"小说","icon":"📖","best":"小说、novel","category":"文艺清新"},
    "fairytale": {"name":"fairytale","desc":"童话","icon":"🧚","best":"童话、fairytale","category":"文艺清新"},
    "myth": {"name":"myth","desc":"神话","icon":"🐉","best":"神话、myth","category":"文艺清新"},
    "haiku": {"name":"haiku","desc":"俳句","icon":"🌸","best":"俳句、haiku","category":"文艺清新"},
    "ceramic": {"name":"ceramic","desc":"陶瓷","icon":"🏺","best":"陶瓷、ceramic","category":"文艺清新"},
    "pottery": {"name":"pottery","desc":"陶器","icon":"🪔","best":"陶器、pottery","category":"文艺清新"},
    "porcelain": {"name":"porcelain","desc":"瓷器","icon":"🍵","best":"瓷器、porcelain","category":"文艺清新"},
    "lacquer": {"name":"lacquer","desc":"漆器","icon":"🪵","best":"漆器、lacquer","category":"文艺清新"},
    "weaving": {"name":"weaving","desc":"编织","icon":"🧶","best":"编织、weaving","category":"文艺清新"},
    "dyeing": {"name":"dyeing","desc":"扎染","icon":"🌀","best":"扎染、dyeing","category":"文艺清新"},
    "calligraphy": {"name":"calligraphy","desc":"书法","icon":"✒️","best":"书法、calligraphy","category":"文艺清新"},
    "seal2": {"name":"seal2","desc":"篆刻","icon":"🔲","best":"篆刻、seal","category":"文艺清新"},
    "wood": {"name":"wood","desc":"木纹","icon":"🪵","best":"木纹、wood","category":"文艺清新"},
    "stone": {"name":"stone","desc":"石头","icon":"🪨","best":"石头、stone","category":"文艺清新"},
    "marble": {"name":"marble","desc":"大理石","icon":"⬜","best":"大理石、marble","category":"文艺清新"},
    "linen": {"name":"linen","desc":"亚麻","icon":"🧵","best":"亚麻、linen","category":"文艺清新"},
    "silk": {"name":"silk","desc":"丝绸","icon":"🧣","best":"丝绸、silk","category":"文艺清新"},
    "leather": {"name":"leather","desc":"皮革","icon":"👜","best":"皮革、leather","category":"文艺清新"},
    "wabi": {"name":"wabi","desc":"侘寂","icon":"🍂","best":"侘寂、wabi","category":"文艺清新"},
    "ikigai": {"name":"ikigai","desc":"ikigai","icon":"☀️","best":"ikigai","category":"文艺清新"},
    "hygge": {"name":"hygge","desc":"hygge","icon":"🕯️","best":"hygge、舒适","category":"文艺清新"},
    "feathers": {"name":"feathers","desc":"羽毛","icon":"🪶","best":"羽毛、feather","category":"文艺清新"},
    "scales": {"name":"scales","desc":"鳞片","icon":"🐉","best":"鳞片、scale","category":"文艺清新"},
    "shell": {"name":"shell","desc":"贝壳","icon":"🐚","best":"贝壳、shell","category":"文艺清新"},
    "coral": {"name":"coral","desc":"珊瑚","icon":"🪸","best":"珊瑚、coral","category":"文艺清新"},
    "basketball": {"name":"basketball","desc":"篮球","icon":"🏀","best":"篮球、basketball","category":"生活娱乐"},
    "football": {"name":"football","desc":"足球","icon":"⚽","best":"足球、football","category":"生活娱乐"},
    "tennis": {"name":"tennis","desc":"网球","icon":"🎾","best":"网球、tennis","category":"生活娱乐"},
    "baseball": {"name":"baseball","desc":"棒球","icon":"⚾","best":"棒球、baseball","category":"生活娱乐"},
    "swimming": {"name":"swimming","desc":"游泳","icon":"🏊","best":"游泳、swimming","category":"生活娱乐"},
    "running": {"name":"running","desc":"跑步","icon":"🏃","best":"跑步、running","category":"生活娱乐"},
    "cycling": {"name":"cycling","desc":"自行车","icon":"🚴","best":"自行车、cycling","category":"生活娱乐"},
    "yoga": {"name":"yoga","desc":"瑜伽","icon":"🧘","best":"瑜伽、yoga","category":"生活娱乐"},
    "climbing": {"name":"climbing","desc":"攀岩","icon":"🧗","best":"攀岩、climbing","category":"生活娱乐"},
    "skiing": {"name":"skiing","desc":"滑雪","icon":"⛷️","best":"滑雪、skiing","category":"生活娱乐"},
    "boxing": {"name":"boxing","desc":"拳击","icon":"🥊","best":"拳击、boxing","category":"生活娱乐"},
    "golf": {"name":"golf","desc":"高尔夫","icon":"⛳","best":"高尔夫、golf","category":"生活娱乐"},
    "bbq": {"name":"bbq","desc":"烧烤","icon":"🔥","best":"烧烤、bbq","category":"生活娱乐"},
    "sushi2": {"name":"sushi2","desc":"寿司","icon":"🍣","best":"寿司、sushi","category":"生活娱乐"},
    "ramen": {"name":"ramen","desc":"拉面","icon":"🍜","best":"拉面、ramen","category":"生活娱乐"},
    "dessert": {"name":"dessert","desc":"甜点","icon":"🍰","best":"甜点、dessert","category":"生活娱乐"},
    "coffee2": {"name":"coffee2","desc":"咖啡","icon":"☕","best":"咖啡、coffee","category":"生活娱乐"},
    "tea": {"name":"tea","desc":"茶","icon":"🍵","best":"茶、tea","category":"生活娱乐"},
    "cocktail": {"name":"cocktail","desc":"鸡尾酒","icon":"🍸","best":"鸡尾酒","category":"生活娱乐"},
    "wine": {"name":"wine","desc":"红酒","icon":"🍷","best":"红酒、wine","category":"生活娱乐"},
    "beer": {"name":"beer","desc":"啤酒","icon":"🍺","best":"啤酒、beer","category":"生活娱乐"},
    "milktea": {"name":"milktea","desc":"奶茶","icon":"🧋","best":"奶茶、milktea","category":"生活娱乐"},
    "juice": {"name":"juice","desc":"果汁","icon":"🧃","best":"果汁、juice","category":"生活娱乐"},
    "christmas": {"name":"christmas","desc":"圣诞","icon":"🎄","best":"圣诞、christmas","category":"生活娱乐"},
    "halloween": {"name":"halloween","desc":"万圣","icon":"🎃","best":"万圣、halloween","category":"生活娱乐"},
    "newyear": {"name":"newyear","desc":"新年","icon":"🎉","best":"新年、newyear","category":"生活娱乐"},
    "midautumn": {"name":"midautumn","desc":"中秋","icon":"🥮","best":"中秋、mooncake","category":"生活娱乐"},
    "springfestival": {"name":"springfestival","desc":"春节","icon":"🧧","best":"春节、spring","category":"生活娱乐"},
    "valentine": {"name":"valentine","desc":"情人","icon":"💝","best":"情人、valentine","category":"生活娱乐"},
    "rpg": {"name":"rpg","desc":"RPG","icon":"⚔️","best":"RPG、角色扮演","category":"生活娱乐"},
    "fps": {"name":"fps","desc":"FPS","icon":"🎯","best":"FPS、射击","category":"生活娱乐"},
    "moba": {"name":"moba","desc":"MOBA","icon":"🏰","best":"MOBA、对战","category":"生活娱乐"},
    "racing": {"name":"racing","desc":"赛车","icon":"🏎️","best":"赛车、racing","category":"生活娱乐"},
    "puzzle": {"name":"puzzle","desc":"解谜","icon":"🧩","best":"解谜、puzzle","category":"生活娱乐"},
    "sandbox": {"name":"sandbox","desc":"沙盒","icon":"🏜️","best":"沙盒、sandbox","category":"生活娱乐"},
    "cozy": {"name":"cozy","desc":"休闲","icon":"🛋️","best":"休闲、cozy","category":"生活娱乐"},
    "classical": {"name":"classical","desc":"古典","icon":"🎼","best":"古典、classical","category":"生活娱乐"},
    "country": {"name":"country","desc":"乡村","icon":"🤠","best":"乡村、country","category":"生活娱乐"},
    "folk": {"name":"folk","desc":"民谣","icon":"🪕","best":"民谣、folk","category":"生活娱乐"},
    "funk": {"name":"funk","desc":"放克","icon":"🕺","best":"放克、funk","category":"生活娱乐"},
    "disco": {"name":"disco","desc":"迪斯科","icon":"🪩","best":"迪斯科、disco","category":"生活娱乐"},
    "techno": {"name":"techno","desc":"techno","icon":"⚙️","best":"techno、电子","category":"生活娱乐"},
    "house": {"name":"house","desc":"house","icon":"🏠","best":"house、舞曲","category":"生活娱乐"},
    "anime2": {"name":"anime2","desc":"动漫","icon":"🌸","best":"动漫、anime","category":"生活娱乐"},
    "drama": {"name":"drama","desc":"剧情","icon":"🎭","best":"剧情、drama","category":"生活娱乐"},
    "comedy": {"name":"comedy","desc":"喜剧","icon":"😂","best":"喜剧、comedy","category":"生活娱乐"},
    "romance": {"name":"romance","desc":"爱情","icon":"💕","best":"爱情、romance","category":"生活娱乐"},
    "action": {"name":"action","desc":"动作","icon":"💥","best":"动作、action","category":"生活娱乐"},
    "fantasy": {"name":"fantasy","desc":"奇幻","icon":"🐉","best":"奇幻、fantasy","category":"生活娱乐"},
    "mystery": {"name":"mystery","desc":"悬疑","icon":"🔍","best":"悬疑、mystery","category":"生活娱乐"},
    "party": {"name":"party","desc":"派对","icon":"🎉","best":"派对、party","category":"生活娱乐"},
    "picnic": {"name":"picnic","desc":"野餐","icon":"🧺","best":"野餐、picnic","category":"生活娱乐"},
    "camping": {"name":"camping","desc":"露营","icon":"⛺","best":"露营、camping","category":"生活娱乐"},
    "roadtrip": {"name":"roadtrip","desc":"公路","icon":"🚗","best":"公路、roadtrip","category":"生活娱乐"},
    "concert": {"name":"concert","desc":"演唱会","icon":"🎤","best":"演唱会、concert","category":"生活娱乐"},
    "karaoke": {"name":"karaoke","desc":"K歌","icon":"🎵","best":"K歌、karaoke","category":"生活娱乐"},
    "slow": {"name":"slow","desc":"慢生活","icon":"🐌","best":"慢生活、slow","category":"生活娱乐"},
    "eco": {"name":"eco","desc":"环保","icon":"🌱","best":"环保、eco","category":"生活娱乐"},
    "diy": {"name":"diy","desc":"DIY","icon":"🔨","best":"DIY、手工","category":"生活娱乐"},
    "reading": {"name":"reading","desc":"阅读","icon":"📚","best":"阅读、reading","category":"生活娱乐"},
    "painting": {"name":"painting","desc":"绘画","icon":"🎨","best":"绘画、painting","category":"生活娱乐"},
    "photo2": {"name":"photo2","desc":"摄影","icon":"📷","best":"摄影、photo","category":"生活娱乐"},
    "gardening": {"name":"gardening","desc":"园艺","icon":"🌱","best":"园艺、garden","category":"生活娱乐"},
    "cooking": {"name":"cooking","desc":"烹饪","icon":"👨‍🍳","best":"烹饪、cooking","category":"生活娱乐"},
    "baking": {"name":"baking","desc":"烘焙","icon":"🥖","best":"烘焙、baking","category":"生活娱乐"},
    "cat": {"name":"cat","desc":"猫","icon":"🐱","best":"猫、cat、猫咪","category":"生活娱乐"},
    "dog": {"name":"dog","desc":"狗","icon":"🐶","best":"狗、dog、狗狗","category":"生活娱乐"},
    "hamster": {"name":"hamster","desc":"仓鼠","icon":"🐹","best":"仓鼠、hamster","category":"生活娱乐"},
    "parrot": {"name":"parrot","desc":"鹦鹉","icon":"🦜","best":"鹦鹉、parrot","category":"生活娱乐"},
    "fish": {"name":"fish","desc":"鱼","icon":"🐟","best":"鱼、fish","category":"生活娱乐"},
    "hiking": {"name":"hiking","desc":"徒步","icon":"🥾","best":"徒步、hiking","category":"生活娱乐"},
    "fishing": {"name":"fishing","desc":"钓鱼","icon":"🎣","best":"钓鱼、fishing","category":"生活娱乐"},
    "kayaking": {"name":"kayaking","desc":"皮划艇","icon":"🛶","best":"皮划艇、kayak","category":"生活娱乐"},
    "stargazing": {"name":"stargazing","desc":"观星","icon":"🔭","best":"观星、star","category":"生活娱乐"},}


def make_mini_card(theme, title, subtitle, tags, badge, quote, highlights):
    """生成主题选择页的迷你卡片"""
    sk = get_scheme_by_theme(theme, 0)
    sc = COLOR_SCHEMES[sk]
    bg = sc["bg"]
    a1 = sc["accent1"]
    a2 = sc["accent2"]
    text_color = sc.get("text_color", "#ffffff")
    is_gradient = sc.get("is_gradient", False)

    # 使用 iconfont 卡通素材
    deco_assets = get_decoration_assets(theme, 0)
    (da1_url, da1_name), (da2_url, da2_name) = deco_assets[0], deco_assets[1] if len(deco_assets) > 1 else (deco_assets[0][0], deco_assets[0][1])

    # 风格对应的 emoji（用于 badge）
    theme_emoji_list = THEME_EMOJIS.get(theme, THEME_EMOJIS.get("cyber", []))
    badge_emoji = theme_emoji_list[0][1] if theme_emoji_list else ""

    dt = apply_highlights(title, highlights, theme, a1, a2)

    th = ""
    for i, t in enumerate(tags):
        tc = [a1,a2,a1,a2][i%4]
        op = 0.25 if i%2==0 else 0.20
        th += f'<span class="cv-tag" style="background:rgba({hex_to_rgb(tc)},{op});color:{tc};">{t}</span>'

    info = THEME_INFO.get(theme, {"name":theme,"desc":"","icon":"📄","best":""})
    bg_style = f"background:{bg};"

    return f'''<div class="theme-card" data-theme="{theme}" onclick="goDetail('{theme}')">
  <div class="theme-preview theme-{theme}" style="--bg-color:{bg};--accent1:{a1};--accent2:{a2};--text-color:{text_color};{bg_style}">
    <div class="cv-bg-decoration">
      <div class="cv-bg-circle" style="width:180px;height:180px;background:{a1};top:-40px;left:-40px;"></div>
      <div class="cv-bg-circle" style="width:140px;height:140px;background:{a2};bottom:-30px;right:-30px;"></div>
      <img class="cv-emoji-deco cv-iconfont-deco" src="{da1_url}" alt="{da1_name}" style="top:8%;left:4%;width:36px;height:36px;filter:drop-shadow(1px 1px 2px rgba(0,0,0,0.15));" onerror="this.style.display='none'">
      <img class="cv-emoji-deco cv-iconfont-deco" src="{da2_url}" alt="{da2_name}" style="bottom:8%;right:4%;width:28px;height:28px;filter:drop-shadow(1px 1px 2px rgba(0,0,0,0.15));" onerror="this.style.display='none'">
      <!-- 迷你卡通角色预览 -->
      <img class="cv-mascot" src="{da1_url}" alt="{da1_name}" style="right:2%;bottom:8%;width:25%;height:auto;opacity:0.88;filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.2));" onerror="this.style.display='none'">
    </div>
    <div class="cv-content">
      <div class="cv-badge" style="background:rgba({hex_to_rgb(a1)},0.2);color:{a1};border:1px solid rgba({hex_to_rgb(a1)},0.4);">{badge_emoji} {badge}</div>
      <div class="cv-main-title" style="font-size:22px;color:{text_color};">{dt}</div>
      <div class="cv-sub-title" style="font-size:11px;color:{text_color};">{subtitle}</div>
      <div class="cv-tag-row">{th}</div>
    </div>
  </div>
  <div class="theme-info">
    <div class="theme-name">{info.get("icon","📄")} {info.get("name",theme)} <span class="theme-tag">点击查看4平台效果 →</span></div>
    <div class="theme-desc">{info.get("desc","")} · 适合：{info.get("best","")}</div>
  </div>
</div>'''


def generate_picker_html(title, subtitle, tags, badge, quote, highlights, photo_url="", photo_position="right"):
    """生成主题选择首页 + 所有风格详情页（单文件）"""

    # 生成19个主题卡片，按分类分组
    all_themes = list(THEME_INFO.keys())
    # 按分类分组
    categories = {}
    for theme in all_themes:
        info = THEME_INFO.get(theme, {})
        cat = info.get("category", "其他")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(theme)
    
    cards_html = ""
    # 子分类定义：主分类 → 子分类列表
    SUBCATEGORIES = {
        "科技知识": [
            ("编程语言", "⌨️", ["python","java","golang","rust","typescript","react","vue","angular","svelte","nodejs"]),
            ("数据库", "🗄️", ["mysql","postgres","redis","mongo","sqlite","elastic"]),
            ("DevOps运维", "🔧", ["docker","k8s","terraform","jenkins","github","gitlab","prometheus","grafana","nginx","cicd","gitops","observ"]),
            ("AI/机器学习", "🧠", ["tensorflow","pytorch","huggingface","openai","langchain","ollama","stable","agent","rag","neural","copilot","embedding","prompt","vibe"]),
            ("前端工具", "🎨", ["webpack","vite","tailwind","figma","graphql","grpc"]),
            ("架构/云", "☁️", ["kafka","rabbit","spring","ddd","microsvc","serverless","blockchain","web3","saas","paas","lowcode"]),
            ("系统/工具", "💻", ["linux","terminal","vim","vscode","ssh","cron","regex","restapi","json2","yaml"]),
            ("算法/数据", "📊", ["dataviz","algo","binary","quantum2","edge","mesh2","chaos"]),
            ("科技经典", "🚀", ["bold","cyber","minimal","magazine","pixel","glass","aurora","blueprint","starfield","typewriter","glitch","synthwave","matrix","quantum","ocean","ice","glassmorph","retrofuturism","galaxy"]),
        ],
        "生活娱乐": [
            ("运动健身", "⚽", ["basketball","football","tennis","baseball","swimming","running","cycling","yoga","climbing","skiing","boxing","golf","hiking","kayaking"]),
            ("美食饮品", "🍜", ["bbq","sushi2","ramen","dessert","coffee2","tea","cocktail","wine","beer","milktea","juice","cooking","baking","food"]),
            ("节日庆典", "🎉", ["christmas","halloween","newyear","midautumn","springfestival","valentine","carnival","party"]),
            ("游戏电竞", "🎮", ["rpg","fps","moba","racing","puzzle","sandbox","gaming"]),
            ("音乐", "🎵", ["classical","country","folk","funk","disco","techno","house","concert","karaoke","jazz","edm","rock","hiphop","punk","metal","blues","reggae"]),
            ("影视娱乐", "🎬", ["anime2","drama","comedy","romance","action","fantasy","mystery","cinema","variety","anime"]),
            ("萌宠动物", "🐱", ["cat","dog","rabbit","hamster","parrot","fish","cute"]),
            ("日常爱好", "📚", ["cozy","slow","eco","diy","reading","painting","photo2","gardening","picnic","camping","roadtrip","stargazing","fishing","funny"]),
            ("娱乐经典", "🥳", ["clay","popart"]),
        ],
        "视觉冲击": [
            ("艺术流派", "🎨", ["cubism","surreal","impression","expression","fauvism","dada","construct","destijl","bauhaus","artnouveau","popart"]),
            ("摄影风格", "📷", ["macro","longexp","tiltshift","doubleexp","infrared","cyberfilm","polaroid","film","photo2","screenshot","portrait","product","zoom","contrast"]),
            ("街头潮流", "💥", ["graffiti","skate","surf","bike","tattoo","doodle","sticker","comic","neon","vaporwave","acid","memphis","holographic","graffiti"]),
            ("设计风格", "📐", ["deco","brutal2","gothic2","modernist","parametric","glam","grunge","preppy","maximal","brutalist","artdeco"]),
            ("年代复古", "📅", ["fifties","sixties","seventies","eighties","nineties","y2k2","retro","vaporwave"]),
            ("科幻赛博", "🔬", ["solarpunk","biopunk","nanopunk","posthuman","glitch2","datamosh","scifi","steampunk","noir","gothic","baroque","fire"]),
            ("数字生成", "🔢", ["ascii","generative","fractal","voronoi","particles","fluid"]),
            ("抽象几何", "🔷", ["abstract","geometric","opart","kinetic","colorfield","monochrome","duotone","pattern","ornate","rococo"]),
            ("材质质感", "✨", ["chrome","gold","silver","iridescent","pearlescent","matte","glossy","mirror","shadow","laser","prism","crystal","diamond"]),
            ("自然力量", "⛈️", ["lightning","storm","volcano","tsunami"]),
            ("冲击经典", "💥", ["paper","dopamine","luxury","tribal"]),
        ],
        "文艺清新": [
            ("东方艺术", "🎨", ["ukiyoe","sumi_e","mingqing","dunhuang","shuimo","gongbi","ink","stamp","guochao"]),
            ("世界文化", "🌍", ["persian","arabesque","moroccan","african","aztec","maya","inca","viking","celtic","egyptian","greek","roman","byzantine","russian","tribal"]),
            ("城市风情", "🏙️", ["tokyo","kyoto","paris","london","nyc","shanghai","chengdu","yunnan","tibet","mongolia"]),
            ("植物花卉", "🌿", ["bamboo","lotus","plum","orchid","pine","maple","willow","ginkgo","cactus","bonsai","moss","dandelion","lavender","sunflower","rose","tulip","spring","summer","autumn","winter"]),
            ("自然风景", "🏔️", ["snow2","fog","drizzle","dawn","dusk","moonlight","starlight","mountain","valley","island","harbor","lighthouse","bridge","windmill","cabin","temple","castle"]),
            ("文学故事", "📖", ["poetry","novel","fairytale","myth","haiku"]),
            ("手工艺", "👐", ["ceramic","pottery","porcelain","lacquer","weaving","dyeing","calligraphy","seal2","kraft","washi","ribbon","journal"]),
            ("材质纹理", "-paper", ["stone","marble","linen","silk","leather","newspaper","risograph","collage","polaroid","film"]),
            ("生活美学", "🌸", ["fresh","anime","cinema","sticker","retro","pastel","washi","terrarium","wabi","ikigai","hygge","feathers","scales","gradientmesh","aurora"]),
        ],
    }
    cat_icons = {"科技知识":"🚀","生活娱乐":"🎉","视觉冲击":"💥","文艺清新":"🍃"}
    cat_descs = {"科技知识":"编程、AI、开发工具、架构模式","生活娱乐":"运动、美食、游戏、音乐、宠物","视觉冲击":"艺术、摄影、影视、时尚、潮流","文艺清新":"文化、自然、手工艺、生活美学"}
    
    # 左侧分类导航
    sidebar_html = '<div class="sidebar">\n'
    sidebar_html += '  <div class="sidebar-header">\n'
    sidebar_html += '    <div class="sidebar-title">📁 风格分类</div>\n'
    sidebar_html += '  </div>\n'
    sidebar_html += '  <nav class="sidebar-nav">\n'
    
    # "全部"选项
    total_count = len(all_themes)
    sidebar_html += "    <a class=\"sidebar-item active\" data-cat=\"all\" onclick=\"filterCategory('all')\">\n"
    sidebar_html += "      <span class=\"sidebar-icon\">📋</span>\n"
    sidebar_html += f"      <span class=\"sidebar-label\">全部风格</span>\n"
    sidebar_html += f"      <span class=\"sidebar-count\">{total_count}</span>\n"
    sidebar_html += "    </a>\n"
    
    # 主分类 + 子分类
    for cat, themes in categories.items():
        icon = cat_icons.get(cat, "📄")
        sidebar_html += "    <div class=\"sidebar-group-header\">\n"
        sidebar_html += f"      <span class=\"sidebar-icon\">{icon}</span>\n"
        sidebar_html += f"      <span class=\"sidebar-label\">{cat}</span>\n"
        sidebar_html += f"      <span class=\"sidebar-count\">{len(themes)}</span>\n"
        sidebar_html += "    </div>\n"
        subcats = SUBCATEGORIES.get(cat, [])
        for sub_name, sub_icon, sub_themes_list in subcats:
            count = sum(1 for t in sub_themes_list if t in themes)
            if count > 0:
                safe_name = sub_name.replace("'", "\\'")
                sidebar_html += f"    <a class=\"sidebar-item sidebar-sub\" data-cat=\"{cat}\" data-subcat=\"{sub_name}\" onclick=\"filterSubCategory('{cat}','{safe_name}')\">\n"
                sidebar_html += f"      <span class=\"sidebar-icon\">{sub_icon}</span>\n"
                sidebar_html += f"      <span class=\"sidebar-label\">{sub_name}</span>\n"
                sidebar_html += f"      <span class=\"sidebar-count\">{count}</span>\n"
                sidebar_html += "    </a>\n"
    
    sidebar_html += "  </nav>\n"
    sidebar_html += "</div>\n"
    
    # 中间内容区 — 按分类生成section
    cards_html = '<div class="content-area">\n'
    cards_html += '  <div class="content-header">\n'
    cards_html += f'    <h1 class="content-title">🎨 选择封面风格</h1>\n'
    cards_html += f'    <p class="content-subtitle">{len(all_themes)}种风格 · 4大分类 · 点击卡片查看4平台详细效果</p>\n'
    
    # 自动匹配
    auto_theme = detect_theme(title, tags)
    auto_info = THEME_INFO.get(auto_theme, {"name":auto_theme,"icon":"🤖"})
    cards_html += f'    <div class="auto-match">🤖 自动推荐：<strong>{auto_info.get("icon","📄")} {auto_info.get("name",theme)}</strong>（基于标题关键词检测）</div>\n'
    cards_html += '  </div>\n'
    
    # "全部"分类区 — 展示所有风格
    cards_html += '  <div class="category-section active" data-cat="all">\n'
    cards_html += f'    <div class="category-title">📋 全部风格（{total_count}）</div>\n'
    cards_html += '    <div class="category-grid">\n'
    for theme in all_themes:
        cards_html += make_mini_card(theme, title, subtitle, tags, badge, quote, highlights) + "\n"
    cards_html += '    </div>\n'
    cards_html += '  </div>\n'
    
    # 各分类区
    for cat, themes in categories.items():
        icon = cat_icons.get(cat, "📄")
        desc = cat_descs.get(cat, "")
        cards_html += f'  <div class="category-section" data-cat="{cat}" style="display:none;">\n'
        cards_html += f'    <div class="category-title">{icon} {cat}（{len(themes)}）</div>\n'
        cards_html += f'    <div class="category-desc">{desc}</div>\n'
        cards_html += '    <div class="category-grid">\n'
        for theme in themes:
            cards_html += make_mini_card(theme, title, subtitle, tags, badge, quote, highlights) + "\n"
        cards_html += '    </div>\n'
        cards_html += '  </div>\n'
    
    cards_html += '  <div class="footer">点击任意风格卡片 → 查看 B站 / 小红书 / 微信视频号 / 手机竖版 4种尺寸效果 · 键盘 ← → 翻页 · ESC 返回选择</div>\n'
    cards_html += '</div>\n'

    # 为每个主题生成4平台详情页的HTML（内嵌为隐藏div）
    detail_pages = []
    for theme in all_themes:
        cover_cfg = {
            "title": title, "highlight_words": highlights,
            "subtitle": subtitle, "tags": tags,
            "badge": badge, "quote": quote, "theme": theme,
            "photo_url": photo_url, "photo_position": photo_position,
        }

        # 生成4平台的slides
        pks = ["bilibili","xiaohongshu","wechat","mobile"]
        slides = []
        thumbs = []
        si = 0
        for pk in pks:
            pf = PLATFORMS[pk]
            si += 1
            first = si == 1
            t = title
            label = pf.get("icon","📄") + " " + pf["name"]
            act = ' active' if first else ''
            slide_html = generate_single_cover(cover_cfg, pk, 0)
            slides.append(f'      <div class="slide{act}" data-slide="{si}">\n{slide_html}\n      </div>')
            thumbs.append(f'''        <button class="thumb-btn{act}" onclick="goSlide('{theme}',{si})" title="{t}">
          <span class="thumb-label">{label}</span>
          <span class="thumb-num">{si}</span>
        </button>''')

        slide_html_str = "\n".join(slides)
        thumb_html_str = "\n".join(thumbs)
        info = THEME_INFO.get(theme, {})
        detail_pages.append(f'''<div class="detail-page" id="detail-{theme}" style="display:none;">
  <div class="detail-header">
    <button class="back-btn" onclick="goPicker()">← 返回选择风格</button>
    <span class="detail-title">{info.get("icon","")} {info.get("name","")} · 4平台封面预览</span>
    <span class="detail-page-num"><span id="curPage-{theme}">1</span> / 4</span>
  </div>
  <div class="stage">
{slide_html_str}
  </div>
  <nav class="navbar">
{thumb_html_str}
  </nav>
</div>''')

    detail_html = "\n".join(detail_pages)

    pf_css = "\n".join(f"  .cover-{pk} {{ aspect-ratio: {v['ratio']}; max-width: {v['width']}px; }}"
                       for pk, v in PLATFORMS.items())

    import json as _json
    _subcat_map = {}
    for _cat, _subs in SUBCATEGORIES.items():
        for _name, _icon, _themes_list in _subs:
            _subcat_map[_name] = _themes_list
    subcat_map_json = _json.dumps(_subcat_map, ensure_ascii=False)
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>选择封面风格 - 视频封面生成器</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800;900&family=ZCOOL+KuaiLe&family=Ma+Shan+Zheng&display=swap');
* {{ margin:0; padding:0; box-sizing:border-box; }}

body {{
  font-family:'Noto Sans SC',-apple-system,sans-serif;
  background:#0d1117; color:rgba(255,255,255,0.8);
  min-height:100vh;
}}

/* ===== 主题选择页 — 左侧目录+中间内容 ===== */
#picker-page {{
  display:flex; min-height:100vh;
}}
#picker-page.hidden {{ display:none; }}

/* 左侧分类目录 */
.sidebar {{
  flex-shrink:0; width:240px; min-height:100vh;
  background:#0a0e14; border-right:1px solid rgba(255,255,255,0.06);
  display:flex; flex-direction:column;
  position:sticky; top:0; height:100vh; overflow-y:auto;
}}
.sidebar-header {{
  padding:20px 20px 16px; border-bottom:1px solid rgba(255,255,255,0.06);
}}
.sidebar-title {{
  font-size:16px; font-weight:800; color:rgba(255,255,255,0.9);
  letter-spacing:0.5px;
}}
.sidebar-nav {{
  flex:1; padding:12px 10px; display:flex; flex-direction:column; gap:4px;
}}
.sidebar-item {{
  display:flex; align-items:center; gap:10px;
  padding:10px 14px; border-radius:8px;
  color:rgba(255,255,255,0.55); font-size:14px; font-weight:600;
  cursor:pointer; transition:all 0.2s ease;
  text-decoration:none; user-select:none;
}}
.sidebar-item:hover {{
  background:rgba(255,255,255,0.05); color:rgba(255,255,255,0.8);
}}
.sidebar-item.active {{
  background:rgba(245,158,11,0.12); color:#f59e0b;
  border:1px solid rgba(245,158,11,0.25);
}}
.sidebar-icon {{ font-size:18px; flex-shrink:0; }}
.sidebar-label {{ flex:1; }}
.sidebar-count {{
  font-size:12px; font-weight:700; color:rgba(255,255,255,0.3);
  background:rgba(255,255,255,0.06); padding:2px 8px; border-radius:10px;
  min-width:28px; text-align:center;
}}
.sidebar-group-header {{
  display: flex; align-items: center; gap: 8px;
  padding: 8px 16px 4px 16px;
  font-size: 13px; font-weight: 700;
  color: #888; text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 8px;
  border-top: 1px solid rgba(255,255,255,0.06);
  cursor: default;
}}
.sidebar-group-header:first-child {{ border-top: none; margin-top: 0; }}
.sidebar-group-header .sidebar-icon {{ font-size: 16px; }}
.sidebar-sub {{
  padding-left: 36px !important;
  font-size: 13px !important;
}}
.sidebar-item.active .sidebar-count {{
  background:rgba(245,158,11,0.2); color:#f59e0b;
}}

/* 中间内容区 */
.content-area {{
  flex:1; padding:24px 32px; min-width:0;
  max-height:100vh; overflow-y:auto;
}}
.content-header {{
  text-align:center; margin-bottom:28px; padding:24px;
  background:linear-gradient(135deg,rgba(99,102,241,0.1),rgba(236,72,153,0.1));
  border-radius:16px; border:1px solid rgba(255,255,255,0.08);
}}
.content-title {{ font-size:28px; font-weight:800; margin-bottom:8px; }}
.content-subtitle {{ color:rgba(255,255,255,0.5); font-size:14px; }}
.auto-match {{
  margin-top:12px; padding:8px 20px; display:inline-block;
  background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.3);
  border-radius:8px; font-size:14px; color:#4ade80;
}}

.grid {{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
  gap:20px; max-width:1400px; margin:0 auto;
}}

/* ===== 分类区块 ===== */
.category-section {{
  margin:0 auto 36px; width:100%;
}}
.category-desc {{
  font-size:13px; color:rgba(255,255,255,0.35); margin-bottom:16px; padding-left:12px;
}}
.category-title {{
  font-size:18px; font-weight:800; color:#f59e0b; margin-bottom:16px; padding-left:4px;
  border-left:3px solid #f59e0b; padding-left:12px;
}}
.category-grid {{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
  gap:16px;
}}

.theme-card {{
  background:#161b22; border:1px solid rgba(255,255,255,0.08);
  border-radius:12px; overflow:hidden; cursor:pointer;
  transition:all 0.25s ease;
}}
.theme-card:hover {{
  border-color:rgba(245,158,11,0.4);
  transform:translateY(-4px);
  box-shadow:0 12px 32px rgba(0,0,0,0.4);
}}
.theme-card .theme-tag {{
  font-size:11px; color:#f59e0b; font-weight:500; float:right;
}}

.theme-preview {{
  width:100%; aspect-ratio:16/9;
  position:relative; overflow:hidden;
  display:flex; align-items:center; justify-content:center;
  color:#fff; text-align:center;
}}
.cv-bg-decoration {{ position:absolute; inset:0; pointer-events:none; z-index:0; }}
.cv-bg-circle {{ position:absolute; border-radius:50%; opacity:.06; }}
.cv-content {{
  position:relative; z-index:2; display:flex; flex-direction:column;
  align-items:center; justify-content:center; width:100%; height:100%; padding:16px;
}}
.cv-badge {{
  display:inline-flex; align-items:center; gap:4px;
  padding:3px 10px; border-radius:12px;
  font-size:10px; font-weight:700; letter-spacing:0.5px; margin-bottom:8px;
}}
.cv-main-title {{
  font-weight:900; line-height:1.1; letter-spacing:1px; margin-bottom:4px;
  max-width:90%; color:var(--text-color,#fff);
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;
}}
.cv-sub-title {{ font-weight:600; font-size:11px; opacity:0.7; margin-bottom:6px; max-width:85%; color:var(--text-color,#fff); }}
.cv-tag-row {{ display:flex; gap:4px; flex-wrap:wrap; justify-content:center; }}
.cv-tag {{ padding:2px 8px; border-radius:10px; font-size:9px; font-weight:700; }}
.cv-emoji-deco {{ position:absolute; opacity:.10; z-index:1; object-fit:contain; }}

.theme-preview[style*="#fff"] .cv-emoji-deco,
.theme-preview[style*="#fbbf24"] .cv-emoji-deco,
.theme-preview[style*="#e0f2fe"] .cv-emoji-deco,
.theme-preview[style*="#f0fdf4"] .cv-emoji-deco,
.theme-preview[style*="#fefce8"] .cv-emoji-deco,
.theme-preview[style*="#fff7ed"] .cv-emoji-deco,
.theme-preview[style*="#fdf2f8"] .cv-emoji-deco,
.theme-preview[style*="#ecfeff"] .cv-emoji-deco,
.theme-preview[style*="#fff0f5"] .cv-emoji-deco,
.theme-preview[style*="#fef3c7"] .cv-emoji-deco {{ opacity:0.15; }}

{THEME_FONT_CSS}

.theme-cute .cv-main-title {{ font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif; }}
.theme-fresh .cv-main-title {{ font-family:'Ma Shan Zheng','Noto Sans SC',sans-serif; font-weight:400; }}
.theme-anime .cv-main-title {{ font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif; }}
.theme-doodle .cv-main-title {{ font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif; }}

.theme-info {{ padding:14px 16px; }}
.theme-name {{ font-size:16px; font-weight:700; margin-bottom:4px; }}
.theme-desc {{ font-size:13px; color:rgba(255,255,255,0.45); }}

/* ===== 详情页 ===== */
.detail-page {{
  display:flex; flex-direction:column;
  height:100vh; width:100vw;
}}
.detail-page[style*="display:none"] {{ display:none !important; }}

.detail-header {{
  flex-shrink:0;
  display:flex; align-items:center; justify-content:space-between;
  padding:10px 28px;
  background:#161b22; border-bottom:1px solid rgba(255,255,255,0.08);
  color:rgba(255,255,255,0.65); font-size:13px; z-index:20;
}}
.back-btn {{
  background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);
  color:rgba(255,255,255,0.7); padding:6px 16px; border-radius:8px;
  font-family:inherit; font-size:13px; font-weight:600; cursor:pointer;
  transition:all 0.2s;
}}
.back-btn:hover {{
  background:rgba(255,255,255,0.1); border-color:rgba(255,255,255,0.2);
  color:#fff;
}}
.detail-title {{ font-weight:600; color:rgba(255,255,255,0.85); font-size:14px; }}
.detail-page-num {{ font-family:'SF Mono',Monaco,monospace; font-size:12px; color:rgba(255,255,255,0.35); }}

.stage {{
  flex:1; display:flex; align-items:center; justify-content:center;
  padding:20px 40px; overflow:hidden; position:relative;
}}
.slide {{
  display:none; width:100%; height:100%;
  align-items:center; justify-content:center;
  animation:slideIn 0.3s ease;
}}
.slide.active {{ display:flex; }}
@keyframes slideIn {{ from{{opacity:0;transform:scale(.96)}} to{{opacity:1;transform:scale(1)}} }}

.cover-card {{
  width:94%; max-height:92%;
  border-radius:8px; overflow:hidden; position:relative;
  box-shadow:0 12px 48px rgba(0,0,0,.5);
  display:flex; align-items:center; justify-content:center;
  color:#fff; text-align:center; background:var(--bg-color,#1a1a2e);
}}
{pf_css}

.cover-card .cv-bg-decoration {{ position:absolute; inset:0; pointer-events:none; z-index:0; }}
.cover-card .cv-bg-circle {{ position:absolute; border-radius:50%; opacity:.06; }}
.cover-card .cv-content {{
  position:relative; z-index:2; display:flex; flex-direction:column;
  align-items:center; justify-content:center; width:100%; height:100%; padding:40px;
}}
.cover-card .cv-badge {{
  display:inline-flex; align-items:center; gap:6px;
  padding:6px 18px; border-radius:20px;
  font-size:14px; font-weight:700; letter-spacing:1px; margin-bottom:16px;
}}
.cover-card .cv-main-title {{
  font-weight:900; line-height:1.08; letter-spacing:2px; margin-bottom:10px;
  text-shadow:0 4px 20px rgba(0,0,0,.4); max-width:90%; color:var(--text-color,#fff);
}}
.cover-card .cv-sub-title {{
  font-weight:600; margin-bottom:16px; letter-spacing:1px; max-width:85%;
  color:var(--text-color,#fff); opacity:0.8;
}}
.cover-card .cv-tag-row {{ display:flex; gap:10px; flex-wrap:wrap; justify-content:center; margin-top:14px; }}
.cover-card .cv-tag {{ padding:6px 18px; border-radius:16px; font-size:15px; font-weight:700; letter-spacing:.5px; }}
.cover-card .cv-emoji-deco {{ position:absolute; opacity:.10; z-index:1; object-fit:contain; }}
.cover-card .cv-bottom-bar {{
  position:absolute; bottom:0; left:0; right:0; height:36px;
  background:rgba(0,0,0,.35); backdrop-filter:blur(4px);
  display:flex; align-items:center; justify-content:space-between;
  padding:0 28px; font-size:13px; color:rgba(255,255,255,.5); z-index:4;
}}

/* 平台适配 */
.cover-xiaohongshu .cv-content {{ padding:36px 32px; }}
.cover-xiaohongshu .cv-main-title {{ line-height:1.12; }}
.cover-wechat .cv-content {{ padding:32px 28px; }}
.cover-wechat .cv-main-title {{ line-height:1.15; }}
.cover-wechat .cv-badge {{ margin-bottom:24px; }}
.cover-mobile .cv-content {{ padding:28px 24px; }}
.cover-mobile .cv-main-title {{ line-height:1.18; letter-spacing:1px; }}
.cover-mobile .cv-badge {{ margin-bottom:28px; padding:5px 14px; font-size:12px; }}
.cover-mobile .cv-sub-title {{ font-size:19px; margin-bottom:12px; }}
.cover-mobile .cv-tag {{ padding:5px 14px; font-size:13px; }}
.cover-card[style*="linear-gradient"] {{ background:var(--bg-color); }}

/* 浅色背景 */
.cover-card[style*="#fff"] .cv-bottom-bar,
.cover-card[style*="#fbbf24"] .cv-bottom-bar,
.cover-card[style*="#e0f2fe"] .cv-bottom-bar,
.cover-card[style*="#f0fdf4"] .cv-bottom-bar,
.cover-card[style*="#fefce8"] .cv-bottom-bar,
.cover-card[style*="#fff7ed"] .cv-bottom-bar,
.cover-card[style*="#fdf2f8"] .cv-bottom-bar,
.cover-card[style*="#ecfeff"] .cv-bottom-bar,
.cover-card[style*="#fff0f5"] .cv-bottom-bar,
.cover-card[style*="#fef3c7"] .cv-bottom-bar {{
  background:rgba(0,0,0,.12); color:rgba(0,0,0,.4);
}}

.navbar {{
  flex-shrink:0;
  display:flex; align-items:center; gap:6px;
  padding:10px 20px 14px;
  background:#161b22; border-top:1px solid rgba(255,255,255,0.08);
  overflow-x:auto; overflow-y:hidden;
  -webkit-overflow-scrolling:touch;
  scrollbar-width:none;
}}
.navbar::-webkit-scrollbar {{ display:none; }}

.thumb-btn {{
  flex-shrink:0;
  display:flex; align-items:center; gap:6px;
  padding:7px 14px; border-radius:6px;
  border:1.5px solid rgba(255,255,255,.12);
  background:rgba(255,255,255,.04);
  color:rgba(255,255,255,.55);
  font-family:inherit; font-size:12px; font-weight:600;
  cursor:pointer; transition:all 0.2s ease; white-space:nowrap;
}}
.thumb-btn:hover {{
  background:rgba(255,255,255,.08); color:rgba(255,255,255,.75);
  border-color:rgba(255,255,255,.2);
}}
.thumb-btn.active {{
  background:rgba(245,158,11,.15); color:#f59e0b;
  border-color:rgba(245,158,11,.5);
  box-shadow:0 0 12px rgba(245,158,11,.15);
}}
.thumb-label {{ font-weight:700; white-space:nowrap; }}
.thumb-num {{
  font-size:10px; font-weight:600;
  min-width:16px; height:16px; line-height:16px;
  border-radius:4px; text-align:center;
  background:currentColor; color:transparent;
  -webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3'/%3E%3C/svg%3E") center/contain no-repeat;
  mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3'/%3E%3C/svg%3E") center/contain no-repeat;
}}
.thumb-btn.active .thumb-num {{
  background:#f59e0b; color:#fff;
  -webkit-mask:none; mask:none;
}}

.footer {{
  text-align:center; margin-top:32px; padding:20px;
  color:rgba(255,255,255,0.3); font-size:13px;
}}
</style>
</head>
<body>

<!-- ===== 主题选择页（左侧目录 + 中间内容） ===== -->
<div id="picker-page">
{sidebar_html}
{cards_html}
</div>

<!-- ===== 13个详情页（隐藏） ===== -->
{detail_html}

<script>
// 子分类映射
const SUBCAT_MAP = {subcat_map_json};

// 分类筛选
function filterCategory(cat) {{
  // 更新左侧导航高亮
  document.querySelectorAll('.sidebar-item').forEach(item => {{
    item.classList.remove('active');
  }});
  const activeItem = document.querySelector('.sidebar-item[data-cat="' + cat + '"]');
  if (activeItem) activeItem.classList.add('active');
  
  // 显示/隐藏中间内容区的分类section
  document.querySelectorAll('.category-section').forEach(section => {{
    if (cat === 'all' || section.dataset.cat === cat) {{
      section.style.display = '';
      section.classList.add('active');
    }} else {{
      section.style.display = 'none';
      section.classList.remove('active');
    }}
  }});
  
  // 滚动到顶部
  document.querySelector('.content-area').scrollTo(0, 0);
}}

// 子分类筛选
function filterSubCategory(cat, subcat) {{
  // 更新左侧导航高亮
  document.querySelectorAll('.sidebar-item').forEach(item => {{
    item.classList.remove('active');
  }});
  const activeItem = document.querySelector('.sidebar-item[data-subcat="' + subcat + '"]');
  if (activeItem) activeItem.classList.add('active');
  
  // 显示对应分类区域
  document.querySelectorAll('.category-section').forEach(section => {{
    if (section.dataset.cat === cat) {{
      section.style.display = '';
      section.classList.add('active');
      // 在section内只显示匹配子分类的卡片
      const subThemes = section.querySelectorAll('.mini-card');
      subThemes.forEach(card => {{
        const themeName = card.dataset.theme;
        const subcatData = SUBCAT_MAP[subcat];
        if (subcatData && subcatData.includes(themeName)) {{
          card.style.display = '';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }} else {{
      section.style.display = 'none';
      section.classList.remove('active');
    }}
  }});
  
  // 更新标题
  const titleEl = document.querySelector('.content-title');
  if (titleEl) titleEl.textContent = subcat + ' 风格';
  
  document.querySelector('.content-area').scrollTo(0, 0);
}}

// 主题选择 → 详情页
function goDetail(theme) {{
  document.getElementById('picker-page').classList.add('hidden');
  document.querySelectorAll('.detail-page').forEach(d => d.style.display = 'none');
  const dp = document.getElementById('detail-' + theme);
  if (dp) {{
    dp.style.display = 'flex';
    // 重置到第一页
    goSlide(theme, 1);
  }}
}}

// 返回选择页
function goPicker() {{
  document.getElementById('picker-page').classList.remove('hidden');
  document.querySelectorAll('.detail-page').forEach(d => d.style.display = 'none');
}}

// 详情页内翻页
var slideState = {{}};
function goSlide(theme, n) {{
  const total = 4;
  if (n < 1 || n > total) return;
  slideState[theme] = n;
  const dp = document.getElementById('detail-' + theme);
  if (!dp) return;
  dp.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
  const slide = dp.querySelector('.slide[data-slide="' + n + '"]');
  if (slide) slide.classList.add('active');
  dp.querySelectorAll('.thumb-btn').forEach(b => b.classList.remove('active'));
  const btns = dp.querySelectorAll('.thumb-btn');
  if (btns[n-1]) btns[n-1].classList.add('active');
  const pg = document.getElementById('curPage-' + theme);
  if (pg) pg.textContent = n;
}}

// 键盘翻页（在详情页时生效）
document.addEventListener('keydown', function(e) {{
  // 找到当前显示的详情页
  let activeTheme = null;
  document.querySelectorAll('.detail-page').forEach(d => {{
    if (d.style.display === 'flex') {{
      activeTheme = d.id.replace('detail-', '');
    }}
  }});
  if (!activeTheme) return;
  
  const cur = slideState[activeTheme] || 1;
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') goSlide(activeTheme, cur - 1);
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') goSlide(activeTheme, cur + 1);
  if (e.key === 'Escape') goPicker();
}});
</script>

</body>
</html>'''


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="主题选择器 v2.0 - 点击跳转4平台详情")
    p.add_argument("--title","-t",default="都在写AI Agent项目，怎么拉开技术差距？")
    p.add_argument("--subtitle",default="阿里也在做的核心技术项目")
    p.add_argument("--tags",default="AI Agent,技术差距,阿里,核心项目")
    p.add_argument("--badge",default="深度解析")
    p.add_argument("--quote",default="")
    p.add_argument("--highlight",default="拉开技术差距,核心技术项目")
    p.add_argument("--output","-o",default="theme-picker.html")
    p.add_argument("--photo-url",default="",help="真人出镜照片URL或本地路径")
    p.add_argument("--photo-position",default="right",choices=["right","left","center"],help="照片位置")
    a = p.parse_args()

    html = generate_picker_html(
        title=a.title, subtitle=a.subtitle,
        tags=[t.strip() for t in a.tags.split(",")],
        badge=a.badge,
        quote=a.quote,
        highlights=[h.strip() for h in a.highlight.split(",")],
        photo_url=a.photo_url,
        photo_position=a.photo_position,
    )
    with open(a.output,"w",encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 主题选择器已生成 → {a.output}")
    print(f"   {len(THEME_INFO)}种风格 · 4大分类 · 点击卡片跳转4平台详情页")