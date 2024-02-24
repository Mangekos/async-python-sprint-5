from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from core.security import (
    create_jwt_token,
    oauth2_scheme,
    pwd_context,
    verify_jwt_token,
)
from db.db import create_user, find_user_by_name

router_auth = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await find_user_by_name(decoded_data["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user


@router_auth.post("/register")
async def register(request: Request, name, password):
    user = await find_user_by_name(name)
    if user is not None:
        return Response(status_code=409)
    await create_user(name, pwd_context.hash(password))
    return Response(status_code=201)


@router_auth.post("/auth")
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await find_user_by_name(form_data.username)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    is_password_correct = pwd_context.verify(
        form_data.password, user.hash_password
    )
    if not is_password_correct:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    jwt_token = create_jwt_token({"sub": user.name})
    return {"access_token": jwt_token, "token_type": "bearer"}
