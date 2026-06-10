#!/usr/bin/env python3
"""
Men's Metabolic -- Static Site Generator
Men's metabolic and hormone health telehealth website (mensmetabolic.com).

Generates a complete production-ready static HTML website into dist/.

Usage:
    python3 src/build.py

Pages:
    - Homepage
    - How It Works
    - What We Treat (conditions hub)
    - Pricing & Membership
    - About
    - FAQ
    - Contact / Book a Visit
    - Thank You
    - Privacy Policy, Terms of Use, Telehealth Consent
    - sitemap.xml, robots.txt
"""

import os
import sys
import json
import html as html_mod
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")
# Committed static files (pre-generated OG images, etc.) copied verbatim into
# dist/. Keeps the build dependency-free, no Pillow needed at deploy time.
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

CURRENT_YEAR = datetime.now().year
CURRENT_DATE = datetime.now().strftime("%B %-d, %Y") if os.name != "nt" else datetime.now().strftime("%B %d, %Y")

# ---------------------------------------------------------------------------
# BUSINESS CONFIG  ***  EDIT THESE WITH REAL DATA BEFORE GOING LIVE  ***
# Anything marked TODO is a reasonable placeholder and must be verified.
# ---------------------------------------------------------------------------
SITE_NAME = "Men's Metabolic"
BASE_URL = "https://www.mensmetabolic.com"

BUSINESS = {
    "name": SITE_NAME,
    "legal_name": "Men's Metabolic, PLLC",            # TODO confirm legal entity
    "tagline": "Men's metabolic and hormone health, by video.",
    "phone": "(000) 000-0000",                   # TODO real phone
    "email": "hello@mensmetabolic.com",             # TODO real inbox
    # States where the physician(s) are licensed to practice telemedicine.
    # Telehealth law requires the patient be physically located in a state
    # the treating physician is licensed in. EDIT to your real footprint.
    "states_licensed": ["Florida"],              # TODO real licensed states
    "founded": "2024",                           # TODO confirm
    # Pricing -- direct pay, no insurance. EDIT to your real prices.
    "price_visit": "89",                         # one-time video visit, USD
    "price_membership_mo": "49",                 # monthly membership, USD
    "price_membership_annual": "468",            # annual (=$39/mo equiv) TODO
    "hours": "7:00 AM - 9:00 PM, 7 days a week", # TODO confirm availability
    # Set True only once you have a real, verifiable rating to show.
    "show_rating": False,
    "rating": "4.9",
    "review_count": "0",
    # Social / profile URLs (populate sameAs in schema when available)
    "facebook_url": "",
    "instagram_url": "",
    "linkedin_url": "",
    "logo_url": BASE_URL + "/images/logo.svg",
    "og_image_url": BASE_URL + "/images/og-cover.png",
}

PHONE_TEL = "+1" + "".join(c for c in BUSINESS["phone"] if c.isdigit())
PHONE_DISPLAY = BUSINESS["phone"]
PRICE_VISIT = BUSINESS["price_visit"]
PRICE_MEMBER = BUSINESS["price_membership_mo"]

# The external scheduling / patient-portal link. Point this at your real
# booking system (e.g. a HIPAA-compliant scheduler). Until set, "Book" CTAs
# route to the on-site contact form.
BOOKING_URL = "/contact/"                        # TODO real scheduler URL

page_count = 0


def states_phrase():
    states = BUSINESS["states_licensed"]
    if not states:
        return "select states"
    if len(states) == 1:
        return states[0]
    if len(states) == 2:
        return f"{states[0]} and {states[1]}"
    return ", ".join(states[:-1]) + f", and {states[-1]}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def e(text):
    return html_mod.escape(str(text))


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def sanitize_html(text):
    """Strip AI-tell punctuation so no em/en dashes ship."""
    text = text.replace(" — ", ", ").replace("—", ", ")
    text = text.replace("&mdash; ", ", ").replace("&mdash;", ", ")
    text = text.replace(" – ", "-").replace("–", "-").replace("&ndash;", "-")
    text = text.replace(" ,", ",").replace(",  ", ", ").replace(", ,", ",")
    return text


