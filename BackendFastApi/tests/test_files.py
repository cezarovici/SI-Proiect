import requests

BASE_URL = "http://localhost:8000/files/"

def test_get_files():
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    files = response.json()
    assert isinstance(files, list), "Response is not a list"
    if files:
        assert "file_id" in files[0], "Missing 'file_id' in first result"
        assert "original_path" in files[0], "Missing 'original_path' in first result"
    print("GET /files/ returned:", files)

def test_get_file_by_id():
    file_id = 1
    response = requests.get(f"{BASE_URL}{file_id}")
    assert response.status_code in [200, 404], f"Unexpected status code: {response.status_code}"

    if response.status_code == 200:
        file_data = response.json()
        assert file_data["file_id"] == file_id
        assert "original_path" in file_data
        print("GET /files/{id} returned:", file_data)
    else:
        print(f"File with ID {file_id} not found (as expected)")

def test_create_file():
    payload = {
        "original_path": "/test/input.txt",
        "encrypted_path": "/test/encrypted.txt",
        "original_hash": "abc123def4567890abc123def4567890abc123def4567890abc123def4567890",
        "encrypted_hash": "def456abc1237890def456abc1237890def456abc1237890def456abc1237890",
        "algorithm_id": 1,
        "key_id": 1
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code in [200, 201], f"Unexpected status code: {response.status_code}"
    file_data = response.json()
    assert "file_id" in file_data, "Missing 'file_id' in response"
    assert file_data["original_path"] == payload["original_path"]
    print("POST /files/ created:", file_data)
