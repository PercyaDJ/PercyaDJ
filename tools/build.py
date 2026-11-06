#!/usr/bin/env python3
"""Generate every image of the profile README and both README files.

    pip install fonttools brotli
    python3 tools/build.py

Outputs:
  assets/**            static images (header, sections, artworks), dark and light
  assets/live-src/     every state of the "now" frame, copied to the `live` branch
                       by .github/workflows/now-frame.yml
  README.md, README.fr.md
Texts live in tools/content.py. Edit them there, then run this script again.
"""
import base64
import html
import io
import math
import os
import re
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.dirname(__file__))
from content import (BUTTON_MAIL, CONTACT, HEADINGS, HOURS, LINKEDIN, NOW_PREFIX, NOWTXT, OWNER,  # noqa: E402
                     PROJECTS, RESERVE, SIGNS, SIGNS_HINT, TALK, TEXTS, TITLE)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "src")
OUT = os.path.join(ROOT, "assets")
LIVE_URL = f"https://raw.githubusercontent.com/{OWNER}/{OWNER}/live"
LANGS = ("en", "fr")
THEMES = ("dark", "light")
SLOTS = (8, 10, 14, 18, 22, 0)

SORA = "Sora"
MONO = "JetBrains Mono"
FONT_FILES = {SORA: "Sora.woff2", MONO: "JetBrainsMono.woff2"}

# GitHub page colours (text drawn straight on the README background)
GH = {
    "dark": {"fg": "#e6edf3", "muted": "#9198a1"},
    "light": {"fg": "#1f2328", "muted": "#59636e"},
}
# artwork palette
P = {
    "dark": dict(mat="#0f171a", panel="#152125", ink="#e7f2f1", sub="#9ab3b3", line="#24373a", bar="#24373a",
                 accent="#4fd1c5", alert="#ff7a66", ok="#56d38a", violet="#9b8cff", amber="#f0b84a"),
    "light": dict(mat="#f3f6f6", panel="#ffffff", ink="#13292a", sub="#5b7172", line="#d7e2e2", bar="#dbe5e5",
                  accent="#0b8a84", alert="#d64f3c", ok="#2e9d62", violet="#6a5bd6", amber="#c98a12"),
}

ANIM_CSS = """
@keyframes scan{0%{transform:translateY(0)}60%,100%{transform:translateY(230px)}}
@keyframes rowIn{0%,30%{opacity:0;transform:translateX(-14px)}38%,92%{opacity:1;transform:none}100%{opacity:0}}
@keyframes wave{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}
@keyframes lineIn{0%{opacity:0;clip-path:inset(0 100% 0 0)}12%{opacity:1;clip-path:inset(0 0 0 0)}88%{opacity:1}100%{opacity:0}}
@keyframes thumb{0%,44%{opacity:0;transform:translateY(8px)}50%,92%{opacity:1;transform:none}100%{opacity:0}}
@keyframes fall{0%{opacity:0;transform:translateY(-60px)}12%{opacity:1;transform:translateY(0)}40%{opacity:1;transform:translate(var(--dx),40px) scale(.4)}46%,100%{opacity:0;transform:translate(var(--dx),40px) scale(.4)}}
@keyframes fillIn{0%,42%{opacity:0}50%,92%{opacity:1}100%{opacity:0}}
@keyframes grow{0%,44%{transform:scaleX(0)}56%,92%{transform:scaleX(1)}100%{transform:scaleX(0)}}
@keyframes mail{0%,62%{opacity:0;transform:translate(0,0)}68%{opacity:1}86%{opacity:1;transform:translate(70px,-26px)}92%,100%{opacity:0;transform:translate(90px,-34px)}}
@keyframes split{0%,15%{transform:translateX(0)}45%,60%{transform:translateX(170px)}90%,100%{transform:translateX(0)}}
@keyframes tagIn{0%,20%{opacity:0;transform:translateY(6px)}28%,90%{opacity:1;transform:none}100%{opacity:0}}
@keyframes pulse{0%,100%{opacity:.5}50%{opacity:1}}
.scanbeam{animation:scan 6s cubic-bezier(.5,0,.5,1) infinite}
.row{opacity:0;animation:rowIn 6s infinite}
.wv{transform-box:fill-box;transform-origin:center;animation:wave 1.1s ease-in-out infinite}
.tl{opacity:0;animation:lineIn 9s infinite}
.th{opacity:0;animation:thumb 9s infinite}
.csv{opacity:0;animation:fall 7s cubic-bezier(.4,0,.3,1) infinite}
.fi{opacity:0;animation:fillIn 7s infinite}
.gr{transform-box:fill-box;transform-origin:left;animation:grow 7s infinite}
.ml{opacity:0;animation:mail 7s infinite}
.splitl{animation:split 8s ease-in-out infinite}
.tg{opacity:0;animation:tagIn 8s infinite}
.pu{animation:pulse 2s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){
 .scanbeam,.wv,.csv,.gr,.ml,.splitl,.pu{animation:none}
 .row,.tl,.th,.fi,.tg{animation:none;opacity:1}.csv,.ml{opacity:0}
}
"""

