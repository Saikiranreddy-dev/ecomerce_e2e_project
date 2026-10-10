from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.schemas import cartCreate, cartResponse
from apps.models import Cart
router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)

# @router.post("/add", response_model=cartResponse, summary="Add item to cart", description="Endpoint to add an item to the user's cart")
# def add_to_cart(cart_item: cartCreate):
#     # Here you would typically add logic to add the item to the user's cart in the database
#     # For demonstration purposes, we'll just return the cart item data
#     return {"id": 1, "user_id": cart_item.user_id, "product_id": cart_item.product_id, "quantity": cart_item.quantity}


@router.post("/add", response_model=cartResponse, summary="Add item to cart", description="Endpoint to add an item to the user's cart")
def add_to_cart(cart_item: cartCreate,db: Session = Depends(get_db)):
    cart_item = Cart(user_id=cart_item.user_id, product_id=cart_item.product_id, quantity=cart_item.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.get("/{user_id}", response_model=list[cartResponse], summary="Get cart items by user ID", description="Endpoint to retrieve all cart items for a specific user")
def get_cart_items_by_user_id(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="No cart items found for this user")
    return cart_items
@router.put("/{cart_id}", summary="Update cart item by ID", description="Endpoint to update a cart item by its ID")
def update_cart_item(cart_id: int, cart_item: cartCreate, db: Session = Depends(get_db)):
    db_cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db_cart_item.user_id = cart_item.user_id
    db_cart_item.product_id = cart_item.product_id
    db_cart_item.quantity = cart_item.quantity
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item
@router.delete("/{cart_id}", summary="Delete cart item by ID", description="Endpoint to delete a cart item by its ID")
def delete_cart_item(cart_id: int, db: Session = Depends(get_db)):
    db_cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(db_cart_item)
    db.commit()
    return {"message": "Cart item deleted successfully"}