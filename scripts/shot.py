#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML -> PNG（1080x1080）。用法: python3 scripts/shot.py out/ [scale]
另外會回報每張卡是否有內容溢出（overflow），方便 Step 4 自檢。"""
import sys, os, glob, asyncio
from playwright.async_api import async_playwright

SIZE = 1080

async def main(d, scale=1):
    files = sorted(glob.glob(os.path.join(d, "card-*.html")))
    if not files:
        raise SystemExit(f"{d} 內找不到 card-*.html")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": SIZE, "height": SIZE},
                              device_scale_factor=scale)
        for f in files:
            await pg.goto("file://" + os.path.abspath(f))
            await pg.wait_for_timeout(500)
            over = await pg.evaluate("""() => {
              const bad = [];
              document.querySelectorAll('.card *').forEach(el => {
                if (el.scrollHeight - el.clientHeight > 6 || el.scrollWidth - el.clientWidth > 6)
                  bad.push((el.className||el.tagName)+'');
              });
              const c = document.querySelector('.card');
              if (c.scrollHeight > c.clientHeight + 6) bad.push('CARD-OVERFLOW');
              return bad.slice(0,5);
            }""")
            out = f.replace(".html", ".png")
            await pg.screenshot(path=out)
            flag = "  ⚠ 溢出: " + ", ".join(over) if over else ""
            print("shot", out, flag)
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1))
