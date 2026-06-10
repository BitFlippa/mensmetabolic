#!/usr/bin/env python3
"""
Generate branded Open Graph share images (1200x630 PNG) into static/images/.

These are committed static assets, copied verbatim into dist/ by the build,
so the site build itself needs no image dependencies. Re-run this only when
branding, prices, or messaging change:

    pip install Pillow
    python3 tools/make_og.py

Pulls live price/state values from src/build.py so the cards stay in sync.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "static", "images")
os.makedirs(OUT, exist_ok=True)

# Pull live config from the build so OG text matches the site.
sys.path.insert(0, os.path.join(ROOT, "src"))
import build as B  # noqa: E402

PRICE = B.PRICE_VISIT
MEMBER = B.PRICE_MEMBER
STATES = B.states_phrase()

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_BOLD = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")

W, H = 1200, 630
PAD = 84

# Brand colors
TEAL = (14, 124, 134)
TEAL_DARK = (8, 58, 64)
MINT = (31, 184, 160)
MINT_LT = (159, 232, 221)
WHITE = (255, 255, 255)


def gradient(w, h, top, bottom):
    base = Image.new("RGB", (w, h), top)
    draw = ImageDraw.Draw(base)
    for y in range(h):
        t = y / (h - 1)
        # diagonal-ish: blend toward bottom and slightly darker right handled by glow
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return base


def radial_glow(img, cx, cy, radius, color, max_alpha=70):
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    steps = 60
    for i in range(steps, 0, -1):
        rr = int(radius * i / steps)
        a = int(max_alpha * (1 - i / steps))
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color + (a,))
    img.alpha_composite(glow)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def make(name, headline, sub):
    img = gradient(W, H, TEAL, TEAL_DARK).convert("RGBA")
    radial_glow(img, int(W * 0.86), int(H * 0.12), 460, MINT, 60)
    d = ImageDraw.Draw(img)

    # left accent bar
    d.rounded_rectangle([PAD, 250, PAD + 10, 250 + 168], radius=5, fill=MINT)

    # wordmark (dot + name) top-left
    f_word = ImageFont.truetype(SERIF_BOLD, 40)
    dot_r = 12
    cy = 92
    d.ellipse([PAD, cy - dot_r, PAD + dot_r * 2, cy + dot_r], fill=MINT)
    d.text((PAD + dot_r * 2 + 16, cy - 28), "Men's Metabolic", font=f_word, fill=WHITE)

    # headline (serif, wrapped)
    f_head = ImageFont.truetype(SERIF_BOLD, 70)
    body_x = PAD + 34
    lines = wrap(d, headline, f_head, W - body_x - PAD)
    y = 250
    for ln in lines:
        d.text((body_x, y), ln, font=f_head, fill=WHITE)
        y += 80

    # subline (sans, mint)
    f_sub = ImageFont.truetype(SANS, 31)
    y += 8
    for ln in wrap(d, sub, f_sub, W - body_x - PAD):
        d.text((body_x, y), ln, font=f_sub, fill=MINT_LT)
        y += 42

    # url bottom-left
    f_url = ImageFont.truetype(SANS_BOLD, 28)
    d.text((PAD, H - 78), "mensmetabolic.com", font=f_url, fill=(255, 255, 255))

    img.convert("RGB").save(os.path.join(OUT, name + ".png"), "PNG", optimize=True)
    print("wrote", name + ".png")


CARDS = {
    "og-cover":       ("Men's metabolic & hormone health, by video",
                       f"GLP-1 weight loss · Testosterone · ED · {STATES}"),
    "og-home":        ("Men's metabolic health, backed by real medicine",
                       f"Board-certified physicians · Flat ${PRICE} · {STATES}"),
    "og-mens-health": ("Men's health telehealth, GLP-1, TRT & ED",
                       f"Board-certified physicians · Lab-guided · {STATES}"),
    "og-weight-loss": ("GLP-1 weight loss for men",
                       "Semaglutide & tirzepatide · Lab-guided · Physician-led"),
    "og-trt":         ("Testosterone therapy (TRT), done right",
                       f"Lab-confirmed · Physician-monitored · {STATES}"),
    "og-ed":          ("Discreet ED treatment online",
                       "Private visits · Proven options · Sent to your pharmacy"),
    "og-pricing":     ("Simple, transparent pricing",
                       f"Flat ${PRICE} visit · ${MEMBER}/mo membership · No insurance"),
    "og-eligibility": ("Am I a fit? A 60-second check",
                       "Private · No obligation · GLP-1, TRT & ED"),
}

if __name__ == "__main__":
    for nm, (hl, sb) in CARDS.items():
        make(nm, hl, sb)
    print(f"\nDone. {len(CARDS)} OG images in {OUT}")
