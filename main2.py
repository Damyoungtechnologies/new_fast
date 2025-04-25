from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict
from uuid import uuid4
app = FastAPI()
users = {
    "user1": "token1",
    "user2": "token2",
}

posts_db: Dict[str, dict] = {}
class Post (BaseModel):
    title : str
    content: str
class PostResponse(Post):
    id: str
    owner: str
def get_current_user(token:str):
    for user, user_token in users.items():
        if token == user_token:
            return user
    raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/posts/", response_model=PostResponse)
def create_post(post: Post, user: str = Depends(get_current_user)):
    post_id = str(uuid4())
    new_post = {"id":post_id, "title":post.title, "content":post.content, "owner":user}
    posts_db[post_id] = new_post
    return new_post
@app.get("/posts/", response_model=list(PostResponse))
def get_post():
    return list(posts_db.values())