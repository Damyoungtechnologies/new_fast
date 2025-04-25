from fastapi import FastAPI, Depends, status, Path, HTTPException
from sqlalchemy.orm import Session, joinedload
import model
from sqlalchemy import or_
from database import engine
from model import User, Category, Products, Orders
from typing import Annotated, Literal
from database import engine, SessionLocal
from pydantic import BaseModel, Field

app = FastAPI()
model.Base.metadata.create_all(bind=engine)

def get_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close() 

class Customer(BaseModel):
    lastname: str
    firstname: str
    middle: str | None = None
    gender: Literal['male', 'female']
    email: str
    phone: str

class ExtraCustomer(Customer):
    status: bool | None

dbDependency = Annotated[Session,Depends(get_db)]   
@app.get('/')
async def getAll(db:dbDependency):
    list = db.query(User).order_by(User.firstname).all()
    cust = []
    for a in list:
        cust.append({'Surname':a.lastname, 'Middle Name': a.middle, 'First Name': a.firstname, 'Gender': a.gender, 'Email Address': a.email, 'Phone Number': a.phone, 'status': a.status})
    return cust

@app.get('/getAllActiveCustomers/')
async def getAllActiveCustomers(db:dbDependency):
    list = db.query(User).order_by(User.firstname).filter(User.status == True).all()
    return list  

@app.get('/getAllDeletedCustomers/')
async def getAllDeletedCustomers(db:dbDependency):
    list = db.query(User).order_by(User.firstname).filter(or_(User.status == False, User.status.is_(None))
    ).all()
    cust = []
    for a in list:
        if a.status == False or a.status == None:
            cust.append({'Surname':a.lastname, 'Middle Name': a.middle, 'First Name': a.firstname, 'Gender': a.gender, 'Email Address': a.email, 'Phone Number': a.phone, 'status': a.status})
    return cust

@app.get("/getUser/{user_id}", status_code=200)
async def getCustomer(db:dbDependency, user_id:int=Path(...,gt=0)):
    customer = db.query(User).filter(User.id==user_id).first()
    if customer is not None:
        return customer
    raise HTTPException(status_code=404, detail='Customer Not Found')

@app.post('/create', status_code=status.HTTP_201_CREATED)
async def create(db:dbDependency, cust: Customer):
    newCust = User(**cust.dict())
    db.add(newCust)
    db.commit()

@app.put('/updateCustomer/{user_id}', status_code=204)
async def updateCustomer(db:dbDependency, custRequest:Customer, user_id:int=Path(gt=0)):
    customer = db.query(User).filter(User.id==user_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")
    customer.email = custRequest.email
    customer.lastname = custRequest.lastname
    customer.firstname = custRequest.firstname
    customer.middle = custRequest.middle
    customer.phone = custRequest.phone
    customer.gender = custRequest.gender
    db.add(customer)
    db.commit()

@app.delete("/deleteUser/{user_id}", status_code=204)
async def deleteUser(db:dbDependency, user_id:int=Path(gt=0)):
    customer = db.query(User).filter(User.id==user_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer Not Found")
    customer.status = False
    db.add(customer)
    db.commit()

# The next is the category ID
class CategoryModel(BaseModel):
    name: str

@app.post("/createCategory", status_code=201)
async def createCategory(db:dbDependency, cat:CategoryModel):
    newCategory = Category(**cat.dict())
    db.add(newCategory)
    db.commit()

# The next is the product section
class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    desc: str | None = Field(..., min_length=3, max_length=50)
    cat_id: int | None = Field(..., gt=0)
    price: float = Field(..., gt=0)
    stock: int = Field(..., gt=0)

@app.post("/createProduct", status_code=status.HTTP_201_CREATED)
async def createProduct(db:dbDependency, prod:Product):
    newProduct = Products(**prod.dict())
    db.add(newProduct)
    db.commit()
    return "Product Created Successfully"

@app.get("/getAllProducts", status_code=status.HTTP_200_OK)
async def getAllProducts(db:dbDependency):
    products = db.query(Products).order_by(Products.name).options(joinedload(Products.category)).all()
    allProducts = []
    for product in products:
        print(product)
        allProducts.append({'Product Name':product.name, 'Product Description':product.desc, 'Product Price': product.price, 'Product Quantity': product.stock, 'Product Category':product.category.name})
    return allProducts
    
# This is to count the number of products in each category
@app.get("/ProductsPerCategory", status_code=status.HTTP_200_OK)
async def ProductsPerCategory(db:dbDependency):
    products = db.query(Products).order_by(Products.name).options().all()
    electronicCount = 0
    clothingCount = 0
    foodstuffCount = 0
    for product in products:
        if product.cat_id == 1:
            electronicCount += 1
        if product.cat_id == 2:
            clothingCount += 1
        if product.cat_id == 3:
            foodstuffCount += 1
    Products_Per_Category = {"electronics":electronicCount, "clothing":clothingCount, "foodstuff":foodstuffCount}  
    return Products_Per_Category
    
