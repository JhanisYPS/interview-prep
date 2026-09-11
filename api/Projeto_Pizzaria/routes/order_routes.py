from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def get_orders():
    """Endpoint for retrieving the list of orders. Returns a message indicating the orders endpoint."""
    return {"message": "List of orders"}