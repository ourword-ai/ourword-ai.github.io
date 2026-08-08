#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO/GEO build for the ourword.ai apex. Run from the repo root: python seo/build_seo.py

The apex is the only origin-level page on the domain, which makes it the one that
matters structurally:

  * robots.txt is per-origin — https://ourword.ai/robots.txt is the ONLY one crawlers
    read. The copies inside /idea/, /zouni/ and friends are decorative. So this file
    is where every project's sitemap has to be declared.
  * sitemap.xml here is a sitemap INDEX pointing at each project's own sitemap, so one
    submission covers the whole domain.
  * llms.txt here is the hub an answer engine lands on first; it forwards to each
    project's llms.txt and llms-full.txt.
  * The directory itself is fetched from the GitHub API at runtime, so a crawler sees
    "正在加载……". The same list is written into the page statically as well.
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo_kit as G

SITE = G.Site(
    path="",
    name="OurWord AI", name_zh="OurWord AI",
    tagline="small, sharp tools and open research — touching the world with AI",
    tagline_zh="用 AI 触摸这个世界",
    description=(
        "OurWord AI builds small, sharp, open things: a board of ideas worth building with "
        "the evidence attached, a shelf of agent skills, a falsifiable monitor of the AI "
        "build-out, a twenty-year projection of AI and work, a knowledge base of how the "
        "world actually works, a road-trip planner that re-plans itself, and a portfolio "
        "dashboard that refuses to know what you are worth. Everything is public on GitHub."),
    description_zh=(
        "OurWord AI 做一些小而锋利的开放项目：一块带证据的灵感看板、一家 Agent Skill 精选店、"
        "一份可证伪的 AI 泡沫监测、一份 AI × 职业的二十年推演、一个关于世界如何运转的知识库、"
        "一个路上有变会自己重排的旅行规划器，以及一个故意不知道你有多少钱的投资看板。"
        "全部开源在 GitHub 上。"),
    keywords=("OurWord AI, ourword.ai, 开源项目, AI 工具, 灵感看板, agent skills, AI 泡沫, "
              "AI 与就业, 生存智慧, 旅行规划, open source AI tools"),
    item_type="WebSite", item_noun="project", item_noun_zh="项目",
    lang="zh-Hans", changefreq="daily",
)

# path, en name, zh name, one-line en, one-line zh, what you get, has its own sitemap
PROJECTS = [
    ("idea", "Idea", "灵感看板",
     "A hand-operated board of things worth building, every entry with first-hand evidence attached.",
     "一块人工维护的灵感看板：只收指得出具体普通人在用的方向，每条都带第一手原声证据。",
     "Reddit / 小红书 / GitHub issue 里的真人原话 + 谁在用、缺什么、什么会杀死它。", True),
    ("skill-store", "Skill Store", "Skill 商店",
     "A daily-restocked shelf of agent skills for coding agents.",
     "每天上新的 Agent Skill 精选店，给 Claude Code、Codex 这类编程智能体用。",
     "249 个 skill，每个都有它做什么、适合谁、一行安装命令。", True),
    ("ai-bubble-detector", "AI Bubble Monitor", "AI 泡沫检测仪",
     "Twenty falsifiable red lines on the AI build-out, checked against live numbers.",
     "20 条可证伪的红线实时监测 AI 基建泡沫，环境 / 结构 / 引爆三级判定。",
     "每条红线的阈值事先写死，公开记录每一次改口，并列出自己已知的盲点。", True),
    ("ai-jobs-20yr-report", "The Restructuring of Work", "工作的重构",
     "How AI reshapes every kind of job, 2026–2046.",
     "AI × 职业的二十年推演（2026–2046）：岗位是任务束，不是一个整体。",
     "20 类职业逐一推演、四个阶段、五分钟暴露度自测、以及这份推演哪里可能错。", True),
    ("HumanWorld", "Human World", "人类世界生存法则",
     "80+ figures and classic texts on how the world actually works, across 2,600 years.",
     "80 多个人物与典籍的生存智慧知识库，跨越 2600 年、7 大分类。",
     "每条写清楚这个人真正留下的那一个想法、背后的故事、拆开的分则与今天怎么用。", True),
    ("zouni", "Zouni", "走你",
     "A road-trip plan you can actually drive, that re-plans itself when things change.",
     "计划赶得上变化：点几下出一份能直接走的旅行攻略，路上有变自己重排。",
     "北疆环线 / 青甘大环线 / 川西 / 滇西北 / 香港，逐日逐站带车程、住宿与花费。", True),
    ("portfolio-tracker", "Market Watch", "投资观察仪表盘",
     "Watch the shape of your portfolio, never the amount.",
     "只看持仓占比与买卖区间，不含金额，数据全部留在浏览器里。",
     "集中度、资产分布、以 100 为起点的指数化净值曲线、实时加密价格。", True),
]

