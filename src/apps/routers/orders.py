from fastapi import Depends, APIRouter, HTTPException
from apps.database import get_db
from sqlalchemy.orm import Session
from apps.models import Order
from apps.schemas import orderCreate, orderResponse
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/add", response_model=orderResponse, summary="Add item to orders", description="Endpoint to add an item to the user's orders")
def add_to_orders(order_item: orderCreate):
    # Here you would typically add logic to add the item to the user's orders in the database
    # For demonstration purposes, we'll just return the order item data
    return {"id": 1, "user_id": order_item.user_id, "product_id": order_item.product_id, "quantity": order_item.quantity, "total_amount": order_item.total_amount, "status": order_item.status}


@router.post("/create", response_model=orderResponse, summary="Create new order", description="Endpoint to create a new order")
def create_order(order_item: orderCreate, db: Session = Depends(get_db)):

    order_item = Order(user_id=order_item.user_id, product_id=order_item.product_id, quantity=order_item.quantity, total_amount=order_item.total_amount, status=order_item.status)
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item

@router.get("/{user_id}", response_model=list[orderResponse], summary="Get orders by user ID", description="Endpoint to retrieve all orders for a specific user")
def get_orders_by_user_id(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders

@router.put("/{order_id}", summary="Update order by ID", description="Endpoint to update an order by its ID")
def update_order(order_id: int, order_item: orderCreate, db: Session = Depends(get_db)):
    db_order_item = db.query(Order).filter(Order.id == order_id).first()
    if not db_order_item:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order_item.user_id = order_item.user_id
    db_order_item.product_id = order_item.product_id
    db_order_item.quantity = order_item.quantity
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

@router.delete("/{order_id}", summary="Delete order by ID", description="Endpoint to delete an order by its ID")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order_item = db.query(Order).filter(Order.id == order_id).first()
    if not db_order_item:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order_item)
    db.commit()
    return {"message": "Order deleted successfully"}


