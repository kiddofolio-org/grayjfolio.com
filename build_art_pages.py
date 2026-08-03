#!/usr/bin/env python3
"""Generate museum-placard art detail pages AND the index art grid for grayjfolio.com.
Single source of truth: the GROUPS list below (school-year groups, newest year first;
within each group, newest first)."""
import os
import re
import html as _html

try:
    from PIL import Image
except ImportError:
    Image = None

ROOT = os.path.dirname(__file__)
ART_DIR = os.path.join(ROOT, "art")
ASSETS_DIR = os.path.join(ROOT, "assets")
os.makedirs(ART_DIR, exist_ok=True)

# Canonical site origin (no trailing slash) used for absolute URLs in SEO tags.
SITE_URL = "https://grayjfolio.com"
SITE_NAME = "Gray J. — Art"
SITE_TAGLINE = "A curated portfolio of preschool artwork by Gray J."
# Default social-share image (used on the homepage and as a fallback).
DEFAULT_OG_IMAGE = f"{SITE_URL}/assets/gray-36-full.jpg"


def esc(s):
    """Escape a string for safe use inside an HTML attribute."""
    return _html.escape(str(s), quote=True)


def is_portrait(slug):
    """True if the piece's thumbnail is taller than it is wide (vertical orientation).
    Vertical pieces get 'fit-contain' so the whole artwork shows in the card (no crop)."""
    if Image is None:
        return False
    path = os.path.join(ASSETS_DIR, f"{slug}-thumb.jpg")
    if not os.path.exists(path):
        return False
    try:
        w, h = Image.open(path).size
        return h > w
    except Exception:
        return False

LAST_UPDATED = "2026-08-03"  # updated 2026-08-03

# School-year groups, NEWEST YEAR FIRST. Within each group, NEWEST FIRST.
#   slug   -> base name; images are assets/<slug>-full.jpg / -thumb.jpg
#   title  -> display title
#   date   -> human label (year, or Mon YYYY)
#   medium -> medium label
GROUPS = [
    {
        "year": "2025\u201326",
        "pieces": [
            {"slug": "gray-37", "title": "St. Simons at Night",      "date": "Jul 2026", "medium": "Acrylic on paper"},
            {"slug": "gray-38", "title": "Abstract Family Portrait", "date": "Jul 2026", "medium": "Acrylic on canvas"},
            {"slug": "gray-39", "title": "Orange Waves",             "date": "Jun 2026", "medium": "Colored pencil on orange paper"},
            {"slug": "gray-36", "title": "Two Hands",        "date": "2025", "medium": "Marker on cut paper"},
            {"slug": "gray-34", "title": "Campfire Hands",   "date": "2025", "medium": "Handprint & cut paper"},
            {"slug": "gray-35", "title": "Red King",         "date": "2025", "medium": "Crayon"},
            {"slug": "gray-30", "title": "Profile",         "date": "2025", "medium": "Pencil on peach paper"},
            {"slug": "gray-14", "title": "Green Hand",      "date": "2025", "medium": "Marker"},
            {"slug": "gray-26", "title": "Three Hearts",    "date": "2025", "medium": "Marker"},
            {"slug": "gray-17", "title": "Big Face",        "date": "2025", "medium": "Marker"},
            {"slug": "gray-11", "title": "Purple Storm",    "date": "2025", "medium": "Marker & colored pencil"},
            {"slug": "gray-16", "title": "Pink Jellyfish",  "date": "2025", "medium": "Marker"},
            {"slug": "gray-19", "title": "Desert Racer",    "date": "2025", "medium": "Crayon on coloring page"},
            {"slug": "gray-23", "title": "Yellow Field",    "date": "2025", "medium": "Marker on yellow paper"},
            {"slug": "gray-29", "title": "Bubbles",         "date": "2025", "medium": "Marker"},
            {"slug": "gray-28", "title": "Sunburst Face",   "date": "2025", "medium": "Marker"},
            {"slug": "gray-15", "title": "Green Letters",   "date": "2025", "medium": "Marker"},
            {"slug": "gray-22", "title": "Rain and Sun",    "date": "2025", "medium": "Marker"},
            {"slug": "gray-18", "title": "Four Flowers",    "date": "2025", "medium": "Crayon"},
            {"slug": "gray-31", "title": "Blue Blizzard",   "date": "2025", "medium": "Crayon"},
            {"slug": "gray-32", "title": "Rainbow Creature","date": "2025", "medium": "Crayon"},
            {"slug": "gray-21", "title": "Sun and Friends", "date": "2025", "medium": "Marker"},
            {"slug": "gray-25", "title": "River Lines",     "date": "2025", "medium": "Marker"},
            {"slug": "gray-20", "title": "Color Steps",     "date": "2025", "medium": "Colored pencil"},
        ],
    },
    {
        "year": "2024\u201325",
        "pieces": [
            {"slug": "gray-01", "title": "Confetti",            "date": "2024",     "medium": "Tempera prints"},
            {"slug": "gray-02", "title": "Night Garden",        "date": "2024",     "medium": "Chalk pastel on black paper"},
            {"slug": "gray-03", "title": "Pink Bloom",          "date": "2024",     "medium": "Tempera on green paper"},
            {"slug": "gray-04", "title": "Driftwood",           "date": "2024",     "medium": "Tempera"},
            {"slug": "gray-05", "title": "Blue Weather",        "date": "2024",     "medium": "Crayon & colored pencil"},
            {"slug": "gray-06", "title": "Raspberry",           "date": "2024",     "medium": "Tempera"},
            {"slug": "gray-08", "title": "Two Lines for Mommy", "date": "Aug 2024", "medium": "Crayon"},
            {"slug": "gray-09", "title": "For Mom",             "date": "Jul 2024", "medium": "Crayon"},
            {"slug": "gray-10", "title": "Green & Black",       "date": "Feb 2024", "medium": "Marker & crayon"},
        ],
    },
]

