import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


PRODUCTS = [
     {"name": "Camping Tent", "price": 129.99},
     {"name": "Hiking Backpack", "price": 59.99},
     {"name": "Fishing Rod", "price": 44.99},
]

class CatalogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/products":
           body = json.dumps(PRODUCTS).encode()
           content_type = "application/json"
        elif self.path == "/":
            items = "".join(
                f"<li>{p['name']} - ${p['price']:.2f}</li>"
                for p in PRODUCTS
            )
            body = f"""
            <!doctype html>
            <html lang="en">
            <meta charset="utf-8">
            <title>Trailside Outdoor Catalog</title>
            <body style="font-family: sans-serif: margin: 50px;
                         background: #eefed; color: #23412b;">
               <h1>Trailside Outdoor Catalog</h1>
               <p>Sample equipment for your next adventure.</p>
               <ul>{items}</u>
               <a href="/api/products">View product data<a/>
               </body>
               </html>
               """.encode()
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
