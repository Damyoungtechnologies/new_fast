from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from uuid import uuid4
app = FastAPI()
books = {
    "users": {
        "sam": 279845,
        "joe": 189294
    },
    "book1": [{"id": 1,
              "title": "Attitude is everything", 
              "author": "Brian Tracy", 
              "description": "This book talks about the importance of positive attitude in the community, place of work and in the family",
              "rating": 5,
              "owner": "sam"
            },
            {"id": 2,
              "title": "Attitude is everything", 
              "author": "Brian Tracy", 
              "description": "This book talks about the importance of positive attitude in the community, place of work and in the family",
              "rating": 1,
              "owner": "joe"
            },
            {"id": 3,
              "title": "Attitude is everything", 
              "author": "Brian Tracy", 
              "description": "This book talks about the importance of positive attitude in the community, place of work and in the family",
              "rating": 5,
              "owner": "sam"
            },
            {"id": 4,
              "title": "Attitude is everything", 
              "author": "Brian Tracy", 
              "description": "This book talks about the importance of positive attitude in the community, place of work and in the family",
              "rating": 3,
              "owner": "joe"
            },
            {"id": 5,
              "title": "Attitude is everything", 
              "author": "Brian Tracy", 
              "description": "This book talks about the importance of positive attitude in the community, place of work and in the family",
              "rating": 2,
              "owner": "joe"
            }
        ]
}

@app.get("/")
async def my_books():
    return books["book1"]
@app.get("/get_all_books_by_id/{id}")
async def my_books_by_id(id:int):
    for book in books["book1"]:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/get_all_books_by_rating/{rating}")
async def my_books_by_rating(rating:int):
    for book in books["book1"]:
        if book["rating"] == rating:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
@app.put("/update_book_by_title/{id}/{title}")
async def update_book_by_title(id: int, title: str):
    for book in books["book1"]:
        if book["id"] == id:
            book["title"] = title
            return book
    raise HTTPException(status_code=404, detail="Unknown book")
@app.delete("/delete_book/{id}")
async def delete_book(id:int):
    for index, book in enumerate(books["book1"]):
        if book["id"] == id:
            del books["book1"][index]
            return {"message": "Book deleted"}
        raise HTTPException(status_code=404, detail="Delete not successful")
