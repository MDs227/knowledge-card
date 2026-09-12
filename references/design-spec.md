# 設計規格（改 CSS 前先讀）

## 畫布與版面
| 項目 | 值 |
|---|---|
| 畫布 | 1080 × 1080（1:1）。要 IG 直式改 1080×1350，其餘不變 |
| 外距 | 上 52 / 左右 40 / 下 30 px（上緣要留給頁碼與 chip） |
| 區塊圓角 | **四角不等值** `26px 22px 28px 20px` — 對稱圓角會立刻失去手繪感 |
| 框線 | 3px 實線，`--ink` |
| 區塊間距 | 16–20px |

## 配色（六色，不要加第七色）
```
--ink    #1B4A2B  深森綠：框線／標題／圖示
--ink-2  #3C7A50  中綠：頁尾／英文小字
--accent #E0491F  朱橘：唯一暖色
--body   #1C1C1A  內文黑
--panel  #EAF2E3  面板底
--paper  #FCFCF8  背景（不要用純白 #FFF，會太刺）
--dot    #9DBBA4  虛線分隔
```
**朱橘每張 ≤3 處**：原則標籤 chip、關鍵數字、底部金句。多了就亂。

## 字級階梯
| 角色 | px |
|---|---|
| 封面主標 h1 | 66 |
| 內頁主標 h2 | 52 |
| 面板標題 .hdr | 38 |
| 底部金句 .punch | 38 |
| 清單主字 .ptxt | 32 |
| 大數字 .val | 58 |
| 內文要點 .bul | 25 |
| 英文小標 / 名單 | 21–23 |
| 頁尾出處 | 22 |

## 字體
`Iansui`（芫荽，SIL OFL）→ `Noto Sans CJK TC` → sans-serif。
一套字體同時吃 CJK 與拉丁，**不要混排兩套**（原圖的一致感來自這裡）。
安裝走 GitHub **Releases**（`raw.githubusercontent.com` 在沙箱常 403）。

## 手繪感
```html
<filter id="rough">
  <feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="3" seed="N"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6.5"
      xChannelSelector="R" yChannelSelector="G"/>
</filter>
```
- **只套在 `.ink`（純 border 的絕對定位層），絕不套在含文字的元素上。**
- `scale`：4 太拘謹｜6.5 對｜>9 變波浪。
- 每張卡用不同 `seed`（build.py 依序號算），避免十張的抖動長得一模一樣。

## 圖示
- 一律 `assets/icons.svg` 的 symbol，`fill:none; stroke:currentColor; stroke-width:2.4; stroke-linecap:round; stroke-linejoin:round`，viewBox `0 0 48 48`。
- `currentColor` 讓同一個圖示能在綠色與橘色語境重用。
- **禁用 emoji**（會渲染成彩色系統字，與線條風格互斥）。
- 現有 24 個：rocket gear verify bricks cycle bulb shield bug doc db chart pie clock warn check people server plug mic tools arrow gate code flask。缺的自己畫，畫完存回 icons.svg，不要 inline 在單張卡裡。

## 已知未解
- 麥克筆的**粗細變化與微雙線**尚未重現（目前抖動偏均勻）。可嘗試疊兩層 `.ink` 錯開 1px＋不同 seed。