# Flattened archive order (newest year first, newest-first within group) for pagination.
FLAT = [p for g in GROUPS for p in g["pieces"]]

# ---------------------------------------------------------------- detail pages
PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Gray J. Art</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="author" content="Gray J." />
  <meta name="theme-color" content="#c4622d" />
  <link rel="canonical" href="{page_url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Gray J. — Art" />
  <meta property="og:title" content="{title} — Gray J. Art" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:image" content="{img_url}" />
  <meta property="og:image:alt" content="{title} by Gray J." />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title} — Gray J. Art" />
  <meta name="twitter:description" content="{meta_desc}" />
  <meta name="twitter:image" content="{img_url}" />

  <!-- Structured data: this artwork -->
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"VisualArtwork","name":"{title}","creator":{{"@type":"Person","name":"Gray J."}},"artMedium":"{medium}","artform":"Children's art","url":"{page_url}","image":"{img_url}","isPartOf":{{"@type":"CollectionPage","name":"Gray J. — Art","url":"{site_url}/"}}}}
  </script>

  <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml" />
  <script>
    (function () {{
      try {{
        var t = window["local" + "Storage"].getItem("gray-theme");
        if (t === "dark") document.documentElement.setAttribute("data-theme", "dark");
      }} catch (e) {{}}
    }})();
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Lora:wght@500;600&family=Inter:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../css/styles.css" />
</head>
<body>
  <header class="site-header">
    <nav class="nav">
      <a class="brand" href="../index.html">Gray J.</a>
      <div class="nav-links">
        <a href="../index.html#art">Art</a>
        <a href="../index.html#contact">Contact</a>
        <button class="theme-toggle" type="button" aria-label="Toggle theme">&#9790;</button>
      </div>
    </nav>
  </header>

  <main>
    <section class="detail">
      <div class="wrap">
        <a class="back-link" href="../index.html#art">&larr; Back to the gallery</a>

        <div class="placard">
          <div class="placard-frame">
            <img src="../assets/{slug}-full.jpg" alt="{title} by Gray J." />
          </div>

          <div class="wall-label">
            <h1>{title}</h1>
            <p class="placard-meta">Gray J. &middot; <em>{medium}</em></p>
          </div>
        </div>

        <nav class="pager">
          {prev_html}
          {next_html}
        </nav>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <p>&copy; <span id="year"></span> Gray J. &middot; Made with <a class="credit-link" href="https://kiddofolio.com" target="_blank" rel="noopener">Kiddofolio</a> &middot; Last updated: {updated}</p>
  </footer>

  <script src="../js/theme.js"></script>
  <script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>
