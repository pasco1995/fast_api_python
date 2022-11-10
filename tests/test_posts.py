import pytest
from app import schemas


def test_authorized_user_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    posts = [schemas.PostAndVotesResponse(**post) for post in res.json()]

    assert len(posts) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts/")

    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"

def test_authorized_user_get_one_post(authorized_client, test_posts, test_user1):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    posts = [schemas.PostAndVotesResponse(**res.json())]

    assert len(posts) == 1
    post = posts[0]
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.owner_id == test_user1["id"]

    assert res.status_code == 200

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"

def test_get_one_post_invalid_id(authorized_client):
    res = authorized_client.get(f"/posts/{0xDEAD}")

    assert res.status_code == 404

@pytest.mark.parametrize(("title", "content", "published", "status_code"),[
    ("post title pub", "post content", True, 201),
    ("post title no pub", "post content", False, 201),
    ("post title auto pub", "post content", None, 201),
    (None, "post content", "true", 422),
    ("post title", None, "true", 422),
    (None, None, None, 422),
])
def test_authorized_user_create_post(authorized_client, test_user1, title, content, published, status_code):
    if published is None:
        res = authorized_client.post("/posts/", json={"title": title, "content": content})
    else:
        res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    assert res.status_code == status_code

    if status_code == 201:
        created_post = schemas.PostResponse(**res.json())

        assert created_post.title == title
        assert created_post.content == content
        assert created_post.published == (True if published is None else published)
        assert created_post.owner_id == test_user1["id"]

def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json={"title": "invalid post title", "content": "invalid post content"})

    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"posts/{test_posts[0].id}")

    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"

def test_authorized_user_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_authorized_user_delete_post_non_exist(authorized_client):
    res = authorized_client.delete(f"posts/9999")

    assert res.status_code == 404
    assert res.json().get("detail") == f"Post with id {9999} not found."


def test_authorized_user_delete_other_user_post(authorized_client, test_posts2):
    res = authorized_client.delete(f"posts/{test_posts2[0].id}")

    assert res.status_code == 403
    assert res.json().get("detail") == 'Not authorized to perform requested action.'

def test_authorized_user_update_post(authorized_client, test_posts):
    data = {
        "title": "updated 1st title", 
        "content": "updated first content",
        "id": test_posts[0].id,
        }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_authorized_user_update_other_user_post(authorized_client, test_posts2):
    data = {
        "title": "updated 1st title of second user", 
        "content": "updated first content",
        "id": test_posts2[0].id,
        }

    res = authorized_client.put(f"/posts/{test_posts2[0].id}", json=data)

    assert res.status_code == 403
    assert res.json().get("detail") == 'Not authorized to perform requested action.'

def test_unauthorized_user_update_post(client, test_posts):
    data = {
        "title": "updated 1st title of second user", 
        "content": "updated first content",
        "id": test_posts[0].id,
        }

    res = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"

def test_authorized_user_update_post_non_exist(authorized_client, test_posts):
    data = {
        "title": "updated 1st title of second user", 
        "content": "updated first content",
        "id": 9999,
        }

    res = authorized_client.put(f"posts/9999", json=data)

    assert res.status_code == 404
    assert res.json().get("detail") == f"Post with id 9999 not found."