def write_page(path_parts, content):
    """path_parts: list of path segments under dist/. Writes index.html style."""
    global page_count
    if isinstance(path_parts, str):
        full = os.path.join(DIST_DIR, path_parts)
    else:
        full = os.path.join(DIST_DIR, *path_parts)
    if full.endswith(".html"):
        content = sanitize_html(content)
    ensure_dir(os.path.dirname(full))
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    page_count += 1


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
FULL_CSS = """
:root{
  /* ── Ink / neutrals — deep premium midnight navy ── */
  --ink:#0A1A2A;
  --ink-2:#0E2738;
  --ink-soft:#51677B;
  --ink-mute:#7B8C9B;

  /* ── Brand teal ── */
  --teal:#0E7C86;
  --teal-600:#0C6A73;
  --teal-700:#0A535A;
  --teal-50:#EBF5F5;
  --teal-100:#D6ECEC;
  --teal-light:#EBF5F5;
  --teal-dark:#0A535A;
  --mint:#23C0A6;

  /* ── Premium metallic accent (the signature cue) ── */
  --copper:#BE844A;
  --copper-2:#A86F38;
  --copper-soft:#E6CBA6;
  --gold:#D6A560;

  /* ── Surfaces ── */
  --paper:#F7F4ED;      /* warm paper */
  --sand:#F7F4ED;
  --cloud:#EFF5F7;      /* cool mist */
  --white:#fff;

  /* ── Lines ── */
  --line:color-mix(in srgb, var(--ink) 9%, transparent);
  --line-2:color-mix(in srgb, var(--ink) 14%, transparent);

  /* ── Elevation — layered, premium depth ── */
  --shadow-sm:0 1px 2px rgba(10,26,42,.05), 0 2px 7px rgba(10,26,42,.05);
  --shadow:0 2px 8px rgba(10,26,42,.05), 0 10px 26px rgba(10,26,42,.08);
  --shadow-lg:0 8px 24px rgba(10,26,42,.08), 0 28px 56px rgba(10,26,42,.14);
  --shadow-xl:0 16px 40px rgba(10,26,42,.12), 0 48px 96px rgba(10,26,42,.22);
  --shadow-copper:0 12px 30px rgba(150,100,45,.20);

  --font:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
  --font-d:'Fraunces','Georgia',serif;

  --radius:18px;
  --radius-sm:12px;
  --radius-lg:26px;
  --t:.28s cubic-bezier(.4,0,.2,1);
  --t-spring:.55s cubic-bezier(.16,1,.3,1);
  --max:1180px;
}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:var(--font);color:var(--ink);background:var(--white);line-height:1.65;font-size:17px;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;font-feature-settings:"cv05","ss01";overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
a{color:var(--teal);text-decoration:none;transition:color var(--t)}
a:hover{color:var(--teal-dark)}

h1,h2,h3,h4{font-family:var(--font-d);font-weight:550;line-height:1.08;color:var(--ink);letter-spacing:-.018em}
h1{font-size:clamp(2.5rem,5.6vw,4.15rem);font-weight:500}
h2{font-size:clamp(1.85rem,3.9vw,2.85rem)}
h3{font-size:clamp(1.2rem,2.2vw,1.55rem)}
p{color:var(--ink-soft)}
.container{max-width:var(--max);margin:0 auto;padding:0 24px}
.center{text-align:center}
h1,h2,h3,.quiz-q{text-wrap:balance}
p,li,.hero-sub,.lead{text-wrap:pretty}
section[id],div[id]{scroll-margin-top:92px}

/* Skip link */
.skip{position:absolute;left:-999px;top:0;z-index:2000;background:var(--ink);color:#fff;padding:12px 20px;border-radius:0 0 12px 0;font-weight:600;font-size:.9rem}
.skip:focus{left:0;color:#fff}

/* Fine grain texture — premium tactile surface */
.grain{position:relative}
.grain::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:0;opacity:.5;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.4'/%3E%3C/svg%3E")}
.grain>*{position:relative;z-index:1}

/* ── NAV ── */
.nav{position:fixed;top:0;left:0;right:0;z-index:1000;background:color-mix(in srgb,#fff 80%,transparent);backdrop-filter:saturate(180%) blur(16px);-webkit-backdrop-filter:saturate(180%) blur(16px);border-bottom:1px solid transparent;height:74px;transition:border-color var(--t),box-shadow var(--t),background var(--t)}
.nav.scrolled{border-bottom-color:var(--line);box-shadow:0 6px 24px rgba(10,26,42,.06);background:color-mix(in srgb,#fff 90%,transparent)}
.nav-inner{max-width:var(--max);margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:100%}
.nav-logo{font-family:var(--font-d);font-size:1.5rem;font-weight:550;color:var(--ink);letter-spacing:-.02em;display:flex;align-items:center;gap:10px}
.nav-logo .dot{width:13px;height:13px;border-radius:50%;background:radial-gradient(circle at 32% 30%,var(--mint),var(--teal));box-shadow:0 0 0 4px var(--teal-light),0 1px 3px rgba(14,124,134,.4)}
.nav-logo b{color:var(--teal);font-weight:550}
.nav-links{display:flex;align-items:center;gap:2px;list-style:none}
.nav-links>li>a{color:var(--ink);font-weight:500;font-size:.94rem;padding:9px 14px;border-radius:10px;transition:all var(--t);position:relative}
.nav-links>li>a:hover{color:var(--teal);background:var(--teal-light)}
.nav-cta{background:var(--ink)!important;color:#fff!important;font-weight:600;padding:11px 22px!important;border-radius:100px!important;box-shadow:0 4px 14px rgba(10,26,42,.22);transition:all var(--t)!important}
.nav-cta:hover{background:var(--teal)!important;transform:translateY(-1px);box-shadow:0 8px 22px rgba(14,124,134,.34)}
.nav-toggle{display:none;background:none;border:none;color:var(--ink);font-size:1.5rem;cursor:pointer;padding:8px;line-height:1}

/* ── HERO ── */
.hero{padding:148px 0 88px;position:relative;overflow:hidden;
  background:
    radial-gradient(120% 90% at 88% -10%, rgba(35,192,166,.18) 0%, transparent 55%),
    radial-gradient(80% 70% at 10% 5%, rgba(14,124,134,.12) 0%, transparent 50%),
    radial-gradient(60% 80% at 95% 110%, rgba(190,132,74,.10) 0%, transparent 55%),
    linear-gradient(178deg,var(--teal-light) 0%,#fff 62%)}
.hero::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.5;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.35'/%3E%3C/svg%3E")}
.hero .container{position:relative;z-index:1}
.hero-grid{display:grid;grid-template-columns:1.08fr .92fr;gap:60px;align-items:center}
.eyebrow{display:inline-flex;align-items:center;gap:9px;font-size:.78rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);background:rgba(255,255,255,.7);border:1px solid var(--line);padding:8px 16px;border-radius:100px;margin-bottom:26px;box-shadow:var(--shadow-sm);backdrop-filter:blur(6px)}
.eyebrow .dot{width:7px;height:7px;border-radius:50%;background:var(--copper);box-shadow:0 0 0 3px color-mix(in srgb,var(--copper) 22%,transparent)}
.hero h1{margin-bottom:24px;letter-spacing:-.028em}
.hero h1 em{font-style:italic;color:var(--teal);font-weight:500}
.hero-sub{font-size:1.2rem;line-height:1.62;max-width:545px;margin-bottom:34px;color:var(--ink-soft)}
.hero-cta-row{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:32px}
.hero-trust{display:flex;flex-wrap:wrap;gap:11px 24px;font-size:.92rem;color:var(--ink-soft);font-weight:500}
.hero-trust span{display:inline-flex;align-items:center;gap:8px}
.hero-trust svg{flex-shrink:0;color:var(--teal)}

/* Hero card — layered premium depth */
.hero-card{background:linear-gradient(180deg,#fff 0%,#FCFBF8 100%);border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow-xl);padding:34px;position:relative}
.hero-card::before{content:"";position:absolute;inset:0;border-radius:24px;padding:1px;background:linear-gradient(160deg,rgba(255,255,255,.9),transparent 40%);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.hero-card .price-pop{position:absolute;top:-19px;right:26px;background:linear-gradient(135deg,var(--copper),var(--copper-2));color:#fff;font-weight:700;font-size:.86rem;letter-spacing:.01em;padding:9px 18px;border-radius:100px;box-shadow:var(--shadow-copper)}
.hero-card h3{font-family:var(--font);font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--teal);margin-bottom:6px}
.hero-card .muted{font-family:var(--font-d);font-size:1.32rem;font-weight:500;letter-spacing:-.01em;color:var(--ink);line-height:1.25;margin-bottom:22px}
.checklist{list-style:none;display:flex;flex-direction:column;gap:14px;margin-bottom:26px}
.checklist li{display:flex;gap:12px;align-items:flex-start;font-size:.97rem;color:var(--ink);line-height:1.45}
.checklist .ck{flex-shrink:0;width:23px;height:23px;border-radius:50%;background:var(--teal-light);color:var(--teal);display:flex;align-items:center;justify-content:center;margin-top:1px;box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--teal) 18%,transparent)}

/* ── BUTTONS ── */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font-weight:600;font-size:1rem;padding:15px 28px;border-radius:100px;cursor:pointer;border:none;transition:all var(--t);font-family:var(--font);line-height:1;letter-spacing:.005em;position:relative}
.btn-primary{background:linear-gradient(180deg,var(--teal) 0%,var(--teal-600) 100%);color:#fff;box-shadow:0 1px 0 rgba(255,255,255,.18) inset,0 8px 20px rgba(14,124,134,.26)}
.btn-primary:hover{color:#fff;transform:translateY(-2px);box-shadow:0 1px 0 rgba(255,255,255,.18) inset,0 14px 30px rgba(14,124,134,.36)}
.btn-dark{background:linear-gradient(180deg,var(--ink-2) 0%,var(--ink) 100%);color:#fff;box-shadow:0 8px 20px rgba(10,26,42,.24)}
.btn-dark:hover{color:#fff;transform:translateY(-2px);box-shadow:0 14px 30px rgba(10,26,42,.32)}
.btn-ghost{background:#fff;color:var(--ink);border:1.5px solid var(--line-2)}
.btn-ghost:hover{border-color:var(--teal);color:var(--teal-dark);transform:translateY(-1px);box-shadow:var(--shadow-sm)}
.btn-light{background:#fff;color:var(--teal)}
.btn-light:hover{background:var(--sand);color:var(--teal-dark);transform:translateY(-2px);box-shadow:var(--shadow-lg)}
.btn-block{width:100%}
.btn-lg{padding:17px 34px;font-size:1.05rem}

/* ── SECTIONS ── */
.section{padding:96px 0;position:relative}
.section-sand{background:var(--sand)}
.section-cloud{background:var(--cloud)}
.section-teal{background:linear-gradient(155deg,var(--ink) 0%,var(--teal-700) 58%,var(--teal-600) 100%);color:#fff;position:relative;overflow:hidden}
.section-teal::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(60% 80% at 85% 10%,rgba(35,192,166,.18),transparent 60%),radial-gradient(50% 70% at 5% 100%,rgba(190,132,74,.14),transparent 60%)}
.section-teal>*{position:relative;z-index:1}
.section-header{max-width:680px;margin:0 auto 60px;text-align:center}
.section-label{display:inline-flex;align-items:center;gap:9px;font-size:.76rem;font-weight:700;text-transform:uppercase;letter-spacing:.13em;color:var(--copper-2);margin-bottom:16px}
.section-label::before{content:"";width:22px;height:1.5px;background:linear-gradient(90deg,transparent,var(--copper))}
.section-label::after{content:"";width:22px;height:1.5px;background:linear-gradient(90deg,var(--copper),transparent)}
.section-teal .section-label{color:var(--gold)}
.section-header p{font-size:1.13rem;line-height:1.6;margin-top:16px;color:var(--ink-soft)}
.section-teal h2,.section-teal h3{color:#fff}
.section-teal p{color:rgba(255,255,255,.82)}

/* ── GRID + CARDS ── */
.grid{display:grid;gap:24px}
.grid-2{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.grid-3{grid-template-columns:repeat(auto-fit,minmax(290px,1fr))}
.grid-4{grid-template-columns:repeat(auto-fit,minmax(232px,1fr))}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:32px;transition:transform var(--t),box-shadow var(--t),border-color var(--t);position:relative}
.card:hover{transform:translateY(-5px);box-shadow:var(--shadow-lg);border-color:color-mix(in srgb,var(--teal) 26%,transparent)}
.card .ic{width:54px;height:54px;border-radius:15px;background:linear-gradient(160deg,var(--teal-light),#fff);color:var(--teal);display:flex;align-items:center;justify-content:center;margin-bottom:20px;box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--teal) 14%,transparent)}
.card h3{font-size:1.22rem;margin-bottom:10px}
.card p{font-size:.96rem;line-height:1.62}

/* ── STEPS — editorial numbered ── */
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(242px,1fr));gap:30px;counter-reset:step}
.step{position:relative;padding-top:10px}
.step .num{width:58px;height:58px;border-radius:50%;background:#fff;border:1.5px solid color-mix(in srgb,var(--teal) 30%,transparent);color:var(--teal);font-family:var(--font-d);font-size:1.5rem;font-weight:550;display:flex;align-items:center;justify-content:center;margin-bottom:20px;box-shadow:var(--shadow-sm),inset 0 0 0 5px #fff}
.section-sand .step .num{box-shadow:var(--shadow-sm),inset 0 0 0 5px var(--sand)}
.step h3{font-size:1.22rem;margin-bottom:9px}
.step p{font-size:.96rem}

/* ── CONDITIONS ── */
.cond-cats{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:26px}
.cond-cat{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:32px;transition:transform var(--t),box-shadow var(--t),border-color var(--t)}
.cond-cat:hover{transform:translateY(-5px);box-shadow:var(--shadow-lg);border-color:color-mix(in srgb,var(--teal) 24%,transparent)}
.cond-cat h3{font-size:1.28rem;margin-bottom:8px;display:flex;align-items:center;gap:12px}
.cond-cat .ic{width:46px;height:46px;border-radius:13px;background:linear-gradient(160deg,var(--teal-light),#fff);color:var(--teal);display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--teal) 14%,transparent)}
.cond-cat>p{font-size:.94rem;margin-bottom:18px;line-height:1.6}
.tags{display:flex;flex-wrap:wrap;gap:8px;list-style:none}
.tags li{font-size:.86rem;font-weight:500;color:var(--ink-soft);background:var(--cloud);border:1px solid var(--line);padding:6px 13px;border-radius:100px;transition:all var(--t)}
.cond-cat:hover .tags li{border-color:color-mix(in srgb,var(--teal) 18%,transparent)}

/* ── PRICING ── */
.price-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px;max-width:880px;margin:0 auto;align-items:stretch}
.price-card{background:#fff;border:1px solid var(--line);border-radius:22px;padding:38px 34px;display:flex;flex-direction:column;position:relative;transition:transform var(--t),box-shadow var(--t)}
.price-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg)}
.price-card.featured{border:1.5px solid color-mix(in srgb,var(--teal) 40%,transparent);box-shadow:var(--shadow-lg);background:linear-gradient(180deg,#fff,#FCFBF8)}
.price-card.featured::before{content:"";position:absolute;inset:0;border-radius:22px;padding:1.5px;background:linear-gradient(160deg,var(--teal),transparent 55%);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.price-card .ribbon{position:absolute;top:-15px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,var(--copper),var(--copper-2));color:#fff;font-size:.74rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:7px 18px;border-radius:100px;box-shadow:var(--shadow-copper)}
.price-card h3{font-family:var(--font);font-size:.84rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-soft);margin-bottom:10px}
.price-card .price{font-family:var(--font-d);font-size:3.4rem;font-weight:500;color:var(--ink);line-height:1;margin:8px 0 6px;letter-spacing:-.02em}
.price-card .price small{font-family:var(--font);font-size:1rem;font-weight:500;color:var(--ink-soft);letter-spacing:0}
.price-card .blurb{font-size:.94rem;margin-bottom:24px;min-height:44px;line-height:1.55}
.price-card ul{list-style:none;display:flex;flex-direction:column;gap:13px;margin-bottom:28px;flex:1}
.price-card li{display:flex;gap:11px;align-items:flex-start;font-size:.95rem;color:var(--ink)}
.price-card li .ck{color:var(--teal);font-weight:800;flex-shrink:0;margin-top:1px}

/* ── FAQ ── */
.faq-list{max-width:800px;margin:0 auto}
.faq-item{border:1px solid var(--line);border-radius:var(--radius-sm);margin-bottom:13px;background:#fff;overflow:hidden;transition:box-shadow var(--t),border-color var(--t)}
.faq-item.open{box-shadow:var(--shadow);border-color:color-mix(in srgb,var(--teal) 22%,transparent)}
.faq-q{width:100%;background:none;border:none;text-align:left;padding:22px 26px;font-size:1.05rem;font-weight:600;font-family:var(--font);color:var(--ink);cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;transition:color var(--t)}
.faq-q:hover{color:var(--teal)}
.faq-q::after{content:'+';width:26px;height:26px;flex-shrink:0;background:var(--teal-light);color:var(--teal);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.35rem;font-weight:400;line-height:1;transition:transform var(--t),background var(--t),color var(--t)}
.faq-item.open .faq-q::after{content:'\\2212';background:var(--teal);color:#fff;transform:rotate(180deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .4s ease,padding .4s ease;padding:0 26px}
.faq-item.open .faq-a{max-height:520px;padding:0 26px 24px}
.faq-a p{font-size:.99rem;line-height:1.72;color:var(--ink-soft)}

/* ── TRUST / STAT BAND ── */
.trust-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;text-align:center}
.trust-strip>div{position:relative;padding:8px 20px}
.trust-strip>div+div::before{content:"";position:absolute;left:0;top:18%;height:64%;width:1px;background:linear-gradient(180deg,transparent,rgba(214,165,96,.5),transparent)}
.trust-strip .ts-num{font-family:var(--font-d);font-size:2.7rem;font-weight:500;color:#fff;line-height:1;letter-spacing:-.01em}
.trust-strip .ts-label{font-size:.9rem;color:rgba(255,255,255,.72);margin-top:8px;letter-spacing:.01em}

/* ── CTA BAND ── */
.cta-band{background:linear-gradient(150deg,var(--ink) 0%,var(--teal-700) 70%,var(--teal-600) 100%);border-radius:30px;padding:68px 48px;text-align:center;color:#fff;position:relative;overflow:hidden;box-shadow:var(--shadow-xl)}
.cta-band::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(50% 90% at 88% 0%,rgba(35,192,166,.22),transparent 60%),radial-gradient(50% 90% at 10% 100%,rgba(190,132,74,.18),transparent 60%)}
.cta-band>*{position:relative;z-index:1}
.cta-band h2{color:#fff;margin-bottom:16px;font-size:clamp(1.9rem,3.6vw,2.7rem)}
.cta-band p{color:rgba(255,255,255,.86);font-size:1.14rem;max-width:580px;margin:0 auto 32px;line-height:1.6}

/* ── CONTENT / PROSE ── */
.prose{max-width:760px;margin:0 auto}
.prose h2{margin:46px 0 16px;font-size:1.8rem}
.prose h3{margin:32px 0 12px;font-size:1.34rem}
.prose p{font-size:1.07rem;line-height:1.8;margin-bottom:19px;color:#33485c}
.prose ul,.prose ol{margin:14px 0 24px 22px;color:#33485c;line-height:1.8}
.prose li{margin-bottom:9px}
.prose a{font-weight:500;text-decoration:underline;text-underline-offset:2px}
.prose>p:first-of-type::first-letter{font-family:var(--font-d);font-size:3.4em;font-weight:500;float:left;line-height:.82;margin:6px 12px 0 0;color:var(--teal)}
.lead{font-size:1.2rem;line-height:1.7;color:var(--ink-soft);margin-bottom:28px}

/* ── PAGE HERO (interior) ── */
.page-hero{padding:140px 0 68px;text-align:center;position:relative;overflow:hidden;
  background:
    radial-gradient(90% 80% at 88% -10%, rgba(35,192,166,.16) 0%, transparent 55%),
    radial-gradient(70% 70% at 8% 0%, rgba(190,132,74,.09) 0%, transparent 55%),
    linear-gradient(178deg,var(--teal-light) 0%,#fff 78%)}
.page-hero::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.45;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.35'/%3E%3C/svg%3E")}
.page-hero .container{position:relative;z-index:1}
.page-hero .eyebrow{margin-bottom:20px}
.page-hero p{font-size:1.16rem;max-width:620px;margin:18px auto 0;color:var(--ink-soft)}

/* ── FORM ── */
.lead-form{background:#fff;border:1px solid var(--line);border-radius:22px;padding:38px;box-shadow:var(--shadow-lg);max-width:620px;margin:0 auto}
.lead-form .fg{margin-bottom:19px}
.lead-form label{display:block;font-size:.84rem;font-weight:600;color:var(--ink);margin-bottom:8px;letter-spacing:.01em}
.lead-form input,.lead-form select,.lead-form textarea{width:100%;padding:14px 16px;border:1.5px solid var(--line-2);border-radius:var(--radius-sm);font-size:.97rem;font-family:inherit;color:var(--ink);background:#fff;transition:border var(--t),box-shadow var(--t)}
.lead-form input:focus,.lead-form select:focus,.lead-form textarea:focus{outline:none;border-color:var(--teal);box-shadow:0 0 0 4px color-mix(in srgb,var(--teal) 14%,transparent)}
.lead-form .row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.form-note{font-size:.84rem;color:var(--ink-soft);text-align:center;margin-top:16px}

/* ── NOTICE / EMERGENCY ── */
.notice{background:linear-gradient(180deg,#FFF8EE,#FFF4E6);border:1px solid #F0D2A0;border-radius:var(--radius-sm);padding:18px 22px;font-size:.95rem;color:#7A5418;display:flex;gap:13px;align-items:flex-start;max-width:880px;margin:0 auto;box-shadow:var(--shadow-sm)}
.notice b{color:#5A3D0E}
.notice .ic{flex-shrink:0;color:var(--copper-2)}

/* ── FOOTER ── */
.footer{background:linear-gradient(180deg,#0B1C2D 0%,var(--ink) 100%);color:rgba(255,255,255,.64);padding:76px 0 30px;position:relative}
.footer::before{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(190,132,74,.5),transparent)}
.footer-grid{display:grid;grid-template-columns:1.7fr 1fr 1fr 1fr;gap:48px;margin-bottom:48px}
.footer h4{color:#fff;font-size:.82rem;font-weight:700;margin-bottom:18px;font-family:var(--font);text-transform:uppercase;letter-spacing:.1em}
.footer a{display:block;color:rgba(255,255,255,.58);padding:6px 0;font-size:.93rem;transition:color var(--t),transform var(--t)}
.footer a:hover{color:var(--mint);transform:translateX(3px)}
.footer-brand .logo{font-family:var(--font-d);font-size:1.5rem;font-weight:550;color:#fff;margin-bottom:14px;display:flex;align-items:center;gap:10px}
.footer-brand .logo .dot{width:12px;height:12px;border-radius:50%;background:radial-gradient(circle at 32% 30%,var(--mint),var(--teal))}
.footer-brand p{font-size:.93rem;line-height:1.75;color:rgba(255,255,255,.58);max-width:330px}
.footer-bottom{border-top:1px solid rgba(255,255,255,.12);padding-top:26px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;font-size:.85rem}
.footer-legal{font-size:.82rem;color:rgba(255,255,255,.44);line-height:1.75;margin-top:20px;max-width:920px}

/* ── STICKY MOBILE CTA ── */
.mobilebar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:1100;background:color-mix(in srgb,#fff 92%,transparent);backdrop-filter:blur(12px);border-top:1px solid var(--line);padding:11px 14px;gap:10px;box-shadow:0 -6px 24px rgba(10,26,42,.12)}
.mobilebar .btn{flex:1;padding:14px 8px;font-size:.97rem}

/* ── SCROLL REVEAL ── */
.reveal{transition:opacity .7s cubic-bezier(.16,1,.3,1),transform .7s cubic-bezier(.16,1,.3,1)}
.js .reveal{opacity:0;transform:translateY(26px)}
.reveal.in{opacity:1;transform:none}
.reveal.d1{transition-delay:.08s}.reveal.d2{transition-delay:.16s}.reveal.d3{transition-delay:.24s}.reveal.d4{transition-delay:.32s}

/* ── RESPONSIVE ── */
@media(max-width:900px){
  .footer-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:820px){
  .nav-links{display:none}
  .nav-links.active{display:flex;flex-direction:column;align-items:stretch;position:fixed;top:74px;left:0;right:0;background:#fff;padding:16px 20px;gap:4px;box-shadow:var(--shadow-lg);border-bottom:1px solid var(--line)}
  .nav-links.active>li>a{padding:13px 14px}
  .nav-toggle{display:block}
  .hero-grid{grid-template-columns:1fr;gap:44px}
  .hero{padding:122px 0 60px}
  .section{padding:66px 0}
  .lead-form .row{grid-template-columns:1fr}
  .cta-band{padding:50px 28px}
  .mobilebar{display:flex}
  body{padding-bottom:74px}
  .footer-grid{grid-template-columns:1fr 1fr;gap:32px}
}
@media(max-width:520px){
  .footer-grid{grid-template-columns:1fr}
  .trust-strip>div+div::before{display:none}
}

/* ── ACCESSIBILITY / POLISH ── */
::selection{background:var(--mint);color:#04372f}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,
textarea:focus-visible,.faq-q:focus-visible,.quiz-opt:focus-visible{
  outline:3px solid var(--copper);outline-offset:2px;border-radius:6px}
.btn:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.001ms!important;animation-iteration-count:1!important;
    transition-duration:.001ms!important;scroll-behavior:auto!important}
  .reveal{opacity:1!important;transform:none!important}
  .card:hover,.cond-cat:hover,.price-card:hover{transform:none}
}
"""