"""

for i, p in enumerate(FLAT):
    prev_p = FLAT[i - 1] if i > 0 else None
    next_p = FLAT[i + 1] if i < len(FLAT) - 1 else None

    if prev_p:
        prev_html = (
            f'<a class="prev" href="{prev_p["slug"]}.html">'
            f'<span class="pager-dir">Newer</span>{prev_p["title"]}</a>'
        )
    else:
        prev_html = '<span class="prev disabled"></span>'

    if next_p:
        next_html = (
            f'<a class="next" href="{next_p["slug"]}.html">'
            f'<span class="pager-dir">Older</span>{next_p["title"]}</a>'
        )
    else:
        next_html = '<span class="next disabled"></span>'

    page_url = f'{SITE_URL}/art/{p["slug"]}.html'
    img_url = f'{SITE_URL}/assets/{p["slug"]}-full.jpg'
    meta_desc = f'{p["title"]} — {p["medium"]} artwork by Gray J., part of a curated portfolio of preschool art.'

    html = PAGE.format(
        title=esc(p["title"]), date=esc(p["date"]), medium=esc(p["medium"]), slug=p["slug"],
        prev_html=prev_html, next_html=next_html, updated=LAST_UPDATED,
        page_url=page_url, img_url=img_url, meta_desc=esc(meta_desc), site_url=SITE_URL,
    )
    with open(os.path.join(ART_DIR, f'{p["slug"]}.html'), "w", encoding="utf-8") as f:
        f.write(html)

# Clean up any old placeholder pages (piece-XX.html)
for f in os.listdir(ART_DIR):
    if f.startswith("piece-") and f.endswith(".html"):
        os.remove(os.path.join(ART_DIR, f))

# ---------------------------------------------------------------- index grid
def render_group(group):
    cards = []
    for p in group["pieces"]:
        # Any vertical (portrait) image is shown uncropped inside the card window.
        window_cls = "art-window fit-contain" if is_portrait(p["slug"]) else "art-window"
        cards.append(
            f'''            <a class="art-card" href="art/{p["slug"]}.html">
              <div class="frame"><div class="{window_cls}"><img src="assets/{p["slug"]}-thumb.jpg" alt="{p["title"]} by Gray J." loading="lazy" /></div></div>
              <div class="art-label"><p class="title">{p["title"]}</p><p class="meta">{p["medium"]}</p></div>
            </a>'''
        )
    grid_html = "\n\n".join(cards)
    return f'''        <!-- Year group: {group["year"]} -->
        <div class="year-group">
          <p class="year-label"><span>{group["year"]}</span></p>
          <div class="art-grid">

{grid_html}

          </div>
        </div>'''

groups_html = "\n\n".join(render_group(g) for g in GROUPS)

# Rewrite the index grid: replace everything from the first "<!-- Year group:" marker
# through the matching wrapper close, up to the "<!-- /Year groups -->" sentinel.
index_path = os.path.join(ROOT, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    idx = f.read()

pattern = re.compile(
    r"        <!-- Year group:.*?<!-- /Year groups -->",
    re.DOTALL,
)
replacement = groups_html + "\n        <!-- /Year groups -->"
if pattern.search(idx):
    idx_new = pattern.sub(replacement, idx, count=1)
else:
    # Backwards-compat: original had no sentinel; match the single old group block.
    old = re.compile(r"        <!-- Year group:.*?</div>\n        </div>", re.DOTALL)
    idx_new = old.sub(groups_html + "\n        <!-- /Year groups -->", idx, count=1)

# Update last-updated date in footer
idx_new = re.sub(r"Last updated: \d{4}-\d{2}-\d{2}", f"Last updated: {LAST_UPDATED}", idx_new)

# Keep the homepage's newest-piece social image + gallery structured data in sync.
newest = FLAT[0]["slug"] if FLAT else "gray-36"
newest_img = f"{SITE_URL}/assets/{newest}-full.jpg"
idx_new = re.sub(
    r'(<meta property="og:image" content=")[^"]*(" />)',
    lambda m: m.group(1) + newest_img + m.group(2), idx_new, count=1)
idx_new = re.sub(
    r'(<meta name="twitter:image" content=")[^"]*(" />)',
    lambda m: m.group(1) + newest_img + m.group(2), idx_new, count=1)

# Build an ImageGallery JSON-LD block listing every piece, injected before </head>.
gallery_items = ", ".join(
    '{{"@type":"ImageObject","name":"{name}","contentUrl":"{url}","creator":{{"@type":"Person","name":"Gray J."}}}}'.format(
        name=esc(p["title"]).replace('"', '\\"'),
        url=f'{SITE_URL}/assets/{p["slug"]}-full.jpg')
    for p in FLAT)
gallery_ld = (
    '  <!-- Structured data: full gallery (auto-generated) -->\n'
    '  <script type="application/ld+json">\n'
    '  {"@context":"https://schema.org","@type":"ImageGallery",'
    '"name":"Gray J. \u2014 Art","url":"' + SITE_URL + '/",'
    '"image":[' + gallery_items + ']}\n'
    '  </script>\n'
)
# Remove any prior auto-generated gallery block, then insert a fresh one before </head>.
idx_new = re.sub(
    r'  <!-- Structured data: full gallery \(auto-generated\) -->.*?</script>\n',
    "", idx_new, flags=re.DOTALL)
idx_new = idx_new.replace("</head>", gallery_ld + "</head>", 1)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(idx_new)

# ---------------------------------------------------------------- robots + sitemap
robots = (
    "User-agent: *\n"
    "Allow: /\n\n"
    f"Sitemap: {SITE_URL}/sitemap.xml\n"
)
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots)

urls = [f"{SITE_URL}/"] + [f'{SITE_URL}/art/{p["slug"]}.html' for p in FLAT]
sitemap_entries = "\n".join(
    f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{LAST_UPDATED}</lastmod>\n"
    f"    <changefreq>monthly</changefreq>\n  </url>"
    for u in urls
)
sitemap = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"{sitemap_entries}\n"
    "</urlset>\n"
)
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"Generated {len(FLAT)} detail pages across {len(GROUPS)} year groups + rebuilt index.")
print(f"Wrote robots.txt and sitemap.xml ({len(urls)} URLs). Last updated {LAST_UPDATED}.")
