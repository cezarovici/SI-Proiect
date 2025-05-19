import requests
import pytest

BASE_URL = "http://localhost:8000/algorithms"

@pytest.fixture(scope="module")
def setup_algorithm():
    data = {
        "name": "TestAlgo",
        "type": "symmetric"
    }
    response = requests.post(BASE_URL + "/", json=data)
    assert response.status_code == 200
    algo = response.json()
    yield algo
    requests.delete(f"{BASE_URL}/{algo['algorithm_id']}")

def test_add_algorithm():
    data = {
        "name": "NewAlgo",
        "type": "asymmetric"
    }
    response = requests.post(BASE_URL + "/", json=data)
    print("Status code:", response.status_code)
    print("Response body:", response.text)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "NewAlgo"
    assert result["type"] == "asymmetric"
    delete_resp = requests.delete(f"{BASE_URL}/{response.json()["algorithm_id"]}")
    assert delete_resp.status_code == 200

def test_list_algorithms(setup_algorithm):
    response = requests.get(BASE_URL + "/")
    print("Status code:", response.status_code)
    print("Response body:", response.text)
    assert response.status_code == 200
    algorithms = response.json()
    assert isinstance(algorithms, list)
    assert any(a["algorithm_id"] == setup_algorithm["algorithm_id"] for a in algorithms)

def test_fetch_algorithm(setup_algorithm):
    algorithm_id = setup_algorithm["algorithm_id"]
    response = requests.get(f"{BASE_URL}/{algorithm_id}")
    print("Status code:", response.status_code)
    print("Response body:", response.text)
    assert response.status_code == 200
    algorithm = response.json()
    assert algorithm["algorithm_id"] == algorithm_id

def test_remove_algorithm():
    data = {
        "name": "ToBeDeleted",
        "type": "symmetric"
    }
    response = requests.post(BASE_URL + "/", json=data)
    assert response.status_code == 200
    algorithm_id = response.json()["algorithm_id"]

    delete_resp = requests.delete(f"{BASE_URL}/{algorithm_id}")

    print("DELETE status:", delete_resp.status_code)
    assert delete_resp.status_code == 200
    assert delete_resp.json()["message"] == "Algorithm deleted"

    get_resp = requests.get(f"{BASE_URL}/{algorithm_id}")
    assert get_resp.status_code == 404
