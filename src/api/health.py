"""W2-002 /health endpoint — Python stdlib only (no external deps).

Fixes F-001: the previous implementation depended on Flask, which was never
declared in any dependency manifest, so the endpoint was non-reproducible in a
clean environment (pytest collection failed with ModuleNotFoundError; the server
could not start). This module uses only the Python standard library so the
endpoint works wherever Python runs, with no external dependencies to declare.

Contract: see contracts/api-health.md — GET /health -> 200 {"status": "ok"}.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def health_response():
    """Return (status_code, headers, body_bytes) for GET /health.

    Pure function for unit testing; the HTTP handler below renders it.
    """
    body = json.dumps({"status": "ok"}).encode("utf-8")
    return 200, {"Content-Type": "application/json"}, body


class HealthHandler(BaseHTTPRequestHandler):
    """Minimal HTTP handler exposing GET /health."""

    def do_GET(self):  # noqa: N802 (BaseHTTPRequestHandler API)
        if self.path == "/health":
            status, headers, body = health_response()
            self.send_response(status)
            for key, value in headers.items():
                self.send_header(key, value)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()

    def log_message(self, *args):  # silence default request logging
        pass


def serve(host="127.0.0.1", port=8000):
    """Run the dev server (entry point for `python3 src/api/health.py`)."""
    HTTPServer((host, port), HealthHandler).serve_forever()


if __name__ == "__main__":
    serve()
