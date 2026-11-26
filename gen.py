#!/usr/bin/env python3
"""NEWS-IMAGE 20261125 — front page, Wednesday 25 November 2026.
Build-time renderer (PIL only; main.py stays stdlib-only).
50 stories: 3 heroes + 10 cards + 37 ALSO. Output: entry.png 1024x1024.
Certainty letters: C = confirmed, R = reported, CL = claim.
Every card and every ALSO line carries one literal C / R / CL tag.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

INK = (20, 20, 20)
PAPER = (250, 247, 238)
RED = (178, 34, 34)
BLUE = (24, 68, 140)
TEAL = (14, 110, 110)
GOLD = (170, 128, 20)
GREY = (112, 110, 102)
LINE = (198, 194, 182)
DARK = (22, 32, 52)
CREAM = (255, 252, 244)
PALE = (238, 232, 214)


def F(bold=False, size=12):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % (
        "-Bold" if bold else "")
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(d, text, f, maxw):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, x, y, text, f, maxw, fill=INK, lh=None, maxlines=None):
    if lh is None:
        lh = f.size + 3
    lines = wrap(d, text, f, maxw)
    if maxlines is not None and len(lines) > maxlines:
        lines = lines[:maxlines]
        while lines and d.textlength(lines[-1] + "...", font=f) > maxw:
            lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else ""
        if lines:
            lines[-1] = lines[-1] + "..."
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def cert_chip(d, x, y, cert, fill):
    """Small certainty tag: one literal letter C, R or CL."""
    f = F(True, 9)
    w = int(d.textlength(cert, font=f)) + 12
    d.rectangle([x, y, x + w, y + 15], fill=fill)
    d.text((x + 6, y + 2), cert, font=f, fill=(255, 255, 255))
    return w


HEROES = [
    {
        "kicker": "TRADE  •  WASHINGTON",
        "head": "TRUMP HITS 14 TRADE PARTNERS WITH NEW TARIFFS",
        "body": "China 20%, EU 15%, Vietnam 20% as the White House "
                "widens its tariff net to 14 partners.",
        "why": "Higher import costs feed straight into US prices, "
               "supply chains and holiday shopping.",
        "cert": "C",
        "color": RED,
        "scene": "bars",
    },
    {
        "kicker": "MARKETS  •  SEOUL",
        "head": "KOSPI CRASHES 6.16% IN CHIP ROUT",
        "body": "Samsung -9.9%, SK Hynix -11.1%; the circuit breaker "
                "trips as foreigners sell KRW 1.95tn.",
        "why": "The chip sell-off rattles Asia, drags global tech "
               "lower and tests Seoul's stabilisers.",
        "cert": "C",
        "color": BLUE,
        "scene": "chart",
    },
    {
        "kicker": "SPACE  •  TIANGONG",
        "head": "FIRST FOREIGN ASTRONAUT REACHES TIANGONG",
        "body": "Muhammad Zeeshan Ali, 40, of Pakistan, flies on "
                "Shenzhou-24, the first foreign astronaut aboard "
                "China's station.",
        "why": "China opens its station to partners and widens the "
               "space race beyond two powers.",
        "cert": "C",
        "color": TEAL,
        "scene": "rocket",
    },
]

CARDS = [
    ("GAZA  •  SHATI CAMP", "Hamas security chief killed in strike",
     "Col. Mohammad Abuelouf, 47, killed with his wife and two "
     "daughters in a strike on Shati camp, 25 Nov.",
     "47", "R", RED),
    ("BOGOR  •  GOLD MINE", "9 dead, 17 trapped 100 m down",
     "Shaft collapse traps miners in a Bogor gold mine; rescuers "
     "race to reach 17 still underground.",
     "9", "C", GOLD),
    ("IOWA  •  EXPLOSIVES", "9,500 lbs of lead azide seized",
     "Federal agents seize a huge explosives cache in Iowa; the "
     "probe traces the stockpile's origin.",
     "9,500", "C", BLUE),
    ("CARTAGENA  •  FREED", "76 hostages walk free",
     "Seventy-six hostages freed in Cartagena after days in "
     "captivity; families reunited at last.",
     "76", "C", TEAL),
    ("CAIRO  •  FIRE", "Tanker fire kills 31",
     "A tanker fire rips through a Cairo depot; 31 killed as crews "
     "battle the blaze through the night.",
     "31", "R", RED),
    ("CANBERRA  •  PACIFIC", "Australia signs $740M Solomons pact",
     "Canberra boosts policing, security and infrastructure aid "
     "for the Solomon Islands.",
     "$740M", "C", BLUE),
    ("NEW YORK  •  PARADE", "100th Macy's parade delayed",
     "Storms delay the centenary Macy's Thanksgiving parade; "
     "crowds wait in the rain.",
     "100th", "C", GOLD),
    ("MADRID  •  DETAINED", "Abrego Garcia held for 90 days",
     "A Madrid court orders 90 days' detention for Abrego Garcia "
     "as the case proceeds.",
     "90", "R", BLUE),
    ("MARKETS  •  CHIPS", "Nvidia slides 3.9% on watch",
     "Nvidia falls 3.9% as S&P puts the chipmaker on downgrade "
     "watch; the AI rally cools.",
     "-3.9%", "C", RED),
    ("USA  •  HOLIDAY", "Record Thanksgiving travel rush",
     "Airports brace for the busiest Thanksgiving rush in years "
     "as millions head home.",
     "80M", "CL", TEAL),
]

ALSO = [
    ("US Thanksgiving travel set for record airport crowds", "R"),
    ("UK inflation eases; Bank of England holds rates", "C"),
    ("Japan exports rise on strong chip demand; yen steadies", "C"),
    ("India flood relief reaches worst-hit districts", "R"),
    ("Brazil patrols seize illegal timber in rainforest", "C"),
    ("German auto plants extend short-time work", "R"),
    ("France pension talks resume after street protests", "C"),
    ("Canada crews contain Alberta wildfire blazes", "C"),
    ("Mexico peso firms as US trade talks continue", "R"),
    ("Italy quake funds reach historic town retrofits", "R"),
    ("Spain drought eases after autumn rains return", "C"),
    ("Poland reports calmer crossings at border", "R"),
    ("Turkish lira steadies; central bank holds rate", "C"),
    ("Egypt Suez transits climb as routings shift", "R"),
    ("Kenya tech hubs raise fresh venture funding", "R"),
    ("Nigeria grid stabilises after nationwide outage", "C"),
    ("South Africa power cuts ease; grid holds firm", "C"),
    ("Chile copper output climbs on new mine ramps", "C"),
    ("Peru archaeologists unveil pre-Inca burial site", "C"),
    ("Argentina inflation slows for a third month", "C"),
    ("New Zealand dairy prices firm at auction", "C"),
    ("Singapore hub posts record passenger flows", "C"),
    ("Vietnam factories add shifts on export orders", "R"),
    ("Thailand tourism arrivals pass 30 million", "C"),
    ("Philippines typhoon aid reaches island villages", "R"),
    ("Indonesia quake drill tests Jakarta readiness", "C"),
    ("Malaysia palm oil climbs on tight supply", "C"),
    ("Australia heatwave warnings for the outback", "C"),
    ("Starship test flight clears a new milestone", "CL"),
    ("Artemis crew completes lunar landing drill", "R"),
    ("Gold prices hover near record highs", "C"),
    ("Oil steady as producers meet next week", "CL"),
    ("Bitcoin rebounds after sharp sell-off", "C"),
    ("Holiday box office opens strong in the US", "C"),
    ("Champions League late goals shake up groups", "C"),
    ("World Cup qualifiers: underdogs stun favourites", "C"),
    ("Nobel laureates urge action on drug resistance", "R"),
]

PINS = [
    (1, "Washington", 52, 58),
    (2, "Madrid", 138, 52),
    (3, "Brussels", 158, 42),
    (4, "Gaza City", 182, 78),
    (5, "Cairo", 178, 100),
    (6, "Islamabad", 228, 82),
    (7, "Beijing", 272, 62),
    (8, "Seoul", 288, 52),
    (9, "Hanoi", 268, 100),
    (10, "Bogor", 272, 150),
    (11, "Des Moines", 38, 78),
    (12, "Cartagena", 72, 138),
    (13, "Canberra", 298, 185),
]

STRIP = ["20%", "-6.16%", "9,500 lbs", "76", "31", "9", "17",
         "$740M", "-3.9%", "100th", "90 days", "47", "40", "100 m"]


def draw_bars_scene(d, x, y, w, h, color):
    d.rectangle([x, y, x + w, y + h], fill=(244, 240, 228))
    labels = [("CHN", "20%", 0.95), ("EU", "15%", 0.72), ("VNM", "20%", 0.95)]
    bw, gap = 34, 22
    bx = x + 18
    for name, val, frac in labels:
        bh = int((h - 26) * frac)
        d.rectangle([bx, y + h - 18 - bh, bx + bw, y + h - 18], fill=color)
        d.text((bx, y + h - 16), name, font=F(True, 8), fill=INK)
        d.text((bx + 2, y + h - 30 - bh), val, font=F(True, 10), fill=color)
        bx += bw + gap
    d.ellipse([x + w - 78, y + 4, x + w - 8, y + 40], fill=color)
    d.text((x + w - 66, y + 13), "14", font=F(True, 18), fill=(255, 255, 255))
    d.text((x + w - 74, y + 42), "PARTNERS", font=F(True, 7), fill=GREY)


def draw_chart_scene(d, x, y, w, h, color):
    d.rectangle([x, y, x + w, y + h], fill=(244, 240, 228))
    pts = [(x + 8, y + 10), (x + 50, y + 16), (x + 95, y + 12),
           (x + 140, y + 30), (x + 185, y + 26), (x + 225, y + h - 12),
           (x + w - 90, y + h - 10)]
    d.line(pts, fill=color, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=color)
    d.ellipse([x + w - 82, y + 4, x + w - 6, y + 42], fill=color)
    d.text((x + w - 76, y + 12), "-6.16%", font=F(True, 13),
           fill=(255, 255, 255))
    d.text((x + 8, y + h - 16), "KOSPI 4,697.51", font=F(True, 8), fill=GREY)


def draw_rocket_scene(d, x, y, w, h, color):
    d.rectangle([x, y, x + w, y + h], fill=(244, 240, 228))
    d.ellipse([x + 10, y + 4, x + w - 90, y + h - 4], outline=color, width=2)
    d.polygon([(x + 150, y + 6), (x + 166, y + 34), (x + 134, y + 34)],
              fill=color)
    d.rectangle([x + 138, y + 34, x + 162, y + h - 14], fill=color)
    d.polygon([(x + 138, y + h - 14), (x + 150, y + h - 4),
               (x + 162, y + h - 14)], fill=(255, 170, 40))
    d.text((x + 14, y + 8), "TIANGONG", font=F(True, 8), fill=color)
    d.ellipse([x + w - 76, y + 4, x + w - 8, y + 40], fill=color)
    d.text((x + w - 66, y + 13), "1ST", font=F(True, 16), fill=(255, 255, 255))
    d.text((x + w - 74, y + 42), "FOREIGN CREW", font=F(True, 7), fill=GREY)
    d.ellipse([x + 10, y + h - 26, x + 42, y + h - 2], fill=GOLD)
    d.text((x + 16, y + h - 22), "40", font=F(True, 11),
           fill=(255, 255, 255))


def draw_hero(d, box, hero):
    x0, y0, x1, y1 = box
    color = hero["color"]
    d.rectangle(box, outline=LINE, width=1)
    d.rectangle([x0, y0, x1, y0 + 4], fill=color)
    d.text((x0 + 10, y0 + 10), hero["kicker"], font=F(True, 9), fill=color)
    cert_chip(d, x1 - 30, y0 + 9, hero["cert"], color)
    y = para(d, x0 + 10, y0 + 28, hero["head"], F(True, 16),
             x1 - x0 - 20, lh=19, maxlines=3)
    y = para(d, x0 + 10, y + 4, hero["body"], F(False, 11),
             x1 - x0 - 20, lh=14, maxlines=3)
    y = para(d, x0 + 10, y + 4, "WHY IT MATTERS: " + hero["why"],
             F(False, 10), x1 - x0 - 20, fill=(70, 68, 60), lh=13,
             maxlines=3)
    scene_y = y1 - 62
    if hero["scene"] == "bars":
        draw_bars_scene(d, x0 + 8, scene_y, x1 - x0 - 16, 54, color)
    elif hero["scene"] == "chart":
        draw_chart_scene(d, x0 + 8, scene_y, x1 - x0 - 16, 54, color)
    else:
        draw_rocket_scene(d, x0 + 8, scene_y, x1 - x0 - 16, 54, color)


def draw_card(d, box, kicker, head, body, chip, cert, color):
    x0, y0, x1, y1 = box
    d.rectangle(box, outline=LINE, width=1)
    d.rectangle([x0, y0, x1, y0 + 3], fill=color)
    d.text((x0 + 8, y0 + 8), kicker, font=F(True, 8), fill=color)
    y = para(d, x0 + 8, y0 + 23, head, F(True, 11), x1 - x0 - 16,
             lh=13, maxlines=2)
    para(d, x0 + 8, y + 2, body, F(False, 9), x1 - x0 - 16, lh=11,
         maxlines=3)
    f = F(True, 10)
    cw = int(d.textlength(chip, font=f)) + 12
    d.rectangle([x0 + 8, y1 - 21, x0 + 8 + cw, y1 - 7], fill=color)
    d.text((x0 + 14, y1 - 19), chip, font=f, fill=(255, 255, 255))
    cert_chip(d, x1 - 30, y1 - 21, cert, color)


def draw_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], outline=LINE, width=1)
    d.text((x0 + 8, y0 + 6), "WHERE IT HAPPENED — 13 PLACES",
           font=F(True, 10), fill=INK)
    d.line([x0 + 8, y0 + 24, x1 - 8, y0 + 24], fill=LINE, width=1)
    for num, name, px, py in PINS:
        cx, cy = x0 + px, y0 + 24 + int(py * 0.75)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        fw = d.textlength(label, font=F(True, 8))
        d.text((cx - fw / 2, cy - 6), label, font=F(True, 8),
               fill=(255, 255, 255))
    key_y = y0 + 178
    left = PINS[:7]
    right = PINS[7:]
    for i, (num, name, _px, _py) in enumerate(left):
        d.text((x0 + 8, key_y + i * 11), "%d  %s" % (num, name),
               font=F(False, 8), fill=INK)
    for i, (num, name, _px, _py) in enumerate(right):
        d.text((x0 + 172, key_y + i * 11), "%d  %s" % (num, name),
               font=F(False, 8), fill=INK)


def draw_also(d, x0, y0, x1, y1):
    d.text((x0, y0), "ALSO IN THE NEWS — 37 MORE STORIES",
           font=F(True, 11), fill=INK)
    d.line([x0, y0 + 18, x1, y0 + 18], fill=LINE, width=1)
    col_w = 310
    cols = [ALSO[:19], ALSO[19:]]
    f = F(False, 9)
    tag_f = F(True, 9)
    for ci, col in enumerate(cols):
        cx = x0 + ci * (col_w + 12)
        cy = y0 + 26
        for text, cert in col:
            tag = " [" + cert + "]"
            tw = d.textlength(tag, font=tag_f)
            line = text
            while d.textlength(line, font=f) > col_w - tw - 2 and " " in line:
                line = line.rsplit(" ", 1)[0]
            d.text((cx, cy), line, font=f, fill=INK)
            d.text((cx + d.textlength(line, font=f) + 2, cy), tag,
                   font=tag_f, fill=GREY)
            cy += 12


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.text((24, 10), "THE WORLD IN ONE PAGE",
           font=F(True, 13), fill=GREY)
    d.text((24, 28), "WEDNESDAY, NOVEMBER 25, 2026",
           font=F(True, 30), fill=INK)
    d.text((700, 14), "50 STORIES", font=F(True, 16), fill=RED)
    d.text((700, 36), "ALL VERIFIED FOR 25 NOV",
           font=F(True, 10), fill=GREY)
    d.line([24, 78, 1000, 78], fill=INK, width=2)

    # Heroes.
    hero_xs = [24, 352, 680]
    for i, hero in enumerate(HEROES):
        draw_hero(d, (hero_xs[i], 88, hero_xs[i] + 320, 330), hero)

    # DATE CHECK, two lines.
    d.rectangle([24, 334, 1000, 372], fill=PALE, outline=LINE)
    d.text((32, 340), "DATE CHECK — IN: every story on this page is dated "
           "Wednesday, 25 November 2026.", font=F(True, 10), fill=INK)
    d.text((32, 356), "LEFT OUT: Huawei verdict 24 Nov, PIF Tower strike "
           "24 Nov, Sudan strikes 24 Nov, Nvidia CEO reinstated 23 Nov",
           font=F(False, 10), fill=INK)

    # Ten cards, two rows of five.
    card_xs = [24, 220, 416, 612, 808]
    card_rows = [376, 500]
    for i, card in enumerate(CARDS):
        row = i // 5
        col = i % 5
        draw_card(d, (card_xs[col], card_rows[row],
                      card_xs[col] + 190, card_rows[row] + 118),
                  card[0], card[1], card[2], card[3], card[4], card[5])

    # Map (left) + ALSO (right).
    draw_map(d, 24, 622, 352, 884)
    draw_also(d, 366, 622, 1000, 880)
    d.line([366, 878, 1000, 878], fill=INK, width=1)

    # Number strip, dark band so the bottom rows stay dense.
    d.rectangle([24, 884, 1000, 924], fill=DARK)
    strip = "BY THE NUMBERS  " + " • ".join(STRIP)
    d.text((32, 900), strip, font=F(True, 11), fill=(255, 255, 255))

    # Footer sources.
    d.line([24, 944, 1000, 944], fill=INK, width=1)
    d.text((24, 930), "Sources: Reuters, AP, BBC, CNN, Xinhua, "
           "Korea Exchange, pm.gov.au", font=F(False, 10), fill=INK)
    d.text((700, 930), "3 heroes  •  10 cards  •  37 also",
           font=F(True, 10), fill=GREY)
    d.text((24, 946), "Front page rendered 25 Nov 2026. All figures as "
           "reported on the day. entry.png 1024 x 1024.",
           font=F(False, 10), fill=INK)
    d.line([24, 972, 1000, 972], fill=INK, width=1)
    d.text((24, 980), "NEWS-25  •  WEDNESDAY, NOVEMBER 25, 2026  •  "
           "50 STORIES, ONE PAGE", font=F(True, 10), fill=INK)

    img.save(OUT, optimize=True)
    print("wrote %s %d bytes" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
