# bookmarks

極簡個人書籤 / 書櫃。整頁無標題、無 bar、無提示，只有封面卡片 + 一個 `＋` 加卡。

`t-rec` 工具箱成員（原 `exe-rec/b/`，曾用名 BMK）。

## 怎麼用

雙擊 `rituals/自動localhost.command`（port 9092），或走工具箱 hub `t-rec/rituals/`（9090）。
**固定用同一個入口**——localStorage 綁 origin，換入口等於換一台機器。

> ### 開起來一片全白？（2026-08-07 已修）
>
> 原因是兩件事疊在一起，都不是搬遷搬壞的：
>
> 1. **空狀態的設計就是全白。** 原本 `.add-icon { opacity: 0 }` —— 加卡的 `＋` 完全隱形，
>    要把游標移到**左上角第一格**才浮到 `opacity: 0.1`。
>    在 `exe.rec.ooo/b/` 上一直有卡片，所以真正的空狀態從沒被看見過。
> 2. **舊書籤沒跟著搬。** 資料原本存在 `https://exe.rec.ooo` 這個 origin 下；
>    localStorage **不會跟著檔案移動**，搬到本機必然是從零開始 —— 於是第 1 點被觸發。
>
> **已修**：加了空狀態逃生口。
>
> ```css
> .add:only-child .add-icon { opacity: 0.22; }
> ```
>
> 一張卡都沒有時 `.add` 是 `#grid` 的唯一子元素，`＋` 直接可見；
> 有卡片之後自動回到原本的 ambient 行為（預設隱形、hover 才浮現）。
> **ambient 設計本身沒被改掉，只是補了零卡片這個邊界。**
>
> **想救舊資料**：趁 GitHub Pages 還沒重新部署，去 `https://exe.rec.ooo/b/` 開 DevTools 執行
> `copy(localStorage["bmk-cards-v1"])`，再到本機同一 key 貼回去。這件事有時效性。

### 操作

- `＋`：新增一張卡
- 點封面：上傳圖片（自動置中裁成 4:5、壓成 JPEG 存進 localStorage）
- 空封面點中間 emoji：循環切換 📕📗📘📙📚📖
- 膠囊第一行：書名；第二行：進度 / 註記（accent 色）
- hover 卡片右上 `✕`：刪除（無 confirm）
- hover 卡片右上 `🔗`：開連結；`✏️`：改連結（就地展開第三行輸入框）

## 設計

- **accent**：`--t-accent: #0000ff` — t-rec 工具箱共用動詞色（進度文字、連結輸入框）。
  原專案的 `--bmk-red #e2402f` 與 `#1a6fd4` 藍已移除。**不得引入第二個強調色。**
- **無 favicon**：t-rec 工具不掛個體 emoji / icon（原 🔖 已刪）
- **加卡鈕**：`＋`（與 `../notes/` 工具列一致；原 🔖 品牌標記已換掉）
- 卡片內的 📕📗📘 / 🔗 / ✏️ 是**功能性符號**（狀態切換、動作按鈕），不是品牌標記，保留。

## 儲存

唯一 source of truth：`localStorage["bmk-cards-v1"]`
= `[{ id, title, note, cover, emoji, link }]`

> key 名 `bmk-*` 是 legacy，**刻意不改** —— 換 key 會讓既有書籤全部消失。

沒有後端、沒有 sync、沒有外部依賴。封面圖以 dataURL 內嵌，注意 localStorage 容量上限。

## 不做的事
- 資料夾 / tag / 排序（純扁平 grid）
- 自動抓 favicon / og:image（封面手動上傳）
- 雲端 sync
- 自有域名 / 自有品牌（t-rec 成員一律不獨立掛名，見 `../README.md`）

## 遷移註記（2026-08-07）

- 從 `exe-rec/b/` 移出；`exe-rec/b.html`（轉址頁）與 `exe-rec/index.html` 的 `/b$` 導向 script、`b/` 導鏈皆已刪除。
- 舊網址 `https://exe.rec.ooo/b/` 自此失效（無轉址）。這是刻意的：t-rec 成員不繼承 exe-rec 的個人服務命名空間。
