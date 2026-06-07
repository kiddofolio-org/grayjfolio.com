# grayjfolio.com

A static art-archive site for Gray J. — Template B in the Kiddofolio family of kid portfolio templates.

This is the light, gallery-wall counterpart to [willamonet.com](https://willamonet.com) (Template A, dark/archive). Same stack, intentionally different design.

## Design
- **Mode:** light default (optional dark toggle), localStorage key `gray-theme`
- **Type:** Fraunces serif headings, Inter sans body
- **Accent:** muted terracotta-orange
- **Grid:** uniform framed mats (gallery wall)
- **Detail pages:** museum-placard layout (centered art + wall label + prev/next pager)
- **Scope:** Hero → Art archive → Contact → Footer only

## Stack
- Static HTML / CSS / minimal JS, no framework
- Hosting: Cloudflare Pages (auto-deploy on push to `main`)
- Contact form: Formspree (AJAX submit + honeypot)
- Domain: grayjfolio.com

## Layout
```
index.html         Hero, art grid, contact form, footer
css/styles.css     Single stylesheet
js/theme.js        Light/dark toggle
js/contact.js      AJAX contact form
art/               One HTML per artwork, museum-placard layout + prev/next
assets/            Images (*-full.jpg @1600px, *-thumb.jpg @800px), favicon.svg
build_art_pages.py Regenerates art detail pages from the PIECES list
```

## Privacy rules (hard)
- No photos of Gray
- No full surname, school name, exact city, address, or phone
- OK to mention Metro Georgia
- Blur any names/teacher names/school markings before publishing

## Image pipeline
1. PDF scans → `pdftoppm -jpeg -r 200`
2. Resize with Pillow `.thumbnail((1600,1600))` → `<slug>-full.jpg`
3. Resize with Pillow `.thumbnail((800,800))` → `<slug>-thumb.jpg`

## Footer
`© <year> Gray J. · Last updated: <YYYY-MM-DD>` — year auto-updates via JS; last-updated is manual.

## Deploy
`git push origin main` → Cloudflare Pages auto-deploys.
