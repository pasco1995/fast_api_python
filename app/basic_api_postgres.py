from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='postgres',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as e:
        print('Unable to connect to database : ', e)
        time.sleep(3)

# my_posts = [
#     {
#         "title": "this is a title!",
#         "content": "the content",
#         "pulished": False,
#         "id": 1
#     },
#     {
#         "title": "favorite foods",
#         "content": "Pizza & Pasta",
#         "pulished": True,
#         "id": 2
#     },
# ]

@app.get("/")
def root():
    return {"message": "LECTURE : Basic API & PostgeSQL Database"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published,))
    new_post = cursor.fetchall()
    conn.commit()
    return {"message": "Ok", "data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,
                    (str(id),))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')
    return {"message": "Ok", "data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *  """,
                   (str(id),))
    ret = cursor.fetchone()
    conn.commit()
    if ret is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(post: Post, id : int):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, str(post.published), str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')
    return {"message": "Ok", "data": updated_post}



