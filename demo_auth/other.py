import secrets
from typing import Annotated
from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix='/demo-auth')
security = HTTPBasic()

@router.get('/basic-auth/')
def basic_auth(credent: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {
        'message': 'Hello',
        'user': credent.username,
        'password': credent.password
    }

user = {
    'danil': '12345',
    'da': 'awda'
}

def get_user(credent: Annotated[HTTPBasicCredentials, Depends(security)]):
    error = HTTPException(status_code=401, detail='Лох')
    user_password = user.get(credent.username)
    if user_password is None:
        raise error
    if credent.username not in user:
        raise error
    if not secrets.compare_digest(credent.password, user_password):
        raise error
    return credent.username


@router.get('/basic-auth-user/')
def basic_auth_cred(auth_user: str = Depends(get_user)):
    return {
        'message': f'Hello {auth_user}',
        'user': auth_user,
    }