PAGE_JS = """
<script>
document.documentElement.classList.add('js');
document.addEventListener('DOMContentLoaded',function(){
  // Mobile nav toggle
  var t=document.querySelector('.nav-toggle'),l=document.querySelector('.nav-links');
  if(t&&l){t.addEventListener('click',function(){l.classList.toggle('active');t.innerHTML=l.classList.contains('active')?'✕':'☰';});}

  // FAQ accordions
  document.querySelectorAll('.faq-q').forEach(function(b){
    b.addEventListener('click',function(){this.parentElement.classList.toggle('open');});
  });

  // Nav elevation on scroll
  var nav=document.querySelector('.nav');
  if(nav){
    var onScroll=function(){nav.classList.toggle('scrolled',window.scrollY>8);};
    onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  }

  // Auto-tag content blocks for scroll reveal, with a gentle stagger per group
  var groups=['.section-header','.steps','.cond-cats','.grid','.price-grid','.faq-list',
              '.hero-card','.trust-strip','.cta-band','.lead-form','.prose'];
  groups.forEach(function(sel){
    document.querySelectorAll(sel).forEach(function(parent){
      var kids=parent.children.length>1&&parent.matches('.steps,.cond-cats,.grid,.price-grid,.trust-strip')
               ? parent.children : [parent];
      Array.prototype.forEach.call(kids,function(el,i){
        el.classList.add('reveal');
        if(i>0&&i<5)el.classList.add('d'+i);
      });
    });
  });

  // Reveal on scroll (respects reduced motion)
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items=document.querySelectorAll('.reveal');
  if(reduce||!('IntersectionObserver' in window)){
    items.forEach(function(el){el.classList.add('in');});
  }else{
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});
    },{rootMargin:'0px 0px -8% 0px',threshold:.08});
    items.forEach(function(el){io.observe(el);});
  }
});
</script>
"""

# ---------------------------------------------------------------------------
# Inline SVG icons (stroke = currentColor)
# ---------------------------------------------------------------------------
def icon(name, size=24):
    paths = {
        "video": '<path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "pill": '<rect x="3" y="8" width="18" height="8" rx="4" transform="rotate(45 12 12)"/><path d="M8.5 8.5l7 7"/>',
        "flask": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/>',
        "heart": '<path d="M19 5a4.5 4.5 0 0 0-7 1 4.5 4.5 0 0 0-7-1c-2 2-1.5 5 1 7l6 6 6-6c2.5-2 3-5 1-7z"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/>',
        "dollar": '<circle cx="12" cy="12" r="9"/><path d="M12 7v10M9.5 9.5a2.5 2 0 0 1 5 0c0 2-5 1.5-5 4a2.5 2 0 0 0 5 0"/>',
        "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',
        "chat": '<path d="M21 12a8 8 0 0 1-11.5 7.2L4 21l1.8-5.5A8 8 0 1 1 21 12z"/>',
        "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
        "check": '<path d="M5 13l4 4L19 7"/>',
        "stethoscope": '<path d="M5 3v6a4 4 0 0 0 8 0V3"/><path d="M9 17a5 5 0 0 0 10 0v-2"/><circle cx="19" cy="11" r="2"/>',
        "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
        "leaf": '<path d="M4 20c8 0 16-4 16-16-8 0-16 4-16 16z"/><path d="M4 20c4-6 8-8 12-10"/>',
        "phone": '<path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
        "alert": '<path d="M12 3l9 16H3l9-16z"/><path d="M12 10v4M12 17h.01"/>',
        "map": '<path d="M9 3L3 5v16l6-2 6 2 6-2V3l-6 2-6-2z"/><path d="M9 3v16M15 5v16"/>',
        "spark": '<path d="M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2 2-6z"/>',
    }
    p = paths.get(name, paths["check"])
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{p}</svg>')


# ---------------------------------------------------------------------------
# Shared layout components
# ---------------------------------------------------------------------------
def render_head(title, desc, canonical_path, extra_head="", schema=None, og_image=None):
    canonical = BASE_URL + canonical_path
    og_img = BASE_URL + "/images/" + og_image if og_image else BUSINESS["og_image_url"]
    schema_tag = ""
    if schema:
        schema_tag = f'<script type="application/ld+json">{json.dumps(schema)}</script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{e(SITE_NAME)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="theme-color" content="#0A1A2A">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{FULL_CSS}</style>
{schema_tag}
{extra_head}
</head>
<body>
<a href="#content" class="skip">Skip to content</a>
"""


def render_nav():
    return f"""
<nav class="nav" role="navigation" aria-label="Main">
  <div class="nav-inner">
    <a href="/" class="nav-logo"><span class="dot"></span>Men's&nbsp;<b>Metabolic</b></a>
    <button class="nav-toggle" aria-label="Toggle menu">&#9776;</button>
    <ul class="nav-links">
      <li><a href="/how-it-works/">How It Works</a></li>
      <li><a href="/what-we-treat/">What We Treat</a></li>
      <li><a href="/mens-health/">Men's Health</a></li>
      <li><a href="/pricing/">Pricing</a></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/faq/">FAQ</a></li>
      <li><a href="{BOOKING_URL}" class="nav-cta">Book a Visit</a></li>
    </ul>
  </div>
</nav>
<span id="content" tabindex="-1"></span>
"""


def render_mobilebar():
    return f"""
<div class="mobilebar">
  <a href="{BOOKING_URL}" class="btn btn-primary">{icon('video',18)} Book a Visit</a>
  <a href="/pricing/" class="btn btn-ghost">See Pricing</a>
</div>
"""


def render_footer():
    yr = CURRENT_YEAR
    return f"""
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <span class="logo"><span class="dot"></span>Men's&nbsp;<b style="color:#fff">Metabolic</b></span>
        <p>Men's metabolic and hormone health, delivered by video. Board-certified physicians, evidence-based protocols, transparent flat pricing, and no insurance required, currently serving men in {e(states_phrase())}.</p>
      </div>
      <div>
        <h4>Care</h4>
        <a href="/how-it-works/">How It Works</a>
        <a href="/what-we-treat/">What We Treat</a>
        <a href="/mens-health/">Men's Health</a>
        <a href="/pricing/">Pricing &amp; Membership</a>
        <a href="{BOOKING_URL}">Book a Visit</a>
      </div>
      <div>
        <h4>Practice</h4>
        <a href="/about/">About Us</a>
        <a href="/faq/">FAQ</a>
        <a href="/contact/">Contact</a>
      </div>
      <div>
        <h4>Legal</h4>
        <a href="/privacy/">Privacy Policy</a>
        <a href="/terms/">Terms of Use</a>
        <a href="/telehealth-consent/">Telehealth Consent</a>
      </div>
    </div>
    <div class="footer-legal">
      <b style="color:rgba(255,255,255,.7)">Not for emergencies.</b> If you are experiencing a medical emergency, call 911 or go to the nearest emergency room. Men's Metabolic provides non-emergency telehealth visits for patients physically located in {e(states_phrase())}. Telehealth is not appropriate for every condition; our physicians will advise you if you need to be seen in person. We do not prescribe high-risk controlled substances such as opioids, stimulants, or benzodiazepines over telehealth. The information on this site is for general educational purposes and is not a substitute for professional medical advice, diagnosis, or treatment.
    </div>
    <div class="footer-bottom">
      <span>&copy; {yr} {e(BUSINESS['legal_name'])}. All rights reserved.</span>
      <span>Telehealth visits, {e(BUSINESS['hours'])}</span>
    </div>
  </div>
</footer>
{render_mobilebar()}
{PAGE_JS}
</body>
</html>"""


def render_emergency_notice():
    return f"""
<div class="container" style="padding-top:34px;padding-bottom:0;">
  <div class="notice">
    <span class="ic">{icon('alert',22)}</span>
    <span><b>This is not for emergencies.</b> If you have chest pain, trouble breathing, signs of a stroke, or any life-threatening symptom, call 911 or go to the nearest ER right away.</span>
  </div>
</div>
"""


def render_cta_band(heading=None, text=None):
    if not heading:
        heading = "Feel better without the waiting room."
    if not text:
        text = f"Book a video visit with a board-certified physician. Flat ${PRICE_VISIT}, no insurance, no surprise bills."
    return f"""
<section class="section">
  <div class="container">
    <div class="cta-band">
      <h2>{e(heading)}</h2>
      <p>{e(text)}</p>
      <div class="hero-cta-row" style="justify-content:center;">
        <a href="{BOOKING_URL}" class="btn btn-light btn-lg">{icon('video',20)} Book a Visit</a>
        <a href="/how-it-works/" class="btn btn-ghost btn-lg" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.4);">See How It Works</a>
      </div>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# Content data
# ---------------------------------------------------------------------------
CONDITION_CATEGORIES = [
    {
        "icon": "leaf",
        "title": "Weight &amp; metabolism",
        "blurb": "Medical weight loss that works with your biology, not against your willpower.",
        "tags": ["GLP-1 weight loss", "Semaglutide", "Tirzepatide", "Appetite &amp; cravings",
                 "Stubborn belly fat", "Prediabetes", "Metabolic health"],
    },
    {
        "icon": "spark",
        "title": "Testosterone &amp; hormones",
        "blurb": "Lab-based testosterone therapy for low energy, drive, and stalled progress.",
        "tags": ["Low testosterone", "Testosterone therapy (TRT)", "Low energy &amp; fatigue",
                 "Low libido", "Brain fog", "Hormone lab panels"],
    },
    {
        "icon": "heart",
        "title": "Sexual health",
        "blurb": "Discreet, effective treatment for ED, and a look at the causes behind it.",
        "tags": ["Erectile dysfunction (ED)", "Performance concerns", "Sildenafil",
                 "Tadalafil", "Libido", "Confidential care"],
    },
    {
        "icon": "shield",
        "title": "Heart &amp; metabolic health",
        "blurb": "Manage the numbers that drive long-term health and energy.",
        "tags": ["High blood pressure", "High cholesterol", "Blood sugar &amp; A1c",
                 "Insulin resistance", "Cardiometabolic risk", "Type 2 diabetes"],
    },
    {
        "icon": "clock",
        "title": "Energy, sleep &amp; stress",
        "blurb": "Get to the root of fatigue, poor sleep, and burnout, the metabolic way.",
        "tags": ["Chronic fatigue", "Poor sleep", "Stress &amp; burnout",
                 "Mood &amp; focus", "Recovery &amp; performance"],
    },
    {
        "icon": "flask",
        "title": "Labs &amp; biomarkers",
        "blurb": "Order the right bloodwork, then review exactly what it means for you.",
        "tags": ["Testosterone &amp; hormone panels", "Metabolic &amp; lipid panels",
                 "A1c &amp; blood sugar", "Thyroid testing", "Results interpretation"],
    },
]

HOW_IT_WORKS = [
    ("Book in minutes", "Pick a time that works for you, days, evenings, and weekends. Tell us briefly what is going on. No insurance card needed.", "calendar"),
    ("Meet your physician by video", "Connect from your phone or computer with a board-certified physician who actually listens, no rushed 7-minute visit.", "video"),
    ("Get your plan", "Your physician explains what is going on in plain language and sends any prescriptions, labs, or referrals you need.", "stethoscope"),
    ("Stay connected", "Message your care team with follow-up questions and keep your records in one secure place.", "chat"),
]

WHY_DIRECT_PAY = [
    ("One flat price", "You see the full cost before you book. No copays, no coding games, no surprise bill weeks later.", "dollar"),
    ("More time with your doctor", "Without insurance billing pressure, visits are unhurried and built around you, not a quota.", "clock"),
    ("Board-certified physicians", "You are seen by a licensed, board-certified physician, not a chatbot and not a rotating call center.", "shield"),
    ("Private and secure", "Your visits and records are protected with HIPAA-aligned, encrypted technology.", "lock"),
]

FAQS = [
    ("Do I need insurance?",
     f"No. Men's Metabolic is a direct-pay practice, which means you pay one flat price per visit (${PRICE_VISIT}) or a low monthly membership. You do not use insurance, and you will always know the price before you book. If you have insurance, you are welcome to submit a receipt to your plan or HSA/FSA, but we do not bill insurers directly."),
    ("Who will I be seeing?",
     "You will be seen by a board-certified physician licensed in your state. Our physicians focus on men's metabolic and hormone health, weight, testosterone, sexual health, and the cardiometabolic numbers behind them, for men 18 and older."),
    ("What can be treated over video?",
     "Most of men's metabolic and hormone health fits telehealth well, including medical weight loss, testosterone therapy, ED, blood pressure, cholesterol, blood sugar, and the labs behind them. If your physician determines you need hands-on care or in-person testing, they will tell you honestly and help you find the right next step."),
    ("Can you send prescriptions to my pharmacy?",
     "Yes, when clinically appropriate your physician can send prescriptions electronically to the pharmacy of your choice. For patient safety and in line with the law, we do not prescribe high-risk controlled substances such as opioids, stimulants, or benzodiazepines over telehealth. Some regulated medications used in men's health, such as testosterone, are only prescribed after appropriate bloodwork confirms they are right for you."),
    ("How fast can I be seen?",
     f"Most patients can book a same-day or next-day visit. Our physicians are available {BUSINESS['hours'].lower()}."),
    ("Which states do you serve?",
     f"We currently care for patients who are physically located in {states_phrase()} at the time of their visit. Telehealth law requires your physician to be licensed where you are located, so this is the area we can serve today. We are expanding, so check back if your state is not listed."),
    ("Do I still need my regular doctor?",
     "Men's Metabolic focuses on your metabolic and hormone health, and works alongside your primary care doctor rather than replacing them. Some situations, such as a physical exam, certain procedures, or emergencies, require in-person care, and we will always be upfront when you need to be seen in person and help coordinate it."),
    ("Is my information private?",
     "Yes. We use HIPAA-aligned, encrypted technology to protect your visits and records. We never sell your personal health information. See our Privacy Policy for full details."),
    ("What if I need a refund or have to cancel?",
     "If we determine that telehealth is not appropriate for your situation and cannot help you during your visit, we will work with you on a fair resolution. You can reschedule or cancel a booked visit ahead of time at no charge."),
    ("Can I use my HSA or FSA?",
     "In most cases, yes. Direct-pay medical visits are commonly eligible HSA/FSA expenses. We provide an itemized receipt you can submit. Check with your plan administrator for your specific rules."),
]


# Men's-health-specific FAQs (answer the top objections head on).
MENS_FAQS = [
    ("Is this legit, or just another online pill mill?",
     "It is real medicine. Every plan is reviewed and managed by a board-certified physician who looks at your history, your goals, and, where needed, your bloodwork before prescribing anything. We follow evidence-based protocols, not internet trends, and we will tell you honestly if a treatment is not right for you."),
    ("Are these treatments safe? What about side effects?",
     "Every medication has trade-offs, and we walk through them with you in plain language before you start. GLP-1 medications, testosterone therapy, and ED medications all have well-studied safety profiles when they are prescribed for the right person and monitored properly. That monitoring, regular check-ins and labs, is exactly how we keep you safe over time."),
    ("How much does it cost?",
     f"Pricing is transparent and direct-pay, so there are no surprise bills. Your initial consult is a flat ${PRICE_VISIT}, and ongoing care is available through a simple monthly membership. The cost of any medication or lab work is separate and billed by the pharmacy or lab, and we will always tell you what to expect before you commit."),
    ("Do I have time for this? I'm busy.",
     "That is the point of telehealth. Visits happen by video on your schedule, no commute and no waiting room. Most men complete their first consult in about 15 minutes, and follow-ups and dose adjustments can often be handled by secure message."),
    ("Will I be judged?",
     "Never. Weight, low energy, and sexual health are medical issues, not character flaws, and our physicians treat them that way. Your visits are private, secure, and HIPAA-aligned, and the conversation stays strictly between you and your care team."),
    ("Do I have to be in Tampa to use this?",
     f"No. We see patients by video anywhere in {states_phrase()}, so whether you are in Tampa, Orlando, Jacksonville, or a small town in between, you can be seen, as long as you are physically located in a state we serve at the time of your visit."),
    ("Can I get testosterone (TRT) online?",
     "When it is clinically appropriate, yes. Because testosterone is a regulated medication, we confirm low testosterone with bloodwork and review your full health picture before prescribing, then monitor you with follow-up labs. We will not prescribe it without the testing that makes it safe."),
    ("What is the difference between semaglutide and tirzepatide for weight loss?",
     "Both are GLP-1-based medications that help control appetite and blood sugar, and both can support meaningful, gradual weight loss alongside lifestyle changes. They differ in how they work and how your body responds, so your physician will help you choose based on your health history, goals, and how you tolerate treatment."),
]


