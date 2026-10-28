"""
Local web server for the pages in this folder, like `python -m http.server`, but it tells the browser
not to cache, so a refresh always shows the latest version of demo.html, lenses.html, chain_viewer.html.

Run from the IS folder:
    python scripts/serve.py          then open http://localhost:8000/demo.html
"""
import http.server, sys


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class Server(http.server.ThreadingHTTPServer):
    # on Windows "reuse" lets a second server silently share the port; fail loudly instead
    allow_reuse_address = False


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    try:
        server = Server(("", port), NoCache)
    except OSError:
        sys.exit(f"Port {port} is already in use: another server is running. Stop it first (Ctrl+C in its terminal).")
    print(f"Serving this folder at http://localhost:{port}/demo.html  (no caching) · Ctrl+C to stop", flush=True)
    server.serve_forever()
