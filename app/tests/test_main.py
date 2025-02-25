from fastapi.testclient import TestClient
from main import app
client = TestClient(app)


# Test response
def test_home_status_code():
    response = client.get("/")
    assert response.status_code == 200

# Test is json
def test_home_response_structure():
    response = client.get("/")
    json_data = response.json()
    assert "status_code" in json_data
    assert "detail" in json_data
    assert "result" in json_data

# Test response data
def test_home_response_values():
    response = client.get("/")
    json_data = response.json()
    assert json_data["status_code"] == 200
    assert json_data["detail"] == "ok"
    assert json_data["result"] == "working"

