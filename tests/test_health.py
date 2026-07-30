"""Tests for the /health endpoint — Python stdlib only (no Flask).

Covers both acceptance items of W2-002:
  * GET /health returns 200 + JSON {"status": "ok"}  (test_health_via_http)
  * unit test test_health.py passes                    (whole module via pytest)
"""

import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import HTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "api"))

from health import health_response, HealthHandler  # noqa: E402


def test_health_response_payload():
    """Pure-function check: status 200, json content-type, body {"status":"ok"}."""
    status, headers, body = health_response()
    assert status == 200
    assert headers.get("Content-Type") == "application/json"
    assert json.loads(body) == {"status": "ok"}


def test_health_via_http():
    """Integration check: real GET /health over HTTP -> 200 + {"status":"ok"}."""
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        time.sleep(0.1)  # let the listener bind
        with urllib.request.urlopen(
            "http://127.0.0.1:{}/health".format(port), timeout=2
        ) as resp:
            assert resp.status == 200
            assert resp.headers.get("Content-Type") == "application/json"
            assert json.loads(resp.read()) == {"status": "ok"}
    finally:
        server.shutdown()


def test_unknown_path_is_404():
    """Non-/health paths return 404 (sanity, does not break the contract)."""
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        time.sleep(0.1)
        try:
            urllib.request.urlopen(
                "http://127.0.0.1:{}/nope".format(port), timeout=2
            )
            assert False, "expected HTTPError 404"
        except urllib.error.HTTPError as err:
            assert err.code == 404
    finally:
        server.shutdown()
