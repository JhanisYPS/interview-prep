from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.dependencies import get_session
from schemas.schemas import OrderSchema
from models.models import Order

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def get_orders():
    """Endpoint for retrieving the list of orders. Returns a message indicating the orders endpoint."""
    return {"message": "List of orders"}

@order_router.post("/create_order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user_id=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return{"message": "order created id {}".format(new_order.id)}
