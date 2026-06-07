#!/usr/bin/env python3
"""Generate museum-placard art detail pages for grayjfolio.com.
Each page links prev/next in archive order (newest first)."""
import os

ART_DIR = os.path.join(os.path.dirname(__file__), "art")
os.makedirs(ART_DIR, exist_ok=True)

# Archive order, newest first. Placeholder data for now.
# When real (anonymized) art arrives, swap title/medium/year/image/description.
PIECES = [
    {"slug": "piece-01", "title": "Untitled No.\u00a01",  "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-02", "title": "Untitled No.\u00a02",  "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-03", "title": "Untitled No.\u00a03",  "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-04", "title": "Untitled No.\u00a04",  "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-05", "title": "Untitled No.\u00a05",  "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-06", "title": "Untitled No.\u00a06",  "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-07", "title": "Untitled No.\u00a07",  "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-08", "title": "Untitled No.\u00a08",  "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-09", "title": "Untitled No.\u00a09",  "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-10", "title": "Untitled No.\u00a010", "year": "2024", "medium": "Mixed media", "desc": ""},
    {"slug": "piece-11", "title": "Untitled No.\u00a011", "year": "2024", "medium": "Mixed media", "desc": ""},
]

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
            {image}
          </div>

          <div class="wall-label">
            <h1>{title}</h1>
            <p class="placard-meta">Gray J. &middot; {year} &middot; <em>{medium}</em></p>
            {desc_html}
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
    <p>&copy; <span id="year"></span> Gray J. &middot; Last updated: 2026-06-07</p>
  </footer>

  <script src="../js/theme.js"></script>
  <script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>
"""

PLACEHOLDER_IMG = (
    '<div class="art-window" style="width:520px;max-width:100%;aspect-ratio:4/3;">'
    '<span class="placeholder">{label}</span></div>'
)

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

    desc_html = f'<p class="description">{p["desc"]}</p>' if p["desc"] else ""

    # Placeholder image window; swap to <img> when real art arrives.
    image = PLACEHOLDER_IMG.format(label=p["title"])

    html = PAGE.format(
        title=p["title"],
        year=p["year"],
        medium=p["medium"],
        desc_html=desc_html,
        image=image,
        prev_html=prev_html,
        next_html=next_html,
    )

    out = os.path.join(ART_DIR, f'{p["slug"]}.html')
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out)

print(f"\nGenerated {len(PIECES)} art detail pages.")
