from app import schemas
from jose import jwt
from app.config import settings

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == 'Python API Development'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "test@mail.com", "password": "test123"})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "test@mail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(token=login_res.access_token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert test_user["id"] == payload.get("user_id")
    assert login_res.token_type == "bearer"
    assert res.status_code == 200