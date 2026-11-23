import json
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Product ids and prices match the catalog and inventory services
PRODUCTS = {
    "camping-tent":    {"name": "Camping Tent",    "price": 129.99},
    "hiking-backpack": {"name": "Hiking Backpack", "price": 59.99},
    "fishing-rod":     {"name": "Fishing Rod",     "price": 44.99},
}

ORDERS = [
    {"id": "1001", "customer": "Alex", "status": "Shipped",
     "items": [{"product": "camping-tent", "qty": 1}, {"product": "hiking-backpack", "qty": 1}]},
    {"id": "1002", "customer": "Sam", "status": "Processing",
     "items": [{"product": "fishing-rod", "qty": 2}]},
    {"id": "1003", "customer": "Jordan", "status": "Delivered",
     "items": [{"product": "hiking-backpack", "qty": 2}, {"product": "fishing-rod", "qty": 1}]},
]


def build(order):
    items, total = [], 0.0
    for it in order["items"]:
        p = PRODUCTS[it["product"]]
        line = round(p["price"] * it["qty"], 2)
        total += line
        items.append({"product": it["product"], "name": p["name"],
                      "qty": it["qty"], "line_total": line})
    return {"id": order["id"], "customer": order["customer"],
            "status": order["status"], "items": items, "total": round(total, 2)}


def render_page():
    rows = ""
    for o in map(build, ORDERS):
        names = ", ".join(f'{i["qty"]} x {escape(i["name"])}' for i in o["items"])
        rows += (f'<tr><td>#{escape(o["id"])}</td><td>{escape(o["customer"])}</td>'
                 f'<td>{names}</td><td>${o["total"]:.2f}</td><td>{escape(o["status"])}</td></tr>\n')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Trailside Orders</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 50px; background: #eefee8; color: #23412b; }}
  table {{ border-collapse: collapse; background: white; }}
  th {{ background: #2e6b3f; color: white; text-align: left; padding: 10px 16px; }}
  td {{ padding: 10px 16px; border-top: 1px solid #e3ebdf; }}
</style>
</head>
<body>
<h1>Trailside Orders</h1>
<p>Sample customer orders.</p>
<table>
<tr><th>Order</th><th>Customer</th><th>Items</th><th>Total</th><th>Status</th></tr>
{rows}</table>
<p><a href="/api/orders">View order data</a></p>
</body>
</html>""".encode()


class OrdersHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content_type = "application/json"

        if self.path == "/api/orders":
            body = json.dumps([build(o) for o in ORDERS]).encode()
        elif self.path.startswith("/api/orders/"):
            oid = self.path.rsplit("/", 1)[-1]
            match = next((o for o in ORDERS if o["id"] == oid), None)
            if match is None:
                self.send_error(404, "Unknown order")
                return
            body = json.dumps(build(match)).encode()
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
    server = ThreadingHTTPServer(("0.0.0.0", 8003), OrdersHandler)
    print("Orders running on port 8003", flush=True)
    server.serve_forever()
