#!/usr/bin/env python3
"""Generate museum-placard art detail pages AND the index art grid for grayjfolio.com.
Single source of truth: the PIECES list below (archive order, newest first)."""
import os

ROOT = os.path.dirname(__file__)
ART_DIR = os.path.join(ROOT, "art")
os.makedirs(ART_DIR, exist_ok=True)

LAST_UPDATED = "2026-06-07"
YEAR_GROUP = "2024\u201325"

# Archive order, NEWEST FIRST. One dict per artwork.
#   slug      -> base name; images are assets/<slug>-full.jpg / -thumb.jpg
#   title     -> display title
#   date      -> human label (year, or Mon YYYY)
#   medium    -> medium label
PIECES = [
    {"slug": "gray-01", "title": "Confetti",            "date": "2024",      "medium": "Tempera prints"},
    {"slug": "gray-02", "title": "Night Garden",        "date": "2024",      "medium": "Chalk pastel on black paper"},
    {"slug": "gray-03", "title": "Pink Bloom",          "date": "2024",      "medium": "Tempera on green paper"},
    {"slug": "gray-04", "title": "Driftwood",           "date": "2024",      "medium": "Tempera"},
    {"slug": "gray-05", "title": "Blue Weather",        "date": "2024",      "medium": "Crayon & colored pencil"},
    {"slug": "gray-06", "title": "Raspberry",           "date": "2024",      "medium": "Tempera"},
    {"slug": "gray-07", "title": "First Smile",         "date": "Aug 2024",  "medium": "Crayon"},
    {"slug": "gray-08", "title": "Two Lines for Mommy", "date": "Aug 2024",  "medium": "Crayon"},
    {"slug": "gray-09", "title": "For Mom",             "date": "Jul 2024",  "medium": "Crayon"},
    {"slug": "gray-10", "title": "Green & Black",       "date": "Feb 2024",  "medium": "Marker & crayon"},
]

# ---------------------------------------------------------------- detail pages
PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Gray J.</title>
  <meta name="description" content="{title} by Gray J." />
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
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500&display=swap" rel="stylesheet" />
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
            <p class="placard-meta">Gray J. &middot; {date} &middot; <em>{medium}</em></p>
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
    <p>&copy; <span id="year"></span> Gray J. &middot; Last updated: {updated}</p>
  </footer>

  <script src="../js/theme.js"></script>
  <script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>
"""

for i, p in enumerate(PIECES):
    prev_p = PIECES[i - 1] if i > 0 else None
    next_p = PIECES[i + 1] if i < len(PIECES) - 1 else None

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

    html = PAGE.format(
        title=p["title"], date=p["date"], medium=p["medium"], slug=p["slug"],
        prev_html=prev_html, next_html=next_html, updated=LAST_UPDATED,
    )
    out = os.path.join(ART_DIR, f'{p["slug"]}.html')
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

# Clean up any old placeholder pages (piece-XX.html)
for f in os.listdir(ART_DIR):
    if f.startswith("piece-") and f.endswith(".html"):
        os.remove(os.path.join(ART_DIR, f))

# ---------------------------------------------------------------- index grid
cards = []
for p in PIECES:
    cards.append(
        f'''            <a class="art-card" href="art/{p["slug"]}.html">
              <div class="frame"><div class="art-window"><img src="assets/{p["slug"]}-thumb.jpg" alt="{p["title"]} by Gray J." loading="lazy" /></div></div>
              <div class="art-label"><p class="title">{p["title"]}</p><p class="meta">{p["date"]} &middot; {p["medium"]}</p></div>
            </a>'''
    )
grid_html = "\n\n".join(cards)

GRID_BLOCK = f'''        <!-- Year group: {YEAR_GROUP} -->
        <div class="year-group">
          <p class="year-label"><span>{YEAR_GROUP}</span></p>
          <div class="art-grid">

{grid_html}

          </div>
        </div>'''

# Rewrite the index grid between markers.
index_path = os.path.join(ROOT, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    idx = f.read()

import re
pattern = re.compile(r"        <!-- Year group:.*?</div>\n        </div>", re.DOTALL)
idx_new = pattern.sub(GRID_BLOCK, idx, count=1)

# Update last-updated date in footer
idx_new = re.sub(r"Last updated: \d{4}-\d{2}-\d{2}", f"Last updated: {LAST_UPDATED}", idx_new)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(idx_new)

print(f"Generated {len(PIECES)} detail pages + rebuilt index grid. Last updated {LAST_UPDATED}.")
