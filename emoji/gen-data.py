#!/usr/bin/env python3
"""t-rec/emoji: 重生 data.js.

來源(都是公開資料, 跑的時候現抓):
  - Unicode emoji-test.txt (latest)      -> 全部 fully-qualified emoji, 分組, 英文名
  - CLDR annotations + annotationsDerived (en / zh-Hant / ja) -> 搜尋關鍵字

用法:
  python3 gen-data.py                 # 現抓, 寫 data.js
  python3 gen-data.py --src DIR       # DIR 裡已有 emoji-test.txt, ann-<l>.json, der-<l>.json 就不抓

膚色: 同一個 base 的五個單一膚色版本收進那一筆的第 4 欄(頁面右上 ✋ 切換);
混合膚色(兩個人不同膚色)不收. Component 組(膚色 / 髮型色塊本身)不收.
新 Unicode 版本出來重跑一次即可; CLDR 版本號改下面 CLDR.
"""
import json, os, re, sys, urllib.request

CLDR = "48.2.0"
LANGS = ["en", "zh-Hant", "ja"]
URLS = {
    "emoji-test.txt": "https://unicode.org/Public/emoji/latest/emoji-test.txt",
    **{f"ann-{l}.json": f"https://cdn.jsdelivr.net/npm/cldr-annotations-full@{CLDR}/annotations/{l}/annotations.json" for l in LANGS},
    **{f"der-{l}.json": f"https://cdn.jsdelivr.net/npm/cldr-annotations-derived-full@{CLDR}/annotationsDerived/{l}/annotations.json" for l in LANGS},
}
TONES = ["1F3FB", "1F3FC", "1F3FD", "1F3FE", "1F3FF"]
TONE_CH = {chr(int(t, 16)) for t in TONES}
ICONS = {  # 分組列的那顆臉(手挑, 比各組第一顆好認)
    "Smileys & Emotion": "😀", "People & Body": "👋", "Animals & Nature": "🐻",
    "Food & Drink": "🍔", "Travel & Places": "🚗", "Activities": "⚽",
    "Objects": "💡", "Symbols": "❤️", "Flags": "🏁",
}


def read(src, name):
    p = os.path.join(src, name) if src else None
    if p and os.path.exists(p):
        return open(p, encoding="utf-8").read()
    with urllib.request.urlopen(URLS[name], timeout=60) as r:
        return r.read().decode("utf-8")


def key(s):
    """CLDR 的鍵不帶 FE0F; 膚色對回 base 也用這個."""
    return s.replace("️", "")


def main():
    src = sys.argv[sys.argv.index("--src") + 1] if "--src" in sys.argv else None
    test = read(src, "emoji-test.txt")
    version = re.search(r"^# Version: ([\d.]+)", test, re.M).group(1)

    ann = {}
    for l in LANGS:
        a = json.loads(read(src, f"ann-{l}.json"))["annotations"]["annotations"]
        d = json.loads(read(src, f"der-{l}.json"))["annotationsDerived"]["annotations"]
        ann[l] = {key(k): v for k, v in {**d, **a}.items()}

    groups, group = [], None
    base_at = {}  # key(base) -> 那一筆
    toned = []
    for line in test.splitlines():
        m = re.match(r"^# group: (.+)$", line)
        if m:
            group = None if m.group(1) == "Component" else {"n": m.group(1), "i": ICONS.get(m.group(1), ""), "e": []}
            if group:
                groups.append(group)
            continue
        m = re.match(r"^([0-9A-F ]+?)\s*; fully-qualified\s*# \S+ E[\d.]+ (.+)$", line)
        if not m or group is None:
            continue
        cps, name = m.group(1).split(), m.group(2)
        ch = "".join(chr(int(c, 16)) for c in cps)
        tones = [c for c in cps if c in TONES]
        if tones:
            toned.append((ch, tones))
            continue
        words = []
        for l in LANGS:
            v = ann[l].get(key(ch), {})
            words += v.get("tts", []) + v.get("default", [])
        seen, kw = set(), []
        for w in words:
            w = w.strip().lower()
            if w and w not in seen and w != name.lower():
                seen.add(w)
                kw.append(w)
        item = [ch, name, "|".join(kw)]
        group["e"].append(item)
        base_at[key(ch)] = item

    lost = 0
    for ch, tones in toned:
        if len(set(tones)) != 1:  # 混合膚色不收
            continue
        b = base_at.get(key("".join(c for c in ch if c not in TONE_CH)))
        if b is None:
            lost += 1
            continue
        if len(b) == 3:
            b.append([None] * 5)
        b[3][TONES.index(tones[0])] = ch
    for g in groups:
        for it in g["e"]:
            if len(it) == 4 and None in it[3]:
                it[3] = [x or it[0] for x in it[3]]

    n = sum(len(g["e"]) for g in groups)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"// 產物, 不要手改. gen-data.py 從 Unicode emoji-test {version} + CLDR {CLDR} annotations (en / zh-Hant / ja) 生成.\n")
        f.write("// [字, 英文名, 搜尋字(| 分隔, 小寫, 不含英文名), 五個膚色版本?]\n")
        f.write("window.EMOJI = " + json.dumps({"v": version, "g": groups}, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(f"emoji {version}: {n} 筆 / {len(groups)} 組 / 膚色 {sum(1 for g in groups for it in g['e'] if len(it) == 4)} 筆有; 對不回 base {lost}; {os.path.getsize(out)//1024} KB -> {out}")


if __name__ == "__main__":
    main()
