from fastapi import FastAPI, Header, Form, status, HTTPException
from enum import Enum
from pydantic import BaseModel, Field

app = FastAPI()
@app.get("/user")
async def get_user(user_agent:str | None = Header(None)):
    return{"user_agent": user_agent}
@app.get("/auth")
async def auth(token:str = Header(..., min_length=10)): 
    return{"token": token}

class token(str, Enum):
    first="1"
    second="2"
    third="3"
class valid(BaseModel):
    # password: str = Field(..., pattern=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    password: str = Field(...)

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def login(Token: token = Header(..., alias="X-Token"), username: str = Form(..., min_length=3, pattern="^[A-Za-z]+$"), firstname: str = Form(..., min_length= 5, pattern="^[a-zA-Z]+$"), middlename: str = Form(None), gender: str = Form("male", min_length=4, max_length=6), dob:str = Form(...), email: str = Form(pattern="^[a-z0-9]+@example\.com$"), phone: str = Form(...,max_length=11), password: valid = Form(...)):
    if (any(c.isalpha() for c in password) and any(c.digit() for c in password) and len(password) >= 8):
        if not Token:
            raise HTTPException(status_code=404, detail="Invalid token, please enter a valid token")
        return "Profile successfully created"
    raise HTTPException(status_code=400, detail="Invalid password")
 