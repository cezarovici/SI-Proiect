from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ------------------------ TEST CASES ------------------------

def test_create_algorithm():
    response = client.post(
        "/algorithms/",
        json={
            "name": "Test Algorithm", 
            "type": "symmetric",
            "parameters": '{"param1": "value1"}'
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Algorithm"

def test_get_algorithms():
    response = client.get("/algorithms/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_update_algorithm():
    create_response = client.post(
        "/algorithms/",
        json={"name": "Old Algorithm", "type": "symmetric", "parameters": '{"param1": "value1"}'}
    )
    algorithm_id = create_response.json()["algorithm_id"]

    response = client.put(
        f"/algorithms/{algorithm_id}",
        json={"name": "Updated Algorithm"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Algorithm"

def test_delete_algorithm():
    create_response = client.post(
        "/algorithms/",
        json={"name": "Delete Me", "type": "symmetric", "parameters": '{"param1": "value1"}'}
    )
    algorithm_id = create_response.json()["algorithm_id"]

    response = client.delete(f"/algorithms/{algorithm_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Algorithm deleted"