# ---------------------------------------------------------------------------
# Page: Home
# ---------------------------------------------------------------------------
def build_home():
    schema = {
        "@context": "https://schema.org",
        "@type": "MedicalBusiness",
        "name": SITE_NAME,
        "description": "Men's metabolic and hormone health telehealth. Board-certified physicians by video for weight loss, testosterone, and ED. Transparent flat pricing, no insurance required.",
        "url": BASE_URL + "/",
        "telephone": PHONE_TEL,
        "priceRange": f"${PRICE_VISIT} per visit",
        "areaServed": [{"@type": "State", "name": s} for s in BUSINESS["states_licensed"]],
        "medicalSpecialty": "Endocrine",
    }

    cond_cards = ""
    for c in CONDITION_CATEGORIES[:6]:
        tags = "".join(f"<li>{t}</li>" for t in c["tags"][:5])
        cond_cards += f"""
<div class="cond-cat">
  <h3><span class="ic">{icon(c['icon'],22)}</span>{c['title']}</h3>
  <p>{c['blurb']}</p>
  <ul class="tags">{tags}</ul>
</div>"""

    steps = ""
    for i, (title, body, ic) in enumerate(HOW_IT_WORKS, 1):
        steps += f"""
<div class="step">
  <div class="num">{i}</div>
  <h3>{e(title)}</h3>
  <p>{e(body)}</p>
</div>"""

    why = ""
    for title, body, ic in WHY_DIRECT_PAY:
        why += f"""
<div class="card">
  <div class="ic">{icon(ic,24)}</div>
  <h3>{e(title)}</h3>
  <p>{e(body)}</p>
</div>"""

    faq_items = ""
    for q, a in FAQS[:6]:
        faq_items += f"""
<div class="faq-item">
  <button class="faq-q">{q}</button>
  <div class="faq-a"><p>{a}</p></div>
</div>"""

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": html_mod.unescape(q.replace("&amp;", "&")),
             "acceptedAnswer": {"@type": "Answer", "text": html_mod.unescape(a)}}
            for q, a in FAQS[:6]
        ],
    }

    html = render_head(
        f"{SITE_NAME} | GLP-1 Weight Loss, TRT & ED in Florida",
        f"See a board-certified physician by video for men's metabolic and hormone health, weight loss, testosterone, and ED. Flat ${PRICE_VISIT} visits, no insurance, serving men in {states_phrase()}.",
        "/",
        schema=schema,
        og_image="og-home.png",
    )
    html += render_nav()
    html += f"""
<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow"><span class="dot"></span>Board-certified physicians, by video</span>
        <h1>Men's metabolic health, <em>backed by real medicine.</em></h1>
        <p class="hero-sub">Men's Metabolic connects you with a board-certified physician over video for medical weight loss, testosterone, and ED, for one transparent price. Evidence-based protocols, lab-guided care, no insurance and no surprise bills.</p>
        <div class="hero-cta-row">
          <a href="{BOOKING_URL}" class="btn btn-primary btn-lg">{icon('video',20)} Book a Visit, ${PRICE_VISIT}</a>
          <a href="/how-it-works/" class="btn btn-ghost btn-lg">How It Works</a>
        </div>
        <div class="hero-trust">
          <span>{icon('check',18)} Same-day appointments</span>
          <span>{icon('check',18)} No insurance required</span>
          <span>{icon('check',18)} HSA/FSA eligible</span>
        </div>
      </div>
      <div class="hero-card">
        <span class="price-pop">Flat ${PRICE_VISIT} / visit</span>
        <h3>A video visit includes</h3>
        <p class="muted">Unhurried time with a physician who listens.</p>
        <ul class="checklist">
          <li><span class="ck">{icon('check',13)}</span>A real conversation with a board-certified physician</li>
          <li><span class="ck">{icon('check',13)}</span>Diagnosis and a clear plan in plain language</li>
          <li><span class="ck">{icon('check',13)}</span>Prescriptions sent to your pharmacy when appropriate</li>
          <li><span class="ck">{icon('check',13)}</span>Lab orders and results review</li>
          <li><span class="ck">{icon('check',13)}</span>Secure follow-up messaging with your care team</li>
        </ul>
        <a href="{BOOKING_URL}" class="btn btn-primary btn-block">Book a Visit</a>
      </div>
    </div>
  </div>
</section>

<section class="section-teal" style="padding:46px 0;">
  <div class="container">
    <div class="trust-strip">
      <div><div class="ts-num">${PRICE_VISIT}</div><div class="ts-label">Flat price per visit</div></div>
      <div><div class="ts-num">Same day</div><div class="ts-label">Appointments available</div></div>
      <div><div class="ts-num">100%</div><div class="ts-label">Board-certified physicians</div></div>
      <div><div class="ts-num">$0</div><div class="ts-label">Surprise bills, ever</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <span class="section-label">How It Works</span>
      <h2>Care in four simple steps</h2>
      <p>From booking to a clear plan, usually in a single day, all from wherever you are.</p>
    </div>
    <div class="steps">{steps}</div>
    <div class="center" style="margin-top:44px;">
      <a href="/how-it-works/" class="btn btn-ghost">See the full walkthrough</a>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="container">
    <div class="section-header">
      <span class="section-label">What We Treat</span>
      <h2>Men's metabolic health, end to end</h2>
      <p>From the weight that will not move to the hormones and numbers behind your energy, our physicians handle the full picture of men's metabolic and hormone health.</p>
    </div>
    <div class="cond-cats">{cond_cards}</div>
    <div class="center" style="margin-top:44px;">
      <a href="/what-we-treat/" class="btn btn-ghost">See everything we treat</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <span class="section-label">Why Direct Pay</span>
      <h2>Healthcare that works for you, not your insurer</h2>
      <p>Direct pay strips out the middlemen so you get more time, more clarity, and a price you can actually see.</p>
    </div>
    <div class="grid grid-4">{why}</div>
  </div>
</section>

<section class="section section-cloud">
  <div class="container">
    <div class="section-header">
      <span class="section-label">Simple Pricing</span>
      <h2>Know the price before you book</h2>
      <p>No copays, no deductibles, no decoding an explanation of benefits. Just two straightforward ways to get care.</p>
    </div>
    <div class="price-grid">
      <div class="price-card">
        <h3>Single Video Visit</h3>
        <div class="price">${PRICE_VISIT}<small> / visit</small></div>
        <p class="blurb">Perfect when something comes up and you just need to be seen.</p>
        <ul>
          <li><span class="ck">{icon('check',16)}</span>One complete video visit</li>
          <li><span class="ck">{icon('check',16)}</span>Diagnosis &amp; treatment plan</li>
          <li><span class="ck">{icon('check',16)}</span>Prescriptions when appropriate</li>
          <li><span class="ck">{icon('check',16)}</span>Lab orders &amp; results review</li>
        </ul>
        <a href="{BOOKING_URL}" class="btn btn-ghost btn-block">Book a Visit</a>
      </div>
      <div class="price-card featured">
        <span class="ribbon">Best value</span>
        <h3>Membership</h3>
        <div class="price">${PRICE_MEMBER}<small> / month</small></div>
        <p class="blurb">Ongoing care, monitoring, and messaging for one low monthly price.</p>
        <ul>
          <li><span class="ck">{icon('check',16)}</span>Included video visits</li>
          <li><span class="ck">{icon('check',16)}</span>Unlimited secure messaging</li>
          <li><span class="ck">{icon('check',16)}</span>Chronic condition management</li>
          <li><span class="ck">{icon('check',16)}</span>Priority same-day scheduling</li>
        </ul>
        <a href="/pricing/" class="btn btn-primary btn-block">See Membership</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <span class="section-label">Questions</span>
      <h2>You probably want to know</h2>
    </div>
    <div class="faq-list">{faq_items}</div>
    <div class="center" style="margin-top:36px;">
      <a href="/faq/" class="btn btn-ghost">Read all FAQs</a>
    </div>
  </div>
  <script type="application/ld+json">{json.dumps(faq_schema)}</script>
</section>
"""
    html += render_cta_band()
    html += render_footer()
    write_page(["index.html"], html)


# ---------------------------------------------------------------------------
# Page: How It Works
# ---------------------------------------------------------------------------
def build_how_it_works():
    steps = ""
    detail = [
        "Choose a visit time from your phone or computer in about a minute. There is no insurance card to dig up and no forms to print. You will tell us a little about what is going on so your physician can prepare.",
        "At your appointment, you connect by secure video with a board-certified physician. This is a real, unhurried conversation, the physician listens, asks questions, and works through what is actually going on with you.",
        "Your physician explains the diagnosis and your options in plain language. When appropriate, they send prescriptions to your pharmacy, order labs at a draw site near you, and provide any notes or referrals you need.",
        "After your visit, you can message your care team with follow-up questions, get your results reviewed, and keep all of your records in one secure place. Care does not stop when the video call ends.",
    ]
    for i, ((title, _b, ic), d) in enumerate(zip(HOW_IT_WORKS, detail), 1):
        steps += f"""
<div class="step">
  <div class="num">{i}</div>
  <h3>{e(title)}</h3>
  <p>{e(d)}</p>
</div>"""

    html = render_head(
        f"How It Works | {SITE_NAME} Telehealth",
        f"See how Men's Metabolic works: book in minutes, meet a board-certified physician by video, and get a clear plan. Flat ${PRICE_VISIT} visits, no insurance.",
        "/how-it-works/",
    )
    html += render_nav()
    html += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow"><span class="dot"></span>How It Works</span>
    <h1>Better care, far less hassle</h1>
    <p>No referrals, no waiting rooms, no guessing what it will cost. Here is exactly what happens from the moment you book.</p>
  </div>
</section>
{render_emergency_notice()}
<section class="section">
  <div class="container">
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="section section-sand">
  <div class="container">
    <div class="prose">
      <h2>What you need to get started</h2>
      <ul>
        <li>A smartphone, tablet, or computer with a camera</li>
        <li>A private spot with a steady internet connection</li>
        <li>To be physically located in {states_phrase()} at the time of your visit</li>
        <li>A list of any current medications and allergies</li>
      </ul>
      <h2>What a visit can cover</h2>
      <p>Our physicians handle medical weight loss, testosterone and hormone therapy, ED, and the cardiometabolic numbers behind them, blood pressure, cholesterol, and blood sugar, plus the labs that guide it all. If something needs hands-on care, they will tell you directly and help you find the right place to be seen.</p>
      <h2>What we cannot do over video</h2>
      <p>Telehealth is powerful, but it is not right for everything. We do not treat medical emergencies, and we do not prescribe high-risk controlled substances such as opioids, stimulants, or benzodiazepines. If you ever have a life-threatening symptom, call 911 or go to the nearest emergency room.</p>
    </div>
  </div>
</section>
"""
    html += render_cta_band()
    html += render_footer()
    write_page(["how-it-works", "index.html"], html)


# ---------------------------------------------------------------------------
# Page: What We Treat
# ---------------------------------------------------------------------------
def build_what_we_treat():
    cards = ""
    for c in CONDITION_CATEGORIES:
        tags = "".join(f"<li>{t}</li>" for t in c["tags"])
        cards += f"""
<div class="cond-cat">
  <h3><span class="ic">{icon(c['icon'],22)}</span>{c['title']}</h3>
  <p>{c['blurb']}</p>
  <ul class="tags">{tags}</ul>
</div>"""

    html = render_head(
        f"What We Treat | {SITE_NAME} Telehealth",
        "From medical weight loss and testosterone to ED, blood pressure, cholesterol, and the labs behind them, see the full range of men's metabolic and hormone health Men's Metabolic physicians handle by video.",
        "/what-we-treat/",
    )
    html += render_nav()
    html += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow"><span class="dot"></span>What We Treat</span>
    <h1>The full range of men's metabolic health</h1>
    <p>Our board-certified physicians focus on the metabolic and hormonal drivers behind how men feel, from weight and energy to testosterone and sexual health.</p>
  </div>
</section>
{render_emergency_notice()}
<section class="section">
  <div class="container">
    <div class="cond-cats">{cards}</div>
  </div>
</section>

<section class="section section-sand">
  <div class="container">
    <div class="prose">
      <h2>Not sure if we can help?</h2>
      <p>This list covers what we treat most often, but it is not exhaustive. If you are dealing with something that is not listed, book a visit and ask, or send us a message. Our physicians will tell you honestly whether telehealth is the right fit, and if you need to be seen in person, they will point you in the right direction.</p>
      <p><b>A note on scope:</b> Men's Metabolic cares for men 18 and older. We do not manage medical emergencies, and we do not prescribe high-risk controlled substances such as opioids, stimulants, or benzodiazepines over telehealth.</p>
    </div>
  </div>
</section>
"""
    html += render_cta_band()
    html += render_footer()
    write_page(["what-we-treat", "index.html"], html)


# ---------------------------------------------------------------------------
# Page: Pricing
# ---------------------------------------------------------------------------
def build_pricing():
    html = render_head(
        f"Pricing & Membership | {SITE_NAME}",
        f"Simple, transparent direct-pay pricing. Single video visits for ${PRICE_VISIT} or a ${PRICE_MEMBER}/month membership. No insurance, no copays, no surprise bills.",
        "/pricing/",
        og_image="og-pricing.png",
    )
    html += render_nav()
    html += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow"><span class="dot"></span>Pricing</span>
    <h1>One price. No surprises.</h1>
    <p>Because we do not bill insurance, there are no copays, deductibles, or mystery charges. You see the full cost before you ever book.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="price-grid">
      <div class="price-card">
        <h3>Single Video Visit</h3>
        <div class="price">${PRICE_VISIT}<small> / visit</small></div>
        <p class="blurb">For when something comes up and you just need to be seen by a physician today.</p>
        <ul>
          <li><span class="ck">{icon('check',16)}</span>One complete video visit</li>
          <li><span class="ck">{icon('check',16)}</span>Diagnosis &amp; clear treatment plan</li>
          <li><span class="ck">{icon('check',16)}</span>Prescriptions sent to your pharmacy when appropriate</li>
          <li><span class="ck">{icon('check',16)}</span>Lab orders and results review</li>
          <li><span class="ck">{icon('check',16)}</span>Itemized receipt for HSA/FSA</li>
        </ul>
        <a href="{BOOKING_URL}" class="btn btn-ghost btn-block">Book a Single Visit</a>
      </div>
      <div class="price-card featured">
        <span class="ribbon">Best value</span>
        <h3>Membership</h3>
        <div class="price">${PRICE_MEMBER}<small> / month</small></div>
        <p class="blurb">Ongoing care for men who want a physician monitoring their progress month to month.</p>
        <ul>
          <li><span class="ck">{icon('check',16)}</span>Included video visits</li>
          <li><span class="ck">{icon('check',16)}</span>Unlimited secure messaging with your care team</li>
          <li><span class="ck">{icon('check',16)}</span>Ongoing chronic condition management</li>
          <li><span class="ck">{icon('check',16)}</span>Priority same-day scheduling</li>
          <li><span class="ck">{icon('check',16)}</span>Annual wellness review</li>
          <li><span class="ck">{icon('check',16)}</span>Cancel anytime</li>
        </ul>
        <a href="{BOOKING_URL}" class="btn btn-primary btn-block">Start Membership</a>
      </div>
    </div>

    <p class="center" style="margin-top:30px;color:var(--ink-soft);font-size:.95rem;max-width:620px;margin-left:auto;margin-right:auto;">
      Lab tests, imaging, and medications obtained through outside pharmacies or labs are billed by those providers and are not included in the visit or membership price. We will always tell you about likely out-of-pocket costs before ordering.
    </p>
  </div>
