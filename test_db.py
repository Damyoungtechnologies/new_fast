import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from uuid import uuid4

app = FastAPI()
DB_FIle = "database.json"
def db_load():
    try:    
        with open(DB_FIle) as f_obj:
            return json.load(f_obj)
    except (FileNotFoundError, json.JSONDecodeError):
        return{"users":{}, "posts":[]}
def db_save(db):
    with open(DB_FIle, "w") as f_obj:
        return json.dump(db, f_obj, indent=4)
    
@app.post("/signup")
def db_signup(username: str, password: str):
    db = db_load()
    user = db.get('users',{})
    if username in user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user[username] = password
    db["users"] = user
    db_save(db)
    return {"message": "User created successfully"}

def get_current_user(username: str, password: str):
    db = db_load()
    user = db.get("users", {})
    for user, password in user.items():
        if username == user and password == password:
            return user
        raise HTTPException(status_code=401, detail="Invalid password")

class Post(BaseModel):
    title: str
    content: str

class PostResponse(Post):
    id: str
    owner: str
@app.post("/posts/", response_model=PostResponse)
def create_post(post:Post, user: str = Depends(get_current_user)):
    db = db_load()
    post_id = str(uuid4())
    new_post = {"id": post_id, "title": post.title, "content": post.content, "owner": user}
    db["posts"].append(new_post)
    db_save(db)
    return new_post
@app.get("/posts/", response_model=List[PostResponse])
def get_post():
    db = db_load()
    return db["post"]
@app.get("/posts/{postid}", response_model=Optional[PostResponse])
def get_post_id(postid: str):
    db = db_load()
    posts = db["posts"]
    for post in posts:
        if post["id"] == postid:
            return post
    raise HTTPException(status_code=404, detail="Post not found")