import pytest
from app import schemas
from jose import jwt
from app.config import settings
from . import conftest

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == 'Python API Development'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "test@mail.com", "password": "test123"})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "test@mail.com"
    assert res.status_code == 201

def test_login_user(client, test_user1):
    res = client.post("/login", data={"username": test_user1["email"], "password": test_user1["password"]})

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(token=login_res.access_token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert test_user1["id"] == payload.get("user_id")
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize(("email", "password", "status_code"), [
    ("wrong" + conftest.user_data1["email"], conftest.user_data1["password"], 403),
    (conftest.user_data1["email"], conftest.user_data1["password"] + "wrong", 403),
    ("wrong" + conftest.user_data1["email"], conftest.user_data1["password"] + "wrong", 403),
    (None, conftest.user_data1["password"], 422),
    (conftest.user_data1["email"], None, 422),
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    if (res.status_code == 403):
        assert res.json().get("detail") == "Invalid Credentials"