</section>

<section class="section section-sand">
  <div class="container">
    <div class="prose">
      <h2>What is, and isn't, included</h2>
      <p><b>Included:</b> Your physician's time, diagnosis, a treatment plan, e-prescriptions when appropriate, lab orders, results review, referrals, and secure follow-up messaging (messaging is unlimited on membership).</p>
      <p><b>Not included:</b> The cost of any prescription medications, the cost of lab draws or imaging performed by an outside facility, and any in-person care you may be referred to. These are billed directly by those providers, often at cash-friendly rates.</p>
      <h2>Can I use my HSA or FSA?</h2>
      <p>In most cases, yes. Direct-pay medical visits are commonly eligible expenses under Health Savings and Flexible Spending Accounts. We provide an itemized receipt you can submit. Check your plan's rules with your administrator.</p>
      <h2>Do you bill insurance?</h2>
      <p>No. We are an intentionally insurance-free practice, which is what lets us keep pricing transparent and visits unhurried. If you would like, you can submit our itemized receipt to your insurer for possible out-of-network reimbursement, though we cannot guarantee what your plan will do.</p>
    </div>
  </div>
</section>
"""
    html += render_cta_band("Ready when you are.",
                            f"Book a single visit for ${PRICE_VISIT}, or start a membership and keep a physician in your corner year-round.")
    html += render_footer()
    write_page(["pricing", "index.html"], html)


# ---------------------------------------------------------------------------
# Page: About
# ---------------------------------------------------------------------------
def build_about():
    values = ""
    vlist = [
        ("Time, not transactions", "We built Men's Metabolic around unhurried visits because good medicine starts with listening.", "clock"),
        ("Honesty first", "We tell you when telehealth is the right call, and just as importantly, when it is not.", "shield"),
        ("Transparent by design", "You will never get a bill you did not see coming. The price is the price.", "dollar"),
        ("Whole-person care", "We treat the metabolic system, not a single symptom in isolation, because it is all connected.", "heart"),
    ]
    for title, body, ic in vlist:
        values += f"""
<div class="card">
  <div class="ic">{icon(ic,24)}</div>
  <h3>{e(title)}</h3>
  <p>{e(body)}</p>
</div>"""

    html = render_head(
        f"About {SITE_NAME} | Men's Health Telehealth",
        "Men's Metabolic is a direct-pay men's metabolic and hormone health telehealth practice built on evidence-based protocols, transparent pricing, and board-certified physicians who actually listen.",
        "/about/",
    )
    html += render_nav()
    html += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow"><span class="dot"></span>About Us</span>
    <h1>Men's health, rebuilt around the patient</h1>
    <p>We started Men's Metabolic because men deserve a physician who has time to listen, and a price they can actually understand.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="prose">
      <p class="lead">Modern healthcare too often means a long wait for a short visit, followed by a bill no one can explain. Men's Metabolic is our answer to that.</p>
      <p>We are a direct-pay men's metabolic and hormone health telehealth practice. That means you see a board-certified physician by video, pay one transparent price, and skip the insurance maze entirely. No copays, no prior authorizations, no surprise statements weeks later.</p>
      <p>Our physicians focus on the metabolic and hormonal drivers of how men feel and perform, weight and metabolism, testosterone, sexual health, and cardiometabolic risk. They diagnose with real labs and manage your plan over time, not with a one-off prescription. By delivering that expertise over secure video, we make it easy to get real care from wherever you are.</p>
      <h2>Why direct pay</h2>
      <p>When a visit is not filtered through insurance billing, two things change for the better. Your physician has time to actually listen instead of racing the clock, and you know the cost up front instead of dreading the mail. That is the entire idea behind Men's Metabolic.</p>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="container">
    <div class="section-header">
      <span class="section-label">What We Stand For</span>
      <h2>Our values</h2>
    </div>
    <div class="grid grid-4">{values}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="prose">
      <h2>Our physicians</h2>
      <p>Every visit is with a board-certified physician licensed in your state. We are a small, focused practice by design, you get a real physician, not a chatbot and not an anonymous call center.</p>
      <p style="background:var(--cloud);border:1px solid var(--line);border-radius:12px;padding:18px 20px;font-size:.95rem;color:var(--ink-soft);"><b style="color:var(--ink)">Note for launch:</b> Add your physician name(s), photo, credentials, medical school, residency, board certification, and state license numbers here before going live. Patients trust real, verifiable credentials, and several states require provider licensing details to be displayed.</p>
    </div>
  </div>
</section>
"""
    html += render_cta_band()
    html += render_footer()
    write_page(["about", "index.html"], html)


# ---------------------------------------------------------------------------
# Page: FAQ
# ---------------------------------------------------------------------------
def build_faq():
    faq_items = ""
    for q, a in FAQS:
        faq_items += f"""
<div class="faq-item">
  <button class="faq-q">{q}</button>
  <div class="faq-a"><p>{a}</p></div>
</div>"""

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": html_mod.unescape(q.replace("&amp;", "&")),
             "acceptedAnswer": {"@type": "Answer", "text": html_mod.unescape(a)}}
            for q, a in FAQS
        ],
    }

    html = render_head(
        f"FAQ | {SITE_NAME} Telehealth",
        "Answers to common questions about Men's Metabolic: pricing, what we treat, prescriptions, states served, privacy, HSA/FSA, and more.",
        "/faq/",
        schema=faq_schema,
    )
    html += render_nav()
    html += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow"><span class="dot"></span>FAQ</span>
    <h1>Questions, answered</h1>
    <p>Everything you might want to know before your first visit. Still curious? Reach out anytime.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="faq-list">{faq_items}</div>
  </div>
</section>
"""
    html += render_cta_band()
    html += render_footer()
    write_page(["faq", "index.html"], html)


# ---------------------------------------------------------------------------
# Page: Contact / Book
# ---------------------------------------------------------------------------
def build_contact():
    html = render_head(
        f"Book a Visit & Contact | {SITE_NAME}",
        f"Book a direct-pay video visit with a board-certified physician, or send us a question. Flat ${PRICE_VISIT} visits, serving {states_phrase()}.",
        "/contact/",
    )
    html += render_nav()
    html += f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow"><span class="dot"></span>Book a Visit</span>
    <h1>Let's get you feeling better</h1>
    <p>Tell us a little about what is going on and how to reach you. A member of our care team will follow up to confirm your video visit.</p>
  </div>
</section>
{render_emergency_notice()}
<section class="section">
  <div class="container">
    <form class="lead-form" name="visit-request" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thank-you/">
      <input type="hidden" name="form-name" value="visit-request">
      <p style="display:none;"><label>Don't fill this out: <input name="bot-field"></label></p>
      <div class="row">
        <div class="fg">
          <label for="name">Full name *</label>
          <input id="name" type="text" name="name" required placeholder="Your name">
        </div>
        <div class="fg">
          <label for="phone">Phone *</label>
          <input id="phone" type="tel" name="phone" required placeholder="(000) 000-0000">
        </div>
      </div>
      <div class="row">
        <div class="fg">
          <label for="email">Email *</label>
          <input id="email" type="email" name="email" required placeholder="you@email.com">
        </div>
        <div class="fg">
          <label for="state">Your state *</label>
          <select id="state" name="state" required>
            <option value="">Select your state...</option>
            {''.join(f'<option value="{e(s)}">{e(s)}</option>' for s in BUSINESS['states_licensed'])}
            <option value="other">Other / not listed</option>
          </select>
        </div>
      </div>
      <div class="row">
        <div class="fg">
          <label for="reason">What do you need help with? *</label>
          <select id="reason" name="reason" required>
            <option value="">Select one...</option>
            <option>Everyday or urgent illness</option>
            <option>Chronic condition management</option>
            <option>Prescription refill</option>
            <option>Lab order or results review</option>
            <option>Mental / behavioral health</option>
            <option>Annual wellness / preventive</option>
            <option>Membership question</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="fg">
          <label for="pref">Preferred time</label>
          <select id="pref" name="preferred_time">
            <option value="">No preference</option>
            <option>Morning</option>
            <option>Afternoon</option>
            <option>Evening</option>
            <option>Weekend</option>
          </select>
        </div>
      </div>
      <div class="fg">
        <label for="msg">Anything else we should know?</label>
        <textarea id="msg" name="message" rows="4" placeholder="Briefly describe your symptoms or question. Do not include sensitive details you would rather discuss live."></textarea>
      </div>
      <button type="submit" class="btn btn-primary btn-block btn-lg">Request My Visit</button>
      <p class="form-note">By submitting, you agree to our <a href="/terms/">Terms</a>, <a href="/privacy/">Privacy Policy</a>, and <a href="/telehealth-consent/">Telehealth Consent</a>. This form is not for emergencies.</p>
    </form>

    <div class="center" style="margin-top:40px;color:var(--ink-soft);">
      <p style="margin-bottom:6px;">Prefer email? Reach us at <a href="mailto:{BUSINESS['email']}">{e(BUSINESS['email'])}</a></p>
      <p>Phone: <a href="tel:{PHONE_TEL}">{e(PHONE_DISPLAY)}</a> &nbsp;&middot;&nbsp; {e(BUSINESS['hours'])}</p>
    </div>
  </div>
</section>
"""
    html += render_footer()
    write_page(["contact", "index.html"], html)


# ---------------------------------------------------------------------------
# Page: Thank You
# ---------------------------------------------------------------------------
def build_thank_you():
    html = render_head(
        f"Thank You | {SITE_NAME}",
        "Thanks for reaching out to Men's Metabolic. Our care team will follow up shortly to confirm your video visit.",
        "/thank-you/",
        extra_head='<meta name="robots" content="noindex,follow">',
    )
    html += render_nav()
    html += f"""
<section class="page-hero" style="padding-bottom:90px;">
  <div class="container">
    <div style="width:72px;height:72px;border-radius:50%;background:var(--mint);color:#fff;display:flex;align-items:center;justify-content:center;margin:0 auto 24px;">{icon('check',38)}</div>
    <span class="eyebrow"><span class="dot"></span>Request received</span>
    <h1>Thank you, we're on it.</h1>
    <p>A member of our care team will reach out shortly to confirm your visit and next steps. If this is urgent and you are experiencing an emergency, please call 911.</p>
    <div class="hero-cta-row" style="justify-content:center;margin-top:28px;">
      <a href="/" class="btn btn-primary">Back to Home</a>
      <a href="/what-we-treat/" class="btn btn-ghost">What We Treat</a>
    </div>
  </div>
</section>
"""
    html += render_footer()
    write_page(["thank-you", "index.html"], html)


# ---------------------------------------------------------------------------
# Legal pages
# ---------------------------------------------------------------------------
def build_legal_page(slug_path, title, intro, sections):
    body = f'<p class="lead">{intro}</p>'
    for h, paras in sections:
        body += f"<h2>{h}</h2>"
        for p in paras:
            body += f"<p>{p}</p>"
    html = render_head(
        f"{title} | {SITE_NAME}",
        f"{title} for {SITE_NAME}, direct-pay men's metabolic health telehealth.",
        f"/{slug_path}/",
        extra_head='<meta name="robots" content="noindex,follow">',
    )
    html += render_nav()
    html += f"""
<section class="page-hero" style="padding-bottom:40px;">
  <div class="container">
    <h1>{e(title)}</h1>
    <p>Last updated {CURRENT_DATE}</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="prose">{body}
    <p style="margin-top:32px;background:var(--cloud);border:1px solid var(--line);border-radius:12px;padding:18px 20px;font-size:.92rem;color:var(--ink-soft);"><b style="color:var(--ink)">Template notice:</b> This document is a starting template, not legal advice. Have it reviewed and customized by a healthcare attorney before publishing.</p>
    </div>
  </div>
</section>
"""
    html += render_footer()
    write_page([slug_path, "index.html"], html)


def build_legal():
    build_legal_page(
        "privacy", "Privacy Policy",
        "Men's Metabolic is committed to protecting your privacy and the security of your health information. This policy explains what we collect, how we use it, and your rights.",
        [
            ("Information we collect", [
                "We collect the information you provide when you book or attend a visit, including your name, contact details, the state you are located in, and the health information you share with your physician.",
                "We also collect limited technical information automatically, such as your device type and how you use our website, to keep the service secure and working well.",
            ]),
            ("How we use your information", [
                "We use your information to provide medical care, communicate with you, process payments, maintain your medical record, and comply with our legal and professional obligations.",
                "We do not sell your personal health information, and we do not use it for advertising.",
            ]),
            ("How we protect it", [
                "We use encryption and HIPAA-aligned safeguards to protect your health information in transit and at rest, and we limit access to those who need it to provide your care.",
            ]),
            ("Your rights", [
                "You have the right to access your medical records, request corrections, and ask how your information has been shared. Contact us at " + BUSINESS["email"] + " to make a request.",
            ]),
            ("Contact", [
                f"Questions about this policy can be directed to {BUSINESS['email']}.",
            ]),
        ],
    )
    build_legal_page(
        "terms", "Terms of Use",
        "These terms govern your use of the Men's Metabolic website and services. By using our services, you agree to them.",
        [
            ("Who we serve", [
                f"Men's Metabolic provides non-emergency telehealth visits to men 18 and older who are physically located in {states_phrase()} at the time of their visit.",
            ]),
            ("Not for emergencies", [
                "Our services are not for medical emergencies. If you are experiencing an emergency, call 911 or go to the nearest emergency room immediately.",
            ]),
            ("Scope of care", [
                "Telehealth is not appropriate for every condition. Your physician will advise you if you need to be seen in person. We do not prescribe high-risk controlled substances such as opioids, stimulants, or benzodiazepines.",
            ]),
            ("Payment", [
                f"Men's Metabolic is a direct-pay practice. Visits are billed at a flat rate of ${PRICE_VISIT}, or under a monthly membership. We do not bill insurance. Fees for medications, labs, and outside services are billed separately by those providers.",
            ]),
            ("No guarantee of outcome", [
                "Medical care involves professional judgment and cannot guarantee specific results. We provide care consistent with accepted medical standards.",
            ]),
        ],
    )
    build_legal_page(
        "telehealth-consent", "Telehealth Informed Consent",
        "Before your visit, please review this consent describing how telehealth works, its benefits, and its limits.",
        [
            ("What telehealth is", [
                "Telehealth uses secure video and messaging to let you receive care from a licensed physician without an in-person visit. You will discuss your symptoms and history, and your physician will provide diagnosis and treatment recommendations remotely.",
            ]),
            ("Benefits", [
                "Telehealth can improve access and convenience, letting you be seen from home, often the same day, without travel or a waiting room.",
            ]),
            ("Limits and risks", [
                "Because the physician cannot physically examine you, some conditions cannot be fully evaluated by video and may require in-person care or testing. As with any technology, there is a small risk of technical issues or information security limitations despite our safeguards.",
                "We do not treat emergencies and do not prescribe high-risk controlled substances such as opioids, stimulants, or benzodiazepines by telehealth.",
            ]),
            ("Your consent", [
                "By proceeding with a visit, you consent to receive care via telehealth, confirm you are physically located in a state we serve, and understand you may stop or decline telehealth at any time and seek in-person care instead.",
            ]),
        ],
    )


