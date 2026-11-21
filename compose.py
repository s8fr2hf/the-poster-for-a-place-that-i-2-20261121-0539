#!/usr/bin/env python3
"""Compose the Luminara travel poster: base art + poster typography."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "luminara-base.png")
OUT = os.path.join(HERE, "entry.png")

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

W = H = 1024

img = Image.open(BASE).convert("RGB").resize((W, H), Image.LANCZOS)

# Bottom gradient band: deep navy, transparent at top fading to solid at bottom.
band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(band)
band_top, band_bottom = 790, H
for y in range(band_top, band_bottom):
    t = (y - band_top) / (band_bottom - band_top)
    alpha = int(235 * (t ** 1.4))
    bd.line([(0, y), (W, y)], fill=(7, 14, 34, alpha))
img = Image.alpha_composite(img.convert("RGBA"), band)
d = ImageDraw.Draw(img)

CREAM = (246, 238, 220, 255)
GOLD = (232, 185, 90, 255)
SHADOW = (5, 10, 26, 255)

def text_center(y, text, font, fill):
    w = d.textlength(text, font=font)
    x = (W - w) / 2
    d.text((x + 3, y + 3), text, font=font, fill=SHADOW)
    d.text((x, y), text, font=font, fill=fill)
    return w

# Thin gold rule above the name
d.line([(W // 2 - 130, 838), (W // 2 + 130, 838)], fill=GOLD, width=3)

name_font = ImageFont.truetype(SERIF_BOLD, 96)
text_center(852, "LUMINARA", name_font, CREAM)

# Letterspaced tagline below the name, auto-fit to max width 920
tag = "WHERE THE SEA LIGHTS THE NIGHT"
for size, gap in ((25, 6), (22, 5), (20, 4), (18, 3)):
    tag_font = ImageFont.truetype(SANS_BOLD, size)
    tw = sum(d.textlength(ch, font=tag_font) for ch in tag) + gap * (len(tag) - 1) + 10 * tag.count(" ")
    if tw <= 920:
        break
x = (W - tw) / 2
y = 968
for ch in tag:
    adv = d.textlength(ch, font=tag_font) + (10 if ch == " " else gap)
    if ch != " ":
        d.text((x + 2, y + 2), ch, font=tag_font, fill=SHADOW)
        d.text((x, y), ch, font=tag_font, fill=GOLD)
    x += adv

rgb = img.convert("RGB")
rgb.save(os.path.join(HERE, "entry-full.png"), "PNG", optimize=True)
# Quantize to an adaptive 256-color palette so the file stays under the 1 MiB cap.
q = rgb.convert("P", palette=Image.ADAPTIVE, colors=256)
q.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
