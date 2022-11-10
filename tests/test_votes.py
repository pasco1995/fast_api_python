import pytest
from app import models

@pytest.fixture
def test_vote(session, test_posts, test_user1):
    session.add(models.Vote(post_id=test_posts[1].id, user_id=test_user1["id"]))
    session.commit()

def test_vote_post(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    assert res.status_code == 201
    assert res.json() == {"message": "Successfully added vote."}

def test_vote_post_twice(authorized_client, test_posts, test_user1, test_vote):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[1].id, "dir": 1})

    assert res.status_code == 409
    assert res.json().get("detail") == f'User {test_user1["id"]} has already voted on post {test_posts[1].id}.'

def test_delte_vote_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[1].id, "dir": 0})

    assert res.status_code == 201
    assert res.json() == {"message": "Successfully deleted vote."}

def test_delte_vote_on_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[1].id, "dir": 0})

    assert res.status_code == 404
    assert res.json().get("detail") == f'Vote does not exist.'

def test_vote_post_non_exist(authorized_client):
    res = authorized_client.post(f"/vote/", json={"post_id": 9999, "dir": 1})

    assert res.status_code == 404
    assert res.json().get("detail") == f'Post with id {9999} not found.'

def test_vote_unauthorized_user(client, test_posts):
    res = client.post(f"/vote/", json={"post_id": test_posts[0].id, "dir": 1})

    assert res.status_code == 401
    assert res.json().get("detail") == f'Not authenticated'
