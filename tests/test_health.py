import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "api"))

from health import app

def test_health_returns_200_and_ok():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}
