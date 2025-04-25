from fastapi import FastAPI
from enum import Enum
app = FastAPI()

class AvailableCuisines(str, Enum):
    indian = "indian"
    american = "american"
    italian = "italian"
    
food_items = {
    "indian" : ["Samosa", "Dosa"],
    "american": ["Hot Dog", "Apple Pie"],
    "italian":["Ravioli", "Pizza"]
}
valid_cuisines = food_items.keys()
# @app.get("/home/{name}")
# async def hello(name):
#     return f"hello to fastapi {name}"


@app.get("/get_food_items/{cuisine}")
async def food(cuisine: AvailableCuisines): 
    return food_items.get(cuisine)


coupons = {
    1: "10%",
    2: "20%",
    3: "30%"
}
@app.get("/get_coupons/{code}")
async def mycoupon(code:int):
    return(f"Discount price: ", coupons.get(code))