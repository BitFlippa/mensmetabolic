# Men's Metabolic

Static site generator for **mensmetabolic.com** — a direct-pay men's
metabolic and hormone health telehealth practice. Board-certified physicians
by video for medical weight loss (GLP-1), testosterone (TRT), and ED, with
transparent flat pricing and no insurance.

## Build

```bash
python3 src/build.py
```

Output goes to `dist/`. No dependencies beyond Python 3.

## Pages

- `/` — Home
- `/how-it-works/`
- `/what-we-treat/`
- `/mens-health/` — men's health hub (GLP-1, TRT, ED)
  - `/mens-health/weight-loss/` — GLP-1 weight loss landing page
  - `/mens-health/testosterone-trt/` — testosterone / TRT landing page
  - `/mens-health/ed/` — ED treatment landing page
- `/pricing/`
- `/about/`
- `/faq/`
- `/eligibility/` — interactive 60-second eligibility quiz (Netlify Forms)
- `/contact/` — booking / lead form (Netlify Forms)
- `/thank-you/` — form success page (both forms redirect here)
- `/privacy/`, `/terms/`, `/telehealth-consent/` — legal (template)
- `404.html` — custom not-found page (served automatically by Netlify)
- `sitemap.xml`, `robots.txt`, `favicon.svg`, `images/logo.svg`
- Per-page Open Graph share images in `images/og-*.png`

## Open Graph / social share images

Branded 1200x630 OG images live in `static/images/og-*.png` and are copied
verbatim into `dist/` by the build (so the build needs no image libraries).
Each key page references its own card. Regenerate them only when branding,
prices, or messaging change:

```bash
pip install Pillow
python3 tools/make_og.py
```

The generator pulls live price/state values from `src/build.py`, so the
cards stay in sync with the `BUSINESS` config.

## Eligibility quiz

`/eligibility/` is a self-contained, client-side multi-step quiz (no
framework). It screens by goal, age, state, and a safety question, gently
handles disqualifiers (under 18, out-of-state waitlist, emergency → 911),
then captures contact details and submits qualified leads to the Netlify
form `eligibility-quiz`. The "60-second eligibility check" CTAs across the
site point here.

## Before going live — edit `src/build.py` `BUSINESS` config

Everything trust-related reads from one config block at the top of
`src/build.py`. Replace all `# TODO` values:

- **phone / email** — real contact details
- **states_licensed** — the states your physician(s) are licensed in
  (telehealth law requires the patient be located in a licensed state)
- **price_visit / price_membership_mo** — your real direct-pay prices
- **legal_name** — your real PLLC / entity name
- **BOOKING_URL** — point at your real HIPAA-compliant scheduler
  (defaults to the on-site `/contact/` form)
- **About page** — add real physician name(s), photo, credentials, and
  license numbers (several states require this to be displayed)
- **Legal pages** — have a healthcare attorney review the templates
- **og-cover.png** — add a real social-share image at `images/og-cover.png`

## Compliance notes baked in

- "Not for emergencies — call 911" notices on care pages and footer
- **TRT handling:** testosterone is a Schedule III controlled substance.
  Copy states it is prescribed only after bloodwork confirms low
  testosterone, and the site-wide policy excludes high-risk controlled
  substances (opioids, stimulants, benzodiazepines) rather than all
  controlled substances. Confirm your physicians are set up to prescribe
  testosterone via telehealth under current state/DEA rules.
- No invented testimonials or unverified ratings (`show_rating` is off)
- Telehealth informed-consent page and HIPAA-aligned privacy language

## Deploy

Netlify: build `python3 src/build.py`, publish `dist` (no base directory needed,
this repo is the site root). The booking form uses Netlify Forms (`visit-request`).
