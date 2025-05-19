import requests
import pytest

BASE_URL = "http://localhost:8000/performance/"

# Fixture pentru a crea o performanță și a returna ID-ul
@pytest.fixture(scope="module")
def new_performance_id():
    payload = {
        "file_id": 1,
        "algorithm_id": 1,
        "key_id": 1,
        "operation_type": "encrypt",
        "execution_time_ms": 123.45,
        "memory_usage_mb": 56.78,
        "success": True,
        "error_message": None
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code in [200, 201]
    perf = response.json()
    assert "performance_id" in perf
    return perf["performance_id"]

def test_create_performance():
    payload = {
        "file_id": 1,
        "algorithm_id": 1,
        "key_id": 1,
        "operation_type": "decrypt",
        "execution_time_ms": 98.76,
        "memory_usage_mb": 45.67,
        "success": False,
        "error_message": "Test error"
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code in [200, 201]
    perf = response.json()
    assert "performance_id" in perf
    assert perf["operation_type"] == payload["operation_type"]
    assert perf["success"] == payload["success"]

def test_read_all_performances():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    perfs = response.json()
    assert isinstance(perfs, list)
    if perfs:
        assert "performance_id" in perfs[0]
        assert "operation_type" in perfs[0]

def test_read_performance_by_id(new_performance_id):
    response = requests.get(f"{BASE_URL}{new_performance_id}")
    assert response.status_code == 200
    perf = response.json()
    assert perf["performance_id"] == new_performance_id
    assert "execution_time_ms" in perf

def test_delete_performance(new_performance_id):
    response = requests.delete(f"{BASE_URL}{new_performance_id}")
    assert response.status_code == 200
    msg = response.json()
    assert "detail" in msg
    assert msg["detail"] == "Deleted successfully"

def test_read_deleted_performance(new_performance_id):
    response = requests.get(f"{BASE_URL}{new_performance_id}")
    assert response.status_code == 404
