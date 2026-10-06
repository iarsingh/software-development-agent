import pytest
from fastapi.testclient import TestClient
from devagent.main import app

client = TestClient(app)


def test_goal_aware_plan_reports_scope_without_applying():
    r = client.post("/agent/run", json={"goal": "add healthz endpoint", "payload": {"files": ["src/api.py", "src/api.py"]}}).json()
    assert r["goal"] == "add healthz endpoint"
    assert r["files"] == ["src/api.py"]
    assert "API handler" in r["plan"][1]
    assert r["acceptance_checks"] and r["planner"] == "deterministic"
    assert r["applied"] is False


@pytest.mark.parametrize("filename", ["../outside.py", "/etc/passwd", "C:/outside.py", "a\\b.py"])
def test_plan_rejects_paths_outside_workspace(filename):
    assert client.post("/agent/run", json={"goal": "add test", "payload": {"files": [filename]}}).status_code == 422


def test_non_mapping_payload_and_excessive_goal_are_rejected():
    assert client.post("/agent/run", json={"goal": "add test", "payload": [1]}).status_code == 422
    assert client.post("/agent/run", json={"goal": "x" * 2001}).status_code == 422
