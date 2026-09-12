---
name: knowledge-card
description: 產出「中文手繪風知識圖卡」——深綠框線＋朱橘重點＋淺綠面板＋繁體手寫字體的 1:1 方形資訊卡，可單張或十連張成套。用 HTML+CSS+Chromium 渲染成 PNG，文字 100% 精確。當使用者說「做成圖卡」「懶人包」「做一張圖給群組看」「這篇整理成圖」「social 卡片」「知識卡」「把重點做成圖」，或要把一篇文章／會議結論／產品比較壓成可轉發的圖片時觸發。不用於：需要照片級寫實或插畫的圖（那走生圖模型）、需要互動的頁面（走 HTML artifact）、正式客戶交付文件（走 docx/pptx skill）。
---

# 手繪風知識圖卡產生器

## 鐵律（違反任一條就是做錯）

1. **不用生圖模型做這種圖。** 圖卡的價值 100% 在文字，生圖模型無法保證繁體中文字形正確與十張風格一致。一律 HTML→Chromium 截圖。
2. **壓縮不得製造來源沒有的東西。** 不外插數字、不補未經查證的歸屬。來源沒說「每半年翻一倍」就不能寫。無法確認的內容直接不放進卡。
3. **每格 ≤4 條要點、每條 ≤20 字。** 塞不下就多開一張卡，不要縮字級。
4. **朱橘色元素每張 ≤3 處**（標籤／關鍵數字／底部金句）。這是這套風格不亂的唯一原因。
5. **頁尾出處欄不可省**：`來源：X｜作者 Y｜YYYY.MM.DD`。

---

## 五步流程

### Step 1 — 先寫 `content.json`，不碰版面

強迫先想清楚要說什麼。結構見 `references/content-schema.md`。最小例：

```json
{
  "meta": { "source": "Claude 官方 blog", "author": "Michael Segner", "date": "2026.08.20", "total": 3 },
  "cards": [
    { "type": "cover", "title": "…", "subCn": "…", "subEn": "…", "note": "…",
      "list": { "heading": "五大原則", "headingEn": "5 Principles",
                "items": [{ "icon": "rocket", "cn": "人人都能發布", "en": "Everyone ships" }] },
      "stats": { "heading": "亮眼數字", "items": [{ "icon": "chart", "name": "ClickHouse", "desc": "多推出 30% 功能" }] },
      "punch": "推出功能的速度，堪比十倍人力的組織" }
  ]
}
```

### Step 2 — 指派頁型

| 頁型 `type` | 用在 | 結構 |
|---|---|---|
| `cover` | 開場／總覽 | 大標＋雙語副標；左清單、右數字；底部金句 |
| `numbers` | 數字牆 | 2×2 數字方格＋底部名單條 |
| `contrast` | 前後對比 | 左「過去」右「現在」＋中間箭頭寫轉變機制＋引言 |
| `panels` | 拆解（**最常用**） | 2×3 或 3 欄面板網格，每格＝一個子概念 |
| `checklist` | 收尾核對 | 編號條列＋下一步區塊＋全篇金句 |

**成套建議**：`cover` 開場 → `numbers` 放數字 → `panels` 撐主體 → `checklist` 收尾。
**單張場景**（多數工作用途）：直接用 `panels`。

### Step 3 — 渲染

```bash
bash assets/fonts.sh                    # 首次執行：裝 Iansui 手寫字體
python3 scripts/build.py content.json out/   # JSON → HTML
python3 scripts/shot.py out/                 # HTML → PNG（1080×1080）
```

### Step 4 — 自檢（看圖，不是看碼）

**必須實際 Read 產出的 PNG 檢查**，不可只看程式跑完就交件：

- [ ] 有無文字溢出／被框線切到
- [ ] 每格要點數與字數是否守住 ≤4／≤20
- [ ] 橘色元素是否 ≤3 處
- [ ] 中文字是否清晰（若糊 → SVG 濾鏡誤套到文字層，見下方「常見錯誤」）
- [ ] 頁碼未與內容重疊
- [ ] 頁尾出處齊全

### Step 5 — 落檔

PNG 與 `content.json` 一起存。改版時**改 JSON 重跑**，不重畫。

---

## 設計系統（改動前先讀 `references/design-spec.md`）

```
--ink    #1B4A2B   深森綠：框線／標題／圖示
--ink-2  #3C7A50   中綠：頁尾／英文小字
--accent #E0491F   朱橘：數字／金句／標籤（唯一暖色）
--body   #1C1C1A   內文黑
--panel  #EAF2E3   淺薄荷綠：面板底
--paper  #FCFCF8   紙白：背景
```

畫布 1080×1080；外距 上52/左右40/下30；框線 3px；圓角**四角不等值**（手繪不對稱）。

字體：`Iansui`（芫荽，SIL OFL，繁體手寫體，CJK＋拉丁一套吃下）→ fallback `Noto Sans CJK TC`。

---

## 常見錯誤（都踩過）

| 症狀 | 原因 | 修法 |
|---|---|---|
| **中文字糊掉、筆畫黏連** | SVG 位移濾鏡套在整個容器上 | 每個區塊拆兩層：絕對定位的 `.ink`（只有 border，套濾鏡）＋上層 `.c`（放內容，不套） |
| 圖示與整體風格違和 | 用了 emoji（渲染成彩色系統字） | 一律用 `assets/icons.svg` 的單線 SVG symbol（`fill:none; stroke:currentColor`） |
| 頁碼壓到內容 | 卡片 padding-top 不足 | `padding-top ≥ 52px` |
| 框線看起來像「沒調好的圓角」 | 濾鏡 `scale` 太小 | `scale` 用 6.5（4 太拘謹、>9 變波浪） |
| 字體沒生效 | 沒跑 `fc-cache`／從 raw.githubusercontent 抓（會 403） | 走 GitHub **Releases** 直連，裝完 `fc-cache -f` |
| 十張風格飄移 | 每張各寫一份 CSS | 全部共用 `assets/card.css`，卡片只放內容 |

---

## 內容紀律（讓卡好讀的真正原因）

1. **雙語只做在術語層**：主標／小標中英並列，內文純中文。全文雙語會爆版。
2. **底部金句要能獨立轉發**——這張卡被單獨截圖轉出去時，只有它會被讀到。
3. **一張卡一個論點**。想放兩個就是兩張卡。

---

## 檔案

```
assets/card.css        設計系統
assets/icons.svg       手繪風單線圖示庫（用 <use href="#i-xxx"/> 引用）
assets/fonts.sh        Iansui 下載安裝
scripts/build.py       content.json → HTML（五種頁型）
scripts/shot.py        Playwright 批次截圖
references/design-spec.md    完整版面／配色／內容文法
references/content-schema.md content.json 欄位定義
examples/              範例 content.json 與成品
```