# ---------------------------------------------------------------------------
# Page: Men's Health hub (GLP-1 weight loss, TRT, ED)
# ---------------------------------------------------------------------------
def build_mens_health():
    # Three core programs rendered as on-page offer sections.
    programs = [
        {
            "id": "weight-loss",
            "url": "/mens-health/weight-loss/",
            "icon": "leaf",
            "kicker": "GLP-1 Weight Loss",
            "h2": "Medical weight loss with GLP-1 medication",
            "lead": "If the scale has not budged no matter how hard you try, it may not be willpower, it may be biology. GLP-1 medications like semaglutide and tirzepatide work with your body to quiet appetite and steady blood sugar, so the changes you make finally stick.",
            "points": [
                "Physician-reviewed eligibility, no one-size-fits-all dosing",
                "Semaglutide or tirzepatide matched to your health and goals",
                "Steady, sustainable loss, not a crash diet",
                "Nutrition and habit coaching built into your plan",
                "Regular check-ins to manage side effects and adjust your dose",
            ],
        },
        {
            "id": "trt",
            "url": "/mens-health/testosterone-trt/",
            "icon": "spark",
            "kicker": "Testosterone (TRT)",
            "h2": "Testosterone therapy, done the responsible way",
            "lead": "Low energy, brain fog, stubborn weight, low drive. These can be signs of low testosterone, and they are treatable. We confirm it with bloodwork first, then build a plan that is monitored, not guessed at.",
            "points": [
                "Diagnosis confirmed with real lab testing, not a questionnaire alone",
                "Board-certified physician oversight at every step",
                "Treatment matched to your levels, symptoms, and goals",
                "Follow-up labs to keep your therapy safe and effective",
                "Honest guidance, including when TRT is not the right answer",
            ],
        },
        {
            "id": "ed",
            "url": "/mens-health/ed/",
            "icon": "heart",
            "kicker": "ED Treatment",
            "h2": "Discreet, effective ED care",
            "lead": "Erectile dysfunction is common, and it is very treatable. It can also be an early signal about your heart and overall health, which is why we treat the whole picture, not just the symptom.",
            "points": [
                "Private video visit, no awkward waiting room",
                "Proven options like sildenafil and tadalafil when appropriate",
                "A look at underlying causes, blood pressure, stress, sleep, hormones",
                "Sent discreetly to the pharmacy of your choice",
                "Ongoing access to adjust if your first plan is not the right fit",
            ],
        },
    ]

    prog_html = ""
    for i, p in enumerate(programs):
        alt = " section-sand" if i % 2 == 1 else ""
        pts = "".join(
            f'<li><span class="ck">{icon("check",16)}</span>{e(x)}</li>' for x in p["points"]
        )
        prog_html += f"""
<section class="section{alt}" id="{p['id']}">
  <div class="container">
    <div class="hero-grid" style="align-items:center;">
      <div>
        <span class="section-label">{p['kicker']}</span>
        <h2>{e(p['h2'])}</h2>
        <p class="lead" style="margin-top:14px;">{e(p['lead'])}</p>
        <div class="hero-cta-row">
          <a href="{BOOKING_URL}" class="btn btn-primary">{icon('video',18)} Book a consult</a>
          <a href="{p['url']}" class="btn btn-ghost">Learn more {icon('check',16)}</a>
        </div>
      </div>
      <div class="hero-card" style="box-shadow:var(--shadow);">
        <h3>What your plan includes</h3>
        <p class="muted">Evidence-based care, monitored over time.</p>
        <ul class="price-card" style="border:none;padding:0;margin:0;list-style:none;display:flex;flex-direction:column;gap:11px;">{pts}</ul>
      </div>
    </div>
  </div>
</section>"""

    # How it works (reuse the 4-step model with a men's-health framing).
    mh_steps = [
        ("Start your eligibility check", "Answer a few quick questions about your health and goals. It takes about a minute and tells us if telehealth is a fit for you.", "calendar"),
        ("Meet your physician by video", "Talk with a board-certified physician who actually listens. Together you will decide if treatment makes sense, and order labs if you need them.", "video"),
        ("Begin your plan", "If it is the right call, your physician sends your medication to your pharmacy and walks you through exactly what to expect.", "pill"),
        ("Check in and stay on track", "Regular follow-ups and lab monitoring keep your plan safe and working, with messaging access whenever questions come up.", "chat"),
    ]
    steps_html = ""
    for i, (t, b, ic) in enumerate(mh_steps, 1):
        steps_html += f"""
<div class="step"><div class="num">{i}</div><h3>{e(t)}</h3><p>{e(b)}</p></div>"""

    # Five objections handled directly.
    objections = [
        ("\"Is this even safe?\"", "Every treatment we offer has a well-studied safety profile when it is prescribed for the right person and monitored properly. That is the whole job of your physician, and the reason we insist on labs and follow-ups."),
        ("\"What about side effects?\"", "We tell you the real trade-offs up front, in plain language, and we adjust your plan if something is not sitting right. You are never on your own between visits."),
        ("\"What will it cost me?\"", f"Transparent, direct-pay pricing. A flat ${PRICE_VISIT} consult and a simple monthly membership for ongoing care. You will always know the price before you commit."),
        ("\"Who has the time?\"", "Most first visits take about 15 minutes by video, and many follow-ups happen by message. No commute, no waiting room, no time off work."),
        ("\"Will I be judged?\"", "Not here. These are medical issues, not personal failings, and your care is private, secure, and HIPAA-aligned from start to finish."),
    ]
    obj_html = ""
    for q, a in objections:
        obj_html += f"""
<div class="card"><h3 style="font-size:1.12rem;">{e(q)}</h3><p>{e(a)}</p></div>"""

    # Men's health FAQ + schema.
    faq_items = ""
    for q, a in MENS_FAQS:
        faq_items += f"""
<div class="faq-item"><button class="faq-q">{e(q)}</button><div class="faq-a"><p>{e(a)}</p></div></div>"""
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in MENS_FAQS
        ],
    }
    page_schema = {
        "@context": "https://schema.org",
        "@type": "MedicalWebPage",
        "name": "Men's Health Telehealth in Tampa, Florida",
        "url": BASE_URL + "/mens-health/",
        "about": [
            {"@type": "MedicalCondition", "name": "Overweight and obesity"},
            {"@type": "MedicalCondition", "name": "Low testosterone"},
            {"@type": "MedicalCondition", "name": "Erectile dysfunction"},
        ],
        "audience": {"@type": "PeopleAudience", "suggestedGender": "Male",
                     "suggestedMinAge": 18},
    }

    html = render_head(
        "Men's Health Telehealth in Tampa, FL | GLP-1, TRT, ED",
        f"Online men's health care in Tampa and across Florida. Board-certified physicians for GLP-1 weight loss, testosterone (TRT), and ED. Flat ${PRICE_VISIT} consult. Book today.",
        "/mens-health/",
        schema=page_schema,
        og_image="og-mens-health.png",
    )
    html += render_nav()
    html += f"""
<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow"><span class="dot"></span>Men's Health, Tampa &amp; statewide Florida</span>
        <h1>Men's health telehealth in Tampa, <em>backed by real medicine.</em></h1>
        <p class="hero-sub">Weight that will not move, low energy, or performance you would rather not discuss in a waiting room. Get evidence-based care for GLP-1 weight loss, testosterone, and ED from a board-certified physician, by video, anywhere in Florida.</p>
        <div class="hero-cta-row">
          <a href="{BOOKING_URL}" class="btn btn-primary btn-lg">{icon('video',20)} Book a 15-minute consult</a>
          <a href="/eligibility/" class="btn btn-ghost btn-lg">{icon('check',18)} Take the 60-second eligibility check</a>
        </div>
        <div class="hero-trust">
          <span>{icon('shield',18)} Board-certified physicians</span>
          <span>{icon('lock',18)} Private &amp; HIPAA-aligned</span>
          <span>{icon('dollar',18)} Transparent pricing</span>
        </div>
      </div>
      <div class="hero-card">
        <span class="price-pop">From ${PRICE_VISIT}</span>
        <h3>Three ways we help men feel like themselves</h3>
        <p class="muted">Pick what fits, your physician confirms it is right for you.</p>
        <ul class="checklist">
          <li><span class="ck">{icon('check',13)}</span><b>GLP-1 weight loss</b>, semaglutide &amp; tirzepatide</li>
          <li><span class="ck">{icon('check',13)}</span><b>Testosterone (TRT)</b>, confirmed by bloodwork first</li>
          <li><span class="ck">{icon('check',13)}</span><b>ED treatment</b>, discreet and effective</li>
          <li><span class="ck">{icon('check',13)}</span>Ongoing monitoring, labs &amp; dose adjustments</li>
        </ul>
        <a href="{BOOKING_URL}" class="btn btn-primary btn-block">Book a consult</a>
      </div>
    </div>
  </div>
</section>

<section class="section-teal" style="padding:46px 0;">
  <div class="container">
    <div class="trust-strip">
      <div><div class="ts-num">${PRICE_VISIT}</div><div class="ts-label">Flat consult, no surprises</div></div>
      <div><div class="ts-num">15 min</div><div class="ts-label">Typical first visit</div></div>
      <div><div class="ts-num">Lab-based</div><div class="ts-label">Evidence over guesswork</div></div>
      <div><div class="ts-num">Statewide</div><div class="ts-label">Care anywhere in Florida</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="prose center" style="max-width:760px;">
      <p class="lead">You are busy, you are skeptical of the hype, and you have heard enough bro-science to last a lifetime. Good. Men's Metabolic treats men's health like the medicine it is, careful diagnosis, proven treatments, and a physician who tells you the truth, including when the answer is no.</p>
      <p>Below are the three areas men ask us about most. Each one starts the same way: a real conversation with a board-certified physician who builds a plan around your health, not a sales target.</p>
    </div>
  </div>
</section>
{prog_html}

<section class="section section-cloud">
  <div class="container">
    <div class="section-header">
      <span class="section-label">How It Works</span>
      <h2>From first question to steady progress</h2>
      <p>Four simple steps. The hard part, the monitoring and adjusting, is on us.</p>
    </div>
    <div class="steps">{steps_html}</div>
    <div class="center" style="margin-top:40px;"><a href="/how-it-works/" class="btn btn-ghost">See the full process</a></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <span class="section-label">Straight Answers</span>
      <h2>The honest answers to what you're thinking</h2>
      <p>No pressure and no spin. Here is what most men want to know before they book.</p>
    </div>
    <div class="grid grid-3">{obj_html}</div>
  </div>
</section>

<section class="section section-teal">
  <div class="container">
    <div class="section-header">
      <span class="section-label">Care That Lasts</span>
      <h2>This is a relationship, not a refill</h2>
      <p>The results men are proud of come from steady, monitored care over time, not a one-time prescription.</p>
    </div>
    <div class="grid grid-3" style="max-width:980px;margin:0 auto;">
      <div class="card" style="background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.14);">
        <div class="ic" style="background:rgba(255,255,255,.12);color:#9FE8DD;">{icon('calendar',24)}</div>
        <h3 style="color:#fff;">Monthly check-ins</h3>
        <p style="color:rgba(255,255,255,.82);">Short, regular visits to track progress, celebrate wins, and keep you accountable.</p>
      </div>
      <div class="card" style="background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.14);">
        <div class="ic" style="background:rgba(255,255,255,.12);color:#9FE8DD;">{icon('flask',24)}</div>
        <h3 style="color:#fff;">Lab monitoring</h3>
        <p style="color:rgba(255,255,255,.82);">Routine bloodwork makes sure your treatment is working and your numbers stay healthy.</p>
      </div>
      <div class="card" style="background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.14);">
        <div class="ic" style="background:rgba(255,255,255,.12);color:#9FE8DD;">{icon('chat',24)}</div>
        <h3 style="color:#fff;">Message anytime</h3>
        <p style="color:rgba(255,255,255,.82);">Question about a side effect or a dose? Reach your care team without booking a new visit.</p>
      </div>
    </div>
    <p class="center" style="margin-top:30px;color:rgba(255,255,255,.85);">Dose adjustments, lab reviews, and follow-up are not upsells, they are simply how responsible care works.</p>
  </div>
</section>

<section class="section section-sand">
  <div class="container">
    <div class="section-header">
      <span class="section-label">Questions</span>
      <h2>Men's health, answered</h2>
    </div>
    <div class="faq-list">{faq_items}</div>
  </div>
  <script type="application/ld+json">{json.dumps(faq_schema)}</script>
</section>
"""
    html += render_cta_band(
        "Ready to feel like yourself again?",
        f"Book a private 15-minute consult with a board-certified physician. Flat ${PRICE_VISIT}, no insurance, no waiting room, care anywhere in Florida.")
    html += render_footer()
    write_page(["mens-health", "index.html"], html)


# ---------------------------------------------------------------------------
# Child service pages: /mens-health/weight-loss/, /testosterone-trt/, /ed/
# ---------------------------------------------------------------------------
def render_breadcrumb(trail):
    """trail = [(label, url_or_None), ...]; last item is current page."""
    cells, schema_items = [], []
    sep = '<span style="opacity:.45;margin:0 8px;">/</span>'
    for i, (label, url) in enumerate(trail, 1):
        lead = sep if i > 1 else ""
        if url:
            cells.append(f'<li>{lead}<a href="{url}">{e(label)}</a></li>')
        else:
            cells.append(f'<li>{lead}<span style="color:var(--ink-soft);">{e(label)}</span></li>')
        schema_items.append({"@type": "ListItem", "position": i, "name": label,
                             "item": BASE_URL + (url or "")})
    inner = "".join(cells)
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": schema_items}
    return (f'<div class="container" style="padding-top:96px;padding-bottom:0;">'
            f'<ol style="list-style:none;display:flex;flex-wrap:wrap;gap:8px;align-items:center;'
            f'font-size:.86rem;color:var(--ink-soft);">{inner}</ol></div>'
            f'<script type="application/ld+json">{json.dumps(schema)}</script>')


