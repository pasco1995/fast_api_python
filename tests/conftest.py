from fastapi.testclient import TestClient
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

from app.basic_api_voting import app


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

user_data1 = {"email": "test1_login@mail.com", "password": "test123"}
user_data2 = {"email": "test2_login@mail.com", "password": "test123"}

@pytest.fixture
def test_user1(client):
    res = client.post("/users/", json=user_data1)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data1["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    res = client.post("/users/", json=user_data2)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data2["password"]
    return new_user

@pytest.fixture
def token(test_user1):
    return create_access_token({"user_id": test_user1["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user1, session):
    posts_data = [
        {"title": "1st title", "content": "first content", "owner_id": test_user1["id"]},
        {"title": "2nd title", "content": "second content", "owner_id": test_user1["id"]},
        {"title": "3rd title", "content": "third content", "owner_id": test_user1["id"]},
    ]

    session.add_all([models.Post(**post) for post in posts_data])
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts

@pytest.fixture
def test_posts2(test_user2, session):
    posts_data = [
        {"title": "1st title of second user", "content": "first content", "owner_id": test_user2["id"]},
        {"title": "2nd title of second user", "content": "second content", "owner_id": test_user2["id"]},
        {"title": "3rd title of second user", "content": "third content", "owner_id": test_user2["id"]},
    ]

    session.add_all([models.Post(**post) for post in posts_data])
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts


