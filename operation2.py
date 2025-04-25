import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import uuid4
app = FastAPI()
DB_Record = "record.json"
def db_load():
    try:
        with open(DB_Record) as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return {"users": {}, "book1": []}
        
def save_load(db):
    try:
        with open(DB_Record, "w") as file:
            return json.dump(db, file, indent=4)
    except(FileNotFoundError, json.JSONDecodeError):
        return {"users": {}, "book1": []}
    
class Post(BaseModel):  
    # id:str = Field(..., min_length=1)
    title: str = Field(...)
    author: str = Field(None)
    description: str | None = Field(None)
    rating: int | None = Field(None, ge=0, le=5)
    owner: str | None = Field(None)
  
class Post_authorization(Post):
    owner: str = Field(...,min_length=5)
    password: str = Field(...,min_length=8)  
    
@app.post("/signup/")
async def signup(owner: str, password: str):
    db = db_load()
    user = db.get("users", {})
    if owner in user.keys():
        raise HTTPException(status_code=400, detail="Username already in use")
    else:
        user[owner] = password
        db["users"]
        save_load(db)
        return ("Username created successfully")

@app.post("/post_book/")
async def update_book_by_title(username:str, post:Post):
    db = db_load()
    user = db.get("users", {})
    if username in user.keys():
            books = db.get("book1", [])
            if post.id in [book["id"] for book in books]:
                raise HTTPException(status_code=400, detail="Book ID already in use")
            else:
                post_id = str(uuid4())
                book = {"id": post_id, "title": post.title, "description": post.description, "owner": username}
                books.append(book)
                db["book1"] = books
                save_load(db) 
                return ("Book created successfully")
      
   
@app.get("/")
async def my_books():
    db = db_load()
    return db["book1"]
@app.get("/get_all_books_by_id/{id}")
async def my_books_by_id(id:int):
    db = db_load()
    for book in db["book1"]:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/get_all_books_by_rating/{rating}")
async def my_books_by_rating(rating:int):
    books = db_load()
    for book in books["book1"]:
        if book["rating"] == rating:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
@app.put("/update_book_by_title/{id}/{title}")
async def update_book_by_title(id: int, title: str):
    db = db_load()
    for book in db["book1"]:
        if book["id"] == id:
            book["title"] = title
            db["book1"].append(book)
            save_load(db) 
            return book
    raise HTTPException(status_code=404, detail="Unknown book")
@app.delete("/delete_book/{id}")
async def delete_book(id:int):
    db = db_load()
    for index, book in enumerate(db["book1"]):
        if book["id"] == id:
            del db["book1"][index]
            return {"message": "Book deleted"}
        raise HTTPException(status_code=404, detail="Delete not successful")
