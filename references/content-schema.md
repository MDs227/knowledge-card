# content.json 欄位定義

```jsonc
{
  "meta": {
    "source": "Claude 官方 blog",   // 必填，進頁尾
    "author": "Michael Segner",     // 選填
    "date":   "2026.08.20",         // 選填
    "total":  10                     // 選填；未填則用 cards 長度（做「1/10」時手動指定）
  },
  "cards": [ /* 每張一個物件，見下 */ ]
}
```

## 所有頁型共用欄位
| 欄位 | 說明 |
|---|---|
| `type` | `cover` \| `numbers` \| `contrast` \| `panels` \| `checklist` |
| `chip` | 左上橘色標籤，如 `"原則3"`（選填） |
| `title` | 主標 |
| `subEn` | 英文副標 |
| `thesis` | 標題下的一句話論點（橘色，選填） |
| `punch` | 底部金句（橘色）— **要能獨立轉發** |
| `punchIcon` | 金句圖示，預設 `bulb` |

## `cover`
```jsonc
{ "type":"cover", "title":"", "subCn":"", "subEn":"", "note":"",
  "list": { "heading":"五大原則", "headingEn":"5 Principles",
            "items":[{"icon":"rocket","cn":"人人都能發布","en":"Everyone ships"}] },
  "stats":{ "heading":"亮眼數字",
            "items":[{"icon":"chart","name":"ClickHouse","desc":"多推出 30% 功能"}] } }
```
`list.items` 建議 4–6 條；`stats.items` 2–3 條。

## `numbers`
```jsonc
{ "type":"numbers",
  "items":[{"icon":"db","name":"ClickHouse","value":"+30%","desc":"多推出 30% 的功能"}],
  "strip":{ "icon":"people","heading":"受訪公司 / 15 startups","text":"A・B・C…" } }
```
`items` **正好 4 個**（2×2）。`strip` 選填。

## `contrast`
```jsonc
{ "type":"contrast",
  "before":{ "heading":"過去：傳話遊戲","headingEn":"Telephone game","items":["…","…"] },
  "after" :{ "heading":"現在：直接發布","headingEn":"Publish it yourself","items":["…"] },
  "arrow" : "Claude Code 壓縮這條鏈",
  "quote" :{ "text":"…","by":"Ryan Daniels，Crosby CEO" } }
```

## `panels`（最常用）
```jsonc
{ "type":"panels", "cols":2,
  "panels":[{ "icon":"doc","heading":"CLAUDE.md 不變量","headingEn":"",
              "items":["≤20 字一條","最多 4 條"], "src":"Zingage" }],
  "quote":{ "text":"…","by":"…" } }
```
`cols` 未填時：>4 格用 3 欄，否則 2 欄。**4 格用 2 欄、6 格用 3 欄**最穩。
`src` 是該格的來源標註（橘色小字，靠底）。

## `checklist`
```jsonc
{ "type":"checklist",
  "items":[{ "icon":"rocket","heading":"人人都能發布","text":"一到兩行" }],
  "links":{ "icon":"code","items":["url（說明）","url（說明）"] } }
```
`items` 建議 5 條；超過 6 條會擠。

## 硬性上限（超過就拆卡）
- 每格要點 ≤ 4 條，每條 ≤ 20 字
- `panels` 每張 ≤ 6 格
- `checklist` 每張 ≤ 6 條
- 橘色元素每張 ≤ 3 處
