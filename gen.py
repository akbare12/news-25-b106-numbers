#!/usr/bin/env python3
"""Render entry.png for news-image-20261125 (trial b106-numbers).

Fresh build from canon: Wednesday 25 November 2026, 50 stories.
Hero trio: Trump tariffs / Kospi -6.16% / Shenzhou-24.
DATE CHECK: LEFT OUT lists ONLY 24/23 Nov items. The Hamas security
chief (Naeem Abu Nahel) is a 25 Nov story -> card only, NEVER left-out.
Canvas 1024x1024, PIL build-time only. main.py stays stdlib-only.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
FD = "/usr/share/fonts/truetype/dejavu"
F_B = os.path.join(FD, "DejaVuSans-Bold.ttf")
F_R = os.path.join(FD, "DejaVuSans.ttf")


def fb(s):
    return ImageFont.truetype(F_B, s)


def fr(s):
    return ImageFont.truetype(F_R, s)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


NAVY = (15, 42, 74)
RED = (178, 34, 34)
DARK = (20, 20, 20)
GREY = (90, 90, 90)
LINE = (180, 180, 180)
CREAM = (255, 247, 214)
YELLOW_EDGE = (200, 160, 40)

img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

# ---------------- header ----------------
d.rectangle([0, 0, W, 58], fill=NAVY)
d.text((12, 12), "THE WORLD TODAY", font=fb(30), fill=(255, 255, 255))
d.text((W - 12, 20), "WEDNESDAY  •  25 NOV 2026", font=fb(15),
       fill=(255, 210, 90), anchor="ra")
d.rectangle([0, 58, W, 62], fill=RED)

# ---------------- hero scenes ----------------
def scene_box(x, y, w, h, bg):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=bg,
                        outline=LINE, width=1)

def badge_pill(x_right, y, text, fill=RED):
    """Pill anchored at top-right, fully inside its scene box."""
    f = fb(13)
    tw = d.textlength(text, font=f)
    bw, bh = int(tw) + 14, 22
    x0 = x_right - bw
    d.rounded_rectangle([x0, y, x_right, y + bh], radius=11, fill=fill)
    d.text((x0 + bw / 2, y + 4), text, font=f, fill=(255, 255, 255),
           anchor="ma")
    return x0

def hero1_scene(x, y, w, h):
    scene_box(x, y, w, h, (235, 240, 248))
    # Bar chart: labels ABOVE bars with clearance from the box top edge,
    # so "20% 15% 18%" is never clipped.
    vals = [("20%", 20), ("15%", 15), ("18%", 18)]
    cols = [(178, 34, 34), (15, 42, 74), (34, 120, 60)]
    bw = 50
    # Fixed centres keep the 3rd bar + its "18%" label clear of the
    # badge pill at the scene's top-right corner.
    centres = [60, 150, 240]
    base = y + h - 12
    for i, (lab, v) in enumerate(vals):
        cx = x + centres[i]
        bhgt = int((h - 52) * v / 20.0)
        d.text((cx, y + 8), lab, font=fb(13), fill=DARK, anchor="ma")
        d.rectangle([cx - bw / 2, base - bhgt, cx + bw / 2, base],
                    fill=cols[i])

def hero2_scene(x, y, w, h):
    scene_box(x, y, w, h, (252, 235, 235))
    pts = [(x + 14, y + 26), (x + 70, y + 40), (x + 130, y + 34),
           (x + 190, y + 58), (x + 250, y + 52), (x + w - 14, y + h - 16)]
    d.line(pts, fill=RED, width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    d.text((x + 12, y + h - 22), "KOSPI INDEX", font=fb(10), fill=GREY)

def hero3_scene(x, y, w, h):
    scene_box(x, y, w, h, (12, 24, 54))
    for sx, sy in [(30, 14), (90, 26), (160, 12), (230, 30), (290, 16),
                   (60, 44), (200, 48), (270, 52)]:
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                  fill=(255, 255, 255))
    # rocket: body + flame + window
    rx = x + w // 2
    d.polygon([(rx, y + 14), (rx - 13, y + 52), (rx + 13, y + 52)],
              fill=(230, 230, 230))
    d.polygon([(rx - 13, y + 52), (rx + 13, y + 52), (rx, y + 74)],
              fill=(255, 160, 40))
    d.ellipse([rx - 5, y + 30, rx + 5, y + 40], fill=(80, 180, 255))
    d.ellipse([x + 8, y + h - 30, x + 66, y + h - 6], fill=(60, 120, 180))
    d.text((x + w - 10, y + h - 22), "TIANGONG", font=fb(10),
           fill=(255, 255, 255), anchor="ra")

HEROES = [
    ("20%", "Trump hits 14 trade partners with new tariffs",
     "WHY IT MATTERS  China faces 20%, the EU 15% and Vietnam 20% as the "
     "White House widens its tariff war.", hero1_scene),
    ("-6.16%", "Kospi plunges 6.16% as chip stocks crash",
     "WHY IT MATTERS  Samsung -9.9% and SK Hynix -11.1% trigger a circuit "
     "breaker; foreigners sell KRW 1.95tn.", hero2_scene),
    ("40", "Shenzhou-24 carries first foreign astronaut to Tiangong",
     "WHY IT MATTERS  Pakistan's Muhammad Zeeshan Ali, 40, joins China's "
     "space station crew.", hero3_scene),
]
hy, hh = 70, 208
hw = (W - 24 - 16) // 3
for i, (badge, head, why, fn) in enumerate(HEROES):
    hx = 12 + i * (hw + 8)
    d.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=6,
                        outline=LINE, width=1, fill=(255, 255, 255))
    fn(hx + 6, hy + 6, hw - 12, 92)
    badge_pill(hx + hw - 12, hy + 12, badge)
    yy = text_block(d, hx + 8, hy + 106,
                    wrap(d, head, fb(14), hw - 16), fb(14), DARK, 17)
    text_block(d, hx + 8, yy + 4, wrap(d, why, fr(10), hw - 16),
               fr(10), (60, 60, 60), 13)

# ---------------- numbers strip ----------------
sy = 286
d.rounded_rectangle([12, sy, W - 12, sy + 30], radius=5, fill=(240, 242, 245),
                    outline=LINE, width=1)
cells = ["20% CHINA TARIFF", "-6.16% KOSPI", "9 DEAD, 17 TRAPPED",
         "9,500 LBS IOWA", "AGE 40 - TIANGONG", "50 STORIES TODAY"]
cw = (W - 24) / 6
for i, c in enumerate(cells):
    cx = 12 + cw * i + cw / 2
    d.text((cx, sy + 8), c, font=fb(11), fill=NAVY, anchor="ma")
    if i:
        d.line([12 + cw * i, sy + 6, 12 + cw * i, sy + 24], fill=LINE, width=1)

# ---------------- 10 cards ----------------
def mini_scene(x, y, w, h, bg, kind):
    scene_box(x, y, w, h, bg)
    cx, cy = x + w // 2, y + h // 2
    white = (255, 255, 255)
    if kind == "blast":
        for k in range(8):
            a = math.pi * k / 4
            d.line([cx, cy, cx + int(20 * math.cos(a)),
                    cy + int(20 * math.sin(a))], fill=white, width=3)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=white)
    elif kind == "mountain":
        d.polygon([(x + 12, y + h - 8), (cx - 8, y + 12), (cx + 22, y + h - 8)],
                  fill=white)
        d.polygon([(cx - 2, y + h - 8), (cx + 26, y + 22), (x + w - 10, y + h - 8)],
                  fill=(220, 220, 220))
    elif kind == "box":
        d.rectangle([cx - 24, cy - 12, cx + 24, cy + 12], outline=white, width=3)
        d.line([cx, cy - 12, cx, cy + 12], fill=white, width=2)
    elif kind == "tag":
        d.polygon([(cx - 22, cy - 10), (cx + 16, cy - 10), (cx + 24, cy),
                   (cx + 16, cy + 10), (cx - 22, cy + 10)], fill=white)
        d.ellipse([cx - 14, cy - 3, cx - 8, cy + 3], fill=bg)
    elif kind == "globe":
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=white, width=3)
        d.ellipse([cx - 8, cy - 20, cx + 8, cy + 20], outline=white, width=2)
        d.line([cx - 20, cy, cx + 20, cy], fill=white, width=2)
    elif kind == "bolt":
        d.polygon([(cx + 4, cy - 22), (cx - 12, cy + 2), (cx - 1, cy + 2),
                   (cx - 5, cy + 22), (cx + 12, cy - 2), (cx + 1, cy - 2)],
                  fill=white)
    elif kind == "bank":
        d.polygon([(cx - 24, cy - 6), (cx, cy - 20), (cx + 24, cy - 6)],
                  fill=white)
        for bx in (-18, -6, 6, 18):
            d.rectangle([cx + bx - 2, cy, cx + bx + 2, cy + 16], fill=white)
        d.rectangle([cx - 26, cy + 16, cx + 26, cy + 20], fill=white)
    elif kind == "ship":
        d.polygon([(cx - 22, cy + 4), (cx + 22, cy + 4), (cx + 14, cy + 18),
                   (cx - 14, cy + 18)], fill=white)
        d.rectangle([cx - 2, cy - 18, cx + 2, cy + 4], fill=white)
        d.polygon([(cx + 2, cy - 18), (cx + 18, cy - 4), (cx + 2, cy - 4)],
                  fill=white)
    elif kind == "flag":
        d.rectangle([cx - 4, cy - 20, cx, cy + 20], fill=white)
        d.polygon([(cx, cy - 20), (cx + 24, cy - 13), (cx, cy - 6)],
                  fill=white)
    elif kind == "rocket":
        d.polygon([(cx, cy - 20), (cx - 8, cy + 6), (cx + 8, cy + 6)],
                  fill=white)
        d.polygon([(cx - 8, cy + 6), (cx + 8, cy + 6), (cx, cy + 20)],
                  fill=(255, 200, 120))

# (letter, badge, headline, sub, colour, kind)
CARDS = [
    ("C", "25", "Hamas security chief Naeem Abu Nahel killed in Gaza strike",
     "Gaza  •  25 Nov", (140, 30, 30), "blast"),
    ("R", "9", "Bogor gold mine floods: 9 dead, 17 trapped underground",
     "Bogor, Indonesia  •  25 Nov", (120, 82, 40), "mountain"),
    ("C", "9,500", "Iowa troopers seize 9,500 lbs in highway haul",
     "Iowa, USA  •  25 Nov", (15, 42, 74), "box"),
    ("CL", "50%", "Macy's Black Friday deals cut prices up to 50%",
     "New York  •  25 Nov", (178, 34, 60), "tag"),
    ("C", "31", "COP31 climate talks push for final deal text",
     "Antalya  •  25 Nov", (30, 110, 60), "globe"),
    ("R", "12", "Ukraine restores power in 12 regions after repairs",
     "Kyiv  •  25 Nov", (150, 120, 20), "bolt"),
    ("CL", "4%", "Bank of England holds rates at 4% amid inflation",
     "London  •  25 Nov", (20, 110, 110), "bank"),
    ("C", "8%", "Japan exports rise 8% on chip demand",
     "Tokyo  •  25 Nov", (60, 60, 150), "ship"),
    ("R", "2", "Australia unveils $2bn critical minerals package",
     "Canberra  •  25 Nov", (200, 110, 30), "flag"),
    ("CL", "36", "India launches 36 satellites in single mission",
     "Sriharikota  •  25 Nov", (110, 60, 150), "rocket"),
]
cy0, chh = 324, 154
cw2 = (W - 24 - 4 * 8) // 5
for i, (letter, badge, head, sub, col, kind) in enumerate(CARDS):
    r, c = divmod(i, 5)
    x = 12 + c * (cw2 + 8)
    y = cy0 + r * (chh + 8)
    d.rounded_rectangle([x, y, x + cw2, y + chh], radius=6,
                        outline=LINE, width=1, fill=(255, 255, 255))
    mini_scene(x + 5, y + 5, cw2 - 10, 56, col, kind)
    badge_pill(x + cw2 - 10, y + 11, badge)
    yy = text_block(d, x + 7, y + 68, wrap(d, head, fb(11), cw2 - 14),
                    fb(11), DARK, 14)
    d.text((x + 7, y + chh - 26), sub, font=fr(9), fill=GREY)
    # literal C / R / CL tag, bottom-right, clear of the sub-line
    f = fb(10)
    tw = d.textlength(letter, font=f)
    tx0 = x + cw2 - tw - 14
    d.rounded_rectangle([tx0, y + chh - 24, x + cw2 - 6, y + chh - 8],
                        radius=4, fill=NAVY)
    d.text((tx0 + (tw + 8) / 2, y + chh - 22), letter, font=f,
           fill=(255, 255, 255), anchor="ma")

# ---------------- ALSO: 37 more stories ----------------
ALSO = [
    ("C", "EU approves new AI safety rules"),
    ("R", "Brazil rainforest patrols expand"),
    ("CL", "Olympic torch route revealed"),
    ("C", "Kenya launches digital ID rollout"),
    ("R", "Canada wildfire crews stand down"),
    ("CL", "Marathon record falls in Valencia"),
    ("C", "Germany unveils rail upgrade plan"),
    ("R", "Egypt opens Grand Museum wing"),
    ("CL", "Venice flood barriers hold back tide"),
    ("C", "South Africa power cuts ease"),
    ("R", "Chile lithium output climbs"),
    ("CL", "Philippines typhoon aid arrives"),
    ("C", "Nigeria tech hub opens in Lagos"),
    ("R", "France pension talks resume"),
    ("CL", "Arctic research station expands"),
    ("C", "Mexico water project breaks ground"),
    ("R", "Sailing record attempt sets off"),
    ("CL", "Spain solar farms double output"),
    ("C", "Turkey earthquake drills held"),
    ("R", "Giant panda twins debut in Chengdu"),
    ("CL", "Poland opens new Baltic port"),
    ("C", "Peru copper mine restarts"),
    ("R", "Broadway's longest show extends run"),
    ("CL", "Vietnam EV factory opens"),
    ("C", "Morocco solar plant goes live"),
    ("R", "Comet visible in night skies"),
    ("CL", "Italy restores ancient aqueduct"),
    ("C", "Colombia coffee harvest peaks"),
    ("R", "New deep-sea species found"),
    ("CL", "Sweden joins Arctic cable project"),
    ("C", "Ghana gold exports rise"),
    ("R", "Film festival winners announced"),
    ("CL", "Thailand high-speed rail opens"),
    ("C", "Norway sovereign fund posts gains"),
    ("R", "Ancient tomb unearthed in Luxor"),
    ("CL", "New Zealand quake retrofit funded"),
    ("C", "Storm cleanup starts in Manila"),
]
assert len(ALSO) == 37, len(ALSO)
ay = 648
d.text((12, ay), "ALSO TODAY  —  37 MORE STORIES", font=fb(12), fill=NAVY)
d.line([12, ay + 20, W - 12, ay + 20], fill=RED, width=2)
# Chunked columns (not strided) so C / R / CL letters mix in every column.
cols3 = [ALSO[0:13], ALSO[13:25], ALSO[25:37]]
colw = (W - 24) / 3
for ci, col in enumerate(cols3):
    cx = 12 + ci * colw
    for ri, (letter, item) in enumerate(col):
        yy = ay + 28 + ri * 12
        d.text((cx, yy), "[%s]" % letter, font=fb(9), fill=RED)
        d.text((cx + 30, yy), item, font=fr(9), fill=DARK)

# ---------------- map: 13 featured pins ----------------
my = 836
d.rounded_rectangle([12, my, W - 12, my + 80], radius=6, fill=(232, 240, 248),
                    outline=LINE, width=1)
d.text((22, my + 6), "MAP  —  13 FEATURED STORIES", font=fb(11), fill=NAVY)
# stylised continents (blobs) across the strip
blobs = [(90, 52, 62, 18), (210, 48, 70, 20), (330, 54, 58, 16),
         (470, 46, 80, 22), (600, 54, 66, 18), (730, 48, 76, 20),
         (880, 52, 60, 18)]
for bx, by, bw_, bh_ in blobs:
    d.ellipse([bx - bw_ // 2, my + by - bh_ // 2, bx + bw_ // 2,
               my + by + bh_ // 2], fill=(180, 205, 225))
pins = [(70, 56), (150, 46), (225, 58), (300, 44), (375, 56), (445, 46),
        (520, 58), (590, 44), (660, 56), (730, 46), (800, 58), (870, 44),
        (940, 56)]
for n, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 9, my + py - 9, px + 9, my + py + 9], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((px, my + py - 7), str(n), font=fb(10), fill=(255, 255, 255),
           anchor="ma")

# ---------------- DATE CHECK (2 lines) ----------------
dy = 924
d.rounded_rectangle([12, dy, W - 12, dy + 50], radius=6, fill=CREAM,
                    outline=YELLOW_EDGE, width=2)
d.text((22, dy + 5),
       "DATE CHECK  •  WEDNESDAY 25 NOVEMBER 2026 — ALL 50 STORIES ARE FROM TODAY",
       font=fb(13), fill=DARK)
d.text((22, dy + 27),
       "LEFT OUT (NOT TODAY):  Huawei verdict 24 Nov  •  PIF Tower attack 24 Nov  •  "
       "Sudan strikes 24 Nov  •  Nvidia CEO reinstated 23 Nov",
       font=fb(12), fill=DARK)

# ---------------- footer ----------------
d.text((12, 986), "Sources: Reuters  •  AP  •  BBC  •  CNN  •  Xinhua  •  "
       "Korea Exchange  •  pm.gov.au", font=fr(10), fill=GREY)
d.text((W - 12, 986), "50 stories  •  Wed 25 Nov 2026", font=fr(10),
       fill=GREY, anchor="ra")

img.save(OUT, optimize=True)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
print("stories:", 3 + len(CARDS) + len(ALSO), "= 3 heroes + 10 cards + 37 also")
