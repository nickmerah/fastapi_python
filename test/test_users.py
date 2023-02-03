from fastapi.testclient import TestClient

from apps.main import app
from apps import schemas

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get('message') == "Welcome to Python API in Ubuntu"


# def test_create_user():
#     response = client.post("/users/", json={"email": "steve@gmail.com", "password": "1111"})
#     newuser = schemas.UserResponse(**response.json())
#     assert response.status_code == 201
#     assert newuser.email == "steve@gmail.com"
#     assert newuser.created_at != ""

def test_login_user():
    response = client.post("/login", data={"username": "hide@gmail.com", "password": "1111"})
    print(response.json())
    assert response.status_code == 200