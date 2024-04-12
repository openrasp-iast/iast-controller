from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from ninja import Router, Schema
from rest_framework.authtoken.models import Token

from controller.services.jwt import create_jwt_token

router = Router()


class AuthItem(Schema):
    username: str
    password: str


@router.post("/login", auth=None)
def login_request(request, auth: AuthItem):
    user = authenticate(request, username=auth.username, password=auth.password)
    if user is not None:
        token = create_jwt_token(user.id)
        return {
            "description": "Login successful",
            "status": 0,
            "data": {"token": token},
        }
    else:
        return {"description": "Invalid credentials", "status": 1}


@router.get("/logout")
def logout_request(request):
    logout(request)
    return {"description": "Logout successful", "status": 0}


@router.get("/islogin")
def islogin(request):
    return {"data": {}, "description": "ok", "status": 0}


@router.api_operation(["GET", "POST"], "/default")
def default(request):
    return {
        "data": {
            "is_default": True,
        },
        "description": "ok",
        "status": 0,
    }


@router.post("/update")
def update(request):
    return {"data": {}, "description": "ok", "status": 0}
