# 
from fastapi import Depends, FastAPI
from apps.database import SessionLocal, engine, Base,get_db
from sqlalchemy.orm import Session
from apps.models import User, Product, Order, Cart
from apps import models
from apps.routers import auth, products, orders, cart
Base.metadata.create_all(bind=engine)
app=FastAPI()



@app.get("/")
def read_root():
    return {"message": "E-commerce API is running!"}

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)
# @app.post("/users/")
# def create_user(db: Session = Depends(get_db)):
#     user = User(username="testing", email="saikiran@gmail.com", password=2345)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return {"user_id": user.id, "username": user.username, "email": user.email}

# with engine.connect() as connection:
#     result = connection.execute(text("SELECT 1"))
#     print(result.fetchone())

