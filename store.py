import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from uuid import uuid4
app = FastAPI()

# JSON  file database
DB_FILE = "database.json"
def load_db():
    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return{"post": [], "users": {}}
    
def save_db(db):
    with open(DB_FILE, "w") as file:
        json.dump(db, file, indent=4)
        
@app.post("/signup/")
def signup(username: str, password: str):
    db = load_db()
    users = db.get("users", {})  
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[username] = password
    db["users"] = users
    save_db(db)   
    return {"message": "User created successfully"}    

def get_current_user(username: str, password: str):
    db = load_db()
    users = db.get("users", {})
    for user, user_password in users.items():
        if username == user and password == user_password:
            return user
    raise HTTPException(status_code=401, detail="Invalid password")

class Post (BaseModel):
    title : Optional[str] = Field(None)
    content: Optional[str] = Field(None)
class PostResponse(Post):
    id: str
    owner: str

@app.post("/posts/", response_model=PostResponse)
def create_post(post: Post, user: str = Depends(get_current_user)):
    db = load_db()
    post_id = str(uuid4())
    new_post = {"id":post_id, "title":post.title, "content":post.content, "owner":user}
    db["posts"].append(new_post)
    save_db(db)
    return new_post

# this gets all post
@app.get("/posts/", response_model=list[PostResponse])
def get_post():
    db = load_db()
    return db["posts"]

# this gets a single post using id

# @app.get("/posts/{post_id}", response_model=Optional[PostResponse])
# def get_single_post(post_id: str):
#     db = load_db()
#     posts = db["posts"]
#     for post in posts:
#         if post["id"] == post_id:
#             return post
#     raise HTTPException(status_code=404, detail="Post not found")

@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: str):
    db = load_db()
    post = next((p for p in db["posts"] if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: str, updated_post: Post, user: str = Depends(get_current_user)):
    db = load_db()
    post = next((p for p in db["posts"] if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post["owner"] != user:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    if updated_post.title:
        post["title"] = updated_post.title
    if updated_post.content:
        post["content"] = updated_post.content
    save_db(db)
    return post