_font_cache = {}


def esc(t):
    return html.escape(str(t), quote=True)


def font_face(family, chars):
    key = (family, chars)
    if key not in _font_cache:
        font = TTFont(os.path.join(SRC, FONT_FILES[family]))
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt"]
        opts.name_IDs = ["*"]
        sub = subset.Subsetter(opts)
        sub.populate(text=chars + " ")
        sub.subset(font)
        font["head"].modified = font["head"].created  # keep the output identical from one build to the next
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.recalcTimestamp = False
        font.save(buf)
        data = base64.b64encode(buf.getvalue()).decode()
        _font_cache[key] = (f"@font-face{{font-family:'{family}';font-weight:100 900;"
                            f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return _font_cache[key]


def T(x, y, text, size=12, fill="#000", weight=400, family=MONO, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{extra}>{esc(text)}</text>')


def svg(view_w, view_h, label, body, css="", vy=0):
    """Wrap a body in an <svg>, embedding subsets of the fonts it uses."""
    faces = []
    for family in (SORA, MONO):
        texts = re.findall(rf'font-family="{family}"[^>]*>([^<]*)<', body)
        if texts:
            chars = "".join(sorted(set(html.unescape("".join(texts)))))
            faces.append(font_face(family, chars))
    style = "".join(faces) + css
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 {vy} {view_w} {view_h}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title><style>{style}</style>{body}</svg>')


def jpeg(name):
    with open(os.path.join(SRC, name), "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def write(path, data):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(data)


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split(" "):
        if len((cur + " " + word).strip()) > width:
            lines.append(cur.strip())
            cur = word
        else:
            cur += " " + word
    if cur.strip():
        lines.append(cur.strip())
    return lines


def tr(pair, lang):
    return pair[0] if lang == "en" else pair[1]


# ---------------------------------------------------------------- header
def banner(lang, theme):
    c = GH[theme]
    body = (T(2, 62, "Jolan D.", 58, c["fg"], 800, SORA, ' letter-spacing="-2"') +
            T(4, 98, tr(TITLE, lang), 19, c["fg"], 300, SORA))
    return svg(640, 112, "Jolan D. " + tr(TITLE, lang), body)


def lang_pill(lang):
    on, off = ("EN", "FR") if lang == "en" else ("FR", "EN")
    # active language drawn filled, the other one outlined; the whole pill links to the other README
    left, right = ("EN", "FR")
    body = (f'<rect x="1" y="1" width="86" height="26" rx="7" fill="none" stroke="#8b949e" stroke-opacity=".6"/>'
            f'<rect x="{1 if lang == "en" else 44}" y="1" width="43" height="26" rx="7" fill="#0b8a84"/>' +
            T(13, 19, left, 12.5, "#ffffff" if lang == "en" else "#8b949e", 600, SORA) +
            T(56, 19, right, 12.5, "#ffffff" if lang == "fr" else "#8b949e", 600, SORA))
    label = "English version (current) / Version française" if lang == "en" else "Version française (actuelle) / English version"
    return svg(88, 28, label, body)


def btn_mail(lang):
    text = tr(BUTTON_MAIL, lang)
    w = 132
    body = (f'<rect width="{w}" height="32" rx="16" fill="#0b8a84"/>'
            '<rect x="14" y="10" width="16" height="12" rx="2" fill="none" stroke="#fff" stroke-width="1.8"/>'
            '<path d="M14 12 l8 5.5 8 -5.5" fill="none" stroke="#fff" stroke-width="1.8"/>' +
            T(38, 20.5, text, 12, "#ffffff", 600, SORA))
    return svg(w, 32, text, body)


def btn_linkedin():
    body = ('<rect width="100" height="32" rx="16" fill="#0a66c2"/>'
            '<rect x="13" y="8" width="16" height="16" rx="3" fill="#fff"/>'
            '<path d="M16.6 13.4h2.3v7h-2.3zM17.75 10.2a1.3 1.3 0 1 1 0 2.6 1.3 1.3 0 0 1 0-2.6zM20.3 13.4h2.2v1c.3-.6 1.1-1.2 2.2-1.2 2.3 0 2.7 1.5 2.7 3.5v3.7h-2.3v-3.3c0-.8 0-1.8-1.1-1.8s-1.3.9-1.3 1.8v3.3h-2.4z" fill="#0a66c2"/>' +
            T(36, 20.5, "LinkedIn", 12, "#ffffff", 600, SORA))
    return svg(100, 32, "LinkedIn", body)


def nowline(slot, lang, theme):
    c = GH[theme]
    text = tr(NOW_PREFIX, lang) + tr(NOWTXT[slot], lang)
    body = (f'<circle class="pu" cx="8" cy="15" r="5" fill="#e5484d"/>' + T(22, 20, text, 14, c["muted"], 400, MONO))
    return svg(1000, 30, text, body, ANIM_CSS)


def slice_svg(i, lang, now):
    h = HOURS[i]
    proj = tr(h["proj"], lang)
    body = (f'<image href="{jpeg(f"slice-{i}.jpg")}" width="360" height="720"/>'
            '<rect y="590" width="360" height="130" fill="#000" opacity=".42"/>' +
            T(28, 646, h["label"], 36, "#ffffff", 600, MONO) + T(28, 690, proj, 30, "#e9f1f5", 400, SORA))
    if i < 4:
        body += '<rect x="357" y="0" width="3" height="720" fill="#fff" opacity=".55"/>'
    if now:
        word = "NOW" if lang == "en" else "MAINTENANT"
        pill_w = 150 if lang == "en" else 288
        body += (f'<rect x="7" y="7" width="346" height="706" fill="none" stroke="#fff" stroke-width="10" rx="6"/>'
                 f'<rect x="36" y="34" width="{pill_w}" height="66" rx="33" fill="#fff"/>'
                 f'<circle class="pu" cx="76" cy="67" r="12" fill="#e5484d"/>' +
                 T(100, 79, word, 32, "#10262a", 600, MONO))
    label = f'{h["label"]} · {proj}' + (" · " + ("now" if lang == "en" else "maintenant") if now else "")
    return svg(360, 720, label, body, ANIM_CSS)


def signs(lang, theme):
    c = GH[theme]
    pos = [dict(x=12, y=12, r=4, d=1), dict(x=318, y=22, r=-2, d=-1), dict(x=624, y=12, r=3.5, d=1)]
    out = ""
    for p, s in zip(pos, SIGNS):
        t, sub = tr(s["title"], lang), tr(s["sub"], lang)
        w, h, x, y = 258, 52, p["x"], p["y"]
        cy = y + h / 2
        if p["d"] > 0:
            path = f"M{x} {y} H{x + w - 26} L{x + w} {cy} L{x + w - 26} {y + h} H{x} Z"
            tx, mx = x + 52, x + 26
        else:
            path = f"M{x + 26} {y} H{x + w} V{y + h} H{x + 26} L{x} {cy} Z"
            tx, mx = x + 74, x + 48
        out += (f'<g transform="rotate({p["r"]} {x + w / 2} {cy})">'
                f'<path d="{path}" fill="#f6f4ef" stroke="#d2232a" stroke-width="3.2"/>'
                f'<g transform="translate({mx} {cy})"><rect x="-11" y="-11" width="22" height="22" fill="#fff" stroke="#d2232a" stroke-width="1.6"/>'
                f'<path d="M-7.5 -6 H7.5 M0 -6 V8.5" stroke="#d2232a" stroke-width="4"/></g>' +
                T(tx, cy - 2, t, 18, "#1b1b1b", 700, SORA) + T(tx, cy + 15, sub, 11, "#5b5b5b", 400, MONO) + "</g>")
    hint = tr(SIGNS_HINT, lang)
    out += (f'<text x="450" y="106" text-anchor="middle" font-family="{MONO}" font-size="12.5" '
            f'fill="{c["muted"]}">{esc(hint)}</text>')
    label = ", ".join(tr(s["title"], lang) for s in SIGNS) + ". " + hint
    return svg(900, 112, label, out)


# ---------------------------------------------------------------- sections
def card(colors, label, title, tag, text, theme):
    """Section text: time pill and label, title, tag, then the description wrapped to fit beside the scene."""
    c = GH[theme]
    stops = "".join(f'<stop offset="{k / (len(colors) - 1)}" stop-color="{col}"/>' for k, col in enumerate(colors))
    lines = wrap(text, 54)
    h = 104 + (len(lines) - 1) * 23 + 12
    body = (f'<defs><linearGradient id="g" x1="0" x2="1">{stops}</linearGradient></defs>'
            f'<rect x="0" y="6" width="40" height="18" rx="9" fill="url(#g)"/>' +
            T(50, 21, label, 14, c["muted"], 600, MONO) +
            T(0, 56, title, 22, c["fg"], 700, SORA) + T(0, 78, tag, 12.5, c["muted"], 400, MONO))
    body += "".join(T(0, 104 + k * 23, l, 14.5, c["fg"], 300, SORA) for k, l in enumerate(lines))
    return svg(440, h, f"{label}. {title}. {tag}. {text}", body)


def project_card(key, lang, theme):
    h = next(x for x in HOURS if x["key"] == key)
    d = PROJECTS[key]
    return card(h["colors"], f'{h["label"]} · {tr(h["what"], lang)}', tr(d["title"], lang), tr(d["tag"], lang),
                tr(d["text"], lang), theme)


def reserve_card(lang, theme):
    return card(["#03060f", "#0b1430", "#1b2b55"], tr(RESERVE["label"], lang), tr(RESERVE["title"], lang),
                tr(RESERVE["tag"], lang), tr(RESERVE["text"], lang), theme)


def paragraph(text, theme):
    c = GH[theme]
    lines = wrap(text, 80)
    body = "".join(T(0, 20 + k * 26, l, 16, c["fg"], 300, SORA) for k, l in enumerate(lines))
    return svg(860, len(lines) * 26 + 8, text, body)


def frame(inner, label, theme, h=380):
    p = P[theme]
    body = (f'<defs><clipPath id="c"><rect width="900" height="{h}" rx="16"/></clipPath></defs>'
            f'<g clip-path="url(#c)"><rect width="900" height="{h}" fill="{p["mat"]}"/>{inner}</g>')
    if h == 380:
        return svg(900, 330, label, body, ANIM_CSS, vy=24)
    return svg(900, h, label, body, ANIM_CSS)


def art_lysbor(lang, theme):
    p = P[theme]
    rows = [(TEXTS["lys_rows"][0], p["alert"]), (TEXTS["lys_rows"][1], p["alert"]), (TEXTS["lys_rows"][2], p["amber"])]
    inner = T(40, 44, tr(TEXTS["lys_in"], lang), 12, p["sub"]) + T(470, 44, tr(TEXTS["lys_out"], lang), 12, p["sub"])
    inner += f'<rect x="40" y="62" width="400" height="280" rx="12" fill="{p["panel"]}" stroke="{p["line"]}"/>'
    for k, w in enumerate([220, 160, 280, 120, 240, 190, 300, 140, 210, 170, 230]):
        inner += f'<rect x="64" y="{82 + k * 23}" width="{w}" height="8" rx="4" fill="{p["alert"] if k in (2, 5, 8) else p["bar"]}"/>'
    inner += f'<rect class="scanbeam" x="40" y="64" width="400" height="12" fill="{p["accent"]}" opacity=".35"/>'
    for k, (r, col) in enumerate(rows):
        a, b = tr(r, lang)
        inner += (f'<g class="row" style="animation-delay:{k * .35}s"><rect x="470" y="{70 + k * 92}" width="390" height="76" rx="12" fill="{p["panel"]}" stroke="{p["line"]}"/>'
                  f'<circle cx="498" cy="{108 + k * 92}" r="8" fill="{col}"/>' +
                  T(520, 102 + k * 92, a, 16, p["ink"], 600, SORA) + T(520, 126 + k * 92, b, 12.5, p["sub"]) + "</g>")
    return frame(inner, tr(TEXTS["lys_alt"], lang), theme)


def art_patchboard(lang, theme):
    p = P[theme]
    inner = T(40, 44, tr(TEXTS["pb_in"], lang), 12, p["sub"]) + T(480, 44, tr(TEXTS["pb_out"], lang), 12, p["sub"])
    for k in range(8):
        x, y = 50 + (k % 4) * 96, 80 + (k // 4) * 120
        inner += (f'<g class="csv" style="--dx:{440 - x}px;animation-delay:{k * .12}s"><rect x="{x}" y="{y}" width="66" height="86" rx="8" fill="{p["panel"]}" stroke="{p["line"]}"/>'
                  f'<text x="{x + 33}" y="{y + 50}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="600" fill="{p["sub"]}">CSV</text></g>')
    inner += (f'<g class="fi"><rect x="480" y="62" width="380" height="280" rx="12" fill="{p["panel"]}" stroke="{p["line"]}"/>' +
              T(506, 140, "18", 58, p["alert"], 800, SORA) + T(590, 118, tr(TEXTS["pb_computers"], lang), 16, p["ink"], 600, SORA) +
              T(590, 140, tr(TEXTS["pb_update"], lang), 15, p["sub"], 400, SORA) + "</g>")
    for k, (lab, v, col) in enumerate([(TEXTS["pb_bars"][0], .72, p["ok"]), (TEXTS["pb_bars"][1], .48, p["amber"]), (TEXTS["pb_bars"][2], .22, p["alert"])]):
        inner += f'<g class="fi">{T(506, 198 + k * 40, tr(lab, lang), 12, p["sub"])}</g>'
        inner += f'<rect class="gr" x="620" y="{188 + k * 40}" width="{v * 200}" height="12" rx="6" fill="{col}"/>'
    inner += (f'<g class="ml"><rect x="770" y="292" width="44" height="30" rx="5" fill="{p["accent"]}"/>'
              f'<path d="M770 294 l22 16 22 -16" fill="none" stroke="{p["panel"]}" stroke-width="2.5"/></g>')
    return frame(inner, tr(TEXTS["pb_alt"], lang), theme)


def art_lowsper(lang, theme):
    p = P[theme]
    inner = T(40, 44, tr(TEXTS["lw_in"], lang), 12, p["sub"]) + T(400, 44, tr(TEXTS["lw_out"], lang), 12, p["sub"])
    for k, who in enumerate(TEXTS["lw_people"]):
        col = p["violet"] if k else p["accent"]
        inner += (f'<g transform="translate(40 {66 + k * 140})"><rect width="330" height="116" rx="12" fill="{p["panel"]}" stroke="{p["line"]}"/>'
                  f'<circle cx="42" cy="58" r="24" fill="{col}"/>' + T(80, 34, tr(who, lang), 12, p["sub"]))
        for j in range(16):
            inner += (f'<rect class="wv" x="{82 + j * 14}" y="48" width="7" height="44" rx="3.5" fill="{col}" '
                      f'style="animation-delay:{((j * 37 + k * 50) % 100) / 100}s"/>')
        inner += "</g>"
    inner += f'<rect x="400" y="62" width="460" height="280" rx="12" fill="{p["panel"]}" stroke="{p["line"]}"/>'
    for k, (time, who, line) in enumerate(TEXTS["lw_lines"]):
        inner += (f'<g class="tl" style="animation-delay:{k * 1.2}s">' + T(424, 102 + k * 52, f"[{time}] {tr(who, lang)}", 12, p["sub"]) +
                  T(424, 124 + k * 52, tr(line, lang), 16, p["ink"], 400, SORA) + "</g>")
    inner += (f'<rect x="630" y="300" width="214" height="28" rx="14" fill="{p["ok"]}" opacity=".16"/>' +
              T(646, 319, tr(TEXTS["lw_local"], lang), 12, p["ok"]))
    return frame(inner, tr(TEXTS["lw_alt"], lang), theme)


def art_labo(lang, theme):
    p = P[theme]
    photo = ('<rect x="40" y="62" width="480" height="280" fill="url(#ph)"/>'
             '<path d="M40 170 C 160 110, 280 200, 400 140 S 520 120, 540 150 L 540 190 C 420 170, 300 240, 180 200 S 60 200, 40 220Z" fill="url(#au)" filter="url(#bl)"/>'
             '<path d="M40 300 L140 250 L230 278 L330 236 L430 270 L520 246 L520 342 L40 342Z" fill="#050a14"/>')
    inner = ('<defs><linearGradient id="ph" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a1430"/><stop offset="1" stop-color="#24366a"/></linearGradient>'
             '<linearGradient id="au" x1="0" x2="1"><stop offset="0" stop-color="#43f5b5" stop-opacity="0"/><stop offset=".5" stop-color="#43f5b5"/><stop offset="1" stop-color="#a28bff" stop-opacity="0"/></linearGradient>'
             '<filter id="bl"><feGaussianBlur stdDeviation="9"/></filter><clipPath id="k"><rect x="40" y="62" width="480" height="280" rx="10"/></clipPath>'
             '<clipPath id="r"><rect class="splitl" x="40" y="62" width="160" height="280"/></clipPath></defs>')
    inner += T(40, 44, tr(TEXTS["lb_in"], lang), 12, p["sub"]) + T(560, 44, tr(TEXTS["lb_out"], lang), 12, p["sub"])
    inner += (f'<g clip-path="url(#k)"><g>{photo}</g><g clip-path="url(#r)" style="filter:brightness(.55) saturate(.4)">{photo}</g>'
              '<rect class="splitl" x="198" y="62" width="3" height="280" fill="#fff"/></g>')
    cols = [p["accent"], p["ok"], p["amber"], p["violet"]]
    for k, tag in enumerate(TEXTS["lb_tags"]):
        inner += (f'<g class="tg" style="animation-delay:{k * .5}s"><rect x="560" y="{70 + k * 52}" width="300" height="40" rx="20" fill="{p["panel"]}" stroke="{p["line"]}"/>'
                  f'<circle cx="584" cy="{90 + k * 52}" r="6" fill="{cols[k]}"/>' + T(600, 95 + k * 52, tr(tag, lang), 14, p["ink"], 600, SORA) + "</g>")
    inner += (f'<rect x="560" y="290" width="300" height="52" rx="12" fill="{p["panel"]}" stroke="{p["accent"]}"/>' +
              T(580, 313, tr(TEXTS["lb_mcp"], lang), 12, p["accent"], 600) + T(580, 332, tr(TEXTS["lb_mcp2"], lang), 12, p["sub"]))
    return frame(inner, tr(TEXTS["lb_alt"], lang), theme)


def art_aurion(lang, theme):
    inner = (f'<image href="{jpeg("aurion.jpg")}" x="0" y="-61" width="900" height="502"/>'
             '<g class="tg"><rect x="330" y="236" width="196" height="38" rx="19" fill="#06101f" fill-opacity=".72" stroke="#43f5b5" stroke-opacity=".7"/>'
             '<circle class="pu" cx="352" cy="255" r="6" fill="#43f5b5"/>' + T(368, 260, tr(TEXTS["au_detect"], lang), 13, "#dff7f1", 600) + "</g>")
    for k, rank in enumerate(TEXTS["au_ranks"]):
        inner += (f'<g class="th" style="animation-delay:{k * .4}s"><rect x="640" y="{22 + k * 54}" width="236" height="44" rx="8" fill="#06101f" fill-opacity=".72" stroke="#43f5b5" stroke-opacity="{.85 - k * .25}"/>'
                  f'<rect x="650" y="{29 + k * 54}" width="50" height="30" rx="4" fill="#12305a"/>'
                  f'<path d="M652 {52 + k * 54} q12 -14 24 -5 t22 -7" stroke="#43f5b5" stroke-opacity="{1 - k * .3}" stroke-width="3" fill="none"/>' +
                  T(712, 50 + k * 54, f"#{k + 1} · {tr(rank, lang)}", 12.5, "#d6efec") + "</g>")
    return frame(inner, tr(TEXTS["au_alt"], lang), theme)


def art_reserve(lang, theme):
    inner = (f'<image href="{jpeg("reserve.jpg")}" x="0" y="-60" width="900" height="502"/>'
             '<defs><linearGradient id="veil" x1="0" x2="1"><stop offset="0" stop-color="#02050c" stop-opacity=".62"/>'
             '<stop offset=".38" stop-color="#02050c" stop-opacity=".4"/><stop offset=".6" stop-color="#02050c" stop-opacity="0"/></linearGradient></defs>'
             '<rect width="900" height="260" fill="url(#veil)"/>' + T(32, 34, tr(RESERVE["badge"], lang), 12, "#f3d27a", 600))
    for k, tag in enumerate(RESERVE["tags"]):
        inner += (f'<rect x="32" y="{48 + k * 41}" width="300" height="33" rx="7" fill="#fbf3df" fill-opacity=".94"/>'
                  f'<circle cx="50" cy="{64.5 + k * 41}" r="4.5" fill="#9b2a1f"/>' + T(64, 69 + k * 41, tr(tag, lang), 13.5, "#2a1a10", 600, SORA))
    label = tr(RESERVE["alt"], lang) + ", ".join(tr(t, lang) for t in RESERVE["tags"])
    return frame(inner, label, theme, 260)


ARTS = {"lowsper": art_lowsper, "lysbor": art_lysbor, "patchboard": art_patchboard, "labo": art_labo, "aurion": art_aurion}


# ---------------------------------------------------------------- README
def readme(lang):
    other = "README.fr.md" if lang == "en" else "README.md"
    fr = lang == "fr"
    L = lambda pair: tr(pair, lang)  # noqa: E731
    out = [f"<!-- Generated by tools/build.py from tools/content.py. Edit the content there, then run the script. -->", ""]
    # header: banner floated left, contacts on the right
    out.append(f'<img align="left" width="64%" src="assets/header/banner-{lang}-dark.svg" alt="{esc("Jolan D. " + L(TITLE))}">')
    out.append("")
    out.append(f'<p align="right"><a href="{other}"><img src="assets/header/lang-{lang}.svg" height="26" '
               f'alt="{"Version française" if lang == "en" else "English version"}"></a></p>')
    out.append(f'<p align="right"><a href="mailto:{CONTACT}?subject=Hello%20Jolan"><img src="assets/header/mail-{lang}.svg" height="30" alt="{esc(L(BUTTON_MAIL))}"></a> '
               f'<a href="{LINKEDIN}"><img src="assets/header/linkedin.svg" height="30" alt="LinkedIn"></a><br>'
               f'<sub><code>{CONTACT}</code></sub></p>')
    out.append("")
    out.append(f'<img width="100%" src="{LIVE_URL}/nowline-{lang}-dark.svg" alt="{esc(L(NOW_PREFIX).strip())}">')
    out.append("")
    # GitHub prefixes every id with "user-content-" and only scrolls when the link uses that full id
    slices = "".join(f'<a href="#user-content-{h["key"]}"><img width="20%" src="{LIVE_URL}/slice-{k}-{lang}.svg" '
                     f'alt="{esc(h["label"] + " · " + L(h["proj"]))}"></a>' for k, h in enumerate(HOURS))
    out.append(f"<p>{slices}</p>")
    out.append("")
    # signs
    sign_alt = ", ".join(L(s["title"]) for s in SIGNS)
    out.append('<details name="reads">')
    out.append(f'<summary><picture><img src="assets/header/signs-{lang}-dark.svg" width="96%" alt="{esc(sign_alt + ". " + L(SIGNS_HINT))}"></picture></summary>')
    out.append("")
    for s in SIGNS:
        out.append(f'**{L(s["title"])}.** {L(s["text"])}')
        out.append("")
    out.append("</details>")
    out.append("")
    # one block per time slot, then the vault: scene on one side, text on the other (zigzag)
    blocks = [dict(key=h["key"], art=(f'art-{h["key"]}-{lang}.svg' if h["key"] == "aurion" else f'art-{h["key"]}-{lang}-dark.svg'),
                   art_alt=L(ARTS_ALT[h["key"]]), card=f'card-{h["key"]}-{lang}-dark.svg',
                   card_alt=f'{h["label"]} · {L(h["what"])}. {L(PROJECTS[h["key"]]["title"])}. {L(PROJECTS[h["key"]]["tag"])}. {L(PROJECTS[h["key"]]["text"])}',
                   href=PROJECTS[h["key"]]["href"], link=L(PROJECTS[h["key"]]["link"]), tech=L(PROJECTS[h["key"]]["tech"]))
              for h in HOURS]
    blocks.append(dict(key="reserve", art=f"art-reserve-{lang}.svg",
                       art_alt=L(RESERVE["alt"]) + ", ".join(L(t) for t in RESERVE["tags"]),
                       card=f"card-reserve-{lang}-dark.svg",
                       card_alt=f'{L(RESERVE["label"])}. {L(RESERVE["title"])}. {L(RESERVE["tag"])}. {L(RESERVE["text"])}',
                       href=f"mailto:{CONTACT}?subject=Demo", link=L(RESERVE["link"]), tech=L(RESERVE["tech"])))
    for k, bl in enumerate(blocks):
        side = "left" if k % 2 == 0 else "right"
        out.append(f'<a id="{bl["key"]}"></a>')
        img = f'<img align="{side}" width="50%" src="assets/sections/{bl["art"]}" alt="{esc(bl["art_alt"])}">'
        # a bare <img> gets wrapped in a link to the file; <picture> avoids it
        out.append(img if bl["art"].endswith("-dark.svg") else f"<picture>{img}</picture>")
        out.append(f'<img width="46%" src="assets/sections/{bl["card"]}" alt="{esc(bl["card_alt"])}">')
        out.append("")
        out.append(f'<details><summary><b>{L(HEADINGS["tech"])}</b> · <a href="{bl["href"]}">{bl["link"]} →</a></summary>')
        out.append("")
        out.append(bl["tech"])
        out.append("")
        out.append("</details>")
        out.append('<br clear="all">')
        out.append("")
    out.append(f'<img width="100%" src="assets/sections/text-talk-{lang}-dark.svg" alt="{esc(L(TALK))}">')
    out.append("")
    text = "\n".join(out)
    # every themed image becomes a <picture> so it follows the GitHub theme
    def themed(m):
        attrs, src = m.group(1) + m.group(3), m.group(2)
        base = src[: -len("-dark.svg")]
        alt = re.search(r'alt="([^"]*)"', attrs).group(1)
        rest = re.sub(r'\s*alt="[^"]*"', "", attrs)
        return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{base}-dark.svg">'
                f'<source media="(prefers-color-scheme: light)" srcset="{base}-light.svg">'
                f'<img{rest} src="{base}-dark.svg" alt="{alt}"></picture>')
    text = re.sub(r'<picture><img([^>]*?) src="([^"]+-dark\.svg)"([^>]*)></picture>', themed, text)
    text = re.sub(r'<img([^>]*?) src="([^"]+-dark\.svg)"([^>]*)>', themed, text)
    return text + "\n"


ARTS_ALT = {"lowsper": TEXTS["lw_alt"], "lysbor": TEXTS["lys_alt"], "patchboard": TEXTS["pb_alt"],
            "labo": TEXTS["lb_alt"], "aurion": TEXTS["au_alt"]}


def main():
    for lang in LANGS:
        write(f"assets/header/lang-{lang}.svg", lang_pill(lang))
        write(f"assets/header/mail-{lang}.svg", btn_mail(lang))
        for i in range(5):
            write(f"assets/live-src/slice-{i}-{lang}.svg", slice_svg(i, lang, False))
            write(f"assets/live-src/slice-{i}-{lang}-now.svg", slice_svg(i, lang, True))
        write(f"assets/sections/art-reserve-{lang}.svg", art_reserve(lang, "dark"))
        write(f"assets/sections/art-aurion-{lang}.svg", art_aurion(lang, "dark"))
        for theme in THEMES:
            write(f"assets/header/banner-{lang}-{theme}.svg", banner(lang, theme))
            write(f"assets/header/signs-{lang}-{theme}.svg", signs(lang, theme))
            for slot in SLOTS:
                write(f"assets/live-src/nowline-{slot}-{lang}-{theme}.svg", nowline(slot, lang, theme))
            for h in HOURS:
                write(f"assets/sections/card-{h['key']}-{lang}-{theme}.svg", project_card(h["key"], lang, theme))
                if h["key"] != "aurion":  # a night photo: the same in both themes
                    write(f"assets/sections/art-{h['key']}-{lang}-{theme}.svg", ARTS[h["key"]](lang, theme))
            write(f"assets/sections/card-reserve-{lang}-{theme}.svg", reserve_card(lang, theme))
            write(f"assets/sections/text-talk-{lang}-{theme}.svg", paragraph(tr(TALK, lang), theme))
    write("assets/header/linkedin.svg", btn_linkedin())
    write("README.md", readme("en"))
    write("README.fr.md", readme("fr"))
    print("done")


if __name__ == "__main__":
    main()
