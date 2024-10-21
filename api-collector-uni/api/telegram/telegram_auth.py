from fastapi import Depends, APIRouter
from python_telegram_auth import verify_auth_data


router_test = APIRouter(
    prefix="/tg",
    tags=["Tg"],
)

def get_current_user(token: str = Depends(verify_auth_data)):
    user_id = verify_auth_data(token)
    return user_id


@router_test.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello, user {user['user_id']}!"}
