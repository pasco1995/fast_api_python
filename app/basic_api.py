from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Response, status, HTTPException

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


my_posts = [
    {
        "title": "this is a title!",
        "content": "the content",
        "id": 1
    },
    {
        "title": "favorite foods",
        "content": "Pizza & Pasta",
        "id": 2
    },
]

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: Post):
    print(payload.dict())
    my_posts.append(
    {
        "title": payload.title,
        "content": payload.content,
        "id": len(my_posts) + 1
    })
    return {"message": "Ok", "data": my_posts[len(my_posts) - 1]}


@app.get("/posts/{id}")
def get_post(id: int):
    for post in my_posts:
        if int(post["id"]) == int(id):
            return {"message": "Ok", "data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with id {id} not found.')

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for idx, post in enumerate(my_posts):
        if int(post["id"]) == int(id):
            del my_posts[idx]
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with id {id} not found.')


@app.put("/posts/{id}")
def update_post(payload: Post, id : int):
    for idx, post in enumerate(my_posts):
        if int(post["id"]) == int(id):
            my_posts[idx] = {
                "title": payload.title,
                "content": payload.content,
                "id": int(id)
            }
            return {"message": "Ok"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with id {id} not found.')
