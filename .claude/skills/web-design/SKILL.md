---
name: web-design
description: Craft high-quality, distinctive websites and UI that avoid the generic "AI slop" look. Use when designing or building any website, landing page, marketing site, web app UI, component, or design system, or when reviewing a site for visual quality, polish, conversion, or accessibility. Covers typography, color, layout/spacing, components, motion, imagery, accessibility, performance, and conversion patterns, plus a pre-ship checklist.
---

# Web Design Craft

Build sites that look intentionally designed by a human with taste, not assembled
from defaults. Most "AI slop" comes from skipping decisions: default fonts,
evenly-spaced equal cards, generic gradients, emoji icons, and hype copy. Make
deliberate choices in every category below.

## The AI-slop tells to eliminate

If a site has these, fix them:
- One default sans (system-ui/Arial/Inter-only) with no display face.
- Emoji used as iconography (🚀✨🔒) instead of a real icon set.
- A center-aligned hero, then 3 identical cards, then a CTA band — the same
  rhythm on every section.
- Purple/blue or teal gradients with a glow blob, used without reason.
- Uniform 12-16px radius + drop shadow on every element.
- Hype copy: "Transform your...", "Unlock the power of...", "Seamlessly...".
- Em dashes and "—" in body copy; perfectly balanced, lifeless layouts.
- Lorem-flavored filler that says nothing specific.
- No focus states, no hover intent, no empty/error states.

## Typography (highest leverage)

- **Pair two faces with contrast**: a display/serif for headings + a clean sans
  for body (e.g. Fraunces/Newsreader + Inter; or a grotesque + humanist sans).
  Avoid one-font sites unless the font is genuinely characterful.
- **Type scale**: pick a ratio (1.2-1.333) and stick to it. Use `clamp()` for
  fluid headings: `clamp(2rem, 5vw, 3.5rem)`.
- **Line length** 60-75ch for body; `max-width` prose, not full-bleed text.
- **Line-height**: ~1.1-1.2 for large headings, 1.5-1.7 for body.
- **Tighten display headings**: `letter-spacing: -0.01em to -0.02em`.
- Use `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs.
- Load only the weights you use; `font-display: swap`.

## Color

- One brand hue + one accent + a neutral ramp. Don't introduce a third bright
  color without a job for it.
- Build a **neutral ramp** (5-7 steps) instead of pure #000/#fff. Text is rarely
  pure black; use a dark ink (#10243B-ish) on near-white (#F7F8FA).
- Check **contrast**: body text >= 4.5:1, large text >= 3:1 (WCAG AA).
- Gradients are fine but should feel like material (subtle, directional), not a
  default radial blob. Prefer tonal shifts within one hue.
- Define everything as CSS custom properties in `:root`.

## Layout & spacing

- **Spacing scale**: multiples of 4px (4/8/12/16/24/32/48/64/96). Consistent
  rhythm is what reads as "designed."
- **Vary section structure**: alternate left/right, asymmetric splits
  (1.1fr/0.9fr), full-bleed vs contained. Don't repeat the same centered block.
- Establish a max content width (1100-1280px) and consistent gutters.
- Use a real grid; align to it. Optical alignment beats mathematical when they
  conflict (e.g. icons, quotation marks).
- Generous whitespace. Crowding reads as cheap.

## Components & detail

- **Icons**: use a real set (inline SVG, consistent stroke width ~1.8px, same
  grid) — never emoji.
- **Don't uniform-radius everything**: pills for tags/buttons, smaller radius for
  cards; or commit to one and apply with intent.
- **Shadows** should imply elevation consistently (one or two tokens), not be
  sprinkled randomly. Soft, low-opacity, color-tinted to the bg.
- **Borders**: hairlines via `color-mix(in srgb, var(--ink) 9%, transparent)`
  read crisper than #ddd.
- Design the **states**: hover (with intent), `:focus-visible` (visible, branded
  outline), active, disabled, loading, empty, and error.

## Motion

- Subtle and purposeful: 150-300ms, ease-out for entrances. Animate transform/
  opacity, not layout.
- Hover should hint affordance (slight lift/color), not bounce.
- Always honor `@media (prefers-reduced-motion: reduce)`.

## Imagery

- Avoid generic stock. Prefer real product/people, custom illustration, or
  abstract brand shapes. If using photos, treat them consistently (duotone,
  same crop ratio, same grain).
- Always set `width`/`height` (prevent CLS), `loading="lazy"` below the fold,
  `fetchpriority="high"` on the LCP image, modern formats (WebP/AVIF).
- Provide meaningful `alt` text.

## Accessibility (non-negotiable, and anti-slop)

- Semantic HTML: real `<nav> <main> <section> <button> <h1-h6>` hierarchy
  (one h1, no skipped levels).
- Visible keyboard focus on every interactive element.
- Labels tied to inputs; errors announced; hit targets >= 44px.
- Color is never the only signal. Respect reduced-motion and color-scheme.

## Performance

- Inline critical CSS for static sites; defer the rest.
- Preconnect to font origins; subset/self-host fonts when possible.
- Keep JS minimal; prefer CSS for interaction. No framework for a brochure site.
- Target good Core Web Vitals (LCP < 2.5s, CLS < 0.1, INP < 200ms).

## Conversion & UX (for marketing sites)

- One clear primary CTA per view; a softer secondary is fine. Don't offer 5
  equal buttons.
- Above the fold: who it's for, the value, and the next step — concrete, not
  abstract.
- Reduce friction: short forms, clear privacy note, real microcopy near actions.
- Trust signals where decisions happen (near pricing, near the form).
- Address the top objections explicitly instead of ignoring them.

## Content & voice

- Specific > generic. "Flat $89 video visit, same day" beats "Affordable,
  convenient care."
- Second person, plain language, short sentences. Cut hype verbs.
- No em/en dashes in shipped copy if the house style forbids them — use commas
  or periods.

## Pre-ship checklist

- [ ] Two-face type system, fluid scale, balanced headings.
- [ ] Brand+accent+neutral ramp; AA contrast verified.
- [ ] 4px spacing scale; sections vary in structure, not one rhythm.
- [ ] Real SVG icons, consistent stroke; no emoji.
- [ ] hover / focus-visible / active / disabled / empty / error states exist.
- [ ] Motion subtle; reduced-motion honored.
- [ ] Images sized, lazy/priority correct, modern formats, alt text.
- [ ] Semantic landmarks, one h1, keyboard navigable, 44px targets.
- [ ] One primary CTA per view; objections + trust signals present.
- [ ] Copy is specific and free of hype/filler.
- [ ] Test at 360px, 768px, 1280px; check dark mode if supported.

## Quick reference: starting CSS tokens

```css
:root{
  --ink:#10243B; --ink-soft:#4A5A6A;
  --brand:#0E7C86; --brand-dark:#0A5A62; --accent:#1FB8A0;
  --bg:#FFFFFF; --bg-soft:#F7F8FA;
  --line:color-mix(in srgb, var(--ink) 9%, transparent);
  --shadow:0 2px 18px rgba(16,36,59,.07);
  --shadow-lg:0 18px 48px rgba(16,36,59,.14);
  --radius:16px; --radius-sm:10px; --radius-pill:100px;
  --step:4px; /* spacing unit */
  --ease:cubic-bezier(.4,0,.2,1);
}
h1,h2,h3{text-wrap:balance;letter-spacing:-.01em}
p{text-wrap:pretty}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
```
