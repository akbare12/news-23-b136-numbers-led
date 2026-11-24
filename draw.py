#!/usr/bin/env python3
"""news-23 b136 numbers-led: draw THE WORLD TODAY, Monday 23 November 2026 (31 stories).
Numbers-led layout: BIG number grid first, then masthead blocks, heroes, cards, map, ALSO, DATE CHECK.
Output: entry.png 1024x1024, < 1 MiB.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
BG = (247, 242, 231)
INK = (18, 18, 18)
RED = (163, 22, 33)
GOLD = (176, 132, 30)
NAVY = (24, 52, 96)
GREEN = (30, 100, 55)
TEAL = (0, 105, 105)
PURPLE = (92, 52, 128)
BROWN = (146, 94, 20)
GREY = (96, 96, 96)
LIGHT = (232, 226, 210)
MAPGREEN = (190, 210, 170)
DARKNAVY = (16, 34, 66)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def tw(text, font):
    return d.textlength(text, font=font)


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrapped(x, y, text, font, max_w, fill=INK, leading=None, max_lines=None):
    lines = wrap(text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(font.size * 1.25)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(x, y, label, fill=NAVY):
    f = SANS_B(8)
    w = int(tw(label, f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return x + w


# ---------- MASTHEAD ----------
d.text((16, 6), "THE WORLD TODAY", font=SERIF_B(44), fill=INK)
d.text((W - 16 - tw("MONDAY 23 NOVEMBER 2026", SANS_B(15)), 22),
       "MONDAY 23 NOVEMBER 2026", font=SANS_B(15), fill=GOLD)
d.rectangle([0, 60, W, 64], fill=RED)
d.text((16, 68), "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
       font=SANS_B(11), fill=RED)

# ---------- BIG NUMBER GRID (first) ----------
NUMBERS = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"),
    ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"),
    ("165", "RUSSIAN MISSILES/WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
gy0 = 88
cell_w = 204
for i, (val, lab) in enumerate(NUMBERS):
    row, col = divmod(i, 5)
    x = 16 + col * cell_w
    y = gy0 + row * 52
    d.text((x, y), val, font=SANS_B(22), fill=INK)
    d.text((x, y + 26), lab, font=SANS_B(9), fill=GREY)
d.line([16, gy0 + 104, W - 16, gy0 + 104], fill=(200, 192, 172), width=1)

# ---------- REGION BAR ----------
REGIONS = [("ASIA-PACIFIC 7", 231, NAVY), ("AMERICAS 8", 264, RED),
           ("MIDDLE EAST 6", 198, GREEN), ("EUROPE 5", 165, TEAL),
           ("AFRICA 3", 99, BROWN), ("WORLD 2", 67, PURPLE)]
rx = 0
ry = 198
for name, wdt, col in REGIONS:
    d.rectangle([rx, ry, rx + wdt, ry + 20], fill=col)
    d.text((rx + 8, ry + 4), name, font=SANS_B(10), fill=(255, 255, 255))
    rx += wdt
d.text((16, 222), "THE DAY IN UTC   ~00:00 Kospi dives   ~05:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
       font=SANS(10), fill=GREY)
d.text((W - 16 - tw("~ APPROX", SANS(9)), 222), "~ APPROX", font=SANS(9), fill=GREY)

# ---------- HEROES ----------
HY = 240
HCOL = 336
heroes = [
    dict(kind="kospi"),
    dict(kind="guterres"),
    dict(kind="power"),
]
for i, h in enumerate(heroes):
    x0 = 8 + i * HCOL
    x1 = x0 + 320
    if h["kind"] == "kospi":
        d.rectangle([x0, HY, x1, HY + 118], fill=DARKNAVY)
        # skyline
        import random
        random.seed(7)
        bx = x0 + 8
        while bx < x1 - 14:
            bw = random.randint(14, 26)
            bh = random.randint(34, 62)
            d.rectangle([bx, HY + 118 - bh, bx + bw, HY + 118], fill=(38, 62, 100))
            for wy in range(HY + 118 - bh + 5, HY + 112, 9):
                for wx in range(bx + 3, bx + bw - 3, 7):
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
            bx += bw + 4
        d.text((x0 + 10, HY + 8), "-3.3%", font=SANS_B(34), fill=(255, 255, 255))
        pts = [(x0 + 150, HY + 26), (x0 + 185, HY + 44), (x0 + 215, HY + 40),
               (x0 + 250, HY + 62), (x0 + 285, HY + 58), (x0 + 312, HY + 84)]
        d.line(pts, fill=(255, 140, 40), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
        d.rectangle([x0, HY + 100, x1, HY + 118], fill=(10, 22, 46))
        d.text((x0 + 8, HY + 104), "KOSPI 4,708.54  ·  -161 PTS  ·  SAMSUNG -3.1%  ·  HYNIX -2.5%",
               font=SANS_B(8), fill=(255, 255, 255))
    elif h["kind"] == "guterres":
        d.rectangle([x0, HY, x1, HY + 118], fill=GREEN)
        d.text((x0 + 10, HY + 10), "150", font=SANS_B(40), fill=(255, 214, 90))
        d.text((x0 + 104, HY + 14), "DELEGATES", font=SANS_B(15), fill=(255, 214, 90))
        d.text((x0 + 104, HY + 34), "BACK A RISK", font=SANS_B(15), fill=(255, 214, 90))
        d.text((x0 + 104, HY + 54), "FRAMEWORK", font=SANS_B(15), fill=(255, 214, 90))
        # globe
        cx, cy, r = x0 + 268, HY + 62, 42
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 232, 214))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
        d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(140, 180, 140), width=1)
        d.line([cx - r, cy, cx + r, cy], fill=(140, 180, 140), width=1)
        d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(140, 180, 140), width=1)
        d.rectangle([x0, HY + 100, x1, HY + 118], fill=(18, 70, 38))
        d.text((x0 + 8, HY + 104), "BRIDGETOWN SUMMIT, BARBADOS",
               font=SANS_B(8), fill=(255, 255, 255))
    else:
        d.rectangle([x0, HY, x1, HY + 118], fill=(238, 232, 214))
        d.text((x0 + 10, HY + 6), "NARROWEST SINCE 2018", font=SANS_B(11), fill=INK)
        d.text((x1 - 8 - tw("GAP 5.3", SANS_B(11)), HY + 6), "GAP 5.3", font=SANS_B(11), fill=RED)
        bars = [("78.9", "US", NAVY, 250), ("73.6", "CHINA", RED, 236), ("40.5", "INDIA", GOLD, 130)]
        by = HY + 28
        for val, lab, col, bw in bars:
            d.text((x0 + 10, by), val, font=SANS_B(12), fill=INK)
            d.rectangle([x0 + 58, by + 2, x0 + 58 + bw, by + 14], fill=col)
            d.text((x0 + 58 + bw - 34, by + 3), lab, font=SANS_B(9), fill=(255, 255, 255))
            by += 22
        d.rectangle([x0, HY + 100, x1, HY + 118], fill=(60, 52, 30))
        d.text((x0 + 8, HY + 104), "ASIA POWER INDEX 2026  ·  LOWY INSTITUTE",
               font=SANS_B(8), fill=(255, 255, 255))

hero_text = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
hy_text = HY + 124
for i, (head, body, src) in enumerate(hero_text):
    x0 = 8 + i * HCOL
    y = wrapped(x0, hy_text, head, SANS_B(16), 318, leading=19, max_lines=2)
    y = wrapped(x0, y + 2, body, SANS(10), 318, leading=13, max_lines=2)
    d.text((x0, y + 3), src, font=SANS(8), fill=GREY)
    chip(x1 - 66 if False else x0 + 318 - 66, y + 2, "REPORTED", NAVY)

# ---------- CARDS ----------
CY = 452
d.rectangle([0, CY, W, CY + 22], fill=INK)
d.text((16, CY + 4), "MORE OF THE DAY  —  10 STORIES", font=SANS_B(12), fill=(255, 255, 255))
cards = [
    ("1", "AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
    ("2", "AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("3", "WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("4", "MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("5", "SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
    ("6", "SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("7", "LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("8", "TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("9", "EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("10", "SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
cw = 200
for i, (num, cat, head, body, src, tag) in enumerate(cards):
    row, col = divmod(i, 5)
    x0 = 8 + col * 204
    y0 = CY + 28 + row * 78
    d.text((x0, y0), num, font=SANS_B(11), fill=RED)
    d.text((x0 + 20, y0), cat, font=SANS_B(9), fill=RED)
    y = wrapped(x0, y0 + 15, head, SANS_B(11), 192, leading=13, max_lines=2)
    y = wrapped(x0, y + 1, body, SANS(9), 192, leading=11, max_lines=1)
    d.text((x0, y0 + 60), src, font=SANS(8), fill=GREY)
    chip(x0 + 192 - 62, y0 + 58, tag, NAVY if tag == "REPORTED" else RED)

# ---------- MAP + ALSO ----------
MY = 640
d.rectangle([0, MY, W, MY + 22], fill=INK)
d.text((16, MY + 4), "WHERE IT HAPPENED", font=SANS_B(12), fill=(255, 255, 255))
map_x0, map_y0, map_x1, map_y1 = 16, MY + 30, 436, MY + 30 + 170
# stylised blobs
d.ellipse([map_x0 + 6, map_y0 + 30, map_x0 + 130, map_y0 + 150], fill=MAPGREEN)   # Americas
d.ellipse([map_x0 + 150, map_y0 + 6, map_x0 + 344, map_y0 + 130], fill=MAPGREEN)  # Eurasia
d.ellipse([map_x0 + 310, map_y0 + 55, map_x0 + 400, map_y0 + 165], fill=MAPGREEN)  # Africa/Asia
pins = [
    (1, 336, 706), (2, 92, 770), (3, 308, 696), (4, 52, 716), (5, 70, 716),
    (6, 250, 700), (7, 218, 700), (8, 212, 690), (9, 262, 716), (10, 232, 692),
    (11, 258, 738), (12, 276, 752), (13, 348, 786),
]
for num, px, py in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px - 3 if num < 10 else px - 6, py - 6), str(num), font=SANS_B(9), fill=(255, 255, 255))
d.text((map_x0, map_y1 + 4), "Pins 1–13:  1 Seoul  ·  2 Bridgetown  ·  3 Beijing  ·  4 Washington", font=SANS(9), fill=INK)
d.text((map_x0, map_y1 + 17), "5 New York  ·  6 Kyiv  ·  7 Paris  ·  8 London  ·  9 Warsaw  ·  10 Manchester", font=SANS(9), fill=INK)
d.text((map_x0, map_y1 + 30), "11 Beirut  ·  12 Gaza  ·  13 Khartoum", font=SANS(9), fill=INK)

also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe [CLAIM]",
    "25. Sudan: defences down drones [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits over AI exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
ax = 452
d.text((ax, MY + 30), "ALSO ON MONDAY", font=SANS_B(12), fill=INK)
for i, item in enumerate(also):
    col = 0 if i < 9 else 1
    row = i % 9
    x = ax + col * 288
    y = MY + 52 + row * 17
    d.text((x, y), item, font=SANS(10), fill=INK)

# ---------- DATE CHECK ----------
DY = 892
d.rectangle([8, DY, W - 8, DY + 66], outline=RED, width=2)
d.text((16, DY + 5), "DATE CHECK  —  READ 23 NOV 2026, 23:59 UTC  ·  STORIES DATED 23 NOV ONLY",
       font=SANS_B(11), fill=RED)
d.text((16, DY + 24), "LEFT OUT — NOT 23 NOV:  Dems reach 258 (22 Nov)  ·  Sparta II fire (22 Nov)  ·  El Chapo Isidro captured (22 Nov)",
       font=SANS(10), fill=INK)
d.text((16, DY + 38), "EU–Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  ICJ Myanmar ruling (19 Nov)",
       font=SANS(10), fill=INK)
d.text((16, DY + 52), "NOT YET — Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff",
       font=SANS(10), fill=INK)

# ---------- FOOTER ----------
FY = 966
d.text((16, FY), "Sources: Reuters  ·  AP  ·  Bloomberg  ·  AFP  ·  Yonhap  ·  BBC  ·  WSJ  ·  ESPN  ·  Lowy Institute (Asia Power Index 2026).",
       font=SANS(9), fill=GREY)
d.text((16, FY + 13), "CHIPS: REPORTED = confirmed by wires  ·  CLAIM = one side's claim, independently unconfirmed  ·  ONGOING = still developing.",
       font=SANS(9), fill=GREY)
d.text((16, FY + 26), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=SANS(9), fill=GREY)
d.line([16, FY + 42, W - 16, FY + 42], fill=GOLD, width=2)
d.text(((W - tw("THE WORLD TODAY  ·  Monday 23 November 2026  ·  31 stories  ·  6 regions", SANS_B(11))) // 2, FY + 47),
       "THE WORLD TODAY  ·  Monday 23 November 2026  ·  31 stories  ·  6 regions",
       font=SANS_B(11), fill=GOLD)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
