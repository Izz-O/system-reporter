import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Keys match the product ids the catalog service should use
STOCK = {
    "camping-tent":    {"name": "Camping Tent",    "quantity": 14},
    "hiking-backpack": {"name": "Hiking Backpack", "quantity": 32},
    "fishing-rod":     {"name": "Fishing Rod",     "quantity": 0},
}


def with_status(sku, item):
    return {
        "id": sku,
        "name": item["name"],
        "quantity": item["quantity"],
        "in_stock": item["quantity"] > 0,
    }


class InventoryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content_type = "application/json"

        if self.path == "/api/stock":
            body = json.dumps([with_status(k, v) for k, v in STOCK.items()]).encode()
        elif self.path.startswith("/api/stock/"):
            sku = self.path.rsplit("/", 1)[-1]
            if sku not in STOCK:
                self.send_error(404, "Unknown product")
                return
            body = json.dumps(with_status(sku, STOCK[sku])).encode()
        elif self.path == "/":
            rows = "".join(
                f"<li>{v['name']}: "
                f"{'In stock (' + str(v['quantity']) + ')' if v['quantity'] > 0 else 'Out of stock'}"
                f"</li>"
                for v in STOCK.values()
            )
            body = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>Trailside Inventory</title>
<body style="font-family: sans-serif; margin: 50px; background: #eefee8; color: #23412b;">
<h1>Trailside Inventory</h1>
<p>Current stock levels.</p>
<ul>{rows}</ul>
<a href="/api/stock">View stock data</a>
</body>
</html>""".encode()
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
    server = ThreadingHTTPServer(("0.0.0.0", 8002), InventoryHandler)
    print("Inventory running on port 8002", flush=True)
    server.serve_forever()
