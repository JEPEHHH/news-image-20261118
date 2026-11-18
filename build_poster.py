#!/usr/bin/env python3
"""Build the 1024x1024 front-page poster for 18 November 2026 (v3).

Design change vs v1/v2: a newspaper front page instead of a card grid.
Big serif lead headline, a stylised locator graphic, four briefs, an
"also today" strip. Everything is drawn from data below, no network.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (250, 249, 245)
INK = (18, 18, 20)
GREY = (92, 96, 104)
LIGHT = (214, 210, 200)
RED = (170, 28, 36)
NAVY = (18, 38, 62)
SEA = (28, 62, 96)
LAND = (196, 190, 176)

STORIES = [
    ("IRAN", "Iran's war widens as Kuwait intercepts 'hostile' drones",
     "The Gulf state says it shot the drones down as the conflict spreads across the region."),
    ("GAZA", "Ceasefire 'on the edge of collapse', board warns",
     "The Board of Peace says the truce could break within days as talks stall."),
    ("MARKETS", "Nvidia's record quarter, and a chief who will not return",
     "Bumper earnings land the same week the company confirms its chief executive stays away."),
    ("ISRAEL", "Knesset elects a speaker backed by the Arab bloc",
     "An ally of Eisenkot takes the chair in a shake-up of Israeli politics."),
]

ALSO = [
    "Congo: rival peace bids fail as the violence in the east goes on",
    "Ireland: a man is accused of 'destroying' a US military aircraft",
    "APEC: Trump heads to Shenzhen with the White House's shopping list",
]

LEAD_KICKER = "LEAD STORY  \u00b7  UKRAINE"
LEAD_HEAD = "Ukraine strikes the Kerch Bridge, the symbol of Putin's rule"
LEAD_DECK = ("Missiles hit the 19 km road-and-rail link to Crimea, cutting a Russian supply "
             "artery and landing the war's most symbolic blow in months.")
MAP_CAPTION = "Where the strike landed: the Kerch Strait link"

M = 40  # page margin


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if not cur or d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, path, max_w, max_lines, start, floor=11):
    size = start
    while size >= floor:
        fnt = font(path, size)
        lines = wrap(d, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, floor)
    lines = wrap(d, text, fnt, max_w)[:max_lines]
    return fnt, lines


def para(d, lines, fnt, x, y, fill, lead_gap=4):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + lead_gap
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- masthead -----------------------------------------------------------
d.rectangle([0, 0, W, 9], fill=RED)

kick = font(SANS_B, 19)
kick_txt = "WEDNESDAY  18 NOVEMBER 2026   \u00b7   LATE EDITION"
d.text(((W - d.textlength(kick_txt, font=kick)) / 2, 34), kick_txt, font=kick, fill=RED)

mast = font(SERIF_B, 76)
mast_txt = "THE WORLD TODAY"
while d.textlength(mast_txt, font=mast) > W - 2 * M and mast.size > 40:
    mast = font(SERIF_B, mast.size - 1)
d.text(((W - d.textlength(mast_txt, font=mast)) / 2, 62), mast_txt, font=mast, fill=INK)

y = 62 + mast.size + 14
d.rectangle([M, y, W - M, y + 3], fill=INK)
d.rectangle([M, y + 6, W - M, y + 7], fill=INK)
y += 22

sect = font(SANS_B, 15)
left_sect = "WORLD  \u00b7  POLITICS  \u00b7  MARKETS  \u00b7  TECH"
d.text((M, y), left_sect, font=sect, fill=GREY)
right_sect = "ONE PAGE  \u00b7  EIGHT STORIES"
d.text((W - M - d.textlength(right_sect, font=sect), y), right_sect, font=sect, fill=GREY)
y += 20
d.line([(M, y), (W - M, y)], fill=LIGHT, width=2)
y += 26

# --- lead story: text left, locator card right ---------------------------
CARD_W = 272
TEXT_W = W - 2 * M - CARD_W - 32

d.rectangle([M, y + 4, M + 5, y + 26], fill=RED)
d.text((M + 14, y + 6), LEAD_KICKER, font=font(SANS_B, 20), fill=RED)
y += 36

hf, hlines = fit(d, LEAD_HEAD, SERIF_B, TEXT_W, 3, 54)
lead_bottom_text = para(d, hlines, hf, M, y, INK, lead_gap=6)
dy = lead_bottom_text + 10
d.line([(M, dy - 4), (M + TEXT_W, dy - 4)], fill=LIGHT, width=2)
df, dlines = fit(d, LEAD_DECK, SANS_R, TEXT_W, 3, 20)
lead_bottom_text = para(d, dlines, df, M, dy + 8, GREY, lead_gap=5)

# illustration card: the bridge under strike
CY = y - 10
card_x0, card_y0 = W - M - CARD_W, CY
card_x1, card_y1 = W - M, CY + CARD_W
d.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=10, fill=NAVY)
inner_pad = 12
ix0, iy0 = card_x0 + inner_pad, card_y0 + inner_pad
ix1, iy1 = card_x1 - inner_pad, card_y1 - inner_pad
d.rectangle([ix0, iy0, ix1, iy1], fill=SEA)

# horizon + water lines
horizon = iy0 + int((iy1 - iy0) * 0.62)
d.rectangle([ix0, horizon, ix1, iy1], fill=(22, 50, 80))
for k in range(1, 7):
    wy = horizon + int((iy1 - horizon) * k / 7)
    d.line([(ix0 + 6, wy), (ix1 - 6, wy)], fill=(34, 66, 100), width=2)

# sky glow over the span
d.rectangle([ix0, iy0, ix1, horizon], fill=(26, 58, 92))

# bridge deck crossing the panel, slight rise in the middle
deck_l, deck_r = ix0 + 4, ix1 - 4
deck_y = int((iy0 + horizon) / 2) + 6
d.line([(deck_l, deck_y + 14), (ix0 + int(CARD_W * 0.30), deck_y),
        (ix0 + int(CARD_W * 0.52), deck_y - 8), (ix0 + int(CARD_W * 0.74), deck_y),
        (deck_r, deck_y + 14)], fill=(232, 228, 218), width=7, joint="curve")
# pylons
for frac in (0.14, 0.28, 0.42, 0.58, 0.72, 0.86):
    px = ix0 + int(CARD_W * frac)
    top = deck_y - 2 if frac != 0.52 else deck_y - 10
    d.line([(px, top), (px, horizon + 26)], fill=(232, 228, 218), width=4)
# cables
for frac in (0.20, 0.35, 0.48, 0.56, 0.70, 0.82):
    px = ix0 + int(CARD_W * frac)
    d.line([(px, horizon + 26), (px - 16, deck_y + 2)], fill=(150, 156, 168), width=1)
    d.line([(px, horizon + 26), (px + 16, deck_y + 2)], fill=(150, 156, 168), width=1)

# impact marker on the span
mx, my = ix0 + int(CARD_W * 0.52), deck_y - 8
for rad, col in ((38, (236, 120, 60)), (26, (240, 90, 50)), (14, (255, 220, 120))):
    d.polygon([(mx, my - rad), (mx + rad * 0.62, my - rad * 0.24), (mx + rad * 0.9, my + rad * 0.3),
               (mx + rad * 0.24, my + rad * 0.5), (mx + rad * 0.34, my + rad * 0.95),
               (mx - rad * 0.1, my + rad * 0.55), (mx - rad * 0.66, my + rad * 0.8),
               (mx - rad * 0.42, my + rad * 0.18), (mx - rad * 0.85, my - rad * 0.2),
               (mx - rad * 0.28, my - rad * 0.3)], fill=col)

lab = font(SANS_B, 15)
tag = "KERCH BRIDGE"
tw = d.textlength(tag, font=lab)
d.rectangle([ix0 + 8, iy1 - 34, ix0 + tw + 22, iy1 - 8], fill=RED)
d.text((ix0 + 14, iy1 - 31), tag, font=lab, fill=(255, 255, 255))
d.text((ix0 + 12, iy0 + 10), "STYLISED", font=font(SANS_B, 11), fill=(150, 176, 204))

cap_f, cap_lines = fit(d, MAP_CAPTION, SANS_R, CARD_W, 2, 16)
para(d, cap_lines, cap_f, W - M - CARD_W, CY + CARD_W + 8, GREY, lead_gap=2)

y = max(lead_bottom_text, CY + CARD_W + 8 + cap_f.size * len(cap_lines)) + 22
d.line([(M, y), (W - M, y)], fill=INK, width=3)
y += 18

# --- four briefs, two columns ------------------------------------------
COL_W = (W - 2 * M - 26) // 2
COL_X = [M, M + COL_W + 26]
grid_top = y
cur_y = grid_top
row_heights = []
for row in range(2):
    row_top = cur_y
    tallest = 0
    for col in range(2):
        i = row * 2 + col
        tag, head, body = STORIES[i]
        x = COL_X[col]
        d.text((x, row_top), tag, font=font(SANS_B, 14), fill=RED)
        hf2, hl = fit(d, head, SANS_B, COL_W, 3, 23)
        cy2 = para(d, hl, hf2, x, row_top + 18, INK, lead_gap=2)
        bf2, bl = fit(d, body, SANS_R, COL_W, 2, 16)
        cy2 = para(d, bl, bf2, x, cy2 + 5, GREY, lead_gap=2)
        tallest = max(tallest, cy2 - row_top)
    if row == 0:
        d.line([(M + COL_W + 13, row_top + 4), (M + COL_W + 13, row_top + tallest - 6)],
               fill=LIGHT, width=1)
    row_heights.append(tallest)
    cur_y = row_top + tallest + 20
y = cur_y + 2
d.line([(M, y), (W - M, y)], fill=INK, width=3)
y += 14

# --- also today --------------------------------------------------------
d.text((M, y), "ALSO TODAY", font=font(SANS_B, 16), fill=RED)
y += 22
af = font(SANS_R, 16)
for line in ALSO:
    d.ellipse([M + 2, y + 6, M + 8, y + 12], fill=RED)
    d.text((M + 16, y), line, font=af, fill=INK)
    y += af.size + 6

# --- footer -----------------------------------------------------------
d.line([(M, H - 52), (W - M, H - 52)], fill=LIGHT, width=2)
foot = font(SANS_R, 14)
foot_txt = "Every story cites a report published on 18 November 2026  \u00b7  sources in NEWS_SOURCES.md"
d.text((M, H - 40), foot_txt, font=foot, fill=GREY)
ftag = "make.fun bounty"
d.text((W - M - d.textlength(ftag, font=foot), H - 40), ftag, font=foot, fill=GREY)

print("bottom_before_footer", y, "footer_rule", H - 52)
assert y < H - 60, f"content overflows footer: {y}"
img.save("/root/work/mfk-ni19/entry3.png", "PNG", optimize=True)
print("saved 1024x1024")
