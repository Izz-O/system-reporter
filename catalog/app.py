import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
PRODUCTS = [
    {"name": "Camping Tent", "price": 129.99},
    {"name": "Hiking Backpack", "price": 59.99},
    {"name": "Fishing Rod", "price": 44.99},
]

ARTWORK = [
    """
    <path d="M30 175L145 40L270 175Z" fill="#c98045"/>
    <path d="M145 40L185 175H85Z" fill="#f4d7a1"/>
    <path d="M145 90L174 175H115Z" fill="#254b3c"/>
    <path d="M20 178H280M145 40V26" stroke="#254b3c"
          stroke-width="5" stroke-linecap="round"/>
    """,
    """
    <path d="M127 50V35Q150 17 173 35V50" fill="none"
          stroke="#244b3c" stroke-width="9"/>
    <rect x="88" y="48" width="124" height="137" rx="28"
          fill="#456b51"/>
    <rect x="82" y="48" width="136" height="49" rx="20"
          fill="#244b3c"/>
    <rect x="111" y="116" width="78" height="51" rx="12"
          fill="#c98045"/>
    <path d="M118 81V109M182 81V109" stroke="#f4d7a1"
          stroke-width="9"/>
    """,
    """
    <path d="M65 178L212 35" stroke="#244b3c"
          stroke-width="7" stroke-linecap="round"/>
    <path d="M58 185L99 145" stroke="#c98045"
          stroke-width="13" stroke-linecap="round"/>
    <circle cx="111" cy="149" r="16" fill="#c98045"/>
    <circle cx="111" cy="149" r="7" fill="#fff8eb"/>
    <path d="M212 35Q247 92 237 147V162Q237 179 222 168"
          fill="none" stroke="#456b51" stroke-width="3"/>
    <path d="M179 189Q202 179 225 189T271 189" fill="none"
          stroke="#8caaa2" stroke-width="4"/>
    """,
]

