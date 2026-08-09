# notes

簡單記事本。寫作、自動儲存、一鍵匯出 / 匯入全部記事為單個 `.md` 檔。

`t-rec` 工具箱成員（原 `CommonLibrary/memo-rec`）。

## 怎麼用

雙擊 `index.html`、或本地 server：`python3 -m http.server 8000`

### 兩種版式（右上角切換鈕）

按鈕顯示的是**切過去會變成的版式**，不是當前版式（同 b-rec `.view-toggle` 慣例）。

| 鈕 | 切到 | 樣子 |
|---|---|---|
| `⇊` | **flow**（流式瀑布） | 所有記事一次攤開成卡片，CSS `columns` masonry。sidebar 收起讓出整片畫布 |
| `≡` | **editor**（單筆編輯） | 280px sidebar + 置中 800px 編輯欄 |

版式記在 `localStorage["notes.view.v1"]`。

**flow 檢視的互動**

- 卡片右下角 `＋` / `−`：收放全文。折合時只顯示前 **140 字**（`COLLAPSE_CHARS`）+ `…`；
  未超過 140 字的卡片**不長出這個鈕**。展開狀態只存記憶體，重載即全部收回。
- 點卡片本體：選中該筆並跳回 editor。
- 左上角**無框的 `＋` 格**：新增一筆並跳進 editor。（有內容的卡片是 1px 直角框，
  新增格無框 —— 靠這個差異區分「內容」與「動作」。）

### 互動（editor 檢視）
- `＋` / `n` 鍵：新建記事
- **無記事時自動建立一份空白記事**（永遠至少一份、刪到空也會自動補）
- 點 sidebar 條目：切換
- 直接在右側 textarea 寫作、停止 400ms 自動存
- hover 條目顯示 `×`、點刪除（無 confirm）
- `e` 鍵：匯出全部記事為 `notes-export-YYYY-MM-DD.md`
- `i` 鍵：選 `.md` / `.json` 檔匯入（merge by id）
- 工具列 search：跨記事內文搜尋

### 匯出格式（單檔 `.md`、含 YAML frontmatter）

```markdown
---
id: m-abc123
updated: 2026-06-01T03:00:00.000Z
---
記事內容
多行可以

---
id: m-def456
updated: 2026-06-01T04:15:00.000Z
---
另一筆
```

可貼進 Obsidian / VSCode / 任何 markdown 工具讀。

## 設計

**前端對齊 b-rec / lib-rec 家族語言**（2026-08-08 重做）。骨架與 token 命名同源：

| 項 | 值 |
|---|---|
| 正文字體 | `-apple-system, "Segoe UI", "PingFang TC", sans-serif`（**非等寬**） |
| line-height | `1.6` |
| token | `--bg` `--fg` `--accent` `--muted` `--line` `--sb-w` `--content-w` |
| sidebar | fixed 280px、`border-right: 1px solid var(--line)`、`translateX` 開合 |
| sidebar toggle | 左緣 `❯` / `❮`（同 lib-rec `.summary-toggle`），狀態記在 `notes.sidebar.v1` |
| view toggle | 右上 `≡` / `⇊`（同 b-rec `.view-toggle`），狀態記在 `notes.view.v1` |
| flow 卡片 | 1px 直角框、無圓角無陰影（維持 b-rec 方框感）；hover / active 邊框轉 accent |
| 內容欄 | 置中 `max-width: 800px`、`padding: 3rem 2rem 4rem` |
| search | 無邊框、accent 淡底，hover（desktop）/ focus（mobile）加深 |
| scroll | `scroll-behavior: auto` —— 不要平滑 |

### 代表色

`--accent: #00ff5e`（notes 系統綠）。同家族：b-rec 系統藍 `#0000ff`、lib-rec 系統紅 `#fc036b`。

> ⚠️ **`#00ff5e` 在白底上對比只有 1.36:1，不能拿來寫字。**
> 所以家族語言中「accent 當文字色」的位置（sidebar hover / active），
> 這裡一律改成 **accent 當底、黑字**（對比 15.47:1）。
> 仍是**單一強調色**，沒有引入第二色；淡底 `rgba(0,255,94,.14/.26)` 是同色 tint。

其餘用法：`caret-color`、`::selection`、`＋` / `×` / 卡片 `＋` `−` 的 hover 底色、
flow 卡片 hover 與 active 的**邊框色**（1px 線不需文字級對比，直接用 accent 沒問題）。

### 其他

- **無底部 status bar**（2026-08-08 移除）。原本顯示 notes / words / chars 計數與 `saved 1m ago`——
  對一個記事本沒有決策價值，純噪音。自動儲存靜默進行。
- **ambient `×`**：刪除鈕預設 `opacity: 0`，hover 條目才出現。
- **無 favicon**：t-rec 工具不掛個體 emoji / icon。
- **routing**：無 hash routing（不切頁；兩種版式靠 body class 切換）。
- **flow 排版零 JS**：用 CSS `columns: 250px` 做 masonry，卡片 `break-inside: avoid`。
  不引入 masonry library，也不自己算欄高。
- **空狀態**：永遠至少一份筆記，刪到空會自動補一份 —— 這同時是空狀態逃生口。

## 儲存

唯一 source of truth：`localStorage.memo.notes.v1` = `[{ id, content, updatedAt }]`

> key 名 `memo.*` 是 legacy，**刻意不改** —— 換 key 會讓既有記事全部消失。
> 這是「內部識別碼」不是「品牌」，不在去品牌化範圍內。

沒有後端、沒有 sync、沒有外部依賴。

## 不做的事
- markdown render preview（保留純文字）
- tag / 分類 / folder（純扁平 list、search 解決）
- rich text / 字體 toggle
- 雲端 sync / 多裝置（匯出檔自己搬）
- confirm 對話框（無 toast、無彈窗）
- 自有域名 / 自有品牌（t-rec 成員一律不獨立掛名，見 `../README.md`）