CHILD_PAGES = {
    "weight-loss": {
        "slug": "weight-loss",
        "og": "og-weight-loss.png",
        "title": "GLP-1 Weight Loss for Men in Tampa, FL | Men's Metabolic",
        "meta": "Doctor-led GLP-1 weight loss for men in Tampa and across Florida. Semaglutide and tirzepatide, lab-guided and monitored. No insurance, flat ${PRICE_VISIT} consult.",
        "kw": "GLP-1 weight loss for men",
        "crumb": "GLP-1 Weight Loss",
        "eyebrow": "GLP-1 Weight Loss, Tampa &amp; statewide Florida",
        "h1": "GLP-1 weight loss for men in Tampa, <em>built on real medicine.</em>",
        "sub": "If diet and the gym keep failing you, the problem may be your metabolism, not your discipline. Our physicians prescribe GLP-1 medications like semaglutide and tirzepatide, matched to your health and monitored over time, so the weight actually comes off and stays off.",
        "card_h": "Your GLP-1 plan includes",
        "card_points": [
            "Physician review of your health and eligibility",
            "Semaglutide or tirzepatide matched to you",
            "Dosing that starts low and adjusts over time",
            "Side-effect management and check-ins",
            "Nutrition and habit guidance, not just a script",
        ],
        "stats": [("Lab-guided", "Care, not guesswork"), ("Weekly", "Simple dosing"),
                  ("Monitored", "Dose adjusted over time"), ("Statewide", "Anywhere in Florida")],
        "body": [
            ("How GLP-1 medication actually works", [
                "GLP-1 medications mimic a hormone your body already makes after you eat. They calm appetite, slow how fast your stomach empties, and help steady blood sugar. In plain terms: you feel full sooner, the constant food noise quiets down, and the changes you make to how you eat finally stick.",
                "This is not a stimulant and it is not a crash diet. It is a tool that makes sustainable change possible, paired with a physician who keeps an eye on your progress.",
            ]),
            ("Semaglutide vs tirzepatide, which is right for you?", [
                "Both are proven GLP-1-based medications, and both can lead to meaningful weight loss alongside lifestyle change. They work slightly differently, and men respond differently to each.",
                "Your physician helps you choose based on your health history, your goals, how your body tolerates treatment, and cost. There is no one-size-fits-all answer, which is exactly why a real doctor is involved.",
            ]),
            ("What results are realistic?", [
                "Done right, GLP-1 weight loss is steady, not dramatic, usually a sustainable pace that protects muscle and is easier to keep off. We will set honest expectations with you up front and adjust as your body responds.",
                "We are not interested in selling you a quick fix. We are interested in helping you build a leaner, healthier metabolism you can maintain for years.",
            ]),
            ("Is it safe? What about side effects?", [
                "GLP-1 medications have a well-studied safety profile when prescribed for the right person and monitored properly. The most common side effects, mild nausea or digestive changes early on, usually fade and can often be managed by adjusting your dose.",
                "Your physician reviews your full health picture before prescribing, tells you the trade-offs in plain language, and stays available between visits if anything feels off.",
            ]),
        ],
        "faqs": [
            ("How do I get started with GLP-1 weight loss?",
             f"Book a ${PRICE_VISIT} video consult. Your physician reviews your health, confirms whether GLP-1 treatment is appropriate, and, if it is, sends your medication to the pharmacy of your choice with a clear plan."),
            ("Do I need labs first?",
             "Often yes. Bloodwork helps your physician prescribe safely and rule out anything that needs attention first. We make ordering labs near you simple, and we review the results with you."),
            ("Will I have to take it forever?",
             "Not necessarily. Many men use GLP-1 medication to reach a healthier weight while building habits that keep it off, then taper with their physician's guidance. Your plan is reviewed continually, not set in stone."),
            ("Is the medication included in the price?",
             "The consult and your physician's care are covered by the visit or membership price. The medication itself is billed separately by the pharmacy, and we will tell you what to expect before you commit."),
        ],
        "cta_h": "Ready to lose the weight for good?",
        "cta_p": f"Book a ${PRICE_VISIT} video consult and find out if GLP-1 treatment is right for you. Lab-guided, physician-led, statewide in Florida.",
    },
    "testosterone-trt": {
        "slug": "testosterone-trt",
        "og": "og-trt.png",
        "title": "Testosterone Therapy (TRT) in Florida | Men's Metabolic",
        "meta": "Lab-based testosterone replacement therapy (TRT) for men in Tampa and across Florida. Diagnosed with real bloodwork, physician-monitored. Flat ${PRICE_VISIT} consult, no insurance.",
        "kw": "testosterone replacement therapy (TRT) online",
        "crumb": "Testosterone (TRT)",
        "eyebrow": "Testosterone Therapy, Tampa &amp; statewide Florida",
        "h1": "Testosterone therapy (TRT) for men in Tampa, <em>done the responsible way.</em>",
        "sub": "Low energy, brain fog, stalled workouts, low drive. These can be signs of low testosterone, and they are treatable. We diagnose it with real bloodwork, then build a monitored plan, no guessing, no shortcuts.",
        "card_h": "Your TRT plan includes",
        "card_points": [
            "Bloodwork to confirm low testosterone",
            "Board-certified physician review of your full health",
            "A treatment plan matched to your levels and goals",
            "Follow-up labs to keep therapy safe",
            "Honest guidance, including when TRT is not right",
        ],
        "stats": [("Lab-based", "Diagnosed, not guessed"), ("Monitored", "Follow-up labs"),
                  ("Physician-led", "Real oversight"), ("Private", "HIPAA-aligned")],
        "body": [
            ("Could it be low testosterone?", [
                "Testosterone naturally declines with age, but a meaningful drop can leave you tired, foggy, heavier around the middle, and less interested in things you used to enjoy. Many men assume it is just getting older. Sometimes it is. Sometimes it is treatable.",
                "The only way to know is to measure it. That is why we start with bloodwork, not a sales pitch.",
            ]),
            ("How we diagnose it, the right way", [
                "We confirm low testosterone with lab testing and review your full health history before recommending treatment. Because testosterone is a regulated medication, this step is not optional, it is what makes therapy safe and appropriate.",
                "If your levels are normal, we will tell you, and we will look for what else might be driving how you feel. We would rather be honest than sell you something you do not need.",
            ]),
            ("What treatment looks like", [
                "If TRT is right for you, your physician builds a plan matched to your levels, symptoms, and goals, and explains exactly what to expect. From there, the focus shifts to monitoring, periodic labs and check-ins to confirm it is working and your numbers stay healthy.",
                "This is ongoing medical care, not a one-time prescription handed out and forgotten.",
            ]),
            ("Safety and monitoring", [
                "Testosterone therapy is well understood when it is properly supervised. Follow-up labs let your physician keep your dose dialed in and watch the markers that matter, so you get the benefits while staying safe.",
                "You will always have a real physician overseeing your care and a way to reach your team between visits.",
            ]),
        ],
        "faqs": [
            ("Can I really get TRT through telehealth?",
             "Yes, when it is clinically appropriate and confirmed by bloodwork. Because testosterone is a regulated medication, we require lab testing and physician review first, and we monitor you with follow-up labs throughout treatment."),
            ("What labs do I need?",
             "Typically a testosterone panel along with related bloodwork your physician selects based on your history. We make it easy to get your blood drawn near you, then review the results with you."),
            ("How is the medication delivered?",
             "Once your physician confirms TRT is right for you and builds your plan, your prescription is sent to the pharmacy of your choice. Your physician will walk you through your options and what to expect."),
            ("What if TRT is not right for me?",
             "Then we will not prescribe it. If your levels are normal or therapy is not appropriate, we will tell you honestly and help you figure out what is actually driving your symptoms."),
        ],
        "cta_h": "Want to know your real numbers?",
        "cta_p": f"Book a ${PRICE_VISIT} consult and start with the bloodwork that tells the truth. Physician-led, monitored TRT, statewide in Florida.",
    },
    "ed": {
        "slug": "ed",
        "og": "og-ed.png",
        "title": "ED Treatment Online in Tampa, FL | Discreet Men's Care",
        "meta": "Discreet, doctor-led ED treatment online for men in Tampa and across Florida. Proven options, private video visits, sent to your pharmacy. Flat ${PRICE_VISIT} consult.",
        "kw": "ED treatment online",
        "crumb": "ED Treatment",
        "eyebrow": "ED Treatment, Tampa &amp; statewide Florida",
        "h1": "ED treatment online in Tampa, <em>private and effective.</em>",
        "sub": "Erectile dysfunction is common, and it is very treatable. A private video visit gets you proven treatment without the waiting room, and a physician who also checks the health signals behind it.",
        "card_h": "Your ED visit includes",
        "card_points": [
            "A private, judgment-free video visit",
            "Proven options like sildenafil and tadalafil",
            "A look at underlying causes, not just symptoms",
            "Discreet delivery to your pharmacy",
            "Follow-up to adjust if needed",
        ],
        "stats": [("Private", "No waiting room"), ("Proven", "Evidence-based options"),
                  ("Discreet", "Sent to your pharmacy"), ("Statewide", "Anywhere in Florida")],
        "body": [
            ("You are far from alone", [
                "ED affects a large share of men, and it becomes more common with age. It is a medical issue, not a character flaw, and treating it is routine. The hardest part for most men is bringing it up, which is exactly why we made it private and simple.",
            ]),
            ("Why ED can be a health signal", [
                "Erections depend on healthy blood flow, so ED can sometimes be an early sign of issues with blood pressure, cholesterol, blood sugar, sleep, stress, or hormones. That is why our physicians look at the bigger picture instead of only treating the symptom.",
                "Often, addressing the underlying drivers improves more than your sex life, it improves your overall metabolic health.",
            ]),
            ("Treatment options that work", [
                "When appropriate, your physician can prescribe well-established medications such as sildenafil or tadalafil, matched to your health and how you want to use them. They will explain the differences, the trade-offs, and what to expect, then send your prescription discreetly to the pharmacy you choose.",
                "If your first plan is not the right fit, you have ongoing access to adjust it.",
            ]),
            ("Private, secure, and judgment-free", [
                "Your visit happens by secure video, and your information is protected with HIPAA-aligned technology. The conversation stays strictly between you and your care team. No awkward front desk, no waiting room, no judgment.",
            ]),
        ],
        "faqs": [
            ("How does online ED treatment work?",
             f"Book a private ${PRICE_VISIT} video visit. Your physician reviews your health, discusses options, and, when appropriate, sends treatment discreetly to your pharmacy. The whole visit usually takes about 15 minutes."),
            ("Which ED medication is best?",
             "It depends on your health and how you prefer to use it. Sildenafil and tadalafil work differently in terms of timing and duration. Your physician will help you choose and adjust if needed."),
            ("Is it discreet?",
             "Completely. Visits are private and HIPAA-aligned, and prescriptions are sent to the pharmacy of your choice. Your care stays between you and your physician."),
            ("Do you check for underlying causes?",
             "Yes. Because ED can signal issues with blood flow, blood sugar, or hormones, your physician looks at the bigger picture and can order labs when it makes sense, so you treat the cause, not just the symptom."),
        ],
        "cta_h": "Get back to feeling like yourself.",
        "cta_p": f"Book a private ${PRICE_VISIT} video visit for discreet, effective ED care. Physician-led, statewide in Florida.",
    },
}


def build_child_page(key):
    d = CHILD_PAGES[key]
    meta = d["meta"].replace("${PRICE_VISIT}", PRICE_VISIT)

    stats = "".join(
        f'<div><div class="ts-num">{n}</div><div class="ts-label">{l}</div></div>'
        for n, l in d["stats"])
    card_pts = "".join(
        f'<li><span class="ck">{icon("check",13)}</span>{e(x)}</li>' for x in d["card_points"])

    body = ""
    for h, paras in d["body"]:
        body += f"<h2>{e(h)}</h2>"
        for para in paras:
            body += f"<p>{e(para)}</p>"

    faq_items = ""
    for q, a in d["faqs"]:
        faq_items += (f'<div class="faq-item"><button class="faq-q">{e(q)}</button>'
                      f'<div class="faq-a"><p>{e(a)}</p></div></div>')
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}}
                                 for q, a in d["faqs"]]}

    other = [(CHILD_PAGES[k]["crumb"], "/mens-health/" + CHILD_PAGES[k]["slug"] + "/")
             for k in CHILD_PAGES if k != key]
    related = "".join(f'<a href="{u}" class="btn btn-ghost">{e(lbl)}</a>' for lbl, u in other)

    html = render_head(d["title"], meta, f"/mens-health/{d['slug']}/", og_image=d["og"])
    html += render_nav()
    html += render_breadcrumb([("Home", "/"), ("Men's Health", "/mens-health/"),
                               (d["crumb"], None)])
    html += f"""
<section class="hero" style="padding-top:30px;">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow"><span class="dot"></span>{d['eyebrow']}</span>
        <h1>{d['h1']}</h1>
        <p class="hero-sub">{e(d['sub'])}</p>
        <div class="hero-cta-row">
          <a href="{BOOKING_URL}" class="btn btn-primary btn-lg">{icon('video',20)} Book a consult, ${PRICE_VISIT}</a>
          <a href="/eligibility/" class="btn btn-ghost btn-lg">{icon('check',18)} 60-second eligibility check</a>
        </div>
        <div class="hero-trust">
          <span>{icon('shield',18)} Board-certified physicians</span>
          <span>{icon('lock',18)} Private &amp; HIPAA-aligned</span>
          <span>{icon('dollar',18)} Transparent pricing</span>
        </div>
      </div>
      <div class="hero-card">
        <span class="price-pop">From ${PRICE_VISIT}</span>
        <h3>{e(d['card_h'])}</h3>
        <p class="muted">Evidence-based care, monitored over time.</p>
        <ul class="checklist">{card_pts}</ul>
        <a href="{BOOKING_URL}" class="btn btn-primary btn-block">Book a consult</a>
      </div>
    </div>
  </div>
</section>

<section class="section-teal" style="padding:42px 0;">
  <div class="container"><div class="trust-strip">{stats}</div></div>
</section>
{render_emergency_notice()}
<section class="section">
  <div class="container">
    <div class="prose">{body}</div>
  </div>
</section>

<section class="section section-sand">
  <div class="container">
    <div class="section-header">
      <span class="section-label">Questions</span>
      <h2>{e(d['crumb'])}, answered</h2>
    </div>
    <div class="faq-list">{faq_items}</div>
  </div>
  <script type="application/ld+json">{json.dumps(faq_schema)}</script>
</section>

<section class="section">
  <div class="container center">
    <span class="section-label">Explore More</span>
    <h2 style="margin-bottom:24px;">Other ways we help men</h2>
    <div class="hero-cta-row" style="justify-content:center;">{related}
      <a href="/mens-health/" class="btn btn-ghost">All men's health</a>
    </div>
  </div>
</section>
"""
    html += render_cta_band(d["cta_h"], d["cta_p"])
    html += render_footer()
    write_page(["mens-health", d["slug"], "index.html"], html)


def build_child_pages():
    for key in CHILD_PAGES:
        build_child_page(key)


