#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""content.json -> card-NN.html（五種頁型）
用法: python3 scripts/build.py content.json out/
"""
import json, sys, os, html, shutil

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HERE, "assets")

FILTERS = '''<svg width="0" height="0" style="position:absolute">
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="3" seed="{seed}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="6.5" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="rough2"><feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="{seed2}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.5" xChannelSelector="R" yChannelSelector="G"/></filter>
</svg>'''

def e(s):
    return html.escape(str(s or ""))

def icon(name, cls="ic"):
    return f'<svg class="{cls}"><use href="#i-{e(name)}"/></svg>' if name else ""

def dashes(green=False, rev=False):
    c = "dashes" + (" g" if green else "") + (" rev" if rev else "")
    return f'<div class="{c}"><i></i><i></i><i></i></div>'

def box(inner, fill=False, style=""):
    bg = '<div class="bg"></div>' if fill else ""
    cls = "box fill" if fill else "box"
    return f'<div class="{cls}" style="{style}">{bg}<div class="ink"></div><div class="c">{inner}</div></div>'

def heading(h, en=None, underline=False, deco=False):
    out = ""
    t = f'<div class="hdr{" hdr-u" if underline else ""}">{e(h)}</div>'
    if deco:
        out += f'<div class="dash-title">{dashes()}{t}{dashes(rev=True)}</div>'
    else:
        out += t
    if en:
        out += f'<div class="hdr-en">{e(en)}</div>'
    return out

def bullets(items):
    return "".join(f'<div class="bul">{e(b)}</div>' for b in items or [])

def quote_block(q):
    if not q:
        return ""
    by = f'<span class="by">—— {e(q.get("by",""))}</span>' if q.get("by") else ""
    return box(f'<div class="quote"><span class="qmark">&ldquo;</span><div>{e(q["text"])}{by}</div></div>', fill=True)

# ---------- 五種頁型 ----------
def t_cover(c):
    L = c.get("list", {})
    rows = ""
    for i, it in enumerate(L.get("items", []), 1):
        en = f'<small>({e(it["en"])})</small>' if it.get("en") else ""
        fs = ' style="font-size:27px"' if len(it.get("cn", "")) > 8 else ""
        rows += (f'<div class="prow"><div class="pnum">{i}.</div>'
                 f'<div class="picon">{icon(it.get("icon"))}</div>'
                 f'<div class="ptxt"{fs}>{e(it["cn"])}{en}</div></div>')
    left = box(heading(L.get("heading",""), L.get("headingEn"), underline=True)
               + f'<div class="plist">{rows}</div>', fill=True)

    S = c.get("stats", {})
    st = []
    for it in S.get("items", []):
        st.append(f'<div class="stat">{icon(it.get("icon"),"ic ic-l")}'
                  f'<div class="name">{e(it.get("name",""))}</div>'
                  f'<div class="desc">{e(it.get("desc",""))}</div></div>')
    right = box(heading(S.get("heading",""), deco=True) + '<div class="hr"></div>'.join(st))

    head = box(f'<div class="dash-title">{dashes(green=True)}<h1>{e(c["title"])}</h1>{dashes(green=True,rev=True)}</div>'
               + (f'<div class="sub-cn" style="margin-top:8px">{e(c["subCn"])}</div>' if c.get("subCn") else "")
               + (f'<div class="sub-en">{e(c["subEn"])}</div>' if c.get("subEn") else "")
               + (f'<div class="sub-note">{e(c["note"])}</div>' if c.get("note") else ""))
    return head + f'<div class="grid2">{left}{right}</div>'

def t_numbers(c):
    cells = ""
    for it in c.get("items", []):
        cells += box(f'<div class="stat">{icon(it.get("icon"),"ic ic-l")}'
                     f'<div class="name">{e(it.get("name",""))}</div>'
                     f'<div class="val">{e(it.get("value",""))}</div>'
                     f'<div class="desc">{e(it.get("desc",""))}</div></div>', fill=True)
    grid = f'<div class="grid2e">{cells}</div>'
    strip = ""
    if c.get("strip"):
        s = c["strip"]
        strip = box(f'<div style="display:flex;align-items:center;gap:16px">{icon(s.get("icon","people"),"ic ic-l")}'
                    f'<div><div class="hdr" style="text-align:left">{e(s.get("heading",""))}</div>'
                    f'<div style="font-size:21px;line-height:1.4">{e(s.get("text",""))}</div></div></div>', fill=True)
    return head_block(c) + grid + strip

def t_contrast(c):
    def side(d, fill):
        return box(heading(d.get("heading",""), d.get("headingEn"), underline=True)
                   + f'<div style="margin-top:10px">{bullets(d.get("items"))}</div>', fill=fill)
    mid = (f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:0 4px">'
           f'{icon("arrow","ic ic-l ic-a")}<div style="font-size:21px;color:var(--accent);text-align:center;line-height:1.2">'
           f'{e(c.get("arrow",""))}</div></div>')
    grid = (f'<div style="display:grid;grid-template-columns:1fr 130px 1fr;gap:10px;flex:1;min-height:0">'
            f'{side(c.get("before",{}),False)}{mid}{side(c.get("after",{}),True)}</div>')
    return head_block(c) + grid + quote_block(c.get("quote"))

def t_panels(c):
    items = c.get("panels", [])
    cols = c.get("cols") or (3 if len(items) > 4 else 2)
    cells = ""
    for p in items:
        cells += box((f'<div style="text-align:center">{icon(p.get("icon"),"ic ic-l")}</div>' if p.get("icon") else "")
                     + heading(p.get("heading",""), p.get("headingEn"))
                     + f'<div style="margin-top:6px">{bullets(p.get("items"))}</div>'
                     + (f'<div class="src">{e(p["src"])}</div>' if p.get("src") else ""), fill=True)
    grid = (f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:16px;flex:1;min-height:0">{cells}</div>')
    return head_block(c) + grid + quote_block(c.get("quote"))

def t_checklist(c):
    rows = ""
    for i, it in enumerate(c.get("items", []), 1):
        rows += box(f'<div style="display:grid;grid-template-columns:66px 1fr;gap:14px;align-items:center">'
                    f'<div style="text-align:center">{icon(it.get("icon"),"ic")}'
                    f'<div class="pnum" style="font-size:30px">{i}</div></div>'
                    f'<div><div style="font-size:33px;color:var(--ink);line-height:1.15">{e(it.get("heading",""))}</div>'
                    f'<div style="font-size:23px;line-height:1.3">{e(it.get("text",""))}</div></div></div>', fill=True)
    tail = ""
    if c.get("links"):
        rows_l = "<br>".join(e(x) for x in c["links"].get("items", []))
        tail = box(f'<div style="display:flex;align-items:center;gap:16px">{icon(c["links"].get("icon","code"),"ic ic-l")}'
                   f'<div style="font-size:22px;line-height:1.5">{rows_l}</div></div>', fill=True)
    return head_block(c) + f'<div class="rows">{rows}{tail}</div>'

def head_block(c):
    out = ""
    if c.get("title"):
        out += f'<h2>{e(c["title"])}</h2>'
    if c.get("subEn"):
        out += f'<div class="sub-en">{e(c["subEn"])}</div>'
    if c.get("thesis"):
        out += f'<div class="thesis">{e(c["thesis"])}</div>'
    return out

TYPES = {"cover": t_cover, "numbers": t_numbers, "contrast": t_contrast,
         "panels": t_panels, "checklist": t_checklist}

def render(c, idx, total, meta, icons):
    body = TYPES[c["type"]](c)
    chip = f'<div class="chip">{e(c["chip"])}</div>' if c.get("chip") else ""
    punch = ""
    if c.get("punch"):
        punch = f'<div class="punch">{icon(c.get("punchIcon","bulb"),"ic ic-a")}<span>{e(c["punch"])}</span></div>'
    foot = f'來源：{e(meta.get("source",""))}'
    if meta.get("author"):
        foot += f'｜作者 {e(meta["author"])}'
    if meta.get("date"):
        foot += f'｜{e(meta["date"])}'
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<link rel="stylesheet" href="card.css"></head><body>
{FILTERS.format(seed=7+idx*3, seed2=3+idx*2)}
{icons}
<div class="card">{chip}<div class="pageno">{idx}/{total}</div>
{body}
{punch}
<div class="foot">{foot}</div>
</div></body></html>'''

def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    data = json.load(open(src, encoding="utf-8"))
    meta = data.get("meta", {})
    cards = data["cards"]
    total = meta.get("total") or len(cards)
    icons = open(os.path.join(ASSETS, "icons.svg"), encoding="utf-8").read()
    shutil.copy(os.path.join(ASSETS, "card.css"), os.path.join(out, "card.css"))
    for i, c in enumerate(cards, 1):
        if c["type"] not in TYPES:
            raise SystemExit(f"未知頁型 {c['type']}；可用：{list(TYPES)}")
        p = os.path.join(out, f"card-{i:02d}.html")
        open(p, "w", encoding="utf-8").write(render(c, i, total, meta, icons))
        print("wrote", p)

if __name__ == "__main__":
    main()
