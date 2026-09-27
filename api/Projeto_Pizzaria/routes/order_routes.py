from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.dependencies import get_session, verify_token
from schemas.schemas import OrderSchema
from models.models import Order, User

order_router = APIRouter(prefix="/order", tags=["order"], dependencies = [Depends(verify_token)])

@order_router.get("/")
async def get_orders():
    """Endpoint for retrieving the list of orders. Returns a message indicating the orders endpoint."""
    return {"message": "List of orders"}

@order_router.post("/create_order")
async def create_order(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    new_order = Order(user_id=user.id)
    session.add(new_order)
    session.commit()
    return{"message": "order created id {}".format(new_order.id)}

@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()

    if not order:
        raise HTTPException(status_code=400, detail="order not found")
    elif order.user_id != user.id and not user.admin:
        raise HTTPException(status_code=401, detail="not Authorized")
    
    order.status = "CANCELADO"
    session.commit()
    return {
        "message": f"order cancel id {order.id}",
        "order": order
        }

@order_router.get("/orders")
async def get_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="not Authorized")
    else:
        orders = session.query(Order).all()
        return {
            "orders": orders
        }
