from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def get_auth():
    """Endpoint for authentication. Returns a message indicating the authentication endpoint."""
    return {"message": "Authentication endpoint"}