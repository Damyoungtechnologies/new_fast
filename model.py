from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String)
    firstname = Column(String)
    middle = Column(String)
    gender = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    status = Column(Boolean, default=True)

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    products = relationship("Products", back_populates="category")
class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    desc = Column(String)
    cat_id = Column(Integer, ForeignKey("category.id"))
    price = Column(Float)
    stock = Column(Integer)
    
    category = relationship("Category", back_populates="products")
class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("users.id"))
    