HOW = ("Everything here is a static site built from public data and committed to GitHub; "
       "each project regenerates its own SEO/GEO artefacts from the same shared generator "
       "(seo/geo_kit.py), so what a crawler reads is always what the site actually contains.")

CITE = ("Cite the individual project page or entry page rather than this directory. Each "
        "project states its own citation rule in its llms.txt.")


def load_items():
    items = []
    for path, en, zh, one_en, one_zh, gets, _sm in PROJECTS:
        base = "https://ourword.ai/%s/" % path
        blocks = [
            ("What is it?", one_en),
            ("What do you get?", G.plain(gets)),
            ("Where to read it", "%s\nMachine-readable: %sllms.txt · %sllms-full.txt"
             % (base, base, base)),
        ]
        blocks_zh = [
            ("Q：这是什么？", one_zh),
            ("Q：能拿到什么？", gets),
            ("在哪读", "%s\n机器可读：%sllms.txt · %sllms-full.txt" % (base, base, base)),
        ]
        items.append(G.Item(slug=path, title=en, summary=one_en, title_zh=zh,
                            summary_zh=one_zh, blocks=blocks, blocks_zh=blocks_zh,
                            source_url="https://github.com/ourword-ai/%s" % path,
                            url_override=base, tags=[en, zh]))
    return items


def static_directory(items):
    """The project list, written into the page — the JS version is invisible to crawlers."""
    rows = []
    for it, (path, en, zh, one_en, one_zh, gets, _s) in zip(items, PROJECTS):
        rows.append(
            '<li><h3><a href="https://ourword.ai/%s/">%s · %s</a></h3>'
            '<p>%s</p><p>%s</p>'
            '<p><a href="https://github.com/ourword-ai/%s">GitHub</a> · '
            '<a href="https://ourword.ai/%s/llms.txt">llms.txt</a></p></li>'
            % (path, G.esc(zh), G.esc(en), G.esc(one_zh), G.esc(gets), path, path))
    return ('<noscript><section id="projects-static"><h2>%s</h2><p>%s</p><ul>%s</ul>'
            '<p><a href="/sitemap.xml">sitemap</a> · <a href="/llms.txt">llms.txt</a> · '
            '<a href="/robots.txt">robots.txt</a></p></section></noscript>'
            % (G.esc("OurWord AI 项目目录"), G.esc(SITE.description_zh), "".join(rows)))


def write_sitemap_index(today):
    """One submission covers the whole domain."""
    rows = ["  <sitemap><loc>https://ourword.ai/%s/sitemap.xml</loc>"
            "<lastmod>%s</lastmod></sitemap>" % (p[0], today) for p in PROJECTS if p[6]]
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           '  <sitemap><loc>https://ourword.ai/sitemap-root.xml</loc>'
           "<lastmod>%s</lastmod></sitemap>\n%s\n</sitemapindex>\n" % (today, "\n".join(rows)))
    return G._write("sitemap.xml", xml)


def write_root_sitemap(today):
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           '  <url><loc>https://ourword.ai/</loc><lastmod>%s</lastmod>'
           "<changefreq>daily</changefreq><priority>1.0</priority></url>\n"
           "</urlset>\n" % today)
    return G._write("sitemap-root.xml", xml)


def write_root_robots():
    """The only robots.txt on the domain that any crawler actually reads."""
    L = ["# ourword.ai — we want to be crawled, indexed and cited by search and AI answer engines.",
         "# This is the origin-level robots.txt; every project sitemap is declared here.", "",
         "User-agent: *", "Allow: /", ""]
    for a in G.AI_AGENTS:
        L += ["User-agent: %s" % a, "Allow: /", ""]
    L.append("Sitemap: https://ourword.ai/sitemap.xml")
    for p in PROJECTS:
        if p[6]:
            L.append("Sitemap: https://ourword.ai/%s/sitemap.xml" % p[0])
    L.append("")
    return G._write("robots.txt", "\n".join(L))


def main():
    today = datetime.date.today().isoformat()
    items = load_items()

    rep = G.build(SITE, items, root=".", today=today, how_built=HOW, cite_as=CITE,
                  item_pages=False)
    # Override the generic artefacts with the apex-specific ones.
    rep["sitemap_index"] = write_sitemap_index(today)
    rep["sitemap_root"] = write_root_sitemap(today)
    rep["robots"] = write_root_robots()

    src = open("index.html", encoding="utf-8").read()
    rep["directory"] = G._write("index.html", G._inject_body(src, G._BODY_MARK[0] +
                                static_directory(items) + G._BODY_MARK[1]))
    print("ourword.ai root seo/geo:", json.dumps(rep, ensure_ascii=False))
    return rep


if __name__ == "__main__":
    main()
