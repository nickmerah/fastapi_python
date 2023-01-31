from random import randrange
from time import sleep
from fastapi import FastAPI, Response, status, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from typing import Optional
import psycopg2


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='root', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Db Connected")
        break

    except Exception as error:
        print("Db Connection Failed")
        print("Error: ", error)
        sleep(2)

app = FastAPI()


my_posts = [{
    "id": 1,
    "title": "title of Post 1",
    "content": "content of post 1"
},
    {
        "id": 2,
        "title": "title of Post 2",
        "content": "content of post 2"
    }]


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return 1


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
async def root():
    return {"message": "Welcome to Python API in Ubuntu"}


@app.get("/posts")
async def get_posts():
    cursor.execute('''select * from posts''')
    posts = cursor.fetchall()
    return {"posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s,%s, %s ) RETURNING * ''',
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"post": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute('''select * from posts WHERE id = %s''', str(id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    return {"post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('''select * from posts WHERE id = %s''', str(id),)
    delete_post = cursor.fetchone()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")

    cursor.execute('''delete from posts WHERE id = %s''', str(id),)
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute('''UPDATE posts SET title= %s, content= %s, published= %s WHERE id = %s RETURNING * ''',
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")

    return {"post": updated_post}