DESCRIPTIONS = [
    "Make room for a night under the stars.",
    "Find inspiration for your next day on the trail.",
    "Plan a quiet afternoon by the water.",
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trailside | Outdoor Catalog</title>
<style>
:root {
  --green: #234b3b;
  --cream: #f7f4ec;
  --ink: #25392f;
  --muted: #58675e;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; background: var(--cream); color: var(--ink);
  font-family: Arial, Helvetica, sans-serif; line-height: 1.6;
}
a { color: var(--green); text-underline-offset: 4px; }
a:focus-visible { outline: 3px solid #bc6b32; outline-offset: 5px; }
.wrap { max-width: 1120px; margin: auto; padding: 0 28px; }
header { background: white; border-bottom: 1px solid #dedfd5; }
nav {
  min-height: 86px; display: flex; align-items: center;
  justify-content: space-between; gap: 20px; flex-wrap: wrap;
  padding-top: 16px !important; padding-bottom: 16px !important;
}
.brand {
  font-size: 24px; font-weight: 800; letter-spacing: 2px;
  text-decoration: none;
}
nav .links { display: flex; gap: 24px; }
nav .links a { font-size: 14px; font-weight: 700; }
.hero { padding: 64px 0 58px; }
.eyebrow {
  color: #706040; font-size: 12px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
}
h1 {
  font-family: Georgia, serif; font-size: clamp(38px, 6vw, 68px);
  line-height: 1.08; letter-spacing: -2px;
  max-width: 740px; margin: 18px 0;
}
.hero p { color: var(--muted); max-width: 540px; font-size: 18px; }
.button {
  display: inline-block; background: var(--green); color: white;
  border-radius: 8px; padding: 12px 22px; font-weight: 700;
  text-decoration: none;
}
.button:hover { background: #35684f; }
.section-heading {
  display: flex; justify-content: space-between;
  align-items: baseline; gap: 12px; flex-wrap: wrap;
}
h2 { font-size: 25px; margin: 0 0 22px; }
.section-heading span { color: var(--muted); font-size: 14px; }
.grid {
  display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}
.card {
  background: white; border: 1px solid #dedfd5;
  border-radius: 16px; overflow: hidden;
}
.art {
  background: #e8eee2; display: block; width: 100%; height: 220px;
  padding: 16px;
}
.card-body { padding: 24px; }
.category {
  font-size: 11px; letter-spacing: 2px;
  font-weight: 700; color: #706040; text-transform: uppercase;
}
h3 { margin: 8px 0; font-size: 22px; }
.description { min-height: 52px; color: var(--muted); font-size: 14px; }
.price { font-size: 25px; font-weight: 700; margin: 18px 0; }
.stock-link { font-size: 14px; font-weight: 700; }
.banner {
  margin: 36px 0; padding: 28px; border-radius: 14px;
  background: var(--green); color: white;
  display: flex; justify-content: space-between;
  align-items: center; gap: 20px; flex-wrap: wrap;
}
.banner h2 { margin: 0; font-size: 22px; }
.banner p { margin: 6px 0 0; color: #e0e9df; }
.banner .button { background: #f2d4a4; color: var(--green); }
footer {
  padding: 20px 0 32px; color: var(--muted); font-size: 13px;
  border-top: 1px solid #dedfd5;
}
footer a { margin-left: 14px; }
@media (max-width: 760px) {
  .grid { grid-template-columns: 1fr; }
  .hero { padding-top: 36px; }
  .wrap { padding-left: 20px; padding-right: 20px; }
  .description { min-height: auto; }
}
</style>
</head>
<body>
<header>
  <nav class="wrap" aria-label="Main navigation">
    <a class="brand" href="/">TRAILSIDE<span aria-hidden="true"> /</span></a>
    <div class="links">
      <a href="#equipment">Equipment</a>
      <a href="http://192.168.64.8:8002/" data-inventory>Inventory</a>
    </div>
  </nav>
</header>
<main class="wrap">
  <section class="hero">
    <div class="eyebrow">The outdoor collection</div>
    <h1>A little gear.<br>A world to explore.</h1>
    <p>Explore our sample outdoor collection and check availability
       before planning your next adventure.</p>
    <a class="button" href="#equipment">Explore equipment</a>
  </section>
  <section id="equipment" aria-labelledby="equipment-title">
    <div class="section-heading">
      <h2 id="equipment-title">Find your next adventure</h2>
      <span>3 essentials · Illustrated collection</span>
    </div>
    <div class="grid">__CARDS__</div>
  </section>
  <aside class="banner">
    <div>
      <h2>Ready to check availability?</h2>
      <p>Visit our inventory page for current stock information.</p>
    </div>
    <a class="button" href="http://192.168.64.8:8002/" data-inventory>
      Check inventory &rarr;
    </a>
  </aside>
</main>
<footer class="wrap">
  Trailside Outdoor · Student demonstration catalog
  <a href="/api/products">View product data</a>
</footer>
<script>
const inventoryURL = new URL(window.location.href);
inventoryURL.port = "8002";
inventoryURL.pathname = "/";
inventoryURL.search = "";
inventoryURL.hash = "";
document.querySelectorAll("[data-inventory]").forEach(link => {
  link.href = inventoryURL.href;
});
</script>
</body>
</html>
"""


def render_page():
    cards = []
    for product, artwork, description, category in zip(
        PRODUCTS, ARTWORK, DESCRIPTIONS, ["Camp", "Hike", "Fish"]
    ):
        cards.append(f"""
        <article class="card">
          <svg class="art" viewBox="0 0 300 210" role="img"
               aria-label="{product['name']} illustration">
            {artwork}
          </svg>
          <div class="card-body">
            <div class="category">{category}</div>
            <h3>{product['name']}</h3>
            <p class="description">{description}</p>
            <p class="price">${product['price']:.2f}</p>
            <a class="stock-link" data-inventory
               href="http://192.168.64.8:8002/">
              Check availability &rarr;
            </a>
          </div>
        </article>
        """)
    return PAGE.replace("__CARDS__", "".join(cards)).encode("utf-8")


class CatalogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/products":
            body = json.dumps(PRODUCTS).encode("utf-8")
            content_type = "application/json"
        elif self.path == "/":
            body = render_page()
            content_type = "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8001), CatalogHandler)
    print("Catalog running on port 8001", flush=True)
    server.serve_forever()