# ---------------------------------------------------------------------------
# Eligibility quiz (client-side, submits qualified leads to Netlify Forms)
# ---------------------------------------------------------------------------
def build_eligibility():
    states_js = json.dumps(BUSINESS["states_licensed"])
    quiz_css = """
<style>
.quiz-wrap{max-width:660px;margin:0 auto}
.quiz-card{background:#fff;border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);padding:34px;min-height:340px;display:flex;flex-direction:column}
.quiz-progress{height:8px;background:var(--cloud);border-radius:100px;overflow:hidden;margin-bottom:26px}
.quiz-progress span{display:block;height:100%;background:var(--mint);width:0;transition:width .3s ease}
.quiz-step{animation:qfade .25s ease}
@keyframes qfade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.quiz-q{font-family:var(--font-d);font-size:1.5rem;font-weight:600;margin-bottom:8px;color:var(--ink)}
.quiz-help{color:var(--ink-soft);font-size:.96rem;margin-bottom:22px}
.quiz-opts{display:flex;flex-direction:column;gap:12px}
.quiz-opt{text-align:left;width:100%;padding:16px 18px;border:1.5px solid var(--line);border-radius:var(--radius-sm);background:#fff;font-size:1rem;font-weight:500;font-family:inherit;color:var(--ink);cursor:pointer;transition:all var(--t);display:flex;align-items:center;gap:12px}
.quiz-opt:hover{border-color:var(--teal);background:var(--teal-light)}
.quiz-opt .dotmark{width:20px;height:20px;border-radius:50%;border:2px solid var(--line);flex-shrink:0}
.quiz-opt:hover .dotmark{border-color:var(--teal)}
.quiz-fields .fg{margin-bottom:16px}
.quiz-fields label{display:block;font-size:.86rem;font-weight:600;margin-bottom:6px}
.quiz-fields input{width:100%;padding:13px 15px;border:1.5px solid var(--line);border-radius:var(--radius-sm);font-size:1rem;font-family:inherit}
.quiz-fields input:focus{outline:none;border-color:var(--teal)}
.quiz-foot{margin-top:auto;padding-top:24px;display:flex;justify-content:space-between;align-items:center}
.quiz-back{background:none;border:none;color:var(--ink-soft);font-family:inherit;font-size:.92rem;cursor:pointer;padding:8px}
.quiz-back:hover{color:var(--teal)}
.quiz-result{text-align:center}
.quiz-result .rico{width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 18px}
.quiz-result.ok .rico{background:var(--mint);color:#fff}
.quiz-result.warn .rico{background:#FFF4E6;color:#B26A00}
.quiz-result h2{margin-bottom:10px}
.quiz-result p{margin-bottom:8px}
</style>
"""
    html = render_head(
        "Am I Eligible? 60-Second Check | " + SITE_NAME,
        "Take a quick, private 60-second check to see if telehealth for GLP-1 weight loss, testosterone (TRT), or ED is a fit for you. No obligation.",
        "/eligibility/",
        extra_head=quiz_css,
        og_image="og-eligibility.png",
    )
    html += render_nav()
    html += render_breadcrumb([("Home", "/"), ("Eligibility Check", None)])
    html += f"""
<section class="hero" style="padding-top:30px;padding-bottom:50px;">
  <div class="container">
    <div class="center" style="max-width:660px;margin:0 auto 30px;">
      <span class="eyebrow"><span class="dot"></span>60-Second Eligibility Check</span>
      <h1 style="margin-bottom:14px;">See if you're a fit, privately</h1>
      <p class="hero-sub" style="margin:0 auto;">A few quick questions, no commitment. Your answers are private and used only to match you with the right care.</p>
    </div>
    <div class="quiz-wrap">
      <div class="quiz-card">
        <div class="quiz-progress"><span id="qbar"></span></div>
        <div id="quiz-mount"></div>
        <form id="elig-form" name="eligibility-quiz" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thank-you/" style="display:none;">
          <input type="hidden" name="form-name" value="eligibility-quiz">
          <p style="display:none;"><label>Skip: <input name="bot-field"></label></p>
          <input type="hidden" name="goal" id="f-goal">
          <input type="hidden" name="answers" id="f-answers">
          <input type="hidden" name="result" id="f-result">
          <input type="hidden" name="state" id="f-state">
          <input type="hidden" name="name" id="f-name">
          <input type="hidden" name="email" id="f-email">
          <input type="hidden" name="phone" id="f-phone">
        </form>
      </div>
      <p class="form-note" style="margin-top:16px;">{icon('lock',14)} Private &amp; HIPAA-aligned. This check is not a medical diagnosis and is not for emergencies.</p>
    </div>
  </div>
</section>
<script>
(function(){{
  var STATES = {states_js};
  var BOOKING = "{BOOKING_URL}";
  var goalQ = {{
    "weight-loss": {{q:"Have you struggled to lose weight despite diet and exercise?", help:"This helps us understand if GLP-1 treatment may help.", opts:[["Yes, it keeps coming back","yes"],["Somewhat","some"],["No","no"]]}},
    "trt": {{q:"Do you have symptoms like low energy, low drive, or brain fog?", help:"Common signs that can point to low testosterone.", opts:[["Yes, several","many"],["One or two","some"],["Not really","no"]]}},
    "ed": {{q:"How often does ED affect you?", help:"Your answers stay private.", opts:[["Often","often"],["Sometimes","sometimes"],["Rarely","rarely"]]}},
    "metabolic": {{q:"What matters most to you right now?", help:"We'll tailor your visit around it.", opts:[["More energy","energy"],["Better labs / numbers","labs"],["Overall health","overall"]]}}
  }};
  var steps = [
    {{id:"goal", q:"What are you hoping to improve?", help:"Pick the one that fits best, you can discuss more on your visit.",
      opts:[["Lose weight (GLP-1)","weight-loss"],["Energy, drive & testosterone","trt"],["Sexual health (ED)","ed"],["Overall metabolic health","metabolic"]]}},
    {{id:"age", q:"What's your age range?", help:"We care for men 18 and older.",
      opts:[["18-39","18-39"],["40-59","40-59"],["60 or older","60+"],["Under 18","under-18"]]}},
    {{id:"state", q:"Which state will you be in for your visit?", help:"Telehealth law requires you to be located where your physician is licensed.", opts:"STATES"}},
    {{id:"goalq"}},  // placeholder, filled from goalQ based on goal
    {{id:"safety", q:"Are you having any of these right now?", help:"Chest pain, trouble breathing, or signs of a stroke.",
      opts:[["No, none of these","ok"],["Yes, one or more","emergency"]]}},
    {{id:"contact"}}
  ];

  var answers = {{}}, idx = 0;
  var mount = document.getElementById("quiz-mount");
  var bar = document.getElementById("qbar");

  function setBar(){{ bar.style.width = Math.round((idx/(steps.length-1))*100)+"%"; }}

  function optBtn(label,val,onClick){{
    var b=document.createElement("button");
    b.type="button"; b.className="quiz-opt";
    b.innerHTML='<span class="dotmark"></span>'+label;
    b.onclick=function(){{ onClick(val,label); }};
    return b;
  }}

  function footer(showBack){{
    var f=document.createElement("div"); f.className="quiz-foot";
    var back=document.createElement("button");
    back.type="button"; back.className="quiz-back"; back.textContent="\\u2190 Back";
    back.onclick=function(){{ idx=Math.max(0,idx-1); render(); }};
    f.appendChild(showBack?back:document.createElement("span"));
    f.appendChild(document.createElement("span"));
    return f;
  }}

  function resolveStep(){{
    var s=steps[idx];
    if(s.id==="goalq"){{ var g=goalQ[answers.goal]||goalQ["metabolic"]; return {{id:"goalq",q:g.q,help:g.help,opts:g.opts}}; }}
    return s;
  }}

  function advance(){{ idx++; render(); }}

  function showResult(kind,title,body,cta){{
    setBar();
    var wrap=document.createElement("div");
    wrap.className="quiz-step quiz-result "+(kind==="ok"?"ok":"warn");
    var ic=kind==="ok"?'{icon("check",38)}':'{icon("alert",34)}';
    wrap.innerHTML='<div class="rico">'+ic+'</div><h2>'+title+'</h2>'+body;
    var box=document.createElement("div"); box.style.marginTop="22px"; box.innerHTML=cta;
    wrap.appendChild(box);
    mount.innerHTML=""; mount.appendChild(wrap);
    bar.style.width="100%";
  }}

  function renderContact(){{
    setBar();
    var wrap=document.createElement("div"); wrap.className="quiz-step";
    wrap.innerHTML='<div class="quiz-q">Good news, you look like a fit.</div>'+
      '<p class="quiz-help">Tell us where to send next steps and a care team member will reach out. No charge to ask.</p>'+
      '<div class="quiz-fields">'+
      '<div class="fg"><label>Full name</label><input id="q-name" type="text" placeholder="Your name" required></div>'+
      '<div class="fg"><label>Email</label><input id="q-email" type="email" placeholder="you@email.com" required></div>'+
      '<div class="fg"><label>Phone</label><input id="q-phone" type="tel" placeholder="(000) 000-0000" required></div>'+
      '</div>';
    var btn=document.createElement("button");
    btn.type="button"; btn.className="btn btn-primary btn-block btn-lg"; btn.textContent="See my next steps";
    btn.onclick=function(){{
      var n=document.getElementById("q-name").value.trim();
      var em=document.getElementById("q-email").value.trim();
      var ph=document.getElementById("q-phone").value.trim();
      if(!n||!em||!ph){{ alert("Please fill in your name, email, and phone."); return; }}
      document.getElementById("f-goal").value=answers.goal||"";
      document.getElementById("f-answers").value=JSON.stringify(answers);
      document.getElementById("f-result").value="eligible";
      document.getElementById("f-state").value=answers.state||"";
      document.getElementById("f-name").value=n;
      document.getElementById("f-email").value=em;
      document.getElementById("f-phone").value=ph;
      var form=document.getElementById("elig-form");
      form.style.display="block"; form.submit();
    }};
    wrap.appendChild(btn);
    wrap.appendChild(footer(true));
    mount.innerHTML=""; mount.appendChild(wrap);
  }}

  function render(){{
    var s=resolveStep();
    if(s.id==="contact"){{ renderContact(); return; }}
    setBar();
    var wrap=document.createElement("div"); wrap.className="quiz-step";
    var h='<div class="quiz-q">'+s.q+'</div>';
    if(s.help) h+='<p class="quiz-help">'+s.help+'</p>';
    wrap.innerHTML=h;
    var opts=document.createElement("div"); opts.className="quiz-opts";
    var list = s.opts==="STATES" ? STATES.map(function(x){{return [x,x];}}).concat([["Another state","other"]]) : s.opts;
    list.forEach(function(o){{
      opts.appendChild(optBtn(o[0],o[1],function(val){{
        answers[s.id==="goalq"?"goalDetail":s.id]=val;
        // Disqualifiers / branches
        if(s.id==="age" && val==="under-18"){{
          showResult("warn","We care for men 18 and older",
            "<p>Thanks for checking. Our telehealth services are available to men 18 and older.</p>",
            '<a href="/" class="btn btn-ghost">Back to Home</a>'); return;
        }}
        if(s.id==="state" && val==="other"){{
          showResult("warn","Not in your state, yet",
            "<p>We're expanding fast. Leave us a note and we'll tell you the moment we reach your state.</p>",
            '<a href="/contact/" class="btn btn-primary">Join the waitlist</a>'); return;
        }}
        if(s.id==="safety" && val==="emergency"){{
          showResult("warn","Please seek care now",
            "<p><b>This may be an emergency.</b> Telehealth is not for emergencies. Call 911 or go to the nearest ER right away.</p>",
            '<a href="tel:911" class="btn btn-primary">Call 911</a>'); return;
        }}
        advance();
      }}));
    }});
    wrap.appendChild(opts);
    wrap.appendChild(footer(idx>0));
    mount.innerHTML=""; mount.appendChild(wrap);
  }}

  render();
}})();
</script>
"""
    html += render_footer()
    write_page(["eligibility", "index.html"], html)


# ---------------------------------------------------------------------------
# sitemap.xml + robots.txt
# ---------------------------------------------------------------------------
def build_sitemap_robots():
    public_paths = [
        "/", "/how-it-works/", "/what-we-treat/", "/mens-health/",
        "/mens-health/weight-loss/", "/mens-health/testosterone-trt/", "/mens-health/ed/",
        "/pricing/", "/about/", "/faq/", "/eligibility/", "/contact/",
    ]
    today = datetime.now().strftime("%Y-%m-%d")
    urls = ""
    for p in public_paths:
        pr = "1.0" if p == "/" else "0.8"
        urls += f"  <url>\n    <loc>{BASE_URL}{p}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{pr}</priority>\n  </url>\n"
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    write_page(["sitemap.xml"], sitemap)

    robots = f"""User-agent: *
Allow: /
Disallow: /thank-you/
Disallow: /privacy/
Disallow: /terms/
Disallow: /telehealth-consent/

Sitemap: {BASE_URL}/sitemap.xml
"""
    write_page(["robots.txt"], robots)


# ---------------------------------------------------------------------------
# Static assets: logo + favicon + minimal OG (SVG)
# ---------------------------------------------------------------------------
def build_assets():
    logo = """<svg xmlns="http://www.w3.org/2000/svg" width="280" height="48" viewBox="0 0 280 48">
<circle cx="16" cy="24" r="8" fill="#1FB8A0"/>
<circle cx="16" cy="24" r="13" fill="none" stroke="#E6F4F4" stroke-width="4"/>
<text x="38" y="32" font-family="Georgia, serif" font-size="24" font-weight="600" fill="#10243B">Men's <tspan fill="#0E7C86">Metabolic</tspan></text>
</svg>
"""
    write_page(["images", "logo.svg"], logo)

    favicon = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="#0E7C86"/>
<circle cx="32" cy="32" r="11" fill="#1FB8A0"/>
<circle cx="32" cy="32" r="17" fill="none" stroke="#9FE8DD" stroke-width="4"/>
</svg>
"""
    write_page(["favicon.svg"], favicon)


# ---------------------------------------------------------------------------
# Copy committed static files (static/**) into dist/ verbatim.
# ---------------------------------------------------------------------------
def copy_static():
    global page_count
    if not os.path.isdir(STATIC_DIR):
        return
    import shutil
    for root, _dirs, files in os.walk(STATIC_DIR):
        rel = os.path.relpath(root, STATIC_DIR)
        for fn in files:
            src = os.path.join(root, fn)
            dst = os.path.join(DIST_DIR, rel, fn) if rel != "." else os.path.join(DIST_DIR, fn)
            ensure_dir(os.path.dirname(dst))
            shutil.copy2(src, dst)
            page_count += 1


# ---------------------------------------------------------------------------
# Netlify form-detection stub (so both forms are registered at build time)
# ---------------------------------------------------------------------------
def build_netlify_form_stub():
    # A hidden static copy of the forms helps Netlify's build-time form detection.
    stub = """<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>
<form name="visit-request" data-netlify="true" netlify-honeypot="bot-field" hidden>
  <input name="name"><input name="phone"><input name="email"><input name="state">
  <input name="reason"><input name="preferred_time"><textarea name="message"></textarea>
</form>
<form name="eligibility-quiz" data-netlify="true" netlify-honeypot="bot-field" hidden>
  <input name="goal"><input name="answers"><input name="result">
  <input name="name"><input name="email"><input name="phone"><input name="state">
</form>
</body></html>"""
    write_page(["forms.html"], stub)


# ---------------------------------------------------------------------------
# Custom 404 (Netlify serves /404.html automatically)
# ---------------------------------------------------------------------------
def build_404():
    html = render_head(
        "Page Not Found | " + SITE_NAME,
        "That page could not be found. Explore men's metabolic health care at " + SITE_NAME + ".",
        "/404.html",
        extra_head='<meta name="robots" content="noindex,follow">',
    )
    html += render_nav()
    html += f"""
<section class="page-hero" style="padding-bottom:90px;">
  <div class="container">
    <span class="eyebrow"><span class="dot"></span>404</span>
    <h1>We couldn't find that page</h1>
    <p>It may have moved. Here is where most men head next.</p>
    <div class="hero-cta-row" style="justify-content:center;margin-top:28px;">
      <a href="/" class="btn btn-primary">Back to Home</a>
      <a href="/mens-health/" class="btn btn-ghost">Men's Health</a>
      <a href="{BOOKING_URL}" class="btn btn-ghost">Book a Visit</a>
    </div>
  </div>
</section>
"""
    html += render_footer()
    write_page(["404.html"], html)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    import shutil
    if os.path.isdir(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    ensure_dir(DIST_DIR)

    build_home()
    build_how_it_works()
    build_what_we_treat()
    build_mens_health()
    build_child_pages()
    build_pricing()
    build_about()
    build_faq()
    build_contact()
    build_eligibility()
    build_thank_you()
    build_404()
    build_legal()
    build_sitemap_robots()
    build_assets()
    build_netlify_form_stub()
    copy_static()

    print(f"Build complete. {page_count} files written to {DIST_DIR}")


if __name__ == "__main__":
    main()
