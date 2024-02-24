from http import HTTPStatus
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
token = None


def test_ping():
    response = client.get("/ping")
    assert response.status_code == HTTPStatus.OK
    result = response.json()
    assert len(result) == 1


def test_work():
    global token
    register_data = {"name": "test1", "password": "123"}
    response = client.post("/register", params=register_data)
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        "/auth", data={"username": "test1", "password": "123"}
    )
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    token = response.json()["access_token"]
    print(token)
    assert token is not None


def test_files_upload():
    global token
    headers = {"Authorization": f"Bearer {token}"}
    file_data = {"file": open("data/test.txt", "rb")}
    params = {"path": "test"}
    response = client.post(
        "files/upload", params=params, headers=headers, files=file_data
    )
    assert response.status_code == HTTPStatus.OK


def test_list_file():
    global token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/files", headers=headers)
    assert response.status_code == HTTPStatus.OK
    result = response.json()
    assert len(result) == 1


def test_files_download():
    global token
    headers = {"Authorization": f"Bearer {token}"}
    params = {"s_path": "test"}
    response = client.get("files/download", params=params, headers=headers)
    print(response.json())
    assert response.status_code == HTTPStatus.OK
