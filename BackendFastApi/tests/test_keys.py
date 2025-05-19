import requests
import pytest

BASE_URL = "http://localhost:8000/keys/"

@pytest.fixture(scope="module")
def new_key_id():
    payload = {
        "algorithm_id": 1,
        "key_name": "pytestkey",
        "key_value": "val",
        "public_key": "pubkey",
        "private_key": "privkey",
        "expiration_date": None,
        "is_active": True
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code in [200, 201]
    key = response.json()
    assert "key_id" in key
    return key["key_id"]

def test_add_key():
    payload = {
        "algorithm_id": 1,
        "key_name": "pytestkey2",
        "key_value": "val",
        "public_key": "pubkey",
        "private_key": "privkey",
        "expiration_date": None,
        "is_active": True
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code in [200, 201]
    key = response.json()
    assert "key_id" in key
    assert key["key_name"] == payload["key_name"]

def test_list_keys():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    keys = response.json()
    assert isinstance(keys, list)
    if keys:
        assert "key_id" in keys[0]
        assert "key_name" in keys[0]

def test_fetch_key_by_id(new_key_id):
    response = requests.get(f"{BASE_URL}{new_key_id}")
    assert response.status_code == 200
    key = response.json()
    assert key["key_id"] == new_key_id
    assert "key_name" in key

def test_delete_key(new_key_id):
    response = requests.delete(f"{BASE_URL}{new_key_id}")
    assert response.status_code == 200
    msg = response.json()
    assert "message" in msg
    assert msg["message"] == "Key deleted"

def test_fetch_deleted_key(new_key_id):
    response = requests.get(f"{BASE_URL}{new_key_id}")
    assert response.status_code == 404
